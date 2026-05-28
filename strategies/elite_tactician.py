import math
from typing import List, Dict, Any, Union, Tuple
from strategies.base_strategy import BaseStrategy
from core.observation import ParsedObservation, Planet, Fleet
from core.physics import distance, intersects_sun, get_planet_position_at_step, intersects_planet


class EliteTactician(BaseStrategy):
    """
    Advanced EliteTactician strategy implementing Coordinated Time-on-Target (ToT) attacks,
    Evacuação Defensiva (Dodging), and dynamic obstacle ray-casting to bypass competitive plateaus.
    """

    def __init__(
        self,
        production_weight: float = 15.0,
        distance_weight: float = 0.7,
        ship_cost_weight: float = 0.1,
        comet_bonus: float = 25.0,
        aggression_weight: float = 1.5,
    ):
        self.production_weight = production_weight
        self.distance_weight = distance_weight
        self.ship_cost_weight = ship_cost_weight
        self.comet_bonus = comet_bonus
        self.aggression_weight = aggression_weight

        # Stateful tracking for Coordinated Time-on-Target (ToT) attacks
        self.active_tot_attacks: Dict[int, Tuple[int, int]] = {}  # target_id -> (arrival_step, total_ships_to_send)
        self.tot_assignments: Dict[Tuple[int, int], int] = {}     # (target_id, source_id) -> ships_to_send
        self.sent_fleets_tracker: Dict[int, int] = {}             # target_id -> arrival_step for classic launches

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

        # ----------------------------------------------------
        # 1. CLEANUP ACTIVE STATEFUL TRACKERS
        # ----------------------------------------------------
        self.active_tot_attacks = {
            tid: (arr_step, total_s)
            for tid, (arr_step, total_s) in self.active_tot_attacks.items()
            if obs.step < arr_step
        }
        self.tot_assignments = {
            (tid, sid): ships
            for (tid, sid), ships in self.tot_assignments.items()
            if tid in self.active_tot_attacks
        }
        self.sent_fleets_tracker = getattr(self, "sent_fleets_tracker", {})
        self.sent_fleets_tracker = {
            pid: arr_step for pid, arr_step in self.sent_fleets_tracker.items()
            if obs.step < arr_step
        }

        if not obs.my_planets:
            return moves

        # ----------------------------------------------------
        # 2. EVACUAÇÃO DEFENSIVA (DODGING)
        # ----------------------------------------------------
        evacuating_planets: Dict[int, int] = {}  # source_id -> ships_to_evacuate
        for mine in obs.my_planets:
            incoming_threats: Dict[int, List[Fleet]] = {}  # arrival_step -> list of threat fleets
            for fleet in obs.all_fleets:
                if fleet.owner == obs.player:
                    continue
                # Calculate threat arrival step
                dist = distance((fleet.x, fleet.y), (mine.x, mine.y))
                speed = self.estimate_fleet_speed(fleet.ships)
                arr_step = obs.step + int(math.ceil(dist / speed))
                if arr_step not in incoming_threats:
                    incoming_threats[arr_step] = []
                incoming_threats[arr_step].append(fleet)

            # Analyze threats by arrival steps
            for arr_step, fleets in sorted(incoming_threats.items()):
                # Project garrison
                turns = arr_step - obs.step
                projected_garrison = mine.ships + turns * mine.production
                # Add incoming allied reinforcements
                for f in obs.all_fleets:
                    if f.owner == obs.player:
                        dist_a = distance((f.x, f.y), (mine.x, mine.y))
                        speed_a = self.estimate_fleet_speed(f.ships)
                        arr_step_a = obs.step + int(math.ceil(dist_a / speed_a))
                        if arr_step_a <= arr_step:
                            projected_garrison += f.ships

                enemy_sum = sum(f.ships for f in fleets)
                if enemy_sum > projected_garrison:
                    # Overwhelming threat detected! If impact is <= 1 turns, trigger evacuation!
                    if arr_step - obs.step <= 1:
                        evacuating_planets[mine.id] = mine.ships
                        break

        # Process evacuations immediately to save our fleets
        for source_id, ships_to_evacuate in evacuating_planets.items():
            if ships_to_evacuate <= 0:
                continue
            mine = obs.all_planets[source_id]
            # Find the best, closest safe target (either our own safe planets or neutral ones)
            best_safe_target = None
            min_dist = float("inf")
            for other in obs.my_planets + obs.neutral_planets:
                if other.id == source_id:
                    continue
                if other.id in evacuating_planets:
                    continue
                # Ray-cast check to prevent defensive evacuation suicide into the Sun!
                if intersects_sun(mine.x, mine.y, other.x, other.y):
                    continue
                dist = distance((mine.x, mine.y), (other.x, other.y))
                if dist < min_dist:
                    min_dist = dist
                    best_safe_target = other

            if best_safe_target:
                # Evacuate 100% of ships to safety!
                angle = math.atan2(best_safe_target.y - mine.y, best_safe_target.x - mine.x)
                moves.append([source_id, angle, ships_to_evacuate])
                planet_ships[source_id] = 0

        # ----------------------------------------------------
        # 3. SCHEDULED TIME-ON-TARGET (ToT) RELEASES
        # ----------------------------------------------------
        for (target_id, source_id), ships in list(self.tot_assignments.items()):
            if source_id in evacuating_planets:
                continue
            available = planet_ships.get(source_id, 0)
            if available < ships:
                continue

            target = obs.all_planets[target_id]
            arrival_step, _ = self.active_tot_attacks[target_id]
            turns_remaining = arrival_step - obs.step

            # Predict target position at arrival_step
            try:
                pred_pos = get_planet_position_at_step(
                    target.id,
                    arrival_step,
                    obs.initial_planets,
                    obs.angular_velocity,
                )
            except ValueError:
                pred_pos = (target.x, target.y)

            mine = obs.all_planets[source_id]
            dist = distance((mine.x, mine.y), pred_pos)
            speed = self.estimate_fleet_speed(ships)
            est_turns = int(math.ceil(dist / speed))

            # Launch today if we are exactly at or past the correct synchronized step window!
            if est_turns >= turns_remaining:
                angle = math.atan2(pred_pos[1] - mine.y, pred_pos[0] - mine.x)
                # Check Sun or Planet Collision
                if not intersects_sun(mine.x, mine.y, pred_pos[0], pred_pos[1]):
                    obstacle_collision = False
                    for other_p in obs.all_planets.values():
                        if other_p.id == mine.id or other_p.id == target.id:
                            continue
                        if intersects_planet(
                            mine.x, mine.y, pred_pos[0], pred_pos[1], other_p.id,
                            obs.initial_planets, obs.angular_velocity, obs.step, est_turns
                        ):
                            obstacle_collision = True
                            break

                    if not obstacle_collision:
                        moves.append([source_id, angle, ships])
                        planet_ships[source_id] -= ships
                
                # Prevent deadlock: if the launch window reached, remove assignment in any case!
                del self.tot_assignments[(target_id, source_id)]

        # ----------------------------------------------------
        # 4. INITIALIZE NEW COORDINATED ToT ATTACKS
        # ----------------------------------------------------
        owners = {p.owner for p in obs.my_planets + obs.enemy_planets if p.owner != -1}
        is_four_player = len(owners) > 2

        # Filter candidates (enemy and neutral)
        candidate_targets: List[Planet] = []
        candidate_targets.extend(obs.enemy_planets)
        candidate_targets.extend(obs.neutral_planets)
        candidate_targets.extend(obs.active_comets)

        for target in candidate_targets:
            if target.id in self.active_tot_attacks:
                continue

            max_attack_dist = 55.0
            if obs.step < 100 and len(obs.my_planets) <= 2:
                max_attack_dist = 35.0

            best_arrival_step = None
            best_launchers = []
            best_ships_needed = 0

            # Solve the Targeting Paradox: Propose a single global arrival step first, then verify launchers
            # Using step of 2 is highly granular and twice as fast!
            for arr_step in range(obs.step + 10, min(500, obs.step + 60), 2):
                try:
                    target_pos = get_planet_position_at_step(
                        target.id, arr_step, obs.initial_planets, obs.angular_velocity
                    )
                except ValueError:
                    target_pos = (target.x, target.y)

                # Project target garrison at global arr_step
                if target.owner == -1 or target.id in obs.comet_planet_ids:
                    predicted_garrison = target.ships
                else:
                    predicted_garrison = target.ships + (arr_step - obs.step) * target.production

                ships_needed = predicted_garrison + 2
                potential_launchers = []
                total_avail_potential = 0

                for mine in obs.my_planets:
                    if mine.id in evacuating_planets:
                        continue
                    available_ships = planet_ships.get(mine.id, 0)

                    # Safe reserve check
                    if len(obs.my_planets) <= 1:
                        min_res = 5
                    elif obs.step < 100 and len(obs.my_planets) <= 2:
                        min_res = 12 if not is_four_player else 20
                    else:
                        min_res = 22 if not is_four_player else 35
                    min_res = min(min_res, int(available_ships * 0.4))
                    min_res = max(5 if len(obs.my_planets) <= 1 else 10, min_res)

                    cap = max(0, available_ships - min_res)
                    if cap <= 5:
                        continue

                    curr_dist = distance((mine.x, mine.y), (target.x, target.y))
                    if curr_dist <= 0 or curr_dist > max_attack_dist:
                        continue

                    # Estimate travel speed using cap
                    est_speed = self.estimate_fleet_speed(max(10, int(cap * 0.75)))
                    dist_to_pred = distance((mine.x, mine.y), target_pos)
                    travel_turns = int(math.ceil(dist_to_pred / est_speed))

                    # Can it arrive exactly at the scheduled global step?
                    if travel_turns <= (arr_step - obs.step):
                        # Cheap Sun collision check
                        if intersects_sun(mine.x, mine.y, target_pos[0], target_pos[1]):
                            continue
                        
                        potential_launchers.append((mine, cap, travel_turns))
                        total_avail_potential += cap

                # Performance Optimization: Only check expensive planet collision if we have enough potential ships!
                if total_avail_potential >= ships_needed:
                    valid_launchers_for_step = []
                    total_avail_for_step = 0

                    for mine, cap, travel_turns in potential_launchers:
                        obstacle_collision = False
                        for other_p in obs.all_planets.values():
                            if other_p.id == mine.id or other_p.id == target.id:
                                continue
                            launch_step = arr_step - travel_turns
                            if intersects_planet(
                                mine.x, mine.y, target_pos[0], target_pos[1], other_p.id,
                                obs.initial_planets, obs.angular_velocity, launch_step, travel_turns
                            ):
                                obstacle_collision = True
                                break

                        if not obstacle_collision:
                            valid_launchers_for_step.append((mine, cap))
                            total_avail_for_step += cap

                    if total_avail_for_step >= ships_needed and total_avail_for_step > 0:
                        best_arrival_step = arr_step
                        best_launchers = valid_launchers_for_step
                        best_ships_needed = ships_needed
                        break  # Eagerly select the earliest viable arrival step

            # If a viable synchronized arrival step is found, allocate the stateful assignment
            if best_arrival_step is not None:
                self.active_tot_attacks[target.id] = (best_arrival_step, best_ships_needed)
                total_avail = sum(x[1] for x in best_launchers)
                allocated_total = 0
                launcher_caps = {mine.id: cap for mine, cap in best_launchers}

                for mine, cap in best_launchers:
                    contrib = int(math.ceil(best_ships_needed * (cap / total_avail)))
                    contrib = min(contrib, cap)
                    if contrib > 0:
                        self.tot_assignments[(target.id, mine.id)] = contrib
                        allocated_total += contrib

                # Adjust rounding differences
                if allocated_total < best_ships_needed and launcher_caps:
                    strongest_id = max(launcher_caps, key=lambda k: launcher_caps[k])
                    diff = best_ships_needed - allocated_total
                    self.tot_assignments[(target.id, strongest_id)] = self.tot_assignments.get((target.id, strongest_id), 0) + diff

        # ----------------------------------------------------
        # 5. EXECUTE SINGLE-SOURCE CLASSIC LAUNCHES FOR SPARE SHIPS
        # ----------------------------------------------------
        for mine in obs.my_planets:
            if mine.id in evacuating_planets:
                continue

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

            best_target: Planet = None
            best_score: float = -float("inf")
            best_ships_to_send: int = 0
            best_angle: float = 0.0
            best_travel_turns: int = 0

            for target in candidate_targets:
                # Skip targets that are already assigned to ToT to avoid redundancy
                if (target.id, mine.id) in self.tot_assignments or target.id in self.active_tot_attacks:
                    continue

                # Skip targets that are already targeted by a classic fleet to avoid spamming
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
                # Register active flight to enforce the lock
                self.sent_fleets_tracker[best_target.id] = obs.step + best_travel_turns

        return moves
