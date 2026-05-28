import json
import math
from strategies.heuristic_scorer import HeuristicScorer
from core.observation import ParsedObservation

def debug_step(filepath, step_idx):
    with open(filepath) as f:
        episode = json.load(f)
    
    step_data = episode["steps"][step_idx]
    # The observation is the same for both players, let's take the first player's observation
    obs = step_data[0]["observation"]
    
    # Let's instantiate our HeuristicScorer with both sets of weights to see which one matches!
    scorers = {
        "submission_weights": HeuristicScorer(
            production_weight=12.0,
            distance_weight=3.5,
            ship_cost_weight=0.1,
            comet_bonus=25.0,
            aggression_weight=1.0
        ),
        "main_weights": HeuristicScorer(
            production_weight=15.0,
            distance_weight=0.7,
            ship_cost_weight=0.1,
            comet_bonus=25.0,
            aggression_weight=1.5
        )
    }
    
    parsed = ParsedObservation(obs)
    print(f"\n--- Debugging Step {step_idx} from {filepath} ---")
    print(f"My player ID: {parsed.player}")
    print(f"Step in obs: {parsed.step}")
    
    for mine in parsed.my_planets:
        print(f"My Planet: ID={mine.id}, Pos=({mine.x:.2f}, {mine.y:.2f}), Ships={mine.ships}, Prod={mine.production}")
        
    for name, scorer in scorers.items():
        print(f"\nEvaluating with {name}:")
        actions = scorer.get_actions(obs)
        print(f"  Actions returned: {actions}")
        
        # Let's print details of all candidates for this planet
        for mine in parsed.my_planets:
            available_ships = mine.ships
            print(f"  Planet {mine.id} available ships: {available_ships}")
            
            candidate_targets = []
            candidate_targets.extend(parsed.enemy_planets)
            candidate_targets.extend(parsed.neutral_planets)
            candidate_targets.extend(parsed.active_comets)
            
            for target in candidate_targets:
                curr_dist = math.hypot(mine.x - target.x, mine.y - target.y)
                if curr_dist <= 0 or curr_dist > 55.0:
                    continue
                    
                proposed_ships = max(target.ships + 2, int(available_ships * 0.75))
                proposed_ships = min(proposed_ships, available_ships - 5)
                
                # Let's print calculation steps
                is_valid = True
                reason = "OK"
                
                if proposed_ships <= target.ships:
                    is_valid = False
                    reason = f"proposed_ships ({proposed_ships}) <= target.ships ({target.ships})"
                
                est_speed = scorer.estimate_fleet_speed(proposed_ships)
                est_turns = int(math.ceil(curr_dist / est_speed))
                arrival_step = parsed.step + est_turns
                
                from core.physics import get_planet_position_at_step, intersects_sun
                try:
                    predicted_pos = get_planet_position_at_step(
                        target.id,
                        arrival_step,
                        parsed.initial_planets,
                        parsed.angular_velocity,
                    )
                except ValueError:
                    predicted_pos = (target.x, target.y)
                    
                if is_valid and intersects_sun(mine.x, mine.y, predicted_pos[0], predicted_pos[1]):
                    is_valid = False
                    reason = "intersects sun"
                    
                pred_dist = math.hypot(mine.x - predicted_pos[0], mine.y - predicted_pos[1])
                angle = math.atan2(predicted_pos[1] - mine.y, predicted_pos[0] - mine.x)
                travel_turns = max(1, int(math.ceil(pred_dist / est_speed)))
                
                if target.owner == -1 or target.id in parsed.comet_planet_ids:
                    predicted_garrison = target.ships
                else:
                    predicted_garrison = target.ships + travel_turns * target.production
                    
                ships_needed = predicted_garrison + 2
                
                # Check proposed ships modification
                overridden = False
                orig_proposed = proposed_ships
                if is_valid and proposed_ships < ships_needed:
                    proposed_ships = ships_needed
                    overridden = True
                    
                if is_valid and available_ships < proposed_ships + 5:
                    is_valid = False
                    reason = f"available_ships ({available_ships}) < proposed_ships + 5 ({proposed_ships + 5})"
                    
                if is_valid:
                    score = (
                        scorer.production_weight * target.production
                        - scorer.distance_weight * pred_dist
                        - scorer.ship_cost_weight * proposed_ships
                    )
                    if target.id in parsed.comet_planet_ids:
                        score += scorer.comet_bonus
                    score *= scorer.aggression_weight
                    
                    print(f"    Target ID={target.id:2d} | Dist={curr_dist:5.1f} | PredDist={pred_dist:5.1f} | TargetShips={target.ships:2d} | GarrisonNeeded={ships_needed:2d} | Proposed={proposed_ships:2d} (orig={orig_proposed:2d}) | Score={score:6.2f} | Valid=YES")
                else:
                    print(f"    Target ID={target.id:2d} | Dist={curr_dist:5.1f} | TargetShips={target.ships:2d} | Valid=NO ({reason})")

if __name__ == "__main__":
    debug_step("docs/episodes/77834940.json", 15)
