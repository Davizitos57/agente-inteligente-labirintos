export class HillClimbing {
  constructor(labirinto) {
    this.labirinto = labirinto;
    this.distancias = new Map();
  }

  distancia(origem, destino) {
    const chave = JSON.stringify([origem, destino]);

    if (this.distancias.has(chave)) {
      return this.distancias.get(chave);
    }

    const inicioOriginal = this.labirinto.inicio;
    const objetivoOriginal = this.labirinto.objetivo;

    this.labirinto.inicio = origem;
    this.labirinto.objetivo = destino;

    const resultado = this.labirinto.buscaAEstrela();

    this.labirinto.inicio = inicioOriginal;
    this.labirinto.objetivo = objetivoOriginal;

    const custo = resultado.custoTotal;
    const caminho = resultado.caminho;

    const retorno = [custo, caminho];

    this.distancias.set(chave, retorno);

    return retorno;
  }

  /**
   * Permutação inicial das coletas
   */
  gerarSolucaoInicial() {
    const solucao = [...this.labirinto.coletas];

    for (let i = solucao.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));

      [solucao[i], solucao[j]] = [solucao[j], solucao[i]];
    }

    return solucao;
  }

  custo(solucao) {
    if (solucao.length === 0) {
      return this.distancia(this.labirinto.inicio, this.labirinto.objetivo);
    }

    let custoTotal = 0;
    let caminhoFinal = [];

    let atual = this.labirinto.inicio;

    for (const coleta of solucao) {
      const [custo, caminho] = this.distancia(atual, coleta);

      custoTotal += custo;

      caminhoFinal.push(...caminho);

      atual = coleta;
    }

    const [custoFinal, caminhoFinalTrecho] = this.distancia(
      atual,
      this.labirinto.objetivo,
    );

    custoTotal += custoFinal;

    caminhoFinal.push(...caminhoFinalTrecho);

    return [custoTotal, caminhoFinal];
  }

  /**
   * Gera toda a vizinhança através de swap
   */
  gerarTodosVizinhos(solucao) {
    const vizinhos = [];
    const n = solucao.length;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const vizinho = [...solucao];

        [vizinho[i], vizinho[j]] = [vizinho[j], vizinho[i]];

        vizinhos.push(vizinho);
      }
    }

    return vizinhos;
  }

  executar() {
    let atual = this.gerarSolucaoInicial();

    let [custoAtual, caminhoAtual] = this.custo(atual);

    const custoInicial = custoAtual;

    const historico = [custoAtual];

    let iteracoes = 0;

    const inicioTempo = performance.now();

    while (true) {
      iteracoes++;

      const vizinhos = this.gerarTodosVizinhos(atual);

      if (vizinhos.length === 0) {
        break;
      }

      let melhorVizinho = null;
      let melhorCustoVizinho = Infinity;
      let melhorCaminhoVizinho = null;

      // Steepest Ascent
      for (const vizinho of vizinhos) {
        const [custo, caminho] = this.custo(vizinho);

        if (custo < melhorCustoVizinho) {
          melhorCustoVizinho = custo;

          melhorVizinho = vizinho;

          melhorCaminhoVizinho = caminho;
        }
      }

      // Move somente se melhorar
      if (melhorCustoVizinho < custoAtual) {
        atual = melhorVizinho;

        custoAtual = melhorCustoVizinho;

        caminhoAtual = melhorCaminhoVizinho;

        historico.push(custoAtual);
      } else {
        // Ótimo local encontrado
        break;
      }
    }

    const tempoExecucao = (performance.now() - inicioTempo) / 1000;

    return {
      melhorSolucao: atual,
      caminho: caminhoAtual,
      custoFinal: custoAtual,
      custoInicial,
      historico,
      iteracoes,
      tempoExecucao,
      houveMelhora: custoAtual < custoInicial,
    };
  }
}
