from pathlib import Path
from buscas import LabirintoBusca

MAPAS = {
    "1": {
        "nome": "Pequeno",
        "arquivo": "labirinto_pequeno.txt"
    },
    "2": {
        "nome": "Médio",
        "arquivo": "labirinto_medio.txt"
    },
    "3": {
        "nome": "Grande",
        "arquivo": "labirinto_grande.txt"
    }
}

def escolher_mapa():
    print("Selecione o mapa:")
    print("1 - Pequeno")
    print("2 - Médio")
    print("3 - Grande")

    opcao = input("Opção: ").strip()

    if opcao not in MAPAS:
        raise ValueError("Opção inválida. Escolha 1, 2 ou 3.")

    return MAPAS[opcao]


def main():
    mapa_escolhido = escolher_mapa()

    nome_arquivo_labirinto = Path("mapas") / mapa_escolhido["arquivo"]

    if not nome_arquivo_labirinto.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {nome_arquivo_labirinto}"
        )

    labirinto = LabirintoBusca(nome_arquivo_labirinto)

    print(f"\nMapa carregado: {mapa_escolhido['nome']}")
    print(f"Arquivo: {nome_arquivo_labirinto}")

    print("\nLabirinto:")
    labirinto.mostrar()

    print(f"\nInício: {labirinto.inicio}")
    print(f"Objetivo: {labirinto.objetivo}")
    print(f"Altura: {labirinto.altura}")
    print(f"Largura: {labirinto.largura}")

    print("\nVizinhos do início:")
    print(labirinto.vizinhos(labirinto.inicio))

    print("\nHeurística do início até o objetivo:", labirinto.h(labirinto.inicio))


if __name__ == "__main__":
    main()