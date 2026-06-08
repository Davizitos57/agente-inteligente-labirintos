import { ResultadoBuscaOnline } from "./resultados.js";
import { No } from "./buscas.js";

export class AgenteOnlineAEstrela {
  static DESCONHECIDO = "?";
  static PAREDE = "#";

  constructor(labirintoReal) {
    this.labirintoReal = labirintoReal;

    this.altura = labirintoReal.altura;
    this.largura = labirintoReal.largura;

    this.inicio = labirintoReal.inicio;
    this.objetivo = labirintoReal.objetivo;

    this.posicaoAtual = this.inicio;

    this.mapaInterno = Array.from({ length: this.altura }, () =>
      Array(this.largura).fill(AgenteOnlineAEstrela.DESCONHECIDO),
    );

    this.celulasReveladas = new Set();

    this.caminhoPercorrido = [this.inicio];

    this.acoesExecutadas = [];

    this.contagemVisitas = new Map();
    this.contagemVisitas.set(this.key(this.inicio), 1);

    this.movimentos = 0;
    this.custoReal = 0;
    this.replanejamentos = 0;
    this.celulasRevisitadas = 0;
  }

  key(estado) {
    return `${estado[0]},${estado[1]}`;
  }

  async executar(mostrarPassoAPasso = true, delay = 150) {
   
    const inicioTempo = performance.now();

    const custoOtimoOffline = this.calcularCustoOtimoOffline();

    const limiteIteracoes = this.altura * this.largura * 10;

    let iteracoes = 0;
    
    while (this.key(this.posicaoAtual) !== this.key(this.objetivo)) {
      iteracoes++;

      if (iteracoes > limiteIteracoes) {
        const tempoExecucao = (performance.now() - inicioTempo) / 1000;

        return this.gerarResultado(false, custoOtimoOffline, tempoExecucao);
      }

      this.perceber();

      if (mostrarPassoAPasso) {
        this.imprimirEstadoAtual();
        await this.sleep(delay);
      }

      const [caminhoPlanejado, acoesPlanejadas] = this.planejarComAEstrela();
      
      this.replanejamentos++;

      if (!caminhoPlanejado || caminhoPlanejado.length < 2) {
        const tempoExecucao = (performance.now() - inicioTempo) / 1000;
        console.log('aquiiii')
        return this.gerarResultado(false, custoOtimoOffline, tempoExecucao);
      }

      const proximoEstado = caminhoPlanejado[1];

      const proximaAcao = acoesPlanejadas[0];

      const movimentoRealizado = this.agir(proximoEstado, proximaAcao);

      if (!movimentoRealizado) {
        continue;
      }
      console.log('iteracao: '+ iteracoes)
    }
    

    this.perceber();

    if (mostrarPassoAPasso) {
      this.imprimirEstadoAtual();
    }

    const tempoExecucao = (performance.now() - inicioTempo) / 1000;
    console.log('termina')
    return this.gerarResultado(true, custoOtimoOffline, tempoExecucao);
  }

  calcularCustoOtimoOffline() {
    const resultado = this.labirintoReal.buscaAEstrela();

    if (resultado.encontrado) {
      return resultado.custoTotal;
    } else {
      return 0.0;
    }
  }

  perceber() {
    const estadosParaRevelar = [this.posicaoAtual];

    const [linha, coluna] = this.posicaoAtual;

    const candidatos = [
      [linha - 1, coluna],
      [linha + 1, coluna],
      [linha, coluna - 1],
      [linha, coluna + 1],
    ];

    for (const estado of candidatos) {
      if (this.estaDentroDoMapa(estado)) {
        estadosParaRevelar.push(estado);
      }
    }

    for (const estado of estadosParaRevelar) {
      this.revelarCelula(estado);
    }
  }

  revelarCelula(estado) {
    const [linha, coluna] = estado;

    let simbolo;
    if (this.labirintoReal.paredes[linha][coluna]) {
      simbolo = AgenteOnlineAEstrela.PAREDE;
    } else if (this.key(estado) === this.key(this.inicio)) {
      simbolo = "A";
    } else if (this.key(estado) === this.key(this.objetivo)) {
      simbolo = "B";
    } else {
      simbolo = this.obterSimboloReal(estado);
    }

    this.mapaInterno[linha][coluna] = simbolo;

    this.celulasReveladas.add(this.key(estado));
  }

  agir(proximoEstado, acao) {
    const [linha, coluna] = proximoEstado;

    if (this.labirintoReal.paredes[linha][coluna]) {
      this.revelarCelula(proximoEstado);

      return false;
    }

    this.posicaoAtual = proximoEstado;

    this.movimentos++;

    this.acoesExecutadas.push(acao);

    this.caminhoPercorrido.push(proximoEstado);

    this.custoReal += this.labirintoReal.custoTerreno(proximoEstado);

    const chave = this.key(proximoEstado);

    const visitas = this.contagemVisitas.get(chave) || 0;

    if (visitas > 0) {
      this.celulasRevisitadas++;
    }

    this.contagemVisitas.set(chave, visitas + 1);

    return true;
  }

  heuristica(estado) {
    return (
      Math.abs(estado[0] - this.objetivo[0]) +
      Math.abs(estado[1] - this.objetivo[1])
    );
  }

  prioridade(no) {
    return no.g + this.heuristica(no.estado);
  }

  custoEstimado(estado) {
    const [l, c] = estado;

    const simbolo = this.mapaInterno[l][c];

    if (simbolo === AgenteOnlineAEstrela.DESCONHECIDO) {
      return 1.0;
    }

    return this.labirintoReal.custoTerreno(estado);
  }

  estaDentroDoMapa(estado) {
    const [linha, coluna] = estado;

    return (
      linha >= 0 && linha < this.altura && coluna >= 0 && coluna < this.largura
    );
  }

  obterSimboloReal(estado) {
    const [linha, coluna] = estado;

    if (coluna < this.labirintoReal.linhas[linha].length) {
      return this.labirintoReal.linhas[linha][coluna];
    }

    return " ";
  }

  sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  imprimirEstadoAtual() {
    let saida = "";

    for (let i = 0; i < this.altura; i++) {
      for (let j = 0; j < this.largura; j++) {
        if (this.key([i, j]) === this.key(this.posicaoAtual)) {
          saida += "@";
        } else {
          saida += this.mapaInterno[i][j];
        }
      }

      saida += "\n";
    }

    const terminal = document.getElementById("terminal-body");

    if (terminal) {
      terminal.innerHTML = `<pre>${saida}</pre>
                <hr>
                Movimentos: ${this.movimentos}
                <br>
                Custo Real: ${this.custoReal}
                <br>
                Replanejamentos: ${this.replanejamentos}`;
    }
  }

  gerarResultado(encontrado, custoOtimoOffline, tempoExecucao) {
    let razao = 0.0;
    if (custoOtimoOffline > 0) {
      razao = this.custoReal / custoOtimoOffline;
    }

    return new ResultadoBuscaOnline({
      algoritmo: "Busca Online com Replanning A*",
      encontrado: encontrado,
      caminho: this.caminhoPercorrido,
      acoes: this.acoesExecutadas,
      movimentos: this.movimentos,
      custoReal: this.custoReal,
      celulasReveladas: this.celulasReveladas.size,
      celulasRevisitadas: this.celulasRevisitadas,
      replanejamentos: this.replanejamentos,
      custoOtimoOffline: custoOtimoOffline,
      razaoOnlineOffline: razao,
      tempoExecucao: tempoExecucao,
    });
  }

  planejarComAEstrela() {
    let contador = 0;

    const inicio = new No(this.posicaoAtual, null, null, 0.0);

    const fronteira = [];

    fronteira.push({
      prioridade: this.prioridade(inicio),
      contador: contador++,
      no: inicio,
    });

    const melhorG = new Map();
    melhorG.set(this.key(this.posicaoAtual), 0.0);

    const fechados = new Set();

    while (fronteira.length > 0) {
      fronteira.sort((a, b) => {
        if (a.prioridade !== b.prioridade) {
          return a.prioridade - b.prioridade;
        }

        return a.contador - b.contador;
      });

      const atual = fronteira.shift();
      const no = atual.no;

      const chaveEstado = this.key(no.estado);

      if (fechados.has(chaveEstado)) {
        continue;
      }

      if (this.key(no.estado) === this.key(this.objetivo)) {
        return this.reconstruirCaminho(no);
      }

      fechados.add(chaveEstado);

      for (const [acao, estado, custo] of this.vizinhosMapaInterno(no.estado)) {
        const chaveVizinho = this.key(estado);

        if (fechados.has(chaveVizinho)) {
          continue;
        }

        const novoG = no.g + custo;

        const melhorAtual = melhorG.get(chaveVizinho) ?? Infinity;

        if (novoG < melhorAtual) {
          const filho = new No(estado, no, acao, novoG);

          melhorG.set(chaveVizinho, novoG);

          fronteira.push({
            prioridade: this.prioridade(filho),
            contador: contador++,
            no: filho,
          });
        }
      }
    }

    return [[], []];
  }

  reconstruirCaminho(no) {
    const estados = [];
    const acoes = [];

    let atual = no;
    console.log('no ' + no)

    while (atual !== null && atual !== undefined) {
        estados.push(atual.estado);

        if (atual.acao !== null && atual.acao !== undefined) {
            acoes.push(atual.acao);
        }

        atual = atual.pai;
    }

    estados.reverse();
    acoes.reverse();

    return [estados, acoes];
}

  vizinhosMapaInterno(estado) {
    const [linha, coluna] = estado;
    
    const candidatos = [
        ["cima", [linha - 1, coluna]],
        ["baixo", [linha + 1, coluna]],
        ["esquerda", [linha, coluna - 1]],
        ["direita", [linha, coluna + 1]]
    ];

    const resultado = [];

    for (const [acao, vizinho] of candidatos) {

        if (!this.estaDentroDoMapa(vizinho)) {
            continue;
        }

        const [l, c] = vizinho;

        const simbolo = this.mapaInterno[l][c];

        // O agente não pode planejar atravessando paredes já reveladas
        if (simbolo === AgenteOnlineAEstrela.PAREDE) {
            continue;
        }

        const custo = this.custoEstimado(vizinho);

        resultado.push([acao, vizinho, custo]);
    }

    return resultado;
}
}
