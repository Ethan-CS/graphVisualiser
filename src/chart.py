import glob
import os
import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

path = "/Users/ethankelly/Documents/Agency/data"
strategies = ["Deterministic", "Mixed", "Random"]
graph_types = ["Erdős–Rényi"]


def create_win_plot(data_file, strategy_name):
    """
    Reads in total number of wins of models from a data csv file
    and creates a scatter plot of the strategy results for the
    given protection allocation strategy.
    """
    data = pd.read_csv(data_file)

    # Scatter plot using seaborn to colour data points by strategy
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=data['P VALUE'], y=data['NUMBER OF WINS'], hue=data['DEFENCE STRATEGY'], palette="bright")

    # Setting the chart title and axis labels
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }
    plt.title(f'Winners for each defence strategy with {strategy_name} protection allocation', **font)
    plt.xlabel('Graph density', **font)
    plt.ylabel('Number of wins', **font)
    plt.savefig(f"charts/{strategy_name}.jpg", format="JPEG")
    plt.show()


def get_win_charts(path_to_win_files, all_strategies, all_graph_types):
    """
    Given a root filepath, a list of strategies and a list of graph types,
    Creates a graph for each of the winning strategy files and returns the file paths.

    :param path_to_win_files: the root directory in which the winning data files can be found.
    :param all_strategies: a list of all strategies used in the models.
    :param all_graph_types: a list of all graph types that we have results to output for.
    """
    win_results = []
    for graph in all_graph_types:
        for strategy in all_strategies:
            win_result = f"{path_to_win_files}/{graph}/{strategy}Winner.csv"
            if os.path.exists(win_result):
                win_results.append(win_result)
                create_win_plot(win_result, strategy)


def create_percent_infected_plot(data, allocation, num_vertices):
    # Scatter plot using seaborn to colour data points by strategy
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x=data['P VALUE'], y=(data['INFECTED'] / num_vertices), hue=data['STRATEGY'], palette="bright", s=60)
    leg = plt.legend(title="Defence Strategies")
    for i in range(len(strategies)):
        leg.get_texts()[i].set_text(strategies[i])

    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }
    plt.title(f'Percentage infections by defence \n({allocation} protection allocation)', **font)
    plt.xlabel('Graph density', **font)
    plt.ylabel('Percent of graph infected', **font)
    plt.savefig(f"charts/{allocation}.jpg", format="JPEG")
    plt.show()


def combine_data(this_path, strategy, p):
    strategy_directory = f"{this_path}/{strategy}/"
    data_files = glob.glob(strategy_directory + f"/{strategy}Data*.csv")
    all_dataframes = []
    for data_file in data_files:
        data = pd.read_csv(data_file)
        data.insert(0, "P VALUE", p)
        all_dataframes.append(data)
    return pd.concat(all_dataframes)


def atof(text):
    try:
        ret_val = float(text)
    except ValueError:
        ret_val = text
    return ret_val


def natural_keys(text):
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]


def main():
    get_win_charts(path, strategies, graph_types)

    # all_paths is a list of all directories in the specified path directory
    all_paths = [f.path for f in os.scandir(path + "/" + graph_types[0]) if f.is_dir()]
    all_paths.sort(key=natural_keys)
    ds_by_strategy = [[], [], []]
    for each_path in all_paths:
        for i in range(len(strategies)):
            ds_by_strategy[i].append(combine_data(each_path, strategies[i], p=each_path.split('/')[-1]))

    for strategy in strategies:
        create_percent_infected_plot(pd.concat(ds_by_strategy[strategies.index(strategy)]), strategy, num_vertices=50)


if __name__ == "__main__":
    main()
