export class SimulatedAnnealing {
  constructor(
    labirinto,
    temperaturaInicial = 100.0,
    temperaturaFinal = 0.01,
    fatorResfriamento = 0.85,
  ) {
    this.labirinto = labirinto;

    this.temperaturaInicial = temperaturaInicial;

    this.temperaturaFinal = temperaturaFinal;

    this.fatorResfriamento = fatorResfriamento;

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

    const [custo, caminho] = this.distancia(atual, this.labirinto.objetivo);

    custoTotal += custo;

    caminhoFinal.push(...caminho);

    return [custoTotal, caminhoFinal];
  }

  ////////////////////////////////////////////////////////////////////
  // VIZINHANÇA
  ////////////////////////////////////////////////////////////////////

  gerarVizinho(solucao) {
    const vizinho = [...solucao];

    if (vizinho.length < 2) {
      return vizinho;
    }

    let i = Math.floor(Math.random() * vizinho.length);

    let j = Math.floor(Math.random() * vizinho.length);

    while (i === j) {
      j = Math.floor(Math.random() * vizinho.length);
    }

    [vizinho[i], vizinho[j]] = [vizinho[j], vizinho[i]];

    return vizinho;
  }

  ////////////////////////////////////////////////////////////////////
  // SIMULATED ANNEALING
  ////////////////////////////////////////////////////////////////////

  executar() {
    let temperatura = this.temperaturaInicial;

    let atual = this.gerarSolucaoInicial();

    let [custoAtual, caminhoAtual] = this.custo(atual);

    const custoInicial = custoAtual;

    let melhorSolucao = [...atual];

    let melhorCusto = custoAtual;

    let melhorCaminho = [...caminhoAtual];

    const historico = [custoAtual];

    let iteracoes = 0;

    const inicioTempo = performance.now();

    while (temperatura > this.temperaturaFinal) {
      const vizinho = this.gerarVizinho(atual);

      const [custoVizinho, caminhoVizinhos] = this.custo(vizinho);

      const delta = custoVizinho - custoAtual;

      ////////////////////////////////////////////////////////////
      // ACEITA SOLUÇÕES MELHORES
      ////////////////////////////////////////////////////////////

      if (delta < 0) {
        atual = vizinho;

        custoAtual = custoVizinho;

        caminhoAtual = caminhoVizinhos;
      }

      ////////////////////////////////////////////////////////////
      // ACEITA SOLUÇÕES PIORES COM CERTA PROBABILIDADE
      ////////////////////////////////////////////////////////////
      else {
        const probabilidade = Math.exp(-delta / temperatura);

        if (Math.random() < probabilidade) {
          atual = vizinho;

          custoAtual = custoVizinho;

          caminhoAtual = caminhoVizinhos;
        }
      }

      ////////////////////////////////////////////////////////////

      if (custoAtual < melhorCusto) {
        melhorSolucao = [...atual];

        melhorCusto = custoAtual;

        melhorCaminho = [...caminhoAtual];
      }

      historico.push(custoAtual);

      temperatura *= this.fatorResfriamento;

      iteracoes++;
    }

    const tempoExecucao = (performance.now() - inicioTempo) / 1000;

    return {
      melhorSolucao: melhorSolucao,

      caminho: melhorCaminho,

      melhorCusto: melhorCusto,

      mediaCusto: historico.reduce((a, b) => a + b, 0) / historico.length,

      piorCusto: Math.max(...historico),

      historico: historico,

      iteracoes: iteracoes,

      tempoExecucao: tempoExecucao,

      isTaxaAceitavel: custoAtual < custoInicial * 1.1,

      houveMelhora: melhorCusto < custoInicial,
    };
  }
}
