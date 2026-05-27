import os
from kaggle_environments import make


def main():
    print("=" * 60)
    print("        ORBIT WARS LOCAL SANDBOX RUNNER (DOC STYLE)")
    print("=" * 60)

    print("Initializing environment with seed 42...")
    # Matches the official documentation configuration and seed
    env = make("orbit_wars", configuration={"seed": 42}, debug=True)

    print("Running match: main.py vs. random...")
    env.run(["main.py", "random"])

    print("\n" + "=" * 60)
    print("               MATCH COMPLETED")
    print("=" * 60)

    # View result using exact documentation syntax
    final = env.steps[-1]
    for i, s in enumerate(final):
        # Safe access supporting both attribute access and dict fallback
        reward = s.reward if hasattr(s, "reward") else s.get("reward")
        status = s.status if hasattr(s, "status") else s.get("status")
        print(f"Player {i}: reward={reward}, status={status}")

    print("=" * 60)


if __name__ == "__main__":
    main()
