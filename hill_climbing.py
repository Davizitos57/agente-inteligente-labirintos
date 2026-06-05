import time
import random
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from buscas import LabirintoBusca
    from buscas import Estado

class HillClimbing:
    
    def __init__(self, labirinto: "LabirintoBusca"):
        self.labirinto = labirinto
        self.distancias = {}

    def distancia(self, origem: "Estado", destino: "Estado"):
        par = (origem, destino)
        if par in self.distancias:
            return self.distancias[par]

        inicio_original = self.labirinto.inicio
        objetivo_original = self.labirinto.objetivo

        self.labirinto.inicio = origem
        self.labirinto.objetivo = destino
        resultado = self.labirinto.busca_a_estrela()
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
            return self.distancia(self.labirinto.inicio, self.labirinto.objetivo)

        custo_total = 0
        caminho_final = []
        atual = self.labirinto.inicio

        for coleta in solucao:
            custo, caminho = self.distancia(atual, coleta)
            custo_total += custo
            caminho_final.extend(caminho)
            atual = coleta

        custo, caminho = self.distancia(atual, self.labirinto.objetivo)
        custo_total += custo
        caminho_final.extend(caminho)

        return custo_total, caminho_final

    def gerar_todos_vizinhos(self, solucao: List["Estado"]) -> List[List["Estado"]]:
        """Gera toda a vizinhança possível através de troca de 2 pontos (Swap)"""
        vizinhos = []
        n = len(solucao)
        for i in range(n):
            for j in range(i + 1, n):
                vizinho = solucao.copy()
                vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
                vizinhos.append(vizinho)
        return vizinhos

    def executar(self):
        atual = self.gerar_solucao_inicial()
        custo_atual, caminho_atual = self.custo(atual)
        custo_inicial = custo_atual
        
        historico = [custo_atual]
        iteracoes = 0
        inicio_tempo = time.time()

        while True:
            iteracoes += 1
            vizinhos = self.gerar_todos_vizinhos(atual)
            
            melhor_vizinho = None
            melhor_custo_vizinho = float('inf')
            melhor_caminho_vizinho = None

            # Avalia TODOS os vizinhos e encontra o melhor (Steepest-Ascent)
            for vizinho in vizinhos:
                c, cam = self.custo(vizinho)
                if c < melhor_custo_vizinho:
                    melhor_custo_vizinho = c
                    melhor_vizinho = vizinho
                    melhor_caminho_vizinho = cam

            # Condição de parada rigorosa: só move se for estritamente melhor
            if melhor_custo_vizinho < custo_atual:
                atual = melhor_vizinho
                custo_atual = melhor_custo_vizinho
                caminho_atual = melhor_caminho_vizinho
                historico.append(custo_atual)
            else:
                # Nenhum vizinho melhora a solução. Ótimo local atingido!
                break

        tempo_execucao = time.time() - inicio_tempo

        return {
            "melhor_solucao": atual,
            "caminho": caminho_atual,
            "custo_final": custo_atual, # O custo real em que o algoritmo parou
            "custo_inicial": custo_inicial,
            "historico": historico,
            "iteracoes": iteracoes,
            "tempo_execucao": tempo_execucao,
            "houve_melhora": custo_atual < custo_inicial
        }