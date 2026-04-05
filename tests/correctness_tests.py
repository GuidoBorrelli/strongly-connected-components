"""Correctness testing for SCC algorithms.

This module verifies the implemented SCC algorithms against NetworkX's
`strongly_connected_components` reference implementation.
"""

import colorsys
import math
import random

import matplotlib.pyplot as plt
import networkx as nx

from algorithms import nuutila, pearce, tarjan
import config


DEBUG = config.DEBUG


def test_algorithms(node_size: int = 0, edge_probability: float = 0.0) -> None:
    """Test the correctness of all SCC algorithms.

    Generates a random directed graph and runs all three SCC algorithms,
    comparing their results against NetworkX's strongly_connected_components.

    Args:
        node_size: Number of nodes in the test graph. If 0, a random size is chosen.
        edge_probability: Probability of edge creation. If 0, a random probability is chosen.

    The function prints correctness results and optionally displays a graph
    visualization for small graphs (<= 40 nodes).
    """
    if node_size == 0:
        node_size = random.randint(10, 600)
    if edge_probability == 0:
        edge_probability = random.randint(1, 90) / 100

    graph = nx.gnp_random_graph(node_size, edge_probability, seed=None, directed=True)
    pearce_result = pearce.apply_alg(graph)
    nuutila_result = nuutila.apply_alg(graph)
    tarjan_result = tarjan.apply_alg(graph)

    if DEBUG:
        control_components = nx.strongly_connected_components(graph)
        for component in control_components:
            component_nodes = list(component)
            print("\nSSC: {}".format(component_nodes))
            for node in component_nodes:
                print("\tRoot of node {}:".format(node), end="")
                print(" {}".format(pearce_result[node]), end="")
                print(" {}".format(nuutila_result[node]), end="")
                print(" {}".format(tarjan_result[node]))

    # Check whether node pairs are in the same SCC in each implementation.
    ok = [True] * 3
    for node_1 in graph.nodes:
        for node_2 in graph.nodes:
            if node_1 <= node_2:
                continue

            connected = nx.has_path(graph, node_1, node_2) and nx.has_path(graph, node_2, node_1)
            if DEBUG:
                if connected is not (pearce_result[node_1] == pearce_result[node_2]):
                    print(
                        "node {} and {} are {}connected, Pearce says: {}/{}".format(
                            node_1,
                            node_2,
                            "" if connected else "NOT ",
                            pearce_result[node_1],
                            pearce_result[node_2],
                        )
                    )
                if connected is not (nuutila_result[node_1] == nuutila_result[node_2]):
                    print(
                        "node {} and {} are {}connected, Nuutila says: {}/{}".format(
                            node_1,
                            node_2,
                            "" if connected else "NOT ",
                            nuutila_result[node_1],
                            nuutila_result[node_2],
                        )
                    )
                if connected is not (tarjan_result[node_1] == tarjan_result[node_2]):
                    print(
                        "node {} and {} are {}connected, Tarjan says: {}/{}".format(
                            node_1,
                            node_2,
                            "" if connected else "NOT ",
                            tarjan_result[node_1],
                            tarjan_result[node_2],
                        )
                    )

            checks = [
                connected == (pearce_result[node_1] == pearce_result[node_2]),
                connected == (nuutila_result[node_1] == nuutila_result[node_2]),
                connected == (tarjan_result[node_1] == tarjan_result[node_2]),
            ]
            ok = [current and check for current, check in zip(ok, checks)]

    print("Pearce: {}".format(ok[0]))
    print("Nuutila: {}".format(ok[1]))
    print("Tarjan: {}".format(ok[2]))

    # For small graphs, color SCC edges using Pearce's result as a representative labeling.
    if node_size <= 40:
        pearce_values = list(pearce_result.values())
        edges = [
            [
                edge
                for edge in graph.edges
                if pearce_result[edge[0]] == component and pearce_result[edge[0]] == pearce_result[edge[1]]
            ]
            for component in set(pearce_values)
            if pearce_values.count(component) > 1
        ]
        pos = nx.circular_layout(graph)
        nx.draw_networkx(graph, pos=pos)
        hbase = 0.3
        for index in range(0, len(edges)):
            hue = (index + 1.0) / len(edges) + hbase
            hue = hue - math.floor(hue)
            if DEBUG:
                print(hue)
            color = colorsys.hsv_to_rgb(hue, 1, 1)
            if DEBUG:
                print(color)
            color = [round(channel * 255) for channel in color]
            if DEBUG:
                print(color)
            color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
            if DEBUG:
                print(color)
            nx.draw_networkx_edges(graph, pos=pos, edgelist=edges[index], edge_color=color)
        plt.show()
