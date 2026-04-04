"""Memory testing utilities for SCC algorithms.

This module provides functions to measure memory usage of the SCC algorithms
during execution.
"""

import networkx as nx
import os
import psutil
from algorithms import tarjan, nuutila, pearce
import pickle
import config

GRAPH = config.GRAPH
TEST_NODE_SIZE = config.TEST_NODE_SIZE
TEST_EDGE_PROBABILITY = config.TEST_EDGE_PROBABILITY
TEST_ALG = config.ALG_TEST

# File path for storing test graphs
MEMORY_TEST_GRAPH_FILE = "./test_graphs/memory_test_graph.pkl"


def memory_test():
    """Test memory usage of SCC algorithms.

    Either generates and saves a test graph, or loads a saved graph and
    measures memory usage while running the specified algorithm.

    The algorithm to test is determined by TEST_ALG:
    - 1: Pearce's algorithm
    - 2: Nuutila's algorithm
    - 3: Tarjan's algorithm
    """
    if GRAPH:
        graph = nx.gnp_random_graph(TEST_NODE_SIZE, TEST_EDGE_PROBABILITY, seed=None, directed=True)
        # Save graph
        os.makedirs(os.path.dirname(MEMORY_TEST_GRAPH_FILE), exist_ok=True)
        with open(MEMORY_TEST_GRAPH_FILE, "wb") as f:
            pickle.dump(graph, f)
        print(f"Graph saved to {MEMORY_TEST_GRAPH_FILE}")
    else:
        process = psutil.Process(os.getpid())
        # Read graph
        with open(MEMORY_TEST_GRAPH_FILE, "rb") as f:
            graph = pickle.load(f)
        print(nx.density(graph))
        tara = process.memory_info().rss
        if TEST_ALG == 1:
            _ = pearce.apply_alg(graph)
            memory_used = process.memory_info().rss
        elif TEST_ALG == 2:
            _ = nuutila.apply_alg(graph)
            memory_used = process.memory_info().rss
        elif TEST_ALG == 3:
            _ = tarjan.apply_alg(graph)
            memory_used = process.memory_info().rss
        else:
            return -1
        increment = memory_used - tara
        percentage_increment = increment * 100 / tara
        print("Memory used: {} - Tara: {}".format(memory_used, tara))
        print("Increment: {} - %: {}%".format(increment, percentage_increment))
    return
