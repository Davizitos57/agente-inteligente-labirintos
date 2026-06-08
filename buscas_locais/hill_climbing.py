import time
from typing import TYPE_CHECKING
from buscas_locais.busca_local import BuscaLocal

if TYPE_CHECKING:
    from labirinto import LabirintoBusca

class HillClimbing(BuscaLocal):
    
    def __init__(self, labirinto: "LabirintoBusca"):
        # Repassa o labirinto para a classe pai
        super().__init__(labirinto)

    def executar(self, max_tentativas_sem_melhora: int = 100):
        atual = self.gerar_solucao_inicial()
        custo_atual, caminho_atual = self.custo(atual)
        custo_inicial = custo_atual
        
        melhor_solucao = atual.copy()
        melhor_custo = custo_atual
        melhor_caminho = caminho_atual

        historico = [custo_atual]
        iteracoes = 0
        tentativas_sem_melhora = 0

        inicio_tempo = time.time()

        # Continua tentando até esgotar o limite de tentativas frustradas
        while tentativas_sem_melhora < max_tentativas_sem_melhora:
            iteracoes += 1
            
            # 1. Gera um vizinho aleatório (herdado da classe base)
            vizinho = self.gerar_vizinho(atual)
            custo_vizinho, caminho_vizinhos = self.custo(vizinho)

            # 2. Avalia: No Hill Climbing (First-Choice), só aceita se for estritamente melhor
            if custo_vizinho < custo_atual:
                atual = vizinho
                custo_atual = custo_vizinho
                caminho_atual = caminho_vizinhos
                
                tentativas_sem_melhora = 0 # Encontrou um caminho melhor, reseta o limite
            else:
                # Se for igual ou pior, não aceita e conta como tentativa frustrada
                tentativas_sem_melhora += 1
                
            # Atualiza o melhor global encontrado até agora
            if custo_atual < melhor_custo:
                melhor_solucao = atual.copy()
                melhor_custo = custo_atual
                melhor_caminho = caminho_atual

            historico.append(custo_atual)

        tempo_execucao = time.time() - inicio_tempo

        return {
            "melhor_solucao": melhor_solucao,
            "caminho": melhor_caminho,
            "custo_final": custo_atual, # Importante: retorna onde ele parou (para expor mínimos locais)
            "custo_inicial": custo_inicial,
            "melhor_custo": melhor_custo,
            "historico": historico,
            "iteracoes": iteracoes,
            "tempo_execucao": tempo_execucao,
            "is_taxa_aceitavel": melhor_custo <= custo_inicial,
            "houve_melhora": melhor_custo < custo_inicial
        }