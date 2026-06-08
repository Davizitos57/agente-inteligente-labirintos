import heapq
import itertools
import math
import os
import time
from typing import Dict, List, Set

from labirinto import Estado, No, LabirintoBusca
from buscas_classicas.buscas import BuscasClassicas
from resultados import ResultadoBuscaOnline


class AgenteOnlineAEstrela:
    DESCONHECIDO = "?"
    PAREDE = "#"

    def __init__(self, labirinto_real: LabirintoBusca):
        # O labirinto real representa o ambiente completo.
        # O agente não deve usar esse mapa inteiro para planejar diretamente.
        self.labirinto_real = labirinto_real

        self.altura = labirinto_real.altura
        self.largura = labirinto_real.largura

        self.inicio = labirinto_real.inicio
        self.objetivo = labirinto_real.objetivo
        self.posicao_atual = self.inicio

        # Mapa interno do agente.
        # Inicialmente, todas as células são desconhecidas.
        self.mapa_interno = [
            [self.DESCONHECIDO for _ in range(self.largura)]
            for _ in range(self.altura)
        ]

        self.celulas_reveladas: Set[Estado] = set()

        self.caminho_percorrido: List[Estado] = [self.inicio]

        self.acoes_executadas: List[str] = []

        self.contagem_visitas: Dict[Estado, int] = {
            self.inicio: 1
        }

        self.movimentos = 0
        self.custo_real = 0.0
        self.replanejamentos = 0
        self.celulas_revisitadas = 0

    def executar(self, mostrar_passo_a_passo: bool = True, delay: float = 0.15) -> ResultadoBuscaOnline:
        inicio_tempo = time.time()

        custo_otimo_offline = self.calcular_custo_otimo_offline()

        # Limite de segurança para evitar loop infinito
        limite_iteracoes = self.altura * self.largura * 10
        iteracoes = 0

        while self.posicao_atual != self.objetivo:
            iteracoes += 1

            if iteracoes > limite_iteracoes:
                tempo_execucao = time.time() - inicio_tempo
                return self.gerar_resultado(False, custo_otimo_offline, tempo_execucao)

            # O agente revela a posição atual e as células vizinhas
            self.perceber()

            # EXIBIÇÃO EM TEMPO REAL AQUI
            if mostrar_passo_a_passo:
               self.imprimir_estado_atual(delay)
            

            caminho_planejado, acoes_planejadas = self.planejar_com_a_estrela()

            self.replanejamentos += 1

            if not caminho_planejado or len(caminho_planejado) < 2:
                tempo_execucao = time.time() - inicio_tempo
                return self.gerar_resultado(False, custo_otimo_offline, tempo_execucao)

            proximo_estado = caminho_planejado[1]
            proxima_acao = acoes_planejadas[0]

            movimento_realizado = self.agir(proximo_estado, proxima_acao)

            if not movimento_realizado:
                continue

        # Ao chegar no objetivo, percebe a célula final
        self.perceber()
        
        # ---> EXIBIÇÃO DO FRAME FINAL (OBJETIVO ALCANÇADO)
        if mostrar_passo_a_passo:
            self.imprimir_estado_atual(delay)

        tempo_execucao = time.time() - inicio_tempo

        return self.gerar_resultado(True, custo_otimo_offline, tempo_execucao)

    def perceber(self):
        # Lista de células que serão reveladas pelo agente
        estados_para_revelar = [self.posicao_atual]

        linha, coluna = self.posicao_atual

        candidatos = [
            (linha - 1, coluna), 
            (linha + 1, coluna),  
            (linha, coluna - 1),  
            (linha, coluna + 1), 
        ]

        for estado in candidatos:
            if self.esta_dentro_do_mapa(estado):
                estados_para_revelar.append(estado)

        for estado in estados_para_revelar:
            self.revelar_celula(estado)

    def revelar_celula(self, estado: Estado):
        linha, coluna = estado

        if self.labirinto_real.paredes[linha][coluna]:
            simbolo = self.PAREDE

        elif estado == self.inicio:
            simbolo = "A"

        elif estado == self.objetivo:
            simbolo = "B"

        else:
            simbolo = self.obter_simbolo_real(estado)

        # Atualiza o mapa interno com a célula revelada
        self.mapa_interno[linha][coluna] = simbolo
        self.celulas_reveladas.add(estado)

    def planejar_com_a_estrela(self):
        contador = itertools.count() # Contador usado para evitar conflito quando dois nós têm mesma prioridade

        inicio = No(
            estado=self.posicao_atual,
            g=0.0
        )

        # Fila de prioridade do A*
        fronteira = []

        heapq.heappush(
            fronteira,
            (self.prioridade(inicio), next(contador), inicio)
        )

        melhor_g: Dict[Estado, float] = { # Guarda o menor custo conhecido até cada estado
            self.posicao_atual: 0.0
        }

        fechados: Set[Estado] = set()

        while fronteira:
            _, _, no = heapq.heappop(fronteira)

            if no.estado in fechados:
                continue

            if no.estado == self.objetivo:
                return self.reconstruir_caminho(no)

            fechados.add(no.estado)

            for acao, estado, custo in self.vizinhos_mapa_interno(no.estado): # Expande os vizinhos conhecidos ou ainda desconhecidos do mapa interno
                if estado in fechados:
                    continue

                novo_g = no.g + custo

                if novo_g < melhor_g.get(estado, math.inf): # Atualiza se encontrou um caminho mais barato até o estado
                    filho = No(
                        estado=estado,
                        pai=no,
                        acao=acao,
                        g=novo_g
                    )

                    melhor_g[estado] = novo_g

                    heapq.heappush(
                        fronteira,
                        (self.prioridade(filho), next(contador), filho)
                    )

        return [], []

    def agir(self, proximo_estado: Estado, acao: str) -> bool:
        linha, coluna = proximo_estado

        if self.labirinto_real.paredes[linha][coluna]: # Se tentou andar para uma parede real, revela a parede e não se move
            self.revelar_celula(proximo_estado)
            return False

        self.posicao_atual = proximo_estado # Atualiza a posição atual do agente

        # Atualiza métricas do movimento
        self.movimentos += 1
        self.acoes_executadas.append(acao)
        self.caminho_percorrido.append(proximo_estado)

        # Soma o custo real do terreno percorrido
        self.custo_real += self.labirinto_real.custo_terreno(proximo_estado)

        visitas_anteriores = self.contagem_visitas.get(proximo_estado, 0)  # Verifica se a célula já foi visitada antes

        if visitas_anteriores > 0:
            self.celulas_revisitadas += 1

        self.contagem_visitas[proximo_estado] = visitas_anteriores + 1

        return True

    def vizinhos_mapa_interno(self, estado: Estado):
        linha, coluna = estado

        candidatos = [
            ("cima", (linha - 1, coluna)),
            ("baixo", (linha + 1, coluna)),
            ("esquerda", (linha, coluna - 1)),
            ("direita", (linha, coluna + 1)),
        ]

        resultado = []

        for acao, vizinho in candidatos:
            if not self.esta_dentro_do_mapa(vizinho):
                continue

            l, c = vizinho
            simbolo = self.mapa_interno[l][c]

            # O agente não pode planejar atravessando paredes já reveladas
            if simbolo == self.PAREDE:
                continue

            custo = self.custo_estimado(vizinho)

            resultado.append((acao, vizinho, custo))

        return resultado

    def custo_estimado(self, estado: Estado) -> float:
        linha, coluna = estado
        simbolo = self.mapa_interno[linha][coluna]

        if simbolo == self.DESCONHECIDO: # Células desconhecidas são tratadas como custo 1

            return 1.0

        return self.labirinto_real.custo_terreno(estado) # Células reveladas usam o custo real do terreno

    def prioridade(self, no: No) -> float:
        return no.g + self.heuristica(no.estado)

    def heuristica(self, estado: Estado) -> float:
        return abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])

    def calcular_custo_otimo_offline(self) -> float:
        buscador = BuscasClassicas(self.labirinto_real) # Executa A* tradicional no mapa completo para comparação
        resultado = buscador.busca_a_estrela()

        if not resultado.encontrado:
            return 0.0

        return resultado.custo_total

    def gerar_resultado(
        self,
        encontrado: bool,
        custo_otimo_offline: float,
        tempo_execucao: float
    ) -> ResultadoBuscaOnline:
        if custo_otimo_offline > 0:
            razao = self.custo_real / custo_otimo_offline
        else:
            razao = 0.0

        return ResultadoBuscaOnline(
            algoritmo="Busca Online com Replanning A*",
            encontrado=encontrado,
            caminho=self.caminho_percorrido,
            acoes=self.acoes_executadas,
            movimentos=self.movimentos,
            custo_real=self.custo_real,
            celulas_reveladas=len(self.celulas_reveladas),
            celulas_revisitadas=self.celulas_revisitadas,
            replanejamentos=self.replanejamentos,
            custo_otimo_offline=custo_otimo_offline,
            razao_online_offline=razao,
            tempo_execucao=tempo_execucao
        )

    def reconstruir_caminho(self, no: No):
        estados = []
        acoes = []

        atual = no

        while atual is not None:
            estados.append(atual.estado)

            if atual.acao is not None:
                acoes.append(atual.acao)

            atual = atual.pai

        estados.reverse()
        acoes.reverse()

        return estados, acoes

    def obter_simbolo_real(self, estado: Estado) -> str:
        linha, coluna = estado

        if coluna < len(self.labirinto_real.linhas[linha]):
            return self.labirinto_real.linhas[linha][coluna]

        return " "

    def esta_dentro_do_mapa(self, estado: Estado) -> bool:
        linha, coluna = estado

        return (
            0 <= linha < self.altura
            and 0 <= coluna < self.largura
        )

    def imprimir_estado_atual(self, delay: float = 0.15):
        # Limpa o terminal a cada frame da animação
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("\n================ EXPLORAÇÃO: AGENTE ONLINE ================\n")
        
        for i in range(self.altura):
            linha_str = ""
            for j in range(self.largura):
                estado = (i, j)
                if estado == self.posicao_atual:
                    # Caractere especial para destacar a posição atual do agente
                    linha_str += "@" 
                else:
                    # Imprime o que o agente já descobriu (ou "?" para o desconhecido)
                    linha_str += self.mapa_interno[i][j]
            print(linha_str)
            
        # Opcional: imprimir as métricas sendo atualizadas em tempo real
        print(f"\nMovimentos: {self.movimentos} | Custo Real: {self.custo_real} | Replanejamentos: {self.replanejamentos}")
        print("=============================================================\n")
        
        time.sleep(delay)