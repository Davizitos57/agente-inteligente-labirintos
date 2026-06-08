import math
import random
import time
from typing import TYPE_CHECKING
from buscas_locais.busca_local import BuscaLocal

if TYPE_CHECKING:
    from labirinto import LabirintoBusca

class SimulatedAnnealing(BuscaLocal):
    
    def __init__(
            self,
            labirinto: "LabirintoBusca",
            temperatura_inicial: float = 100.0,
            temperatura_final: float = 0.01,
            fator_resfriamento: float = 0.85):

        super().__init__(labirinto)
        self.temperatura_inicial = temperatura_inicial
        self.temperatura_final = temperatura_final
        self.fator_resfriamento = fator_resfriamento

    def executar(self):
        temperatura = self.temperatura_inicial

        atual = self.gerar_solucao_inicial()
        custo_atual, caminho_atual = self.custo(atual)
        custo_inicial = custo_atual
        
        melhor_solucao = atual.copy()
        melhor_custo = custo_atual
        melhor_caminho = caminho_atual

        historico = [custo_atual]
        iteracoes = 0

        inicio_tempo = time.time()

        while temperatura > self.temperatura_final:
            
            vizinho = self.gerar_vizinho(atual)
            custo_vizinho, caminho_vizinhos = self.custo(vizinho)

            delta = custo_vizinho - custo_atual

            ########################################################
            # ACEITA SOLUÇÕES MELHORES
            ########################################################
            if delta < 0:
                atual = vizinho
                custo_atual = custo_vizinho
                caminho_atual = caminho_vizinhos

            ########################################################
            # ACEITA SOLUÇÕES PIORES COM CERTA PROBABILIDADE
            ########################################################
            else:
                probabilidade = math.exp(-delta / temperatura)
                
                if random.random() < probabilidade:
                    atual = vizinho
                    custo_atual = custo_vizinho
                    caminho_atual = caminho_vizinhos

            ########################################################
            if custo_atual < melhor_custo:
                melhor_solucao = atual.copy()
                melhor_custo = custo_atual
                melhor_caminho = caminho_atual

            historico.append(custo_atual)
            temperatura *= self.fator_resfriamento
            iteracoes += 1

        tempo_execucao = time.time() - inicio_tempo

        return {
            "melhor_solucao": melhor_solucao,
            "caminho": melhor_caminho,
            "melhor_custo": melhor_custo,
            "media_custo": sum(historico) / len(historico),
            "pior_custo": max(historico),
            "historico": historico,
            "iteracoes": iteracoes,
            "tempo_execucao": tempo_execucao,
            "is_taxa_aceitavel": custo_atual < custo_inicial * 1.1,
            "houve_melhora": melhor_custo < custo_inicial
        }