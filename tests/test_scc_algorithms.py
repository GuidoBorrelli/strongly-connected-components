"""Unit tests for the SCC implementations."""

import io
import unittest
from contextlib import redirect_stdout

import networkx as nx

import main
from tests import correctness_tests


class SCCAlgorithmTests(unittest.TestCase):
    """Validate the SCC implementations against NetworkX."""

    def assert_matches_networkx(self, graph: nx.DiGraph) -> None:
        results = correctness_tests.evaluate_algorithms(graph)
        self.assertTrue(all(results.values()), msg=results)

    def test_known_component_structure(self) -> None:
        graph = nx.DiGraph()
        graph.add_nodes_from(range(6))
        graph.add_edges_from(
            [
                (0, 1),
                (1, 2),
                (2, 0),
                (2, 3),
                (3, 4),
                (4, 3),
            ]
        )

        self.assert_matches_networkx(graph)

    def test_random_graphs_match_networkx(self) -> None:
        for seed in range(5):
            with self.subTest(seed=seed):
                graph = nx.gnp_random_graph(25, 0.18, seed=seed, directed=True)
                self.assert_matches_networkx(graph)

    def test_partition_helper_matches_networkx(self) -> None:
        graph = nx.gnp_random_graph(20, 0.22, seed=11, directed=True)
        algorithm_results = correctness_tests.run_algorithms(graph)
        expected = correctness_tests.expected_partition(graph)

        for algorithm_name, component_map in algorithm_results.items():
            with self.subTest(algorithm=algorithm_name):
                self.assertEqual(
                    correctness_tests.component_partition(component_map), expected
                )


class MainModuleTests(unittest.TestCase):
    """Validate the public entry points in main.py."""

    def test_main_returns_success_in_correctness_mode(self) -> None:
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main.main(), 0)


if __name__ == "__main__":
    unittest.main()
