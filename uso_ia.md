# Uso de Inteligência Artificial 


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

A resposta gerada foi um algoritmo eficiente e funcional no qual não apresentou quebras significativas e se integrou bem ao código existente. O único ponto de quebra foi em relação as métricas geradas ao final da execução do algoritmo que apresentam um estrutura diferente da classe existente `ResultadoBusca`. 
Durante a execução do algoritmo em um dos labirintos foi observado que a histórico de custo que eram alimentado, continham apenas o melhor custo durante todas as execuções, por isso o código foi alterado para que o histórico armazene toda a variação dos custos entre os vizinhos e a solução atual. Por fim, a partir do código gerado, foi alterado/incluido novas métricas que estavam ausentes ou mal calculadas dado o enunciado do trabalho.
