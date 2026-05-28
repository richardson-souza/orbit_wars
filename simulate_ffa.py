import os
import sys
import json
import argparse
from kaggle_environments import make

def parse_final_ships(env):
    """
    Parse the final ship counts for all 4 players from the environment's final state.
    Each planet is represented as a list: [id, owner, x, y, radius, ships, production]
    Each fleet is represented as a list: [id, owner, x, y, angle, from_planet_id, ships]
    """
    final_step = env.steps[-1]
    # Observation is shared among players
    obs = final_step[0].get("observation", {})
    if not obs:
        return [0, 0, 0, 0]
        
    ship_counts = [0, 0, 0, 0]
    
    # Sum ships on planets
    planets = obs.get("planets", [])
    for p in planets:
        if len(p) > 5:
            owner = p[1]  # owner
            ships = p[5]  # ships
            if 0 <= owner < 4:
                ship_counts[owner] += ships
            
    # Sum ships in fleets
    fleets = obs.get("fleets", [])
    for f in fleets:
        if len(f) > 6:
            owner = f[1]  # owner
            ships = f[6]  # ships
            if 0 <= owner < 4:
                ship_counts[owner] += ships
            
    return ship_counts

def calculate_placements(ship_counts):
    """
    Rank players 0-3 based on final ship counts.
    Returns a list of placements (1-indexed: 1 = first, 4 = fourth).
    """
    # Create (player_idx, ship_count) tuples
    player_ships = list(enumerate(ship_counts))
    # Sort descending by ship count
    player_ships.sort(key=lambda x: x[1], reverse=True)
    
    placements = [0, 0, 0, 0]
    current_rank = 1
    for rank_idx, (player_idx, ships) in enumerate(player_ships):
        # Resolve ties: same ship count gets same placement rank
        if rank_idx > 0 and ships == player_ships[rank_idx - 1][1]:
            placements[player_idx] = placements[player_ships[rank_idx - 1][0]]
        else:
            placements[player_idx] = rank_idx + 1
            
    return placements

def run_simulation_arena(scenario, num_seeds):
    print("=" * 95)
    print("                   ORBIT WARS: 4-PLAYER MULTI-AGENT ARENA BENCHMARK")
    print("=" * 95)
    print(f"Scenario: {scenario.upper()}")
    print(f"Number of Matches: {num_seeds}")
    print("-" * 95)

    # Agent map
    # 0 = Elite Tactician (elite_main.py)
    # 1 = Improved Heuristic (main.py)
    # 2 = Nearest Planet Sniper (starter)
    
    if scenario == "shark_tank":
        # 1x Elite vs 3x Heuristics
        agents = ["elite_main.py", "main.py", "main.py", "main.py"]
        agent_names = ["Elite Tactician", "Heuristic 1", "Heuristic 2", "Heuristic 3"]
        elite_indices = [0]
    elif scenario == "asymmetric_mirror":
        # 2x Elite vs 2x Heuristics
        agents = ["elite_main.py", "elite_main.py", "main.py", "main.py"]
        agent_names = ["Elite 1", "Elite 2", "Heuristic 1", "Heuristic 2"]
        elite_indices = [0, 1]
    elif scenario == "cold_war":
        # 4x Elite Tacticians
        agents = ["elite_main.py", "elite_main.py", "elite_main.py", "elite_main.py"]
        agent_names = ["Elite 1", "Elite 2", "Elite 3", "Elite 4"]
        elite_indices = [0, 1, 2, 3]
    else:  # balanced / classic
        # 1x Elite vs 1x Heuristics vs 2x Starters
        agents = ["elite_main.py", "main.py", "starter", "starter"]
        agent_names = ["Elite Tactician", "Heuristic Scorer", "Starter Sniper 1", "Starter Sniper 2"]
        elite_indices = [0]

    # Historical robust seeds to avoid biased layout outcomes
    seeds = [
        0, 1576566668, 749729973, 1009547534, 1502729423,
        12345, 54321, 99999, 88888, 77777,
        11111, 22222, 33333, 44444, 55555,
        66666, 12121, 23232, 34343, 45454
    ][:num_seeds]

    # Match results tracking
    elite_placements = []
    elite_survivals = 0
    elite_wins = 0
    elite_final_ships = []
    
    total_played = 0

    for match_idx, seed in enumerate(seeds):
        env = make("orbit_wars", configuration={"seed": seed, "episodeSteps": 500}, debug=False)
        env.run(agents)
        
        final_ships = parse_final_ships(env)
        placements = calculate_placements(final_ships)
        
        total_played += 1
        
        # Calculate stats for Elite agents in this match
        match_elite_places = [placements[idx] for idx in elite_indices]
        match_elite_ships = [final_ships[idx] for idx in elite_indices]
        
        elite_placements.extend(match_elite_places)
        elite_final_ships.extend(match_elite_ships)
        
        for idx in elite_indices:
            if placements[idx] == 1:
                elite_wins += 1
            if final_ships[idx] > 0:
                elite_survivals += 1
                
        # Format a beautifully human-readable line for this match
        ships_str = ", ".join([f"{name}: {final_ships[i]} (P{placements[i]})" for i, name in enumerate(agent_names)])
        print(f"Match {match_idx+1:2d} | Seed: {seed:10d} | {ships_str}")

    # Compute aggregate stats for Elite Tacticians
    num_elite_instances = len(elite_indices) * total_played
    avg_placement = sum(elite_placements) / num_elite_instances
    win_rate = (elite_wins / num_elite_instances) * 100
    survival_rate = (elite_survivals / num_elite_instances) * 100
    avg_ships = sum(elite_final_ships) / num_elite_instances

    print("\n" + "=" * 95)
    print("                           AGGREGATED ARENA RESULTS SUMMARY")
    print("=" * 95)
    print(f"Scenario:                    {scenario.upper()}")
    print(f"Total Matches Simulated:      {total_played}")
    print(f"Total Elite Instances:       {num_elite_instances}")
    print(f"Average Placement Rank:       {avg_placement:.2f} (1.00 = Perfect First, 4.00 = Last)")
    print(f"Win Rate (1st Place):        {win_rate:.1f}%")
    print(f"Survival Rate:               {survival_rate:.1f}%")
    print(f"Average Ships at Turn 500:   {avg_ships:.1f}")
    print("=" * 95)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orbit Wars 4-Player FFA Sandbox Simulator")
    parser.add_argument(
        "--scenario",
        type=str,
        default="balanced",
        choices=["shark_tank", "asymmetric_mirror", "cold_war", "balanced"],
        help="Confrontation scenario matrix to benchmark"
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=10,
        help="Number of matches to simulate (max 20)"
    )
    args = parser.parse_args()
    
    run_simulation_arena(args.scenario, args.seeds)
