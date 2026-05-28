import json

def check_initial_p18(filepath):
    with open(filepath) as f:
        episode = json.load(f)
    obs = episode["steps"][0][0]["observation"]
    p18_init = next(p for p in obs["initial_planets"] if p[0] == 18)
    p18_step15 = next(p for p in episode["steps"][15][0]["observation"]["planets"] if p[0] == 18)
    print(f"P18 initial_planets: {p18_init}")
    print(f"P18 at step 15:       {p18_step15}")

check_initial_p18("docs/episodes/77834940.json")
