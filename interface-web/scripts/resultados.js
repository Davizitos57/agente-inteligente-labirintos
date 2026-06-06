export class ResultadoBusca {
  constructor({
    algoritmo = "",
    encontrado = false,
    caminho = [],
    acoes = [],
    nosExplorados = 0,
    nosExpandidos = 0,
    estadosExplorados = [],
    tempoExecucao = 0.0,
    tamanhoFronteira = 0,
    custoTotal = 0.0,
  } = {}) {
    this.algoritmo = algoritmo;
    this.encontrado = encontrado;
    this.caminho = caminho;
    this.acoes = acoes;
    this.nosExplorados = nosExplorados;
    this.nosExpandidos = nosExpandidos;
    this.estadosExplorados = estadosExplorados;
    this.tempoExecucao = tempoExecucao;
    this.tamanhoFronteira = tamanhoFronteira;
    this.custoTotal = custoTotal;
  }

  get tamanhoCaminho() {
    return this.encontrado ? this.acoes.length : null;
  }
}

export class ResultadoSimulatedAnnealing extends ResultadoBusca {
  constructor({
    melhorCusto = 0.0,
    piorCusto = 0.0,
    custoMedio = 0.0,
    tempoMedio = 0.0,
    iteracoesMedias = 0.0,
    taxaSucesso = 0.0,
    temperaturaInicial = 0.0,
    temperaturaFinal = 0.0,
    fatorResfriamento = 0.0,
    quantidadeExecucoes = 0,
    melhorSolucao = [],
    taxaMelhora = 0.0,
    ...resultadoBusca
  } = {}) {
    super(resultadoBusca);

    this.melhorCusto = melhorCusto;
    this.piorCusto = piorCusto;
    this.custoMedio = custoMedio;
    this.tempoMedio = tempoMedio;
    this.iteracoesMedias = iteracoesMedias;
    this.taxaSucesso = taxaSucesso;
    this.temperaturaInicial = temperaturaInicial;
    this.temperaturaFinal = temperaturaFinal;
    this.fatorResfriamento = fatorResfriamento;
    this.quantidadeExecucoes = quantidadeExecucoes;
    this.melhorSolucao = melhorSolucao;
    this.taxaMelhora = taxaMelhora;
  }
}

export class ResultadoHillClimbing extends ResultadoBusca {
  constructor({
    melhorCusto = 0.0,
    piorCusto = 0.0,
    custoMedio = 0.0,
    tempoMedio = 0.0,
    iteracoesMedias = 0.0,
    quantidadeExecucoes = 0,
    melhorSolucao = [],
    taxaSucesso = 0.0,
    taxaMelhora = 0.0,
    ...resultadoBusca
  } = {}) {
    super(resultadoBusca);

    this.melhorCusto = melhorCusto;
    this.piorCusto = piorCusto;
    this.custoMedio = custoMedio;
    this.tempoMedio = tempoMedio;
    this.iteracoesMedias = iteracoesMedias;
    this.quantidadeExecucoes = quantidadeExecucoes;
    this.melhorSolucao = melhorSolucao;
    this.taxaSucesso = taxaSucesso;
    this.taxaMelhora = taxaMelhora;
  }
}
