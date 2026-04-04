"""Pearce's algorithm for finding strongly connected components.

This module implements Pearce's PEA_FIND_SSC2 algorithm, an efficient
method for finding SCCs in directed graphs.
"""

from utils import stack as s
from typing import Dict, List
import networkx as nx

DEBUG = False


def apply_alg(graph: nx.DiGraph) -> Dict[int, int]:
    """Apply Pearce's algorithm to find strongly connected components.

    Args:
        graph: A directed graph represented as a NetworkX DiGraph.

    Returns:
        A dictionary mapping each node to its component representative.
        Nodes in the same SCC have the same representative value.
    """
    stack = s.Stack()
    index = 1
    c = graph.number_of_nodes() - 1
    rindex: Dict[int, int] = {}

    def visit(v: int) -> None:
        """Recursive visit function for Pearce's algorithm.

        Args:
            v: The current node being visited.
        """
        nonlocal graph, stack, index, c, rindex
        if DEBUG:
            print(f"Visiting: {v}")
        root = True
        rindex[v] = index
        index += 1
        if DEBUG:
            print(f"\tOutgoing edge: {len(graph.out_edges(v))}")
        for out_edge in graph.out_edges(v):
            w = out_edge[1]
            if rindex[w] == 0:
                visit(w)
            if rindex[w] < rindex[v]:
                rindex[v] = rindex[w]
                root = False
        if root:
            index -= 1
            while (not stack.isEmpty()) and rindex[v] <= rindex[stack.peek()]:
                w = stack.pop()
                rindex[w] = c
                index -= 1
            rindex[v] = c
            c -= 1
        else:
            stack.push(v)
        return

    for node in graph.nodes:
        rindex[node] = 0
    for node in graph.nodes:
        if rindex[node] == 0:
            visit(node)
    return rindex
