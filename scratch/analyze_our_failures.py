import os
import json
import glob
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

files = sorted(glob.glob('/home/rsouza/Projects/orbit_wars/docs/episodes/78*.json'))
print(f"Analyzing {len(files)} files...")

our_team = "Richardson Allan Ferreira De Souza"

results = []

for filepath in files:
    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            continue
            
    team_names = data.get('info', {}).get('TeamNames', [])
    if our_team not in team_names:
        continue
    our_idx = team_names.index(our_team)
    
    steps = data.get('steps', [])
    num_steps = len(steps)
    
    # Calculate our collisions and OOBs
    our_sun_collisions = 0
    our_planet_collisions = 0
    our_oob = 0
    our_fleets_launched = 0
    our_ships_launched = 0
    
    # Let's track active fleets
    active_fleets = {}
    
    for step_idx, step_data in enumerate(steps):
        obs = step_data[0]['observation']
        fleets = obs.get('fleets', [])
        
        # Track our launches
        action = step_data[our_idx].get('action', [])
        if action:
            for move in action:
                if len(move) >= 3:
                    our_fleets_launched += 1
                    our_ships_launched += move[2]
        
        current_fids = set()
        for f in fleets:
            fid, fowner, fx, fy, fangle, ffrom, fships = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
            if fowner == our_idx:
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
            
            # Check if out of bounds
            if last_pos[0] < 0 or last_pos[0] > 100 or last_pos[1] < 0 or last_pos[1] > 100:
                our_oob += 1
            else:
                # Check collision with sun
                d_sun = distance(last_pos, (50.0, 50.0))
                if d_sun < 6.0:  # Sun radius is 5.0 + small epsilon
                    our_sun_collisions += 1
                else:
                    # Check collision with planets
                    planets_obs = steps[step_idx][0]['observation'].get('planets', [])
                    collided_planet = False
                    for p in planets_obs:
                        p_pos = (p[2], p[3])
                        p_rad = p[4]
                        if distance(last_pos, p_pos) < p_rad + 0.1:
                            # If it's a planet collision but not the intended target
                            # In Orbit Wars, landing on any planet causes collision or landing
                            collided_planet = True
                            break
                    if collided_planet:
                        our_planet_collisions += 1
                        
    # Get final placement
    rewards = data.get('rewards', [])
    final_reward = rewards[our_idx] if our_idx < len(rewards) else -1
    
    # Calculate final planets and ships
    final_obs = steps[-1][0]['observation']
    final_planets = 0
    final_ships = 0
    for p in final_obs.get('planets', []):
        if p[1] == our_idx:
            final_planets += 1
            final_ships += p[5]
    for f in final_obs.get('fleets', []):
        if f[1] == our_idx:
            final_ships += f[6]
            
    results.append({
        'match': os.path.basename(filepath),
        'steps': num_steps,
        'reward': final_reward,
        'fleets_launched': our_fleets_launched,
        'ships_launched': our_ships_launched,
        'oob': our_oob,
        'sun_collisions': our_sun_collisions,
        'planet_collisions': our_planet_collisions,
        'final_planets': final_planets,
        'final_ships': final_ships
    })

import pandas as pd
df = pd.DataFrame(results)
print("\n" + "="*80)
print("                    STATISTICAL REPORT ON NEW KAGGLE LOSSES")
print("="*80)
print(df.to_string(index=False))
print("-"*80)
print(f"Mean Steps:             {df['steps'].mean():.2f}")
print(f"Mean Fleets Launched:   {df['fleets_launched'].mean():.2f}")
print(f"Mean Ships Launched:    {df['ships_launched'].mean():.2f}")
print(f"Mean OOB Fleets:        {df['oob'].mean():.2f}")
print(f"Mean Sun Collisions:    {df['sun_collisions'].mean():.2f}")
print(f"Mean Planet Collisions: {df['planet_collisions'].mean():.2f}")
print(f"Mean Final Planets:     {df['final_planets'].mean():.2f}")
print(f"Mean Final Ships:       {df['final_ships'].mean():.2f}")
print("="*80)
