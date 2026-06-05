from buscas_locais.experimentos import (executar_experimentos_annealing, executar_experimentos_hill_climbing)
from pathlib import Path
from labirinto import LabirintoBusca
from buscas_classicas.buscas import BuscasClassicas
from visualizacao import imprimir_labirinto

MAPAS = {
    "1": {
        "nome": "Pequeno",
        "uniforme": "labirinto_pequeno_uniforme.txt",
        "variado": "labirinto_pequeno_custos_variados.txt",
        "coleta": "labirinto_pequeno_com_coletas.txt"
    },
    "2": {
        "nome": "Médio",
        "uniforme": "labirinto_medio_uniforme.txt",
        "variado": "labirinto_medio_custos_variados.txt",
        "coleta": "labirinto_medio_com_coletas.txt"
    },
    "3": {
        "nome": "Grande",
        "uniforme": "labirinto_grande_uniforme.txt",
        "variado": "labirinto_grande_custos_variados.txt",
        "coleta": "labirinto_grande_com_coletas.txt"
    }
}

def escolher_mapa():
    print("\nSelecione o mapa:")
    print("1 - Pequeno")
    print("2 - Médio")
    print("3 - Grande")

    opcao = input("Opção: ").strip()

    if opcao not in MAPAS:
        raise ValueError("Opção inválida. Escolha 1, 2 ou 3.")

    return MAPAS[opcao]

def escolher_tipo_mapa():
    print("\nSelecione o tipo de mapas:")
    print("1 - Mapa com custo uniforme")
    print("2 - Mapa com custo variado")
    print("3 - Mapa com pontos de coleta")

    opcao = input("Opção: " ).strip()

    if opcao not in ["1", "2", "3"]:
        raise ValueError("Opção inválida. Escolha 1, 2 ou 3.")
    
    return opcao

def escolher_algoritmo(mapa_com_coletas: bool): 
    print("\n------------------------------------------------------\n")
    print("Selecione o algoritmo de busca:")
    print("1 - Busca em Profundidade (DFS)")
    print("2 - Busca em Largura (BFS)")
    print("3 - Busca Uniforme (UCS)")
    print("4 - Busca Gulosa (Greedy Best-First Search)")
    print("5 - A*")

    if mapa_com_coletas:
        print("6 - Simulated Annealing")
        print("7 - Hill Climbing")

    opcao = input("Opção: ").strip()
    return opcao

def obter_configuracao_mapa(mapa_escolhido, tipo_mapa):
    if tipo_mapa == "1":
        return mapa_escolhido["uniforme"], False, False

    if tipo_mapa == "2":
        return mapa_escolhido["variado"], True, False

    return mapa_escolhido["coleta"], True, True

def carregar_labirinto():
    mapa_escolhido = escolher_mapa()
    tipo_mapa = escolher_tipo_mapa()

    arquivo_mapa, usar_custo_variado, mapa_com_coletas = obter_configuracao_mapa(
        mapa_escolhido,
        tipo_mapa
    )

    caminho_mapa = Path("mapas") / arquivo_mapa

    if not caminho_mapa.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_mapa}")

    labirinto = LabirintoBusca(
        caminho_mapa,
        usar_custo_variado=usar_custo_variado
    )

    return labirinto, mapa_escolhido, caminho_mapa, mapa_com_coletas

def imprimir_informacoes_labirinto(labirinto, mapa_escolhido, caminho_mapa, mapa_com_coletas):
    print("\n------------------------------------------------------\n")
    print(f"Mapa carregado: {mapa_escolhido['nome']}")
    print(f"Arquivo: {caminho_mapa}")

    print("\nLabirinto:")
    labirinto.mostrar()

    print(f"\nInício: {labirinto.inicio}")
    print(f"Objetivo: {labirinto.objetivo}")
    print(f"Altura: {labirinto.altura}")
    print(f"Largura: {labirinto.largura}")

    print("\nVizinhos do início:")
    for acao, estado, custo in labirinto.vizinhos(labirinto.inicio):
        print(f"{acao} -> {estado} | custo: {custo}")

    print("\nHeurística do início até o objetivo:", labirinto.heuristica(labirinto.inicio))

    if mapa_com_coletas:
        labirinto.mostrar_coletas()

        ordem = labirinto.ordem_inicial_coletas()
        labirinto.mostrar_ordem_coletas(ordem)


def executar_algoritmo(opcao, buscador, labirinto, mapa_com_coletas):
    match opcao:
        case "1":
            return buscador.DFS()

        case "2":
            return buscador.BFS()

        case "3":
            return buscador.UCS()

        case "4":
            return buscador.busca_gulosa()

        case "5":
            return buscador.busca_a_estrela()

        case "6":
            if not mapa_com_coletas:
                print("\nOpção disponível apenas para mapas com pontos de coleta.")
                print("Escolha o tipo de mapa 3 - Mapa com pontos de coleta.")
                return None

            return executar_experimentos_annealing(labirinto)

        case "7":
            if not mapa_com_coletas:
                print("\nOpção disponível apenas para mapas com pontos de coleta.")
                print("Escolha o tipo de mapa 3 - Mapa com pontos de coleta.")
                return None

            return executar_experimentos_hill_climbing(labirinto)

        case _:
            print("Opção inválida!")
            return None


def main():
    labirinto, mapa_escolhido, caminho_mapa, mapa_com_coletas = carregar_labirinto()

    imprimir_informacoes_labirinto(labirinto, mapa_escolhido, caminho_mapa, mapa_com_coletas)

    buscador = BuscasClassicas(labirinto)

    while True:
        opcao = escolher_algoritmo(mapa_com_coletas)
        resultado = executar_algoritmo(opcao, buscador, labirinto, mapa_com_coletas)

        if resultado is None:
            continue

        print("\nResultado da busca:")
        imprimir_labirinto(labirinto, resultado=resultado, mostrar_explorados=True)

        resultado.imprimir_metricas()

        continuar = input("\nDeseja testar outra busca neste mesmo mapa? (s/n): ").strip().lower()

        if continuar != "s":
            print("Encerrando...")
            break


if __name__ == "__main__":
    main()