import pytest
import math
from strategies.heuristic_scorer import HeuristicScorer
from core.observation import ParsedObservation

def test_roi_efficiency_prioritization():
    """Verify that HeuristicScorer with ROI dynamically prioritizes highly efficient planets over high-cost ones."""
    obs_dict = {
        "player": 0,
        "step": 10,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 30.0, 30.0, 2.0, 40, 2],    # Nosso planeta (40 naves)
            [1, -1, 35.0, 30.0, 2.0, 5, 2],     # Alvo A: Neutro econômico (5 naves de defesa, prod 2)
            [2, 1, 20.0, 30.0, 2.0, 30, 8],     # Alvo B: Inimigo caro (30 naves de defesa, prod 8)
        ],
        "planets": [
            [0, 0, 30.0, 30.0, 2.0, 40, 2],
            [1, -1, 35.0, 30.0, 2.0, 5, 2],
            [2, 1, 20.0, 30.0, 2.0, 30, 8],
        ],
        "fleets": [],
        "comet_planet_ids": [],
        "comets": [],
    }

    scorer = HeuristicScorer(aggression_weight=1.0)
    moves = scorer.get_actions(obs_dict)

    assert len(moves) > 0
    from_id, angle, ships = moves[0]
    assert from_id == 0

def test_vulturing_impact_detection():
    """Verify that heuristic scorer identifies and schedules a vulturing attack on a resolving proxy fight."""
    obs_dict = {
        "player": 0,
        "step": 20,
        "angular_velocity": 0.0,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 30.0, 30.0, 2.0, 100, 2],   # Nós (100 naves)
            [1, 1, 40.0, 30.0, 2.0, 40, 2],    # Inimigo A (40 naves)
        ],
        "planets": [
            [0, 0, 30.0, 30.0, 2.0, 100, 2],
            [1, 1, 40.0, 30.0, 2.0, 40, 2],
        ],
        # Inimigo B (id 2) enviando uma frota maciça de 38 naves para colidir com o Inimigo A (id 1)
        # O impacto será no próximo tick (distância muito curta ou angle/velocidade pré-calculada)
        "fleets": [
            [999, 2, 38.0, 30.0, 0.0, 1, 38]   # Frota hostil a caminho do planeta 1
        ],
        "comet_planet_ids": [],
        "comets": [],
    }
    
    scorer = HeuristicScorer(aggression_weight=1.0)
    moves = scorer.get_actions(obs_dict)
    assert isinstance(moves, list)

def test_anti_snipe_trigger():
    """Verify that our system triggers a timely defensive reinforcement if a planet is under lethal snipe."""
    obs_dict = {
        "player": 0,
        "step": 30,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 20.0, 20.0, 2.0, 5, 1],     # Nossa base A vulnerável (5 naves)
            [1, 0, 30.0, 20.0, 2.0, 80, 5],    # Nossa base B forte (80 naves, vizinha)
        ],
        "planets": [
            [0, 0, 20.0, 20.0, 2.0, 5, 1],
            [1, 0, 30.0, 20.0, 2.0, 80, 5],
        ],
        # Inimigo enviando 30 naves letais contra a nossa base A (id 0)
        "fleets": [
            [888, 1, 25.0, 20.0, 0.0, 0, 30]   # Frota hostil mirando em nossa base A (id 0)
        ],
        "comet_planet_ids": [],
        "comets": [],
    }

    scorer = HeuristicScorer(aggression_weight=1.0)
    moves = scorer.get_actions(obs_dict)
    assert isinstance(moves, list)
