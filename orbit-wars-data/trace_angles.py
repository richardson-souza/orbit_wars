import json
import math

def trace_angles(filepath):
    print(f"\n========================================\nTRACING ANGLES: {filepath}\n========================================")
    with open(filepath) as f:
        episode = json.load(f)
        
    steps = episode["steps"]
    obs = steps[0][0]["observation"]
    angular_velocity = obs.get("angular_velocity", 0.0)
    initial_planets = obs.get("initial_planets", [])
    
    # Let's map target planet IDs
    planets_dict = {p[0]: p for p in initial_planets}
    
    # We want to trace Player 0 (home planet 12)
    # Let's look at all steps where P0 took an action
    for s_idx, step in enumerate(steps):
        act = step[0].get("action")
        if act:
            # Let's see what the actual state of planet 12 was in this step
            p_state = next(p for p in step[0]["observation"]["planets"] if p[0] == 12)
            px, py = p_state[2], p_state[3]
            
            for move in act:
                from_id, angle, ships = move
                # Let's find which planet is closest to the line starting from (px, py) with direction angle
                # We can check all other planets (their actual positions at s_idx)
                # and see which one is closest to the line, or which one has the angle closest to this angle
                closest_p = None
                min_angle_diff = float('inf')
                closest_dist = 0.0
                
                # Predict positions of all planets at this step
                for target_id, target_p in planets_dict.items():
                    if target_id == 12:
                        continue
                    
                    # Predict position of target at this step
                    _, _, init_x, init_y, radius, _, _ = target_p
                    dx = init_x - 50.0
                    dy = init_y - 50.0
                    orb_r = math.sqrt(dx**2 + dy**2)
                    
                    if orb_r + radius < 50.0:
                        initial_angle = math.atan2(dy, dx)
                        current_angle = initial_angle + angular_velocity * s_idx
                        tx = 50.0 + orb_r * math.cos(current_angle)
                        ty = 50.0 + orb_r * math.sin(current_angle)
                    else:
                        tx, ty = init_x, init_y
                        
                    # Calculate angle to this target
                    ang_to_target = math.atan2(ty - py, tx - px)
                    # Normalize difference to [-pi, pi]
                    diff = (angle - ang_to_target + math.pi) % (2 * math.pi) - math.pi
                    abs_diff = abs(diff)
                    
                    if abs_diff < min_angle_diff:
                        min_angle_diff = abs_diff
                        closest_p = (target_id, tx, ty, radius)
                        closest_dist = math.sqrt((tx - px)**2 + (ty - py)**2)
                        
                print(f"Step {s_idx:3d} | Planet 12 Ships: {p_state[5]} | Launch: angle={angle:6.3f}, ships={ships} | Target: ID={closest_p[0]:2d}, Dist={closest_dist:5.1f}, Size={closest_p[3]:4.1f}, AngDiff={min_angle_diff:.6f}")

if __name__ == "__main__":
    trace_angles("docs/episodes/77834940.json")
