import heapq
import itertools
import math
import time

from collections import deque
from typing import Dict, List, Set
from labirinto import Estado, No, LabirintoBusca
from resultados import ResultadoBusca

class BuscasClassicas:
    def __init__(self, labirinto: LabirintoBusca):
        self.labirinto = labirinto

    @staticmethod
    def reconstruir_caminho(no: No):
        estados = []
        acoes = []

        atual = no

        while atual is not None:
            estados.append(atual.estado)

            if atual.acao is not None:
                acoes.append(atual.acao)

            atual = atual.pai

        estados.reverse()
        acoes.reverse()

        return estados, acoes

    def BFS(self) -> ResultadoBusca:
        inicio_tempo = time.time()

        inicio = No(self.labirinto.inicio)
        fronteira = deque([inicio])
        em_fronteira = {self.labirinto.inicio}

        explorados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []

        nos_explorados = 0
        nos_expandidos = 0
        maior_tamanho_fronteira = len(fronteira)

        while fronteira:
            maior_tamanho_fronteira = max(maior_tamanho_fronteira, len(fronteira))

            no = fronteira.popleft()
            em_fronteira.remove(no.estado)

            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.labirinto.objetivo:
                caminho, acoes = self.reconstruir_caminho(no)
                tempo_execucao = time.time() - inicio_tempo

                return ResultadoBusca(
                    algoritmo="Busca em Largura (BFS)",
                    encontrado=True,
                    caminho=caminho,
                    acoes=acoes,
                    nos_explorados=nos_explorados,
                    nos_expandidos=nos_expandidos,
                    estados_explorados=ordem_explorados,
                    tempo_execucao=tempo_execucao,
                    tamanho_fronteira=maior_tamanho_fronteira,
                    custo_total=no.g
                )

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.labirinto.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(
                        estado=estado,
                        pai=no,
                        acao=acao,
                        g=no.g + custo
                    )

                    fronteira.append(filho)
                    em_fronteira.add(estado)

        tempo_execucao = time.time() - inicio_tempo

        return ResultadoBusca(
            algoritmo="Busca em Largura (BFS)",
            encontrado=False,
            caminho=[],
            acoes=[],
            nos_explorados=nos_explorados,
            nos_expandidos=nos_expandidos,
            estados_explorados=ordem_explorados,
            tempo_execucao=tempo_execucao,
            tamanho_fronteira=maior_tamanho_fronteira,
            custo_total=0.0
        )

    def DFS(self) -> ResultadoBusca:
        inicio_tempo = time.time()

        inicio = No(self.labirinto.inicio)
        fronteira = [inicio]
        em_fronteira = {self.labirinto.inicio}

        explorados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []

        nos_explorados = 0
        nos_expandidos = 0
        maior_tamanho_fronteira = len(fronteira)

        while fronteira:
            maior_tamanho_fronteira = max(maior_tamanho_fronteira, len(fronteira))

            no = fronteira.pop()
            em_fronteira.remove(no.estado)

            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.labirinto.objetivo:
                caminho, acoes = self.reconstruir_caminho(no)
                tempo_execucao = time.time() - inicio_tempo

                return ResultadoBusca(
                    algoritmo="Busca em Profundidade (DFS)",
                    encontrado=True,
                    caminho=caminho,
                    acoes=acoes,
                    nos_explorados=nos_explorados,
                    nos_expandidos=nos_expandidos,
                    estados_explorados=ordem_explorados,
                    tempo_execucao=tempo_execucao,
                    tamanho_fronteira=maior_tamanho_fronteira,
                    custo_total=no.g
                )

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.labirinto.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(
                        estado=estado,
                        pai=no,
                        acao=acao,
                        g=no.g + custo
                    )

                    fronteira.append(filho)
                    em_fronteira.add(estado)

        tempo_execucao = time.time() - inicio_tempo

        return ResultadoBusca(
            algoritmo="Busca em Profundidade (DFS)",
            encontrado=False,
            caminho=[],
            acoes=[],
            nos_explorados=nos_explorados,
            nos_expandidos=nos_expandidos,
            estados_explorados=ordem_explorados,
            tempo_execucao=tempo_execucao,
            tamanho_fronteira=maior_tamanho_fronteira,
            custo_total=0.0
        )

    def UCS(self) -> ResultadoBusca:
        return self._busca_prioridade(
            nome="Busca de Custo Uniforme (UCS)",
            funcao_prioridade=lambda no: no.g
        )

    def busca_gulosa(self) -> ResultadoBusca:
        return self._busca_prioridade(
            nome="Greedy Best-First Search",
            funcao_prioridade=lambda no: self.labirinto.heuristica(no.estado)
        )

    def busca_a_estrela(self) -> ResultadoBusca:
        return self._busca_prioridade(
            nome="A*",
            funcao_prioridade=lambda no: no.g + self.labirinto.heuristica(no.estado)
        )

    def _busca_prioridade(self, nome: str, funcao_prioridade) -> ResultadoBusca:
        inicio_tempo = time.time()

        contador = itertools.count()
        inicio = No(self.labirinto.inicio, g=0.0)

        fronteira = []
        heapq.heappush(
            fronteira,
            (funcao_prioridade(inicio), next(contador), inicio)
        )

        melhor_g: Dict[Estado, float] = {
            self.labirinto.inicio: 0.0
        }

        fechados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []

        nos_explorados = 0
        nos_expandidos = 0
        maior_tamanho_fronteira = len(fronteira)

        while fronteira:
            maior_tamanho_fronteira = max(maior_tamanho_fronteira, len(fronteira))

            _, _, no = heapq.heappop(fronteira)

            if no.estado in fechados:
                continue

            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.labirinto.objetivo:
                caminho, acoes = self.reconstruir_caminho(no)
                tempo_execucao = time.time() - inicio_tempo

                return ResultadoBusca(
                    algoritmo=nome,
                    encontrado=True,
                    caminho=caminho,
                    acoes=acoes,
                    nos_explorados=nos_explorados,
                    nos_expandidos=nos_expandidos,
                    estados_explorados=ordem_explorados,
                    tempo_execucao=tempo_execucao,
                    tamanho_fronteira=maior_tamanho_fronteira,
                    custo_total=no.g
                )

            fechados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.labirinto.vizinhos(no.estado):
                if estado in fechados:
                    continue

                novo_g = no.g + custo

                if novo_g < melhor_g.get(estado, math.inf):
                    filho = No(
                        estado=estado,
                        pai=no,
                        acao=acao,
                        g=novo_g
                    )

                    melhor_g[estado] = novo_g

                    heapq.heappush(
                        fronteira,
                        (funcao_prioridade(filho), next(contador), filho)
                    )

        tempo_execucao = time.time() - inicio_tempo

        return ResultadoBusca(
            algoritmo=nome,
            encontrado=False,
            caminho=[],
            acoes=[],
            nos_explorados=nos_explorados,
            nos_expandidos=nos_expandidos,
            estados_explorados=ordem_explorados,
            tempo_execucao=tempo_execucao,
            tamanho_fronteira=maior_tamanho_fronteira,
            custo_total=0.0
        )