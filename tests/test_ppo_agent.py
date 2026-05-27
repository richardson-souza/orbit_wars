import pytest
import math
import numpy as np
try:
    import gymnasium as gym
except ImportError:
    import gym

from core.observation import Planet
# We'll import these from the modules we're about to write:
# from core.ppo_env import OrbitWarsGymEnv
# from strategies.ppo_agent import PPOAgent

def test_gym_env_spaces():
    """TDD: Test that OrbitWarsGymEnv has correct Gym Spaces definition."""
    # We will import it inside the test so pytest loads it after we create the file
    from core.ppo_env import OrbitWarsGymEnv
    
    # Instantiate Gym Env in test mode
    env = OrbitWarsGymEnv(test_mode=True)
    
    assert isinstance(env.observation_space, gym.spaces.Box)
    assert env.observation_space.shape == (35,)
    
    assert isinstance(env.action_space, gym.spaces.Discrete)
    assert env.action_space.n == 5

def test_feature_extraction():
    """TDD: Test that observation feature extraction outputs correct localized vector."""
    from core.ppo_env import OrbitWarsGymEnv
    
    env = OrbitWarsGymEnv(test_mode=True)
    
    # Mock home planet at (50, 50) and target planets
    home = Planet(id=0, owner=0, x=50.0, y=50.0, radius=2.0, ships=100, production=1)
    
    # 5 target planets at various distances
    targets = [
        Planet(id=1, owner=-1, x=50.0, y=60.0, radius=1.5, ships=10, production=2),  # Dist 10.0
        Planet(id=2, owner=1, x=60.0, y=50.0, radius=2.0, ships=20, production=3),   # Dist 10.0
        Planet(id=3, owner=-1, x=50.0, y=30.0, radius=1.0, ships=5, production=1),   # Dist 20.0
        Planet(id=4, owner=0, x=50.0, y=80.0, radius=2.5, ships=50, production=2),   # Dist 30.0
        Planet(id=5, owner=1, x=90.0, y=50.0, radius=1.0, ships=15, production=1),   # Dist 40.0
    ]
    
    initial_planets = [
        [0, 0, 50.0, 50.0, 2.0, 100, 1],
        [1, -1, 50.0, 60.0, 1.5, 10, 2],
        [2, 1, 60.0, 50.0, 2.0, 20, 3],
        [3, -1, 50.0, 30.0, 1.0, 5, 1],
        [4, 0, 50.0, 80.0, 2.5, 50, 2],
        [5, 1, 90.0, 50.0, 1.0, 15, 1],
    ]
    
    # Mock observation dict
    mock_obs = {
        "player": 0,
        "step": 10,
        "angular_velocity": 0.0,
        "planets": [list(p) for p in [home] + targets],
        "initial_planets": initial_planets,
        "comet_planet_ids": [],
        "comets": [],
        "fleets": []
    }
    
    features = env._extract_features(mock_obs, home)
    
    assert len(features) == 35
    assert isinstance(features, np.ndarray)
    
    # The nearest target (Planet 1 or 2) should be represented in the first neighbourhood slot
    # Let's verify that the values are finite and within range
    assert np.all(np.isfinite(features))

def test_action_conversion():
    """TDD: Test that neural network action index maps correctly to Kaggle format."""
    from core.ppo_env import OrbitWarsGymEnv
    
    env = OrbitWarsGymEnv(test_mode=True)
    
    home = Planet(id=0, owner=0, x=50.0, y=50.0, radius=2.0, ships=100, production=1)
    targets = [
        Planet(id=1, owner=-1, x=50.0, y=60.0, radius=1.5, ships=10, production=2),  # Dist 10.0
        Planet(id=2, owner=1, x=60.0, y=50.0, radius=2.0, ships=20, production=3),
        Planet(id=3, owner=-1, x=50.0, y=30.0, radius=1.0, ships=5, production=1),
        Planet(id=4, owner=0, x=50.0, y=80.0, radius=2.5, ships=50, production=2),
        Planet(id=5, owner=1, x=90.0, y=50.0, radius=1.0, ships=15, production=1),
    ]
    
    mock_obs = {
        "player": 0,
        "step": 10,
        "angular_velocity": 0.0,
        "planets": [list(p) for p in [home] + targets],
        "initial_planets": [list(p) for p in [home] + targets],
        "comet_planet_ids": [],
        "comets": [],
        "fleets": []
    }
    
    # Test taking action 0 (attack 0-th nearest target which is Planet 1 or 2)
    kaggle_actions = env._translate_nn_action(mock_obs, home, action=0)
    
    assert len(kaggle_actions) == 1
    move = kaggle_actions[0]
    assert move[0] == 0  # from planet 0
    # Ships to send should be close to 75% of available (100 * 0.75 = 75)
    assert 70 <= move[2] <= 75
