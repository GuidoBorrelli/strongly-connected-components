"""Load graphs from files or generated benchmarks."""

import json
from pathlib import Path

import networkx as nx

SUPPORTED_FORMATS = {
    ".adjlist": "adjlist",
    ".edgelist": "edgelist",
    ".edges": "edgelist",
    ".graphml": "graphml",
    ".json": "json",
    ".txt": "edgelist",
}


def resolve_format(path: Path, file_format: str) -> str:
    """Resolve a loader format from an explicit value or a file suffix."""
    if file_format != "auto":
        return file_format

    try:
        return SUPPORTED_FORMATS[path.suffix.lower()]
    except KeyError as error:
        supported = ", ".join(sorted(SUPPORTED_FORMATS.values()))
        raise ValueError(
            f"Could not infer graph format from {path.name}. Supported formats: {supported}"
        ) from error


def normalize_graph(
    graph: nx.Graph | nx.DiGraph,
    *,
    directed: bool = True,
    relabel: bool = True,
) -> nx.DiGraph:
    """Normalize a graph to the repository's preferred directed representation."""
    normalized = nx.DiGraph(graph) if directed else nx.Graph(graph)
    normalized.graph.update(graph.graph)

    if not relabel:
        normalized.graph["was_relabelled"] = False
        return nx.DiGraph(normalized) if directed else normalized

    mapping = {node: index for index, node in enumerate(normalized.nodes)}
    relabelled = nx.relabel_nodes(normalized, mapping, copy=True)
    relabelled.graph.update(normalized.graph)
    relabelled.graph["was_relabelled"] = mapping != {
        node: node for node in normalized.nodes if isinstance(node, int)
    }
    relabelled.graph["original_node_labels"] = {
        str(index): str(original_label) for original_label, index in mapping.items()
    }
    return relabelled


def load_graph(
    path: str | Path,
    *,
    file_format: str = "auto",
    directed: bool = True,
    relabel: bool = True,
) -> nx.DiGraph:
    """Load a graph from disk and normalize it for the platform."""
    graph_path = Path(path)
    resolved_format = resolve_format(graph_path, file_format)

    match resolved_format:
        case "edgelist":
            graph = nx.read_edgelist(
                graph_path,
                create_using=nx.DiGraph() if directed else nx.Graph(),
                data=False,
            )
        case "adjlist":
            graph = nx.read_adjlist(
                graph_path,
                create_using=nx.DiGraph() if directed else nx.Graph(),
            )
        case "graphml":
            graph = nx.read_graphml(graph_path)
        case "json":
            graph = load_json_graph(graph_path, directed=directed)
        case _:
            raise ValueError(f"Unsupported graph format: {resolved_format}")

    graph.graph["graph_source"] = "file"
    graph.graph["graph_path"] = str(graph_path)
    graph.graph["graph_format"] = resolved_format
    return normalize_graph(graph, directed=directed, relabel=relabel)


def load_json_graph(path: Path, *, directed: bool = True) -> nx.DiGraph:
    """Load a graph from a small JSON interchange format."""
    with path.open("r", encoding="utf-8") as file_obj:
        payload = json.load(file_obj)

    graph_directed = bool(payload.get("directed", directed))
    graph = nx.DiGraph() if graph_directed else nx.Graph()

    for node in payload.get("nodes", []):
        graph.add_node(node)

    for edge in payload.get("edges", []):
        if isinstance(edge, dict):
            source = edge["source"]
            target = edge["target"]
        else:
            source, target = edge
        graph.add_edge(source, target)

    graph.graph["description"] = payload.get("description", "")
    return graph


def generate_graph(
    kind: str = "gnp",
    *,
    nodes: int,
    edge_probability: float,
    directed: bool = True,
    seed: int | None = None,
) -> nx.DiGraph:
    """Generate one graph and normalize it for the platform."""
    match kind:
        case "fast_gnp":
            graph = nx.fast_gnp_random_graph(
                nodes,
                edge_probability,
                seed=seed,
                directed=directed,
            )
        case "gnp":
            graph = nx.gnp_random_graph(
                nodes,
                edge_probability,
                seed=seed,
                directed=directed,
            )
        case _:
            raise ValueError(f"Unsupported graph generator kind: {kind}")

    graph.graph.update(
        {
            "graph_source": "generated",
            "graph_kind": kind,
            "edge_probability": edge_probability,
            "seed": seed if seed is not None else -1,
        }
    )
    return normalize_graph(graph, directed=directed, relabel=False)
