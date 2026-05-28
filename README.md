# Orbit Wars: Multi-Agent Intelligent Simulation & Neural Engine 🌌

Bem-vindo ao repositório oficial de desenvolvimento da equipe para o **Kaggle Orbit Wars**! Este projeto combina heurísticas de física orbital de alta precisão (como Ray Casting e simulação preditiva de colisão solar/planetária) com Aprendizado por Reforço por Otimização de Política Próxima (PPO).

Nossa arquitetura foi desenhada seguindo a metodologia **CRISP-DM** de ciência de dados para garantir máxima robustez tática na tomada de decisão em tempo real.

---

## 🗺️ Estrutura do Projeto

A organização dos diretórios é projetada para ser modular e extensível:

```text
├── core/                        # Núcleo físico e ambiental do projeto
│   ├── physics.py               # Fórmulas físicas oficiais, distâncias e Ray Casting
│   ├── observation.py           # Parser da observação crua do Kaggle para namedtuples
│   └── ppo_env.py               # Wrapper Gym Environment para treino PPO local
│
├── strategies/                  # Algoritmos e heurísticas de decisão
│   ├── base_strategy.py         # Interface padrão do Agente Modular
│   ├── heuristic_scorer.py      # Heurística Aprimorada com Trava Stateful e Defesa Dinâmica
│   ├── ppo_agent.py             # Agente de Rede Neural (SB3 PPO)
│   └── mcts_search.py           # Fallback e busca tática complementar
│
├── orbit-wars-data/             # Pipelines locais de treinamento, dados e benchmarks
│   ├── train_ppo.py             # Script de treino de rede neural local
│   ├── kaggle_train_ppo.py      # Monolítico consolidado para execução rápida no Kaggle GPU
│   └── simulate_all_episodes.py # Simulador da arena comparativa contra baseline (23+ seeds)
│
├── docs/                        # Ciclo de Vida do CRISP-DM e Planejamento
│   ├── episodes/                # JSONs históricos baixados do Kaggle para testes locais
│   └── *.md                     # Documentação das fases do projeto
│
├── tests/                       # Suíte de testes unitários e de integração (TDD)
├── build.py                     # Compilador das submissões oficiais do Kaggle
├── requirements.txt             # Dependências de execução
└── README.md                    # Este guia oficial
```

---

## 📖 Documentação CRISP-DM e Planejamento

Nosso projeto segue rigorosamente o ciclo de vida de desenvolvimento científico. Consulte nossa documentação detalhada em [docs/](file:///home/rsouza/Projects/orbit_wars/docs):

1. **[Compreensão do Problema](file:///home/rsouza/Projects/orbit_wars/docs/1.%20Compreensão%20do%20Problema.md)**: Regras do jogo, condições de vitória, limites de naves, colisão solar e velocidade.
2. **[Compreensão dos Dados](file:///home/rsouza/Projects/orbit_wars/docs/2.%20Compreensão%20dos%20Dados.md)**: Análise das observações em formato JSON, posições estelares e vetorização de estado.
3. **[Preparação dos Dados](file:///home/rsouza/Projects/orbit_wars/docs/3.%20Preparação%20dos%20Dados.md)**: Engenharia de características (Features) locais relativas aos $K$-vizinhos mais próximos.
4. **[Modelagem](file:///home/rsouza/Projects/orbit_wars/docs/4.%20Modelagem.md)**: Estrutura da Rede Neural MLP, algoritmo PPO e as equações da heurística tática.
5. **[Avaliação](file:///home/rsouza/Projects/orbit_wars/docs/5.%20Avaliação.md)**: Resultados da nossa arena local multi-modelos e comparação estatística de seeds.
6. **[Implantação](file:///home/rsouza/Projects/orbit_wars/docs/6.%20Implantação.md)**: Processo de submissão do agente compilado em arquivo único e governança de dados.
7. **[Plano de Ação Tático](file:///home/rsouza/Projects/orbit_wars/docs/action_plan.md)**: Próximos passos e backlog de melhorias.

---

## 🛠️ Configuração do Ambiente Local (Passo a Passo)

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local (Linux/macOS):

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.8** ou superior instalado em seu sistema:
```bash
python3 --version
```

### 2. Criação do Ambiente Virtual (`.venv`)
Crie e ative o ambiente virtual para isolar as dependências do projeto:
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate
```

### 3. Instalação das Dependências
Com o ambiente virtual ativo, instale os pacotes necessários especificados no `requirements.txt` (inclui PyTorch, Gym, Numpy e Stable-Baselines3):
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔑 Configuração da API do Kaggle (CLI)

Para interagir e fazer submissões automáticas direto pelo terminal, configure suas credenciais do Kaggle:

1. Acesse sua conta no [Kaggle](https://www.kaggle.com), vá até as configurações do seu perfil e clique em **Create New Token**. Isso fará o download de um arquivo chamado `kaggle.json`.
2. Mova o arquivo para o diretório `.kaggle` em sua pasta home do Linux:
   ```bash
   mkdir -p ~/.kaggle
   mv /caminho/para/o/download/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```
3. Teste a conexão listando a nossa competição:
   ```bash
   .venv/bin/kaggle competitions list | grep orbit-wars
   ```

---

## 🧪 Como Rodar e Testar o Projeto

### 1. Executando os Testes Unitários (TDD)
Garantimos a integridade de todas as equações físicas e comportamento dos agentes com o PyTest:
```bash
PYTHONPATH=. .venv/bin/pytest tests/
```

### 2. Treinando o Modelo PPO Neural Localmente
Para iniciar o pipeline de treinamento por Reforço local (salvando os pesos gerados em `models/ppo_orbit_wars.zip`):
```bash
PYTHONPATH=. .venv/bin/python3 orbit-wars-data/train_ppo.py
```

### 3. Rodando o Simulador da Arena Benchmark
Para rodar a nossa arena multi-modelos e avaliar a taxa de vitória do **Improved Heuristic** e do **PPO** contra a versão baseline original em todas as 34 seeds históricas:
```bash
PYTHONPATH=. .venv/bin/python3 orbit-wars-data/simulate_all_episodes.py
```

---

## 📦 Compilação e Submissão ao Kaggle

Para enviar o seu agente ao Kaggle, é necessário empacotar o código nos formatos oficiais aceitos pela competição (standalone compilado ou tarball):

### 1. Compilando as Submissões
Rode o script builder para gerar automaticamente as duas versões de entrega:
```bash
PYTHONPATH=. .venv/bin/python3 build.py
```
Isso criará:
* `submission.py`: Arquivo único standalone contendo todas as classes acopladas para validação direta.
* `submission.tar.gz`: Pacote compactado estruturado contendo todos os módulos táticos.

### 2. Enviando para o Servidor do Kaggle
Para submeter a versão de melhor desempenho direto do seu terminal:
```bash
.venv/bin/kaggle competitions submit -c orbit-wars -f submission.tar.gz -m "refactor(heuristic): implement stateful targeting tracker and dynamic defense reserve scaling"
```

### 3. Verificando o Status da Submissão
Para monitorar a avaliação e a pontuação pública na escada competitiva:
```bash
.venv/bin/kaggle competitions submissions -c orbit-wars
```