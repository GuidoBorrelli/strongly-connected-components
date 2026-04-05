"""Memory testing utilities for SCC algorithms."""

import pickle
from collections.abc import Callable
from pathlib import Path

import networkx as nx
import psutil

import config
from algorithms import nuutila, pearce, tarjan

GRAPH = config.GRAPH
TEST_NODE_SIZE = config.TEST_NODE_SIZE
TEST_EDGE_PROBABILITY = config.TEST_EDGE_PROBABILITY
TEST_ALG = config.ALG_TEST

MEMORY_TEST_GRAPH_FILE = Path("test_graphs") / "memory_test_graph.pkl"

type ComponentMap = dict[int, int]
type Algorithm = Callable[[nx.DiGraph], ComponentMap]


def memory_test() -> int:
    """Create or load a graph and report memory usage for one algorithm."""
    if GRAPH:
        graph = nx.gnp_random_graph(
            TEST_NODE_SIZE, TEST_EDGE_PROBABILITY, seed=None, directed=True
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

    algorithm_name, algorithm = select_algorithm(TEST_ALG)
    print(nx.density(graph))

    baseline_memory = process.memory_info().rss
    algorithm(graph)
    memory_used = process.memory_info().rss
    increment = memory_used - baseline_memory
    percentage_increment = increment * 100 / baseline_memory

    print(f"{algorithm_name} memory used: {memory_used} - baseline: {baseline_memory}")
    print(f"Increment: {increment} - %: {percentage_increment}%")
    return 0


def select_algorithm(algorithm_id: int) -> tuple[str, Algorithm]:
    """Return the selected algorithm callable for memory testing."""
    match algorithm_id:
        case 1:
            return "Pearce", pearce.apply_alg
        case 2:
            return "Nuutila", nuutila.apply_alg
        case 3:
            return "Tarjan", tarjan.apply_alg
        case _:
            raise ValueError(f"Invalid algorithm id: {algorithm_id}")
