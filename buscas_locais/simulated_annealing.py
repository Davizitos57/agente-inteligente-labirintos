import math
import random
import time
from typing import List, TYPE_CHECKING

from buscas_classicas.buscas import BuscasClassicas

if TYPE_CHECKING:
    from labirinto import LabirintoBusca
    from labirinto import Estado
    
    
class SimulatedAnnealing:
    
    def __init__(
            self,
            labirinto: "LabirintoBusca",
            temperatura_inicial: float = 100.0,
            temperatura_final: float = 0.01,
            fator_resfriamento: float = 0.85):

        self.labirinto = labirinto
        self.temperatura_inicial = temperatura_inicial
        self.temperatura_final = temperatura_final
        self.fator_resfriamento = fator_resfriamento

        self.distancias = {}

    def distancia(self, origem: "Estado", destino: "Estado"):
        par = (origem, destino)

        if par in self.distancias:
            return self.distancias[par]

        inicio_original = self.labirinto.inicio
        objetivo_original = self.labirinto.objetivo

        self.labirinto.inicio = origem
        self.labirinto.objetivo = destino

        buscador = BuscasClassicas(self.labirinto)
        resultado = buscador.busca_a_estrela()

        self.labirinto.inicio = inicio_original
        self.labirinto.objetivo = objetivo_original

        custo = resultado.custo_total
        caminho = resultado.caminho

        self.distancias[par] = (custo, caminho)

        return custo, caminho

    def gerar_solucao_inicial(self) -> List["Estado"]:
        solucao = self.labirinto.coletas.copy()
        random.shuffle(solucao)

        return solucao

    def custo(self, solucao: List["Estado"]):

        if len(solucao) == 0:

            return self.distancia(
                self.labirinto.inicio,
                self.labirinto.objetivo
            )

        custo_total = 0
        caminho_final = []

        atual = self.labirinto.inicio

        for coleta in solucao:

            custo, caminho = self.distancia(
                atual,
                coleta
            )

            custo_total += custo
            caminho_final.extend(caminho)

            atual = coleta

        custo, caminho = self.distancia(
            atual,
            self.labirinto.objetivo
        )

        custo_total += custo
        caminho_final.extend(caminho)

        return custo_total, caminho_final

    ####################################################################
    # VIZINHANÇA
    ####################################################################

    def gerar_vizinho(
            self,
            solucao: List["Estado"]) -> List["Estado"]:

        vizinho = solucao.copy()

        if len(vizinho) < 2:
            return vizinho

        i, j = random.sample(
            range(len(vizinho)),
            2
        )

        vizinho[i], vizinho[j] = (
            vizinho[j],
            vizinho[i]
        )

        return vizinho

    ####################################################################
    # SIMULATED ANNEALING
    ####################################################################

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

                probabilidade = math.exp(
                    -delta / temperatura
                )

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