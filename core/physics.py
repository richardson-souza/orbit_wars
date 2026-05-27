import math
from typing import Tuple, List, Union

CENTER = 50.0
SUN_RADIUS = 10.0
ROTATION_RADIUS_LIMIT = 50.0


def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def point_to_segment_distance(
    p: Tuple[float, float], v: Tuple[float, float], w: Tuple[float, float]
) -> float:
    """Calculate the minimum distance from point p to line segment v-w."""
    l2 = (v[0] - w[0]) ** 2 + (v[1] - w[1]) ** 2
    if l2 == 0.0:
        return distance(p, v)

    t = max(
        0.0,
        min(1.0, ((p[0] - v[0]) * (w[0] - v[0]) + (p[1] - v[1]) * (w[1] - v[1])) / l2),
    )
    projection = (v[0] + t * (w[0] - v[0]), v[1] + t * (w[1] - v[1]))
    return distance(p, projection)


def intersects_sun(
    start_x: float, start_y: float, target_x: float, target_y: float
) -> bool:
    """
    Check if a straight line trajectory from start to target intersects
    the deadly central sun at (50, 50) with radius 10.
    """
    sun_pos = (CENTER, CENTER)
    traj_distance = point_to_segment_distance(
        sun_pos, (start_x, start_y), (target_x, target_y)
    )
    return traj_distance < SUN_RADIUS


def get_planet_position_at_step(
    planet_id: int,
    step: int,
    initial_planets: List[List[Union[int, float]]],
    angular_velocity: float,
) -> Tuple[float, float]:
    """
    Calculate and forecast the exact position of a planet at a specific step in the future.
    """
    planet = next((p for p in initial_planets if p[0] == planet_id), None)
    if planet is None:
        raise ValueError(f"Planet ID {planet_id} not found in initial planets.")

    _, _, init_x, init_y, radius, _, _ = planet

    dx = init_x - CENTER
    dy = init_y - CENTER
    orbital_radius = math.sqrt(dx**2 + dy**2)

    if orbital_radius + radius < ROTATION_RADIUS_LIMIT:
        initial_angle = math.atan2(dy, dx)
        current_angle = initial_angle + angular_velocity * step
        new_x = CENTER + orbital_radius * math.cos(current_angle)
        new_y = CENTER + orbital_radius * math.sin(current_angle)
        return (new_x, new_y)

    return (init_x, init_y)
