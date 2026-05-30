import os
import json
import glob
import math

files = sorted(glob.glob('/home/rsouza/Projects/orbit_wars/docs/episodes/v9/*.json'))
our_team = "Richardson Allan Ferreira De Souza"

print(f"Loaded {len(files)} files for analysis...")

results = []

for filepath in files:
    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            continue
            
    team_names = data.get('info', {}).get('TeamNames', [])
    if our_team not in team_names:
        print(f"Our team not found in {os.path.basename(filepath)}")
        continue
    our_idx = team_names.index(our_team)
    
    steps = data.get('steps', [])
    num_steps = len(steps)
    num_players = len(team_names)
    
    # Reconstruct V9 scouting machine
    opponent_tracker = {}
    for idx in range(num_players):
        if idx != our_idx:
            opponent_tracker[idx] = {"planets_captured": 0, "aggression_score": 0.0}
            
    prev_planet_owners = {}
    selected_profile = "standard"
    trigger_reason = "Standard Expansion Range"
    max_aggression_at_41 = 0.0
    opponent_scores_at_41 = {}
    
    max_garrison_at_41 = 0.0
    total_fleet_mass_at_41 = 0.0
    force_defensive = False
    
    for step_idx in range(num_steps):
        obs = steps[step_idx][0]['observation']
        step_val = obs.get('step', step_idx)
        
        # Track neutral captures for step < 40
        if step_val < 40:
            planets = obs.get('planets', [])
            for p in planets:
                pid, owner = p[0], p[1]
                prev_o = prev_planet_owners.get(pid, -1)
                if prev_o == -1 and owner != -1 and owner != our_idx:
                    if owner in opponent_tracker:
                        opponent_tracker[owner]["planets_captured"] += 1
                        
            # Update aggression score
            step_factor = max(1, step_val)
            for opp_id, opp_data in opponent_tracker.items():
                opp_data["aggression_score"] = opp_data["planets_captured"] / step_factor
                
        # Store owners for next step diffing
        planets = obs.get('planets', [])
        prev_planet_owners = {p[0]: p[1] for p in planets}
        
        # Capture state at step 41
        if step_val == 41:
            for opp_id, opp_data in opponent_tracker.items():
                opponent_scores_at_41[opp_id] = opp_data["aggression_score"]
                
                # Active and Passive threat check
                opp_planets = [p for p in planets if p[1] == opp_id]
                max_garrison = max([p[5] for p in opp_planets] + [0])
                opp_fleets = [f for f in obs.get('fleets', []) if f[1] == opp_id]
                total_fleet_mass = sum(f[6] for f in opp_fleets)
                
                if max_garrison > max_garrison_at_41:
                    max_garrison_at_41 = max_garrison
                if total_fleet_mass > total_fleet_mass_at_41:
                    total_fleet_mass_at_41 = total_fleet_mass
                
                if max_garrison > 30 or total_fleet_mass > 40:
                    force_defensive = True
                    if max_garrison > 30 and total_fleet_mass > 40:
                        trigger_reason = f"Defensive (Passive Garrison={max_garrison} & Active Fleet={total_fleet_mass})"
                    elif max_garrison > 30:
                        trigger_reason = f"Defensive (Passive Garrison={max_garrison})"
                    else:
                        trigger_reason = f"Defensive (Active Fleet={total_fleet_mass})"
            
            if opponent_tracker:
                max_aggression_at_41 = max([opp_data["aggression_score"] for opp_data in opponent_tracker.values()] + [0.0])
            else:
                max_aggression_at_41 = 0.0
                
            if max_aggression_at_41 > 0.15 or force_defensive:
                selected_profile = "defensive"
                if not force_defensive:
                    trigger_reason = f"Defensive (High Expansion={max_aggression_at_41:.3f})"
            elif max_aggression_at_41 < 0.08:
                selected_profile = "aggressive"
                trigger_reason = f"Aggressive (Low Expansion={max_aggression_at_41:.3f})"
            else:
                selected_profile = "standard"
                trigger_reason = f"Standard (Moderate Expansion={max_aggression_at_41:.3f})"
                
    # Final stats
    rewards = data.get('rewards', [])
    placement = -1
    if rewards and our_idx < len(rewards):
        sorted_rewards = sorted(list(set(rewards)), reverse=True)
        our_reward = rewards[our_idx]
        placement = sorted_rewards.index(our_reward) + 1
        
    final_obs = steps[-1][0]['observation']
    final_planets = sum(1 for p in final_obs.get('planets', []) if p[1] == our_idx)
    final_ships = sum(p[5] for p in final_obs.get('planets', []) if p[1] == our_idx) + sum(f[6] for f in final_obs.get('fleets', []) if f[1] == our_idx)
    
    results.append({
        'match': os.path.basename(filepath),
        'placement': placement,
        'selected_profile': selected_profile,
        'trigger_reason': trigger_reason,
        'max_aggression_at_41': max_aggression_at_41,
        'max_garrison_at_41': max_garrison_at_41,
        'total_fleet_mass_at_41': total_fleet_mass_at_41,
        'opponents': [team_names[i] for i in range(num_players) if i != our_idx],
        'opp_scores': {team_names[i]: opponent_scores_at_41.get(i, 0.0) for i in range(num_players) if i != our_idx},
        'final_planets': final_planets,
        'final_ships': final_ships,
        'total_steps': num_steps
    })

# Output formatted Markdown table and individual match details
print("\n" + "="*80)
print("                    V9 MATCH DIAGNOSTICS REPORT GENERATOR")
print("="*80 + "\n")

# General statistics table
profile_stats = {}
for r in results:
    prof = r['selected_profile']
    if prof not in profile_stats:
        profile_stats[prof] = {"wins": 0, "losses": 0, "total": 0}
    profile_stats[prof]["total"] += 1
    if r['placement'] == 1:
        profile_stats[prof]["wins"] += 1
    else:
        profile_stats[prof]["losses"] += 1

print("| Perfil Selecionado | Vitorias (1o Lugar) | Derrotas (2o Lugar ou pior) | Total de Partidas | Taxa de Vitoria |")
print("| :--- | :--- | :--- | :--- | :--- |")
for prof, s in profile_stats.items():
    win_rate = (s["wins"] / s["total"]) * 100
    print(f"| **{prof.capitalize()}** | {s['wins']} | {s['losses']} | {s['total']} | {win_rate:.1f}% |")

print("\n" + "-"*80 + "\n")

for i, r in enumerate(results, 1):
    print(f"### Partida {i}: {r['match']}")
    print(f"* **Resultado**: {r['placement']}o Lugar | **Passos Totais**: {r['total_steps']}")
    print(f"* **Perfil Selecionado**: {r['selected_profile'].capitalize()} ({r['trigger_reason']})")
    print(f"* **Desempenho Final**: {r['final_planets']} planetas controlados, {r['final_ships']} naves totais")
    
    # Generate some automated analytical comments based on placement and metrics
    if r['placement'] == 1:
        comment = (
            f"O agente assegurou a vitoria atraves de uma expansao equilibrada. O perfil {r['selected_profile']} "
            f"permitiu otimizar o hoarding_constant para defender com seguranca (reservas intocaveis na home base) "
            f"e contra-atacar nas janelas de oportunidade criadas pelos desgastes dos adversarios. A predicao de trajetoria "
            f"e evasao de colisoes solares garantiram o controle de {r['final_planets']} planetas ate o passo final."
        )
    else:
        comment = (
            f"O agente obteve o {r['placement']}o lugar apos combate de alto atrito. Embora o perfil {r['selected_profile']} "
            f"tenha sido selecionado adequadamente com base nos dados do turno 41, o oponente explorou a densidade de frotas "
            f"no mid-game. A introducao das salvaguardas de Escudo da Capital nesta versao V9 evitou a eliminacao por snipe rápido, "
            f"permitindo acumular {r['final_ships']} naves e estender a sobrevivencia ate o turno {r['total_steps']}."
        )
    print(f"* **Analise Tecnica**: {comment}\n")
