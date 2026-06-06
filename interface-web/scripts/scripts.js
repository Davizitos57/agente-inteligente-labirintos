import { ResultadoBusca } from "./resultados.js";
import { ResultadoHillClimbing } from "./resultados.js";
import { ResultadoSimulatedAnnealing } from "./resultados.js";
import { LabirintoBusca } from "./buscas.js";
import { HillClimbing } from "./buscasLocais/hillClimbing.js";
import { SimulatedAnnealing } from "./buscasLocais/simulatedAnnealing.js";

const MAPAS = {
  labirinto_pequeno_uniforme: "../../mapas/labirinto_pequeno_uniforme.txt",
  labirinto_pequeno_custos_variados:
    "../../mapas/labirinto_pequeno_custos_variados.txt",
  labirinto_pequeno_com_coletas:
    "../../mapas/labirinto_pequeno_com_coletas.txt",
  labirinto_medio_uniforme: "../../mapas/labirinto_medio_uniforme.txt",
  labirinto_medio_custos_variados:
    "../../mapas/labirinto_medio_custos_variados.txt",
  labirinto_medio_com_coletas: "../../mapas/labirinto_medio_com_coletas.txt",
  labirinto_grande_uniforme: "../../mapas/labirinto_grande_uniforme.txt",
  labirinto_grande_custos_variados:
    "../../mapas/labirinto_grande_custos_variados.txt",
  labirinto_grande_com_coletas: "../../mapas/labirinto_grande_com_coletas.txt",
};

let LABIRINTO_ATUAL = {};

window.executar = executar;

export async function executar() {
  const algoritmo = document.getElementById("algoritmo").value;
  const labirinto = document.getElementById("labirinto").value;

  if (algoritmo === "none" || labirinto === "none")
    return alert(
      "Por favor, selecione um labirinto e um algoritmo para executar.",
    );

  const btn = document.querySelector("button[onclick='executar()']");
  btn.disabled = true;
  btn.querySelector(".spinner-border").style.display = "inline-block";
  btn.querySelector(".spinner-label").style.display = "Carregando...";

  const quantidadeExecucoes = parseInt(
    document.getElementById("qtdExecucoes").value,
  );
  console.log(
    `labirinto: ${labirinto}, algoritmo: ${algoritmo}, execuções: ${quantidadeExecucoes}`,
  );
  const labirintoPath = await carregarMapa(MAPAS[labirinto]);
  const usarCustoVariado =
    MAPAS[labirinto].includes("custos_variados") ||
    MAPAS[labirinto].includes("coletas");

  const labirintoObj = new LabirintoBusca(labirintoPath, usarCustoVariado);
  LABIRINTO_ATUAL = labirintoObj;
  let resultado;

  switch (algoritmo) {
    case "BFS":
      resultado = labirintoObj.BFS();
      break;
    case "DFS":
      resultado = labirintoObj.DFS();
      break;
    case "UCS":
      resultado = labirintoObj.UCS();
      break;
    case "Greedy Best First":
      resultado = labirintoObj.buscaGulosa();
      break;
    case "A*":
      resultado = labirintoObj.buscaAEstrela();
      break;
    case "Hill Climbing":
      resultado =
        labirintoObj.executarExperimentosHillClimbing(quantidadeExecucoes);
      break;

    case "Simulated Annealing":
      const temperaturaInicial = parseFloat(
        document.getElementById("temperaturaInicial").value,
      );
      const temperaturaFinal = parseFloat(
        document.getElementById("temperaturaFinal").value,
      );
      const fatorResfriamento = parseFloat(
        document.getElementById("fatorResfriamento").value,
      );

      resultado =
        labirintoObj.executarExperimentosAnnealing(quantidadeExecucoes);
      break;

    default:
      console.error("Algoritmo desconhecido");
  }

  atualizarResultados(resultado);

  btn.querySelector(".spinner-border").style.display = "none";
  btn.querySelector(".spinner-label").style.display = "Executar";
  btn.disabled = false;

  setResultadoLabirinto(resultado);
}

function atualizarResultados(resultado) {
  const metricasBuscasClassicas = document.getElementById(
    "metricas-buscas-classicas",
  );
  const metricasBuscasLocais = document.getElementById(
    "metricas-buscas-locais",
  );

  if (
    resultado instanceof ResultadoHillClimbing ||
    resultado instanceof ResultadoSimulatedAnnealing
  ) {
    atualizarResultadosBuscaLocal(resultado);
    metricasBuscasClassicas.style.display = "none";
    metricasBuscasLocais.style.display = "block";
  } else {
    setResultadosBuscaClassica(resultado);
    metricasBuscasClassicas.style.display = "block";
    metricasBuscasLocais.style.display = "none";
  }
}


function atualizarResultadosBuscaLocal(resultado) {
  document.getElementById("melhorCusto").textContent =
    resultado.melhorCusto.toFixed(2);

  document.getElementById("piorCusto").textContent =
    resultado.piorCusto.toFixed(2);

  document.getElementById("custoMedio").textContent =
    resultado.custoMedio.toFixed(2);

  document.getElementById("tempoMedio").textContent =
    resultado.tempoMedio.toFixed(4) + "s";

  document.getElementById("iteracoes").textContent =
    resultado.iteracoesMedias.toFixed(0);

  document.getElementById("execucoes").textContent =
    resultado.quantidadeExecucoes;

  document.getElementById("taxaSucesso").textContent =
    (resultado.taxaSucesso * 100).toFixed(2) + "%";

  document.getElementById("taxaMelhora").textContent =
    (resultado.taxaMelhora * 100).toFixed(2) + "%";

  document.getElementById("custoFinal").textContent =
    resultado.custoTotal.toFixed(2);

  document.getElementById("encontrado").textContent = resultado.encontrado
    ? "Sim"
    : "Não";
}

function setResultadosBuscaClassica(resultado) {
  const sucesso = resultado.encontrado ? "Sim" : "Não";
  const custo = resultado.custoTotal !== null ? resultado.custoTotal : "N/A";
  const tempo = resultado.tempoExecucao.toFixed(2) + " ms";
  const nosExplorados = resultado.estadosExplorados.length;
  const nosExpandidos = resultado.nosExpandidos;
  const tamanhoCaminho =
    resultado.tamanhoCaminho !== null ? resultado.tamanhoCaminho : "N/A";

  document.getElementById("sucesso").textContent = sucesso;
  document.getElementById("custo").textContent = custo;
  document.getElementById("tempo").textContent = tempo;
  document.getElementById("explorados").textContent = nosExplorados;
  document.getElementById("expandidos").textContent = nosExpandidos;
  document.getElementById("caminho").textContent = tamanhoCaminho;
}

async function carregarMapa(caminho) {
  const resposta = await fetch(caminho);

  if (!resposta.ok) {
    throw new Error("Erro ao carregar mapa");
  }

  return await resposta.text();
}

window.getLabirinto = getLabirinto;

function imprimirLabirinto(lab, resultado = null, mostrarExplorados = true) {
  const caminho =
    resultado && resultado.encontrado
      ? new Set(resultado.caminho.map((e) => JSON.stringify(e)))
      : new Set();

  const explorados =
    resultado && mostrarExplorados
      ? new Set(resultado.estadosExplorados.map((e) => JSON.stringify(e)))
      : new Set();

  let saida = "\n";

  for (let i = 0; i < lab.altura; i++) {
    let linha = "";

    for (let j = 0; j < lab.largura; j++) {
      const estado = [i, j];
      const chave = JSON.stringify(estado);

      if (lab.paredes[i][j]) {
        linha += "█";
      } else if (i === lab.inicio[0] && j === lab.inicio[1]) {
        linha += "A";
      } else if (i === lab.objetivo[0] && j === lab.objetivo[1]) {
        linha += "B";
      } else if (caminho.has(chave)) {
        linha += "#";
      } else if (explorados.has(chave)) {
        linha += ".";
      } else {
        linha += " ";
      }
    }
    saida += linha + "\n";
  }
  return saida;
}

export function getLabirinto() {
  const labirintoSelecionado = document.getElementById("labirinto").value;
  const labirintoView = document.getElementById("labirintoView");
  const caminhoMapa = MAPAS[labirintoSelecionado];

  carregarMapa(caminhoMapa)
    .then((conteudo) => {
      const labirintoObj = new LabirintoBusca(conteudo);
      labirintoView.innerHTML = imprimirLabirinto(labirintoObj);
    })
    .catch((erro) => {
      console.error("Erro ao carregar mapa:", erro);
    });
}

export function setResultadoLabirinto(resultado) {
  const labirintoView = document.getElementById("labirintoView");
  labirintoView.innerHTML = imprimirLabirinto(LABIRINTO_ATUAL, resultado);
}

window.setConfiguracoes = setConfiguracoes;

export function setConfiguracoes() {
  const configs = document.getElementById("conf-sa-hc");
  const algoritmo = document.getElementById("algoritmo").value;

  if (algoritmo === "Simulated Annealing") {
    configs.style.display = "block";
  } else {
    configs.style.display = "none";
  }
}
