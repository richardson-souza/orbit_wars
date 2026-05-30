import os
import json
import glob
import math

files = sorted(glob.glob('/home/rsouza/Projects/orbit_wars/docs/episodes/78*.json'))
our_team = "Richardson Allan Ferreira De Souza"

print(f"Loaded {len(files)} files for analysis...")

results = []

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
    num_players = len(team_names)
    
    # Let's reconstruct the scouting state machine
    opponent_tracker = {}
    for idx in range(num_players):
        if idx != our_idx:
            opponent_tracker[idx] = {"planets_captured": 0, "aggression_score": 0.0}
            
    prev_planet_owners = {}
    selected_profile = "standard"
    max_aggression_at_41 = 0.0
    opponent_scores_at_41 = {}
    
    for step_idx in range(num_steps):
        obs = steps[step_idx][0]['observation']
        step_val = obs.get('step', step_idx)
        
        # Track neutral captures for step < 40
        if step_val < 40:
            planets = obs.get('planets', [])
            for p in planets:
                pid, owner = p[0], p[1]
                prev_o = prev_planet_owners.get(pid, -1)
                if prev_o == -1 and owner != -1 and owner != our_idx:
                    if owner in opponent_tracker:
                        opponent_tracker[owner]["planets_captured"] += 1
                        
            # Update aggression score
            step_factor = max(1, step_val)
            for opp_id, opp_data in opponent_tracker.items():
                opp_data["aggression_score"] = opp_data["planets_captured"] / step_factor
                
        # Store owners for next step diffing
        planets = obs.get('planets', [])
        prev_planet_owners = {p[0]: p[1] for p in planets}
        
        # Capture state at step 41
        if step_val == 41:
            for opp_id, opp_data in opponent_tracker.items():
                opponent_scores_at_41[opp_id] = opp_data["aggression_score"]
            if opponent_tracker:
                max_aggression_at_41 = max([opp_data["aggression_score"] for opp_data in opponent_tracker.values()] + [0.0])
            else:
                max_aggression_at_41 = 0.0
            if max_aggression_at_41 > 0.15:
                selected_profile = "defensive"
            elif max_aggression_at_41 < 0.08:
                selected_profile = "aggressive"
            else:
                selected_profile = "standard"
                
    # Final stats
    rewards = data.get('rewards', [])
    placement = -1
    if rewards and our_idx < len(rewards):
        sorted_rewards = sorted(list(set(rewards)), reverse=True)
        our_reward = rewards[our_idx]
        placement = sorted_rewards.index(our_reward) + 1
        
    final_obs = steps[-1][0]['observation']
    final_planets = sum(1 for p in final_obs.get('planets', []) if p[1] == our_idx)
    final_ships = sum(p[5] for p in final_obs.get('planets', []) if p[1] == our_idx) + sum(f[6] for f in final_obs.get('fleets', []) if f[1] == our_idx)
    
    results.append({
        'match': os.path.basename(filepath),
        'placement': placement,
        'selected_profile': selected_profile,
        'max_aggression_at_41': max_aggression_at_41,
        'opponents': [team_names[i] for i in range(num_players) if i != our_idx],
        'opp_scores': {team_names[i]: opponent_scores_at_41.get(i, 0.0) for i in range(num_players) if i != our_idx},
        'final_planets': final_planets,
        'final_ships': final_ships,
        'total_steps': num_steps
    })

for r in sorted(results, key=lambda x: x['placement']):
    print("-" * 80)
    print(f"Match: {r['match']} | Result: Placement {r['placement']} | Total Steps: {r['total_steps']}")
    print(f"Selected Profile at Step 41: {r['selected_profile'].upper()} (Max Opponent Aggression: {r['max_aggression_at_41']:.3f})")
    print("Opponent Scores:")
    for opp, score in r['opp_scores'].items():
        print(f"  - {opp}: {score:.3f}")
    print(f"Our Final Standing: {r['final_planets']} planets, {r['final_ships']} ships")
