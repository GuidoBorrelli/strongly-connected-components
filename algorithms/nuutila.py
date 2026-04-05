"""Nuutila SCC implementation."""

import networkx as nx

from utils.stack import Stack

DEBUG = False

type ComponentMap = dict[int, int]


def apply_alg(graph: nx.DiGraph) -> ComponentMap:
    """Return a mapping from node to SCC representative using Nuutila's algorithm."""
    node_count = graph.number_of_nodes()
    current_counter = 0
    stack: Stack[int] = Stack()
    stack.push(-1)
    root: ComponentMap = {}
    in_component: list[bool] = [False] * node_count
    order: list[int] = [node_count] * node_count

    def visit(node: int) -> None:
        nonlocal current_counter

        if DEBUG:
            print(f"Visiting: {node}")

        root[node] = node
        order[node] = current_counter
        current_counter += 1
        in_component[node] = False

        for _, neighbor in graph.out_edges(node):
            if order[neighbor] == node_count:
                visit(neighbor)
            if (
                not in_component[root[neighbor]]
                and order[root[node]] > order[root[neighbor]]
            ):
                root[node] = root[neighbor]

        if root[node] == node:
            while stack.peek() > -1 and order[stack.peek()] >= order[node]:
                member = stack.pop()
                in_component[member] = True
                root[member] = node
            in_component[node] = True
        elif not stack.contains(root[node]):
            stack.push(root[node])

    for node in graph.nodes:
        if order[node] == node_count:
            visit(node)

    def compress_path(node: int) -> None:
        if root[node] != root[root[node]]:
            compress_path(root[node])
            root[node] = root[root[node]]

    for node in root:
        compress_path(node)

    return root
