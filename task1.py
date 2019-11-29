from networkx import nx
import pickle
import numpy as np
import queue


def BFS(graph, seed):
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


with open('graph.pickle', 'rb') as input_graph_file:
    G = pickle.load(input_graph_file)

with open('simulation.pickle', 'rb') as input_simulation_file:
    newGs = pickle.load(input_simulation_file)

candidates = list(G.nodes)
selected = list()

for iter in range(25):
    max_index, max_influenced = -1, -1
    for seed in candidates:
        influenced_nums = []
        for newG_index, newG in zip(range(len(newGs)), newGs):
            if seed in newG.nodes:
                influenced_nodes = BFS(newG, seed)
                influenced_nums.append(len(influenced_nodes) - 1)
            else:
                influenced_nums.append(0)
        ave_influenced = np.asarray(influenced_nums).mean()
        if ave_influenced > max_influenced:
            max_index, max_influenced = seed, ave_influenced
    candidates.remove(max_index)
    selected.append(max_index)
    print('Greedy selected seed:', max_index)

    for newG_index, newG in zip(range(len(newGs)), newGs):
        if max_index in newG.nodes:
            influenced_nodes = BFS(newG, max_index)
            newG.remove_nodes_from(influenced_nodes)

print('Seed set:\n', selected)
print('Average number of people influenced:\n', max_influenced)
