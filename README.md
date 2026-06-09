# 🤖 Agente Inteligente para Resolução de Labirintos

Projeto educacional desenvolvido para a disciplina CSI701 - Inteligência Artificial, com foco no estudo e comparação de diferentes estratégias de busca aplicadas à resolução de labirintos.

A proposta do projeto é observar como diferentes algoritmos se comportam diante de mapas com tamanhos, custos e restrições distintas, permitindo analisar seus resultados de forma prática por meio de uma interface em terminal e uma interface web.

## 📌 Descrição do Projeto

O sistema Agente Inteligente para Resolução de Labirintos permite executar algoritmos de busca em labirintos previamente definidos, considerando cenários de custo uniforme, custos variados e pontos de coleta. Além das buscas clássicas, o projeto também contempla buscas locais e um agente online, capaz de tomar decisões a partir do conhecimento parcial do ambiente.

O projeto permite:

- Resolução de labirintos utilizando algoritmos de busca clássica.
- Aplicação de buscas locais em cenários com pontos de coleta.
- Execução de um agente online em ambientes inicialmente desconhecidos.
- Comparação entre diferentes estratégias de busca.
- Análise de métricas como custo total, caminho encontrado, nós explorados e tempo de execução.
- Visualização dos resultados por meio de interface CLI e interface web interativa.

## 🧠 Algoritmos Implementados

- DFS — Busca em Profundidade
- BFS — Busca em Largura
- UCS — Busca de Custo Uniforme
- A* — Busca com heurística
- Hill Climbing
- Simulated Annealing
- Agente Online com replanejamento

## 🗺️ Tipos de Mapas

| Tipo | Descrição |
|---|---|
| Uniforme | Todos os movimentos possuem custo igual. |
| Custos variados | Cada terreno pode possuir um custo diferente. |
| Com pontos de coleta | O agente deve considerar pontos intermediários no caminho. |

## 🚀 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=plotly&logoColor=white)

## 📁 Estrutura do Projeto
```
agente-inteligente-labirintos/
├── main.py                          # Ponto de entrada (interface CLI)
├── labirinto.py                     # Classe LabirintoBusca e No
├── visualizacao.py                  # Funções de visualização
├── agente_online.py                 # Implementação do agente online
├── resultados.py                    # Classe para armazenar resultados
│
├── buscas_classicas/
│   ├── __init__.py
│   └── buscas.py                   # DFS, BFS, UCS, A*
│
├── buscas_locais/
│   ├── __init__.py
│   ├── busca_local.py              # Classe base para buscas locais
│   ├── hill_climbing.py            # Implementação Hill Climbing
│   ├── simulated_annealing.py      # Implementação Simulated Annealing
│   └── experimentos.py             # Execução de testes
│
├── mapas/                           # Arquivos de labirintos
│   ├── labirinto_pequeno_uniforme.txt
│   ├── labirinto_pequeno_custos_variados.txt
│   ├── labirinto_pequeno_com_coletas.txt
│   ├── labirinto_medio_uniforme.txt
│   ├── labirinto_medio_custos_variados.txt
│   ├── labirinto_medio_com_coletas.txt
│   ├── labirinto_grande_uniforme.txt
│   ├── labirinto_grande_custos_variados.txt
│   └── labirinto_grande_com_coletas.txt
│
├── interface-web/                   # Interface web
│   ├── index.html
│   ├── styles/
│   │   └── style.css
│   └── scripts/
│       ├── scripts.js
│       ├── buscas.js
│       ├── agenteOnline.js
│       ├── resultados.js
│       └── buscasLocais/
│           ├── buscaLocal.js
│           ├── hillClimbing.js
│           └── simulatedAnnealing.js
│
└── README.md                        # Este arquivo
```

## 🛠️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone git@github.com:Davizitos57/agente-inteligente-labirintos.git
cd agente-inteligente-labirintos
```

---

### 2. Executar a versão em Python

Para executar a interface via terminal, utilize:

```bash
python main.py
```

Caso esteja no Linux ou o comando `python` não funcione, utilize:

```bash
python3 main.py
```

Ao executar o programa, será exibido um menu interativo no terminal. Nele, é possível selecionar o tamanho do labirinto, o tipo de mapa e o algoritmo de busca desejado.

---

### 3. Executar a interface web

Acesse a pasta da interface web:

```bash
cd interface-web
```

Abra o arquivo `index.html` diretamente no navegador.

Caso os mapas não sejam carregados corretamente, execute um servidor HTTP local a partir da pasta principal do projeto:

```bash
python -m http.server 8000
```

Ou, no Linux:

```bash
python3 -m http.server 8000
```

Depois, acesse no navegador:

```txt
http://localhost:8000/interface-web/
```

---

### 4. Instalar dependências opcionais

O projeto utiliza apenas bibliotecas padrão do Python para a execução principal. Porém, caso deseje gerar gráficos ou visualizações adicionais, instale o Matplotlib:

```bash
python -m pip install matplotlib
```

Ou, no Linux:

```bash
python3 -m pip install matplotlib
```

---

## 👨‍🏫 Créditos

Projeto desenvolvido para a disciplina **CSI701 - Inteligência Artificial**  
**Professor:** Talles Henrique de Medeiros

**Alunos:**
- [Davi Abner Almeida Santiago](https://github.com/Davizitos57)
- [Hálisson Silveira Piovezana ](https://github.com/HalissonPiov)
- [Maria Clara Barbosa Fernandes](https://github.com/mclara831)