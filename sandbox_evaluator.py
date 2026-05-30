import os
import sys
import json
import csv
import math
import argparse
import multiprocessing
from typing import List, Dict, Any, Tuple
from kaggle_environments import make

# Add workspace root to PYTHONPATH to ensure import correctness
sys.path.append(os.getcwd())

from strategies.elite_tactician import EliteTactician
from strategies.heuristic_scorer import HeuristicScorer

HISTORICAL_SEEDS = [
    0, 1576566668, 749729973, 1009547534, 1502729423,
    12345, 54321, 99999, 88888, 77777,
    11111, 22222, 33333, 44444, 55555,
    66666, 12121, 23232, 34343, 45454
]

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def parse_final_ships(env):
    final_step = env.steps[-1]
    obs = final_step[0].get("observation", {})
    if not obs:
        return [0, 0, 0, 0]
    ship_counts = [0, 0, 0, 0]
    for p in obs.get("planets", []):
        owner = p[1]
        ships = p[5]
        if 0 <= owner < 4:
            ship_counts[owner] += ships
    for f in obs.get("fleets", []):
        owner = f[1]
        ships = f[6]
        if 0 <= owner < 4:
            ship_counts[owner] += ships
    return ship_counts

def calculate_placements(ship_counts):
    player_ships = list(enumerate(ship_counts))
    player_ships.sort(key=lambda x: x[1], reverse=True)
    placements = [0, 0, 0, 0]
    for rank_idx, (player_idx, ships) in enumerate(player_ships):
        if rank_idx > 0 and ships == player_ships[rank_idx - 1][1]:
            placements[player_idx] = placements[player_ships[rank_idx - 1][0]]
        else:
            placements[player_idx] = rank_idx + 1
    return placements

def extract_telemetry(env, elite_idx=0) -> Dict[str, Any]:
    steps = env.steps
    num_steps = len(steps)
    
    planets_100 = 0
    planets_300 = 0
    planets_500 = 0
    
    total_idle_ships = 0
    steps_with_planets = 0
    
    active_fleets = {}
    sun_losses = 0
    oob_losses = 0
    
    for step_idx, step_data in enumerate(steps):
        obs = step_data[0].get("observation", {})
        if not obs:
            continue
            
        planets = obs.get("planets", [])
        fleets = obs.get("fleets", [])
        
        our_planets = [p for p in planets if p[1] == elite_idx]
        num_our_planets = len(our_planets)
        
        if step_idx == min(100, num_steps - 1):
            planets_100 = num_our_planets
        if step_idx == min(300, num_steps - 1):
            planets_300 = num_our_planets
        if step_idx == min(500, num_steps - 1):
            planets_500 = num_our_planets
            
        if num_our_planets > 0:
            steps_with_planets += 1
            total_idle_ships += sum(p[5] for p in our_planets)
            
        # Track fleet paths
        current_fids = set()
        for f in fleets:
            fid, fowner, fx, fy, fangle, ffrom, fships = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
            if fowner == elite_idx:
                current_fids.add(fid)
                if fid not in active_fleets:
                    active_fleets[fid] = {
                        'ships': fships,
                        'coords': [(fx, fy)]
                    }
                else:
                    active_fleets[fid]['coords'].append((fx, fy))
                    
        # Check terminated fleets
        terminated = set(active_fleets.keys()) - current_fids
        for fid in list(terminated):
            f_info = active_fleets.pop(fid)
            last_pos = f_info['coords'][-1]
            ships = f_info['ships']
            
            # Check OOB
            if last_pos[0] < 0 or last_pos[0] > 100 or last_pos[1] < 0 or last_pos[1] > 100:
                oob_losses += ships
            else:
                # Check Sun Collision
                d_sun = distance(last_pos, (50.0, 50.0))
                if d_sun < 6.0:
                    sun_losses += ships
                    
    avg_idle_ships = total_idle_ships / steps_with_planets if steps_with_planets > 0 else 0.0
    
    final_ships = 0
    last_obs = steps[-1][0].get("observation", {})
    if last_obs:
        for p in last_obs.get("planets", []):
            if p[1] == elite_idx:
                final_ships += p[5]
        for f in last_obs.get("fleets", []):
            if f[1] == elite_idx:
                final_ships += f[6]
                
    return {
        'final_ships': final_ships,
        'planets_100': planets_100,
        'planets_300': planets_300,
        'planets_500': planets_500,
        'avg_idle_ships': avg_idle_ships,
        'sun_losses': sun_losses,
        'oob_losses': oob_losses
    }

def run_single_match(args_tuple) -> Dict[str, Any]:
    seed, scenario, params = args_tuple
    
    # Initialize agents
    elite_strategy = EliteTactician(
        production_weight=params.get('production_weight', 12.0),
        distance_weight=params.get('distance_weight', 3.5),
        ship_cost_weight=params.get('ship_cost_weight', 0.1),
        comet_bonus=params.get('comet_bonus', 25.0),
        aggression_weight=params.get('aggression_weight', 1.0)
    )
    
    # Inject dynamically tuned hyperparameters
    elite_strategy.hoarding_constant = params.get('hoarding_constant', 6.0)
    elite_strategy.evacuation_trigger = params.get('evacuation_trigger', 4)
    elite_strategy.tot_min_turns = params.get('tot_min_turns', 15)
    elite_strategy.tot_max_turns = params.get('tot_max_turns', 45)
    
    def elite_agent(obs):
        return elite_strategy.get_actions(obs)
        
    heuristic_strategy = HeuristicScorer()
    def heuristic_agent(obs):
        return heuristic_strategy.get_actions(obs)
        
    if scenario == "shark_tank":
        agents = [elite_agent, heuristic_agent, heuristic_agent, heuristic_agent]
    else:  # balanced
        agents = [elite_agent, heuristic_agent, "starter", "starter"]
        
    env = make("orbit_wars", configuration={"seed": seed, "episodeSteps": 500}, debug=False)
    env.run(agents)
    
    final_ships = parse_final_ships(env)
    placements = calculate_placements(final_ships)
    
    telemetry = extract_telemetry(env, elite_idx=0)
    
    return {
        'seed': seed,
        'winner': placements.index(1),
        'our_placement': placements[0],
        'our_ships': final_ships[0],
        'heuristic_ships': final_ships[1],
        'opponent_ships_sum': sum(final_ships[1:]),
        'planets_100': telemetry['planets_100'],
        'planets_300': telemetry['planets_300'],
        'planets_500': telemetry['planets_500'],
        'avg_idle_ships': telemetry['avg_idle_ships'],
        'sun_losses': telemetry['sun_losses'],
        'oob_losses': telemetry['oob_losses'],
        'total_steps': len(env.steps)
    }

def run_simulation(scenario: str, seeds: List[int], params: Dict[str, Any], verbose: bool = True) -> List[Dict[str, Any]]:
    tasks = [(seed, scenario, params) for seed in seeds]
    
    num_workers = min(multiprocessing.cpu_count(), len(seeds))
    if verbose:
        print(f"Starting parallel execution with {num_workers} workers...")
        
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(run_single_match, tasks)
        
    return results

def print_results_summary(results: List[Dict[str, Any]], scenario: str, params: Dict[str, Any]):
    num_matches = len(results)
    our_placements = [r['our_placement'] for r in results]
    our_ships = [r['our_ships'] for r in results]
    wins = sum(1 for r in results if r['our_placement'] == 1)
    survivals = sum(1 for r in results if r['our_ships'] > 0)
    avg_placement = sum(our_placements) / num_matches
    avg_ships = sum(our_ships) / num_matches
    
    avg_idle = sum(r['avg_idle_ships'] for r in results) / num_matches
    total_sun_losses = sum(r['sun_losses'] for r in results)
    total_oob_losses = sum(r['oob_losses'] for r in results)
    
    avg_planets_100 = sum(r['planets_100'] for r in results) / num_matches
    avg_planets_300 = sum(r['planets_300'] for r in results) / num_matches
    avg_planets_500 = sum(r['planets_500'] for r in results) / num_matches

    print("\n" + "=" * 90)
    print("                    SANDBOX SIMULATOR METRIC EVALUATION REPORT")
    print("=" * 90)
    print(f"Scenario:                  {scenario.upper()}")
    print(f"Total Matches:             {num_matches}")
    print(f"Hyperparameters:           {json.dumps(params)}")
    print("-" * 90)
    print(f"Win Rate (1st Place):      {wins / num_matches * 100:.1f}%")
    print(f"Survival Rate (Ships > 0): {survivals / num_matches * 100:.1f}%")
    print(f"Average Placement Rank:    {avg_placement:.2f} (1 = Perfect, 4 = Last)")
    print(f"Average Final Ships:       {avg_ships:.1f}")
    print("-" * 90)
    print(f"Average Idle Ships/Turn:   {avg_idle:.1f} (Garrison Hoarding Indicator)")
    print(f"Total Ships Lost to Sun:   {total_sun_losses} (Path Finder Accuracy)")
    print(f"Total Ships Lost to OOB:   {total_oob_losses} (Arena Boundary Accuracy)")
    print("-" * 90)
    print(f"Avg Planets Controlled:")
    print(f"  - Turn 100:              {avg_planets_100:.2f} (Early Colonization)")
    print(f"  - Turn 300:              {avg_planets_300:.2f} (Mid-Game Consolidation)")
    print(f"  - Turn 500:              {avg_planets_500:.2f} (Late-Game Domination)")
    print("=" * 90 + "\n")

def save_csv(results: List[Dict[str, Any]], filename: str):
    keys = results[0].keys()
    with open(filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    print(f"Successfully saved detailed telemetry CSV to: {filename}")

def execute_grid_search(scenario: str, seeds: List[int], hoarding_grid: List[float], evac_grid: List[int]):
    print("=" * 90)
    print("                    GRID SEARCH HYPERPARAMETER OPTIMIZATION ENGINE")
    print("=" * 90)
    print(f"Scenario:     {scenario.upper()}")
    print(f"Seeds Count:  {len(seeds)}")
    print(f"Grid Size:    {len(hoarding_grid)} x {len(evac_grid)} = {len(hoarding_grid) * len(evac_grid)} configs")
    print("-" * 90)
    
    grid_results = []
    
    for hoarding in hoarding_grid:
        for evac in evac_grid:
            params = {
                'hoarding_constant': hoarding,
                'evacuation_trigger': evac
            }
            print(f"Testing configuration: hoarding={hoarding}, evac={evac}...")
            results = run_simulation(scenario, seeds, params, verbose=False)
            
            # Aggregate stats
            wins = sum(1 for r in results if r['our_placement'] == 1)
            survivals = sum(1 for r in results if r['our_ships'] > 0)
            avg_placement = sum(r['our_placement'] for r in results) / len(results)
            avg_ships = sum(r['our_ships'] for r in results) / len(results)
            avg_idle = sum(r['avg_idle_ships'] for r in results) / len(results)
            total_sun = sum(r['sun_losses'] for r in results)
            
            grid_results.append({
                'hoarding_constant': hoarding,
                'evacuation_trigger': evac,
                'win_rate': wins / len(results) * 100,
                'survival_rate': survivals / len(results) * 100,
                'avg_placement': avg_placement,
                'avg_ships': avg_ships,
                'avg_idle_ships': avg_idle,
                'sun_losses': total_sun
            })
            
    # Print Grid Search Table
    print("\n" + "=" * 100)
    print("                                GRID SEARCH FINAL SUMMARY TABLE")
    print("=" * 100)
    print(f"{'Hoarding':10s} | {'Evac':5s} | {'Win Rate':10s} | {'Survival':10s} | {'Avg Place':10s} | {'Avg Ships':10s} | {'Idle Ships':10s} | {'Sun Losses':10s}")
    print("-" * 100)
    for gr in grid_results:
        print(f"{gr['hoarding_constant']:10.1f} | {gr['evacuation_trigger']:5d} | {gr['win_rate']:9.1f}% | {gr['survival_rate']:9.1f}% | {gr['avg_placement']:10.2f} | {gr['avg_ships']:10.1f} | {gr['avg_idle_ships']:10.1f} | {gr['sun_losses']:10d}")
    print("=" * 100 + "\n")
    
    # Save Grid Search to CSV
    keys = grid_results[0].keys()
    grid_filename = "grid_search_results.csv"
    with open(grid_filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(grid_results)
    print(f"Saved comparative grid search results to: {grid_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orbit Wars High-Fidelity Validation Sandbox")
    parser.add_argument("--mode", type=str, default="evaluate", choices=["evaluate", "grid_search"], help="Execution mode")
    parser.add_argument("--scenario", type=str, default="balanced", choices=["shark_tank", "balanced"], help="FFA scenario Matrix")
    parser.add_argument("--seeds", type=int, default=10, help="Number of seeds to run (max 20)")
    parser.add_argument("--hoarding", type=float, default=6.0, help="Hoarding constant for evaluate mode")
    parser.add_argument("--evac", type=int, default=4, help="Evacuation trigger window for evaluate mode")
    
    args = parser.parse_args()
    seeds = HISTORICAL_SEEDS[:args.seeds]
    
    if args.mode == "evaluate":
        params = {
            'hoarding_constant': args.hoarding,
            'evacuation_trigger': args.evac
        }
        results = run_simulation(args.scenario, seeds, params)
        print_results_summary(results, args.scenario, params)
        save_csv(results, "sandbox_results.csv")
    else:
        # Define grid vectors
        hoarding_grid = [5.0, 6.0, 7.0]
        evac_grid = [3, 4, 5]
        execute_grid_search(args.scenario, seeds, hoarding_grid, evac_grid)
