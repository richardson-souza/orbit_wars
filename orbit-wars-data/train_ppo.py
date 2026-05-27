import os
import argparse
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from core.ppo_env import OrbitWarsGymEnv

def main():
    import sys
    parser = argparse.ArgumentParser(description="Train PPO Reinforcement Learning Agent for Orbit Wars (High Performance).")
    parser.add_argument("--steps", type=int, default=150000, help="Number of timesteps to train.")
    parser.add_argument("--save-path", type=str, default="models/ppo_orbit_wars.zip", help="Path to save model weights.")
    parser.add_argument("--envs", type=int, default=8, help="Number of parallel environments.")
    
    # Detect Jupyter / Kaggle / Colab kernel execution to prevent SystemExit: 2
    is_jupyter = any(x in sys.argv[0].lower() for x in ["kernel", "ipykernel", "colab"]) or any("kernel" in arg for arg in sys.argv)
    if is_jupyter:
        args = parser.parse_args(args=[])
    else:
        args = parser.parse_args()

    print("=" * 70)
    print("   ORBIT WARS: HIGH-PERFORMANCE VEC-ENVIRONMENT PPO TRAINER")
    print("=" * 70)
    print(f"Goal: Train PPO neural policy for {args.steps} steps.")
    print(f"Parallel Simulator Envs:  {args.envs} (SubprocVecEnv)")
    print(f"Model Save Path:          {args.save_path}")
    
    # Determine hardware device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Hardware Accelerator:     {device.upper()}")
    print("-" * 70)

    # Make sure output directory exists
    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)

    # 1. Initialize vectorized multiprocessed environment wrapper
    print(f"Launching {args.envs} parallel simulators in child processes...")
    env = make_vec_env(
        OrbitWarsGymEnv,
        n_envs=args.envs,
        seed=42,
        vec_env_cls=SubprocVecEnv
    )

    # 2. Setup the PPO model with standard Multi-Layer Perceptron (MLP) policy
    print("Configuring PPO model architecture (SB3 MLP Policy)...")
    model = PPO(
        policy="MlpPolicy",
        env=env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        verbose=1,
        device=device,
        tensorboard_log=None
    )

    # 3. Execute training loop
    print("\nStarting high-performance reinforcement learning training loop...")
    try:
        model.learn(total_timesteps=args.steps)
        print("\nTraining completed successfully!")
    except KeyboardInterrupt:
        print("\nTraining cleanly interrupted. Saving current model state...")

    # 4. Save model weights
    model.save(args.save_path)
    print(f"Weights saved successfully to {args.save_path}.")
    print("=" * 70)

if __name__ == "__main__":
    main()
