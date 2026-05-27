from strategies.ppo_agent import PPOAgent

# Initialize the PPO agent with our trained model weights
ppo_strategy = PPOAgent("models/ppo_orbit_wars.zip")

def agent(obs) -> list:
    return ppo_strategy.get_actions(obs)
