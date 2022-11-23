"""
Project: Final Project - Covid19 Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 19/11/2022
Version: 1.0.0
Function: Generate base graph
"""

# ###########################################
# Importing Libraries
# ###########################################
import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# ###########################################
# Library Methods
# ###########################################


def drawGraph(graph, output):
    try:
        # drawing graph
        pos = nx.spring_layout(graph)  # positions for all nodes
        # pos = nx.spring_layout(graph, seed=3113794652)  # positions for all nodes
        # pos = nx.random_layout(graph)  # positions for all nodes
        # pos = nx.circular_layout(graph)  # positions for all nodes
        # pos = nx.spectral_layout(graph)  # positions for all nodes

        # setting nodes
        nx.draw_networkx_nodes(graph, pos, node_size=50, node_color="tab:red")
        nx.draw_networkx_labels(graph, pos, font_size=8, font_family="sans-serif")

        # setting edges
        # edges = [(u, v) for (u, v, d) in G.edges(data=True)]
        # nx.draw_networkx_edges(graph, pos, edgelist=edges, width=2, alpha=0.5, edge_color="tab:blue")
        # edge_values = nx.get_edge_attributes(graph, "weight")
        # nx.draw_networkx_edge_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos, width=2, alpha=0.5, edge_color="tab:gray")

        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.tight_layout()
        plt.axis("off")
        plt.savefig(output + '.png')
        plt.show()

    except:
        pass


def generateGraphs(data_series):
    for input_serie in data_series:
        # To work better
        input_files_path = input_serie['input_files_path']
        input_file_prefix = input_serie['input_file_prefix']
        input_files = input_serie['input_files']
        parameters = input_serie['parameters']
        brazilian_states = parameters[0]
        np_cities = parameters[1]
        output_path = input_serie['output_path']
        targets = input_serie['targets']
        prefixes = input_serie['prefixes']
        output_file = input_serie['output_file']
        name = input_serie['name']
        ratio_threshold = input_serie['ratio_threshold']

        print()
        print(f"1) Processing data for {name}")

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # processing input files to build graphs
        for input_file in input_files:
            # setting the full name of input file
            input_filename = input_files_path + input_file_prefix + input_file + '.csv'

            # reading the raw data of vaccination proximity ratio
            print()
            print(f"2) Reading data from {input_filename}")
            raw_data = pd.read_csv(input_filename, sep=',', header=None)
            np_raw_data = raw_data.to_numpy()

            # evaluate_values(np_raw_data)

            print()
            print(f"3) Building graphs")

            for id in range(len(targets)):
                target = targets[id]
                output_file_name = output_file + '_' + input_file

                # possible targets:
                # 1) brazil
                # 2) list of regions of brazil: north, northeast, midwest, south, southeast
                # 3) list of some states related by initials

                if target == 'brazil':

                    # selecting nodes and edges
                    nodes = []
                    edges = []
                    for i in range(1, len(np_raw_data)):
                        print(f'origin index {i}')
                        for j in range(i + 1, len(np_raw_data)):
                            # applying threshold value
                            if 0 < np_raw_data[i][j] <= ratio_threshold:
                                # origin_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[i][0]]['city'].array[0]
                                # target_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[0][j]]['city'].array[0]
                                # compact_origin_city = origin_city[:5] + origin_city[-3:]
                                # compact_target_city = target_city[:5] + target_city[-3:]
                                # edges.append((compact_origin_city, compact_target_city, np_raw_data[i][j]))
                                edges.append((np_raw_data[i][0], np_raw_data[0][j], np_raw_data[i][j]))

                # getting the city name
                # origin_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[i][0]]['city'].array[0]
                # target_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[0][j]]['city'].array[0]
                # compact_origin_city = origin_city[:5] + origin_city[-3:]
                # compact_target_city = target_city[:5] + target_city[-3:]
                # edges.append((compact_origin_city, compact_target_city, np_raw_data[i][j]))

                # building list of nodes fom edges
                np_edges = np.array(edges)
                nodes = np.unique(np.concatenate((np.unique(np_edges[:, 0]), np.unique(np_edges[:, 1])))).tolist()

                # creating graph
                graph = nx.Graph()

                # adding nodes
                graph.add_nodes_from(nodes)

                # adding edges
                for edge in edges:
                    graph.add_edge(edge[0], edge[1])

                print()
                print(f"4) Showing graph")

                # saving graph in gexf format
                # print(output_path + output_file + '.gexf')
                nx.write_gexf(graph, output_path + output_file_name + '.gexf')

                # showing graph
                # drawGraph(graph, output_path + output_file_name)


def evaluate_values(np_raw_data):
    min_value = 999999999
    max_value = 0
    for i in range(2, len(np_raw_data)):
        for j in range(i + 1, len(np_raw_data)):
            if 0 < np_raw_data[i][j] < min_value:
                min_value = np_raw_data[i][j]
            if np_raw_data[i][j] > max_value:
                max_value = np_raw_data[i][j]

    print(f"Min value: {min_value}")
    print(f"Max value: {max_value}")


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/../"
    data_path = root_path + 'data/'

    inputs_path = data_path + 'input/'
    outputs_path = data_path + 'output/'
    calculations_path = data_path + 'calculations/'
    graphs_path = data_path + 'graphs/'

    # getting states of Brazil
    brazilian_states = pd.read_excel(inputs_path + 'states_of_brazil.xlsx')

    # getting all cities
    cities = pd.read_excel(outputs_path + 'city.xlsx')

    # Series that describe files to read
    data_series = []

    # ratio threshold used in all base graphs
    ratio_threshold = 0.05

    # Vaccination_Cases data
    data_series.append({
        'input_files_path': calculations_path,
        'input_file_prefix': "vaccination_ratio_",
        'input_files': ['2021_0', '2021_1', '2021_2', '2021_3', '2022_0', '2022_1', '2022_2', '2022_3'],
        'parameters': [brazilian_states, cities],
        'prefixes': ['vacc_proxy_ratio'],
        'targets': ['brazil'],
        'output_path': graphs_path + "graphs_vacc_proxy_ratio/",
        'output_file': 'brazil',
        'name': "Vaccination-Proximity Ratio Graphs",
        'ratio_threshold': ratio_threshold,
    })

    # print("\n----------------------------------------------")

    # This processes all the input files described before
    generateGraphs(data_series)

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
