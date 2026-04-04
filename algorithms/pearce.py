from utils import stack as s
from typing import Dict, List
import networkx as nx

DEBUG = False


# Perform and evaluate PEA_FIND_SSC2 algorithm
def apply_alg(graph: nx.DiGraph) -> Dict[int, int]:
    stack = s.Stack()
    index = 1
    c = graph.number_of_nodes() - 1
    rindex: Dict[int, int] = {}

    def visit(v: int) -> None:
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
