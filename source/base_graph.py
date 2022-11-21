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
        pos = nx.spring_layout(graph, seed=3113794652)  # positions for all nodes

        # setting nodes
        nx.draw_networkx_nodes(graph, pos, node_size=50, node_color="tab:red")
        nx.draw_networkx_labels(graph, pos, font_size=8, font_family="sans-serif")

        # setting edges
        nx.draw_networkx_edges(graph, pos, width=2, alpha=0.5, edge_color="tab:blue")

        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.tight_layout()
        plt.axis("off")
        plt.savefig(output + '.png')
        plt.show()

    except:
        pass


# def drawGraph2(G, output):
#     try:
#         X, Y = bipartite.sets(G)
#         X = sorted(X)
#         Y = sorted(Y)
#         pos = dict()
#         pos.update((n, (1, i * 10)) for i, n in enumerate(X))  # put nodes from X at x=1
#         pos.update((n, (2, i * 10)) for i, n in enumerate(Y))  # put nodes from Y at x=2
#
#         edges = [(u, v) for (u, v, d) in G.edges(data=True)]
#
#         # Nodes
#         nx.draw_networkx_nodes(G, pos, node_size=2000)
#
#         # node labels
#         nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
#
#         # Edges
#         nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.5, edge_color="b")
#
#         # edge weight labels
#         edge_values = nx.get_edge_attributes(G, "weight")
#         nx.draw_networkx_edge_labels(G, pos, edge_values, 0.85)
#
#         ax = plt.gca()
#         ax.margins(0.08)
#         plt.axis("off")
#         plt.tight_layout()
#         plt.savefig(output + '.png')
#         plt.show()
#     except:
#         pass
#

def generateGraphs(data_series):
    for input_serie in data_series:
        # To work better
        input_file = input_serie['input_file']
        parameters = input_serie['parameters']
        brazilian_states = parameters[0]
        np_cities = parameters[1]
        output_path = input_serie['output_path']
        targets = input_serie['targets']
        prefixes = input_serie['prefixes']
        output_files = input_serie['output_files']
        name = input_serie['name']
        ratio_threshold = input_serie['ratio_threshold']

        print()
        print(f"1) Processing data for {name}")

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # reading the raw data of vaccination proximity ratio
        print()
        print(f"2) Reading data from {input_file}")
        raw_data = pd.read_csv(input_file, sep=',', header=None)
        np_raw_data = raw_data.to_numpy()

        for id in range(len(targets)):
            target = targets[id]
            output_file = output_files[id]

            # possible targets:
            # 1) brazil
            # 2) list of regions of brazil: north, northeast, midwest, south, southeast
            # 3) list of some states related by initials

            if target == 'brazil':

                # selecting nodes and edges
                nodes = []
                edges = []
                for i in range(1, len(np_raw_data)):
                    for j in range(i + 1, len(np_raw_data)):
                        # applying threshold value
                        if np_raw_data[i][j] > 0 and np_raw_data[i][j] <= ratio_threshold:
                            origin_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[i][0]]['city'].array[0]
                            target_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[0][j]]['city'].array[0]
                            compact_origin_city = origin_city[:5] + origin_city[-3:]
                            compact_target_city = target_city[:5] + target_city[-3:]
                            nodes.append(compact_origin_city)
                            nodes.append(compact_target_city)
                            edges.append((compact_origin_city, compact_target_city, np_raw_data[i][j]))

            # removing duplicates values
            nodes = np.unique(nodes)

            # creating graph
            graph = nx.Graph()

            # adding nodes
            graph.add_nodes_from(nodes)

            # adding edges
            for edge in edges:
                graph.add_edge(edge[0], edge[1])

            print()
            print(f"3) Showing graph")

            # saving graph in gexf format
            # print(output_path + output_file + '.gexf')
            nx.write_gexf(graph, output_path + output_file + '.gexf')

            # showing graph
            drawGraph(graph, output_path + output_file)


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

    # Vaccination_Cases data
    data_series.append({
        'input_file': calculations_path + "vaccination_ratio_proximity.csv",
        'parameters': [brazilian_states, cities],
        'prefixes': ['vacc_proxy_ratio'],
        'targets': ['brazil'],
        'output_path': graphs_path + "graphs_vacc_proxy_ratio/",
        'output_files': ['brazil'],
        'name': "Vaccination-Proximity Ratio Graphs",
        'ratio_threshold': 0.009,
    })

    # print("\n----------------------------------------------")

    # This processes all the input files described before
    generateGraphs(data_series)
