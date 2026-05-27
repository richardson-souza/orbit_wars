### 5. Avaliação (Evaluation)

Nesta etapa, o nosso agente deixa de ser um experimento de laboratório e é submetido a um escrutínio rigoroso focado exclusivamente na capacidade de gerar valor de negócio: vencer o jogo.

#### 5.1 Avaliar Resultados (Evaluate Results)

Aqui avaliamos a extensão em que o modelo atende aos critérios de sucesso finais: terminar o turno 500 com a maior quantidade de naves somadas ou ser o último jogador sobrevivente.

- **Teste de Estresse em Múltiplos Cenários:** Uma avaliação técnica pode mostrar que o nosso modelo vence a heurística básica "Nearest Planet Sniper". Porém, a avaliação de negócio exige testar o agente em arenas de 4 jogadores, onde a simetria de início muda (cada jogador recebe apenas um planeta do grupo inicial em vez de planetas diagonalmente opostos no quadrante 1 e 4). O modelo lida bem com a diplomacia implícita e o caos de 3 oponentes?
    
- **Análise de Falsos Positivos Estratégicos:** O modelo pode ter aprendido tecnicamente a capturar planetas perfeitamente. No entanto, do ponto de vista do negócio, ele pode estar capturando cometas (que produzem apenas 1 nave por turno e desaparecem) no exato momento em que eles estão prestes a sair do mapa, perdendo toda a frota investida. Isso é uma falha de negócio grave.
    
- **Saídas (Outputs):** Um relatório de avaliação confirmando se o agente sobrevive aos 500 turnos de forma lucrativa (acumulando naves) ou se o modelo precisa ser rejeitado por falhas estratégicas.
#### 5.2 Revisar Processo (Review Process)

Esta tarefa exige que a equipe olhe para o retrovisor e identifique gargalos no nosso ciclo de desenvolvimento usando as ferramentas de telemetria da competição.

- **Auditoria de Decisões via Replay:** Precisamos baixar o JSON de replay das partidas e cruzar o comportamento visual com os arquivos de log do agente. Por exemplo: o agente perdeu porque os nossos cálculos matemáticos na Fase 3 falharam em detectar a colisão contínua com o sol (raio 10 centrado em 50, 50), resultando na destruição completa das nossas frotas?.
    
- **Auditoria de Performance Operacional:** O negócio exige que as decisões sejam tomadas rapidamente. O processo de feature engineering ficou tão pesado que o modelo está consumindo o limite de 1 segundo por turno (`actTimeout`) e queimando rapidamente o orçamento de `remainingOverageTime`?. Se sim, precisamos simplificar a modelagem.
    
- **Saídas (Outputs):** Documentação das lições aprendidas, como a percepção de que enviar múltiplas frotas pequenas viaja a apenas 1.0 unidade/turno, enquanto agrupá-las em frotas maiores aumentaria a velocidade para até 6.0 unidades/turno.