import {
  ResultadoBusca,
  ResultadoHillClimbing,
  ResultadoSimulatedAnnealing,
} from "./resultados.js";
import { SimulatedAnnealing } from "./buscasLocais/simulatedAnnealing.js";
import { HillClimbing } from "./buscasLocais/hillClimbing.js";

export class No {
  constructor(estado, pai = null, acao = null, g = 0) {
    this.estado = estado;
    this.pai = pai;
    this.acao = acao;
    this.g = g;
  }
}

class PriorityQueue {
  constructor() {
    this.items = [];
  }

  enqueue(element, priority) {
    this.items.push({
      element,
      priority,
    });

    this.items.sort((a, b) => a.priority - b.priority);
  }

  dequeue() {
    return this.items.shift();
  }

  isEmpty() {
    return this.items.length === 0;
  }

  size() {
    return this.items.length;
  }
}

export class LabirintoBusca {
  static CUSTOS_VARIADOS = {
    " ": 1,
    ".": 1,
    "*": 2,
    "~": 3,
    "^": 5,
    A: 1,
    B: 1,
  };

  static CUSTOS_COLETAS = {
    " ": 1,
    ".": 1,
    "*": 2,
    "~": 3,
    "^": 5,
    A: 1,
    B: 1,
    C: 1,
  };

  constructor(conteudoMapa, usarCustoVariado = false) {
    this.usarCustoVariado = usarCustoVariado;

    const linhas = conteudoMapa.split("\n");

    this.linhas = linhas;
    this.altura = linhas.length;
    this.largura = Math.max(...linhas.map((l) => l.length));

    this.paredes = [];
    this.coletas = [];

    for (let i = 0; i < this.altura; i++) {
      let row = [];

      for (let j = 0; j < this.largura; j++) {
        let char = linhas[i][j] || " ";

        if (char === "A") {
          this.inicio = [i, j];
          row.push(false);
        } else if (char === "B") {
          this.objetivo = [i, j];
          row.push(false);
        } else if (char === "C") {
          this.coletas.push([i, j]);
          row.push(false);
        } else if (char === "#") {
          row.push(true);
        } else {
          row.push(false);
        }
      }

      this.paredes.push(row);
    }
  }

  reconstruirCaminho(no) {
    const estados = [];
    const acoes = [];

    let atual = no;

    while (atual !== null) {
      estados.push(atual.estado);

      if (atual.acao !== null) {
        acoes.push(atual.acao);
      }

      atual = atual.pai;
    }

    estados.reverse();
    acoes.reverse();

    return {
      estados,
      acoes,
    };
  }

  custoTerreno(estado) {
    const [linha, coluna] = estado;

    const simbolo =
      coluna < this.linhas[linha].length ? this.linhas[linha][coluna] : " ";

    if (!this.usarCustoVariado) {
      return 1.0;
    }

    return LabirintoBusca.CUSTOS_VARIADOS[simbolo] ?? 1.0;
  }

  heuristica(estado) {
    return (
      Math.abs(estado[0] - this.objetivo[0]) +
      Math.abs(estado[1] - this.objetivo[1])
    );
  }

  vizinhos(estado) {
    const [linha, coluna] = estado;

    const candidatos = [
      ["cima", [linha - 1, coluna]],
      ["baixo", [linha + 1, coluna]],
      ["esquerda", [linha, coluna - 1]],
      ["direita", [linha, coluna + 1]],
    ];

    const resultado = [];

    for (const [acao, [l, c]] of candidatos) {
      const dentroAltura = l >= 0 && l < this.altura;
      const dentroLargura = c >= 0 && c < this.largura;

      if (dentroAltura && dentroLargura && !this.paredes[l][c]) {
        resultado.push([acao, [l, c], this.custoTerreno([l, c])]);
      }
    }

    return resultado;
  }

  BFS() {
    const inicioTempo = performance.now();

    const inicio = new No(this.inicio);
    const fronteira = [inicio];

    const explorados = new Set();
    const emFronteira = new Set([JSON.stringify(this.inicio)]);

    const ordemExplorados = [];

    let nosExplorados = 0;
    let nosExpandidos = 0;
    let maiorTamanhoFronteira = fronteira.length;

    while (fronteira.length > 0) {
      maiorTamanhoFronteira = Math.max(maiorTamanhoFronteira, fronteira.length);

      const no = fronteira.shift();
      emFronteira.delete(JSON.stringify(no.estado));

      nosExplorados++;
      ordemExplorados.push(no.estado);

      if (
        no.estado[0] === this.objetivo[0] &&
        no.estado[1] === this.objetivo[1]
      ) 
      {
        const resultado = this.reconstruirCaminho(no);

        return new ResultadoBusca({
          algoritmo: "BFS",
          encontrado: true,
          caminho: resultado.estados,
          acoes: resultado.acoes,
          nosExplorados,
          nosExpandidos,
          estadosExplorados: ordemExplorados,
          tempoExecucao: performance.now() - inicioTempo,
          tamanhoFronteira: maiorTamanhoFronteira,
          custoTotal: no.g,
        });
      }

      explorados.add(JSON.stringify(no.estado));
      nosExpandidos++;

      for (const [acao, estado, custo] of this.vizinhos(no.estado)) {
        const chaveEstado = JSON.stringify(estado);

        if (!explorados.has(chaveEstado) && !emFronteira.has(chaveEstado)) {
          fronteira.push(new No(estado, no, acao, no.g + custo));
          emFronteira.add(chaveEstado);
        }
      }
    }

    return new ResultadoBusca({
      algoritmo: "BFS",
      encontrado: false,
    });
  }

  DFS() {
    const inicioTempo = performance.now();

    const inicio = new No(this.inicio);
    const fronteira = [inicio];

    const explorados = new Set();
    const emFronteira = new Set([JSON.stringify(this.inicio)]);

    const ordemExplorados = [];

    let nosExplorados = 0;
    let nosExpandidos = 0;
    let maiorTamanhoFronteira = fronteira.length;

    while (fronteira.length > 0) {
      maiorTamanhoFronteira = Math.max(maiorTamanhoFronteira, fronteira.length);

      const no = fronteira.pop();
      emFronteira.delete(JSON.stringify(no.estado));

      nosExplorados++;
      ordemExplorados.push(no.estado);

      if (
        no.estado[0] === this.objetivo[0] &&
        no.estado[1] === this.objetivo[1]
      ) {
        const resultado = this.reconstruirCaminho(no);

        return new ResultadoBusca({
          algoritmo: "DFS",
          encontrado: true,
          caminho: resultado.estados,
          acoes: resultado.acoes,
          nosExplorados,
          nosExpandidos,
          estadosExplorados: ordemExplorados,
          tempoExecucao: performance.now() - inicioTempo,
          tamanhoFronteira: maiorTamanhoFronteira,
          custoTotal: no.g,
        });
      }

      explorados.add(JSON.stringify(no.estado));
      nosExpandidos++;

      for (const [acao, estado, custo] of this.vizinhos(no.estado)) {
        const chaveEstado = JSON.stringify(estado);

        if (!explorados.has(chaveEstado) && !emFronteira.has(chaveEstado)) {
          fronteira.push(new No(estado, no, acao, no.g + custo));
          emFronteira.add(chaveEstado);
        }
      }
    }

    return new ResultadoBusca({
      algoritmo: "DFS",
      encontrado: false,
      caminho: [],
      acoes: [],
      nosExplorados,
      nosExpandidos,
      estadosExplorados: ordemExplorados,
      tempoExecucao: performance.now() - inicioTempo,
      tamanhoFronteira: maiorTamanhoFronteira,
      custoTotal: 0,
    });
  }

  buscaPrioridade(nome, funcaoPrioridade) {
    const inicioTempo = performance.now();

    const fronteira = new PriorityQueue();

    const inicio = new No(this.inicio);

    fronteira.enqueue(inicio, funcaoPrioridade(inicio));

    const fechados = new Set();

    const melhorG = new Map();

    melhorG.set(JSON.stringify(this.inicio), 0);

    let nosExplorados = 0;
    let nosExpandidos = 0;
    let maiorTamanhoFronteira = fronteira.size();

    const ordemExplorados = [];

    while (!fronteira.isEmpty()) {
      maiorTamanhoFronteira = Math.max(maiorTamanhoFronteira, fronteira.size());

      const { element: no } = fronteira.dequeue();

      const chave = JSON.stringify(no.estado);

      if (fechados.has(chave)) {
        continue;
      }

      nosExplorados++;

      ordemExplorados.push(no.estado);

      if (
        no.estado[0] === this.objetivo[0] &&
        no.estado[1] === this.objetivo[1]
      ) {
        const resultado = this.reconstruirCaminho(no);

        return new ResultadoBusca({
          algoritmo: nome,
          encontrado: true,
          caminho: resultado.estados,
          acoes: resultado.acoes,
          nosExplorados,
          nosExpandidos,
          estadosExplorados: ordemExplorados,
          tempoExecucao: (performance.now() - inicioTempo) / 1000,
          tamanhoFronteira: maiorTamanhoFronteira,
          custoTotal: no.g,
        });
      }

      fechados.add(chave);

      nosExpandidos++;

      for (const [acao, estado, custo] of this.vizinhos(no.estado)) {
        const novoG = no.g + custo;

        const chaveFilho = JSON.stringify(estado);

        const melhor = melhorG.get(chaveFilho);

        if (melhor === undefined || novoG < melhor) {
          melhorG.set(chaveFilho, novoG);

          const filho = new No(estado, no, acao, novoG);

          fronteira.enqueue(filho, funcaoPrioridade(filho));
        }
      }
    }

    return new ResultadoBusca({
      algoritmo: nome,
      encontrado: false,
    });
  }

  UCS() {
    return this.buscaPrioridade("UCS", (no) => no.g);
  }

  buscaGulosa() {
    return this.buscaPrioridade("Greedy", (no) => this.heuristica(no.estado));
  }

  buscaAEstrela() {
    return this.buscaPrioridade(
      "A*",
      (no) => no.g + this.heuristica(no.estado),
    );
  }

  executarExperimentosAnnealing(
    temperaturaInicial = 1000.0,
    temperaturaFinal = 0.01,
    fatorResfriamento = 0.85,
    quantidadeExecucoes = 10,
  ) {
    const melhoresCustos = [];
    const pioresCustos = [];
    const mediasCustos = [];
    const tempos = [];
    const iteracoes = [];
    const solucoes = [];
    const caminhosExplorados = [];
    const historicos = [];

    let taxaSucesso = 0;
    let melhoriasRegistradas = 0;

    let sa;

    for (let i = 0; i < quantidadeExecucoes; i++) {
      sa = new SimulatedAnnealing(
        this,
        temperaturaInicial,
        temperaturaFinal,
        fatorResfriamento,
      );

      const resultado = sa.executar();

      melhoresCustos.push(resultado.melhorCusto);
      pioresCustos.push(resultado.piorCusto);
      mediasCustos.push(resultado.mediaCusto);
      tempos.push(resultado.tempoExecucao);
      iteracoes.push(resultado.iteracoes);
      solucoes.push(resultado.melhorSolucao);
      caminhosExplorados.push(resultado.caminho);
      historicos.push(resultado.historico);

      if (resultado.isTaxaAceitavel) {
        taxaSucesso++;
      }

      if (resultado.houveMelhora) {
        melhoriasRegistradas++;
      }
    }

    const melhorCusto = Math.min(...melhoresCustos);
    const indiceMelhor = melhoresCustos.indexOf(melhorCusto);
    const historico = historicos[indiceMelhor]

    return new ResultadoSimulatedAnnealing({
      algoritmo: "SIMULATED ANNEALING",
      encontrado: true,
      melhorCusto,
      melhorSolucao: solucoes[indiceMelhor],
      piorCusto: Math.max(...pioresCustos),
      custoMedio: mediasCustos.reduce((a, b) => a + b, 0) / mediasCustos.length,
      tempoMedio: tempos.reduce((a, b) => a + b, 0) / tempos.length,
      iteracoesMedias: iteracoes.reduce((a, b) => a + b, 0) / iteracoes.length,
      quantidadeExecucoes,
      temperaturaInicial: sa.temperaturaInicial,
      temperaturaFinal: sa.temperaturaFinal,
      fatorResfriamento: sa.fatorResfriamento,
      caminho: caminhosExplorados[indiceMelhor],
      taxaSucesso: taxaSucesso / quantidadeExecucoes,
      taxaMelhora: melhoriasRegistradas / quantidadeExecucoes,
      custoTotal: melhorCusto,
      historico: historico
    });
  }

  executarExperimentosHillClimbing(quantidadeExecucoes = 10) {
    const custosFinais = [];
    const tempos = [];
    const iteracoes = [];
    const solucoes = [];
    const caminhosExplorados = [];
    const historicos = [];

    let melhoriasRegistradas = 0;

    for (let i = 0; i < quantidadeExecucoes; i++) {
      const hc = new HillClimbing(this);
      const resultado = hc.executar();

      // Caso 'custoFinal' não exista no arquivo retornado, usa 'melhorCusto'
      const custoSeguro = resultado.custoFinal !== undefined ? resultado.custoFinal : resultado.melhorCusto;

      custosFinais.push(custoSeguro);
      tempos.push(resultado.tempoExecucao || 0);
      iteracoes.push(resultado.iteracoes || 0);
      solucoes.push(resultado.melhorSolucao || []);
      caminhosExplorados.push(resultado.caminho || []);
      historicos.push(resultado.historico || []);

      if (resultado.houveMelhora) {
        melhoriasRegistradas++;
      }
    }

    const melhorCusto = Math.min(...custosFinais);

    // Proteção de índice para evitar travamento do renderizador do labirinto
    let indiceMelhor = custosFinais.indexOf(melhorCusto);
    if (indiceMelhor === -1) indiceMelhor = 0;

    const historico = historicos[indiceMelhor];

    return new ResultadoHillClimbing({
      algoritmo: "Hill Climbing",
      encontrado: true,
      caminho: caminhosExplorados[indiceMelhor],
      melhorCusto,
      piorCusto: Math.max(...custosFinais),
      custoMedio: custosFinais.reduce((a, b) => a + b, 0) / custosFinais.length,
      tempoMedio: tempos.reduce((a, b) => a + b, 0) / tempos.length,
      iteracoesMedias: iteracoes.reduce((a, b) => a + b, 0) / iteracoes.length,
      quantidadeExecucoes,
      taxaSucesso: 1.0,
      taxaMelhora: melhoriasRegistradas / quantidadeExecucoes,
      melhorSolucao: solucoes[indiceMelhor],
      custoTotal: melhorCusto,
      historico: historico
    });
  }
}
