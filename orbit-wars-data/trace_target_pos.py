import json
import math
from core.physics import get_planet_position_at_step
from core.observation import ParsedObservation

def print_positions(filepath):
    with open(filepath) as f:
        episode = json.load(f)
    obs = episode["steps"][15][0]["observation"]
    parsed = ParsedObservation(obs)
    
    p12 = next(p for p in parsed.all_planets.values() if p.id == 12)
    print(f"Planet 12 pos: ({p12.x:.3f}, {p12.y:.3f})")
    
    for p_id in [14, 16, 18, 20]:
        target = parsed.all_planets[p_id]
        try:
            pred_pos = get_planet_position_at_step(
                target.id,
                15 + 7, # let's assume 7 turns travel
                parsed.initial_planets,
                parsed.angular_velocity
            )
        except ValueError:
            pred_pos = (target.x, target.y)
        angle = math.atan2(pred_pos[1] - p12.y, pred_pos[0] - p12.x)
        print(f"Planet {p_id:2d} | CurrPos=({target.x:.2f}, {target.y:.2f}) | PredPos=({pred_pos[0]:.2f}, {pred_pos[1]:.2f}) | Angle={angle:.4f}")

print_positions("docs/episodes/77834940.json")
