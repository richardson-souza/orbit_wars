from typing import List, Dict, Any, Union, Set
from collections import namedtuple

Planet = namedtuple(
    "Planet", ["id", "owner", "x", "y", "radius", "ships", "production"]
)
Fleet = namedtuple(
    "Fleet", ["id", "owner", "x", "y", "angle", "from_planet_id", "ships"]
)


class ParsedObservation:
    """
    Parses and transforms raw game observations from the Kaggle environment
    into clean, structured, and easy-to-use domain objects.
    """

    def __init__(self, obs: Union[Dict[str, Any], Any]):
        def get_val(key: str, default: Any = None) -> Any:
            if isinstance(obs, dict):
                return obs.get(key, default)
            return getattr(obs, key, default)

        self.player: int = int(get_val("player", 0))
        self.step: int = int(get_val("step", 0))
        self.angular_velocity: float = float(get_val("angular_velocity", 0.0))
        self.remaining_overage_time: float = float(
            get_val("remainingOverageTime", 60.0)
        )

        raw_initial = get_val("initial_planets", [])
        self.initial_planets: List[Planet] = [Planet(*p) for p in raw_initial]
        self.initial_planets_dict: Dict[int, Planet] = {
            p.id: p for p in self.initial_planets
        }

        self.comet_planet_ids: Set[int] = set(get_val("comet_planet_ids", []))
        self.raw_comets: List[Dict[str, Any]] = get_val("comets", [])

        self.exiting_comet_ids: Set[int] = set()
        for group in self.raw_comets:
            path_index = group.get("path_index", -1)
            planet_ids = group.get("planet_ids", [])
            paths = group.get("paths", [])

            for i, pid in enumerate(planet_ids):
                if i < len(paths):
                    path = paths[i]
                    if len(path) - path_index <= 2:
                        self.exiting_comet_ids.add(pid)

        raw_planets = get_val("planets", [])
        self.all_planets: Dict[int, Planet] = {}
        self.my_planets: List[Planet] = []
        self.enemy_planets: List[Planet] = []
        self.neutral_planets: List[Planet] = []
        self.active_comets: List[Planet] = []

        for p_list in raw_planets:
            p = Planet(*p_list)
            self.all_planets[p.id] = p

            if p.id in self.comet_planet_ids:
                if p.id not in self.exiting_comet_ids:
                    self.active_comets.append(p)

            if p.owner == self.player:
                self.my_planets.append(p)
            elif p.owner == -1:
                self.neutral_planets.append(p)
            else:
                self.enemy_planets.append(p)

        raw_fleets = get_val("fleets", [])
        self.all_fleets: List[Fleet] = [Fleet(*f) for f in raw_fleets]
        self.my_fleets: List[Fleet] = [
            f for f in self.all_fleets if f.owner == self.player
        ]
        self.enemy_fleets: List[Fleet] = [
            f for f in self.all_fleets if f.owner != self.player
        ]
