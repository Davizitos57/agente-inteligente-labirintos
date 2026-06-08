import { BuscaLocal } from './buscaLocal.js';

export class HillClimbing extends BuscaLocal {
  constructor(labirinto) {
    // Repassa o labirinto para a classe pai
    super(labirinto);
  }

  executar(maxTentativasSemMelhora = 100) {
    let atual = this.gerarSolucaoInicial();
    let [custoAtual, caminhoAtual] = this.custo(atual);
    const custoInicial = custoAtual;

    let melhorSolucao = [...atual];
    let melhorCusto = custoAtual;
    let melhorCaminho = [...caminhoAtual];

    const historico = [custoAtual];
    let iteracoes = 0;
    let tentativasSemMelhora = 0;

    const inicioTempo = performance.now();

    // Continua tentando até esgotar o limite de tentativas frustradas
    while (tentativasSemMelhora < maxTentativasSemMelhora) {
      iteracoes++;

      // 1. Gera um vizinho aleatório (herdado da classe base)
      const vizinho = this.gerarVizinho(atual);
      const [custoVizinho, caminhoVizinho] = this.custo(vizinho);

      // 2. Avalia: No Hill Climbing (First-Choice), só aceita se for estritamente melhor
      if (custoVizinho < custoAtual) {
        atual = vizinho;
        custoAtual = custoVizinho;
        caminhoAtual = caminhoVizinho;

        tentativasSemMelhora = 0; // Encontrou um caminho melhor, reseta o limite
      } else {
        // Se for igual ou pior, não aceita e conta como tentativa frustrada
        tentativasSemMelhora++;
      }

      // Atualiza o melhor global encontrado até agora
      if (custoAtual < melhorCusto) {
        melhorSolucao = [...atual];
        melhorCusto = custoAtual;
        melhorCaminho = [...caminhoAtual];
      }

      historico.push(custoAtual);
    }

    const tempoExecucao = (performance.now() - inicioTempo) / 1000;

    return {
      melhorSolucao: melhorSolucao,
      caminho: melhorCaminho,
      custoFinal: custoAtual, // Importante: retorna onde ele parou (para expor mínimos locais)
      custoInicial: custoInicial,
      melhorCusto: melhorCusto,
      historico: historico,
      iteracoes: iteracoes,
      tempoExecucao: tempoExecucao,
      isTaxaAceitavel: melhorCusto <= custoInicial,
      houveMelhora: melhorCusto < custoInicial
    };
  }
}