import glob
import os
import re
import csv

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_filepath = "/Users/ethankelly/Documents/Agency/data"
graph_filepath = f'{data_filepath}/Erdos Renyi 0.05-0.95/0.05/Graph0.csv'
out = "charts"
protection_allocation = ["Deterministic", "Mixed", "Random"]
defence_strategies = ["Proximity", "Degree", "Protection"]
graph_types = ["Erdos Renyi"]
ranges = ["0.05-0.95"]
font = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 20}
num_v = len(next(csv.reader(open(graph_filepath, 'r'))))
filter_by = 'P VALUE'
x_lab = filter_by.title()


def get_degree_distributions(graphs, data_path):
    plt.figure(figsize=(14, 10))
    sns.set(rc={"figure.dpi": 300, 'savefig.dpi': 300})
    sns.set_context('notebook')
    sns.set_style("ticks")
    plt.xlabel(filter_by.title(), **font)
    my_dict = dict()
    for g in graphs:
        for r in ranges:
            paths = glob.glob(f"{data_path}/{g} {r}/*/")
            paths.sort(key=natural_keys)
            probabilities = list()
            for path in paths:
                prob = float(path.split('/')[-2])
                probabilities.append(prob)
                my_dict[prob] = list()
                with open(f"{path}Degrees.csv", 'r') as csv_file:
                    import csv
                    degrees = csv.reader(csv_file, delimiter=',')
                    for row in degrees:
                        for entry in row:
                            my_dict[prob].append(int(entry))
            data = [*zip(*my_dict.items())][1]  # 'transpose' items to parallel key, value lists
            sns.boxplot(data=data, hue_order=probabilities)
            plt.xticks(range(len(probabilities)), probabilities)

            plt.title("Degree distributions", **font)
            plt.ylabel("Degree distribution", **font)
            where_to_save = f"{out}/degrees/{r}"
            if not os.path.exists(where_to_save):
                os.makedirs(where_to_save)

            plt.savefig(where_to_save + "/Degrees.jpg", format="JPEG")
            plt.show()


def get_win_charts(graphs, data_path):
    """
    Given a root filepath, a list of strategies and a list of graph types,
    Creates a graph for each of the winning strategy files and returns the file paths.
    """
    for graph in graphs:
        for allocation in protection_allocation:
            for each_range in ranges:
                win_result = f"{data_path}/{graph} {each_range}/{allocation}Winner.csv"
                if os.path.exists(win_result):
                    data = pd.read_csv(win_result)
                    create_plot(type_of_plot='win', data=data, allocation=allocation, value_range=each_range,
                                filter_by_key=filter_by)


def create_plot(type_of_plot, data, allocation, value_range, filter_by_key):
    """
    Reads in total number of wins of models from a data csv file
    and creates a scatter plot of the strategy results for the
    given protection allocation strategy.
    """
    # Scatter plot using seaborn to colour data points by strategy
    plt.figure(figsize=(14, 10))
    sns.set(rc={"figure.dpi": 300, 'savefig.dpi': 300})
    sns.set_context('notebook')
    sns.set_style("ticks")
    where_to_save = f"{out}/"
    plt.xlabel(filter_by_key.title(), **font)

    if type_of_plot == 'win':
        where_to_save += f"winners/{value_range}"
        sns.lineplot(x=data[filter_by_key], y=data['NUMBER OF WINS'], hue=data['DEFENCE STRATEGY'],
                     palette="bright", linewidth=5, alpha=0.8)
        plt.title(f'Winners for each defence strategy\n({allocation} protection allocation)', **font)
        plt.xlabel(filter_by_key.title(), **font)
        plt.ylabel('Number of wins', **font)
        leg = plt.legend(title="Defence Strategies")
        for i in range(len(defence_strategies)):
            leg.get_texts()[i].set_text(defence_strategies[i])
    elif type_of_plot == 'percent':
        where_to_save += f"percent_infected/{value_range}"
        sns.boxplot(x=data[filter_by_key], y=(data['INFECTED'] / num_v), hue=data['STRATEGY'], palette="bright")
        plt.title(f'Percentage infections by defence\n({allocation} protection allocation)', **font)
        plt.xlabel(filter_by_key.title(), **font)
        plt.ylabel('Percent of graph infected', **font)
        leg = plt.legend(title="Defence Strategies")
        for i in range(len(defence_strategies)):
            leg.get_texts()[i].set_text(defence_strategies[i])

    if not os.path.exists(where_to_save):
        os.makedirs(where_to_save)
    plt.savefig(where_to_save + f"/{allocation}.jpg", format="JPEG")
    plt.show()


def get_infected_plots(data_path):
    # all_paths is a list of all directories in the specified path directory
    for graph in graph_types:
        for p_range in ranges:
            all_paths = [f.path for f in os.scandir(data_path + "/" + graph + " " + p_range) if f.is_dir()]
            all_paths.sort(key=natural_keys)
            ds_by_strategy = [[], [], []]
            for path in all_paths:
                for i in range(len(protection_allocation)):
                    ds_by_strategy[i].append(
                        combine_data(this_path=path, strategy=protection_allocation[i], extra_val=path.split('/')[-1],
                                     data_filter=filter_by))

            for allocation in protection_allocation:
                data = pd.concat(ds_by_strategy[protection_allocation.index(allocation)])
                create_plot(type_of_plot='percent', data=data, allocation=allocation,
                            value_range=p_range, filter_by_key=filter_by)


def combine_data(this_path, strategy, extra_val, data_filter):
    strategy_directory = f"{this_path}/{strategy}/"
    data_files = glob.glob(strategy_directory + f"/{strategy}Data*.csv")
    all_dataframes = []
    for data_file in data_files:
        data = pd.read_csv(data_file)
        data.insert(0, data_filter, extra_val)
        all_dataframes.append(data)
    return pd.concat(all_dataframes)


def atof(text):
    try:
        ret_val = float(text)
    except ValueError:
        ret_val = text
    return ret_val


# Used to sort file names by the number at the end
# Of the string, also known as "human sorting"
def natural_keys(text):
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]


def main():
    get_degree_distributions(graph_types, data_filepath)
    get_win_charts(graph_types, data_filepath)
    get_infected_plots(data_filepath)


if __name__ == "__main__":
    main()
