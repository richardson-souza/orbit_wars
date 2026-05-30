import json
import math

filepath = '/home/rsouza/Projects/orbit_wars/docs/episodes/78160692.json'
with open(filepath, 'r') as f:
    data = json.load(f)

team_names = data.get('info', {}).get('TeamNames', [])
our_team = "Richardson Allan Ferreira De Souza"
our_idx = team_names.index(our_team)

steps = data.get('steps', [])
elim_step = 105

print(f"Match: {filepath}")
print(f"Our Index: {our_idx} ({our_team})")
print(f"Leaderboard Teams: {team_names}")
print("-" * 100)

for s in range(40, 90):
    obs = steps[s][0]['observation']
    planets = obs.get('planets', [])
    fleets = obs.get('fleets', [])
    
    # Let's see our planets at step s
    our_planets = [p for p in planets if p[1] == our_idx]
    our_planets_str = ", ".join([f"P{p[0]}(ships={p[5]}, prod={p[6]})" for p in our_planets])
    
    # Active fleets targeting our planets
    incoming_fleets = []
    for f in fleets:
        fid, fowner, fx, fy, fangle, ffrom, fships = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
        # Check distance to our last planet (P8)
        p8 = next((p for p in planets if p[0] == 8), None)
        if p8:
            d = math.sqrt((fx - p8[2])**2 + (fy - p8[3])**2)
            if d < 15.0:
                owner_name = team_names[fowner] if fowner != -1 else "Neutral"
                incoming_fleets.append(f"Fleet{fid}(owner={owner_name}, ships={fships}, dist={d:.1f})")
                
    print(f"Step {s:3d} | Our Planets: [{our_planets_str}]")
    
    # Action taken by us in step s
    action = steps[s][our_idx].get('action', [])
    if action:
        print(f"         Our Action: {action}")
            
print("-" * 100)
