from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, List

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

    def h(self, estado: Estado) -> float:
        return abs(estado[0] - self.objetivo[0]) + abs(
            estado[1] - self.objetivo[1]
        )

    @staticmethod
    def reconstruir(no: No):
        estados = []
        acoes = []

        atual = no

        while atual.pai is not None:
            estados.append(atual.estado)
            acoes.append(atual.acao)
            atual = atual.pai

        estados.reverse()
        acoes.reverse()

        return estados, acoes