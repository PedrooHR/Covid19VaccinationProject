"""
Project: Final Project - Covid19 Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 21/10/2022
Version: 1.0.0
Function: Generate graphs
"""

# ###########################################
# Importing Libraries
# ###########################################
import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite


# ###########################################
# Library Methods
# ###########################################

def drawGraph(G, title, output):
    fig = plt.figure(figsize=(5, 5))
    X = {n for n, d in G.nodes(data=True) if d["bipartite"] == 0}
    Y = set(G) - X
    X = sorted(X)
    Y = sorted(Y)
    pos = dict()
    pos.update( (n, (1, i*10)) for i, n in enumerate(X) ) # put nodes from X at x=1
    pos.update( (n, (2, i*10)) for i, n in enumerate(Y) ) # put nodes from Y at x=2

    edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    # Nodes
    nx.draw_networkx_nodes(G, pos, node_size=2000)

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    # Edges
    edge_values = nx.get_edge_attributes(G, "weight")
    edges_df = pd.DataFrame(edge_values.values(), columns=['weight'], index=pd.MultiIndex.from_tuples(edge_values.keys(), names=["first", "second"]))
    sum_edges_df = edges_df.groupby(level=['first']).sum()
    values_edges_perc = []
    for idx, row in edges_df.iterrows():
       values_edges_perc.append(row[0]/sum_edges_df['weight'][idx[0]])
    edges_df['percentage'] = values_edges_perc
    # pd.set_option('precision', 4)
    edges_df.to_excel(output + '.xlsx')
    edge_widths = np.array(list(edge_values.values()))
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=(edge_widths / 250), alpha=0.5, edge_color="b")

    # edge weight labels        
    # nx.draw_networkx_edge_labels(G, pos, edge_values, 0.85)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output + '.png')
    plt.close()
    # plt.show()

def generateGraphs(data_series, number_of_classes):
    for input_serie in data_series:
        # To work better
        input_files = input_serie['input_files']
        output_path = input_serie['output_path']
        targets = input_serie['targets']
        prefixes = input_serie['prefixes']
        output_files = input_serie['output_files']
        name = input_serie['name']

        print("\n----------------------------------------------")
        print(f"Processing data for {name}")

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        for id in range(len(targets)):
            target = targets[id] 
            output_file = output_files[id] 

            prefix_id = 0
            bipartite_series = []
            for sheet in input_files:
                print(f"Reading data from {sheet}")
                raw_data = pd.read_excel(sheet)
                prefix_data = prefixes[prefix_id] + raw_data[target].astype(str)
                bipartite_series.append({'name': prefixes[prefix_id], 'value': pd.DataFrame(prefix_data)})
                prefix_id = prefix_id + 1

            bipartite_nodes = []
            bipartite_id = 0
            for bipartite_serie in bipartite_series:
                unique_values = bipartite_serie['value'].nunique()
                nodes = np.arange(0, number_of_classes)
                nodes = [bipartite_serie['name'] + str(x) for x in nodes]
                bipartite_nodes.append({'id': bipartite_id, 'nodes': nodes})
                bipartite_id = bipartite_id + 1

            bipartite_edges = []
            for serie_id in range(len(bipartite_series)-1):
                mixed_series = pd.concat([bipartite_series[serie_id]['value'], bipartite_series[serie_id + 1]['value']], axis=1) 
                mixed_series = mixed_series.dropna()
                for id, row in mixed_series.iterrows():
                    bipartite_edges.append((row[0], row[1]))


            set_edges = set(bipartite_edges)
            weighted_edges = []
            for edge_type in set_edges:
                count_edges = bipartite_edges.count(edge_type)
                weighted_edges.append({'n1': edge_type[0], 'n2': edge_type[1], 'weight': count_edges})

            # Construct graph
            G = nx.Graph()
            # Nodes
            for nodes in bipartite_nodes:
                G.add_nodes_from(nodes['nodes'], bipartite=nodes['id']) 

            # Edges
            for edge in weighted_edges:
                G.add_edge(edge['n1'], edge['n2'], weight=edge['weight'])

            title = name.split(' ')[0] + " - " + target
            drawGraph(G, title, output_path + output_file)

            print(output_path + output_file + '.gexf')
            nx.write_gexf(G, output_path + output_file + '.gexf')



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

    # Series that describe files to read
    data_series = []

    # Vaccination_Cases data
    data_series.append({
        'input_files': [calculations_path + "classes_vaccination.xlsx", calculations_path + "classes_cases.xlsx"],
        'prefixes': ['vacc_', 'cases_'],
        'targets': ['(1-3)/2021', '(4-6)/2021', '(7-9)/2021', '(10-12)/2021', '(1-3)/2022','(4-6)/2022', '(7-9)/2022'],
        'output_path': graphs_path + "graphs_vacc_cases/",
        'output_files': ['2021-1to3','2021-4to6', '2021-7to9', '2021-10to12', '2022-1to3', '2022-4to6', '2022-7to9'],
        'name': "Vaccination-Cases BiGraphs",
    })

    # Vaccination_Deaths data
    data_series.append({
        'input_files': [calculations_path + "classes_vaccination.xlsx", calculations_path + "classes_deaths.xlsx"],
        'prefixes': ['vacc_', 'deaths_'],
        'targets': ['(1-3)/2021', '(4-6)/2021', '(7-9)/2021', '(10-12)/2021', '(1-3)/2022','(4-6)/2022', '(7-9)/2022'],
        'output_path': graphs_path + "graphs_vacc_deaths/",
        'output_files': ['2021-1to3','2021-4to6', '2021-7to9', '2021-10to12', '2022-1to3', '2022-4to6', '2022-7to9'],
        'name': "Vaccination-Deaths BiGraphs",
    })

    # Vaccination_CHDI data
    data_series.append({
        'input_files': [calculations_path + "classes_vaccination.xlsx", calculations_path + "classes_chdi.xlsx"],
        'prefixes': ['vacc_', 'chdi_'],
        'targets': ['(1-3)/2021', '(4-6)/2021', '(7-9)/2021', '(10-12)/2021', '(1-3)/2022','(4-6)/2022', '(7-9)/2022'],
        'output_path': graphs_path + "graphs_vacc_chdi/",
        'output_files': ['2021-1to3','2021-4to6', '2021-7to9', '2021-10to12', '2022-1to3', '2022-4to6', '2022-7to9'],
        'name': "Vaccination-CHDI BiGraphs",
    })

    # This processes all the input files described before
    generateGraphs(data_series, 5)

