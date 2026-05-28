import json
import math
from collections import defaultdict

def analyze_episode(filepath):
    print(f"\n========================================\nDETAILED ANALYSIS: {filepath}\n========================================")
    with open(filepath) as f:
        episode = json.load(f)
    
    steps = episode["steps"]
    rewards = episode.get("rewards", [0, 0])
    statuses = episode.get("statuses", ["DONE", "DONE"])
    
    print(f"Total steps in episode: {len(steps)}")
    print(f"Final rewards: {rewards}")
    print(f"Statuses: {statuses}")
    
    # Check if there is some header or metadata indicating player names
    # Sometimes it's in the first step or episode-level metadata
    print("Episode keys:", list(episode.keys()))
    if "info" in episode:
        print("Episode info:", episode["info"])
    
    # Let's inspect the first step
    first_step = steps[0]
    print("First step length:", len(first_step))
    for i, agent_step in enumerate(first_step):
        print(f"Agent {i} keys:", list(agent_step.keys()))
        if "action" in agent_step:
            print(f"Agent {i} initial action:", agent_step["action"])
        if "reward" in agent_step:
            print(f"Agent {i} initial reward:", agent_step["reward"])
        if "status" in agent_step:
            print(f"Agent {i} initial status:", agent_step["status"])
            
    # Let's analyze the game progression
    # We want to trace planet counts and total ships for each player at each step
    history = []
    
    for s_idx, step in enumerate(steps):
        obs = step[0]["observation"]
        planets = obs.get("planets", [])
        fleets = obs.get("fleets", [])
        
        # Count ships on planets and in fleets
        ships_on_planets = defaultdict(int)
        planets_count = defaultdict(int)
        for p in planets:
            p_id, owner, px, py, radius, ships, prod = p
            ships_on_planets[owner] += ships
            planets_count[owner] += 1
            
        ships_in_fleets = defaultdict(int)
        fleets_count = defaultdict(int)
        for f in fleets:
            f_id, owner, fx, fy, angle, from_planet, ships = f
            ships_in_fleets[owner] += ships
            fleets_count[owner] += 1
            
        history.append({
            "step": s_idx,
            "planets_count": dict(planets_count),
            "ships_on_planets": dict(ships_on_planets),
            "ships_in_fleets": dict(ships_in_fleets),
            "fleets_count": dict(fleets_count),
            "total_ships": {owner: ships_on_planets[owner] + ships_in_fleets[owner] for owner in [-1, 0, 1]}
        })
        
    # Let's print milestones:
    # 1. Initial state (step 0)
    # 2. Step 50
    # 3. Step 100
    # 4. Step 200
    # 5. Step 300
    # 6. Step 400
    # 7. Final step
    print("\n--- Milestones ---")
    milestones = [0, 50, 100, 150, 200, 250, 300, 350, 400, len(steps)-1]
    for m in milestones:
        if m < len(steps):
            h = history[m]
            print(f"Step {m:3d}:")
            print(f"  Planets Owned: P0: {h['planets_count'].get(0, 0)}, P1: {h['planets_count'].get(1, 0)}, Neutral: {h['planets_count'].get(-1, 0)}")
            print(f"  Total Ships:   P0: {h['total_ships'].get(0, 0)}, P1: {h['total_ships'].get(1, 0)}, Neutral: {h['total_ships'].get(-1, 0)}")
            print(f"  Fleets:        P0: {h['fleets_count'].get(0, 0)} ({h['ships_in_fleets'].get(0, 0)} ships), P1: {h['fleets_count'].get(1, 0)} ({h['ships_in_fleets'].get(1, 0)} ships)")

    # Analyze actions and rules in detail
    # Let's see who launched fleets, what size, and where.
    print("\n--- Detailed Action Patterns ---")
    for p_idx in [0, 1]:
        launches = []
        for s_idx, step in enumerate(steps):
            act = step[p_idx].get("action")
            if act:
                for move in act:
                    if isinstance(move, list) and len(move) >= 3:
                        from_id, angle, ships_count = move[0], move[1], move[2]
                        launches.append((s_idx, from_id, angle, ships_count))
        
        print(f"\nPlayer {p_idx}: Total actions={len(launches)}")
        if launches:
            print(f"  First 5 launches:")
            for s, fid, ang, cnt in launches[:5]:
                print(f"    Step {s}: From planet {fid}, angle={ang:.3f}, ships={cnt}")
            print(f"  Last 5 launches:")
            for s, fid, ang, cnt in launches[-5:]:
                print(f"    Step {s}: From planet {fid}, angle={ang:.3f}, ships={cnt}")
                
            # Fleet sizes distribution
            sizes = [l[3] for l in launches]
            print(f"  Fleet size - Min: {min(sizes)}, Max: {max(sizes)}, Avg: {sum(sizes)/len(sizes):.1f}")
            
    # Let's analyze why the loser lost.
    # In Orbit Wars, a player is eliminated or loses if they lose all planets.
    # Let's find out when the loser lost their home planet or all planets.
    for p_idx in [0, 1]:
        lost_all_step = None
        for s_idx, h in enumerate(history):
            if h['planets_count'].get(p_idx, 0) == 0:
                lost_all_step = s_idx
                break
        if lost_all_step is not None:
            print(f"\nPlayer {p_idx} lost all planets at step {lost_all_step}!")
        else:
            print(f"\nPlayer {p_idx} kept at least one planet throughout.")

if __name__ == "__main__":
    analyze_episode("docs/episodes/77835230.json")
    analyze_episode("docs/episodes/77834940.json")
