import os
import json
import glob
import numpy as np

files = sorted(glob.glob('/home/rsouza/Projects/orbit_wars/docs/relatorio_de_avaliacao/grandmaster/isaiah_tufa_labs/*.json'))
grandmaster_name = "Isaiah @ Tufa Labs"

print(f"Loaded {len(files)} files for analysis...")

results = []

for filepath in files:
    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            continue
            
    team_names = data.get('info', {}).get('TeamNames', [])
    if grandmaster_name not in team_names:
        continue
    gm_idx = team_names.index(grandmaster_name)
    
    steps = data.get('steps', [])
    num_steps = len(steps)
    num_players = len(team_names)
    
    # Analyze expansion speed (captures by step 41)
    prev_planet_owners = {}
    planets_captured_at_41 = 0
    
    # For hoarding telemetry
    idle_ships_series = []
    production_series = []
    
    for step_idx in range(num_steps):
        obs = steps[step_idx][0]['observation']
        step_val = obs.get('step', step_idx)
        
        # Track neutral captures for step < 40
        if step_val < 40:
            planets = obs.get('planets', [])
            for p in planets:
                pid, owner = p[0], p[1]
                prev_o = prev_planet_owners.get(pid, -1)
                if prev_o == -1 and owner == gm_idx:
                    planets_captured_at_41 += 1
                        
        # Store owners for next step diffing
        planets = obs.get('planets', [])
        prev_planet_owners = {p[0]: p[1] for p in planets}
        
        # Telemetry for hoarding: count ships at owned planets vs their production
        our_planets = [p for p in planets if p[1] == gm_idx]
        if our_planets:
            total_ships = sum(p[5] for p in our_planets)
            total_prod = sum(p[6] for p in our_planets)
            idle_ships_series.append(total_ships)
            production_series.append(total_prod)
            
    # Final stats
    rewards = data.get('rewards', [])
    placement = -1
    if rewards and gm_idx < len(rewards):
        sorted_rewards = sorted(list(set(rewards)), reverse=True)
        gm_reward = rewards[gm_idx]
        placement = sorted_rewards.index(gm_reward) + 1
        
    final_obs = steps[-1][0]['observation']
    final_planets = sum(1 for p in final_obs.get('planets', []) if p[1] == gm_idx)
    final_ships = sum(p[5] for p in final_obs.get('planets', []) if p[1] == gm_idx) + sum(f[6] for f in final_obs.get('fleets', []) if f[1] == gm_idx)
    
    # Estimate average hoarding ratio (ships/production)
    avg_hoarding_ratio = 0.0
    if idle_ships_series and production_series:
        avg_ships = np.mean(idle_ships_series)
        avg_prod = np.mean(production_series)
        if avg_prod > 0:
            avg_hoarding_ratio = avg_ships / avg_prod

    results.append({
        'match': os.path.basename(filepath),
        'placement': placement,
        'opponents': [team_names[i] for i in range(num_players) if i != gm_idx],
        'final_planets': final_planets,
        'final_ships': final_ships,
        'total_steps': num_steps,
        'planets_captured_at_41': planets_captured_at_41,
        'avg_hoarding_ratio': avg_hoarding_ratio
    })

print("\n" + "="*80)
print("                    GRANDMASTER MATCH DIAGNOSTICS REPORT")
print("="*80 + "\n")

# Compute placements distribution
placements = [r['placement'] for r in results]
unique_placements, counts = np.unique(placements, return_counts=True)
dist = dict(zip(unique_placements, counts))

print(f"Total de Partidas Analisadas: {len(results)}")
print("Distribuicao de Colocacao:")
for plac, count in sorted(dist.items()):
    rate = (count / len(results)) * 100
    print(f"  - {plac}o Lugar: {count} partidas ({rate:.2f}%)")

avg_steps = np.mean([r['total_steps'] for r in results])
avg_planets = np.mean([r['final_planets'] for r in results])
avg_ships = np.mean([r['final_ships'] for r in results])
avg_caps_41 = np.mean([r['planets_captured_at_41'] for r in results])
avg_hoard = np.mean([r['avg_hoarding_ratio'] for r in results])

print("\nMetricas Medias de Jogo:")
print(f"  - Duracao Media da Partida: {avg_steps:.1f} turnos")
print(f"  - Planetas Finais Controlados: {avg_planets:.2f}")
print(f"  - Naves Finais: {avg_ships:.2f}")
print(f"  - Expansao Inicial (Capturas ate Turno 40): {avg_caps_41:.2f} planetas")
print(f"  - Hoarding Ratio Medio (Naves/Producao): {avg_hoard:.2f}")

print("\n" + "-"*80 + "\n")

# Top 5 most interesting losses/low placement matches
losses = [r for r in results if r['placement'] > 1]
print(f"Total de Derrotas (Placement > 1): {len(losses)}")
for i, r in enumerate(sorted(losses, key=lambda x: x['placement'], reverse=True)[:10], 1):
    print(f"\nDerrota Notavel {i}: {r['match']}")
    print(f"  - Resultado: {r['placement']}o Lugar | Passos Totais: {r['total_steps']}")
    print(f"  - Expansao Inicial: {r['planets_captured_at_41']} planetas | Hoarding Ratio: {r['avg_hoard'] if 'avg_hoard' in r else r['avg_hoarding_ratio']:.2f}")
    print(f"  - Oponentes: {', '.join(r['opponents'])}")
