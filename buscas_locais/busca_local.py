import random
from typing import List, TYPE_CHECKING
from buscas_classicas.buscas import BuscasClassicas

if TYPE_CHECKING:
    from labirinto import LabirintoBusca
    from labirinto import Estado

class BuscaLocal:
    """Classe base que contém as funções compartilhadas de otimização"""
    
    def __init__(self, labirinto: "LabirintoBusca"):
        self.labirinto = labirinto
        self.distancias = {}  # Cache para não reexecutar o A* à toa

    def distancia(self, origem: "Estado", destino: "Estado"):
        par = (origem, destino)

        if par in self.distancias:
            return self.distancias[par]

        inicio_original = self.labirinto.inicio
        objetivo_original = self.labirinto.objetivo

        self.labirinto.inicio = origem
        self.labirinto.objetivo = destino

        # Chama o A* pela nova estrutura refatorada
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

    def gerar_vizinho(self, solucao: List["Estado"]) -> List["Estado"]:
        """Faz a troca simples (swap) de dois pontos para explorar a vizinhança"""
        vizinho = solucao.copy()

        if len(vizinho) < 2:
            return vizinho

        i, j = random.sample(range(len(vizinho)), 2)
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]

        return vizinho