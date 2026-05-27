import math
import numpy as np
try:
    import gymnasium as gym
except ImportError:
    import gym

from kaggle_environments import make
from core.observation import ParsedObservation, Planet, Fleet
from core.physics import distance, get_planet_position_at_step

# Baseline starter agent importable here
def starter_agent(obs):
    moves = []
    player = obs.get("player", 0)
    planets = [Planet(*p) for p in obs.get("planets", [])]
    CENTER = 50.0
    ROTATION_RADIUS_LIMIT = 50.0

    static_targets = []
    for p in planets:
        orbital_r = math.sqrt((p.x - CENTER) ** 2 + (p.y - CENTER) ** 2)
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
    """
    Gym/Gymnasium Environment wrapper for Orbit Wars.
    Uses localized neighborhood relative features (K=5 nearest planets)
    and a discrete action space to facilitate high-speed PPO training.
    """

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
        initial_planets = obs.get("initial_planets", [])
        angular_velocity = obs.get("angular_velocity", 0.0)

        # Map to Planet objects
        planets = [Planet(*p) if isinstance(p, list) else p for p in planets_list]

        # Filter out from_planet itself and owned planets
        targets = [p for p in planets if p.id != from_planet.id and p.owner != player]

        # Sort targets by Euclidean distance
        targets.sort(key=lambda t: distance((from_planet.x, from_planet.y), (t.x, t.y)))

        CENTER = 50.0
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
                # Check if it rotates
                dx_c = target.x - CENTER
                dy_c = target.y - CENTER
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
                # Padding for less than 5 planets
                features.extend([0.0] * 7)

        return np.array(features, dtype=np.float32)

    def _translate_nn_action(self, obs, from_planet: Planet, action: int) -> list:
        player = obs.get("player", 0)
        planets_list = obs.get("planets", [])
        planets = [Planet(*p) if isinstance(p, list) else p for p in planets_list]

        # Find target candidates sorted by distance (filter out owned planets)
        targets = [p for p in planets if p.id != from_planet.id and p.owner != player]
        targets.sort(key=lambda t: distance((from_planet.x, from_planet.y), (t.x, t.y)))

        if action >= len(targets):
            return []

        target = targets[action]
        ships_to_send = int(from_planet.ships * 0.75)
        if ships_to_send < 5:
            return []

        # Predict target position at step + 1 to target accurately
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

        # Reset actual Kaggle Environment
        self.env = make("orbit_wars", debug=False)
        self.env.reset(num_agents=2)

        # Get initial state
        state = self.env.steps[0]
        self.last_kaggle_obs = state[0].observation

        # Initialize tracking metrics for differential reward
        planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        self.prev_ally_ships = sum(p.ships for p in planets if p.owner == 0)
        self.prev_ally_prod = sum(p.production for p in planets if p.owner == 0)
        self.prev_enemy_ships = sum(p.ships for p in planets if p.owner == 1)

        # Find our home planet (owned by player 0)
        home = next((p for p in planets if p.owner == 0), None)

        if home is None:
            # Fallback
            return np.zeros((35,), dtype=np.float32), {}

        obs_vector = self._extract_features(self.last_kaggle_obs, home)
        return obs_vector, {}

    def step(self, action):
        self.steps_count += 1

        if self.test_mode:
            return np.zeros((35,), dtype=np.float32), 0.0, True, False, {}

        # 1. Get opponent's action (starter agent baseline)
        opp_obs = self.env.steps[-1][1].observation
        opp_action = starter_agent(opp_obs)

        # 2. Get our action
        planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        home = next((p for p in planets if p.owner == 0), None)

        if home is None or home.ships < 10:
            our_action = []
        else:
            our_action = self._translate_nn_action(self.last_kaggle_obs, home, int(action))

        # 3. Step environment
        state = self.env.step([our_action, opp_action])
        self.last_kaggle_obs = state[0].observation

        # 4. Calculate reward
        reward = self._calculate_reward()

        # Check if done
        done = self.env.done or self.steps_count >= 200

        # Find our home planet again (or any planet we own)
        curr_planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        my_planets = [p for p in curr_planets if p.owner == 0]

        if not my_planets:
            done = True
            obs_vector = np.zeros((35,), dtype=np.float32)
        else:
            # Focus on our strongest planet
            my_planets.sort(key=lambda p: p.ships, reverse=True)
            obs_vector = self._extract_features(self.last_kaggle_obs, my_planets[0])

        return obs_vector, reward, done, False, {}

    def _calculate_reward(self) -> float:
        # Stationary Differential Reward: reward changes in state metrics
        curr_planets = [Planet(*p) for p in self.last_kaggle_obs["planets"]]
        
        ally_ships = sum(p.ships for p in curr_planets if p.owner == 0)
        ally_prod = sum(p.production for p in curr_planets if p.owner == 0)
        enemy_ships = sum(p.ships for p in curr_planets if p.owner == 1)
        
        # Calculate deltas since previous turn
        delta_ally_ships = ally_ships - self.prev_ally_ships
        delta_ally_prod = ally_prod - self.prev_ally_prod
        delta_enemy_ships = enemy_ships - self.prev_enemy_ships
        
        # Combine deltas into stationary step reward
        reward = delta_ally_ships + 10.0 * delta_ally_prod - 0.2 * delta_enemy_ships
        
        # Win/Loss terminal bonuses
        if enemy_ships == 0 and ally_ships > 0:
            reward += 100.0
        elif ally_ships == 0 and enemy_ships > 0:
            reward -= 100.0
            
        # Update trackers for next step
        self.prev_ally_ships = ally_ships
        self.prev_ally_prod = ally_prod
        self.prev_enemy_ships = enemy_ships
        
        return float(reward)
