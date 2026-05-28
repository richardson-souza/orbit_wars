import json

def view_config(filepath):
    with open(filepath) as f:
        episode = json.load(f)
    print("Top-level keys:", list(episode.keys()))
    if "configuration" in episode:
        print("Configuration:", episode["configuration"])
    else:
        print("No top-level configuration key found.")
    
    # Check if there is config in the first step
    first_step = episode["steps"][0][0]
    print("First step keys:", list(first_step.keys()))
    if "observation" in first_step:
        obs = first_step["observation"]
        print("Observation keys:", list(obs.keys()))

view_config("docs/episodes/77834940.json")
