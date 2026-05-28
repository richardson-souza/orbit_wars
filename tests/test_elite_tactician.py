import pytest
import math
from strategies.elite_tactician import EliteTactician
from core.observation import ParsedObservation


def test_elite_tactician_basic():
    """Verify that EliteTactician returns valid moves and parses observation correctly."""
    obs_dict = {
        "player": 0,
        "step": 5,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 50, 2],
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
            [2, 1, 90.0, 90.0, 2.0, 15, 1],
            [3, -1, 50.0, 90.0, 2.0, 5, 1],
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

    tactician = EliteTactician()
    moves = tactician.get_actions(obs_dict)
    assert isinstance(moves, list)


def test_elite_tactician_evacuation_dodge():
    """Verify that EliteTactician successfully triggers Evacuação Defensiva (Dodging) when a lethal threat is 1 tick away."""
    # Source planet 0 has 10 ships.
    # An enemy fleet with 50 ships is heading to planet 0 and will arrive at step 6 (next step, since current step is 5).
    obs_dict = {
        "player": 0,
        "step": 5,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 10, 2],
            [1, -1, 30.0, 10.0, 2.0, 5, 1],
        ],
        "planets": [
            [0, 0, 10.0, 10.0, 2.0, 10, 2],
            [1, -1, 30.0, 10.0, 2.0, 5, 1],
        ],
        "fleets": [
            [1, 1, 12.0, 10.0, 0.0, 1, 50]  # Owner 1, 50 ships. Arrives next turn (dist = 2, speed = 3.13).
        ],
        "comet_planet_ids": [],
        "comets": [],
    }

    tactician = EliteTactician()
    moves = tactician.get_actions(obs_dict)

    # Evacuation should trigger and send ALL 10 ships away from planet 0 to planet 1!
    evac_moves = [m for m in moves if m[0] == 0]
    assert len(evac_moves) > 0
    # Evacuate 100% of ships (10 ships)
    assert evac_moves[0][2] == 10
