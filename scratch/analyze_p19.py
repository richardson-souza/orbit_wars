import json
import math

filepath = '/home/rsouza/Projects/orbit_wars/docs/episodes/78160692.json'
with open(filepath, 'r') as f:
    data = json.load(f)

team_names = data.get('info', {}).get('TeamNames', [])
our_team = "Richardson Allan Ferreira De Souza"
our_idx = team_names.index(our_team)
steps = data.get('steps', [])

print(f"Tracing P19 around step 83...")
for s in range(78, 86):
    obs = steps[s][0]['observation']
    planets = obs.get('planets', [])
    fleets = obs.get('fleets', [])
    
    p19 = next((p for p in planets if p[0] == 19), None)
    if p19:
        owner_name = team_names[p19[1]] if p19[1] != -1 else "Neutral"
        print(f"Step {s:3d} | P19 Owner: {owner_name} | Ships: {p19[5]} | Prod: {p19[6]}")
    else:
        print(f"Step {s:3d} | P19 not found!")
        
    # Incoming fleets specifically close to P19
    for f in fleets:
        fid, fowner, fx, fy, fangle, ffrom, fships = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
        if p19:
            d = math.sqrt((fx - p19[2])**2 + (fy - p19[3])**2)
            if d < 10.0:
                f_owner_name = team_names[fowner] if fowner != -1 else "Neutral"
                print(f"         Fleet{fid}(owner={f_owner_name}, ships={fships}, dist={d:.2f})")
                
    # Actions
    for p_idx, team in enumerate(team_names):
        act = steps[s][p_idx].get('action', [])
        if act:
            # check if any action targets or starts from P19
            # wait, in kaggle-environments, moves are list of moves: [from_id, angle, ships]
            # to check if it's from P19: move[0] == 19
            p19_moves = [move for move in act if move[0] == 19]
            if p19_moves:
                print(f"         {team} Action from P19: {p19_moves}")
