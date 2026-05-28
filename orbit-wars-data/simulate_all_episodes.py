import os
import glob
import json
from kaggle_environments import make

def run_simulation_benchmarks():
    print("=" * 80)
    print("        ORBIT WARS: MULTI-MODEL ARENA BENCHMARK COMPARISON")
    print("=" * 80)
    print("Evaluating: 1. Improved Heuristic (main.py)")
    print("            2. Reinforcement Learning PPO (ppo_main.py)")
    print("Against baseline 'starter' agent on all historical seeds.")
    print("-" * 80)

    filepaths = sorted(glob.glob("docs/episodes/*.json"))
    
    heur_wins = 0
    ppo_wins = 0
    total_played = 0

    results = []

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        if filename == "summary.json":
            continue
            
        episode_id = filename.replace(".json", "")
        
        with open(filepath) as f:
            data = json.load(f)
            
        info = data.get("info", {})
        seed = info.get("seed")
        num_agents = len(data["steps"][0])
        
        # Determine who our team was and original outcome
        team_names = info.get("TeamNames", [])
        our_idx = -1
        for idx, name in enumerate(team_names):
            if "Richardson" in name or "rsouza" in name:
                our_idx = idx
                break
        
        if our_idx == -1:
            our_idx = 0
            
        original_reward = data["steps"][-1][our_idx].get("reward", -1)
        original_outcome = "WIN" if original_reward == 1 else ("LOSS" if original_reward == -1 else "TIE")
        
        # 1. Run Improved Heuristic
        heur_agents = ["main.py"] + ["starter"] * (num_agents - 1)
        env_heur = make("orbit_wars", configuration={"seed": seed, "episodeSteps": 500}, debug=False)
        env_heur.run(heur_agents)
        
        final_heur = env_heur.steps[-1]
        heur_reward = final_heur[0].get("reward", -1)
        heur_opp_rewards = [final_heur[i].get("reward", -1) for i in range(1, num_agents)]
        
        if heur_reward == 1 and all(r == -1 for r in heur_opp_rewards):
            heur_outcome = "WIN"
            heur_wins += 1
        elif heur_reward == -1:
            heur_outcome = "LOSS"
        else:
            heur_outcome = "TIE"
            
        # 2. Run PPO Agent
        ppo_agents = ["ppo_main.py"] + ["starter"] * (num_agents - 1)
        env_ppo = make("orbit_wars", configuration={"seed": seed, "episodeSteps": 500}, debug=False)
        env_ppo.run(ppo_agents)
        
        final_ppo = env_ppo.steps[-1]
        ppo_reward = final_ppo[0].get("reward", -1)
        ppo_opp_rewards = [final_ppo[i].get("reward", -1) for i in range(1, num_agents)]
        
        if ppo_reward == 1 and all(r == -1 for r in ppo_opp_rewards):
            ppo_outcome = "WIN"
            ppo_wins += 1
        elif ppo_reward == -1:
            ppo_outcome = "LOSS"
        else:
            ppo_outcome = "TIE"
            
        total_played += 1
        
        print(f"Episode {episode_id:8s} ({num_agents}p) | Seed: {seed:10d} | Orig: {original_outcome:4s} | Heur: {heur_outcome:4s} | PPO: {ppo_outcome:4s}")
        results.append({
            "episode": episode_id,
            "players": num_agents,
            "seed": seed,
            "original": original_outcome,
            "heuristic": heur_outcome,
            "ppo": ppo_outcome
        })

    heur_win_rate = (heur_wins / total_played) * 100
    ppo_win_rate = (ppo_wins / total_played) * 100
    
    print("\n" + "=" * 80)
    print("                      AGGREGATED ARENA RESULTS COMPARISON")
    print("=" * 80)
    print(f"Total Matches Simulated:      {total_played}")
    print(f"Original Win Rate:            {(sum(1 for r in results if r['original'] == 'WIN') / total_played) * 100:.1f}%")
    print(f"Improved Heuristic Win Rate:  {heur_win_rate:.1f}% ({heur_wins} Wins)")
    print(f"Reinforcement Learning PPO:   {ppo_win_rate:.1f}% ({ppo_wins} Wins)")
    print("-" * 80)
    print(f"Heuristic Delta:             {heur_win_rate - (sum(1 for r in results if r['original'] == 'WIN') / total_played) * 100:+.1f}%")
    print(f"PPO RL Delta:                 {ppo_win_rate - (sum(1 for r in results if r['original'] == 'WIN') / total_played) * 100:+.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    run_simulation_benchmarks()
