import json
import math

def trace_p12(filepath):
    with open(filepath) as f:
        episode = json.load(f)
    steps = episode["steps"]
    
    # Let's print Planet 12 position and details from step 0 to 18
    for s in range(18):
        obs = steps[s][0]["observation"]
        p12 = next(p for p in obs["planets"] if p[0] == 12)
        print(f"Step {s:2d} | Planet 12 Pos: ({p12[2]:6.2f}, {p12[3]:6.2f}) | Ships: {p12[5]}")

trace_p12("docs/episodes/77834940.json")
