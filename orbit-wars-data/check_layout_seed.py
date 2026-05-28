import json
from kaggle_environments import make

def check_seed():
    episode_id = 77834940
    with open(f"docs/episodes/{episode_id}.json") as f:
        episode = json.load(f)
    json_initial = episode["steps"][0][0]["observation"]["initial_planets"]
    
    # Try using episode ID as seed
    env = make("orbit_wars", configuration={"seed": episode_id})
    env.reset()
    env_initial = env.steps[0][0]["observation"]["initial_planets"]
    
    match = json_initial == env_initial
    print(f"Seed matches directly? {match}")
    if not match:
        print("JSON initial count:", len(json_initial))
        print("Env initial count:", len(env_initial))
        print("JSON first 3:", json_initial[:3])
        print("Env first 3:", env_initial[:3])

check_seed()
