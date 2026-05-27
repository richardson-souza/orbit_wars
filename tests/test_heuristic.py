import pytest
import math
from strategies.heuristic_scorer import HeuristicScorer
from core.observation import ParsedObservation


def test_heuristic_moves_basic():
    """Verify that heuristic strategy returns valid moves and obeys basic rules."""
    obs_dict = {
        "player": 0,
        "step": 5,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 50, 2],
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
            [2, 1, 90.0, 90.0, 2.0, 15, 1],
            [
                3,
                -1,
                50.0,
                90.0,
                2.0,
                5,
                1,
            ],
        ],
        "planets": [
            [0, 0, 10.0, 10.0, 2.0, 50, 2],
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
            [2, 1, 90.0, 90.0, 2.0, 15, 1],
            [3, -1, 50.0, 90.0, 2.0, 5, 1],
        ],
        "fleets": [],
        "comet_planet_ids": [],
        "comets": [],
    }

    scorer = HeuristicScorer(aggression_weight=1.0)
    moves = scorer.get_actions(obs_dict)

    assert isinstance(moves, list)
    if len(moves) > 0:
        for move in moves:
            assert len(move) == 3
            from_id, angle, ships = move
            assert from_id == 0
            assert 0 < ships <= 50
            assert -2 * math.pi <= angle <= 2 * math.pi


def test_heuristic_sun_avoidance():
    """Verify that heuristic scorer never shoots fleets directly through the sun."""
    obs_dict = {
        "player": 0,
        "step": 5,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 50.0, 2.0, 50, 2],
            [
                1,
                -1,
                90.0,
                50.0,
                15.0,
                10,
                1,
            ],
        ],
        "planets": [[0, 0, 10.0, 50.0, 2.0, 50, 2], [1, -1, 90.0, 50.0, 15.0, 10, 1]],
        "fleets": [],
        "comet_planet_ids": [],
        "comets": [],
    }

    scorer = HeuristicScorer(aggression_weight=1.0)
    moves = scorer.get_actions(obs_dict)

    assert len(moves) == 0


def test_heuristic_garrison_validation():
    """Verify that fleet sizes sent never exceed the available garrison on our origin planet."""
    obs_dict = {
        "player": 0,
        "step": 10,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 5, 2],
            [1, -1, 15.0, 10.0, 2.0, 100, 1],
        ],
        "planets": [[0, 0, 10.0, 10.0, 2.0, 5, 2], [1, -1, 15.0, 10.0, 2.0, 100, 1]],
        "fleets": [],
        "comet_planet_ids": [],
        "comets": [],
    }

    scorer = HeuristicScorer(aggression_weight=1.0)
    moves = scorer.get_actions(obs_dict)

    for move in moves:
        assert move[2] <= 5
