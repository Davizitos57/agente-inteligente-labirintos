from pathlib import Path
from buscas import LabirintoBusca, ResultadoBusca
from typing import Optional

MAPAS = {
    "1": {
        "nome": "Pequeno",
        "uniforme": "labirinto_pequeno_uniforme.txt",
        "variado": "labirinto_pequeno_custos_variados.txt"
    },
    "2": {
        "nome": "Médio",
        "uniforme": "labirinto_medio_uniforme.txt",
        "variado": "labirinto_medio_custos_variados.txt"
    },
    "3": {
        "nome": "Grande",
        "uniforme": "labirinto_grande_uniforme.txt",
        "variado": "labirinto_grande_custos_variados.txt"
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

def escolher_tipo_custo():
    print("\nSelecione o tipo de custo:")
    print("1 - Custo uniforme")
    print("2 - Custo variado")

    opcao = input("Opção: " ).strip()

    if opcao not in ["1", "2"]:
        raise ValueError("Opção inválida. Escolha 1 ou 2.")
    
    return opcao == "2"

def escolher_algoritmo(): 
    print("\n------------------------------------------------------\n")
    print("Selecione o algoritmo de busca:")
    print("1 - Busca em Profundidade (DFS)")
    print("2 - Busca em Largura (BFS)")
    print("3 - Busca Uniforme (UCS)")
    print("4 - Busca Gulosa (Greedy Best-First Search)")
    print("5 - A*")

    opcao = input("Opção: ").strip()
    return opcao

def imprimir_labirinto(lab: LabirintoBusca, resultado: Optional[ResultadoBusca] = None, mostrar_explorados: bool = True):
    caminho = set(resultado.caminho) if resultado and resultado.encontrado else set()
    explorados = set(resultado.estados_explorados) if resultado and mostrar_explorados else set()

    print()
    for i in range(lab.altura):
        for j in range(lab.largura):
            estado = (i, j)
            if lab.paredes[i][j]:
                print('#', end='')
            elif estado == lab.inicio:
                print('A', end='')
            elif estado == lab.objetivo:
                print('B', end='')
            elif estado in caminho:
                print('█', end='')
            elif estado in explorados:
                print('░', end='')
            else:
                print(' ', end='')
        print()
    print()

def imprimir_metricas(resultado: ResultadoBusca):
    print("\n------------------------------------------------------\n")
    print(f'Resultados obtidos:\n')
    print(f'Algoritmo executado: {resultado.algoritmo}')
    print(f'Solução encontrada: {"sim" if resultado.encontrado else "não"}')
    print(f'Nós explorados: {resultado.nos_explorados}')
    print(f'Nós expandidos: {resultado.nos_expandidos}')
    print(f'Tamanho do caminho encontrado: {resultado.tamanho_caminho}')
    print(f'Custo total do caminho: {resultado.custo_total}')
    print(f'Tempo de execução: {resultado.tempo_execucao:.4f}')
    print(f'Tamanho máximo da fronteira: {resultado.tamanho_fronteira}')

def main():
    mapa_escolhido = escolher_mapa()
    usar_custo_variado = escolher_tipo_custo()

    arquivo_mapa = mapa_escolhido["variado"] if usar_custo_variado else mapa_escolhido["uniforme"]

    nome_arquivo_labirinto = Path("mapas") / arquivo_mapa

    if not nome_arquivo_labirinto.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {nome_arquivo_labirinto}"
        )

    labirinto = LabirintoBusca(
        nome_arquivo_labirinto,
        usar_custo_variado = usar_custo_variado
    )

    print("\nCustos dos vizinhos do início:")
    for acao, estado, custo in labirinto.vizinhos(labirinto.inicio):
        print(f"{acao} -> {estado} | custo: {custo}")

    print("\n------------------------------------------------------\n")
    print(f"Mapa carregado: {mapa_escolhido['nome']}")
    print(f"Arquivo: {nome_arquivo_labirinto}")

    print("\nLabirinto:")
    labirinto.mostrar()

    print(f"\nInício: {labirinto.inicio}")
    print(f"Objetivo: {labirinto.objetivo}")
    print(f"Altura: {labirinto.altura}")
    print(f"Largura: {labirinto.largura}")

    print("\nVizinhos do início:")
    print(labirinto.vizinhos(labirinto.inicio))

    print("\nHeurística do início até o objetivo:", labirinto.heuristica(labirinto.inicio))

    while True:
        opcao = escolher_algoritmo()

        match opcao:
            case '1':
                resultado = labirinto.DFS()
            case '2':
                resultado = labirinto.BFS()
            case '3':
                resultado = labirinto.UCS()
            case '4':
                resultado = labirinto.busca_gulosa()
            case '5':
                resultado = labirinto.busca_a_estrela()
            case _:
                print('Opção inválida!')
                continue

        print('\nResultado da busca:')
        imprimir_labirinto(labirinto, resultado=resultado, mostrar_explorados=True)
        imprimir_metricas(resultado)

        continuar = input("\nDeseja testar outra busca neste mesmo mapa? (s/n): ").strip().lower()

        if continuar != 's':
            print("Encerrando...")
            break

if __name__ == "__main__":
    main()