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
graph_types = ["Simple"]
ranges = ["25-250"]
font = {'family': 'serif',
        'color': 'black',
        'weight': 'normal',
        'size': 16,
        }
num_v = 50
data_filter = 'NUMBER OF EDGES'
x_lab = 'Number of Edges'


def get_win_charts():
    """
    Given a root filepath, a list of strategies and a list of graph types,
    Creates a graph for each of the winning strategy files and returns the file paths.
    """
    for graph in graph_types:
        for allocation in protection_allocation:
            for each_range in ranges:
                win_result = f"{data_path}/{graph} {each_range}/{allocation}Winner.csv"
                if os.path.exists(win_result):
                    create_win_plot(win_result, allocation, each_range, out_path + "winners", filter_by=data_filter)
                    print(win_result)


def create_win_plot(data_file, allocation, p_range, output_path, filter_by):
    """
    Reads in total number of wins of models from a data csv file
    and creates a scatter plot of the strategy results for the
    given protection allocation strategy.
    """
    data = pd.read_csv(data_file)
    print(data)

    # Scatter plot using seaborn to colour data points by strategy
    plt.figure(figsize=(10, 8))
    sns.set(rc={"figure.dpi": 300, 'savefig.dpi': 300})
    sns.set_context('notebook')
    sns.set_style("ticks")
    sns.scatterplot(
        x=data[filter_by], y=data['NUMBER OF WINS'], hue=data['DEFENCE STRATEGY'], palette="bright", s=60, alpha=0.8)
    leg = plt.legend(title="Defence Strategies")
    for i in range(len(defence_strategies)):
        leg.get_texts()[i].set_text(defence_strategies[i])

    plt.title(f'Winners for each defence strategy\n({allocation} protection allocation)', **font)
    plt.xlabel(x_lab, **font)
    plt.ylabel('Number of wins', **font)
    plt.savefig(f"{output_path}/{p_range}/{allocation}.jpg", format="JPEG")
    plt.show()


def get_infected_plots():
    # all_paths is a list of all directories in the specified path directory
    for graph in graph_types:
        for p_range in ranges:
            all_paths = [f.path for f in os.scandir(data_path + "/" + graph + " " + p_range) if f.is_dir()]
            all_paths.sort(key=natural_keys)
            for path in all_paths:
                print(path)

            ds_by_strategy = [[], [], []]
            for each_path in all_paths:
                for i in range(len(protection_allocation)):
                    ds_by_strategy[i].append(
                        combine_data(each_path, protection_allocation[i], extra_val=each_path.split('/')[-1]))

            for allocation in protection_allocation:
                data = pd.concat(ds_by_strategy[protection_allocation.index(allocation)])
                create_percent_infected_plot(data, allocation,
                                             num_vertices=num_v, value_range=p_range, filter_by=data_filter)


def create_percent_infected_plot(data, allocation, num_vertices, value_range, filter_by):
    # Scatter plot using seaborn to colour data points by strategy
    plt.figure(figsize=(10, 8))
    sns.set(rc={"figure.dpi": 300, 'savefig.dpi': 300})
    sns.set_context('notebook')
    sns.set_style("ticks")
    sns.scatterplot(
        x=data[filter_by], y=(data['INFECTED'] / num_vertices), hue=data['STRATEGY'], palette="bright", s=60, alpha=0.8)
    leg = plt.legend(title="Defence Strategies")
    for i in range(len(defence_strategies)):
        leg.get_texts()[i].set_text(defence_strategies[i])

    plt.title(f'Percentage infections by defence\n({allocation} protection allocation)', **font)
    plt.xlabel(x_lab, **font)
    plt.ylabel('Percent of graph infected', **font)
    plt.savefig(f"{out_path}/percent_infected/{value_range}/{allocation}.jpg", format="JPEG")
    plt.show()


def combine_data(this_path, strategy, extra_val):
    strategy_directory = f"{this_path}/{strategy}/"
    data_files = glob.glob(strategy_directory + f"/{strategy}Data*.csv")
    all_dataframes = []
    for data_file in data_files:
        data = pd.read_csv(data_file)
        data.insert(0, 'NUMBER OF EDGES', extra_val)
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
