from collections import deque
from dataclasses import dataclass
from resultados import ResultadoBusca, ResultadoSimulatedAnnealing
from simulated_annealing import SimulatedAnnealing
from typing import Optional, Tuple, List, Dict, Set
from pathlib import Path
import heapq
import itertools
import math
import time

Estado = Tuple[int, int]

@dataclass
class No:
    estado: Estado
    pai: Optional["No"] = None
    acao: Optional[str] = None
    g: float = 0.0

class LabirintoBusca:
    CUSTOS_VARIADOS = {
        " ": 1.0,
        ".": 1.0,
        "*": 2.0,
        "~": 3.0,
        "^": 5.0,
        "A": 1.0,
        "B": 1.0,
    }
    
    CUSTOS_COLETAS = {
        " ": 1.0,
        ".": 1.0,
        "*": 2.0,
        "~": 3.0,
        "^": 5.0,
        "A": 1.0,
        "B": 1.0,
        "C": 1.0,
    }
        
    def __init__(self, filename: str | Path, usar_custo_variado: bool = False):
        self.usar_custo_variado = usar_custo_variado

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
        self.coletas = []

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

                elif char == "C":
                    self.coletas.append((i, j))
                    row.append(False)

                elif char == "#":
                    row.append(True)

                elif char in self.CUSTOS_VARIADOS:
                    row.append(False)
                
                elif char in self.CUSTOS_COLETAS:
                    row.append(False)

                else:
                    raise ValueError(f"Caractere inválido no labirinto: {char!r}")

            self.paredes.append(row)

    def mostrar(self):
        for linha in self.linhas:
            print(linha)
    
    def mostrar_coletas(self):
        if not self.coletas:
            print("Nenhum ponto de coleta encontrado")
            return
        print("\nPontos de coleta encontrados:")

        for indice, coleta in enumerate(self.coletas, start=1):
            print(f"C{indice}:{coleta}")
        
    def mostrar_ordem_coletas(self, ordem: List[Estado]):
        if not ordem:
            print("Nenhuma ordem de coleta disponível")
            return
        print("\nOrdem inicial de visitação:")
        print(f"A {self.inicio}")

        for indice, coleta in enumerate(ordem, start=1):
            print(f"C{indice} {coleta}")

        print(f"B {self.objetivo}")

    def custo_terreno(self, estado: Estado) -> float:
        linha, coluna = estado
        simbolo = self.linhas[linha][coluna] if coluna < len(self.linhas[linha]) else " "

        if not self.usar_custo_variado:
            return 1.0

        return self.CUSTOS_VARIADOS.get(simbolo, 1.0)

    def vizinhos(self, estado: Estado):
        linha, coluna = estado

        candidatos = [
            ("cima", (linha - 1, coluna)),
            ("baixo", (linha + 1, coluna)),
            ("esquerda", (linha, coluna - 1)),
            ("direita", (linha, coluna + 1)),
        ]

        resultado = []

        for acao, (l, c) in candidatos:
            dentro_da_altura = 0 <= l < self.altura
            dentro_da_largura = 0 <= c < self.largura

            if dentro_da_altura and dentro_da_largura and not self.paredes[l][c]:
                custo = self.custo_terreno((l, c))
                resultado.append((acao, (l, c), custo))

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
        inicio_temp = time.time()
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

                fim_temp = time.time()
                tempo_execucao = fim_temp - inicio_temp

                return ResultadoBusca('Busca em Largura (BFS)', True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, len(fronteira), no.g)

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                    fronteira.append(filho)
                    em_fronteira.add(estado)

        fim_temp = time.time()
        tempo_execucao = fim_temp - inicio_temp

        return ResultadoBusca('Busca em Largura (BFS)', False, [], [], nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, len(fronteira))

    def DFS(self) -> ResultadoBusca:
        inicio_temp = time.time()
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
                fim_temp = time.time()
                tempo_execucao = fim_temp - inicio_temp
                return ResultadoBusca('Busca em Profundidade (DFS)', True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, len(fronteira), no.g)

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                    fronteira.append(filho)
                    em_fronteira.add(estado)
        
        fim_temp = time.time()
        tempo_execucao = fim_temp - inicio_temp
        return ResultadoBusca('Busca em Profundidade (DFS)', False, [], [], nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, len(fronteira))

    def _busca_prioridade(self, nome: str, funcao_prioridade) -> ResultadoBusca:
        inicio_temp = time.time()
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
                fim_temp = time.time()
                tempo_execucao = fim_temp - inicio_temp
                return ResultadoBusca(nome, True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, len(fronteira), no.g)

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

        fim_temp = time.time()
        tempo_execucao = fim_temp - inicio_temp
        return ResultadoBusca(nome, False, [], [], nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, len(fronteira))
    
    def ordem_inicial_coletas(self) -> List[Estado]:
        return self.coletas.copy()

    def executar_experimentos_annealing(self,quantidade_execucoes: int = 10):

        melhores_custos = []
        piores_custos = []
        medias_custos = []
        tempos = []
        iteracoes = []
        solucoes = []
        caminhos_explorados = []
        historicos = []
        taxa_sucesso = 0
        melhoras_registradas = 0

        for _ in range(quantidade_execucoes):

            sa = SimulatedAnnealing(labirinto=self)
       
            resultado = sa.executar()

            melhores_custos.append(resultado["melhor_custo"])
            piores_custos.append(resultado["pior_custo"])
            medias_custos.append(resultado["media_custo"])
            tempos.append(resultado["tempo_execucao"])
            iteracoes.append(resultado["iteracoes"])
            solucoes.append(resultado['melhor_solucao'])
            caminhos_explorados.append(resultado['caminho'])
            historicos.append(resultado['historico'])

            if resultado["is_taxa_aceitavel"]:
                taxa_sucesso += 1

            if resultado["houve_melhora"]:
                melhoras_registradas += 1

        melhor_custo = min(melhores_custos)
        indice_melhor = melhores_custos.index(melhor_custo)
        melhor_solucao = solucoes[indice_melhor]
        melhor_caminhos_explorado = caminhos_explorados[indice_melhor]
        # historico = historicos[indice_melhor]

        resultado = ResultadoSimulatedAnnealing('SIMULATED ANNEALING', 
                                           encontrado=True,
                                           melhor_custo=min(melhores_custos),
                                           melhor_solucao=melhor_solucao,
                                           pior_custo=max(piores_custos),
                                           custo_medio=sum(medias_custos)/len(medias_custos),
                                           tempo_medio=sum(tempos)/len(tempos),
                                           iteracoes_medias=sum(iteracoes)/len(iteracoes),
                                           quantidade_execucoes=quantidade_execucoes,
                                           temperatura_inicial=sa.temperatura_inicial,
                                           temperatura_final=sa.temperatura_final,
                                           fator_resfriamento=sa.fator_resfriamento,
                                           caminho=melhor_caminhos_explorado,
                                            taxa_sucesso=taxa_sucesso / quantidade_execucoes,
                                            taxa_melhora=melhoras_registradas / quantidade_execucoes
                                           )
        return resultado
    
    def hill_climbing(self) -> ResultadoBusca:
            inicio_temp = time.time()
            atual = No(self.inicio)
            
            nos_explorados = 1
            nos_expandidos = 0
            ordem_explorados = [atual.estado]
            
            while True:
                if atual.estado == self.objetivo:
                    caminho, acoes = self.reconstruirCaminho(atual)
                    tempo_execucao = time.time() - inicio_temp
                    return ResultadoBusca('Subida de Encosta (Hill Climbing)', True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, 1, atual.g)
                
                nos_expandidos += 1
                vizinhos = self.vizinhos(atual.estado)
                
                if not vizinhos:
                    break
                    
                melhor_vizinho = None
                # Inicializamos com a heurística atual. Qualquer vizinho precisará ser ESTRITAMENTE menor que isso.
                melhor_h = self.heuristica(atual.estado)
                
                for acao, estado, custo in vizinhos:
                    h = self.heuristica(estado)
                    
                    # Exige melhoria estrita (<) para seguir a regra "se não melhora, retorne"
                    if h < melhor_h:
                        melhor_h = h
                        melhor_vizinho = No(estado=estado, pai=atual, acao=acao, g=atual.g + custo)
                
                # Se nenhum vizinho melhorou a heurística atual, o algoritmo para (ótimo local alcançado)
                if melhor_vizinho is None:
                    break 
                    
                atual = melhor_vizinho
                nos_explorados += 1
                ordem_explorados.append(atual.estado)
                
            tempo_execucao = time.time() - inicio_temp
            return ResultadoBusca('Subida de Encosta (Hill Climbing)', False, [], [], nos_explorados, nos_expandidos, ordem_explorados, tempo_execucao, 1, atual.g)
