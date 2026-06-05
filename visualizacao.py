from typing import Optional

from labirinto import LabirintoBusca
from resultados import ResultadoBusca


def imprimir_labirinto(
    labirinto: LabirintoBusca,
    resultado: Optional[ResultadoBusca] = None,
    mostrar_explorados: bool = True
):
    caminho = set(resultado.caminho) if resultado and resultado.encontrado else set()

    explorados = (
        set(getattr(resultado, "estados_explorados", []))
        if resultado and mostrar_explorados
        else set()
    )

    print()

    for i in range(labirinto.altura):
        for j in range(labirinto.largura):
            estado = (i, j)

            if labirinto.paredes[i][j]:
                print("#", end="")

            elif estado == labirinto.inicio:
                print("A", end="")

            elif estado == labirinto.objetivo:
                print("B", end="")

            elif estado in caminho:
                print("█", end="")

            elif estado in explorados:
                print("░", end="")

            else:
                print(" ", end="")

        print()

    print()