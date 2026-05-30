import os
import json
import math
import glob
import pandas as pd
import numpy as np

CENTER = 50.0
ROTATION_RADIUS_LIMIT = 50.0

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def estimate_fleet_speed(num_ships):
    if num_ships <= 1:
        return 1.0
    log_ratio = math.log(num_ships) / math.log(1000.0)
    speed = 1.0 + 5.0 * max(0.0, log_ratio) ** 1.5
    return min(speed, 6.0)

def get_planet_position_at_step(planet_id, step, initial_planets, angular_velocity):
    planet = next((p for p in initial_planets if p[0] == planet_id), None)
    if planet is None:
        raise ValueError(f"Planet ID {planet_id} not found.")
    
    init_x, init_y, radius = planet[2], planet[3], planet[4]
    dx = init_x - CENTER
    dy = init_y - CENTER
    orbital_radius = math.sqrt(dx**2 + dy**2)
    
    if orbital_radius + radius < ROTATION_RADIUS_LIMIT:
        initial_angle = math.atan2(dy, dx)
        current_angle = initial_angle + angular_velocity * step
        new_x = CENTER + orbital_radius * math.cos(current_angle)
        new_y = CENTER + orbital_radius * math.sin(current_angle)
        return (new_x, new_y)
    return (init_x, init_y)

logs_path = '/home/rsouza/Projects/orbit_wars/docs/logs/*.json'
files = glob.glob(logs_path)
print(f"Loaded {len(files)} files.")

target_agent = 'typeIIIfairy'

tot_records = []
hoarding_records = []
evacuation_records = []

for file_idx, filepath in enumerate(files):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    team_names = data.get('info', {}).get('TeamNames', [])
    if target_agent not in team_names:
        continue
    target_idx = team_names.index(target_agent)
    
    steps = data.get('steps', [])
    initial_planets = steps[0][0]['observation']['initial_planets']
    angular_velocity = steps[0][0]['observation']['angular_velocity']
    
    active_fleets = {}
    all_fleets_history = []
    
    for step_idx, step_data in enumerate(steps):
        obs = step_data[0]['observation']
        current_fleets = obs.get('fleets', [])
        
        current_fleet_ids = set()
        for f in current_fleets:
            fid, fowner, fx, fy, fangle, ffrom, fships = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
            current_fleet_ids.add(fid)
            
            if fid not in active_fleets:
                active_fleets[fid] = {
                    'id': fid,
                    'owner': fowner,
                    'from_planet_id': ffrom,
                    'ships': fships,
                    'spawn_step': step_idx,
                    'trajectory': [(fx, fy)],
                    'angle': fangle
                }
            else:
                active_fleets[fid]['trajectory'].append((fx, fy))
                
        terminated_ids = set(active_fleets.keys()) - current_fleet_ids
        for fid in terminated_ids:
            fleet_info = active_fleets.pop(fid)
            fleet_info['landing_step'] = step_idx
            
            last_pos = fleet_info['trajectory'][-1]
            closest_planet = None
            min_dist = float('inf')
            
            planets_at_landing = steps[step_idx - 1][0]['observation']['planets']
            for p in planets_at_landing:
                pid, px, py = p[0], p[2], p[3]
                d = distance(last_pos, (px, py))
                if d < min_dist:
                    min_dist = d
                    closest_planet = pid
            
            if min_dist < 10.0:
                fleet_info['target_planet_id'] = closest_planet
                all_fleets_history.append(fleet_info)

    for step_idx, step_data in enumerate(steps):
        if step_idx == 0:
            continue
            
        action = step_data[target_idx].get('action', [])
        if not action:
            continue
            
        obs_before = steps[step_idx - 1][0]['observation']
        planets_before = obs_before.get('planets', [])
        
        planet_ships = {p[0]: p[5] for p in planets_before}
        planet_production = {p[0]: p[6] for p in planets_before}
        
        for move in action:
            if len(move) < 3:
                continue
            from_pid, angle, num_ships = move[0], move[1], move[2]
            
            if from_pid not in planet_ships:
                continue
            
            ships_before = planet_ships[from_pid]
            ships_left = ships_before - num_ships
            prod = planet_production[from_pid]
            ratio = ships_left / prod if prod > 0 else 0.0
            
            hoarding_records.append({
                'match': os.path.basename(filepath),
                'step': step_idx,
                'planet_id': from_pid,
                'ships_before': ships_before,
                'ships_launched': num_ships,
                'ships_left': ships_left,
                'production': prod,
                'ratio': ratio
            })
            
            matching_fleet = next((
                f for f in all_fleets_history 
                if f['owner'] == target_idx 
                and f['from_planet_id'] == from_pid 
                and f['spawn_step'] == step_idx
                and abs(f['ships'] - num_ships) <= 1
            ), None)
            
            if matching_fleet:
                spawn_step = matching_fleet['spawn_step']
                landing_step = matching_fleet['landing_step']
                target_pid = matching_fleet['target_planet_id']
                travel_turns = landing_step - spawn_step
                
                try:
                    pos_origin = get_planet_position_at_step(from_pid, spawn_step, initial_planets, angular_velocity)
                    pos_target_init = get_planet_position_at_step(target_pid, spawn_step, initial_planets, angular_velocity)
                except ValueError:
                    obs_at_spawn = steps[spawn_step][0]['observation']
                    planets_at_spawn = obs_at_spawn.get('planets', [])
                    p_from = next((p for p in planets_at_spawn if p[0] == from_pid), None)
                    p_tgt = next((p for p in planets_at_spawn if p[0] == target_pid), None)
                    if p_from is not None and p_tgt is not None:
                        pos_origin = (p_from[2], p_from[3])
                        pos_target_init = (p_tgt[2], p_tgt[3])
                    else:
                        continue
                
                dist_init = distance(pos_origin, pos_target_init)
                
                v = estimate_fleet_speed(num_ships)
                eta_euclid = dist_init / v
                
                tot_records.append({
                    'match': os.path.basename(filepath),
                    'step': step_idx,
                    'from_pid': from_pid,
                    'target_pid': target_pid,
                    'ships': num_ships,
                    'travel_turns': travel_turns,
                    'dist': dist_init,
                    'speed': v,
                    'eta_euclid': eta_euclid,
                    'tot_offset': travel_turns - eta_euclid
                })
            
            for f in all_fleets_history:
                if f['owner'] != target_idx and f['target_planet_id'] == from_pid:
                    if f['spawn_step'] <= step_idx < f['landing_step']:
                        ticks_to_impact = f['landing_step'] - step_idx
                        if ships_left <= 2:
                            evacuation_records.append({
                                'match': os.path.basename(filepath),
                                'step': step_idx,
                                'planet_id': from_pid,
                                'hostile_fleet_ships': f['ships'],
                                'ticks_to_impact': ticks_to_impact,
                                'ships_left': ships_left
                            })

df_tot = pd.DataFrame(tot_records)
df_hoarding = pd.DataFrame(hoarding_records)
df_evacuation = pd.DataFrame(evacuation_records)

print("="*60)
print("              REPLAY ANALYSIS STATISTICAL REPORT")
print("="*60)
print(f"Total files analyzed:         {len(files)}")
print(f"Total ToT/ETA samples:         {len(df_tot)}")
print(f"Total Hoarding samples:        {len(df_hoarding)}")
print(f"Total Evacuation samples:      {len(df_evacuation)}")
print("-"*60)

if not df_tot.empty:
    print("PROVA 1: Time-on-Target (ToT) / Travel Turns")
    print(df_tot['travel_turns'].describe())
    print(f"Median Travel Turns:           {df_tot['travel_turns'].median():.2f}")
    print(f"Mean Travel Turns:             {df_tot['travel_turns'].mean():.2f}")
    print("-"*60)

if not df_hoarding.empty:
    print("PROVA 2: Garrison Hoarding Ratio (ships_left / production)")
    df_filtered = df_hoarding[df_hoarding['ratio'] <= 35]
    print(df_filtered['ratio'].describe())
    print(f"Median Hoarding Ratio:         {df_filtered['ratio'].median():.2f}")
    print(f"Mode Hoarding Ratio (rounded): {df_filtered['ratio'].round().mode()[0]:.2f}")
    print("-"*60)

if not df_evacuation.empty:
    print("PROVA 3: Evacuation Ticks-to-Impact Window")
    print(df_evacuation['ticks_to_impact'].describe())
    print(f"Median Ticks to Impact:        {df_evacuation['ticks_to_impact'].median():.2f}")
    print(f"Mode Ticks to Impact:          {df_evacuation['ticks_to_impact'].mode()[0]:.2f}")
    print("="*60)
else:
    print("PROVA 3: Evacuation Ticks-to-Impact Window")
    print("No direct evacuations detected in the parsed logs.")
    print("="*60)
