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
            [1, 1, 13.13, 10.0, 3.1415926535, 1, 50]  # Heading left to land exactly at (10,10) on step 6.
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


def test_elite_tactician_evacuation_sun_avoidance():
    """Verify that EliteTactician does not evacuate to a planet if the flight path intersects the Sun."""
    # Planet 0 is our threatened planet.
    # Planet 1 is closer but flight path to it crosses the Sun (which is at 0, 0, radius 10.5).
    # Planet 2 is further but has a safe flight path.
    obs_dict = {
        "player": 0,
        "step": 5,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, -20.0, 0.0, 2.0, 10, 2],  # My planet
            [1, -1, 20.0, 0.0, 2.0, 5, 1],   # Closer but crosses Sun (from -20, 0 to 20, 0 passes through 0, 0)
            [2, -1, -20.0, 30.0, 2.0, 5, 1],  # Further but safe (path -20,0 to -20,30 does not cross 0,0)
        ],
        "planets": [
            [0, 0, -20.0, 0.0, 2.0, 10, 2],
            [1, -1, 20.0, 0.0, 2.0, 5, 1],
            [2, -1, -20.0, 30.0, 2.0, 5, 1],
        ],
        "fleets": [
            [1, 1, -16.87, 0.0, 3.1415926535, 1, 50]  # Heading left to land exactly at (-20,0) on step 6.
        ],
        "comet_planet_ids": [],
        "comets": [],
    }

    tactician = EliteTactician()
    moves = tactician.get_actions(obs_dict)

    evac_moves = [m for m in moves if m[0] == 0]
    assert len(evac_moves) > 0
    # Must evacuate to planet 2, not planet 1!
    # Expected angle from (-20, 0) to (-20, 30) is pi/2 (approx 1.57)
    angle = evac_moves[0][1]
    assert math.isclose(angle, math.pi / 2, abs_tol=0.1)


def test_elite_tactician_tot_no_deadlock():
    """Verify that ToT assignments are cleared once the arrival step is reached, preventing deadlock."""
    tactician = EliteTactician()
    # Add a mock assignment that has reached its window
    tactician.active_tot_attacks[1] = (6, 20)  # Target 1, arrives at step 6
    tactician.tot_assignments[(1, 0)] = 15      # From planet 0 to 1, send 15 ships

    obs_dict = {
        "player": 0,
        "step": 6,  # Step matches arrival step, should trigger release/cleanup
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 5, 2],  # Low ships (5) to avoid new ToT init
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
        ],
        "planets": [
            [0, 0, 10.0, 10.0, 2.0, 5, 2],
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
        ],
        "fleets": [],
        "comet_planet_ids": [],
        "comets": [],
    }

    # Execute action
    tactician.get_actions(obs_dict)

    # The assignment should be removed from tot_assignments to prevent any deadlock
    assert (1, 0) not in tactician.tot_assignments


def test_elite_tactician_state_machine():
    """Verify that EliteTactician dynamically tracks opponent captures and locks the correct profile at step 41."""
    tactician = EliteTactician()

    # Step 1: Initial state
    assert tactician.current_profile == "standard"
    assert not tactician.profile_locked

    # Mock sequence of observations
    # Turn 5: opponent 1 captures planet 2 (which was neutral -1)
    obs_step_5 = {
        "player": 0,
        "step": 5,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 5, 2],
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
            [2, -1, 30.0, 10.0, 2.0, 10, 1],
        ],
        "planets": [
            [0, 0, 10.0, 10.0, 2.0, 5, 2],
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
            [2, 1, 30.0, 10.0, 2.0, 10, 1],  # Owned by opponent 1!
        ],
        "fleets": [],
        "comet_planet_ids": [],
        "comets": [],
    }

    tactician.get_actions(obs_step_5)
    # Opponent 1 planets_captured should be 1
    assert tactician.opponent_tracker[1]["planets_captured"] == 1
    assert tactician.opponent_tracker[1]["aggression_score"] == 1.0 / 5.0  # 0.20 (> 0.15)

    # Step 41: Should trigger classification and select "defensive" because aggression_score (0.20) > 0.15
    obs_step_41 = {
        "player": 0,
        "step": 41,
        "angular_velocity": 0.05,
        "remainingOverageTime": 60.0,
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 5, 2],
            [1, -1, 20.0, 10.0, 2.0, 10, 1],
            [2, -1, 30.0, 10.0, 2.0, 10, 1],
        ],
        "planets": [
            [0, 0, 10.0, 10.0, 2.0, 5, 2],
            [1, 1, 20.0, 10.0, 2.0, 10, 1],
            [2, 1, 30.0, 10.0, 2.0, 10, 1],
        ],
        "fleets": [],
        "comet_planet_ids": [],
        "comets": [],
    }

    tactician.get_actions(obs_step_41)
    assert tactician.current_profile == "defensive"
    assert tactician.profile_locked

    # Verify that changing state again does not affect locked profile (Step 45)
    # Even if aggression score changes or all oponents become passive, the profile must stay defensive
    tactician.opponent_tracker[1]["aggression_score"] = 0.00
    obs_step_45 = dict(obs_step_41, step=45)
    tactician.get_actions(obs_step_45)
    assert tactician.current_profile == "defensive"
    assert tactician.profile_locked


