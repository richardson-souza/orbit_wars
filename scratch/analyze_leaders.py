import os
import json
import glob
import math
import numpy as np
import pandas as pd

files = sorted(glob.glob('/home/rsouza/Projects/orbit_wars/docs/episodes/78*.json'))
print(f"Analyzing {len(files)} Kaggle Leader replays...")

fleet_sizes = []
massive_attack_steps = {}
evacuation_ticks = []

for filepath in files:
    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except Exception:
            continue
            
    team_names = data.get('info', {}).get('TeamNames', [])
    rewards = data.get('rewards', [])
    
    # Identify winner (1st place) and runner-up (2nd place)
    ranked_players = list(enumerate(rewards))
    ranked_players.sort(key=lambda x: x[1], reverse=True)
    
    leader_indices = [ranked_players[0][0], ranked_players[1][0]]
    match_name = os.path.basename(filepath)
    
    steps = data.get('steps', [])
    num_steps = len(steps)
    
    for l_idx in leader_indices:
        if l_idx >= len(team_names):
            continue
        leader_name = team_names[l_idx]
        
        # Track fleet sizes and massive attack steps
        first_massive_step = None
        
        # Track fleets step-by-step
        active_fleets = {}
        
        for step_idx, step_data in enumerate(steps):
            obs = step_data[0]['observation']
            fleets = obs.get('fleets', [])
            
            # Action taken by this leader
            action = step_data[l_idx].get('action', [])
            if action:
                for move in action:
                    if len(move) >= 3:
                        size = move[2]
                        fleet_sizes.append(size)
                        if size >= 50 and first_massive_step is None:
                            first_massive_step = step_idx
                            
            # Trajectory analysis to discover evacuation patterns
            current_fids = set()
            for f in fleets:
                fid, fowner, fx, fy, fangle, ffrom, fships = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
                if fowner == l_idx:
                    current_fids.add(fid)
                    if fid not in active_fleets:
                        active_fleets[fid] = {
                            'spawn_step': step_idx,
                            'ships': fships,
                            'coords': [(fx, fy)]
                        }
                    else:
                        active_fleets[fid]['coords'].append((fx, fy))
                        
            # Check terminated fleets
            terminated = set(active_fleets.keys()) - current_fids
            for fid in list(terminated):
                f_info = active_fleets.pop(fid)
                last_pos = f_info['coords'][-1]
                
                # If a leader's fleet landed on their OWN planet and it was an evacuation?
                # Usually evacuations happen when a planet has very high enemy fleets targeting it.
                # Let's check steps preceding this to see if an enemy was approaching.
                pass
                
        if first_massive_step is not None:
            if leader_name not in massive_attack_steps:
                massive_attack_steps[leader_name] = []
            massive_attack_steps[leader_name].append(first_massive_step)

# Compute analytics
fleet_sizes = np.array(fleet_sizes)
print("\n" + "="*80)
# Use humble, direct phrasing as per guidelines
print("                  TOP 10 LEADER FLEET SIZING ANALYSIS")
print("="*80)
print(f"Total Fleets Analyzed:       {len(fleet_sizes)}")
print(f"Mean Fleet Size:             {np.mean(fleet_sizes):.2f} ships")
print(f"Median Fleet Size (50%):     {np.median(fleet_sizes):.2f} ships")
print(f"Percentile 75%:              {np.percentile(fleet_sizes, 75):.2f} ships")
print(f"Percentile 90% (Massive):    {np.percentile(fleet_sizes, 90):.2f} ships")
print(f"Min Fleet Size:              {np.min(fleet_sizes)} ships")
print(f"Max Fleet Size:              {np.max(fleet_sizes)} ships")
print("="*80)

# Time to attack
print("\n" + "="*80)
print("               TIME-TO-ATTACK (FIRST MASSIVE LAUNCH >= 50 SHIPS)")
print("="*80)
attack_data = []
for leader, steps_list in massive_attack_steps.items():
    attack_data.append({
        'Leader': leader,
        'Avg Step': np.mean(steps_list),
        'Min Step': np.min(steps_list),
        'Max Step': np.max(steps_list)
    })
df_attack = pd.DataFrame(attack_data)
df_attack.sort_values(by='Avg Step', inplace=True)
print(df_attack.to_string(index=False))
print("="*80)
