Este documento é um **Plano de Ação e Especificação Técnica** estruturado para ser lido e interpretado por um **Agente de Criação de Código (Code Agent)**. Ele orienta o desenvolvimento passo a passo de uma solução de Inteligência Artificial para a competição "Orbit Wars" no Kaggle, cobrindo todo o ciclo de vida do projeto baseado na metodologia CRISP-DM.

---

# 🚀 SYSTEM INSTRUCTIONS FOR CODE AGENT

**Context:** You are an expert Software Engineer and Data Scientist tasked with building a reinforcement learning / algorithmic agent for the Kaggle "Orbit Wars" competition.
**Goal:** Build a modular, locally testable agent that uses a parameterized strategy pattern to easily switch between a "Scoring System Heuristic" and a "Monte Carlo Tree Search (MCTS)".
**Language & Style Requirements:**

1. **Code & Docstrings:** MUST be written strictly in **English**.
2. **Formatting:** MUST strictly follow **PEP 8** standards.
3. **Typing:** MUST use strict Python **Type Hints** for all function arguments and return values.
4. **Methodology:** MUST use **Test-Driven Development (TDD)**. Write tests (`pytest`) before implementing the core logic.
5. **Environment:** MUST use **.venv** with python 3.8.

---

## 🛠️ PHASE 1: Project Setup & Problem Comprehension

**CRISP-DM:** Compreensão do Problema & Implantação (Preparação do Ambiente Local)

**Justification:** Before sending code to the Kaggle servers, we need a local sandbox to simulate the environment, validate physics (100x100 continuous board, central sun radius 10), and prevent wasting submission quotas.

**Action Items:**

1. **Environment Setup:** Create a `requirements.txt` containing `kaggle-environments>=1.28.0` and `pytest`.
2. **Local Runner (`run_local.py`):** Build a script to instantiate the environment and run matches between our agent and the default `random` or a baseline `sniper` agent.
3. **Project Structure:**
```text
orbit_wars/
├── core/
│   ├── __init__.py
│   ├── observation.py       # Data parsing
│   ├── physics.py           # Collision and trajectory math
├── strategies/
│   ├── __init__.py
│   ├── base_strategy.py     # Abstract base class
│   ├── heuristic_scorer.py  # Strategy 1
│   ├── mcts_search.py       # Strategy 2
├── tests/                   # TDD test cases
│   ├── test_physics.py
│   ├── test_heuristic.py
├── main.py                  # Kaggle submission entrypoint

```

---

## 🧹 PHASE 2: Data Parsing & Feature Engineering

**CRISP-DM:** Compreensão dos Dados & Preparação dos Dados

**Justification:** The raw `obs` dictionary from Kaggle contains perfect information but needs mathematical transformation to be actionable. We need to filter invalid moves (e.g., shooting through the sun) and calculate forces.

**Action Items:**

1. **Observation Parser:** Create a class to parse `obs.planets`, `obs.fleets`, and `obs.player`.
* *Rule:* Ignore comets that are exiting the map (`path_index` nearing the end).
* *Rule:* Only consider origin planets where `owner == obs.player`.


2. **Physics Module (`physics.py`):** Write functions using `math.atan2` to calculate angles in radians.
* *Rule:* Implement a mathematical check for line-segment to circle intersection to avoid the central sun at `(50, 50)` with a `radius` of `10`.



**TDD Example (Write this test first):**

```python
def test_sun_collision_detection():
    """Test if the trajectory intersects the deadly sun at (50, 50) with radius 10."""
    from core.physics import intersects_sun
    # Trajectory passing directly through the center
    assert intersects_sun(start_x=10, start_y=50, target_x=90, target_y=50) is True
    # Trajectory safely away from the sun
    assert intersects_sun(start_x=10, start_y=10, target_x=20, target_y=20) is False

```

---

## 🧠 PHASE 3: Modeling (The Strategy Pattern)

**CRISP-DM:** Modelagem

**Justification:** Hardcoding logic makes iteration difficult. Using a Strategy Pattern allows the `main.py` to instantiate either the Heuristic or MCTS model dynamically based on configuration.

**Action Items:**

1. **Base Strategy (`base_strategy.py`):** Define an abstract class or Protocol that takes parsed observation data and returns a list of moves `[from_planet_id, direction_angle, num_ships]`.
2. **Heuristic Scoring Model (`heuristic_scorer.py`):**
* *Logic:* Assign a mathematical weight to targets based on distance, enemy garrison size, and production value.
* *Validation:* Ensure `num_ships` sent never exceeds the current garrison of the origin planet.


3. **MCTS Model (`mcts_search.py`):**
* *Logic:* Build a node-based tree simulating `T+N` turns.
* *Constraint:* Must monitor `obs.remainingOverageTime`. If less than 100ms remain, abort the tree search and yield the best move to prevent a "Timeout Kill".



**Code Standard Example:**

```python
from typing import List, Dict, Any
import math

class BaseStrategy:
    """Abstract base class for all Orbit Wars agent strategies."""
    
    def get_actions(self, observation: Dict[str, Any]) -> List[List[float]]:
        """
        Calculate the next moves based on the current environment observation.
        
        Args:
            observation (Dict[str, Any]): The raw observation dictionary from Kaggle.
            
        Returns:
            List[List[float]]: A list of actions in the format 
            [from_planet_id, direction_angle_rad, num_ships].
        """
        raise NotImplementedError("Strategies must implement the get_actions method.")

```

---

## 📊 PHASE 4: Local Evaluation & Business Metrics

**CRISP-DM:** Avaliação

**Justification:** A model might have flawless math but fail "business" objectives (e.g., capturing a comet just before it leaves the board, losing all invested ships). We need automated evaluation loops to prove the model wins games.

**Action Items:**

1. **Local Arena Script (`evaluate_models.py`):** Create an automated loop that plays 100 matches of `heuristic_scorer` vs Kaggle's baseline Sniper agent.
* *Target Metric:* Technical Win Rate > 55%.


2. **Replay & Debugging:** Output JSON replays for matches that the agent loses to audit logic failures (e.g., debugging "False Positives" where the agent attacked a leaving comet).
3. **Performance Profiling:** Monitor the 1-second `actTimeout`. Ensure the MCTS parameterization depth does not cause timeouts.

---

## 📦 PHASE 5: Deployment & CI/CD Pipeline

**CRISP-DM:** Implantação

**Justification:** The Kaggle platform expects either a single `main.py` or a `tar.gz` archive. Since our architecture is modular, we need an automated way to bundle it.

**Action Items:**

1. **Bundler Script:** Create a Python script (`build.py`) that uses `tarfile` to compress the `core/`, `strategies/`, and a standardized `main.py` into a `submission.tar.gz`.
2. **CLI Integration:** Provide instructions in the README to use `kaggle competitions submit -c orbit-wars -f submission.tar.gz -m "Version X"`.
3. **Entrypoint Wrapper (`main.py`):**
```python
from strategies.heuristic_scorer import HeuristicScorer

# Initialize globally to maintain state if necessary
agent_strategy = HeuristicScorer(aggression_weight=1.5)

def agent(obs: dict) -> list:
    """Kaggle environment entrypoint."""
    return agent_strategy.get_actions(obs)

```
---

**Instrução Final para o Code Agent:** Inicie a implementação lendo este plano. Comece criando a estrutura de diretórios e o arquivo `tests/test_physics.py` de acordo com a filosofia TDD exigida. Aguarde a validação de cada etapa antes de avançar para a próxima.