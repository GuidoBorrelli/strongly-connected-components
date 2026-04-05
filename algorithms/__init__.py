"""Public algorithm interfaces for the SCC platform."""

from algorithms.registry import get_algorithm, list_algorithms, run_algorithm
from algorithms.specs import AlgorithmResult, AlgorithmSpec

__all__ = [
    "AlgorithmResult",
    "AlgorithmSpec",
    "get_algorithm",
    "list_algorithms",
    "run_algorithm",
]
