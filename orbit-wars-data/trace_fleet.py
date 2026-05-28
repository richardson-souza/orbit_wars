import json
import math

def trace_fleet(filepath):
    print(f"\n========================================\nTRACING FLEET: {filepath}\n========================================")
    with open(filepath) as f:
        episode = json.load(f)
        
    steps = episode["steps"]
    
    # Let's inspect step 16 and 17
    # Step 16 action is executed, so at step 17 the fleet should be in transit.
    # Each fleet: [id, owner, x, y, angle, from_planet_id, ships]
    for s in range(16, 30):
        step = steps[s]
        obs = step[0]["observation"]
        fleets = obs.get("fleets", [])
        planets = obs.get("planets", [])
        
        # P0 fleets
        p0_fleets = [f for f in fleets if f[1] == 0]
        p1_fleets = [f for f in fleets if f[1] == 1]
        
        print(f"Step {s:2d}:")
        print(f"  P0 Fleets: {p0_fleets}")
        print(f"  P1 Fleets: {p1_fleets}")
        
        # Check if any planet owner changed
        for p in planets:
            p_id, owner, px, py, r, ships, prod = p
            if p_id in [12, 15, 20, 24, 28, 16]:
                print(f"    Planet {p_id:2d}: Owner={owner}, Ships={ships}")

if __name__ == "__main__":
    trace_fleet("docs/episodes/77834940.json")
