"""Shared algorithm metadata and result types."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

import networkx as nx

type ComponentMap = dict[int, int]
type ResultMetadata = Mapping[str, str | int | float | bool]


@dataclass(frozen=True, slots=True)
class AlgorithmResult:
    """Normalized result returned by a registered algorithm."""

    algorithm_key: str
    algorithm_name: str
    category: str
    component_map: ComponentMap
    component_count: int
    metadata: dict[str, str | int | float | bool] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AlgorithmSpec:
    """Metadata and callable wrapper for a graph algorithm."""

    key: str
    name: str
    category: str
    graph_kind: str
    description: str
    time_complexity: str
    space_complexity: str
    requires_consecutive_int_nodes: bool
    implementation_path: str
    runner: Callable[[nx.DiGraph], ComponentMap]

    def run(
        self, graph: nx.DiGraph, metadata: ResultMetadata | None = None
    ) -> AlgorithmResult:
        """Execute the registered algorithm and normalize its result."""
        component_map = self.runner(graph)
        return AlgorithmResult(
            algorithm_key=self.key,
            algorithm_name=self.name,
            category=self.category,
            component_map=component_map,
            component_count=len(set(component_map.values())),
            metadata=dict(metadata or {}),
        )
