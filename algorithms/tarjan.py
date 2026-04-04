"""Tarjan's algorithm for finding strongly connected components.

This module implements Tarjan's linear-time algorithm for finding SCCs
in a directed graph using depth-first search and a stack.
"""

from utils import stack as s
from typing import Dict, List
import networkx as nx

DEBUG = False


def apply_alg(graph: nx.DiGraph) -> Dict[int, int]:
    """Apply Tarjan's algorithm to find strongly connected components.

    Args:
        graph: A directed graph represented as a NetworkX DiGraph.

    Returns:
        A dictionary mapping each node to its component representative.
        Nodes in the same SCC have the same representative value.
    """
    DIM_NODES = len(graph)
    current_counter = 0
    stack = s.Stack()
    root: Dict[int, int] = {}
    in_component: Dict[int, bool] = {}
    order: List[int] = [DIM_NODES] * DIM_NODES
    in_component_list: List[bool] = [False] * DIM_NODES

    def visit(v: int) -> None:
        """Recursive DFS visit function for Tarjan's algorithm.

        Args:
            v: The current node being visited.
        """
        if DEBUG:
            print(f"Visiting: {v}")
        nonlocal graph, current_counter, order, stack, root, in_component_list
        root[v] = v
        order[v] = current_counter
        current_counter += 1
        stack.push(v)
        if DEBUG:
            print(f"\tOutgoing edge: {len(graph.out_edges(v))}")
        for out_edge in graph.out_edges(v):
            w = out_edge[1]
            # If the value of node w in the dictionary is still DIM_NODES, not yet visited
            if order[w] == DIM_NODES:
                visit(w)
            if not in_component_list[w]:
                if order[root[v]] > order[root[w]]:
                    root[v] = root[w]

        if root[v] == v:
            while True:
                w = stack.pop()
                in_component_list[w] = True
                # Otherwise I don't have all references of all nodes updated to allow testing, - no side effects
                root[w] = v
                if v == w:
                    break
        return

    for node in graph.nodes:
        # If the value of node w in the dictionary is still DIM_NODES, not yet visited
        if order[node] == DIM_NODES:
            visit(node)
    return root
