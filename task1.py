from networkx import nx
import pickle
import numpy as np
import queue


def BFS(graph, seeds):
    influenced_dict = {seed: None for seed in seeds}
    BFS_queue = queue.Queue(500)
    for seed in seeds:
        BFS_queue.put(seed)
    while not BFS_queue.empty():
        first = BFS_queue.get()
        for node in graph.successors(first):
            if node not in influenced_dict:
                influenced_dict[node] = None
                BFS_queue.put(node)
    return list(influenced_dict.keys())


with open('graph.pickle', 'rb') as input_graph_file:
    G = pickle.load(input_graph_file)

with open('simulation.pickle', 'rb') as input_simulation_file:
    newGs = pickle.load(input_simulation_file)

candidates = list(G.nodes)
selected = list()

for iter in range(25):
    max_index, max_influenced = -1, -1
    for candidate in candidates:
        seeds = selected.copy()
        seeds.append(candidate)
        influenced_nums = []
        for newG_index, newG in zip(range(len(newGs)), newGs):
            influenced_nodes = BFS(newG, seeds)
            influenced_nums.append(len(influenced_nodes) - len(seeds))
        ave_influenced = np.asarray(influenced_nums).mean()
        if ave_influenced > max_influenced:
            max_index, max_influenced = candidate, ave_influenced
    candidates.remove(max_index)
    selected.append(max_index)
    print('Greedy selected seed:', max_index)

print('Seed set:\n', selected)
print('Average number of people influenced:\n', max_influenced)
