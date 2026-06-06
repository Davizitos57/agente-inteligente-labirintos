# Uso de Inteligência Artificial 

## Adaptação dos mapas gerados

Durante a realização dos testes, foi observado que o mapa original gerado pela ferramenta ASCII Maze Generator apresentava uma estrutura com poucas possibilidades de percurso entre os pontos *A* e *B*. Na prática, isso fazia com que alguns algoritmos de busca, mesmo utilizando estratégias diferentes, encontrassem resultados muito semelhantes, pois havia apenas uma rota principal disponível.

Por esse motivo, foi utilizado o auxílio da IA para adaptar o mapa original, mantendo os pontos de início e fim, mas criando novas possibilidades de caminho entre eles. O objetivo dessa adaptação não foi substituir a construção do mapa, mas melhorar o cenário de testes, tornando-o mais adequado para comparar o comportamento dos algoritmos implementados.

Essa adaptação foi especialmente importante para os testes com custos variados nos movimentos. No mapa original, mesmo com a presença de pesos, algoritmos como *DFS* e *UCS* acabavam chegando à mesma solução, já que não existiam rotas alternativas suficientes para que a diferença entre as estratégias fosse percebida com clareza. Com o mapa adaptado, passou a ser possível observar melhor como cada algoritmo se comporta diante de diferentes possibilidades de percurso.

#### Mapa original gerado pela ferramenta ASCII Maze Generator

```txt
#####################
A   #   #   #   #   #
# ### ##### # ### ###
# #   #             #
# # ##### # ##### ###
#   # #   # # #     #
### # # # ### ### ###
#       # # #   #   #
# # # ##### # ### ###
# # #     #     #   #
# # ######### # ### #
# #   #       # #   #
### ### ##### ##### #
#   #   #   #     # #
# # # ##### ### #####
# # # #       #     #
# ### # # # # # #####
# #     # # # #   # #
# ### # ### ##### # #
#     #   #     #   B
#####################
```

**Mapa adaptado com auxílio de Inteligência Artificial**

```txt
#####################
A   #     #     #   #
# # ##   ##  ## # # #
#   #               #
# ### ## #### #   # #
#         #       # #
# # # # ### # ##### #
# #   #     # # #   #
# # ### # # ### ### #
#     # # #   #   # #
# ### # ### ### ### #
# # # # #     # #   #
# # ### # ### # ##  #
# #             #   #
#   ### # ##### ### #
# #       # # #     #
###  ## # # # ### ###
# #   # #           #
# ##  ### # # ### # #
#         # # #     B
#####################
```

Após a adaptação, os mapas foram revisados manualmente para verificar se continuavam válidos, se preservavam os pontos de início e fim e se apresentavam mais de uma rota viável entre A e B. Com a existência de múltiplas rotas entre A e B, torna-se possível comparar de forma mais adequada as estratégias adotadas pelos algoritmos de busca, considerando aspectos como caminho encontrado, custo total, quantidade de nós explorados e tempo de execução.

<br>

## Busca Local com Pontos de Coleta

### Simulated Annealing

Para o desenvolvimento do algoritmo de Simulated Annealing, foi feito o uso da IA para o desenvolvimento do algoritmo de acordo com a estrutura de código que o projeto já contava. Para uma resposta mais completa, foram utilizadas duas fontes de pesquisa que continha o algoritmo especificado além do enunciado da tarefa passado no trabalho e o arquivo de `busca.py`. Segue a base do prompt utilizado:

```bash
Com base na descrição 1 e 2 dos algoritmos de simmulated annealing, crie o agoritmo de busca do simulated annealing com base no enunciado da tarefa onde a fonte do arquivo é um labirinto em formato txt

##### Descrição 1: 
Disponível em: https://github.com/AlvaroCavalcante/algoritmos-busca/blob/master/Computa%C3%A7%C3%A3o%20bio.ipynb

###### Descrição 2:
Disponível em: https://sites.icmc.usp.br/sandra/G9_t2/annealing.htm

##### Descrição da atividade:
Foi submetido todo o tópico 6 da descrição do trabalho que cintém: função de custo, vizinhança, métricas obrigatórias, etc.

##### Arquivo já implementado de busca que pode ser usado como base:
busca.py
```

A resposta gerada pela IA apresentou uma implementação funcional e compatível com a estrutura geral do projeto, integrando-se ao código já existente sem quebras significativas. No entanto, foram necessários ajustes manuais para adequar a implementação aos requisitos específicos do trabalho.

O principal ponto de correção esteve relacionado às métricas geradas ao final da execução do algoritmo, pois a estrutura retornada inicialmente não estava totalmente compatível com a classe *ResultadoBusca* utilizada no projeto. Além disso, durante a execução do algoritmo em um dos labirintos, observou-se que o histórico de custos armazenava apenas o melhor custo encontrado ao longo das iterações. Por esse motivo, o código foi alterado para que o histórico registrasse também a variação dos custos entre os vizinhos gerados e a solução atual.

Por fim, a partir do código inicialmente gerado, foram realizadas alterações e inclusões de novas métricas que estavam ausentes ou eram calculadas de forma inadequada em relação ao enunciado do trabalho. Dessa forma, a IA foi utilizada como ferramenta de apoio ao desenvolvimento, enquanto a validação, adaptação e correção da solução foram realizadas manualmente conforme os critérios definidos para o projeto.



### Hill-Climbing

O algoritmo foi desenvolvido seguindo uma base de implementação pública e material disponível da disciplina, utilizando a IA para auxiliar na adaptação, mediante à lógica que deveria ser garantida e as funções desenvolvidas existentes no arquivo buscas.py. 

O prompt base e fontes foram os seguintes:

```bash
"Estou desenvolvendo o algoritmo de hill climbing, seguindo os requisitos do tp01_CSI457_2026-1 e o princípio no material CSI457_2026_busca_local_online. Me ajude a adaptar e garantir sua lógica, considerando a base do algoritmo atual e funções dos arquivos buscas e main"

"Revise de forma crítica e explicativa se a implementação do algoritmo de hill climbing está correta, considerando a implementação requisitada desse algoritmo obrigatório no trabalho tp01_CSI457_2026-1 e o princípio dele definido no material CSI457_2026_busca_local_online, dada a estrutura existente e funções do arquivo buscas. "

#### Implementação base:
Disponível em: https://github.com/AlvaroCavalcante/algoritmos-busca/blob/master/Computa%C3%A7%C3%A3o%20bio.ipynb

#### Material CSI457_2026_busca_local_online.pdf:
Disponível em: https://moodlepresencial.ufop.br/pluginfile.php/2075586/mod_resource/content/1/CSI457_2026_busca_local_online.pdf

#### Arquivo de buscas com base reutilizada de funções
buscas.py
```

A princípio, os resultados da IA foram válidos de acordo com a demanda e funcionais. Entretanto, alguns erros/incompatibilidades foram identificados ao executar:
-  Adequação para a estrutura 'LabirintoBusca', em que foram estipuladas funções inexistentes.
- Ausência da estrutura 'ResultadoExperimentoHillClimbing' herdar de 'ResultadoBusca', recebendo acesso a propriedades, como encontrado, caminho e estados_explorados
- Erro conceitual da implementação original do algoritmo ser apenas andar (cima, baixo, direta, esquerda), sem a ordem de visitação dos pontos de coleta e cálculo desse caminho, considerando ainda a função de custo

Após uma série de correções e alinhamentos entre o que estava sendo desenvolvido e o que era esperado de acordo com os requisitos do trabalho, foi atingida uma versão estável e coerente do algoritmo de Hill-Climbing.

Versão essa que consiste em uma variação denominada "Steepest-Ascent" (ou Descida Mais Íngreme): avalia todos os vizinhos possíveis, depois de mapear tudo em volta, avança exatamente na direção que desce mais rápido.