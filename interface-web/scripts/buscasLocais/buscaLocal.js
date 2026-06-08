export class BuscaLocal {
  constructor(labirinto) {
    this.labirinto = labirinto;
    this.distancias = new Map(); // Cache para não reexecutar o A* à toa
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

    const [custoFinal, caminhoFinalTrecho] = this.distancia(atual, this.labirinto.objetivo);
    custoTotal += custoFinal;
    caminhoFinal.push(...caminhoFinalTrecho);

    return [custoTotal, caminhoFinal];
  }

  /**
   * Faz a troca simples (swap) de dois pontos para explorar a vizinhança
   */
  gerarVizinho(solucao) {
    const vizinho = [...solucao];

    if (vizinho.length < 2) {
      return vizinho;
    }

    // Sorteia dois índices distintos
    let i = Math.floor(Math.random() * vizinho.length);
    let j = Math.floor(Math.random() * vizinho.length);
    
    while (i === j) {
      j = Math.floor(Math.random() * vizinho.length);
    }

    // Swap
    [vizinho[i], vizinho[j]] = [vizinho[j], vizinho[i]];

    return vizinho;
  }
}