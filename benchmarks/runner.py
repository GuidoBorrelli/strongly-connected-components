"""Benchmark execution and summarization helpers."""

import platform
import sys
from dataclasses import asdict, dataclass
from importlib import metadata
from statistics import StatisticsError, mean, variance
from time import perf_counter

import networkx as nx

from algorithms.registry import AlgorithmSpec, list_algorithms, run_algorithm
from benchmarks.suites import BenchmarkCase
from graph_io.loaders import generate_graph


@dataclass(frozen=True, slots=True)
class BenchmarkRunRecord:
    """One algorithm execution on one generated graph."""

    suite_name: str
    case_key: str
    density_label: str
    graph_kind: str
    node_count: int
    edge_probability: float
    edge_count: int
    density: float
    repeat_index: int
    seed: int
    algorithm_key: str
    algorithm_name: str
    runtime_seconds: float
    runtime_milliseconds: float
    component_count: int

    def to_row(self) -> dict[str, str | int | float]:
        """Serialize the record into a CSV-friendly row."""
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BenchmarkSummaryRecord:
    """Aggregate metrics for one algorithm on one benchmark case."""

    suite_name: str
    case_key: str
    density_label: str
    graph_kind: str
    node_count: int
    edge_probability: float
    algorithm_key: str
    algorithm_name: str
    repeat_count: int
    mean_runtime_seconds: float
    mean_runtime_milliseconds: float
    variance_runtime_seconds: float
    variance_runtime_milliseconds: float
    min_runtime_seconds: float
    max_runtime_seconds: float
    avg_edge_count: float
    avg_density: float
    component_count: int

    def to_row(self) -> dict[str, str | int | float]:
        """Serialize the summary into a CSV-friendly row."""
        return asdict(self)


def run_benchmark_suite(
    cases: list[BenchmarkCase],
    *,
    repeat_count: int,
    algorithms: list[AlgorithmSpec] | None = None,
    suite_name: str = "scc-default",
    base_seed: int = 0,
) -> tuple[list[BenchmarkRunRecord], list[BenchmarkSummaryRecord], dict[str, object]]:
    """Execute a benchmark suite and return raw records, summaries, and metadata."""
    selected_algorithms = algorithms or list_algorithms(category="scc")
    run_records: list[BenchmarkRunRecord] = []

    for case_index, case in enumerate(cases):
        for repeat_index in range(repeat_count):
            seed = base_seed + (case_index * repeat_count) + repeat_index
            graph = generate_graph(
                case.graph_kind,
                nodes=case.node_count,
                edge_probability=case.edge_probability,
                directed=case.directed,
                seed=seed,
            )
            edge_count = graph.number_of_edges()
            graph_density = nx.density(graph)
            for algorithm in selected_algorithms:
                start = perf_counter()
                result = run_algorithm(
                    algorithm.key,
                    graph,
                    metadata={"suite_name": suite_name, "case_key": case.case_key},
                )
                runtime_seconds = perf_counter() - start
                run_records.append(
                    BenchmarkRunRecord(
                        suite_name=suite_name,
                        case_key=case.case_key,
                        density_label=case.density_label,
                        graph_kind=case.graph_kind,
                        node_count=case.node_count,
                        edge_probability=case.edge_probability,
                        edge_count=edge_count,
                        density=graph_density,
                        repeat_index=repeat_index,
                        seed=seed,
                        algorithm_key=algorithm.key,
                        algorithm_name=algorithm.name,
                        runtime_seconds=runtime_seconds,
                        runtime_milliseconds=runtime_seconds * 1000,
                        component_count=result.component_count,
                    )
                )

    summary_records = summarize_run_records(run_records)
    metadata_payload = build_benchmark_metadata(
        cases=cases,
        repeat_count=repeat_count,
        selected_algorithms=selected_algorithms,
        suite_name=suite_name,
        base_seed=base_seed,
    )
    return run_records, summary_records, metadata_payload


def summarize_run_records(
    run_records: list[BenchmarkRunRecord],
) -> list[BenchmarkSummaryRecord]:
    """Aggregate benchmark run records into per-case summaries."""
    grouped: dict[tuple[str, str], list[BenchmarkRunRecord]] = {}
    for record in run_records:
        grouped.setdefault((record.case_key, record.algorithm_key), []).append(record)

    summary_records: list[BenchmarkSummaryRecord] = []
    for _, records in sorted(grouped.items()):
        reference = records[0]
        runtimes = [record.runtime_seconds for record in records]
        edge_counts = [record.edge_count for record in records]
        densities = [record.density for record in records]
        try:
            runtime_variance = variance(runtimes)
        except StatisticsError:
            runtime_variance = 0.0

        summary_records.append(
            BenchmarkSummaryRecord(
                suite_name=reference.suite_name,
                case_key=reference.case_key,
                density_label=reference.density_label,
                graph_kind=reference.graph_kind,
                node_count=reference.node_count,
                edge_probability=reference.edge_probability,
                algorithm_key=reference.algorithm_key,
                algorithm_name=reference.algorithm_name,
                repeat_count=len(records),
                mean_runtime_seconds=mean(runtimes),
                mean_runtime_milliseconds=mean(runtimes) * 1000,
                variance_runtime_seconds=runtime_variance,
                variance_runtime_milliseconds=runtime_variance * 1000,
                min_runtime_seconds=min(runtimes),
                max_runtime_seconds=max(runtimes),
                avg_edge_count=mean(edge_counts),
                avg_density=mean(densities),
                component_count=records[-1].component_count,
            )
        )

    return summary_records


def build_benchmark_metadata(
    *,
    cases: list[BenchmarkCase],
    repeat_count: int,
    selected_algorithms: list[AlgorithmSpec],
    suite_name: str,
    base_seed: int,
) -> dict[str, object]:
    """Build reproducibility metadata for a benchmark export."""
    packages = {}
    for package_name in ("matplotlib", "networkx", "numpy", "pandas", "psutil"):
        try:
            packages[package_name] = metadata.version(package_name)
        except metadata.PackageNotFoundError:
            packages[package_name] = "not-installed"

    return {
        "suite_name": suite_name,
        "repeat_count": repeat_count,
        "base_seed": base_seed,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "algorithms": [
            {
                "key": algorithm.key,
                "name": algorithm.name,
                "category": algorithm.category,
                "implementation_path": algorithm.implementation_path,
            }
            for algorithm in selected_algorithms
        ],
        "cases": [case.to_metadata() for case in cases],
    }
