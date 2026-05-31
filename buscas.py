from dataclasses import dataclass
from pathlib import Path
from collections import deque
from typing import Optional, Tuple, List, Dict, Set
import heapq
import itertools
import math

Estado = Tuple[int, int]

@dataclass
class No:
    estado: Estado
    pai: Optional["No"] = None
    acao: Optional[str] = None
    g: float = 0.0

@dataclass
class ResultadoBusca:
    algoritmo: str
    encontrado: bool
    caminho: List[Estado]
    acoes: List[str]
    nos_explorados: int
    nos_expandidos: int
    estados_explorados: List[Estado]

    @property
    def tamanho_caminho(self) -> Optional[int]:
        return len(self.acoes) if self.encontrado else None

class LabirintoBusca:
    def __init__(self, filename: str | Path):
        with open(filename, encoding="utf-8") as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise ValueError("O labirinto deve ter exatamente um ponto inicial A.")

        if contents.count("B") != 1:
            raise ValueError("O labirinto deve ter exatamente um objetivo B.")

        linhas = contents.splitlines()

        self.linhas = linhas
        self.altura = len(linhas)
        self.largura = max(len(linha) for linha in linhas)
        self.paredes = []

        for i in range(self.altura):
            row = []

            for j in range(self.largura):
                char = linhas[i][j] if j < len(linhas[i]) else " "

                if char == "A":
                    self.inicio = (i, j)
                    row.append(False)

                elif char == "B":
                    self.objetivo = (i, j)
                    row.append(False)

                elif char == " ":
                    row.append(False)

                else:
                    row.append(True)

            self.paredes.append(row)

    def mostrar(self):
        for linha in self.linhas:
            print(linha)

    def vizinhos(self, estado: Estado):
        linha, coluna = estado

        candidatos = [
            ("up", (linha - 1, coluna)),
            ("down", (linha + 1, coluna)),
            ("left", (linha, coluna - 1)),
            ("right", (linha, coluna + 1)),
        ]

        resultado = []

        for acao, (l, c) in candidatos:
            dentro_da_altura = 0 <= l < self.altura
            dentro_da_largura = 0 <= c < self.largura

            if dentro_da_altura and dentro_da_largura and not self.paredes[l][c]:
                resultado.append((acao, (l, c), 1.0))

        return resultado

    def heuristica(self, estado: Estado) -> float:
        return abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])

    @staticmethod   
    def reconstruirCaminho(no: No):
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
    
    def UCS(self) -> ResultadoBusca:
        return self._busca_prioridade(
            'Busca de Custo Uniforme (UCS)',
            lambda no: no.g
        ) 

    def busca_gulosa(self) -> ResultadoBusca:
        return self._busca_prioridade(
            'Greedy Best-First Search',
            lambda no: self.heuristica(no.estado)
        )

    def busca_a_estrela(self) -> ResultadoBusca:
        return self._busca_prioridade(
            'A*',
            lambda no: no.g + self.heuristica(no.estado)
        )
    
    def BFS(self) -> ResultadoBusca:
        inicio = No(self.inicio)
        fronteira = deque([inicio])
        em_fronteira = {self.inicio}
        explorados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0

        while fronteira:
            no = fronteira.popleft()
            em_fronteira.remove(no.estado)
            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruirCaminho(no)
                return ResultadoBusca('Busca em Largura (BFS)', True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados)

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                    fronteira.append(filho)
                    em_fronteira.add(estado)

        return ResultadoBusca('Busca em Largura (BFS)', False, [], [], nos_explorados, nos_expandidos, ordem_explorados)

    def DFS(self) -> ResultadoBusca:
        inicio = No(self.inicio)
        fronteira = [inicio]
        em_fronteira = {self.inicio}
        explorados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0

        while fronteira:
            no = fronteira.pop()
            em_fronteira.remove(no.estado)
            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruirCaminho(no)
                return ResultadoBusca('Busca em Profundidade (DFS)', True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados)

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                    fronteira.append(filho)
                    em_fronteira.add(estado)

        return ResultadoBusca('Busca em Profundidade (DFS)', False, [], [], nos_explorados, nos_expandidos, ordem_explorados)

    def _busca_prioridade(self, nome: str, funcao_prioridade) -> ResultadoBusca:
        contador = itertools.count()
        inicio = No(self.inicio, g=0.0)
        fronteira = []
        heapq.heappush(fronteira, (funcao_prioridade(inicio), next(contador), inicio))
        melhor_g: Dict[Estado, float] = {self.inicio: 0.0}
        fechados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0

        while fronteira:
            _, _, no = heapq.heappop(fronteira)

            if no.estado in fechados:
                continue

            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruirCaminho(no)
                return ResultadoBusca(nome, True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados)

            fechados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                novo_g = no.g + custo
                if estado in fechados:
                    continue
                if novo_g < melhor_g.get(estado, math.inf):
                    filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                    melhor_g[estado] = novo_g
                    heapq.heappush(fronteira, (funcao_prioridade(filho), next(contador), filho))

        return ResultadoBusca(nome, False, [], [], nos_explorados, nos_expandidos, ordem_explorados)
