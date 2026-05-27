### 6. Implantação (Deployment)

Nesta fase final, o nosso agente sai do ambiente controlado de testes locais e é empacotado para o ambiente de produção (a nuvem do Kaggle). O foco muda da construção matemática para a engenharia de operações (MLOps) e monitoramento contínuo.

#### 6.1 Planejar Implantação (Plan Deployment)

A estratégia de implantação define como o nosso código validado será entregue ao sistema de avaliação do Kaggle para receber novos dados e gerar ações.

- **Arquitetura de Arquivo Único:** Se o modelo for baseado em heurísticas simples, consolidaremos toda a lógica matemática dentro da função obrigatória `def agent(obs):` na raiz de um arquivo chamado `main.py`.
    
- **Arquitetura Multi-arquivo:** Se o modelo utilizar bibliotecas auxiliares ou redes neurais, o plano de implantação exigirá empacotar todos os recursos em um arquivo `tar.gz` mantendo o `main.py` no diretório raiz.
    
- **Automação de Submissão:** A entrega ao ambiente de produção será feita via interface de linha de comando (CLI) usando o comando `kaggle competitions submit -c orbit-wars -f main.py -m "Sua Mensagem"` para garantir agilidade no fluxo de CI/CD.
#### 6.2 Planejar Monitoramento e Manutenção (Plan Monitoring and Maintenance)

Após a submissão, o agente começa a jogar contra adversários desconhecidos. Precisamos de um plano para monitorar sua saúde operacional e determinar quando uma nova iteração (manutenção) é necessária.

- **Rastreamento de Status:** Monitorar a compilação do agente na nuvem através do comando CLI `kaggle competitions submissions -c orbit-wars` para garantir que o código não quebrou por falta de dependências no servidor.
    
- **Auditoria de Partidas (Replays):** Como manutenção proativa, listar os episódios recentes do agente usando `kaggle competitions episodes -c orbit-wars`. A equipe fará o download do log e do JSON de episódios onde o agente perdeu ("Download Replays and Logs") para investigar falhas na lógica.
    
- **Gatilho de Retreinamento:** Estabelecer a tabela de classificação (_Leaderboard_) como o termômetro de negócios. Se a taxa de vitórias globais do agente estagnar ou cair posições no ranking oficial, o ciclo do CRISP-DM será reiniciado a partir da Fase 3 (Preparação de Dados) ou 4 (Modelagem).
#### 6.3 Produzir Relatório Final (Produce Final Report)

A documentação dos artefatos finais é essencial tanto para o histórico da equipe quanto para o compartilhamento de conhecimento.

- **Documentação do Agente:** Criar um relatório interno detalhando quais hiperparâmetros foram escolhidos para a produção (por exemplo, os pesos exatos usados no sistema de pontuação de alvos).
    
- **Notebook de Apresentação:** Construir um Kaggle Notebook explicativo (uma forma de implantação suportada). Este notebook detalhará aos stakeholders (ou à comunidade Kaggle, caso o código seja aberto) como o modelo lida com restrições críticas, como o raio mortal do sol e a predição da velocidade logarítmica das frotas.
#### 6.4 Revisar Projeto (Review Project)

A retrospectiva encerra o ciclo de vida da versão atual do agente, garantindo melhorias no processo da equipe para a próxima submissão.

- **Avaliação de Gargalos:** Discutir se o tempo gasto calculando o raio dos planetas usando a fórmula de produção demorou mais que o previsto na Fase de Compreensão de Dados.
    
- **Lições de Engenharia:** Documentar na base de conhecimento as armadilhas (_pitfalls_) do motor do jogo, como o fato de que frotas não mudam de tamanho durante a viagem e que cometas expiram e somem com as naves garrisonadas.
    
- **Refinamento do Fluxo:** Avaliar se a arena de testes locais de fato refletiu o caos do _Leaderboard_ oficial e o que deve ser ajustado no nosso desenho de teste para a próxima iteração.