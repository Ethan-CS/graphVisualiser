import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def create_graph(data, strategy_name):
    """
    Reads in total number of wins of models from a data csv file
    and creates a scatter plot of the strategy results for the
    given protection allocation strategy.
    """
    data = pd.read_csv(data)
    print(data)  # Print the data to verify

    # Scatter plot using seaborn to colour data points by strategy
    sns.scatterplot(x=data['P VALUE'], y=data['NUMBER OF WINS'], hue=data['DEFENCE STRATEGY'], palette="muted")

    # Setting the chart title and axis labels
    font = {'fontname': 'Helvetica Neue'}
    plt.title(f'Winners for each defence strategy with {strategy_name} protection allocation', **font)
    plt.xlabel('Graph density', **font)
    plt.ylabel('Number of wins', **font)
    plt.savefig(f"charts/{strategy_name}.jpg", format="JPEG")
    plt.show()


def get_win_charts(path, strategies, graph_types):
    """
    Given a root filepath, a list of strategies and a list of graph types,
    Creates a graph for each of the winning strategy files and returns the file paths.

    :param path: the root directory in which the winning data files can be found.
    :param strategies: a list of all strategies used in the models.
    :param graph_types: a list of all graph types that we have results to output for.
    """
    win_results = []
    for graph in graph_types:
        for strategy in strategies:
            win_result = f"{path}/{graph}/{strategy}Winner.csv"
            if os.path.exists(win_result):
                win_results.append(win_result)
                create_graph(win_result, strategy)


def main():
    path = "/Users/ethankelly/Documents/Agency/data"
    strategies = ["Deterministic", "Mixed", "Random"]
    graph_types = ["Erdős–Rényi"]

    get_win_charts(path, strategies, graph_types)


if __name__ == "__main__":
    main()
