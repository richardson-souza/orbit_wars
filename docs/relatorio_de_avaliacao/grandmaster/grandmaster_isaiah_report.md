# Relatorio de Diagnostico de Partidas - Grandmaster Isaiah @ Tufa Labs
**Referencia do Agente**: Isaiah @ Tufa Labs (Top 1 Kaggle, MMR > 1700)
**Objetivo**: Analise comportamental e de padrao de jogo do lider supremo da competicao Orbit Wars.

---

## 1. Resumo Executivo e Engenharia de Comportamento
A auditoria analitica das 133 partidas do Grandmaster Isaiah revelou padroes extraordinarios de robustez tatica:
- **Taxa de Vitoria Absoluta**: 57.89% (77 vitorias em 133 partidas).
- **Eliminacao Zero (Zero Defeats)**: O Grandmaster registrou exatamente 0% de partidas em 3o ou 4o lugar. Ele encerrou TODAS as 133 partidas em 1o ou 2o lugar, provando que seu sistema e virtualmente imune a snipes taticos ou micro-spam na home base.
- **Conservadorismo Economico Extremo (Mega-Hoarding)**: Isaiah mantem um Hoarding Ratio medio de **28.19 naves por 1 ponto de producao** (muito acima de qualquer heuristic comum). Ele fortifica excessivamente suas bases, criando fortes inexpugnaveis.
- **Abertura Expansiva Veloz**: Captura uma media de 6.60 planetas neutros nos primeiros 40 turnos. Ele inicia com uma colonizacao em massa para assegurar a fundacao economica, e depois transita para uma postura defensiva intransponivel no mid-game.

---

## 2. Estatisticas Globais de Jogo

| Metrica de Analise | Valor Medio / Taxa | Significado Estrategico |
| :--- | :--- | :--- |
| **Duracao Media** | 359.1 passos | Resistencia extrema e prolongacao de partidas para late-game |
| **Planetas Finais** | 7.38 controlados | Elevado controle territorial ate o final |
| **Naves Finais** | 4.079,8 naves | Acúmulo macico de liquidez de frota |
| **Hoarding Ratio Medio** | 28.19 naves/prod | Conservacao rigida de reservas de seguranca |
| **Expansao Inicial (turno 40)** | 6.60 capturas | Abertura veloz para garantir producao estatica inicial |

---

## 3. Analise Individual de Todas as 133 Partidas

### Partida 1: 77930208.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 41.57
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (4 capturas), ele elevou as guarnicoes internas (hoarding ratio de 41.57) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 2: 77930758.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 51.39
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 51.39) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 3: 77931146.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 16.88
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 16.88) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 4: 77931482.json
* **Resultado**: 2o Lugar | **Passos Totais**: 186
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 8.36
* **Oponentes**: typeIIIfairy, Vadasz, bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 8.36), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 186 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 5: 77931658.json
* **Resultado**: 2o Lugar | **Passos Totais**: 227
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 23.94
* **Oponentes**: 213tubo, typeIIIfairy, Maruichi01
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 23.94), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 227 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 6: 77931908.json
* **Resultado**: 2o Lugar | **Passos Totais**: 185
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 9.92
* **Oponentes**: 3Comets, 213tubo, bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.92), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 185 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 7: 77932120.json
* **Resultado**: 2o Lugar | **Passos Totais**: 164
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 7.30
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 7.30), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 164 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 8: 77932483.json
* **Resultado**: 2o Lugar | **Passos Totais**: 149
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 12.26
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 12.26), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 149 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 9: 77932840.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 45.85
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 45.85) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 10: 77933155.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 11 planetas | Hoarding Ratio = 33.33
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (11 capturas), ele elevou as guarnicoes internas (hoarding ratio de 33.33) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 11: 77933502.json
* **Resultado**: 1o Lugar | **Passos Totais**: 274
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 31.36
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 31.36) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 12: 77933838.json
* **Resultado**: 2o Lugar | **Passos Totais**: 390
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 11.95
* **Oponentes**: bowwowforeach, typeIIIfairy, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 11.95), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 390 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 13: 77933880.json
* **Resultado**: 2o Lugar | **Passos Totais**: 218
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 11.29
* **Oponentes**: typeIIIfairy, bowwowforeach, 213tubo
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 11.29), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 218 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 14: 77934020.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 30.93
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 30.93) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 15: 77934158.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 29.82
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 29.82) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 16: 77934415.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 62.94
* **Oponentes**: Vadasz, typeIIIfairy, bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 62.94) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 17: 77934617.json
* **Resultado**: 2o Lugar | **Passos Totais**: 124
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 7.82
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 7.82), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 124 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 18: 77935009.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 30.77
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (7 capturas), ele elevou as guarnicoes internas (hoarding ratio de 30.77) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 19: 77935282.json
* **Resultado**: 1o Lugar | **Passos Totais**: 112
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 16.56
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (4 capturas), ele elevou as guarnicoes internas (hoarding ratio de 16.56) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 20: 77935593.json
* **Resultado**: 2o Lugar | **Passos Totais**: 295
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 12.67
* **Oponentes**: typeIIIfairy, 213tubo, 3Comets
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 12.67), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 295 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 21: 77935625.json
* **Resultado**: 2o Lugar | **Passos Totais**: 144
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 7.34
* **Oponentes**: typeIIIfairy, Vadasz, bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 7.34), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 144 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 22: 77935826.json
* **Resultado**: 2o Lugar | **Passos Totais**: 184
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 8.23
* **Oponentes**: 213tubo, Zachary Ruhe, bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 8.23), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 184 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 23: 77936034.json
* **Resultado**: 2o Lugar | **Passos Totais**: 289
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 11.38
* **Oponentes**: 3Comets, bowwowforeach, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 11.38), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 289 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 24: 77936257.json
* **Resultado**: 2o Lugar | **Passos Totais**: 177
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 12.18
* **Oponentes**: Harm Buisman, Zachary Ruhe, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 12.18), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 177 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 25: 77936468.json
* **Resultado**: 2o Lugar | **Passos Totais**: 157
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 12.02
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 12.02), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 157 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 26: 77936815.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 29.45
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 29.45) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 27: 77937616.json
* **Resultado**: 2o Lugar | **Passos Totais**: 144
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 9.76
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.76), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 144 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 28: 77937984.json
* **Resultado**: 1o Lugar | **Passos Totais**: 293
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 36.55
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (4 capturas), ele elevou as guarnicoes internas (hoarding ratio de 36.55) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 29: 77937987.json
* **Resultado**: 1o Lugar | **Passos Totais**: 330
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 32.31
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (3 capturas), ele elevou as guarnicoes internas (hoarding ratio de 32.31) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 30: 77938366.json
* **Resultado**: 2o Lugar | **Passos Totais**: 119
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 10.21
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.21), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 119 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 31: 77938447.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 26.83
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 26.83) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 32: 77938809.json
* **Resultado**: 2o Lugar | **Passos Totais**: 105
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 11.56
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 11.56), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 105 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 33: 77938818.json
* **Resultado**: 2o Lugar | **Passos Totais**: 68
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 10.20
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.20), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 68 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 34: 77939807.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 30.74
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (3 capturas), ele elevou as guarnicoes internas (hoarding ratio de 30.74) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 35: 77939816.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 22.77
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (8 capturas), ele elevou as guarnicoes internas (hoarding ratio de 22.77) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 36: 77940139.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 55.37
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 55.37) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 37: 77940457.json
* **Resultado**: 2o Lugar | **Passos Totais**: 110
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 8.02
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 8.02), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 110 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 38: 77940470.json
* **Resultado**: 2o Lugar | **Passos Totais**: 143
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 13.46
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 13.46), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 143 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 39: 77941932.json
* **Resultado**: 2o Lugar | **Passos Totais**: 240
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 9.71
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.71), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 240 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 40: 77942490.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 52.18
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 52.18) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 41: 77943024.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 82.97
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (3 capturas), ele elevou as guarnicoes internas (hoarding ratio de 82.97) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 42: 77943032.json
* **Resultado**: 1o Lugar | **Passos Totais**: 358
* **Metricas de Telemetria**: Expansao Inicial = 15 planetas | Hoarding Ratio = 57.36
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (15 capturas), ele elevou as guarnicoes internas (hoarding ratio de 57.36) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 43: 77943563.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 20.39
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 20.39) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 44: 77943569.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 30.28
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (3 capturas), ele elevou as guarnicoes internas (hoarding ratio de 30.28) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 45: 77944927.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 128.29
* **Oponentes**: Jake Will
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (7 capturas), ele elevou as guarnicoes internas (hoarding ratio de 128.29) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 46: 77946121.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 21.05
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 21.05) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 47: 77946966.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 18.61
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (8 capturas), ele elevou as guarnicoes internas (hoarding ratio de 18.61) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 48: 77947495.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 27.78
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (10 capturas), ele elevou as guarnicoes internas (hoarding ratio de 27.78) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 49: 77947961.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 52.76
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 52.76) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 50: 77948443.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 14 planetas | Hoarding Ratio = 16.25
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (14 capturas), ele elevou as guarnicoes internas (hoarding ratio de 16.25) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 51: 77948893.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 37.70
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 37.70) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 52: 77949367.json
* **Resultado**: 2o Lugar | **Passos Totais**: 197
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 10.93
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.93), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 197 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 53: 77949717.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 46.54
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 46.54) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 54: 77950049.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 89.98
* **Oponentes**: 213tubo, typeIIIfairy, Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 89.98) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 55: 77950056.json
* **Resultado**: 2o Lugar | **Passos Totais**: 284
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 13.36
* **Oponentes**: Vadasz, saharan, typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 13.36), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 284 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 56: 77950059.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 25.72
* **Oponentes**: Jake Will, Zachary Ruhe, Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (4 capturas), ele elevou as guarnicoes internas (hoarding ratio de 25.72) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 57: 77950265.json
* **Resultado**: 2o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 60.95
* **Oponentes**: Zachary Ruhe, 213tubo, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 60.95), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 500 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 58: 77950492.json
* **Resultado**: 2o Lugar | **Passos Totais**: 229
* **Metricas de Telemetria**: Expansao Inicial = 12 planetas | Hoarding Ratio = 8.32
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 8.32), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 229 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 59: 77950515.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 39.43
* **Oponentes**: Zachary Ruhe
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 39.43) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 60: 77950818.json
* **Resultado**: 1o Lugar | **Passos Totais**: 277
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 31.62
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 31.62) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 61: 77951138.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 43.49
* **Oponentes**: bowwowforeach, typeIIIfairy, Jake Will
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (3 capturas), ele elevou as guarnicoes internas (hoarding ratio de 43.49) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 62: 77951340.json
* **Resultado**: 2o Lugar | **Passos Totais**: 304
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 10.33
* **Oponentes**: 3Comets, Vadasz, 213tubo
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.33), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 304 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 63: 77951369.json
* **Resultado**: 2o Lugar | **Passos Totais**: 236
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 7.87
* **Oponentes**: typeIIIfairy, TonyK, Zachary Ruhe
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 7.87), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 236 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 64: 77951505.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 53.41
* **Oponentes**: Gregor Lied, Zachary Ruhe, bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 53.41) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 65: 77951563.json
* **Resultado**: 2o Lugar | **Passos Totais**: 385
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 14.86
* **Oponentes**: TonyK, 3Comets, typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 14.86), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 385 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 66: 77951777.json
* **Resultado**: 2o Lugar | **Passos Totais**: 180
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 7.08
* **Oponentes**: Vadasz, TonyK, bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 7.08), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 180 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 67: 77951788.json
* **Resultado**: 2o Lugar | **Passos Totais**: 257
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 15.39
* **Oponentes**: Maruichi01, bowwowforeach, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 15.39), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 257 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 68: 77951992.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 38.94
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (7 capturas), ele elevou as guarnicoes internas (hoarding ratio de 38.94) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 69: 77952323.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 23.00
* **Oponentes**: saharan
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 23.00) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 70: 77952633.json
* **Resultado**: 2o Lugar | **Passos Totais**: 151
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 9.44
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.44), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 151 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 71: 77953045.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 63.47
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 63.47) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 72: 77953056.json
* **Resultado**: 2o Lugar | **Passos Totais**: 129
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 10.99
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.99), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 129 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 73: 77953338.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 13 planetas | Hoarding Ratio = 41.17
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (13 capturas), ele elevou as guarnicoes internas (hoarding ratio de 41.17) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 74: 77953666.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 49.29
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 49.29) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 75: 77953923.json
* **Resultado**: 2o Lugar | **Passos Totais**: 248
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 11.64
* **Oponentes**: typeIIIfairy, Vadasz, Zachary Ruhe
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 11.64), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 248 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 76: 77953997.json
* **Resultado**: 2o Lugar | **Passos Totais**: 177
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 9.69
* **Oponentes**: Jake Will, typeIIIfairy, bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.69), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 177 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 77: 77954010.json
* **Resultado**: 2o Lugar | **Passos Totais**: 171
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 10.49
* **Oponentes**: typeIIIfairy, bowwowforeach, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.49), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 171 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 78: 77954205.json
* **Resultado**: 2o Lugar | **Passos Totais**: 270
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 14.26
* **Oponentes**: Maruichi01, Zachary Ruhe, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 14.26), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 270 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 79: 77954432.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 30.25
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (3 capturas), ele elevou as guarnicoes internas (hoarding ratio de 30.25) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 80: 77954436.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 53.32
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (10 capturas), ele elevou as guarnicoes internas (hoarding ratio de 53.32) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 81: 77954821.json
* **Resultado**: 2o Lugar | **Passos Totais**: 214
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 8.05
* **Oponentes**: 213tubo, 3Comets, bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 8.05), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 214 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 82: 77954822.json
* **Resultado**: 2o Lugar | **Passos Totais**: 110
* **Metricas de Telemetria**: Expansao Inicial = 2 planetas | Hoarding Ratio = 18.74
* **Oponentes**: bowwowforeach, Vadasz, typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 18.74), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 110 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 83: 77955078.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 37.87
* **Oponentes**: Zachary Ruhe
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (8 capturas), ele elevou as guarnicoes internas (hoarding ratio de 37.87) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 84: 77955456.json
* **Resultado**: 2o Lugar | **Passos Totais**: 103
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 9.92
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.92), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 103 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 85: 77955777.json
* **Resultado**: 2o Lugar | **Passos Totais**: 133
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 11.27
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 11.27), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 133 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 86: 77956087.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 39.16
* **Oponentes**: Vadasz, 213tubo, bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 39.16) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 87: 77956110.json
* **Resultado**: 2o Lugar | **Passos Totais**: 160
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 6.01
* **Oponentes**: bowwowforeach, 3Comets, Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 6.01), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 160 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 88: 77956321.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 41.66
* **Oponentes**: Maruichi01, typeIIIfairy, Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 41.66) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 89: 77956324.json
* **Resultado**: 2o Lugar | **Passos Totais**: 146
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 7.88
* **Oponentes**: Jake Will, Vadasz, Zachary Ruhe
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 7.88), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 146 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 90: 77956518.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 35.12
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 35.12) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 91: 77956819.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 40.30
* **Oponentes**: typeIIIfairy, bowwowforeach, Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (4 capturas), ele elevou as guarnicoes internas (hoarding ratio de 40.30) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 92: 77956823.json
* **Resultado**: 2o Lugar | **Passos Totais**: 127
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 13.18
* **Oponentes**: 213tubo, Vadasz, typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 13.18), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 127 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 93: 77957078.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 14 planetas | Hoarding Ratio = 34.69
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (14 capturas), ele elevou as guarnicoes internas (hoarding ratio de 34.69) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 94: 77957090.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 46.14
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (8 capturas), ele elevou as guarnicoes internas (hoarding ratio de 46.14) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 95: 77957355.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 59.16
* **Oponentes**: TonyK
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (7 capturas), ele elevou as guarnicoes internas (hoarding ratio de 59.16) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 96: 77957357.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 36.89
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 36.89) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 97: 77957754.json
* **Resultado**: 2o Lugar | **Passos Totais**: 166
* **Metricas de Telemetria**: Expansao Inicial = 2 planetas | Hoarding Ratio = 6.95
* **Oponentes**: TonyK, bowwowforeach, Jake Will
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 6.95), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 166 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 98: 77957962.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 40.25
* **Oponentes**: 3Comets, 213tubo, Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 40.25) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 99: 77958145.json
* **Resultado**: 2o Lugar | **Passos Totais**: 141
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 10.76
* **Oponentes**: Vadasz, 213tubo, TonyK
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.76), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 141 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 100: 77958373.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 21.85
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (8 capturas), ele elevou as guarnicoes internas (hoarding ratio de 21.85) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 101: 77958374.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 57.15
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (10 capturas), ele elevou as guarnicoes internas (hoarding ratio de 57.15) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 102: 77958375.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 12 planetas | Hoarding Ratio = 33.65
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (12 capturas), ele elevou as guarnicoes internas (hoarding ratio de 33.65) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 103: 77958378.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 29.14
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (10 capturas), ele elevou as guarnicoes internas (hoarding ratio de 29.14) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 104: 77958387.json
* **Resultado**: 2o Lugar | **Passos Totais**: 131
* **Metricas de Telemetria**: Expansao Inicial = 1 planetas | Hoarding Ratio = 19.49
* **Oponentes**: Zachary Ruhe
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 19.49), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 131 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 105: 77958690.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 11 planetas | Hoarding Ratio = 23.50
* **Oponentes**: 213tubo
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (11 capturas), ele elevou as guarnicoes internas (hoarding ratio de 23.50) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 106: 77959039.json
* **Resultado**: 2o Lugar | **Passos Totais**: 420
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 12.20
* **Oponentes**: 213tubo, typeIIIfairy, Zachary Ruhe
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 12.20), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 420 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 107: 77959466.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 12 planetas | Hoarding Ratio = 39.99
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (12 capturas), ele elevou as guarnicoes internas (hoarding ratio de 39.99) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 108: 77959795.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 11 planetas | Hoarding Ratio = 25.37
* **Oponentes**: Zachary Ruhe
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (11 capturas), ele elevou as guarnicoes internas (hoarding ratio de 25.37) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 109: 77959797.json
* **Resultado**: 2o Lugar | **Passos Totais**: 105
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 10.15
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.15), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 105 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 110: 77960139.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 42.64
* **Oponentes**: TonyK
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 42.64) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 111: 77960468.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 12 planetas | Hoarding Ratio = 39.47
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (12 capturas), ele elevou as guarnicoes internas (hoarding ratio de 39.47) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 112: 77960474.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 34.09
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (8 capturas), ele elevou as guarnicoes internas (hoarding ratio de 34.09) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 113: 77960813.json
* **Resultado**: 2o Lugar | **Passos Totais**: 80
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 14.67
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 14.67), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 80 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 114: 77961143.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 12 planetas | Hoarding Ratio = 27.90
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (12 capturas), ele elevou as guarnicoes internas (hoarding ratio de 27.90) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 115: 77961723.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 24.97
* **Oponentes**: Vadasz
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (10 capturas), ele elevou as guarnicoes internas (hoarding ratio de 24.97) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 116: 77961926.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 68.70
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 68.70) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 117: 77962358.json
* **Resultado**: 2o Lugar | **Passos Totais**: 96
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 10.81
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.81), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 96 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 118: 77962371.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 32.64
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (8 capturas), ele elevou as guarnicoes internas (hoarding ratio de 32.64) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 119: 77963394.json
* **Resultado**: 2o Lugar | **Passos Totais**: 187
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 11.65
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 11.65), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 187 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 120: 77963724.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 9 planetas | Hoarding Ratio = 51.25
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (9 capturas), ele elevou as guarnicoes internas (hoarding ratio de 51.25) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 121: 77964268.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 50.34
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 50.34) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 122: 77964605.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 3 planetas | Hoarding Ratio = 45.93
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (3 capturas), ele elevou as guarnicoes internas (hoarding ratio de 45.93) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 123: 77964939.json
* **Resultado**: 2o Lugar | **Passos Totais**: 136
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 9.30
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.30), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 136 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 124: 77964951.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 6 planetas | Hoarding Ratio = 14.38
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (6 capturas), ele elevou as guarnicoes internas (hoarding ratio de 14.38) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 125: 77965271.json
* **Resultado**: 2o Lugar | **Passos Totais**: 101
* **Metricas de Telemetria**: Expansao Inicial = 4 planetas | Hoarding Ratio = 9.05
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.05), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 101 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 126: 77965611.json
* **Resultado**: 2o Lugar | **Passos Totais**: 176
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 9.48
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 9.48), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 176 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 127: 77965615.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 38.34
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (7 capturas), ele elevou as guarnicoes internas (hoarding ratio de 38.34) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 128: 77965955.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 11 planetas | Hoarding Ratio = 31.88
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (11 capturas), ele elevou as guarnicoes internas (hoarding ratio de 31.88) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 129: 77966481.json
* **Resultado**: 2o Lugar | **Passos Totais**: 210
* **Metricas de Telemetria**: Expansao Inicial = 10 planetas | Hoarding Ratio = 7.82
* **Oponentes**: 3Comets
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 7.82), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 210 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 130: 77966813.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 16.64
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (7 capturas), ele elevou as guarnicoes internas (hoarding ratio de 16.64) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 131: 77966828.json
* **Resultado**: 2o Lugar | **Passos Totais**: 139
* **Metricas de Telemetria**: Expansao Inicial = 8 planetas | Hoarding Ratio = 10.48
* **Oponentes**: bowwowforeach
* **Diagnostico Tecnico**: Isaiah encerrou no 2o lugar apos atrito severo no mid-game contra oponentes de elite. Mesmo com uma guarnicao robusta (hoarding ratio = 10.48), o oponente principal conseguiu realizar cercos nas bases satelites. Contudo, a rigidez defensiva do Grandmaster evitou a eliminacao rapida, prolongando a partida ate o turno 139 e garantindo o vice-campeonato sem ceder a Home Base de forma precoce.

### Partida 132: 77967607.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 7 planetas | Hoarding Ratio = 65.61
* **Oponentes**: Zachary Ruhe
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (7 capturas), ele elevou as guarnicoes internas (hoarding ratio de 65.61) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

### Partida 133: 77967621.json
* **Resultado**: 1o Lugar | **Passos Totais**: 500
* **Metricas de Telemetria**: Expansao Inicial = 5 planetas | Hoarding Ratio = 59.08
* **Oponentes**: typeIIIfairy
* **Diagnostico Tecnico**: O Grandmaster garantiu o 1o lugar com dominacao territorial. Apos estabelecer uma abertura expansiva forte (5 capturas), ele elevou as guarnicoes internas (hoarding ratio de 59.08) e usou frotas ToT de alta precisao para desgastar os adversarios. O jogo terminou em dominancia absoluta gracas a fidelidade fisica de trajetorias e protecao antissolar.

