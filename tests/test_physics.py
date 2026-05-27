import math
from core.physics import (
    distance,
    point_to_segment_distance,
    intersects_sun,
    get_planet_position_at_step,
)


def test_distance():
    """Test Euclidean distance calculation."""
    assert math.isclose(distance((0, 0), (3, 4)), 5.0)
    assert math.isclose(distance((10, 20), (10, 20)), 0.0)


def test_point_to_segment_distance():
    """Test shortest distance from a point to a line segment."""
    assert math.isclose(point_to_segment_distance((5, 5), (0, 5), (10, 5)), 0.0)
    assert math.isclose(point_to_segment_distance((5, 10), (0, 5), (10, 5)), 5.0)
    assert math.isclose(point_to_segment_distance((-5, 5), (0, 5), (10, 5)), 5.0)
    assert math.isclose(point_to_segment_distance((15, 5), (0, 5), (10, 5)), 5.0)


def test_sun_collision_detection():
    """Test if the trajectory intersects the deadly sun at (50, 50) with radius 10."""
    assert intersects_sun(start_x=10, start_y=50, target_x=90, target_y=50) is True
    assert intersects_sun(start_x=10, start_y=10, target_x=20, target_y=20) is False
    assert intersects_sun(start_x=30, start_y=42, target_x=70, target_y=42) is True
    assert intersects_sun(start_x=30, start_y=38, target_x=70, target_y=38) is False


def test_planet_position_projection():
    """Test forecasting the exact future coordinate of an orbiting planet."""
    initial_planets = [[0, -1, 50.0, 80.0, 2.0, 10, 1]]
    angular_velocity = 0.05

    pos_0 = get_planet_position_at_step(0, 0, initial_planets, angular_velocity)
    assert math.isclose(pos_0[0], 50.0, abs_tol=1e-5)
    assert math.isclose(pos_0[1], 80.0, abs_tol=1e-5)
    pos_10 = get_planet_position_at_step(0, 10, initial_planets, angular_velocity)
    expected_angle = math.pi / 2 + 0.05 * 10
    expected_x = 50.0 + 30.0 * math.cos(expected_angle)
    expected_y = 50.0 + 30.0 * math.sin(expected_angle)
    assert math.isclose(pos_10[0], expected_x, abs_tol=1e-5)
    assert math.isclose(pos_10[1], expected_y, abs_tol=1e-5)
