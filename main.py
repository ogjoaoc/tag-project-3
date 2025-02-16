'''
Projeto 3
Teoria e Aplicação de Grafos - 2024.2
Prof. Díbio

Autores:
Arthur Bispo - 232000490 
João Carlos Gonçalves - 232009511
'''
import networkx as nx
import plotly.graph_objects as go

''' 
*Função que checa se houve violação da restrição dos mandantes
*naquela coloração
*Parâmetros:
jogo: jogo atual que será verificado.
cor: cor atual que estamos tentando colocar para esse jogo
jogos_por_cores: dicionário que mapeia jogo pela cor (rodada) correspondente
restricoes_mandantes: lista com jogos que não podem ocorrer por conta dos mandantes
*Retorno: True se viola as condições de mandantes em rodadas, False caso contrário
'''
def viola_restricoes_mandantes(jogo, cor, jogos_por_cores, restricoes_mandantes):
  mandante_i, visitante_i = jogo
  for jogo_vizinho, cor_vizinho in jogos_por_cores.items():
    if cor_vizinho == cor:  
      mandante_j, visitante_j = jogo_vizinho
      for (mi, mj) in restricoes_mandantes:
        if (mandante_i == mi and mandante_j == mj) or (mandante_i == mj and mandante_j == mi):
          return True  
  return False

'''
*Função de backtracking para coloração
*Complexidade exponencial: O(cores^jogos) 
*Parâmetros:
idx: índice do jogo atual que estamos tentando colorir (colocar em uma rodada)
lista_de_jogos: contém todos os possívels jogos do campeonato
jogos_por_cores: dicionário que mapeia jogo pela cor (rodada) correspondente
g: grafo que representa o campeonato
cores: lista com as cores possíveis
restricoes_rodadas: lista de restrições sobre jogos que não podem ter cores específicas (acontecer em rodadas específicas)
restricoes_mandantes: lista com jogos que não podem ocorrer por conta dos mandantes
*Retorno: True se foi possível achar uma coloração ótima, False caso contrário
'''
def backtracking(idx, lista_de_jogos, jogos_por_cores, g, cores, restricoes_rodadas, restricoes_mandantes):
  if idx >= len(lista_de_jogos):
    return True  
  jogo_atual = lista_de_jogos[idx]

  cores_utilizadas = set()
  for jogo_vizinho in g.neighbors(jogo_atual):
    if jogo_vizinho in jogos_por_cores:
      cores_utilizadas.add(jogos_por_cores[jogo_vizinho])

  for cor in range(14):
    if (cor not in cores_utilizadas and cor not in restricoes_rodadas.get(jogo_atual, []) and not viola_restricoes_mandantes(jogo_atual, cor, jogos_por_cores, restricoes_mandantes)):
      jogos_por_cores[jogo_atual] = cor
      if backtracking(idx + 1, lista_de_jogos, jogos_por_cores, g, cores, restricoes_rodadas, restricoes_mandantes):
        return True      
      del jogos_por_cores[jogo_atual]
  return False  

'''
*Função para visualização do grafo em formato de site 
*interativo usando Plotly
*Parâmetros:
G: grafo que representa o campeonato
colors: lista com as cores possíveis
coloring: dicionário que mapeia jogo pela cor (rodada) correspondente
'''
def mostrar_grafo(G, colors, coloring):
  pos = nx.spring_layout(G)
  edge_x = []
  edge_y = []
  for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]  
    edge_y += [y0, y1, None]
  edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color='#888'), 
    hoverinfo='none',
    mode='lines'
  )
  # Preparar os dados para os nós
  node_x = []
  node_y = []
  node_text = []
  node_colors = []
  for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    color_index = coloring.get(node, 0) 
    node_text.append(f"Partida {node[0]} vs {node[1]}<br>Rodada: {color_index + 1}<br>Cor: {colors[color_index]}")
    node_colors.append(colors[color_index])
  node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=[f"{node[0]} vs {node[1]}" for node in G.nodes()],
    textposition='top center',
    hovertext=node_text,
    hoverinfo='text',
    marker=dict(
        color=node_colors,
        size=20,
        line_width=2
    )
  )
  # Criar a figura Plotly
  fig = go.Figure(data=[edge_trace, node_trace],
    layout=go.Layout(
        title="<br>Grafo de Partidas e Rodadas (Coloração)",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ))
  fig.show()


if __name__ == '__main__':
  # Lista com todos os times do campeonato
  times = ['DFC', 'TFC', 'AFC', 'LFC', 'FFC', 'OFC', 'CFC']
  lista_de_jogos = []

  # Cores utilizadas
  cores = [
    'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink',
    'brown', 'gray', 'cyan', 'magenta', 'lime', 'teal', 'navy'
  ]

  # Criando o grafo
  g = nx.Graph()

  # Acionando cada jogo possível como um vértice 
  for a in times:
    for b in times:
      if a != b:
        g.add_node((a, b))
        lista_de_jogos.append((a, b))

  # Adicionando arestas entre jogos conflituosos
  for i in range(len(lista_de_jogos)):
    for j in range(i + 1, len(lista_de_jogos)):
      mandante_i, visitante_i = lista_de_jogos[i]
      mandante_j, visitante_j = lista_de_jogos[j]
      if mandante_i == mandante_j or mandante_i == visitante_j or visitante_i == mandante_j or visitante_i == visitante_j:
        g.add_edge(lista_de_jogos[i], lista_de_jogos[j])

  # Dicionário com restrições de jogos por rodadas 
  restricoes_rodadas = {
    ('DFC', 'CFC'): [0, 13],  
    ('LFC', 'FFC'): [6, 12],  
    ('OFC', 'LFC'): [9, 10],  
    ('AFC', 'FFC'): [11, 12], 
    ('CFC', 'TFC'): [1, 2],    
  }

  # Dicionário com restrições de jogos por mandantes
  restricoes_mandantes = { ('TFC', 'OFC'),  ('AFC', 'FFC') }

  jogos_por_cores = {}
  rodada_por_jogos = {}

  if backtracking(0, lista_de_jogos, jogos_por_cores, g, cores, restricoes_rodadas, restricoes_mandantes):
    print("Coloração encontrada com sucesso!")
  else:
    print("Erro ao tentar encontrar uma coloração válida.")

  for jogo, cor in jogos_por_cores.items():
    print(f"Partida {jogo[0]} vs {jogo[1]} -> Rodada {cor + 1} (Cor: {cores[cor]})")
    if cor + 1 in rodada_por_jogos:
      rodada_por_jogos[cor + 1].append(jogo)
    else:
      rodada_por_jogos[cor + 1] = [jogo]

  print()
  for i in range(len(cores)):
    print(f'Rodada {i + 1} - Cor: {cores[i]}')
  print()

  for i in range(1, 15):
    print(f'{"="*7} - Rodada {i} -{"="*7}')
    for (mandante, visitante) in rodada_por_jogos[i]:
      print(f'{mandante} vs {visitante}')
  print()

  mostrar_grafo(g, cores, jogos_por_cores)
