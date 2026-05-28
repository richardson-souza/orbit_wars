import json
import os
from collections import defaultdict

def analyze_wins():
    win_files = ["77837130.json", "77837345.json", "77837563.json"]
    for filename in win_files:
        filepath = os.path.join("docs/episodes", filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath) as f:
            episode = json.load(f)
            
        steps = episode["steps"]
        rewards = episode["rewards"]
        info = episode.get("info", {})
        team_names = info.get("TeamNames", [])
        
        our_idx = -1
        for idx, name in enumerate(team_names):
            if "Richardson" in name:
                our_idx = idx
                break
        if our_idx == -1:
            our_idx = 0
            
        print(f"\n========================================\nWIN FILE: {filename} | Our Index: {our_idx}\n========================================")
        print(f"Total Steps: {len(steps)}")
        
        our_planets_timeline = []
        opp_planets_timeline = []
        for s_idx, step in enumerate(steps):
            obs = step[0]["observation"]
            planets = obs.get("planets", [])
            our_cnt = sum(1 for p in planets if p[1] == our_idx)
            opp_cnt = sum(1 for p in planets if p[1] != -1 and p[1] != our_idx)
            our_planets_timeline.append(our_cnt)
            opp_planets_timeline.append(opp_cnt)
            
        print(f"Planet count timeline:")
        print(f"  Step 0:   Ours={our_planets_timeline[0]}, Opponents={opp_planets_timeline[0]}")
        print(f"  Step 50:  Ours={our_planets_timeline[50] if len(steps)>50 else 'N/A'}, Opponents={opp_planets_timeline[50] if len(steps)>50 else 'N/A'}")
        print(f"  Step 100: Ours={our_planets_timeline[100] if len(steps)>100 else 'N/A'}, Opponents={opp_planets_timeline[100] if len(steps)>100 else 'N/A'}")
        print(f"  Final:    Ours={our_planets_timeline[-1]}, Opponents={opp_planets_timeline[-1]}")
        
        our_launches = []
        for s_idx, step in enumerate(steps):
            our_act = step[our_idx].get("action")
            if our_act:
                for move in our_act:
                    our_launches.append((s_idx, move))
        
        print(f"Our fleets launched: {len(our_launches)}")
        if our_launches:
            sizes = [m[1][2] for m in our_launches]
            print(f"Our fleet size: Min={min(sizes)}, Max={max(sizes)}, Avg={sum(sizes)/len(sizes):.1f}")

if __name__ == "__main__":
    analyze_wins()
