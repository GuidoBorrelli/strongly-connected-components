"""Unit tests for the Python 3.14-targeted SCC project."""

import unittest

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
    """Validate the public helpers in main.py."""

    def test_invalid_density_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            main.create_direct_graph(10, 99)

    def test_apply_alg_returns_three_non_negative_durations(self) -> None:
        graph = nx.gnp_random_graph(18, 0.2, seed=17, directed=True)
        durations = main.apply_alg(graph)

        self.assertEqual(len(durations), 3)
        for duration in durations:
            self.assertGreaterEqual(duration, 0.0)


if __name__ == "__main__":
    unittest.main()
