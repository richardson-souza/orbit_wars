import os
import math
import numpy as np
from typing import List, Dict, Any, Union
from strategies.base_strategy import BaseStrategy
from core.observation import ParsedObservation, Planet, Fleet
from core.physics import distance, get_planet_position_at_step

class PPOAgent(BaseStrategy):
    """
    Kaggle-compliant PPO Agent that loads a trained Stable-Baselines3 model
    and uses localized relative target-neighborhood states to make real-time decisions.
    """

    def __init__(self, model_path: str = "models/ppo_orbit_wars.zip"):
        self.model_path = model_path
        self.model = None

        if os.path.exists(model_path):
            from stable_baselines3 import PPO
            try:
                self.model = PPO.load(model_path)
                print(f"PPO model loaded successfully from {model_path}.")
            except Exception as e:
                print(f"Warning: Failed to load PPO model from {model_path}: {e}")
        else:
            print(f"Warning: PPO model {model_path} not found. Operating in fallback mode.")

    def _extract_features(self, obs: ParsedObservation, from_planet: Planet) -> np.ndarray:
        # Filter out from_planet itself
        targets = [p for p in obs.all_planets.values() if p.id != from_planet.id]

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
                if target.owner == obs.player:
                    owner_val = 0.0
                elif target.owner == -1:
                    owner_val = 0.5
                else:
                    owner_val = 1.0

                # Orbiting verification
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
                features.extend([0.0] * 7)

        return np.array(features, dtype=np.float32)

    def _translate_nn_action(self, obs: ParsedObservation, from_planet: Planet, action: int) -> list:
        targets = [p for p in obs.all_planets.values() if p.id != from_planet.id]
        targets.sort(key=lambda t: distance((from_planet.x, from_planet.y), (t.x, t.y)))

        if action >= len(targets):
            return []

        target = targets[action]
        ships_to_send = int(from_planet.ships * 0.75)
        if ships_to_send < 5:
            return []

        # Predict target position at step + 1
        try:
            target_pos = get_planet_position_at_step(
                target.id, obs.step + 1, obs.initial_planets, obs.angular_velocity
            )
        except ValueError:
            target_pos = (target.x, target.y)

        angle = math.atan2(target_pos[1] - from_planet.y, target_pos[0] - from_planet.x)
        return [[from_planet.id, angle, ships_to_send]]

    def get_actions(self, observation: Union[Dict[str, Any], Any]) -> List[List[Union[int, float]]]:
        obs = ParsedObservation(observation)
        if not obs.my_planets:
            return []

        # Focus on our strongest planet
        obs.my_planets.sort(key=lambda p: p.ships, reverse=True)
        best_planet = obs.my_planets[0]

        if best_planet.ships < 10:
            return []

        # Fallback behaviour if no SB3 model is trained/loaded
        if self.model is None:
            # Let's perform a simple rule-based action (attack the closest non-owned planet)
            targets = [p for p in obs.all_planets.values() if p.id != best_planet.id and p.owner != obs.player]
            if not targets:
                return []
            targets.sort(key=lambda t: distance((best_planet.x, best_planet.y), (t.x, t.y)))
            closest = targets[0]
            angle = math.atan2(closest.y - best_planet.y, closest.x - best_planet.x)
            ships = int(best_planet.ships * 0.75)
            if ships >= 15:
                return [[best_planet.id, angle, ships]]
            return []

        # 1. Extract localized neighbourhood state
        obs_vector = self._extract_features(obs, best_planet)

        # 2. Query PPO neural policy
        action, _state = self.model.predict(obs_vector, deterministic=True)

        # 3. Translate neural index to Kaggle action
        return self._translate_nn_action(obs, best_planet, int(action))
