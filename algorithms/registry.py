"""Registry of graph algorithms available in the platform."""

from collections.abc import Iterable

import networkx as nx

from algorithms import nuutila, pearce, tarjan
from algorithms.specs import AlgorithmResult, AlgorithmSpec

REGISTRY: dict[str, AlgorithmSpec] = {
    "pearce": AlgorithmSpec(
        key="pearce",
        name="Pearce",
        category="scc",
        graph_kind="directed",
        description="Pearce's SCC algorithm with reverse topological component order.",
        time_complexity="O(V + E)",
        space_complexity="O(V)",
        requires_consecutive_int_nodes=True,
        implementation_path="algorithms/pearce.py",
        runner=pearce.apply_alg,
    ),
    "nuutila": AlgorithmSpec(
        key="nuutila",
        name="Nuutila",
        category="scc",
        graph_kind="directed",
        description="Nuutila's SCC algorithm with path compression and stack optimizations.",
        time_complexity="O(V + E)",
        space_complexity="O(V)",
        requires_consecutive_int_nodes=True,
        implementation_path="algorithms/nuutila.py",
        runner=nuutila.apply_alg,
    ),
    "tarjan": AlgorithmSpec(
        key="tarjan",
        name="Tarjan",
        category="scc",
        graph_kind="directed",
        description="Classic Tarjan SCC algorithm using DFS and low-link roots.",
        time_complexity="O(V + E)",
        space_complexity="O(V)",
        requires_consecutive_int_nodes=True,
        implementation_path="algorithms/tarjan.py",
        runner=tarjan.apply_alg,
    ),
}


def list_algorithms(category: str | None = None) -> list[AlgorithmSpec]:
    """Return the registered algorithms, optionally filtered by category."""
    algorithms = list(REGISTRY.values())
    if category is None:
        return algorithms
    return [algorithm for algorithm in algorithms if algorithm.category == category]


def get_algorithm(key: str) -> AlgorithmSpec:
    """Return one algorithm spec by registry key."""
    try:
        return REGISTRY[key]
    except KeyError as error:
        available = ", ".join(sorted(REGISTRY))
        raise KeyError(
            f"Unknown algorithm '{key}'. Available algorithms: {available}"
        ) from error


def ensure_graph_compatibility(graph: nx.DiGraph, algorithm: AlgorithmSpec) -> None:
    """Validate graph properties required by a registered algorithm."""
    if algorithm.graph_kind == "directed" and not graph.is_directed():
        raise ValueError(f"{algorithm.name} requires a directed graph.")

    if algorithm.requires_consecutive_int_nodes:
        expected_nodes = set(range(graph.number_of_nodes()))
        if set(graph.nodes) != expected_nodes:
            raise ValueError(
                f"{algorithm.name} requires nodes labeled with consecutive integers from 0 to n - 1."
            )


def run_algorithm(
    key: str,
    graph: nx.DiGraph,
    metadata: dict[str, str | int | float | bool] | None = None,
) -> AlgorithmResult:
    """Run one registered algorithm after validating the input graph."""
    algorithm = get_algorithm(key)
    ensure_graph_compatibility(graph, algorithm)
    return algorithm.run(graph, metadata=metadata)


def iter_algorithm_keys(category: str | None = None) -> Iterable[str]:
    """Yield registry keys in the same order as `list_algorithms`."""
    for algorithm in list_algorithms(category=category):
        yield algorithm.key
