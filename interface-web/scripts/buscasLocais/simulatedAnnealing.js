import { BuscaLocal } from './buscaLocal.js';

export class SimulatedAnnealing extends BuscaLocal {
  constructor(
    labirinto,
    temperaturaInicial = 100.0,
    temperaturaFinal = 0.01,
    fatorResfriamento = 0.85
  ) {
    // Repassa o labirinto para a classe pai (BuscaLocal)
    super(labirinto);
    
    // Configurações específicas do SA
    this.temperaturaInicial = temperaturaInicial;
    this.temperaturaFinal = temperaturaFinal;
    this.fatorResfriamento = fatorResfriamento;
  }

  executar() {
    // Usa os métodos herdados da classe base
    let atual = this.gerarSolucaoInicial();
    let [custoAtual, caminhoAtual] = this.custo(atual);
    const custoInicial = custoAtual;

    let melhorSolucao = [...atual];
    let melhorCusto = custoAtual;
    let melhorCaminho = [...caminhoAtual];

    const historico = [custoAtual];
    let iteracoes = 0;
    let temperatura = this.temperaturaInicial;

    const inicioTempo = performance.now();

    // Loop principal até que a "temperatura" esfrie
    while (temperatura > this.temperaturaFinal) {
      iteracoes++;

      // 1. Gera um ÚNICO vizinho aleatório por iteração (herdado)
      const vizinho = this.gerarVizinho(atual);
      const [custoVizinho, caminhoVizinho] = this.custo(vizinho);

      // Delta: diferença de custo (como queremos minimizar, delta < 0 é melhor)
      const delta = custoVizinho - custoAtual;

      // 2. Aceita automaticamente se a nova solução for melhor (delta negativo)
      if (delta < 0) {
        atual = vizinho;
        custoAtual = custoVizinho;
        caminhoAtual = caminhoVizinho;
      } 
      // 3. Se for pior, aceita baseando-se na probabilidade térmica
      else {
        const probabilidade = Math.exp(-delta / temperatura);
        
        // Sorteia um número entre 0 e 1 e compara com a probabilidade
        if (Math.random() < probabilidade) {
          atual = vizinho;
          custoAtual = custoVizinho;
          caminhoAtual = caminhoVizinho;
        }
      }

      // Atualiza a melhor solução global encontrada até agora (para não perdê-la)
      if (custoAtual < melhorCusto) {
        melhorSolucao = [...atual];
        melhorCusto = custoAtual;
        melhorCaminho = [...caminhoAtual];
      }

      historico.push(custoAtual);
      
      // 4. Resfria o sistema
      temperatura *= this.fatorResfriamento;
    }

    const tempoExecucao = (performance.now() - inicioTempo) / 1000;

    return {
      melhorSolucao: melhorSolucao,
      caminho: melhorCaminho,
      custoFinal: custoAtual,
      custoInicial: custoInicial,
      melhorCusto: melhorCusto,
      mediaCusto: historico.reduce((a, b) => a + b, 0) / historico.length,
      piorCusto: Math.max(...historico),
      historico: historico,
      iteracoes: iteracoes,
      tempoExecucao: tempoExecucao,
      isTaxaAceitavel: melhorCusto <= custoInicial,
      houveMelhora: melhorCusto < custoInicial
    };
  }
}