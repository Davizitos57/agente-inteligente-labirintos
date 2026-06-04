from typing import TYPE_CHECKING, List, Optional, Any
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from buscas import Estado
    
@dataclass
class ResultadoBusca:
    algoritmo: str
    encontrado: bool
    caminho: List["Estado"] = field(default_factory=list)
    acoes: List[str] = field(default_factory=list)
    nos_explorados: int = 0
    nos_expandidos: int = 0
    estados_explorados: List["Estado"] = field(default_factory=list)
    tempo_execucao: Any = 0.0
    tamanho_fronteira: int = 0
    custo_total: float = 0.0

    @property
    def tamanho_caminho(self) -> Optional[int]:
        return len(self.acoes) if self.encontrado else None
    
    def imprimir_metricas(self):
        print("\n------------------------------------------------------\n")
        print(f'Resultados obtidos:\n')
        print(f'Algoritmo executado: {self.algoritmo}')
        print(f'Solução encontrada: {"sim" if self.encontrado else "não"}')
        print(f'Nós explorados: {self.nos_explorados}')
        print(f'Nós expandidos: {self.nos_expandidos}')
        print(f'Tamanho do caminho encontrado: {self.tamanho_caminho}')
        print(f'Custo total do caminho: {self.custo_total}')
        print(f'Tempo de execução: {self.tempo_execucao:.4f}')
        print(f'Tamanho máximo da fronteira: {self.tamanho_fronteira}')

@dataclass
class ResultadoSimulatedAnnealing(ResultadoBusca):
    
    melhor_custo: float = 0.0
    pior_custo: float = 0.0
    custo_medio: float = 0.0
    tempo_medio: float = 0.0
    iteracoes_medias: float = 0.0
    taxa_sucesso: float = 0.0
    temperatura_inicial: float = 0.0
    temperatura_final: float = 0.0
    fator_resfriamento: float = 0.0
    quantidade_execucoes: int = 0
    melhor_solucao: Optional[List["Estado"]] = field(default_factory=list)

    def imprimir_metricas(self):
        print("\n------------------------------------------------------\n")
        print(f'Resultados obtidos:\n')
        print(f'Algoritmo executado: {self.algoritmo}')
        print(f'Solução encontrada: {"sim" if self.encontrado else "não"}')
        print(f'Número de execuções: {self.quantidade_execucoes}')
        print(f'Temperatura inicial: {self.temperatura_inicial}')
        print(f'Temperatura final: {self.temperatura_final}')
        print(f'Fator de resfriamento: {self.fator_resfriamento}')
        print(f'Melhor custo encontrado: {self.melhor_custo}')
        print(f'Pior custo encontrado: {self.pior_custo}')
        print(f'Custo médio: {self.custo_medio:.4f}')
        print(f'Tempo médio: {self.tempo_medio:.4f}')
        print(f'Iterações médias: {self.iteracoes_medias}')