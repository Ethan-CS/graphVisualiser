import glob
import os
import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_path = "/Users/ethankelly/Documents/Agency/data"
out_path = "charts/"
protection_allocation = ["Deterministic", "Mixed", "Random"]
defence_strategies = ["Proximity", "Degree", "Protection"]
graph_types = ["Erdős–Rényi"]
p_ranges = ["0.01-0.20", "0.05-1.00"]
font = {'family': 'serif',
        'color': 'black',
        'weight': 'normal',
        'size': 16,
        }
num_v = 50


def get_win_charts():
    """
    Given a root filepath, a list of strategies and a list of graph types,
    Creates a graph for each of the winning strategy files and returns the file paths.

    :param output_path: the location to save the generated graphs to.
    """
    for graph in graph_types:
        for allocation in protection_allocation:
            for p_range in p_ranges:
                win_result = f"{data_path}/{graph} {p_range}/{allocation}Winner.csv"
                if os.path.exists(win_result):
                    create_win_plot(win_result, allocation, p_range, out_path + "winners")
                    print(win_result)


def create_win_plot(data_file, allocation, p_range, output_path):
    """
    Reads in total number of wins of models from a data csv file
    and creates a scatter plot of the strategy results for the
    given protection allocation strategy.
    """
    data = pd.read_csv(data_file)
    print(data)

    # Scatter plot using seaborn to colour data points by strategy
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x=data['P VALUE'], y=data['NUMBER OF WINS'], hue=data['DEFENCE STRATEGY'], palette="bright", s=60, alpha=0.3)
    leg = plt.legend(title="Defence Strategies")
    for i in range(len(defence_strategies)):
        leg.get_texts()[i].set_text(defence_strategies[i])

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.title(f'Winners for each defence strategy\n({allocation} protection allocation)', **font)
    plt.xlabel('Graph density', **font)
    plt.ylabel('Number of wins', **font)
    plt.savefig(f"{output_path}/{p_range}/{allocation}.jpg", format="JPEG")
    plt.show()


def get_infected_plots():
    # all_paths is a list of all directories in the specified path directory
    for graph in graph_types:
        for p_range in p_ranges:
            all_paths = [f.path for f in os.scandir(data_path + "/" + graph + " " + p_range) if f.is_dir()]
            all_paths.sort(key=natural_keys)

            ds_by_strategy = [[], [], []]
            for each_path in all_paths:
                for i in range(len(protection_allocation)):
                    ds_by_strategy[i].append(
                        combine_data(each_path, protection_allocation[i], p=each_path.split('/')[-1]))

            for allocation in protection_allocation:
                data = pd.concat(ds_by_strategy[protection_allocation.index(allocation)])
                create_percent_infected_plot(data, allocation,
                                             num_vertices=num_v, p_range=p_range)


def create_percent_infected_plot(data, allocation, num_vertices, p_range):
    # Scatter plot using seaborn to colour data points by strategy
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x=data['P VALUE'], y=(data['INFECTED'] / num_vertices), hue=data['STRATEGY'], palette="bright", s=60, alpha=0.7)
    leg = plt.legend(title="Defence Strategies")
    for i in range(len(defence_strategies)):
        leg.get_texts()[i].set_text(defence_strategies[i])

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.title(f'Percentage infections by defence\n({allocation} protection allocation)', **font)
    plt.xlabel('Graph density', **font)
    plt.ylabel('Percent of graph infected', **font)
    plt.savefig(f"{out_path}/percent_infected/{p_range}/{allocation}.jpg", format="JPEG")
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


# Used to sort file names by the number at the end
# Of the string, also known as "human sorting"
def natural_keys(text):
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]


def main():
    get_win_charts()
    get_infected_plots()


if __name__ == "__main__":
    main()
