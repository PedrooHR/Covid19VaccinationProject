"""
Project: Final Project - Covid19 Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 23/11/2022
Version: 1.0.0
Function: Generate communities
"""

# ###########################################
# Importing Libraries
# ###########################################
import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm


# ###########################################
# Library Methods
# ###########################################


# def drawGraph(graph, output):
#     try:
#         # drawing graph
#         pos = nx.spring_layout(graph)  # positions for all nodes
#         # pos = nx.spring_layout(graph, seed=3113794652)  # positions for all nodes
#         # pos = nx.random_layout(graph)  # positions for all nodes
#         # pos = nx.circular_layout(graph)  # positions for all nodes
#         # pos = nx.spectral_layout(graph)  # positions for all nodes
#
#         # setting nodes
#         nx.draw_networkx_nodes(graph, pos, node_size=50, node_color="tab:red")
#         nx.draw_networkx_labels(graph, pos, font_size=8, font_family="sans-serif")
#
#         # setting edges
#         # edges = [(u, v) for (u, v, d) in G.edges(data=True)]
#         # nx.draw_networkx_edges(graph, pos, edgelist=edges, width=2, alpha=0.5, edge_color="tab:blue")
#         # edge_values = nx.get_edge_attributes(graph, "weight")
#         # nx.draw_networkx_edge_labels(graph, pos)
#         nx.draw_networkx_edges(graph, pos, width=2, alpha=0.5, edge_color="tab:gray")
#
#         # Set margins for the axes so that nodes aren't clipped
#         ax = plt.gca()
#         ax.margins(0.20)
#         plt.tight_layout()
#         plt.axis("off")
#         plt.savefig(output + '.png')
#         plt.show()
#
#     except:
#         pass


def generateCommunities(data_series):
    for input_serie in data_series:
        # To work better
        input_files_path = input_serie['input_files_path']
        input_file_prefix = input_serie['input_file_prefix']
        input_files = input_serie['input_files']
        output_path = input_serie['output_path']
        targets = input_serie['targets']
        prefixes = input_serie['prefixes']
        output_file = input_serie['output_file']
        name = input_serie['name']
        ratio_threshold = input_serie['ratio_threshold']

        print()
        print(f"1) Processing data for {name}")

        # if not os.path.exists(output_path):
        #     os.mkdir(output_path)

        # processing input files to build graphs
        for input_file in input_files:

            print()
            print(f"---------------------------------------------------------")
            print()

            # setting the full name of input file
            input_filename = input_files_path + input_file_prefix + input_file + '.gexf'

            # reading the raw data of vaccination proximity ratio
            print()
            # print(f"2) Reading data from {input_filename}")
            graph = nx.read_gexf(input_filename)

            # finding communities
            print(f"Communities of {input_file}")
            communities = greedy_modularity_communities(graph)
            print(f"Number of Communities: {len(communities)}")

            modularity = nx_comm.modularity(graph, communities)
            print(f"Modularity of network: {modularity}")

            i = 0
            for community in communities:
                modularity = nx_comm.modularity(graph, communities)
                i = i + 1
                print(f"Communnity {i} - # nodes: {len(community)}")


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
    gexf_path = graphs_path + 'graphs_vacc_proxy_ratio_ratio/'

    # Series that describe files to read
    data_series = []

    # ratio threshold used in all base graphs
    ratio_threshold = 0.05

    # Vaccination_Cases data
    data_series.append({
        'input_files_path': gexf_path,
        'input_file_prefix': "brazil_",
        'input_files': ['2022_2'],
        # 'input_files': ['2021_0', '2021_1', '2021_2', '2021_3', '2022_0', '2022_1', '2022_2', '2022_3'],
        'prefixes': ['vacc_proxy_ratio'],
        'targets': ['brazil'],
        'output_path': graphs_path + "graphs_vacc_proxy_ratio/",
        'output_file': 'brazil',
        'name': "Vaccination-Proximity Ratio Graphs",
        'ratio_threshold': ratio_threshold,
    })

    # print("\n----------------------------------------------")

    # This processes all the input files described before
    generateCommunities(data_series)

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
