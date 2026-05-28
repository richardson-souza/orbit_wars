import json
from kaggle_environments import make

def check_reproducibility(episode_id, expected_seed):
    with open(f"docs/episodes/{episode_id}.json") as f:
        episode = json.load(f)
    json_initial = episode["steps"][0][0]["observation"]["initial_planets"]
    
    # 2. Get number of agents from the episode
    num_agents = len(episode["steps"][0])
    print(f"Episode {episode_id} is a {num_agents}-player match.")
    
    # 3. Create local env with the exact seed and number of agents
    # In kaggle_environments, we can set number of agents by passing a list of mock agents of that length.
    mock_agents = ["random"] * num_agents
    env = make("orbit_wars", configuration={"seed": expected_seed})
    env.reset(num_agents)
    env_initial = env.steps[0][0]["observation"]["initial_planets"]
    
    match = json_initial == env_initial
    print(f"Seed matches directly? {match}")
    if not match:
        print("JSON initial count:", len(json_initial))
        print("Env initial count:", len(env_initial))
        print("JSON first 3:", json_initial[:3])
        print("Env first 3:", env_initial[:3])

print("--- Testing 77834940 with seed 0 ---")
check_reproducibility(77834940, 0)

print("\n--- Testing 77837891 with seed 973728955 ---")
check_reproducibility(77837891, 973728955)
