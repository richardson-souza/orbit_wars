import json
import glob
import os

def find_all_seeds():
    paths = glob.glob("docs/episodes/*.json")
    for filepath in sorted(paths):
        with open(filepath) as f:
            data = json.load(f)
        episode_id = os.path.basename(filepath).replace(".json", "")
        # Get info.seed
        info = data.get("info", {})
        seed = info.get("seed")
        print(f"Episode: {episode_id} -> info.seed = {seed}")

find_all_seeds()
