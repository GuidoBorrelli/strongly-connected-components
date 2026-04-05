"""Tests for the small graph algorithms platform layers."""

import json
import tempfile
import unittest
from pathlib import Path

import networkx as nx
import pandas as pd

from algorithms.registry import list_algorithms, run_algorithm
from benchmarks.exporters import export_benchmark_results
from benchmarks.runner import run_benchmark_suite
from benchmarks.suites import BenchmarkCase
from graph_io.examples import list_examples, load_example_graph
from graph_io.loaders import generate_graph, load_graph


class RegistryTests(unittest.TestCase):
    """Validate the algorithm registry."""

    def test_registry_lists_scc_algorithms(self) -> None:
        algorithm_keys = [
            algorithm.key for algorithm in list_algorithms(category="scc")
        ]
        self.assertEqual(algorithm_keys, ["pearce", "nuutila", "tarjan"])

    def test_run_algorithm_returns_normalized_result(self) -> None:
        graph = nx.DiGraph([(0, 1), (1, 0), (1, 2)])
        result = run_algorithm("tarjan", graph)

        self.assertEqual(result.algorithm_key, "tarjan")
        self.assertEqual(result.algorithm_name, "Tarjan")
        self.assertEqual(result.component_count, 2)

    def test_registry_rejects_non_normalized_nodes(self) -> None:
        graph = nx.DiGraph([("a", "b"), ("b", "a")])
        with self.assertRaises(ValueError):
            run_algorithm("pearce", graph)


class LoaderTests(unittest.TestCase):
    """Validate file and example loaders."""

    def test_load_edgelist_relabels_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            edge_path = Path(temp_dir) / "sample.edgelist"
            edge_path.write_text("A B\nB A\nB C\n", encoding="utf-8")

            graph = load_graph(edge_path)

        self.assertEqual(set(graph.nodes), {0, 1, 2})
        self.assertTrue(graph.graph["was_relabelled"])
        self.assertEqual(graph.number_of_edges(), 3)

    def test_load_json_graph(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = Path(temp_dir) / "sample.json"
            json_path.write_text(
                json.dumps(
                    {
                        "directed": True,
                        "nodes": ["s", "a", "b"],
                        "edges": [["s", "a"], ["a", "b"], ["b", "a"]],
                    }
                ),
                encoding="utf-8",
            )

            graph = load_graph(json_path)

        self.assertEqual(set(graph.nodes), {0, 1, 2})
        self.assertEqual(graph.number_of_edges(), 3)

    def test_load_graphml_graph(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            graph_path = Path(temp_dir) / "sample.graphml"
            graph = nx.DiGraph()
            graph.add_edge("u", "v")
            nx.write_graphml(graph, graph_path)

            loaded_graph = load_graph(graph_path)

        self.assertEqual(set(loaded_graph.nodes), {0, 1})

    def test_generate_graph_has_expected_metadata(self) -> None:
        graph = generate_graph("gnp", nodes=10, edge_probability=0.2, seed=7)
        self.assertEqual(graph.graph["graph_source"], "generated")
        self.assertEqual(graph.graph["seed"], 7)

    def test_load_example_graph(self) -> None:
        examples = list_examples()
        self.assertIn("two_sccs", examples)
        graph = load_example_graph("two_sccs")
        self.assertTrue(graph.is_directed())
        self.assertGreaterEqual(graph.number_of_nodes(), 2)


class BenchmarkTests(unittest.TestCase):
    """Validate benchmark execution and export."""

    def test_benchmark_export_writes_expected_files(self) -> None:
        cases = [
            BenchmarkCase(
                case_key="tiny-sparse",
                density_label="Sparse",
                graph_kind="fast_gnp",
                node_count=8,
                edge_probability=0.125,
            )
        ]
        run_records, summary_records, metadata = run_benchmark_suite(
            cases,
            repeat_count=2,
            suite_name="unit-test-suite",
            base_seed=10,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            export_dir = export_benchmark_results(
                run_records,
                summary_records,
                metadata,
                output_root=temp_dir,
            )

            self.assertTrue((export_dir / "runs.csv").exists())
            self.assertTrue((export_dir / "summary.csv").exists())
            self.assertTrue((export_dir / "metadata.json").exists())

            runs_frame = pd.read_csv(export_dir / "runs.csv")
            summary_frame = pd.read_csv(export_dir / "summary.csv")
            self.assertIn("algorithm_key", runs_frame.columns)
            self.assertIn("mean_runtime_milliseconds", summary_frame.columns)

            with (export_dir / "metadata.json").open("r", encoding="utf-8") as file_obj:
                exported_metadata = json.load(file_obj)
            self.assertEqual(exported_metadata["suite_name"], "unit-test-suite")


if __name__ == "__main__":
    unittest.main()
