import os
import sys
import json
from kaggle_environments import make


def main():
    print("=" * 60)
    print("        ORBIT WARS LOCAL SANDBOX RUNNER")
    print("=" * 60)

    print("Initializing environment...")
    env = make("orbit_wars", configuration={"episodeSteps": 100}, debug=True)

    print("Running match: Our MCTS Agent vs. Kaggle Starter Agent...")
    env.run(["main.py", "starter"])

    steps = env.toJSON()["steps"]
    final_step = steps[-1]

    print("\n" + "=" * 60)
    print("               MATCH COMPLETED")
    print("=" * 60)
    print(f"Total Steps: {len(steps)}")

    for i, agent_state in enumerate(final_step):
        reward = agent_state.get("reward")
        status = agent_state.get("status")
        print(f"Player {i} ({'MCTS Agent' if i == 0 else 'Starter Agent'}):")
        print(f"  Status: {status}")
        print(f"  Reward: {reward}")

    print("=" * 60)


if __name__ == "__main__":
    main()
