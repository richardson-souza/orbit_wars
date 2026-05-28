import json
import os
import math
from collections import defaultdict

def analyze_specific_losses():
    # We want to inspect:
    # 77836758.json (2p loss vs Pascal)
    # 77836781.json (2p loss vs Clifford Cheefoon)
    # 77837891.json (2p loss vs Cheong woon Kang)
    # 77835919.json (4p loss vs Adam Soltan)
    # 77836128.json (4p loss vs Quentin Garnier)
    # 77838235.json (4p loss vs Charles Coonce)
    
    loss_files = [
        "77836758.json",
        "77836781.json",
        "77837891.json",
        "77835919.json",
        "77836128.json",
        "77838235.json"
    ]
    
    for filename in loss_files:
        filepath = os.path.join("docs/episodes", filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath) as f:
            episode = json.load(f)
            
        steps = episode["steps"]
        rewards = episode["rewards"]
        info = episode.get("info", {})
        team_names = info.get("TeamNames", [])
        
        # Identify our player index
        our_idx = -1
        for idx, name in enumerate(team_names):
            if "Richardson" in name:
                our_idx = idx
                break
        if our_idx == -1:
            our_idx = 0
            
        # Identify winner
        winner_idx = rewards.index(max(rewards))
        
        print(f"\n========================================\nLOSS FILE: {filename} | VS {team_names[winner_idx]} (Winner)\n========================================")
        print(f"Total Steps: {len(steps)} | Our Index: {our_idx} | Winner Index: {winner_idx}")
        
        # Trace timelines
        our_planets_timeline = []
        winner_planets_timeline = []
        our_ships_timeline = []
        winner_ships_timeline = []
        
        for s_idx, step in enumerate(steps):
            obs = step[0]["observation"]
            planets = obs.get("planets", [])
            
            our_p_cnt = 0
            winner_p_cnt = 0
            our_s_cnt = 0
            winner_s_cnt = 0
            
            for p in planets:
                p_id, owner, px, py, r, ships, prod = p
                if owner == our_idx:
                    our_p_cnt += 1
                    our_s_cnt += ships
                elif owner == winner_idx:
                    winner_p_cnt += 1
                    winner_s_cnt += ships
                    
            our_planets_timeline.append(our_p_cnt)
            winner_planets_timeline.append(winner_p_cnt)
            our_ships_timeline.append(our_s_cnt)
            winner_ships_timeline.append(winner_s_cnt)
            
        print(f"Timeline:")
        print(f"  Step 0:   Our Planets={our_planets_timeline[0]}, Winner Planets={winner_planets_timeline[0]}")
        print(f"  Step 50:  Our Planets={our_planets_timeline[50] if len(steps)>50 else 'N/A'}, Winner Planets={winner_planets_timeline[50] if len(steps)>50 else 'N/A'}")
        print(f"  Step 100: Our Planets={our_planets_timeline[100] if len(steps)>100 else 'N/A'}, Winner Planets={winner_planets_timeline[100] if len(steps)>100 else 'N/A'}")
        print(f"  Final:    Our Planets={our_planets_timeline[-1]}, Winner Planets={winner_planets_timeline[-1]}")
        
        # Actions analysis
        our_launches = []
        winner_launches = []
        
        for s_idx, step in enumerate(steps):
            our_act = step[our_idx].get("action")
            winner_act = step[winner_idx].get("action")
            
            if our_act:
                for move in our_act:
                    our_launches.append((s_idx, move))
            if winner_act:
                for move in winner_act:
                    winner_launches.append((s_idx, move))
                    
        print(f"\nFleet launch stats:")
        print(f"  Our total fleets: {len(our_launches)} | Total ships sent: {sum(m[1][2] for m in our_launches)}")
        if our_launches:
            sizes = [m[1][2] for m in our_launches]
            print(f"  Our fleet size: Min={min(sizes)}, Max={max(sizes)}, Avg={sum(sizes)/len(sizes):.1f}")
            
        print(f"  Winner total fleets: {len(winner_launches)} | Total ships sent: {sum(m[1][2] for m in winner_launches)}")
        if winner_launches:
            sizes = [m[1][2] for m in winner_launches]
            print(f"  Winner fleet size: Min={min(sizes)}, Max={max(sizes)}, Avg={sum(sizes)/len(sizes):.1f}")
            
        # Detect why we lost:
        # 1. Did we get completely wiped out? (Final planets == 0)
        # 2. Or did we lose by ship count?
        if our_planets_timeline[-1] == 0:
            # Wiped out! When did we lose all planets?
            wiped_step = our_planets_timeline.index(0)
            print(f"\nOutcome: Wiped out at step {wiped_step}!")
            
            # Let's inspect the step where we lost our last planet
            # What happened in the turns leading to wiped_step?
            # Let's look at steps around wiped_step
            print(f"  Context around step {wiped_step}:")
            for offset in range(max(0, wiped_step - 5), min(len(steps), wiped_step + 1)):
                obs = steps[offset][0]["observation"]
                our_planets = [p for p in obs.get("planets", []) if p[1] == our_idx]
                winner_planets = [p for p in obs.get("planets", []) if p[1] == winner_idx]
                our_fleets = [f for f in obs.get("fleets", []) if f[1] == our_idx]
                winner_fleets = [f for f in obs.get("fleets", []) if f[1] == winner_idx]
                print(f"    Step {offset:3d}: Our Planets={len(our_planets)} ({sum(p[5] for p in our_planets)} ships), Winner Planets={len(winner_planets)} ({sum(p[5] for p in winner_planets)} ships)")
                print(f"              Our Fleets={len(our_fleets)} ({sum(f[6] for f in our_fleets)} ships), Winner Fleets={len(winner_fleets)} ({sum(f[6] for f in winner_fleets)} ships)")
        else:
            print(f"\nOutcome: Ended by step limit. Ships: Ours={our_ships_timeline[-1]}, Winner={winner_ships_timeline[-1]}")
            
        # Let's look at the winner's first 5 actions to see their strategy
        print("\nWinner's first 5 launches:")
        for s, move in winner_launches[:5]:
            print(f"  Step {s:3d}: {move}")

if __name__ == "__main__":
    analyze_specific_losses()
