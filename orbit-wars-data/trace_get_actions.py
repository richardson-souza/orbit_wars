import json
import math
from strategies.heuristic_scorer import HeuristicScorer
from core.observation import ParsedObservation
from core.physics import distance, get_planet_position_at_step, intersects_sun

def trace_target_18(filepath):
    with open(filepath) as f:
        episode = json.load(f)
    obs = episode["steps"][15][0]["observation"]
    parsed = ParsedObservation(obs)
    
    scorer = HeuristicScorer(
        production_weight=12.0,
        distance_weight=3.5,
        ship_cost_weight=0.1,
        comet_bonus=25.0,
        aggression_weight=1.0
    )
    
    mine = next(p for p in parsed.my_planets if p.id == 12)
    target = parsed.all_planets[18]
    
    curr_dist = distance((mine.x, mine.y), (target.x, target.y))
    proposed_ships = max(target.ships + 2, int(mine.ships * 0.75))
    proposed_ships = min(proposed_ships, mine.ships - 5)
    
    est_speed = scorer.estimate_fleet_speed(proposed_ships)
    est_turns = int(math.ceil(curr_dist / est_speed))
    arrival_step = parsed.step + est_turns
    
    predicted_pos = get_planet_position_at_step(
        target.id,
        arrival_step,
        parsed.initial_planets,
        parsed.angular_velocity,
    )
    
    pred_dist = distance((mine.x, mine.y), predicted_pos)
    angle = math.atan2(predicted_pos[1] - mine.y, predicted_pos[0] - mine.x)
    
    print("DEBUG TARGET 18:")
    print(f"  mine.x, mine.y: ({mine.x:.4f}, {mine.y:.4f})")
    print(f"  target.x, target.y: ({target.x:.4f}, {target.y:.4f})")
    print(f"  curr_dist: {curr_dist:.4f}")
    print(f"  proposed_ships: {proposed_ships}")
    print(f"  est_speed: {est_speed:.4f}")
    print(f"  est_turns: {est_turns}")
    print(f"  arrival_step: {arrival_step}")
    print(f"  predicted_pos: ({predicted_pos[0]:.4f}, {predicted_pos[1]:.4f})")
    print(f"  pred_dist: {pred_dist:.4f}")
    print(f"  angle: {angle:.6f}")

trace_target_18("docs/episodes/77834940.json")
