import json
import os
import glob
import math
from collections import defaultdict

def analyze_all_episodes():
    episode_files = glob.glob("docs/episodes/*.json")
    print(f"Found {len(episode_files)} episode files to analyze.\n")
    
    results = []
    
    for filepath in sorted(episode_files):
        filename = os.path.basename(filepath)
        with open(filepath) as f:
            try:
                episode = json.load(f)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                continue
                
        steps = episode.get("steps", [])
        rewards = episode.get("rewards", [0, 0])
        statuses = episode.get("statuses", ["DONE", "DONE"])
        info = episode.get("info", {})
        
        team_names = info.get("TeamNames", ["Unknown", "Unknown"])
        
        # Identify our player index
        our_indices = []
        for idx, name in enumerate(team_names):
            if "Richardson" in name or "rsouza" in name:
                our_indices.append(idx)
                
        is_self_play = len(our_indices) == 2
        
        if not our_indices:
            # Fallback check if our name is not in team names (maybe it's main.py vs starter or something)
            our_indices = [0] # default to 0
            is_self_play = False
            
        print(f"File: {filename} | Teams: {team_names} | Our Indices: {our_indices} | Rewards: {rewards}")
        
        # Metrics to collect for each player
        fleets_launched = defaultdict(int)
        ships_launched = defaultdict(int)
        oob_fleets = defaultdict(int)
        sun_collisions = defaultdict(int)
        planet_collisions = defaultdict(int)
        
        # We can track the fleets that existed
        # fleet_id -> (owner, from_planet_id, ships, last_seen_pos)
        active_fleets = {}
        
        for s_idx, step in enumerate(steps):
            obs = step[0]["observation"]
            fleets = obs.get("fleets", [])
            planets = obs.get("planets", [])
            
            # Count actions
            for p_idx in [0, 1]:
                act = step[p_idx].get("action")
                if act:
                    for move in act:
                        if isinstance(move, list) and len(move) >= 3:
                            fleets_launched[p_idx] += 1
                            ships_launched[p_idx] += move[2]
            
            # Trace fleets to detect OOB and collisions
            # In Orbit Wars:
            # - If a fleet is in step s_idx, and disappears in step s_idx+1:
            # - We can check why:
            #   - Did it hit a planet? (Check if the planet's garrison changed or owner changed, or check if it was close to a planet)
            #   - Did it hit the sun? (Check if its path crossed the sun)
            #   - Did it go out of bounds? (Check if its next step would be outside 100x100)
            # Let's use a simpler heuristic for tracking where fleets end up
            current_fleet_ids = set()
            for f in fleets:
                fid, owner, fx, fy, angle, from_planet, fships = f
                current_fleet_ids.add(fid)
                active_fleets[fid] = {
                    "owner": owner,
                    "pos": (fx, fy),
                    "angle": angle,
                    "ships": fships,
                    "last_step": s_idx
                }
                
            # If a fleet was in active_fleets, but is not in current_fleet_ids, and its last_step was s_idx-1:
            # it was removed in this step. Let's see why:
            for fid, f_data in list(active_fleets.items()):
                if fid not in current_fleet_ids and f_data["last_step"] == s_idx - 1:
                    # It was removed. Let's analyze why:
                    owner = f_data["owner"]
                    fx, fy = f_data["pos"]
                    ang = f_data["angle"]
                    ships = f_data["ships"]
                    
                    # Estimate next position
                    # speed
                    speed = 1.0
                    if ships > 1:
                        log_ratio = math.log(ships) / math.log(1000.0)
                        speed = 1.0 + 5.0 * max(0.0, log_ratio) ** 1.5
                        speed = min(speed, 6.0)
                        
                    next_x = fx + speed * math.cos(ang)
                    next_y = fy + speed * math.sin(ang)
                    
                    # Check OOB
                    if next_x < 0 or next_x > 100 or next_y < 0 or next_y > 100:
                        oob_fleets[owner] += 1
                    # Check Sun collision
                    elif math.sqrt((next_x - 50.0)**2 + (next_y - 50.0)**2) < 10.0:
                        sun_collisions[owner] += 1
                    else:
                        planet_collisions[owner] += 1
                        
                    f_data["last_step"] = -999 # mark as processed
                    
        # Let's count final planets and ships
        last_step = steps[-1]
        last_obs = last_step[0]["observation"]
        final_planets = defaultdict(int)
        final_ships = defaultdict(int)
        for p in last_obs.get("planets", []):
            final_planets[p[1]] += 1
            final_ships[p[1]] += p[5]
            
        for f in last_obs.get("fleets", []):
            final_ships[f[1]] += f[6]
            
        results.append({
            "filename": filename,
            "team_names": team_names,
            "our_indices": our_indices,
            "is_self_play": is_self_play,
            "rewards": rewards,
            "statuses": statuses,
            "steps": len(steps),
            "fleets_launched": dict(fleets_launched),
            "ships_launched": dict(ships_launched),
            "oob_fleets": dict(oob_fleets),
            "sun_collisions": dict(sun_collisions),
            "planet_collisions": dict(planet_collisions),
            "final_planets": dict(final_planets),
            "final_ships": dict(final_ships)
        })
        
    # Write summary report to scratch/episodes_summary.json
    with open("docs/episodes/summary.json", "w") as out:
        json.dump(results, out, indent=2)
        
    print("\n========================================")
    print("            SUMMARY REPORT")
    print("========================================")
    for r in results:
        name = r["filename"]
        rewards = r["rewards"]
        steps = r["steps"]
        if r["is_self_play"]:
            print(f"{name:15s} | Self-Play | Steps: {steps:3d} | Rewards: {rewards}")
        else:
            our_idx = r["our_indices"][0]
            our_reward = rewards[our_idx]
            opp_idx = 1 - our_idx
            opp_reward = rewards[opp_idx]
            opp_name = r["team_names"][opp_idx]
            outcome = "WIN 🚀" if our_reward > opp_reward else ("LOSS ⚠️" if our_reward < opp_reward else "DRAW 🤝")
            print(f"{name:15s} | VS {opp_name[:20]:20s} | {outcome} | Our reward: {our_reward:2d} | Opp reward: {opp_reward:2d} | Steps: {steps:3d}")

if __name__ == "__main__":
    analyze_all_episodes()
