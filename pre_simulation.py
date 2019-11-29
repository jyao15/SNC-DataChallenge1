from networkx import nx
import pickle
import numpy as np

with open('graph.pickle', 'rb') as input_graph_file:
    G = pickle.load(input_graph_file)

newGs = []

for i in range(500):
    newG = nx.DiGraph()
    newG.add_nodes_from(list(G.nodes))
    for u, v in G.out_edges:
        rand_num = np.random.random()
        if G.nodes[u]['region'] == G.nodes[v]['region']:
            if rand_num < 0.2:
                newG.add_edge(u, v)
        else:
            if rand_num < 0.1:
                newG.add_edge(u, v)
    newGs.append(newG)
with open('simulation.pickle', 'wb') as output_graph_file:
    pickle.dump(newGs, output_graph_file, pickle.HIGHEST_PROTOCOL)
