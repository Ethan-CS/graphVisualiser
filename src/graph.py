import glob
import json
import os.path

import matplotlib.pyplot as plt
import networkx
import networkx as nx
import numpy as np


def draw_graph_from_file(filepath):
    plt.figure(figsize=(14, 10))
    plt.rcParams['figure.dpi'] = 300
    # Convert CSV into numpy matrix
    data = np.genfromtxt(filepath, delimiter=',', dtype=int)
    graph = nx.from_numpy_matrix(data)

    # Ensure layouts are displayed using a force-directed (Kamada-Kawai) layout
    pos = nx.kamada_kawai_layout(graph, scale=1, dim=2)
    nx.draw(graph, pos, node_color='#007a5a', node_size=300, font_size=10, with_labels=True)

    # Save to a .jpg file in the output file
    filename = os.path.splitext(filepath)[0]
    plt.savefig(f"{filename}.jpg", format="JPEG", dpi=300)
    plt.show()


def draw_graph(graph, name, filepath):
    plt.figure(figsize=(14, 10))
    plt.rcParams['figure.dpi'] = 300
    # Ensure layouts are displayed using a force-directed (Kamada-Kawai) layout
    pos = nx.spring_layout(graph, scale=1, dim=2)
    nx.draw(graph, pos, width=6, edge_color='#1f4d3c', node_color='#2bd999', node_size=2000, font_size=25,
            font_weight='bold', with_labels=False)
    # Save to a .jpg file in the output file
    plt.savefig(f"{filepath}/{name}.jpg", format="JPEG", dpi=300)
    plt.show()


def get_files(source_dir):
    # Add the name of each graph CSV file to the list of files and return the list
    files = []
    for f in glob.iglob(f"{source_dir}/*.csv", recursive=True):
        files.append(f)
        print(f)
    return files


# for file in get_files('graphs'):
#    draw_graph_from_file(file)
draw_graph(nx.random_tree(5), 'tree', 'graphs')
