"""
Kaggle Notebook Self-Contained PPO Training Script.
This file bundles all dependencies (physics, observation parser, and gym environment wrapper)
into a single file that can be copied directly into a Kaggle Notebook cell.

Prerequisites in Kaggle Notebook (Run in a cell):
!pip install stable-baselines3 kaggle-environments
"""

import os
import math
import argparse
import numpy as np
import torch
try:
    import gymnasium as gym
except ImportError:
    import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from kaggle_environments import make

# ==============================================================================
# 1. CORE PHYSICS & OBSERVATION CLASSES (Inlined for Self-Containment)
# ==============================================================================

SUN_RADIUS = 10.5
CENTER = 50.0

def distance(p1, p2):
    if hasattr(p1, "x"):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def get_planet_position_at_step(planet_id: int, step: int, initial_planets: list, angular_velocity: float) -> tuple:
    if planet_id >= len(initial_planets):
        raise ValueError(f"Planet ID {planet_id} not found in initial planets.")
    
    init_data = initial_planets[planet_id]
    x0, y0 = init_data[2], init_data[3]
    
    # Calculate radius from sun
    dx = x0 - CENTER
    dy = y0 - CENTER
    r = math.sqrt(dx**2 + dy**2)
    
    if r < 1e-5:
        return (CENTER, CENTER)
        
    initial_angle = math.atan2(dy, dx)
    current_angle = initial_angle + angular_velocity * step
    
    x = CENTER + r * math.cos(current_angle)
    y = CENTER + r * math.sin(current_angle)
    return (x, y)


class Planet:
    def __init__(self, id: int, owner: int, x: float, y: float, radius: float, ships: int, production: int):
        self.id = id
        self.owner = owner
        self.x = x
        self.y = y
        self.radius = radius
        self.ships = ships
        self.production = production


class Fleet:
    def __init__(self, id: int, owner: int, x: float, y: float, ships: int, target_planet_id: int, step_created: int):
        self.id = id
        self.owner = owner
        self.x = x
        self.y = y
        self.ships = ships
        self.target_planet_id = target_planet_id
        self.step_created = step_created


class ParsedObservation:
    def __init__(self, obs: dict):
        self.player = obs.get("player", 0)
        self.step = obs.get("step", 0)
        self.angular_velocity = obs.get("angular_velocity", 0.0)
        self.initial_planets = obs.get("initial_planets", [])
        
        # Parse planets list
        self.all_planets = {}
        for p in obs.get("planets", []):
            planet = Planet(*p)
            self.all_planets[planet.id] = planet
            
        # Filter planets by owner
        self.my_planets = [p for p in self.all_planets.values() if p.owner == self.player]
        self.neutral_planets = [p for p in self.all_planets.values() if p.owner == -1]
        self.enemy_planets = [p for p in self.all_planets.values() if p.owner != self.player and p.owner != -1]
        
        # Parse fleets list
        self.all_fleets = {}
        for f in obs.get("fleets", []):
            fleet = Fleet(*f)
            self.all_fleets[fleet.id] = fleet
            
        # Filter fleets by owner
        self.my_fleets = [f for f in self.all_fleets.values() if f.owner == self.player]
        self.enemy_fleets = [f for f in self.all_fleets.values() if f.owner != self.player]

# ==============================================================================
# 2. GYM ENVIRONMENT WRAPPER
# ==============================================================================

def starter_agent(obs):
    moves = []
    player = obs.get("player", 0)
    planets = [Planet(*p) for p in obs.get("planets", [])]
    CENTER_VAL = 50.0
    ROTATION_RADIUS_LIMIT = 50.0

    static_targets = []
    for p in planets:
        orbital_r = math.sqrt((p.x - CENTER_VAL) ** 2 + (p.y - CENTER_VAL) ** 2)
        if orbital_r + p.radius >= ROTATION_RADIUS_LIMIT and p.owner != player:
            static_targets.append(p)

    my_planets = [p for p in planets if p.owner == player]
    for mp in my_planets:
        if mp.ships <= 0:
            continue
        closest = None
        min_dist = float("inf")
        for t in static_targets:
            dist = math.sqrt((mp.x - t.x) ** 2 + (mp.y - t.y) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest = t
        if closest is not None:
            angle = math.atan2(closest.y - mp.y, closest.x - mp.x)
            ships = mp.ships // 2
            if ships >= 20:
                moves.append([mp.id, angle, ships])
    return moves


class OrbitWarsGymEnv(gym.Env):
    def __init__(self, test_mode: bool = False, opponent_type: str = "starter"):
        super(OrbitWarsGymEnv, self).__init__()
        self.test_mode = test_mode
        self.opponent_type = opponent_type

        # Shape: 5 nearest targets * 7 features = 35 elements
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(35,), dtype=np.float32
        )

        # Action Space: 5 choices representing attacking the i-th nearest planet
        self.action_space = gym.spaces.Discrete(5)

        self.env = None
        self.last_kaggle_obs = None
        self.steps_count = 0

    def _extract_features(self, obs, from_planet: Planet) -> np.ndarray:
        player = obs.get("player", 0)
        planets_list = obs.get("planets", [])
        planets = [Planet(*p) if isinstance(p, list) else p for p in planets_list]

        # Filter out from_planet itself
        targets = [p for p in planets if p.id != from_planet.id]

        # Sort targets by Euclidean distance
        targets.sort(key=lambda t: distance((from_planet.x, from_planet.y), (t.x, t.y)))

        CENTER_VAL = 50.0
        ROTATION_RADIUS_LIMIT = 50.0

        features = []
        for i in range(5):
            if i < len(targets):
                target = targets[i]
                dist = distance((from_planet.x, from_planet.y), (target.x, target.y))
                dx = target.x - from_planet.x
                dy = target.y - from_planet.y

                # Owner normalization: Allied=0.0, Neutral=0.5, Enemy=1.0
                if target.owner == player:
                    owner_val = 0.0
                elif target.owner == -1:
                    owner_val = 0.5
                else:
                    owner_val = 1.0

                # Orbiting verification
                dx_c = target.x - CENTER_VAL
                dy_c = target.y - CENTER_VAL
                orb_r = math.sqrt(dx_c**2 + dy_c**2)
                is_orbiting = 1.0 if orb_r + target.radius < ROTATION_RADIUS_LIMIT else 0.0

                features.extend([
                    dist / 100.0,
                    dx / 100.0,
                    dy / 100.0,
                    target.ships / 100.0,
                    target.production / 5.0,
                    owner_val,
                    is_orbiting
                ])
            else:
                features.extend([0.0] * 7)

        return np.array(features, dtype=np.float32)

    def _translate_nn_action(self, obs, from_planet: Planet, action: int) -> list:
        planets_list = obs.get("planets", [])
        planets = [Planet(*p) if isinstance(p, list) else p for p in planets_list]

        # Find target candidates sorted by distance
        targets = [p for p in planets if p.id != from_planet.id]
        targets.sort(key=lambda t: distance((from_planet.x, from_planet.y), (t.x, t.y)))

        if action >= len(targets):
            return []

        target = targets[action]
        ships_to_send = int(from_planet.ships * 0.75)
        if ships_to_send < 5:
            return []

        # Predict target position at step + 1
        step = obs.get("step", 0)
        try:
            target_pos = get_planet_position_at_step(
                target.id, step + 1, obs.get("initial_planets", []), obs.get("angular_velocity", 0.0)
            )
        except ValueError:
            target_pos = (target.x, target.y)

        angle = math.atan2(target_pos[1] - from_planet.y, target_pos[0] - from_planet.x)
        return [[from_planet.id, angle, ships_to_send]]

    def reset(self, seed=None):
        if seed is not None:
            np.random.seed(seed)

        self.steps_count = 0

        if self.test_mode:
            return np.zeros((35,), dtype=np.float32), {}

        self.env = make("orbit_wars", debug=False)
        self.env.reset(num_agents=2)

        state = self.env.steps[0]
        self.last_kaggle_obs = state[0].observation

        planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        home = next((p for p in planets if p.owner == 0), None)

        if home is None:
            return np.zeros((35,), dtype=np.float32), {}

        obs_vector = self._extract_features(self.last_kaggle_obs, home)
        return obs_vector, {}

    def step(self, action):
        self.steps_count += 1

        if self.test_mode:
            return np.zeros((35,), dtype=np.float32), 0.0, True, False, {}

        opp_obs = self.env.steps[-1][1].observation
        opp_action = starter_agent(opp_obs)

        planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        home = next((p for p in planets if p.owner == 0), None)

        if home is None or home.ships < 10:
            our_action = []
        else:
            our_action = self._translate_nn_action(self.last_kaggle_obs, home, int(action))

        state = self.env.step([our_action, opp_action])
        self.last_kaggle_obs = state[0].observation

        reward = self._calculate_reward()
        done = self.env.done or self.steps_count >= 200

        curr_planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        my_planets = [p for p in curr_planets if p.owner == 0]

        if not my_planets:
            done = True
            obs_vector = np.zeros((35,), dtype=np.float32)
        else:
            my_planets.sort(key=lambda p: p.ships, reverse=True)
            obs_vector = self._extract_features(self.last_kaggle_obs, my_planets[0])

        return obs_vector, reward, done, False, {}

    def _calculate_reward(self) -> float:
        curr_planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        ally_ships = sum(p.ships for p in curr_planets if p.owner == 0)
        ally_prod = sum(p.production for p in curr_planets if p.owner == 0)
        enemy_ships = sum(p.ships for p in curr_planets if p.owner == 1)
        
        reward = (ally_ships + 5.0 * ally_prod) - 0.2 * enemy_ships
        return float(reward)

# ==============================================================================
# 3. HIGH PERFORMANCE TRAINING LOOP (CUDA & MULTIPROCESSING READY)
# ==============================================================================

if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(description="Kaggle Notebook High-Performance PPO Trainer.")
    parser.add_argument("--steps", type=int, default=500000, help="Number of training steps.")
    parser.add_argument("--envs", type=int, default=4, help="Number of parallel environments (use 2 or 4 in Kaggle CPU).")
    parser.add_argument("--save-path", type=str, default="/kaggle/working/ppo_orbit_wars.zip", help="Path to save weights in Kaggle output.")
    
    # Detect Jupyter / Kaggle / Colab kernel execution to prevent SystemExit: 2
    is_jupyter = any(x in sys.argv[0].lower() for x in ["kernel", "ipykernel", "colab"]) or any("kernel" in arg for arg in sys.argv)
    if is_jupyter:
        args = parser.parse_args(args=[])
    else:
        args = parser.parse_args()

    print("=" * 70)
    print("   KAGGLE ARENA: SELF-CONTAINED HIGH-PERFORMANCE PPO TRAINER")
    print("=" * 70)
    print(f"Target Timesteps:         {args.steps}")
    print(f"Parallel Worker Envs:     {args.envs} (SubprocVecEnv)")
    print(f"Output Weights Path:      {args.save_path}")

    # Determine hardware accelerator
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Hardware Accelerator:     {device.upper()}")
    if device == "cuda":
        print(f"GPU Model:                {torch.cuda.get_device_name(0)}")
    print("-" * 70)

    # Resolve output directory
    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)

    print("Spawning parallel environment instances...")
    env = make_vec_env(
        OrbitWarsGymEnv,
        n_envs=args.envs,
        seed=42,
        vec_env_cls=SubprocVecEnv
    )

    print("Configuring PPO Deep Policy model...")
    model = PPO(
        policy="MlpPolicy",
        env=env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        verbose=1,
        device=device,
        tensorboard_log=None
    )

    print("\nExecuting PyTorch training loop on Kaggle GPU/CPU...")
    try:
        model.learn(total_timesteps=args.steps)
        print("\nTraining completed successfully!")
    except KeyboardInterrupt:
        print("\nTraining cleanly interrupted by user. Saving current checkpoint...")

    # Save output
    model.save(args.save_path)
    print(f"Weights saved successfully! File is downloadable at: {args.save_path}")
    print("=" * 70)
