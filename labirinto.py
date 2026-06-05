from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

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
            conteudo = f.read()

        if conteudo.count("A") != 1:
            raise ValueError("O labirinto deve ter exatamente um ponto inicial A.")

        if conteudo.count("B") != 1:
            raise ValueError("O labirinto deve ter exatamente um objetivo B.")

        self.linhas = conteudo.splitlines()
        self.altura = len(self.linhas)
        self.largura = max(len(linha) for linha in self.linhas)

        self.paredes: List[List[bool]] = []
        self.coletas: List[Estado] = []

        self.inicio: Estado
        self.objetivo: Estado

        self._processar_linhas()

    def _processar_linhas(self):
        for i in range(self.altura):
            linha_paredes = []

            for j in range(self.largura):
                char = self.linhas[i][j] if j < len(self.linhas[i]) else " "

                if char == "A":
                    self.inicio = (i, j)
                    linha_paredes.append(False)

                elif char == "B":
                    self.objetivo = (i, j)
                    linha_paredes.append(False)

                elif char == "C":
                    self.coletas.append((i, j))
                    linha_paredes.append(False)

                elif char == "#":
                    linha_paredes.append(True)

                elif char in self.CUSTOS_VARIADOS:
                    linha_paredes.append(False)

                elif char in self.CUSTOS_COLETAS:
                    linha_paredes.append(False)

                else:
                    raise ValueError(f"Caractere inválido no labirinto: {char!r}")

            self.paredes.append(linha_paredes)

    def mostrar(self):
        for linha in self.linhas:
            print(linha)

    def mostrar_coletas(self):
        if not self.coletas:
            print("Nenhum ponto de coleta encontrado.")
            return

        print("\nPontos de coleta encontrados:")

        for indice, coleta in enumerate(self.coletas, start=1):
            print(f"C{indice}: {coleta}")

    def mostrar_ordem_coletas(self, ordem: List[Estado]):
        if not ordem:
            print("Nenhuma ordem de coleta disponível.")
            return

        print("\nOrdem inicial de visitação:")
        print(f"A {self.inicio}")

        for indice, coleta in enumerate(ordem, start=1):
            print(f"C{indice} {coleta}")

        print(f"B {self.objetivo}")

    def ordem_inicial_coletas(self) -> List[Estado]:
        return self.coletas.copy()

    def custo_terreno(self, estado: Estado) -> float:
        linha, coluna = estado

        simbolo = (
            self.linhas[linha][coluna]
            if coluna < len(self.linhas[linha])
            else " "
        )

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