"""Reusable benchmark case definitions."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    """One graph-generation case in a benchmark suite."""

    case_key: str
    density_label: str
    graph_kind: str
    node_count: int
    edge_probability: float
    directed: bool = True

    def to_metadata(self) -> dict[str, str | int | float | bool]:
        """Serialize the case into JSON-friendly metadata."""
        return asdict(self)


def build_default_scc_suite(
    node_counts: tuple[int, ...] = (50, 100, 200, 600),
) -> list[BenchmarkCase]:
    """Build the repository's default SCC benchmark suite."""
    cases: list[BenchmarkCase] = []
    for node_count in node_counts:
        cases.append(
            BenchmarkCase(
                case_key=f"sparse-{node_count}",
                density_label="Sparse",
                graph_kind="fast_gnp",
                node_count=node_count,
                edge_probability=1 / node_count,
            )
        )
        cases.append(
            BenchmarkCase(
                case_key=f"medium-{node_count}",
                density_label="Medium",
                graph_kind="gnp",
                node_count=node_count,
                edge_probability=3 / node_count,
            )
        )
        cases.append(
            BenchmarkCase(
                case_key=f"dense-{node_count}",
                density_label="Dense",
                graph_kind="gnp",
                node_count=node_count,
                edge_probability=1 / (node_count**0.1),
            )
        )
    return cases
