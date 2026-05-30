import os
import json
import glob
import math

files = sorted(glob.glob('/home/rsouza/Projects/orbit_wars/docs/episodes/78*.json'))
print(f"Analyzing {len(files)} files...")

our_team = "Richardson Allan Ferreira De Souza"

elimination_data = []

for filepath in files:
    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            continue
            
    team_names = data.get('info', {}).get('TeamNames', [])
    if our_team not in team_names:
        continue
    our_idx = team_names.index(our_team)
    
    steps = data.get('steps', [])
    num_steps = len(steps)
    
    elimination_step = None
    last_owned_planets = []
    
    # Track the last step where we owned at least one planet
    for step_idx in range(num_steps):
        obs = steps[step_idx][0]['observation']
        owned_planets = [p for p in obs.get('planets', []) if p[1] == our_idx]
        if owned_planets:
            elimination_step = step_idx
            last_owned_planets = owned_planets
            
    if elimination_step is not None and elimination_step < num_steps - 1:
        # We were eliminated before the end!
        next_step_obs = steps[elimination_step + 1][0]['observation']
        # See what happened to our last owned planets
        for lp in last_owned_planets:
            lp_id = lp[0]
            lp_ships = lp[5]
            # Check who owns it now
            now_p = next((p for p in next_step_obs.get('planets', []) if p[0] == lp_id), None)
            if now_p:
                new_owner = now_p[1]
                new_ships = now_p[5]
                owner_name = team_names[new_owner] if new_owner != -1 else "Neutral"
                elimination_data.append({
                    'match': os.path.basename(filepath),
                    'eliminated_at_step': elimination_step + 1,
                    'last_planet_id': lp_id,
                    'our_garrison_before': lp_ships,
                    'new_owner_name': owner_name,
                    'new_owner_ships': new_ships,
                    'total_match_steps': num_steps
                })
    else:
        # We survived to the end but lost!
        elimination_data.append({
            'match': os.path.basename(filepath),
            'eliminated_at_step': "Survived",
            'last_planet_id': last_owned_planets[0][0] if last_owned_planets else None,
            'our_garrison_before': last_owned_planets[0][5] if last_owned_planets else 0,
            'new_owner_name': "N/A",
            'new_owner_ships': 0,
            'total_match_steps': num_steps
        })

import pandas as pd
df_elim = pd.DataFrame(elimination_data)
print("\n" + "="*80)
print("                       ELIMINATION DETAIL ANALYSIS")
print("="*80)
print(df_elim.to_string(index=False))
print("="*80)
