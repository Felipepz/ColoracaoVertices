import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image

class GrafoMapaVisualizador:
    def __init__(self, mapa_path):
        self.mapa = Image.open(mapa_path)
        self.grafo = nx.Graph()

    def adicionar_cidade(self, cidade, posicao):
        self.grafo.add_node(cidade, pos=posicao)

    def adicionar_conexao(self, cidade1, cidade2):
        self.grafo.add_edge(cidade1, cidade2)

    def carregar_conexoes_do_arquivo(self, arquivo_path):
        with open(arquivo_path, 'r') as arquivo:
            for linha in arquivo:
                # Verifica se a linha não está vazia
                if linha.strip():
                    # Divide a linha apenas se houver pelo menos dois valores
                    cidades = linha.strip().split(' - ')
                    if len(cidades) >= 2:
                        cidade1, cidade2 = cidades
                        self.adicionar_conexao(cidade1, cidade2)
                    else:
                        print(f"A linha '{linha.strip()}' não possui informações suficientes para criar uma conexão.")

    def visualizar_grafo_no_mapa(self):
        plt.imshow(self.mapa)

        posicoes = {cidade: pos for cidade, pos in nx.get_node_attributes(self.grafo, 'pos').items()}

        # Obtém o dicionário de cores para os nós usando a coloração gulosa
        colors = nx.coloring.greedy_color(self.grafo, strategy="largest_first", interchange=True)

        nx.draw_networkx(self.grafo, pos=posicoes, with_labels=False, font_weight='bold', node_size=90, node_color=list(colors.values()))

        plt.show()

# Inicialize o visualizador de mapa
grafo_mapa_vis = GrafoMapaVisualizador('Sede_Cachoeiro.png')

# Adicione cidades
grafo_mapa_vis.adicionar_cidade('burarama', (250, 350))
grafo_mapa_vis.adicionar_cidade('pacotuba', (750, 1000))
grafo_mapa_vis.adicionar_cidade('conduru', (1000, 600))
grafo_mapa_vis.adicionar_cidade('saovicente', (1800, 500))
grafo_mapa_vis.adicionar_cidade('itaoca', (1600, 750))
grafo_mapa_vis.adicionar_cidade('coutinho', (1200, 950))
grafo_mapa_vis.adicionar_cidade('cachoeiro', (1400, 1400))
grafo_mapa_vis.adicionar_cidade('gironda', (1750, 1100))
grafo_mapa_vis.adicionar_cidade('soturno', (2100, 1000))
grafo_mapa_vis.adicionar_cidade('cmonos', (1150, 1640))
grafo_mapa_vis.adicionar_cidade('gruta', (2200, 1500))

# Carregue as conexões do arquivo
grafo_mapa_vis.carregar_conexoes_do_arquivo('conexoes.txt')

# Visualize o grafo no mapa
grafo_mapa_vis.visualizar_grafo_no_mapa()
