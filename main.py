"""Main module for the Strongly Connected Components project.

This module serves as the entry point for running correctness tests,
performance benchmarks, or memory tests based on configuration settings.
"""

import time
from typing import Dict, Tuple
import networkx as nx
import pandas as pd
from algorithms import tarjan, nuutila, pearce
from utils import benchmarking
from tests import correctness_tests
from utils import memory_tests
import config

SIZE_BENCHMARK = config.SIZE_BENCHMARK
TEST = config.TEST
MEMORY_TEST = config.MEMORY_TEST
TEST_NODE_SIZE = config.TEST_NODE_SIZE
TEST_EDGE_PROBABILITY = config.TEST_EDGE_PROBABILITY
DEBUG = config.DEBUG


def create_test_set() -> Dict[str, pd.DataFrame]:
    """Create a test set of graphs and measure algorithm performance.

    Generates graphs of different sizes and densities, runs all three SCC
    algorithms on each graph, and collects performance statistics.

    Returns:
        Dict containing performance DataFrames for each algorithm, organized
        by graph density (Sparse, Medium, Dense).
    """
    dimension_list = [50, 100, 200, 600]
    density_list = [0, 1, 2]
    # Create a dataframe to save performance for each algorithm
    df1 = pd.DataFrame(columns=['Sparse', 'Medium', 'Dense'], index=dimension_list)
    df2 = pd.DataFrame(columns=['Sparse', 'Medium', 'Dense'], index=dimension_list)
    df3 = pd.DataFrame(columns=['Sparse', 'Medium', 'Dense'], index=dimension_list)
    performance_dict = {'Tarjan': df1, 'Nuutila': df2, 'Pearce': df3}
    for graph_density in density_list:
        column_1 = []
        column_2 = []
        column_3 = []
        for nodes_dimension in dimension_list:
            column_performance = create_benchmark(nodes_dimension, graph_density)
            column_1.append(column_performance['Tarjan'])
            column_2.append(column_performance['Nuutila'])
            column_3.append(column_performance['Pearce'])
        # Based on graph_density, I fill the right column
        if graph_density == 0:
            df1['Sparse'] = column_1
            df2['Sparse'] = column_2
            df3['Sparse'] = column_3
        elif graph_density == 1:
            df1['Medium'] = column_1
            df2['Medium'] = column_2
            df3['Medium'] = column_3
        elif graph_density == 2:
            df1['Dense'] = column_1
            df2['Dense'] = column_2
            df3['Dense'] = column_3
    return performance_dict


def create_benchmark(nodes_dimension: int, graph_density: int) -> Dict[str, list]:
    """Create benchmark for a specific graph size and density.

    Args:
        nodes_dimension: Number of nodes in the graphs.
        graph_density: Density type (0=sparse, 1=medium, 2=dense).

    Returns:
        Dictionary with timing results for each algorithm.
    """
    print(f"Create benchmark : Nodes {nodes_dimension}  -  Density type {graph_density}")
    # List containing time records for each algorithm
    times1_list = []
    times2_list = []
    times3_list = []
    dict_times = {}
    for _ in range(0, SIZE_BENCHMARK):
        # print(i, end="\r")
        times1, times2, times3 = create_direct_graph(nodes_dimension, graph_density)
        times1_list.append(times1)
        times2_list.append(times2)
        times3_list.append(times3)
    dict_times['Pearce'] = times1_list
    dict_times['Nuutila'] = times2_list
    dict_times['Tarjan'] = times3_list
    return dict_times


def set_quantity(nodes_dimension: int, graph_density: int) -> int:
    """Set the quantity of graphs for benchmarking (deprecated).

    This function was initially designed to adapt the benchmark size based on
    graph characteristics, but is no longer used.

    Args:
        nodes_dimension: Number of nodes.
        graph_density: Graph density type.

    Returns:
        Suggested cardinality for the benchmark.
    """
    if graph_density <= 10 ** 2:
        card = nodes_dimension
    elif 1 == graph_density:
        card = 2 * (10 ** 2)
    else:
        card = 10 ** 2
    return card


def create_direct_graph(n: int, d: int) -> Tuple[float, float, float]:
    """Create a random directed graph and measure algorithm performance.

    Args:
        n: Number of nodes.
        d: Density type (0=sparse, 1=medium, 2=dense).

    Returns:
        Tuple of execution times for (Pearce, Nuutila, Tarjan) algorithms.
    """
    # An heuristic to build valid edge probabilities
    def switch_density(argument: int) -> float:
        """Convert density type to edge probability."""
        switcher = {
            0: 1 / n,
            1: 3 / n,
            2: 1 / (n ** 0.1),
        }
        value = switcher.get(argument, False)
        if value is False:
            raise ValueError(f"Invalid Density: {argument}")
        return switcher[argument]

    p = switch_density(d)
    if d == 0:
        graph = nx.fast_gnp_random_graph(n, p, seed=None, directed=True)
    else:
        graph = nx.gnp_random_graph(n, p, seed=None, directed=True)
    return apply_alg(graph)


def apply_alg(graph: nx.DiGraph) -> Tuple[float, float, float]:
    """Apply all three SCC algorithms to a graph and measure execution time.

    Args:
        graph: The input directed graph.

    Returns:
        Tuple of execution times for (Pearce, Nuutila, Tarjan) algorithms.
    """
    # Keep track of time of each algorithm executed
    t0 = time.time()
    pearce.apply_alg(graph)
    duration0 = time.time() - t0
    t1 = time.time()
    nuutila.apply_alg(graph)
    duration1 = time.time() - t1
    t2 = time.time()
    tarjan.apply_alg(graph)
    duration2 = time.time() - t2
    return duration0, duration1, duration2


def main() -> int:
    """Main entry point for the SCC project.

    Based on configuration settings, runs either correctness tests,
    performance benchmarks, or memory tests.

    Returns:
        Exit code (0 for success).
    """
    if not TEST:
        print("Start")
        dict_performance = create_test_set()
        if DEBUG:
            print(f"Tarjan performance: {dict_performance['Tarjan']}")
            print(f"Nuutila performance: {dict_performance['Nuutila']}")
            print(f"Pearce performance: {dict_performance['Pearce']}")
        benchmarking.plot_result(dict_performance)
        print("End")
    else:
        if not MEMORY_TEST:
            correctness_tests.test_algorithms(TEST_NODE_SIZE, TEST_EDGE_PROBABILITY)
        else:
            memory_tests.memory_test()
    return 0


if __name__ == "__main__":
    main()
