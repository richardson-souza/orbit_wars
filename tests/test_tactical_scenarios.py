import math
import pytest
from core.observation import ParsedObservation, Planet, Fleet
from strategies.elite_tactician import EliteTactician

def create_mock_obs(player=0, step=0, planets=None, fleets=None, comet_planet_ids=None):
    if planets is None:
        planets = []
    if fleets is None:
        fleets = []
    if comet_planet_ids is None:
        comet_planet_ids = []
    return {
        "player": player,
        "step": step,
        "angular_velocity": 0.01,
        "remainingOverageTime": 60.0,
        "initial_planets": planets,
        "planets": planets,
        "fleets": fleets,
        "comet_planet_ids": comet_planet_ids,
        "comets": []
    }

# ==============================================================================
# CATEGORIA 1: SOBREVIVÊNCIA E EVACUAÇÃO (DODGING)
# ==============================================================================

def test_evacuation_mandatory_lethal():
    """
    Teste 1.1: Evasão Obrigatória sob Ameaça Letal
    Nosso planeta tem 20 naves (produz +2). Ameaça de 50 naves a 4 ticks de distância.
    O agente DEVE evacuar 100% das naves para o planeta seguro mais próximo.
    """
    agent = EliteTactician()
    agent.evacuation_trigger = 5
    
    planets = [
        [0, 0, 30.0, 30.0, 5.0, 20, 2],  # Nosso planeta (id 0) - longe do Sol a (50,50)
        [1, 0, 30.0, 50.0, 5.0, 10, 2],  # Nosso planeta seguro (id 1) - rota limpa do Sol
    ]
    # Fleet id 100 owned by opponent 1, flying straight down from (30, 42.5) to (30, 30)
    # Speed for 50 ships is approx 3.13. Distance is 12.5. Turns = ceil(12.5 / 3.13) = 4.
    fleets = [
        [100, 1, 30.0, 42.5, -math.pi/2, 10, 50]
    ]
    
    obs = create_mock_obs(player=0, step=10, planets=planets, fleets=fleets)
    moves = agent.get_actions(obs)
    
    # Assert that an evacuation move from planet 0 was scheduled
    evac_move = next((m for m in moves if m[0] == 0), None)
    assert evac_move is not None, "O agente deveria ter gerado um comando de evacuação para o planeta 0"
    assert evac_move[2] == 20, "O agente deveria evacuar 100% das 20 naves do planeta 0"

def test_evacuation_ignored_non_lethal():
    """
    Teste 1.2: Ignorar Ameaça Não-Letal (Anti-Ghost Fleet)
    Nosso planeta tem 50 naves. Ameaça de 5 naves a 1 tick de distância.
    O agente NÃO deve evacuar, pois a ameaça morre para a guarnição local.
    """
    agent = EliteTactician()
    agent.evacuation_trigger = 5
    
    planets = [
        [0, 0, 30.0, 30.0, 5.0, 50, 2],  # Nosso planeta (id 0)
        [1, 0, 30.0, 50.0, 5.0, 10, 2],  # Nosso planeta seguro (id 1)
    ]
    # Small fleet of 5 ships at T-1
    # Speed for 5 ships is approx 1.62. Distance is 1.5. Turns = ceil(1.5 / 1.62) = 1.
    fleets = [
        [100, 1, 30.0, 31.5, -math.pi/2, 10, 5]
    ]
    
    obs = create_mock_obs(player=0, step=10, planets=planets, fleets=fleets)
    moves = agent.get_actions(obs)
    
    # Verify no evacuation command was sent from planet 0
    evac_move = next((m for m in moves if m[0] == 0), None)
    if evac_move is not None:
        assert evac_move[2] < 50, "O agente não deveria evacuar o planeta 0 frente a uma ameaça não-letal"

def test_evacuation_ignored_false_positive():
    """
    Teste 1.3: Ignorar Falso Positivo (Rota de Passagem)
    Uma frota inimiga de 200 naves passa próxima, mas o cálculo de física comprova que ela passará reto.
    O agente NÃO deve evacuar.
    """
    agent = EliteTactician()
    agent.evacuation_trigger = 5
    
    planets = [
        [0, 0, 30.0, 30.0, 5.0, 30, 2],  # Nosso planeta (id 0)
        [1, 0, 30.0, 50.0, 5.0, 10, 2],  # Nosso planeta seguro (id 1)
    ]
    # Fleet flying east from (10, 45) to (90, 45) - completely bypasses the planet at (30, 30)
    fleets = [
        [100, 1, 10.0, 45.0, 0.0, 10, 200]
    ]
    
    obs = create_mock_obs(player=0, step=10, planets=planets, fleets=fleets)
    moves = agent.get_actions(obs)
    
    evac_move = next((m for m in moves if m[0] == 0), None)
    if evac_move is not None:
        assert evac_move[2] < 30, "O agente não deveria evacuar o planeta 0 para frotas que passam longe do planeta"

# ==============================================================================
# CATEGORIA 2: MÁQUINA DE ESTADOS E RASTREAMENTO (SCOUTING)
# ==============================================================================

def test_scouting_death_star_trigger():
    """
    Teste 2.1: Gatilho de Ameaça Passiva (Estrela da Morte)
    O inimigo tem 0 capturas mas acumulou 250 naves na base principal.
    A agressão deve disparar e carregar o Perfil Defensivo no turno 41.
    """
    agent = EliteTactician()
    agent.opponent_tracker = {
        1: {"planets_captured": 0, "aggression_score": 0.0},
        2: {"planets_captured": 0, "aggression_score": 0.0},
        3: {"planets_captured": 0, "aggression_score": 0.0}
    }
    
    planets = [
        [0, 0, 20.0, 20.0, 5.0, 20, 2],   # Nosso planeta
        [1, 1, 80.0, 80.0, 5.0, 250, 2],  # Base inimiga acumulando 250 naves (Estrela da Morte!)
    ]
    
    obs = create_mock_obs(player=0, step=41, planets=planets, fleets=[])
    agent.get_actions(obs)
    
    assert agent.profile_locked is True
    assert agent.hoarding_constant >= 6.0, "O agente deveria ter ativado o perfil DEFENSIVO devido ao hoarding massivo do inimigo"

def test_scouting_rush_trigger():
    """
    Teste 2.2: Gatilho de Expansão (Rush)
    O inimigo capturou 6 planetas neutros em 40 turnos.
    O bot deve carregar o Perfil Defensivo para frear o snowball do oponente.
    """
    agent = EliteTactician()
    agent.opponent_tracker = {
        1: {"planets_captured": 6, "aggression_score": 0.20},  # Set to > 0.15
        2: {"planets_captured": 0, "aggression_score": 0.0},
        3: {"planets_captured": 0, "aggression_score": 0.0}
    }
    planets = [
        [0, 0, 20.0, 20.0, 5.0, 20, 2],
        [1, 1, 80.0, 80.0, 5.0, 20, 2],
    ]
    
    obs = create_mock_obs(player=0, step=41, planets=planets, fleets=[])
    agent.get_actions(obs)
    
    assert agent.profile_locked is True
    assert agent.hoarding_constant >= 6.0, "O agente deveria ter ativado o perfil DEFENSIVO para conter a expansão veloz"

def test_scouting_transition_lock():
    """
    Teste 2.3: Trava de Transição (Golden Rule Lock)
    No turno 150, o inimigo que era passivo captura 3 planetas repentinamente.
    O perfil do bot NÃO deve mudar, respeitando a trava de abertura.
    """
    agent = EliteTactician()
    agent.profiles["standard"]["hoarding_constant"] = 4.5
    agent.apply_profile("standard")
    agent.profile_locked = True
    
    agent.opponent_tracker = {
        1: {"planets_captured": 0, "aggression_score": 0.0},
        2: {"planets_captured": 0, "aggression_score": 0.0},
        3: {"planets_captured": 0, "aggression_score": 0.0}
    }
    
    planets = [
        [0, 0, 20.0, 20.0, 5.0, 20, 2],
        [1, 1, 80.0, 80.0, 5.0, 20, 2],
    ]
    obs = create_mock_obs(player=0, step=150, planets=planets, fleets=[[200, 1, 50.0, 50.0, 0.0, 1, 100]])
    agent.get_actions(obs)
    
    assert 3.0 < agent.hoarding_constant < 6.0, "O perfil não deveria mudar no mid-game, respeitando o Golden Rule Lock"

# ==============================================================================
# CATEGORIA 3: ECONOMIA E ALOCAÇÃO DE FORÇAS (HOARDING & SURPLUS)
# ==============================================================================

def test_economy_hard_floor():
    """
    Teste 3.1: Escudo Absoluto da Capital (Hard Floor)
    Base principal de produção 5, com 100 naves. Nenhum inimigo no mapa.
    O agente NUNCA pode enviar mais do que 100 - (produção * 5) = 75 naves.
    """
    agent = EliteTactician()
    agent.apply_profile("standard")
    agent.hoarding_constant = 4.0
    
    planets = [
        [0, 0, 50.0, 50.0, 5.0, 100, 5],  # Capital (prod 5, 100 ships)
        [1, -1, 70.0, 50.0, 5.0, 10, 1],  # Target neutro próximo
    ]
    
    obs = create_mock_obs(player=0, step=125, planets=planets, fleets=[])
    moves = agent.get_actions(obs)
    
    launch_move = next((m for m in moves if m[0] == 0), None)
    if launch_move is not None:
        assert launch_move[2] <= 75, "O agente violou o Escudo da Capital enviando mais do que o limite permitido de 75 naves"

def test_economy_peaceful_front_release():
    """
    Teste 3.2: Liberação de Front Pacífico
    Um planeta de produção 1 no canto do mapa, a 80 unidades de qualquer inimigo.
    A guarnição de reserva dinâmica deve decair para perto de 1.0 * produção.
    """
    agent = EliteTactician()
    agent.apply_profile("standard")
    agent.hoarding_constant = 4.0
    
    planets = [
        [0, 0, 10.0, 10.0, 5.0, 30, 1],   # Planeta no canto (prod 1)
        [1, -1, 30.0, 10.0, 5.0, 5, 1],   # Alvo próximo
        [2, 1, 90.0, 90.0, 5.0, 20, 2],   # Inimigo longe (distância 113)
    ]
    
    obs = create_mock_obs(player=0, step=125, planets=planets, fleets=[])
    moves = agent.get_actions(obs)
    
    launch_move = next((m for m in moves if m[0] == 0), None)
    if launch_move is not None:
        assert launch_move[2] > 15, "O agente deveria ter liberado quase todo o seu saldo no front pacífico"

def test_economy_micro_spam_blocked():
    """
    Teste 3.3: Bloqueio de Micro-Spam
    Nosso planeta com produção 1 possui saldo livre de apenas 3 naves.
    O ataque deve ser bloqueado por não atingir o limite mínimo de lançamento.
    """
    agent = EliteTactician()
    agent.apply_profile("standard")
    agent.hoarding_constant = 4.0
    
    planets = [
        [0, 0, 50.0, 50.0, 5.0, 11, 1],  # 11 ships, min_res is 8. Surplus is 3.
        [1, -1, 60.0, 50.0, 5.0, 1, 1],  # Target neutro próximo
    ]
    
    obs = create_mock_obs(player=0, step=125, planets=planets, fleets=[])
    moves = agent.get_actions(obs)
    
    attack_move = next((m for m in moves if m[0] == 0), None)
    assert attack_move is None, "O agente deveria bloquear o micro-spam de apenas 3 naves"

# ==============================================================================
# CATEGORIA 4: INTEGRIDADE FÍSICA GEOMÉTRICA
# ==============================================================================

def test_physics_sun_intersection_blocked():
    """
    Teste 4.1: Interseção Solar Abortada
    O caminho de ataque direto cruza a zona mortal do Sol (raio 10 a 50,50).
    O ataque deve ser abortado.
    """
    agent = EliteTactician()
    agent.apply_profile("standard")
    
    planets = [
        [0, 0, 20.0, 50.0, 5.0, 50, 2],   # Nosso planeta (oeste do Sol)
        [1, -1, 80.0, 50.0, 5.0, 5, 2],   # Alvo neutro (leste do Sol - a rota cruza exatamente 50,50!)
    ]
    
    obs = create_mock_obs(player=0, step=125, planets=planets, fleets=[])
    moves = agent.get_actions(obs)
    
    attack_move = next((m for m in moves if m[0] == 0), None)
    assert attack_move is None, "O agente deveria ter abortado o ataque cuja trajetória colide com o Sol"

def test_physics_evacuation_solar_dodging():
    """
    Teste 4.2: Fuga Segura (Dodging Solar)
    Nosso planeta sob evacuação. O planeta aliado mais próximo cruza o Sol.
    O agente deve evacuar para o segundo planeta aliado mais próximo que tem rota limpa.
    """
    agent = EliteTactician()
    agent.evacuation_trigger = 5
    
    planets = [
        [0, 0, 20.0, 50.0, 5.0, 20, 2],  # Nosso planeta a evacuar (id 0)
        [1, 0, 80.0, 50.0, 5.0, 10, 2],  # Aliado mais próximo mas rota cruza o Sol (id 1)
        [2, 0, 20.0, 20.0, 5.0, 10, 2],  # Aliado um pouco mais longe mas rota é limpa (id 2)
    ]
    # Incoming lethal fleet
    fleets = [
        [100, 1, 20.0, 60.0, -math.pi/2, 10, 50]
    ]
    
    obs = create_mock_obs(player=0, step=10, planets=planets, fleets=fleets)
    moves = agent.get_actions(obs)
    
    evac_move = next((m for m in moves if m[0] == 0), None)
    assert evac_move is not None, "O agente deveria ter evacuado"
    expected_angle = math.atan2(20.0 - 50.0, 20.0 - 20.0) # dx=0, dy=-30 => -pi/2
    assert math.isclose(evac_move[1], expected_angle, abs_tol=0.1), "O agente escolheu a rota suicida através do Sol em vez da rota segura"

# ==============================================================================
# CATEGORIA 5: COMPORTAMENTO GRANDMASTER BIPOLAR (V10)
# ==============================================================================

def test_mega_hoarding_patience():
    """
    Teste 5.1: Paciência do Mega-Hoarding (Território Isaiah)
    Turno 100. Nosso planeta P1 tem Produção 5 e 120 naves. Planeta inimigo P2 tem 50 naves.
    Perfil Defensivo Ativo (hoarding_constant = 28.0).
    O bot NÃO PODE atacar. Ele precisa reter 5 * 28 = 140 naves. Ele deve retornar [].
    """
    agent = EliteTactician()
    agent.apply_profile("defensive")
    agent.hoarding_constant = 28.0
    
    planets = [
        [0, 0, 30.0, 30.0, 5.0, 120, 5],  # Nosso planeta (id 0)
        [1, 1, 50.0, 30.0, 5.0, 50, 2],   # Planeta inimigo (id 1)
    ]
    
    obs = create_mock_obs(player=0, step=100, planets=planets, fleets=[])
    moves = agent.get_actions(obs)
    
    attack_move = next((m for m in moves if m[0] == 0), None)
    assert attack_move is None, "O agente deveria ter paciência e acumulado naves em vez de atacar sob mega-hoarding"

def test_bipolar_early_expansion():
    """
    Teste 5.2: Expansão Rápida na Abertura (Burst Opening)
    Turno 15. Nosso planeta P1 tem Produção 5 e 15 naves. Alvo neutro P2 tem 10 naves.
    O bot DEVE ignorar as regras normais de hoarding e atacar para garantir a captura precoce.
    """
    agent = EliteTactician()
    agent.apply_profile("defensive")
    agent.hoarding_constant = 28.0
    
    planets = [
        [0, 0, 30.0, 30.0, 5.0, 15, 5],  # Nosso planeta (id 0)
        [1, -1, 50.0, 30.0, 5.0, 10, 1], # Alvo neutro (id 1)
    ]
    
    obs = create_mock_obs(player=0, step=15, planets=planets, fleets=[])
    moves = agent.get_actions(obs)
    
    attack_move = next((m for m in moves if m[0] == 0), None)
    assert attack_move is not None, "O agente deveria ter atacado o planeta neutro durante o Burst Opening"
    assert attack_move[2] >= 12, "O agente deveria ter enviado frotas suficientes para capturar"

def test_opportunistic_snipe():
    """
    Teste 5.3: Snipe Oportunista (Capital Vazia)
    Turno 200. Nós temos 3 bases acumuladas com 150 naves cada. Um inimigo acabou de usar todas as suas naves,
    deixando a capital dele (Produção 5) com apenas 5 naves.
    O bot DEVE acionar o ToT sincronizado massivo ignorando limites de hoarding.
    """
    agent = EliteTactician()
    agent.apply_profile("defensive")
    agent.hoarding_constant = 28.0
    
    # We need to make sure we have 4 planets to enable ToT
    planets = [
        [0, 0, 30.0, 70.0, 5.0, 150, 5],  # Nosso planeta 1
        [1, 0, 30.0, 90.0, 5.0, 150, 5],  # Nosso planeta 2
        [2, 0, 70.0, 70.0, 5.0, 150, 5],  # Nosso planeta 3
        [4, 0, 70.0, 90.0, 5.0, 150, 5],  # Nosso planeta 4
        [3, 1, 50.0, 90.0, 5.0, 5, 5],    # Capital inimiga vulnerável (id 3) - fora do Sol!
    ]
    
    obs = create_mock_obs(player=0, step=200, planets=planets, fleets=[])
    obs["angular_velocity"] = 0.0
    agent.get_actions(obs)
    
    # Verify that the ToT attack was successfully scheduled
    assert len(agent.active_tot_attacks) > 0, "O ToT deveria ter sido agendado"
    
    # Advance to step 203 to reach the synchronized launch window (T-12)
    obs2 = create_mock_obs(player=0, step=203, planets=planets, fleets=[])
    obs2["angular_velocity"] = 0.0
    moves2 = agent.get_actions(obs2)
    
    tot_moves = [m for m in moves2 if m[2] > 0]
    assert len(tot_moves) > 0, "As naves de ToT deveriam ter sido lançadas no launch window em step 203"

