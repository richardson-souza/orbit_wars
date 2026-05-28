import math
from typing import List, Dict, Any, Union, Tuple
from strategies.base_strategy import BaseStrategy
from core.observation import ParsedObservation, Planet, Fleet
from core.physics import distance, intersects_sun, get_planet_position_at_step, intersects_planet


class HeuristicScorer(BaseStrategy):
    """
    Refined High-Performance Heuristic Scorer strategy for Orbit Wars.
    Integrates Outgoing Fleet Lock to prevent spamming, high-proximity targeting,
    and high concentration of launch force.
    """

    def __init__(
        self,
        production_weight: float = 12.0,
        distance_weight: float = 3.5,
        ship_cost_weight: float = 0.1,
        comet_bonus: float = 25.0,
        aggression_weight: float = 1.0,
    ):
        self.production_weight = production_weight
        self.distance_weight = distance_weight
        self.ship_cost_weight = ship_cost_weight
        self.comet_bonus = comet_bonus
        self.aggression_weight = aggression_weight

    def estimate_fleet_speed(self, num_ships: int) -> float:
        """
        Estimate fleet speed based on the official Kaggle Orbit Wars formula.
        """
        max_speed = 6.0
        if num_ships <= 1:
            return 1.0

        log_ratio = math.log(num_ships) / math.log(1000.0)
        speed = 1.0 + 5.0 * max(0.0, log_ratio) ** 1.5
        return min(speed, max_speed)

    def get_actions(
        self, observation: Union[Dict[str, Any], Any]
    ) -> List[List[Union[int, float]]]:
        obs = ParsedObservation(observation)
        moves: List[List[Union[int, float]]] = []

        planet_ships = {p.id: p.ships for p in obs.my_planets}

        self.sent_fleets_tracker = getattr(self, "sent_fleets_tracker", {})
        self.sent_fleets_tracker = {pid: arr_step for pid, arr_step in self.sent_fleets_tracker.items() if obs.step < arr_step}

        candidate_targets: List[Planet] = []
        candidate_targets.extend(obs.enemy_planets)
        candidate_targets.extend(obs.neutral_planets)
        candidate_targets.extend(obs.active_comets)

        if not candidate_targets or not obs.my_planets:
            return moves

        owners = {p.owner for p in obs.my_planets + obs.enemy_planets if p.owner != -1}
        is_four_player = len(owners) > 2

        for mine in obs.my_planets:
            best_target: Planet = None
            best_score: float = -float("inf")
            best_ships_to_send: int = 0
            best_angle: float = 0.0
            best_travel_turns: int = 0

            available_ships = planet_ships.get(mine.id, 0)

            if len(obs.my_planets) <= 1:
                min_reserve_ships = 5
            elif obs.step < 100 and len(obs.my_planets) <= 2:
                min_reserve_ships = 12 if not is_four_player else 20
            else:
                min_reserve_ships = 22 if not is_four_player else 35

            min_reserve_ships = min(min_reserve_ships, int(available_ships * 0.4))
            min_reserve_ships = max(5 if len(obs.my_planets) <= 1 else 10, min_reserve_ships)
            if available_ships < min_reserve_ships:
                continue

            for target in candidate_targets:
                if target.id in self.sent_fleets_tracker:
                    continue
                curr_dist = distance((mine.x, mine.y), (target.x, target.y))
                if curr_dist <= 0:
                    continue

                max_attack_dist = 55.0
                if obs.step < 100 and len(obs.my_planets) <= 2:
                    max_attack_dist = 35.0

                if curr_dist > max_attack_dist:
                    continue

                proposed_ships = max(target.ships + 2, int(available_ships * 0.75))
                proposed_ships = min(proposed_ships, available_ships - 5)

                if proposed_ships <= target.ships:
                    continue

                est_speed = self.estimate_fleet_speed(proposed_ships)

                best_t = None
                min_diff = float("inf")
                best_pred_pos = None

                for t in range(1, 80):
                    arrival_step = obs.step + t
                    try:
                        pred_pos = get_planet_position_at_step(
                            target.id,
                            arrival_step,
                            obs.initial_planets,
                            obs.angular_velocity,
                        )
                    except ValueError:
                        pred_pos = (target.x, target.y)

                    dist = distance((mine.x, mine.y), pred_pos)
                    travel_turns = dist / est_speed
                    diff = abs(travel_turns - t)
                    if diff < min_diff:
                        min_diff = diff
                        best_t = t
                        best_pred_pos = pred_pos

                predicted_pos = best_pred_pos
                travel_turns = max(1, int(math.ceil(distance((mine.x, mine.y), predicted_pos) / est_speed)))

                if intersects_sun(mine.x, mine.y, predicted_pos[0], predicted_pos[1]):
                    continue

                obstacle_collision = False
                for other_p in obs.all_planets.values():
                    if other_p.id == mine.id or other_p.id == target.id:
                        continue
                    if intersects_planet(
                        mine.x,
                        mine.y,
                        predicted_pos[0],
                        predicted_pos[1],
                        other_p.id,
                        obs.initial_planets,
                        obs.angular_velocity,
                        obs.step,
                        travel_turns,
                    ):
                        obstacle_collision = True
                        break

                if obstacle_collision:
                    continue

                pred_dist = distance((mine.x, mine.y), predicted_pos)
                angle = math.atan2(predicted_pos[1] - mine.y, predicted_pos[0] - mine.x)

                if target.owner == -1 or target.id in obs.comet_planet_ids:
                    predicted_garrison = target.ships
                else:
                    predicted_garrison = target.ships + travel_turns * target.production

                ships_needed = predicted_garrison + 2

                if proposed_ships < ships_needed:
                    proposed_ships = ships_needed

                if available_ships < proposed_ships + 5:
                    continue

                score = (
                    self.production_weight * target.production
                    - self.distance_weight * pred_dist
                    - self.ship_cost_weight * proposed_ships
                )

                if target.id in obs.comet_planet_ids:
                    score += self.comet_bonus

                score *= self.aggression_weight

                if score > best_score:
                    best_score = score
                    best_target = target
                    best_ships_to_send = proposed_ships
                    best_angle = angle
                    best_travel_turns = travel_turns

            if best_target is not None and best_ships_to_send > 0:
                moves.append([mine.id, best_angle, best_ships_to_send])
                planet_ships[mine.id] -= best_ships_to_send
                self.sent_fleets_tracker[best_target.id] = obs.step + best_travel_turns

        return moves
