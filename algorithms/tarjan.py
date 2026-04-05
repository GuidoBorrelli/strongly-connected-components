"""Tarjan SCC implementation."""

import networkx as nx

from utils.stack import Stack

DEBUG = False

type ComponentMap = dict[int, int]


def apply_alg(graph: nx.DiGraph) -> ComponentMap:
    """Return a mapping from node to SCC representative using Tarjan's algorithm."""
    node_count = graph.number_of_nodes()
    current_counter = 0
    stack: Stack[int] = Stack()
    root: ComponentMap = {}
    order: list[int] = [node_count] * node_count
    in_component: list[bool] = [False] * node_count

    def visit(node: int) -> None:
        nonlocal current_counter

        if DEBUG:
            print(f"Visiting: {node}")

        root[node] = node
        order[node] = current_counter
        current_counter += 1
        stack.push(node)

        if DEBUG:
            print(f"\tOutgoing edge: {len(graph.out_edges(node))}")

        for _, neighbor in graph.out_edges(node):
            if order[neighbor] == node_count:
                visit(neighbor)
            if not in_component[neighbor] and order[root[node]] > order[root[neighbor]]:
                root[node] = root[neighbor]

        if root[node] == node:
            while True:
                member = stack.pop()
                in_component[member] = True
                root[member] = node
                if member == node:
                    break

    for node in graph.nodes:
        if order[node] == node_count:
            visit(node)

    return root
