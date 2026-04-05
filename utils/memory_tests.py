"""Memory testing utilities for SCC algorithms."""

import pickle
from pathlib import Path

import networkx as nx
import psutil

import config
from algorithms.registry import get_algorithm, run_algorithm
from graph_io.loaders import generate_graph

GRAPH = config.GRAPH
TEST_NODE_SIZE = config.TEST_NODE_SIZE
TEST_EDGE_PROBABILITY = config.TEST_EDGE_PROBABILITY
TEST_ALG = config.ALG_TEST

MEMORY_TEST_GRAPH_FILE = Path("test_graphs") / "memory_test_graph.pkl"
ALGORITHM_ID_TO_KEY = {1: "pearce", 2: "nuutila", 3: "tarjan"}


def memory_test() -> int:
    """Create or load a graph and report memory usage for one algorithm."""
    if GRAPH:
        graph = generate_graph(
            "gnp",
            nodes=TEST_NODE_SIZE,
            edge_probability=TEST_EDGE_PROBABILITY,
            directed=True,
            seed=None,
        )
        MEMORY_TEST_GRAPH_FILE.parent.mkdir(parents=True, exist_ok=True)
        with MEMORY_TEST_GRAPH_FILE.open("wb") as file_obj:
            pickle.dump(graph, file_obj)
        print(f"Graph saved to {MEMORY_TEST_GRAPH_FILE}")
        return 0

    if not MEMORY_TEST_GRAPH_FILE.exists():
        raise FileNotFoundError(
            f"Missing {MEMORY_TEST_GRAPH_FILE}. Set GRAPH = True and run python main.py once first."
        )

    process = psutil.Process()
    with MEMORY_TEST_GRAPH_FILE.open("rb") as file_obj:
        graph = pickle.load(file_obj)

    algorithm = select_algorithm(TEST_ALG)
    print(nx.density(graph))

    baseline_memory = process.memory_info().rss
    run_algorithm(algorithm.key, graph)
    memory_used = process.memory_info().rss
    increment = memory_used - baseline_memory
    percentage_increment = increment * 100 / baseline_memory

    print(f"{algorithm.name} memory used: {memory_used} - baseline: {baseline_memory}")
    print(f"Increment: {increment} - %: {percentage_increment}%")
    return 0


def select_algorithm(algorithm_id: int):
    """Return the selected algorithm spec for memory testing."""
    try:
        return get_algorithm(ALGORITHM_ID_TO_KEY[algorithm_id])
    except KeyError as error:
        raise ValueError(f"Invalid algorithm id: {algorithm_id}") from error
