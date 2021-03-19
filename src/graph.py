import glob
import os.path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def show_graph(filepath):
    # Convert CSV into numpy matrix
    data = np.genfromtxt(filepath, delimiter=',', dtype=int)
    graph = nx.from_numpy_matrix(data)

    # Ensure layouts are displayed using a force-directed (Kamada-Kawai) layout
    pos = nx.kamada_kawai_layout(graph, scale=1, dim=2)
    nx.draw(graph, pos, node_color='#007a5a', node_size=300, font_size=10, with_labels=True)

    # Save to a .jpg file in the output file
    filename = os.path.splitext(filepath)[0]
    plt.savefig(f"{filename}.jpg", format="JPEG")
    plt.show()


def get_files(source_dir):
    # Add the name of each graph CSV file to the list of files and return the list
    files = []
    for f in glob.iglob(f"{source_dir}/*.csv", recursive=True):
        files.append(f)
        print(f)
    return files


for file in get_files('graphs'):
    show_graph(file)
