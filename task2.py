from networkx import nx
import pickle
import numpy as np
import queue
from collections import defaultdict


def BFS(graph, seed):
    if seed not in graph.nodes:
        return []
    influenced_dict = {seed: None}
    BFS_queue = queue.Queue(500)
    BFS_queue.put(seed)
    while not BFS_queue.empty():
        first = BFS_queue.get()
        for node in graph.successors(first):
            if node not in influenced_dict:
                influenced_dict[node] = None
                BFS_queue.put(node)
    return list(influenced_dict.keys())


def calculate_objective(graph, region_total_count, region_selected_count, influenced_nodes, softmin=True):
    region_selected_count = region_selected_count.copy()
    for node in influenced_nodes:
        region_selected_count[graph.nodes[node]['region']] += 1
    proportions = []
    for region, size in region_total_count.items():
        selected_count = region_selected_count[region]
        proportions.append(selected_count / size)
    if softmin:
        objective = np.sum(np.sqrt(np.asarray(proportions))) ** 2
    else:
        objective = np.asarray(proportions).min()
    return objective


with open('graph.pickle', 'rb') as input_graph_file:
    G = pickle.load(input_graph_file)

with open('simulation.pickle', 'rb') as input_simulation_file:
    newGs = pickle.load(input_simulation_file)

candidates = list(G.nodes)
selected = list()
region_total_count = defaultdict(int)
for node in G.nodes:
    region_total_count[G.nodes[node]['region']] += 1
region_selected_count = defaultdict(int)

for iter in range(25):
    max_index, max_objective = -1, -1
    for seed in candidates:
        objectives = []
        for newG_index, newG in zip(range(len(newGs)), newGs):
            influenced_nodes = BFS(newG, seed)
            objective = calculate_objective(G, region_total_count, region_selected_count, influenced_nodes)
            objectives.append(objective)
        ave_objective = np.asarray(objectives).mean()
        if ave_objective > max_objective:
            max_index, max_objective = seed, ave_objective
    candidates.remove(max_index)
    selected.append(max_index)
    print('Greedy selected seed', iter + 1, ':', max_index)

    for newG_index, newG in zip(range(len(newGs)), newGs):
        influenced_nodes = BFS(newG, max_index)
        newG.remove_nodes_from(influenced_nodes)

print('Seed set:\n', selected)
print('Average number of people influenced (including seeds):')
influenced_nums = []
for newG_index, newG in zip(range(len(newGs)), newGs):
    influenced_nums.append(len(G.nodes) - len(newG.nodes))
print(np.asarray(influenced_nums).mean())
print('Average minimal of people influenced (including seeds):')
print(calculate_objective(G, region_total_count, region_selected_count, [], softmin=False))
