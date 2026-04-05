"""Pearce SCC implementation."""

import networkx as nx

from utils.stack import Stack

DEBUG = False

type ComponentMap = dict[int, int]


def apply_alg(graph: nx.DiGraph) -> ComponentMap:
    """Return a mapping from node to SCC index using Pearce's algorithm."""
    stack: Stack[int] = Stack()
    index = 1
    component_index = graph.number_of_nodes() - 1
    reverse_index: ComponentMap = {node: 0 for node in graph.nodes}

    def visit(node: int) -> None:
        nonlocal index, component_index

        if DEBUG:
            print(f"Visiting: {node}")

        is_root = True
        reverse_index[node] = index
        index += 1

        if DEBUG:
            print(f"\tOutgoing edge: {len(graph.out_edges(node))}")

        for _, neighbor in graph.out_edges(node):
            if reverse_index[neighbor] == 0:
                visit(neighbor)
            if reverse_index[neighbor] < reverse_index[node]:
                reverse_index[node] = reverse_index[neighbor]
                is_root = False

        if is_root:
            index -= 1
            while (
                not stack.is_empty()
                and reverse_index[node] <= reverse_index[stack.peek()]
            ):
                member = stack.pop()
                reverse_index[member] = component_index
                index -= 1
            reverse_index[node] = component_index
            component_index -= 1
        else:
            stack.push(node)

    for node in graph.nodes:
        if reverse_index[node] == 0:
            visit(node)

    return reverse_index
