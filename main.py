"""Entry point for correctness checks, benchmarks, and memory tests."""

from collections.abc import Callable
from time import perf_counter

import networkx as nx
import pandas as pd

import config
from algorithms import nuutila, pearce, tarjan
from tests import correctness_tests
from utils import benchmarking, memory_tests

SIZE_BENCHMARK = config.SIZE_BENCHMARK
TEST = config.TEST
MEMORY_TEST = config.MEMORY_TEST
TEST_NODE_SIZE = config.TEST_NODE_SIZE
TEST_EDGE_PROBABILITY = config.TEST_EDGE_PROBABILITY
DEBUG = config.DEBUG

type ComponentMap = dict[int, int]
type Algorithm = Callable[[nx.DiGraph], ComponentMap]
type AlgorithmTimings = tuple[float, float, float]
type BenchmarkRuns = dict[str, list[float]]
type BenchmarkFrames = dict[str, pd.DataFrame]

ALGORITHMS: tuple[tuple[str, Algorithm], ...] = (
    ("Pearce", pearce.apply_alg),
    ("Nuutila", nuutila.apply_alg),
    ("Tarjan", tarjan.apply_alg),
)
GRAPH_SIZES = (50, 100, 200, 600)
GRAPH_DENSITIES = ("Sparse", "Medium", "Dense")


def create_test_set() -> BenchmarkFrames:
    """Create the full benchmark matrix for every graph size and density."""
    performance_dict = {
        algorithm_name: pd.DataFrame(
            columns=list(GRAPH_DENSITIES), index=list(GRAPH_SIZES)
        )
        for algorithm_name, _ in ALGORITHMS
    }

    for density_index, density_label in enumerate(GRAPH_DENSITIES):
        benchmark_by_algorithm = {
            algorithm_name: [] for algorithm_name, _ in ALGORITHMS
        }
        for node_count in GRAPH_SIZES:
            benchmark_results = create_benchmark(node_count, density_index)
            for algorithm_name, measurements in benchmark_results.items():
                benchmark_by_algorithm[algorithm_name].append(measurements)
        for algorithm_name, results in benchmark_by_algorithm.items():
            performance_dict[algorithm_name][density_label] = results

    return performance_dict


def create_benchmark(node_count: int, graph_density: int) -> BenchmarkRuns:
    """Benchmark all algorithms on a fixed graph size and density class."""
    print(f"Create benchmark: nodes={node_count} density={graph_density}")

    benchmark_runs = {algorithm_name: [] for algorithm_name, _ in ALGORITHMS}
    for _ in range(SIZE_BENCHMARK):
        pearce_duration, nuutila_duration, tarjan_duration = create_direct_graph(
            node_count, graph_density
        )
        benchmark_runs["Pearce"].append(pearce_duration)
        benchmark_runs["Nuutila"].append(nuutila_duration)
        benchmark_runs["Tarjan"].append(tarjan_duration)

    return benchmark_runs


def create_direct_graph(node_count: int, graph_density: int) -> AlgorithmTimings:
    """Create one random graph and benchmark every algorithm on it."""
    density_by_class = {
        0: 1 / node_count,
        1: 3 / node_count,
        2: 1 / (node_count**0.1),
    }

    try:
        edge_probability = density_by_class[graph_density]
    except KeyError as error:
        raise ValueError(f"Invalid density: {graph_density}") from error

    graph_factory = (
        nx.fast_gnp_random_graph if graph_density == 0 else nx.gnp_random_graph
    )
    graph = graph_factory(node_count, edge_probability, seed=None, directed=True)
    return apply_alg(graph)


def apply_alg(graph: nx.DiGraph) -> AlgorithmTimings:
    """Measure the execution time of every SCC implementation on one graph."""
    timings = []
    for _, algorithm in ALGORITHMS:
        start = perf_counter()
        algorithm(graph)
        timings.append(perf_counter() - start)

    pearce_duration, nuutila_duration, tarjan_duration = timings
    return pearce_duration, nuutila_duration, tarjan_duration


def main() -> int:
    """Run the selected repository mode and return an exit status."""
    if not TEST:
        print("Start")
        performance_results = create_test_set()
        if DEBUG:
            for algorithm_name in performance_results:
                print(
                    f"{algorithm_name} performance: {performance_results[algorithm_name]}"
                )
        benchmarking.plot_result(performance_results)
        print("End")
        return 0

    if MEMORY_TEST:
        try:
            return memory_tests.memory_test()
        except (FileNotFoundError, ValueError) as error:
            print(error)
            return 1

    results = correctness_tests.test_algorithms(TEST_NODE_SIZE, TEST_EDGE_PROBABILITY)
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
