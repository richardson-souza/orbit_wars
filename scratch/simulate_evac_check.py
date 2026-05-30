import json
import math
from core.physics import get_planet_position_at_step

filepath = '/home/rsouza/Projects/orbit_wars/docs/episodes/78160692.json'
with open(filepath, 'r') as f:
    data = json.load(f)

steps = data.get('steps', [])
initial_planets = steps[0][0]['observation']['initial_planets']
angular_velocity = steps[0][0]['observation']['angular_velocity']

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def estimate_fleet_speed(num_ships):
    max_speed = 6.0
    if num_ships <= 1:
        return 1.0
    log_ratio = math.log(num_ships) / math.log(1000.0)
    speed = 1.0 + 5.0 * max(0.0, log_ratio) ** 1.5
    return min(speed, max_speed)

for s in [80, 81, 82]:
    obs = steps[s][0]['observation']
    planets = obs.get('planets', [])
    fleets = obs.get('fleets', [])
    
    mine = next((p for p in planets if p[0] == 19), None)
    if not mine:
        print(f"Step {s:3d}: P19 not found!")
        continue
        
    mine_id, mine_owner, mine_x, mine_y, mine_rad, mine_ships, mine_prod = mine[0], mine[1], mine[2], mine[3], mine[4], mine[5], mine[6]
    
    print(f"\nStep {s:3d} | P19 at ({mine_x:.2f}, {mine_y:.2f}) with {mine_ships} ships")
    
    for fleet in fleets:
        fid, fowner, fx, fy, fangle, ffrom, fships = fleet[0], fleet[1], fleet[2], fleet[3], fleet[4], fleet[5], fleet[6]
        if fid == 224:
            dist = distance((fx, fy), (mine_x, mine_y))
            speed = estimate_fleet_speed(fships)
            arr_step = s + int(math.ceil(dist / speed))
            
            # Precise landing calculation
            try:
                mine_pos_at_arr = get_planet_position_at_step(
                    mine_id, arr_step, initial_planets, angular_velocity
                )
            except Exception as e:
                mine_pos_at_arr = (mine_x, mine_y)
                
            vel_x = math.cos(fangle)
            vel_y = math.sin(fangle)
            fleet_x_at_arr = fx + (arr_step - s) * vel_x * speed
            fleet_y_at_arr = fy + (arr_step - s) * vel_y * speed
            
            dist_at_arr = distance((fleet_x_at_arr, fleet_y_at_arr), mine_pos_at_arr)
            
            print(f"  Fleet 224: pos=({fx:.2f}, {fy:.2f}), dist={dist:.2f}, speed={speed:.2f}, arr_step={arr_step} (in {arr_step - s} turns)")
            print(f"  Planet pos at arr_step: {mine_pos_at_arr}")
            print(f"  Fleet pos at arr_step:  ({fleet_x_at_arr:.2f}, {fleet_y_at_arr:.2f})")
            print(f"  Trajectory Intersection Distance: {dist_at_arr:.4f}")
            print(f"  Intersection Check Passed? {dist_at_arr < 2.0}")
