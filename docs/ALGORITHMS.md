# Algorithm Documentation

## Overview

This document provides detailed information about the three SCC (Strongly Connected Components) algorithms implemented in this project.

All implementations in this repository expect directed NetworkX graphs whose nodes are labeled with consecutive integers from `0` to `n - 1`.
The repository now targets Python 3.14 only.
Python versions earlier than 3.14 are unsupported for this codebase.

## Tarjan's Algorithm

### Description
Tarjan's algorithm is a linear-time depth-first search (DFS) based algorithm that finds all SCCs in a single pass through the graph.

### Key Characteristics
- **Time Complexity**: O(V + E) where V = vertices, E = edges
- **Space Complexity**: O(V)
- **Approach**: DFS with a stack-based approach
- **Root Reference Updates**: Yes, updates all node references to their component representative

### How It Works
1. Start DFS from an unvisited node
2. Maintain a stack of nodes in the current path
3. Track the "order" of discovery for each node
4. Update root references to the lowest-order reachable node
5. When a root node is found (root[v] == v), pop all nodes from stack until reaching v
6. Mark all popped nodes as belonging to the same SCC

### Implementation File
`algorithms/tarjan.py`

### References
- Tarjan, R. E. (1972). "Depth-first search and linear graph algorithms"

---

## Nuutila's Algorithm

### Description
Nuutila's algorithm is an improved version of Tarjan's algorithm with better space efficiency and different handling of strongly connected components.

### Key Characteristics
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V) with better constant factors than Tarjan
- **Approach**: DFS with sentinel stack element optimization
- **Difference from Tarjan**: Uses a sentinel (-1) in the stack for cleaner termination

### How It Works
1. Similar to Tarjan but uses a sentinel stack element
2. When root[v] == v and stack.peek() > -1, pop elements with order >= order[v]
3. Mark those elements as in a component
4. Different stack management strategy reduces special cases
5. Includes a path compression step at the end to update all node references

### Implementation File
`algorithms/nuutila.py`

### Key Optimization
The sentinel value (-1) eliminates edge cases in stack management, making the algorithm cleaner and sometimes faster in practice.

---

## Pearce's Algorithm

### Description
Pearce's PEA_FIND_SSC2 algorithm is another efficient method for finding SCCs, using a different indexing approach.

### Key Characteristics
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Approach**: DFS with incremental indexing
- **Index Assignment**: Assigns indices to nodes in reverse topological order of SCCs

### How It Works
1. Initialize rindex (reverse index) to 0 for all nodes
2. For each unvisited node, perform DFS
3. Assign incrementing indices during traversal
4. Track root status (whether node is root of SCC)
5. For root nodes, assign components by decrementing counter
6. Use stack to hold non-root nodes for later SCC assignment
7. Return mapping of nodes to component indices

### Implementation File
`algorithms/pearce.py`

### Unique Aspect
This algorithm assigns component IDs in descending order, which can be useful for specific applications where reverse topological ordering is needed.

---

## Comparison Table

| Aspect | Tarjan | Nuutila | Pearce |
|--------|--------|---------|--------|
| **Time Complexity** | O(V + E) | O(V + E) | O(V + E) |
| **Space Complexity** | O(V) | O(V) | O(V) |
| **Stack Management** | Standard | With sentinel | Using rindex |
| **Practical Speed** | Very Fast | Very Fast | Fast |
| **Memory Usage** | Moderate | Low | Moderate |
| **Code Complexity** | Medium | Medium | Medium |
| **Easiest to Understand** | Yes | With explanation | No |

---

## Testing Correctness

All three algorithms are tested for correctness by:
1. Building deterministic and seeded random directed graphs
2. Running all three algorithms
3. Comparing their SCC partitions with NetworkX's built-in `strongly_connected_components()`
4. Verifying that the repository's CLI harness still exits cleanly in correctness mode

Run tests with:
```bash
python -m unittest discover -s tests -p 'test_*.py'
python main.py  # with TEST=True in config.py and Python 3.14
```

---

## Performance Benchmarking

Performance is measured on graphs of different sizes and densities:
- **Sizes**: 50, 100, 200, 600 nodes
- **Densities**:
  - Sparse: p = 1/n
  - Medium: p = 3/n
  - Dense: p = 1/(n^0.1)

Run benchmarks with:
```bash
python main.py  # with TEST=False in config.py and Python 3.14
```

Results are plotted in `graphs/` directory.

---

## Memory Analysis

Memory usage is tracked using the `psutil` library:
1. Generate a test graph
2. Record baseline memory usage
3. Run algorithm
4. Measure memory usage after algorithm completes
5. Calculate increment and percentage increase

Run memory tests with:
```bash
python main.py  # with MEMORY_TEST=True in config.py and Python 3.14
```

---

## Choosing an Algorithm

### Use Tarjan if:
- You need a well-tested, widely understood algorithm
- You want an educational implementation
- Readability is a priority

### Use Nuutila if:
- You want slightly better memory efficiency
- You prefer cleaner stack management
- You need production-grade performance

### Use Pearce if:
- You need SCCs ordered in a specific topological manner
- You're benchmarking alternative approaches
- You're studying algorithm variations

---

## References

1. Tarjan, R. E. (1972). "Depth-first search and linear graph algorithms." SIAM Journal on Computing, 1(2), 146-160.

2. Nuutila, E., & Soisalon-Soininen, E. (1994). "On finding the strongly connected components in a directed graph." Information Processing Letters, 49(1), 9-14.

3. Pearce, D. J. (2005). "A space-efficient algorithm for computing strongly connected components." Information Processing Letters, 83(5), 231-235.

4. NetworkX Documentation: https://networkx.org/

5. Graph Theory - Stanford Encyclopedia: https://plato.stanford.edu/entries/logic-graphs/
