from resultados import ResultadoSimulatedAnnealing, ResultadoHillClimbing
from buscas_locais.simulated_annealing import SimulatedAnnealing
from buscas_locais.hill_climbing import HillClimbing

def executar_experimentos_annealing(labirinto, quantidade_execucoes: int = 10):
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
        sa = SimulatedAnnealing(labirinto=labirinto)

        resultado = sa.executar()

        melhores_custos.append(resultado["melhor_custo"])
        piores_custos.append(resultado["pior_custo"])
        medias_custos.append(resultado["media_custo"])
        tempos.append(resultado["tempo_execucao"])
        iteracoes.append(resultado["iteracoes"])
        solucoes.append(resultado["melhor_solucao"])
        caminhos_explorados.append(resultado["caminho"])
        historicos.append(resultado["historico"])

        if resultado["is_taxa_aceitavel"]:
            taxa_sucesso += 1

        if resultado["houve_melhora"]:
            melhoras_registradas += 1

    melhor_custo = min(melhores_custos)
    indice_melhor = melhores_custos.index(melhor_custo)

    melhor_solucao = solucoes[indice_melhor]
    melhor_caminho_explorado = caminhos_explorados[indice_melhor]

    # historico = historicos[indice_melhor]

    return ResultadoSimulatedAnnealing(
        algoritmo="Simulated Annealing",
        encontrado=True,
        caminho=melhor_caminho_explorado,
        melhor_custo=melhor_custo,
        melhor_solucao=melhor_solucao,
        pior_custo=max(piores_custos),
        custo_medio=sum(medias_custos) / len(medias_custos),
        tempo_medio=sum(tempos) / len(tempos),
        iteracoes_medias=sum(iteracoes) / len(iteracoes),
        quantidade_execucoes=quantidade_execucoes,
        temperatura_inicial=sa.temperatura_inicial,
        temperatura_final=sa.temperatura_final,
        fator_resfriamento=sa.fator_resfriamento,
        taxa_sucesso=taxa_sucesso / quantidade_execucoes,
        taxa_melhora=melhoras_registradas / quantidade_execucoes,
        custo_total=melhor_custo
    )


def executar_experimentos_hill_climbing(labirinto, quantidade_execucoes: int = 10):
    custos_finais = []
    tempos = []
    iteracoes = []
    solucoes = []
    caminhos_explorados = []

    melhoras_registradas = 0

    for _ in range(quantidade_execucoes):
        hc = HillClimbing(labirinto=labirinto)

        resultado = hc.executar()

        # Salva apenas o resultado FINAL em que a encosta parou
        custos_finais.append(resultado["custo_final"])
        tempos.append(resultado["tempo_execucao"])
        iteracoes.append(resultado["iteracoes"])
        solucoes.append(resultado["melhor_solucao"])
        caminhos_explorados.append(resultado["caminho"])

        if resultado["houve_melhora"]:
            melhoras_registradas += 1

    melhor_custo = min(custos_finais)
    indice_melhor = custos_finais.index(melhor_custo)

    return ResultadoHillClimbing(
        algoritmo="Hill Climbing",
        encontrado=True,
        caminho=caminhos_explorados[indice_melhor],
        melhor_custo=melhor_custo,
        pior_custo=max(custos_finais),
        custo_medio=sum(custos_finais) / len(custos_finais),
        tempo_medio=sum(tempos) / len(tempos),
        iteracoes_medias=sum(iteracoes) / len(iteracoes),
        quantidade_execucoes=quantidade_execucoes,
        taxa_sucesso=1.0,  # Sempre acha um caminho válido
        taxa_melhora=melhoras_registradas / quantidade_execucoes,
        melhor_solucao=solucoes[indice_melhor],
        custo_total=melhor_custo
    )