import os
import sys
import json
import argparse
import optuna

# Ensure workspace root is in PYTHONPATH
sys.path.append(os.getcwd())

from sandbox_evaluator import run_simulation, HISTORICAL_SEEDS

def optimize_aggressive(n_trials: int, seeds: list) -> dict:
    print("\n" + "="*80)
    print("                    STARTING OPTUNA STUDY: AGGRESSIVE PROFILE")
    print("="*80)
    
    def objective(trial):
        params = {
            'hoarding_constant': trial.suggest_float('hoarding_constant', 1.0, 3.0),
            'evacuation_trigger': trial.suggest_int('evacuation_trigger', 2, 8),
            'max_attack_dist': trial.suggest_float('max_attack_dist', 30.0, 100.0),
            'early_rush_limit': trial.suggest_int('early_rush_limit', 4, 15)
        }
        
        results = run_simulation("balanced", seeds, params, verbose=False)
        
        avg_planets_100 = sum(r['planets_100'] for r in results) / len(results)
        return avg_planets_100

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    
    print(f"Aggressive Best Params: {study.best_params}")
    print(f"Aggressive Best Value (Planets@100): {study.best_value:.2f}")
    return study.best_params

def optimize_defensive(n_trials: int, seeds: list) -> dict:
    print("\n" + "="*80)
    print("                    STARTING OPTUNA STUDY: DEFENSIVE PROFILE")
    print("="*80)
    
    def objective(trial):
        params = {
            'hoarding_constant': trial.suggest_float('hoarding_constant', 22.0, 35.0),
            'evacuation_trigger': trial.suggest_int('evacuation_trigger', 2, 8),
            'max_attack_dist': trial.suggest_float('max_attack_dist', 30.0, 100.0),
            'early_rush_limit': trial.suggest_int('early_rush_limit', 4, 15)
        }
        
        results = run_simulation("balanced", seeds, params, verbose=False)
        
        survival_rate = sum(1 for r in results if r['our_ships'] > 0) / len(results) * 100.0
        total_sun_losses = sum(r['sun_losses'] for r in results)
        total_oob_losses = sum(r['oob_losses'] for r in results)
        
        # Maximize survival rate while heavily penalizing sun/oob losses
        score = survival_rate - 0.1 * (total_sun_losses + total_oob_losses)
        return score

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    
    print(f"Defensive Best Params: {study.best_params}")
    print(f"Defensive Best Value: {study.best_value:.2f}")
    return study.best_params

def optimize_standard(n_trials: int, seeds: list) -> dict:
    print("\n" + "="*80)
    print("                    STARTING OPTUNA STUDY: STANDARD PROFILE")
    print("="*80)
    
    def objective(trial):
        params = {
            'hoarding_constant': trial.suggest_float('hoarding_constant', 10.0, 20.0),
            'evacuation_trigger': trial.suggest_int('evacuation_trigger', 2, 8),
            'max_attack_dist': trial.suggest_float('max_attack_dist', 30.0, 100.0),
            'early_rush_limit': trial.suggest_int('early_rush_limit', 4, 15)
        }
        
        results = run_simulation("balanced", seeds, params, verbose=False)
        
        avg_ships = sum(r['our_ships'] for r in results) / len(results)
        avg_placement = sum(r['our_placement'] for r in results) / len(results)
        
        # Maximize composite value of final ships and placement rank
        score = avg_ships * (5.0 - avg_placement)
        return score

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    
    print(f"Standard Best Params: {study.best_params}")
    print(f"Standard Best Value: {study.best_value:.2f}")
    return study.best_params

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optuna Bayesian Hyperparameter Optimization Engine")
    parser.add_argument("--trials", type=int, default=15, help="Number of trials per optimization study")
    parser.add_argument("--seeds", type=int, default=5, help="Number of seeds to run per trial")
    args = parser.parse_args()
    
    seeds = HISTORICAL_SEEDS[:args.seeds]
    
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    
    aggressive_params = optimize_aggressive(args.trials, seeds)
    defensive_params = optimize_defensive(args.trials, seeds)
    standard_params = optimize_standard(args.trials, seeds)
    
    profiles = {
        "aggressive": aggressive_params,
        "defensive": defensive_params,
        "standard": standard_params
    }
    
    with open("profiles.json", "w") as f:
        json.dump(profiles, f, indent=2)
        
    print("\n" + "="*80)
    print("                    SUCCESSFULLY EXPORTED PROFILES TO profiles.json")
    print("="*80)
    print(json.dumps(profiles, indent=2))
