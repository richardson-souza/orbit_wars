import time
import os
import json
from typing import List, Dict, Any
from kaggle_environments import make, evaluate


def run_arena(num_matches: int = 100):
    print("=" * 60)
    print("               ORBIT WARS LOCAL ARENA EVALUATOR")
    print("=" * 60)
    print(
        f"Goal: Win Rate > 55% over {num_matches} matches against baseline starter agent."
    )

    wins = 0
    losses = 0
    ties = 0
    total_duration = 0.0
    act_durations: List[float] = []

    os.makedirs("docs/replays", exist_ok=True)

    print("\nStarting evaluation loop...")
    for match_idx in range(num_matches):
        if match_idx % 2 == 0:
            agents = ["main.py", "starter"]
            our_idx = 0
        else:
            agents = ["starter", "main.py"]
            our_idx = 1

        start_time = time.perf_counter()

        env = make("orbit_wars", configuration={"episodeSteps": 200}, debug=False)
        env.run(agents)

        match_duration = time.perf_counter() - start_time
        total_duration += match_duration

        steps = env.toJSON()["steps"]
        final_step = steps[-1]

        our_reward = final_step[our_idx].get("reward", -1)
        opponent_reward = final_step[1 - our_idx].get("reward", -1)

        if our_reward == 1 and opponent_reward == -1:
            wins += 1
            outcome = "WIN"
        elif our_reward == -1 and opponent_reward == 1:
            losses += 1
            outcome = "LOSS"
            replay_path = f"docs/replays/loss_match_{match_idx}.json"
            with open(replay_path, "w") as f:
                json.dump(env.toJSON(), f, indent=2)
        else:
            ties += 1
            outcome = "TIE"

        win_rate = (wins / (match_idx + 1)) * 100

        if (match_idx + 1) % 10 == 0 or match_idx == 0:
            print(
                f"Match {match_idx + 1:3d}/{num_matches:3d} | Result: {outcome:4s} | Win Rate: {win_rate:5.1f}% | Duration: {match_duration:.2f}s"
            )

    overall_win_rate = (wins / num_matches) * 100
    print("\n" + "=" * 60)
    print("                      EVALUATION RESULTS")
    print("=" * 60)
    print(f"Total Matches:    {num_matches}")
    print(f"Wins:             {wins}")
    print(f"Losses:           {losses}")
    print(f"Ties:             {ties}")
    print(f"Overall Win Rate: {overall_win_rate:.1f}%")
    print(f"Avg Match Time:   {total_duration / num_matches:.2f}s")
    print(f"Goal Met (>55%):  {'YES 🚀' if overall_win_rate > 55.0 else 'NO ⚠️'}")
    print("=" * 60)


if __name__ == "__main__":
    run_arena()
