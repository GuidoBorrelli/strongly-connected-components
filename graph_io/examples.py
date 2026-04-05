"""Curated example graphs for notebooks, tests, and demos."""

from pathlib import Path

import networkx as nx

from graph_io.loaders import load_graph

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "examples"
EXAMPLE_FILES: dict[str, Path] = {
    "lecture_example": EXAMPLES_DIR / "lecture_example.adjlist",
    "two_sccs": EXAMPLES_DIR / "two_sccs.edgelist",
    "branched_scc": EXAMPLES_DIR / "branched_scc.json",
}


def list_examples() -> dict[str, str]:
    """Return the curated example graph names and paths."""
    return {name: str(path) for name, path in EXAMPLE_FILES.items()}


def load_example_graph(name: str, *, relabel: bool = True) -> nx.DiGraph:
    """Load one of the curated example graphs."""
    try:
        example_path = EXAMPLE_FILES[name]
    except KeyError as error:
        available = ", ".join(sorted(EXAMPLE_FILES))
        raise KeyError(
            f"Unknown example '{name}'. Available examples: {available}"
        ) from error

    return load_graph(example_path, relabel=relabel)
