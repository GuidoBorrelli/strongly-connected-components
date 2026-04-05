"""Correctness helpers for SCC algorithms."""

import colorsys
import math
import random

import matplotlib.pyplot as plt
import networkx as nx

import config
from algorithms.registry import list_algorithms, run_algorithm
from graph_io.loaders import generate_graph

DEBUG = config.DEBUG

type ComponentMap = dict[int, int]
type ComponentPartition = frozenset[frozenset[int]]

SCC_ALGORITHMS = list_algorithms(category="scc")


def component_partition(component_map: ComponentMap) -> ComponentPartition:
    """Normalize a component mapping into a partition of node sets."""
    partition: dict[int, set[int]] = {}
    for node, component in component_map.items():
        partition.setdefault(component, set()).add(node)
    return frozenset(frozenset(nodes) for nodes in partition.values())


def expected_partition(graph: nx.DiGraph) -> ComponentPartition:
    """Return the SCC partition produced by NetworkX."""
    return frozenset(
        frozenset(component) for component in nx.strongly_connected_components(graph)
    )


def run_algorithms(graph: nx.DiGraph) -> dict[str, ComponentMap]:
    """Execute every registered SCC implementation on the same graph."""
    return {
        algorithm.name: run_algorithm(algorithm.key, graph).component_map
        for algorithm in SCC_ALGORITHMS
    }


def evaluate_algorithms(graph: nx.DiGraph) -> dict[str, bool]:
    """Compare every implementation against NetworkX on a graph."""
    expected = expected_partition(graph)
    return {
        name: component_partition(component_map) == expected
        for name, component_map in run_algorithms(graph).items()
    }


def test_algorithms(
    node_size: int = 0, edge_probability: float = 0.0
) -> dict[str, bool]:
    """Generate a graph, validate the algorithms, and print the results."""
    if node_size == 0:
        node_size = random.randint(10, 600)
    if edge_probability == 0:
        edge_probability = random.randint(1, 90) / 100

    graph = generate_graph(
        "gnp",
        nodes=node_size,
        edge_probability=edge_probability,
        directed=True,
        seed=None,
    )
    algorithm_results = run_algorithms(graph)
    expected = expected_partition(graph)
    results = {
        name: component_partition(component_map) == expected
        for name, component_map in algorithm_results.items()
    }

    if DEBUG:
        for component in nx.strongly_connected_components(graph):
            component_nodes = list(component)
            print("\nSSC: {}".format(component_nodes))
            for node in component_nodes:
                print("\tRoot of node {}:".format(node), end="")
                for algorithm in SCC_ALGORITHMS:
                    print(" {}".format(algorithm_results[algorithm.name][node]), end="")
                print()

    for name, is_correct in results.items():
        print(f"{name}: {is_correct}")

    if node_size <= 40:
        _draw_scc_graph(graph, algorithm_results["Pearce"])

    return results


def _draw_scc_graph(graph: nx.DiGraph, component_map: ComponentMap) -> None:
    """Draw a small graph with SCC edges highlighted."""
    component_values = list(component_map.values())
    edges = [
        [
            edge
            for edge in graph.edges
            if component_map[edge[0]] == component
            and component_map[edge[0]] == component_map[edge[1]]
        ]
        for component in set(component_values)
        if component_values.count(component) > 1
    ]

    pos = nx.circular_layout(graph)
    nx.draw_networkx(graph, pos=pos)
    hue_base = 0.3

    for index, edge_group in enumerate(edges, start=1):
        hue = (index / len(edges)) + hue_base
        hue -= math.floor(hue)
        if DEBUG:
            print(hue)
        color = colorsys.hsv_to_rgb(hue, 1, 1)
        if DEBUG:
            print(color)
        rgb_color = [round(channel * 255) for channel in color]
        if DEBUG:
            print(rgb_color)
        hex_color = "#{:02x}{:02x}{:02x}".format(
            rgb_color[0], rgb_color[1], rgb_color[2]
        )
        if DEBUG:
            print(hex_color)
        nx.draw_networkx_edges(
            graph, pos=pos, edgelist=edge_group, edge_color=hex_color
        )

    plt.show()
