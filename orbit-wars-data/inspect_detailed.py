import json
import math

def inspect_match_details(filepath):
    print(f"\n========================================\nINSPECTING DETAILS: {filepath}\n========================================")
    with open(filepath) as f:
        episode = json.load(f)
        
    steps = episode["steps"]
    
    # Let's inspect step 0 observation
    obs0 = steps[0][0]["observation"]
    print("Player ID:", obs0.get("player"))
    print("Angular Velocity:", obs0.get("angular_velocity"))
    
    initial_planets = obs0.get("initial_planets", [])
    print(f"Number of initial planets: {len(initial_planets)}")
    for p in initial_planets:
        p_id, owner, x, y, radius, ships, prod = p
        if owner != -1:
            print(f"Initial Owned Planet: ID={p_id}, Owner={owner}, Pos=({x}, {y}), Ships={ships}, Prod={prod}")
            
    # Let's find all planets in step 0
    planets0 = obs0.get("planets", [])
    print(f"Number of planets in step 0: {len(planets0)}")
    
    # Let's print out the details of all targets (neutral planets) in step 0
    # to understand why our agent didn't target them.
    # Specifically, their distance from planet 12 (home of P0) and planet 15 (home of P1).
    p12_pos = None
    p15_pos = None
    for p in planets0:
        if p[0] == 12:
            p12_pos = (p[2], p[3])
        if p[0] == 15:
            p15_pos = (p[2], p[3])
            
    print(f"Planet 12 position: {p12_pos}")
    print(f"Planet 15 position: {p15_pos}")
    
    # Let's see the distances and details of other planets from 12 and 15
    distances_from_12 = []
    distances_from_15 = []
    
    for p in planets0:
        p_id, owner, x, y, radius, ships, prod = p
        if p_id == 12 or p_id == 15:
            continue
        dist_12 = math.sqrt((x - p12_pos[0])**2 + (y - p12_pos[1])**2)
        dist_15 = math.sqrt((x - p15_pos[0])**2 + (y - p15_pos[1])**2)
        distances_from_12.append((p_id, dist_12, ships, prod, x, y))
        distances_from_15.append((p_id, dist_15, ships, prod, x, y))
        
    distances_from_12.sort(key=lambda x: x[1])
    distances_from_15.sort(key=lambda x: x[1])
    
    print("\nClosest 10 planets to Planet 12 (P0's home):")
    for p_id, dist, ships, prod, x, y in distances_from_12[:10]:
        print(f"  ID={p_id:2d} | Dist={dist:5.1f} | Ships={ships:2d} | Prod={prod} | Pos=({x:5.1f}, {y:5.1f})")
        
    # Let's check which targets were valid.
    # In HeuristicScorer:
    # 1. Dist must be <= 55.0
    # 2. available_ships >= 25
    # 3. proposed_ships = max(target.ships + 2, int(available_ships * 0.75))
    # 4. proposed_ships = min(proposed_ships, available_ships - 5)
    # 5. proposed_ships > target.ships
    # 6. Does not intersect sun (x=50, y=50, r=10)
    # Let's see what happens step by step for P0 when it decides to launch
    
    # Let's trace steps where actions were taken:
    actions_p0 = []
    for s_idx, step in enumerate(steps):
        act = step[0].get("action")
        if act:
            actions_p0.append((s_idx, act, step[0]["observation"]))
            
    print(f"\n--- Actions P0 (Total: {len(actions_p0)}) ---")
    for s_idx, act, obs in actions_p0[:3]:
        print(f"Step {s_idx}: action={act}")
        # Let's print the state of planet 12 and the targeted planet
        planets = obs.get("planets", [])
        my_planet = next(p for p in planets if p[0] == 12)
        print(f"  Planet 12: ships={my_planet[5]}, prod={my_planet[6]}")
        # The target planet must be the one that is in the direction of the action
        # Let's calculate which planet it was based on the angle and position
        from_x, from_y = my_planet[2], my_planet[3]
        angle = act[0][1]
        ships_sent = act[0][2]
        
        # Let's print which planet this matches at arrival
        print(f"  Action: angle={angle:.3f}, ships={ships_sent}")

if __name__ == "__main__":
    inspect_match_details("docs/episodes/77834940.json")
