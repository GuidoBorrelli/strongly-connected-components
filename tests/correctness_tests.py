"""Correctness testing for SCC algorithms.

This module provides functions to verify that the implemented SCC algorithms
produce correct results by comparing against NetworkX's built-in SCC finder.
"""

import random
import networkx as nx
from algorithms import tarjan, nuutila, pearce
import colorsys
import math
import matplotlib.pyplot as plt
import config


DEBUG = config.DEBUG


def test_algorithms(node_size: int = 0, edge_probability: float = 0.0):
    """Test the correctness of all SCC algorithms.

    Generates a random directed graph and runs all three SCC algorithms,
    comparing their results against NetworkX's strongly_connected_components.

    Args:
        node_size: Number of nodes in the test graph. If 0, a random size is chosen.
        edge_probability: Probability of edge creation. If 0, a random probability is chosen.

    The function prints correctness results and optionally displays a graph
    visualization for small graphs (≤40 nodes).
    """
    if node_size == 0:
        node_size = random.randint(10, 600)
    if edge_probability == 0:
        edge_probability = random.randint(1, 90) / 100
    graph = nx.gnp_random_graph(node_size, edge_probability, seed=None, directed=True)
    pass
    res_1 = pearce.apply_alg(graph)
    res_2 = nuutila.apply_alg(graph)
    res_3 = tarjan.apply_alg(graph)
    if DEBUG:
        ctrl = nx.strongly_connected_components(graph)
        for comp in ctrl:
            lst = list(comp)
            print("\nSSC: {}".format(lst))
            for n in lst:
                print("\tRoot of node {}:".format(n), end='')
                print(" {}".format(res_1[n]), end='')
                print(" {}".format(res_2[n]), end='')
                print(" {}".format(res_3[n]))

    # Check if 2 nodes are effectively in the same component or not as expected
    ok = [True] * 3
    for n1 in graph.nodes:
        for n2 in graph.nodes:
            if n1 > n2:
                connected = nx.has_path(graph, n1, n2) and nx.has_path(graph, n2, n1)
                if DEBUG:
                    if connected is not (res_1[n1] == res_1[n2]):
                        print("node {} and {} are {}connected, algo 1 says: {}/{}".format(
                            n1, n2, "" if connected else "NOT ", res_1[n1], res_1[n2]
                        ))
                    if connected is not (res_2[n1] == res_2[n2]):
                        print("node {} and {} are {}connected, algo 2 says: {}/{}".format(
                            n1, n2, "" if connected else "NOT ", res_2[n1], res_2[n2]
                        ))
                    if connected is not (res_3[n1] == res_3[n2]):
                        print("node {} and {} are {}connected, algo 3 says: {}/{}".format(
                            n1, n2, "" if connected else "NOT ", res_3[n1], res_3[n2]
                        ))
                ok = [ok[i] and [
                    connected == (res_1[n1] == res_1[n2]),
                    connected == (res_2[n1] == res_2[n2]),
                    connected == (res_3[n1] == res_3[n2])
                ][i] for i in range(len(ok))]
    print("Algorithm 1: {}".format(ok[0]))
    print("Algorithm 2: {}".format(ok[1]))
    print("Algorithm 3: {}".format(ok[2]))
    # Print graph result in case of affordable graph size, using in this case alg1 results.
    # If previous results are True, results are the same.
    # In case of a False, you can select its result to debug: change res_x variable
    if node_size <= 40:
        # Select group of edges for each SSC not composed only by one node for the sake of coloring
        edges = [[e for e in graph.edges if res_1[e[0]] == n and res_1[e[0]] == res_1[e[1]]] for n in set(res_1.values()) if list(res_1.values()).count(n) > 1]
        pos = nx.circular_layout(graph)
        nx.draw_networkx(graph, pos=pos)
        hbase = 0.3
        for g in range(0, len(edges)):
            h = (g + 1.0) / len(edges) + hbase
            h = h - math.floor(h)
            if DEBUG:
                print(h)
            color = colorsys.hsv_to_rgb(h, 1, 1)
            if DEBUG:
                print(color)
            color = [round(c * 255) for c in color]
            if DEBUG:
                print(color)
            color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
            if DEBUG:
                print(color)
            nx.draw_networkx_edges(graph, pos=pos, edgelist=edges[g], edge_color=color)
        plt.show()
    return
