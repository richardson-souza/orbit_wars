from strategies.elite_tactician import EliteTactician

agent_strategy = EliteTactician(
    production_weight=12.0,
    distance_weight=3.5,
    ship_cost_weight=0.1,
    comet_bonus=25.0,
    aggression_weight=1.0,
)


def agent(obs) -> list:
    """
    Kaggle environment agent entrypoint for EliteTactician V10.
    Takes raw environment observations and returns the calculated moves.
    """
    return agent_strategy.get_actions(obs)
