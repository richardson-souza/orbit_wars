from strategies.elite_tactician import EliteTactician

agent_strategy = EliteTactician(
    production_weight=15.0,
    distance_weight=0.7,
    ship_cost_weight=0.1,
    comet_bonus=25.0,
    aggression_weight=1.5,
)


def agent(obs) -> list:
    """
    Kaggle environment agent entrypoint for EliteTactician.
    Takes raw environment observations and returns the calculated moves.
    """
    return agent_strategy.get_actions(obs)
