from pathlib import Path

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

print("Selecione o mapa:")
print("1 - Pequeno")
print("2 - Médio")
print("3 - Grande")

opcao = input("Opção: ").strip()

if opcao not in MAPAS:
    raise ValueError("Opção inválida. Escolha 1, 2 ou 3.")

mapa_escolhido = MAPAS[opcao]

NOME_ARQUIVO_LABIRINTO = Path("mapas") / mapa_escolhido["arquivo"]

if not NOME_ARQUIVO_LABIRINTO.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {NOME_ARQUIVO_LABIRINTO}")

print(f"Mapa carregado: {mapa_escolhido['nome']}")
print(f"Arquivo: {NOME_ARQUIVO_LABIRINTO}")

with open(NOME_ARQUIVO_LABIRINTO, "r", encoding="utf-8") as arquivo:
    labirinto = arquivo.readlines()

for linha in labirinto:
    print(linha.strip())