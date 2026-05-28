import time
import math
import random
from typing import List, Dict, Any, Union, Tuple
from strategies.base_strategy import BaseStrategy
from strategies.heuristic_scorer import HeuristicScorer
from core.observation import ParsedObservation, Planet, Fleet
from core.physics import distance, intersects_sun, get_planet_position_at_step


class MCTSNode:
    """Represents a node in the MCTS tree."""

    def __init__(
        self, actions: List[List[Union[int, float]]], parent: "MCTSNode" = None
    ):
        self.actions = actions
        self.parent = parent
        self.children: List["MCTSNode"] = []
        self.visits = 0
        self.value = 0.0


class MCTSSearch(BaseStrategy):
    """
    Heuristic-Guided Monte Carlo Tree Search (MCTS) Strategy for Orbit Wars.
    Uses dynamic time budgeting and checks remaining overage time to prevent timeouts.
    """

    def __init__(self, simulation_depth: int = 15, max_iterations: int = 200):
        self.simulation_depth = simulation_depth
        self.max_iterations = max_iterations
        self.heuristic = HeuristicScorer(aggression_weight=1.2)

    def get_actions(
        self, observation: Union[Dict[str, Any], Any]
    ) -> List[List[Union[int, float]]]:
        start_time = time.perf_counter()

        obs = ParsedObservation(observation)

        if obs.remaining_overage_time < 0.2:
            return self.heuristic.get_actions(observation)

        time_limit = min(0.15, obs.remaining_overage_time - 0.1)

        heuristic_actions = self.heuristic.get_actions(observation)
        if not heuristic_actions:
            return []

        root = MCTSNode(actions=[])

        variations = [heuristic_actions, []]

        if len(heuristic_actions) > 1:
            for action in heuristic_actions:
                variations.append([action])

        for var in variations:
            root.children.append(MCTSNode(actions=var, parent=root))

        iterations = 0
        while iterations < self.max_iterations:
            elapsed = time.perf_counter() - start_time
            if elapsed >= time_limit:
                break
            node = self.select(root)
            score = self.rollout(obs, node.actions)
            self.backpropagate(node, score)

            iterations += 1

        best_child = None
        best_avg_value = -float("inf")

        for child in root.children:
            if child.visits > 0:
                avg_value = child.value / child.visits
                if avg_value > best_avg_value:
                    best_avg_value = avg_value
                    best_child = child

        if best_child is not None:
            return best_child.actions

        return heuristic_actions

    def select(self, node: MCTSNode) -> MCTSNode:
        """Select node using UCB1 formula."""
        if not node.children:
            return node

        best_node = None
        best_score = -float("inf")

        for child in node.children:
            if child.visits == 0:
                return child

            exploration = 1.414 * math.sqrt(math.log(node.visits) / child.visits)
            score = (child.value / child.visits) + exploration

            if score > best_score:
                best_score = score
                best_node = child

        return self.select(best_node) if best_node else node

    def rollout(
        self, obs: ParsedObservation, candidate_actions: List[List[Union[int, float]]]
    ) -> float:
        """Simulate state transition forward in time and evaluate the final score."""
        score = 0.0

        my_planet_ships = {p.id: p.ships for p in obs.my_planets}
        enemy_planet_ships = {p.id: p.ships for p in obs.enemy_planets}
        neutral_planet_ships = {p.id: p.ships for p in obs.neutral_planets}

        # Apply candidate actions immediately
        for action in candidate_actions:
            from_id, _, ships = action
            ships = int(ships)
            if from_id in my_planet_ships:
                my_planet_ships[from_id] = max(0, my_planet_ships[from_id] - ships)

        # Estimate incoming fleets' arrivals
        fleet_impacts: Dict[int, List[Tuple[int, int]]] = {} # step_offset -> list of (planet_id, owner, ships)
        for fleet in obs.all_fleets:
            target_planet = self.heuristic.estimate_fleet_target(fleet, list(obs.all_planets.values()))
            if target_planet:
                dist = distance((fleet.x, fleet.y), (target_planet.x, target_planet.y))
                speed = self.heuristic.estimate_fleet_speed(fleet.ships)
                arr_offset = int(math.ceil(dist / speed))
                
                if 1 <= arr_offset <= self.simulation_depth:
                    if arr_offset not in fleet_impacts:
                        fleet_impacts[arr_offset] = []
                    fleet_impacts[arr_offset].append((target_planet.id, fleet.owner, fleet.ships))

        # Forward simulate step-by-step
        for step_offset in range(1, self.simulation_depth + 1):
            # 1. Grow production
            for pid in list(my_planet_ships.keys()):
                p = obs.all_planets[pid]
                my_planet_ships[pid] += p.production
            for pid in list(enemy_planet_ships.keys()):
                p = obs.all_planets[pid]
                enemy_planet_ships[pid] += p.production

            # 2. Resolve incoming fleet impacts at this step
            if step_offset in fleet_impacts:
                for pid, owner, ships in fleet_impacts[step_offset]:
                    if owner == obs.player:
                        # Our fleet
                        if pid in my_planet_ships:
                            my_planet_ships[pid] += ships
                        elif pid in enemy_planet_ships:
                            if ships > enemy_planet_ships[pid]:
                                ships_left = ships - enemy_planet_ships[pid]
                                enemy_planet_ships.pop(pid)
                                my_planet_ships[pid] = ships_left
                            else:
                                enemy_planet_ships[pid] -= ships
                        elif pid in neutral_planet_ships:
                            if ships > neutral_planet_ships[pid]:
                                ships_left = ships - neutral_planet_ships[pid]
                                neutral_planet_ships.pop(pid)
                                my_planet_ships[pid] = ships_left
                            else:
                                neutral_planet_ships[pid] -= ships
                    else:
                        # Enemy fleet
                        if pid in enemy_planet_ships:
                            enemy_planet_ships[pid] += ships
                        elif pid in my_planet_ships:
                            if ships > my_planet_ships[pid]:
                                ships_left = ships - my_planet_ships[pid]
                                my_planet_ships.pop(pid)
                                enemy_planet_ships[pid] = ships_left
                            else:
                                my_planet_ships[pid] -= ships
                        elif pid in neutral_planet_ships:
                            if ships > neutral_planet_ships[pid]:
                                ships_left = ships - neutral_planet_ships[pid]
                                neutral_planet_ships.pop(pid)
                                enemy_planet_ships[pid] = ships_left
                            else:
                                neutral_planet_ships[pid] -= ships

        total_my_ships = sum(my_planet_ships.values())
        total_enemy_ships = sum(enemy_planet_ships.values())

        capture_score = len(my_planet_ships) * 10.0

        score = (total_my_ships - total_enemy_ships) + capture_score
        return score

    def backpropagate(self, node: MCTSNode, score: float):
        """Backpropagate the rollout score up the tree."""
        curr = node
        while curr is not None:
            curr.visits += 1
            curr.value += score
            curr = curr.parent
