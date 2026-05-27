from typing import List, Dict, Any, Union


class BaseStrategy:
    """
    Abstract base class for all Orbit Wars agent strategies.
    Ensures that any strategy implements get_actions method with proper types.
    """

    def get_actions(
        self, observation: Union[Dict[str, Any], Any]
    ) -> List[List[Union[int, float]]]:
        """
        Calculate and return actions for this step.

        Args:
            observation (Union[Dict[str, Any], Any]): Raw observation from the environment.

        Returns:
            List[List[Union[int, float]]]: List of moves, where each move is:
                                          [from_planet_id, direction_angle_rad, num_ships]
        """
        raise NotImplementedError("Strategies must implement the get_actions method.")
