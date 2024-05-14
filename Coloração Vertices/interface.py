import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class GrafoColoracao:
    def __init__(self):
        self.grafo = {}
        self.cores = {}

    def ler_grafo(self, arquivo):
        with open(arquivo, 'r') as f:
            for linha in f:
                vertices = linha.strip().split(',')
                vertice = vertices[0].strip()
                vizinhos = [vizinho.strip() for vizinho in vertices[1:]]
                self.grafo[vertice] = vizinhos
                self.cores[vertice] = None

    def colorir_grafo(self):
        for vertice in self.grafo:
            cores_vizinhos = {self.cores[vizinho] for vizinho in self.grafo[vertice] if self.cores[vizinho] is not None}
            cor_disponivel = 1
            while cor_disponivel in cores_vizinhos:
                cor_disponivel += 1
            self.cores[vertice] = cor_disponivel

    def plotar_grafo(self, container):
        G = nx.Graph()
        for vertice, vizinhos in self.grafo.items():
            G.add_node(vertice)
            for vizinho in vizinhos:
                G.add_edge(vertice, vizinho)

        cores = [self.cores[vertice] for vertice in G.nodes()]
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=cores, cmap=plt.cm.rainbow, font_color='white', font_weight='bold')
        
        canvas = FigureCanvasTkAgg(plt.gcf(), master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def criar_tabela(self, container):
        tabela = ttk.Treeview(container)
        tabela["columns"] = ("Vertice", "Cor", "Vizinhos")
        tabela.column("#0", width=0, stretch=tk.NO)
        tabela.column("Vertice", anchor=tk.W, width=50)
        tabela.column("Cor", anchor=tk.W, width=50)
        tabela.column("Vizinhos", anchor=tk.W, width=150)

        tabela.heading("#0", text="", anchor=tk.W)
        tabela.heading("Vertice", text="Vertice", anchor=tk.W)
        tabela.heading("Cor", text="Cor", anchor=tk.W)
        tabela.heading("Vizinhos", text="Vizinhos", anchor=tk.W)

        for vertice, cor in self.cores.items():
            vizinhos_str = ", ".join(self.grafo[vertice])
            tabela.insert("", "end", values=(vertice, cor, vizinhos_str))

        tabela.pack()

def main():
    root = tk.Tk()
    root.withdraw()

    arquivo_path = filedialog.askopenfilename(title="Escolha o arquivo do grafo")

    if not arquivo_path:
        print("Nenhum arquivo selecionado. Encerrando o programa.")
        return

    grafo_coloracao = GrafoColoracao()
    grafo_coloracao.ler_grafo(arquivo_path)
    grafo_coloracao.colorir_grafo()

    print("Resultado da coloração:")
    for vertice, cor in grafo_coloracao.cores.items():
        print(f"Vértice {vertice}: Cor {cor}")

    # Criar a interface gráfica principal
    main_window = tk.Toplevel(root)
    main_window.title("Visualização do Grafo e Tabela")

    # Criar um frame para o gráfico
    frame_grafico = tk.Frame(main_window)
    frame_grafico.pack(side=tk.LEFT, padx=10, pady=10)
    grafo_coloracao.plotar_grafo(frame_grafico)

    # Criar um frame para a tabela
    frame_tabela = tk.Frame(main_window)
    frame_tabela.pack(side=tk.RIGHT, padx=10, pady=10)
    grafo_coloracao.criar_tabela(frame_tabela)

    root.mainloop()

if __name__ == "__main__":
    main()
