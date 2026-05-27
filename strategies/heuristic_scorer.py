import math
from typing import List, Dict, Any, Union, Tuple
from strategies.base_strategy import BaseStrategy
from core.observation import ParsedObservation, Planet, Fleet
from core.physics import distance, intersects_sun, get_planet_position_at_step


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

        planets_with_outgoing_fleets = {f.from_planet_id for f in obs.my_fleets}

        candidate_targets: List[Planet] = []
        candidate_targets.extend(obs.enemy_planets)
        candidate_targets.extend(obs.neutral_planets)
        candidate_targets.extend(obs.active_comets)

        if not candidate_targets or not obs.my_planets:
            return moves

        for mine in obs.my_planets:
            if mine.id in planets_with_outgoing_fleets:
                continue

            best_target: Planet = None
            best_score: float = -float("inf")
            best_ships_to_send: int = 0
            best_angle: float = 0.0

            available_ships = planet_ships.get(mine.id, 0)

            if available_ships < 25:
                continue

            for target in candidate_targets:
                curr_dist = distance((mine.x, mine.y), (target.x, target.y))
                if curr_dist <= 0:
                    continue

                if curr_dist > 55.0:
                    continue

                proposed_ships = max(target.ships + 2, int(available_ships * 0.75))
                proposed_ships = min(proposed_ships, available_ships - 5)

                if proposed_ships <= target.ships:
                    continue
                est_speed = self.estimate_fleet_speed(proposed_ships)
                est_turns = int(math.ceil(curr_dist / est_speed))
                arrival_step = obs.step + est_turns
                try:
                    predicted_pos = get_planet_position_at_step(
                        target.id,
                        arrival_step,
                        obs.initial_planets,
                        obs.angular_velocity,
                    )
                except ValueError:
                    predicted_pos = (target.x, target.y)

                if intersects_sun(mine.x, mine.y, predicted_pos[0], predicted_pos[1]):
                    continue

                pred_dist = distance((mine.x, mine.y), predicted_pos)
                angle = math.atan2(predicted_pos[1] - mine.y, predicted_pos[0] - mine.x)
                travel_turns = max(1, int(math.ceil(pred_dist / est_speed)))

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

            if best_target is not None and best_ships_to_send > 0:
                moves.append([mine.id, best_angle, best_ships_to_send])
                planet_ships[mine.id] -= best_ships_to_send

        return moves
