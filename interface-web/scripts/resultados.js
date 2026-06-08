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
    historico = [],
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
    this.historico = historico;
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

  plotarConvergencia() {
    const canvas = document.getElementById("graficoConvergencia");

    const labels = this.historico.map((_, indice) => indice);

    if (window.graficoSA) {
      window.graficoSA.destroy();
    }

    window.graficoSA = new Chart(canvas, {
      type: "line",

      data: {
        labels: labels,

        datasets: [
          {
            label: "Custo",

            data: this.historico,

            borderColor: "rgb(54, 162, 235)",

            backgroundColor: "rgba(54, 162, 235, 0.2)",

            tension: 0.2,

            fill: false,
          },
        ],
      },

      options: {
        responsive: true,

        plugins: {
          title: {
            display: true,
            text: "Simulated Annealing - Curva de Convergência",
          },
        },

        scales: {
          x: {
            title: {
              display: true,
              text: "Iteração",
            },
          },

          y: {
            title: {
              display: true,
              text: "Custo",
            },
          },
        },
      },
    });
  }
}

export class ResultadoHillClimbing extends ResultadoBusca {
  constructor({
    historico = [],
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
    this.historico = historico
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

export class ResultadoBuscaOnline extends ResultadoBusca {
  constructor({
    algoritmo,
    encontrado,
    caminho = [],
    acoes = [],
    movimentos = 0,
    custoReal = 0.0,
    celulasReveladas = 0,
    celulasRevisitadas = 0,
    replanejamentos = 0,
    custoOtimoOffline = 0.0,
    razaoOnlineOffline = 0.0,
    tempoExecucao = 0.0,
    ...resultado
  }) {
    super(resultado);
    this.algoritmo = algoritmo;
    this.encontrado = encontrado;

    this.caminho = caminho;
    this.acoes = acoes;

    this.movimentos = movimentos;
    this.custoReal = custoReal;

    this.celulasReveladas = celulasReveladas;
    this.celulasRevisitadas = celulasRevisitadas;

    this.replanejamentos = replanejamentos;

    this.custoOtimoOffline = custoOtimoOffline;
    this.razaoOnlineOffline = razaoOnlineOffline;

    this.tempoExecucao = tempoExecucao;
  }

  get tamanhoCaminho() {
    return this.encontrado ? this.acoes.length : null;
  }
}
