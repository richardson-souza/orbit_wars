### 4. Modelagem (Modeling)

Nesta fase, decidimos _como_ o agente processará as características (features) criadas na etapa de Preparação de Dados para tomar uma decisão tática. O objetivo técnico final do modelo é sempre cuspir uma lista de listas no formato `[from_planet_id, direction_angle, num_ships]` ou uma lista vazia `[]`.
#### 4.1 Selecionar Técnica de Modelagem (Select Modeling Technique)

Como o ambiente de "Orbit Wars" fornece informação perfeita do tabuleiro, diferentes abordagens podem ser selecionadas dependendo da complexidade desejada e do tempo de computação disponível.

- **Heurística de Pontuação (Scoring System):** Uma técnica determinística baseada em regras de negócio. Atribui um peso matemático para cada planeta neutro ou inimigo baseado em sua distância, produção e defesas atuais. Ideal como técnica inicial devido à facilidade de interpretação e alta velocidade de execução.
    
- **Busca em Árvore (Monte Carlo Tree Search - MCTS):** Uma técnica de planejamento que simula múltiplos futuros possíveis antes de decidir a ação. Como o espaço é contínuo 100x100 e a física do jogo envolve colisões precisas, o MCTS exigiria a criação de um simulador interno simplificado do motor do jogo.
    
- **Aprendizado por Reforço (ex: PPO):** Uma técnica avançada onde uma rede neural atua como a política do agente. Exigiria transformar os atributos espaciais (raio, posição $x$ e $y$ e tamanho das frotas) em tensores ou imagens de matriz.
#### 4.2 Gerar Desenho de Teste (Generate Test Design)

Em problemas de Machine Learning tradicional, usaríamos _train/test split_ ou _K-Fold_. Em um ambiente de competição simulada, o desenho de teste é baseado em torneios e arenas locais.

- **Arena Local:** Utilizaremos o pacote `kaggle_environments` (versão 1.28.0 ou superior) para executar episódios localmente em Python.
    
- **Baseline de Confronto:** O modelo candidato sempre jogará séries de 100 partidas contra o agente base fornecido na documentação, o "Nearest Planet Sniper".
    
- **Simetria de Testes:** Como o jogo suporta partidas de 2 ou 4 jogadores, o desenho de teste deve incluir confrontos em ambos os modos para garantir que o modelo lide bem com o caos de múltiplos inimigos simultâneos.
#### 4.3 Construir Modelo (Build Model)

Esta tarefa envolve a codificação algorítmica da técnica escolhida dentro das restrições do motor do Kaggle. O modelo deve ser inteiramente encapsulado na função principal.

- **Encapsulamento:** Toda a lógica de inferência da técnica selecionada será codificada dentro da função estrita `def agent(obs):` no arquivo `main.py`.
    
- **Condicionais de Ação:** O modelo deve extrair o seu próprio identificador da variável `obs.player` (ou `obs.get("player", 0)`) para saber quais planetas ele controla e pode usar como base de lançamento.
    
- **Controle Estrito de Saída:** O modelo deve garantir que a saída final gere ângulos (`direction_angle`) estritamente em radianos, calculados através de funções trigonométricas como `math.atan2`.
#### 4.4 Avaliar Modelo (Assess Model)

Esta é a avaliação puramente técnica para verificar se o modelo construído aprendeu as regras e funciona conforme planejado, antes de pensarmos no impacto para o negócio (que será a Fase 5 de Avaliação).

- **Métricas de Performance Preditiva:** Avaliar a _Win Rate_ (Taxa de Vitórias) do modelo atual contra as versões anteriores. Uma técnica só avançará se obtiver uma taxa de vitória técnica consistentemente superior a 55%.
    
- **Eficiência Computacional:** Monitorar se o modelo executa a sua lógica dentro do limite padrão de tempo do jogo, que é de 1 segundo por turno (`actTimeout`), e se ele consome o seu orçamento de emergência `remainingOverageTime`.
    
- **Debugging de Regras Ocultas:** Fazer o download do replay em JSON ("Download Replays and Logs") e usar os logs locais para checar tecnicamente a matriz de confusão das nossas predições. Por exemplo: o modelo enviou uma frota, mas calculou a curva logarítmica de velocidade (de 1.0 a 6.0) de forma incorreta e errou a interceptação de um cometa que viaja a 4.0 unidades/turno?.