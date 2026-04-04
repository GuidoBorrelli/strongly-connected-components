"""Nuutila's algorithm for finding strongly connected components.

This module implements Nuutila's improved version of Tarjan's algorithm,
which has better space complexity characteristics.
"""

from utils import stack as s
from typing import Dict, List
import networkx as nx

DEBUG = False


def apply_alg(graph: nx.DiGraph) -> Dict[int, int]:
    """Apply Nuutila's algorithm to find strongly connected components.

    Args:
        graph: A directed graph represented as a NetworkX DiGraph.

    Returns:
        A dictionary mapping each node to its component representative.
        Nodes in the same SCC have the same representative value.
    """
    DIM_NODES = len(graph)
    current_counter = 0
    stack = s.Stack()
    stack.push(-1)
    root: Dict[int, int] = {}
    in_component_list: List[bool] = [False] * DIM_NODES
    order: List[int] = [DIM_NODES] * DIM_NODES

    def visit(v: int) -> None:
        """Recursive DFS visit function for Nuutila's algorithm.

        Args:
            v: The current node being visited.
        """
        if DEBUG:
            print(f"Visiting: {v}")
        nonlocal current_counter, order, stack, root, graph, in_component_list
        root[v] = v
        order[v] = current_counter
        current_counter += 1
        in_component_list[v] = False
        for out_edge in graph.out_edges(v):
            w = out_edge[1]
            if order[w] == DIM_NODES:
                visit(w)
            if not in_component_list[root[w]]:
                if order[root[v]] > order[root[w]]:
                    root[v] = root[w]
        if root[v] == v:
            if stack.peek() > -1 and order[stack.peek()] >= order[v]:
                while stack.peek() > -1 and order[stack.peek()] >= order[v]:
                    w = stack.pop()
                    in_component_list[w] = True
                    root[w] = v
            else:
                in_component_list[v] = True
        elif not stack.contains(root[v]):
            stack.push(root[v])
        return

    for node in graph.nodes:
        # If the value of node w in the dictionary is still DIM_NODES, not yet visited
        if order[node] == DIM_NODES:
            visit(node)

    # Due to let me test the results, I need to store all component reference of all nodes like in the other alg
    def update(i: int) -> None:
        """Update function to flatten the component tree."""
        nonlocal root
        if root[i] != root[root[i]]:
            update(root[i])
            root[i] = root[root[i]]

    for i in root:
        update(i)
    return root
