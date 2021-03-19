import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os.path


def show_graph(filepath):
    data = np.genfromtxt(filepath, delimiter=',', dtype=int)
    graph = nx.from_numpy_matrix(data)
    pos = nx.kamada_kawai_layout(graph, scale=1, dim=2)
    nx.draw(graph, pos, node_color='#007a5a', node_size=300, font_size=10, with_labels=True)
    filename = os.path.splitext(filepath)[0]
    plt.savefig(f"{filename}.jpg", format="JPEG")
    plt.show()


files = ["tree.csv", "4regular.csv", "erdosRenyi.csv", "complete.csv"]

for file in files:
    show_graph(file)
