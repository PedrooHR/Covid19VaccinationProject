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
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
from datetime import datetime


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
        input_files_prefix = input_serie['input_files_prefix']
        input_prefix_vaccination_ratio = input_files_prefix[0]
        input_prefix_city_doses = input_files_prefix[1]
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
        generate_graph_gexf = input_serie['generate_graph_gexf']

        print()
        print(f"1) Processing data for {name}")
        printNow("Step 1")

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # processing input files to build graphs
        for input_file_year_month in input_files:
            # setting the full name of input file
            input_vaccination_ratio_csv = input_files_path + input_prefix_vaccination_ratio + input_file_year_month + '.csv'
            input_city_doses_csv = input_files_path + input_prefix_city_doses + input_file_year_month + '.csv'

            # reading the raw data of vaccination proximity ratio
            print()
            print(f"2) Reading data from vaccination ratio and cities - {input_file_year_month}")
            printNow("Step 2")

            raw_vaccination_ratio_data = pd.read_csv(input_vaccination_ratio_csv, sep=',', header=None)
            np_raw_data = raw_vaccination_ratio_data.to_numpy()
            raw_city_doses_data = pd.read_csv(input_city_doses_csv)
            community_cities = raw_city_doses_data[['ibgeID', 'dose_0', 'dose_1']]
            community_cities['dose'] = community_cities['dose_0'] + community_cities['dose_1']
            community_cities.index = community_cities['ibgeID'].tolist()

            print()
            print(f"3) Building graphs")
            printNow("Step 3")

            for id in range(len(targets)):
                target = targets[id]
                output_file_name = output_file + '_' + input_file_year_month

                # possible targets:
                # 1) brazil
                # 2) list of regions of brazil: north, northeast, midwest, south, southeast
                # 3) list of some states related by initials

                if target == 'brazil':
                    # selecting nodes and edges
                    nodes = []
                    edges = []
                    count = 0
                    for i in range(1, len(np_raw_data)):
                        # print(f'origin index {i}')
                        # print(f'{input_file_year_month} - origin city index {i}')

                        for j in range(i + 1, len(np_raw_data)):
                            # applying threshold value
                            if 0 < np_raw_data[i][j] <= ratio_threshold:
                                edges.append((np_raw_data[i][0], np_raw_data[0][j], np_raw_data[i][j]))

                    # getting the city name
                    # origin_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[i][0]]['city'].array[0]
                    # target_city = np_cities.loc[np_cities['ibgeID'] == np_raw_data[0][j]]['city'].array[0]
                    # compact_origin_city = origin_city[:5] + origin_city[-3:]
                    # compact_target_city = target_city[:5] + target_city[-3:]
                    # edges.append((compact_origin_city, compact_target_city, np_raw_data[i][j]))

                    # building list of nodes of the network
                    # np_edges = np.array(edges)
                    # nodes = np.unique(np.concatenate((np.unique(np_edges[:, 0]), np.unique(np_edges[:, 1])))).tolist()
                    nodes = np_raw_data[1:, 0].tolist()

                    # creating graph
                    graph = nx.Graph()

                    # adding nodes
                    graph.add_nodes_from(nodes)

                    # adding edges
                    for edge in edges:
                        graph.add_edge(edge[0], edge[1])

                    print()
                    print(f"4) Creating communities of the graph")
                    printNow("Step 4")

                    # generating communities
                    communities_graph, communities, community_cities_result = generateCommunities( \
                        input_file_year_month, graph, community_cities, output_path)

                    printNow("Step 5")

                    # saving results
                    output_file_community_cities_result_xlsx = \
                        output_path + "community_cities_result_" + input_file_year_month + ".xlsx"
                    if os.path.exists(output_file_community_cities_result_xlsx):
                        os.remove(output_file_community_cities_result_xlsx)
                    community_cities_result.to_excel(output_file_community_cities_result_xlsx, index=False)

                    # saving graph in gexf format
                    if generate_graph_gexf:
                        print(output_path + output_file_name + '.gexf')
                        nx.write_gexf(communities_graph, output_path + output_file_name + '.gexf')

                    # showing graph
                    # drawGraph(graph, output_path + output_file_name)


def generateCommunities(input_file_year_month, graph, community_cities, output_path):
    # finding communities
    print(f"Finding Communities of {input_file_year_month} ")
    printNow("Step 4.1")
    communities = greedy_modularity_communities(graph)
    print(f"Number of Communities: {len(communities)}")
    printNow("Step 4.2")

    modularity = nx_comm.modularity(graph, communities)
    print(f"Modularity of network: {modularity}")
    printNow("Step 4.3")

    # initializing object
    community_cities_classified = pd.DataFrame()

    community_id = 0
    for community_item in communities:
        community_id = community_id + 1
        print(f"Communnity {community_id} - # nodes: {len(community_item)}")
        print(community_item)
        printNow("Step 4.4")

        # processing community
        community_item_cities_aux = [int(item) for item in community_item]
        community_item_cities_processed = community_cities.loc[community_item_cities_aux]
        community_item_cities_processed['community'] = community_id
        community_cities_classified = pd.concat([community_cities_classified, community_item_cities_processed])

    community_cities_classified['number_of_cities'] = 1

    # saving sheet community cities classified
    output_file_community_cities_classified_xlsx = \
        output_path + "community_cities_classified_" + input_file_year_month + ".xlsx"
    if os.path.exists(output_file_community_cities_classified_xlsx):
        os.remove(output_file_community_cities_classified_xlsx)
    community_cities_classified.to_excel(output_file_community_cities_classified_xlsx, index=False)

    # calculating metrics
    sum = community_cities_classified.groupby(['community'], as_index=False).count()
    sum = sum.drop(columns=['ibgeID', 'dose_0', 'dose_1', 'dose'], axis=1)
    mean = community_cities_classified.groupby(['community'], as_index=False).mean()
    mean = mean.drop(columns=['ibgeID', 'dose_0', 'dose_1', 'number_of_cities'], axis=1)
    mean = mean.rename(columns={"community": "x"})
    community_cities_result = pd.concat([sum, mean], axis=1, join="inner")
    community_cities_result = community_cities_result.drop(columns=['x'], axis=1)
    community_cities_result['period'] = input_file_year_month
    community_cities_result = community_cities_result.rename(columns={"dose": "average_vaccination_ratio"})
    first_column = community_cities_result.pop('period')
    community_cities_result.insert(0, 'period', first_column)
    community_cities_result['modularity_of_network'] = modularity

    # defining colors list for components in the graph
    colors = ['k', 'y', 'b', 'r', 'g', 'c', 'm', 'w']

    # setting color and communities attributes in node
    i = 0
    for community_item in communities:
        for node in community_item:
            graph.nodes[node]["color"] = colors[i]
            graph.nodes[node]["community"] = "community_" + str(i + 1)
        if i <= 6:
            i += 1

    return graph, communities, community_cities_result


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


def printNow(text):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    print(f"{text} : {time}")


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
        'input_files_prefix': ['vaccination_ratio_', 'city_doses_'],
        # 'input_files': ['2021_0'],
        'input_files': ['2021_0', '2021_1', '2021_2', '2021_3', '2022_0', '2022_1', '2022_2', '2022_3'],
        'parameters': [brazilian_states, cities],
        'prefixes': ['vacc_proxy_ratio'],
        'targets': ['brazil'],
        'output_path': graphs_path + "graphs_vacc_proxy_ratio/",
        'output_file': 'brazil',
        'name': "Vaccination-Proximity Ratio Graphs",
        'ratio_threshold': ratio_threshold,
        'generate_graph_gexf': True,
    })

    # print("\n----------------------------------------------")

    # This processes all the input files described before
    generateGraphs(data_series)
