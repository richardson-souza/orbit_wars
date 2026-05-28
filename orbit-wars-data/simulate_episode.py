import os
import sys
import json
from kaggle_environments import make

def simulate_episode(episode_id: int, agent_path: str = "main.py", opponent: str = "starter"):
    filepath = f"docs/episodes/{episode_id}.json"
    if not os.path.exists(filepath):
        print(f"Error: Episode file {filepath} not found.")
        return

    with open(filepath) as f:
        data = json.load(f)

    # Get seed and players
    info = data.get("info", {})
    seed = info.get("seed")
    num_agents = len(data["steps"][0])

    if seed is None:
        print(f"Error: Could not find seed for episode {episode_id}.")
        return

    print("=" * 60)
    print(f"   SIMULATING EPISODE {episode_id} LOCALLY (REPRODUCING MAP LAYOUT)")
    print("=" * 60)
    print(f"Original Seed:      {seed}")
    print(f"Number of Players:  {num_agents}")
    print(f"Agents playing:     {agent_path} vs. {opponent}")
    print("-" * 60)

    # Setup agents list
    if num_agents == 4:
        agents = [agent_path, opponent, "starter", "starter"]
    else:
        agents = [agent_path, opponent]

    # Initialize environment with the exact seed and steps
    env = make("orbit_wars", configuration={"seed": seed, "episodeSteps": 500}, debug=True)
    env.run(agents)

    print("\nMatch completed! Final states:")
    final = env.steps[-1]
    for idx, state in enumerate(final):
        reward = state.reward if hasattr(state, "reward") else state.get("reward")
        status = state.status if hasattr(state, "status") else state.get("status")
        team_names = data.get("info", {}).get("TeamNames", [])
        name = team_names[idx] if idx < len(team_names) else f"Player {idx}"
        print(f"Slot {idx} ({name}): reward={reward}, status={status}")
    print("=" * 60)

if __name__ == "__main__":
    episode = 77837891  # Default
    if len(sys.argv) > 1:
        try:
            episode = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 simulate_episode.py [episode_id] [agent_path] [opponent]")
            sys.exit(1)
            
    agent = sys.argv[2] if len(sys.argv) > 2 else "main.py"
    opponent = sys.argv[3] if len(sys.argv) > 3 else "starter"
    
    simulate_episode(episode, agent, opponent)
