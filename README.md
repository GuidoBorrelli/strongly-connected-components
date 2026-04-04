"""Main module for the Strongly Connected Components project.

This module serves as the entry point for running correctness tests,
performance benchmarks, or memory tests based on configuration settings.
"""

# Strongly Connected Components Algorithms

This repository contains implementations and comparisons of algorithms for finding strongly connected components (SCCs) in directed graphs. It was originally a university project from 2017/2018 for the Advanced Algorithms and Parallel Programming course at Politecnico di Milano.

## Algorithms Implemented

- **Tarjan's Algorithm** (`alg1.py`): A linear-time algorithm for finding SCCs using DFS and a stack.
- **Nuutila's Algorithm** (`alg2.py`): An improved version of Tarjan's algorithm with better space efficiency.
- **Pearce's Algorithm** (`alg3.py`): Another efficient SCC finding algorithm.

## Features

- Correctness testing against NetworkX's built-in SCC finder.
- Performance benchmarking on graphs of varying sizes and densities.
- Memory usage analysis.
- Visualization of small graphs with SCC coloring.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/strongly-connected-components.git
   cd strongly-connected-components
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Tests

To test the correctness of the algorithms:
```bash
python main.py
```

This will run tests on a random graph and verify that all algorithms produce the same SCCs as NetworkX.

### Performance Benchmarking

To run performance benchmarks (this may take time):
1. Set `TEST = False` in `config.py`.
2. Run `python main.py`.

This will generate performance plots in the `graphs/` directory.

### Memory Testing

To test memory usage:
1. Set `MEMORY_TEST = True` in `config.py`.
2. Ensure `GRAPH = True` to generate a test graph first.
3. Run `python main.py` to save the graph.
4. Set `GRAPH = False` and run again to test memory usage.

## Configuration

All settings are in `config.py`:

- `SIZE_BENCHMARK`: Number of graphs to generate for benchmarking (default: 100).
- `TEST`: Run correctness tests if True, benchmarks if False.
- `MEMORY_TEST`: Run memory test instead of correctness test.
- `TEST_NODE_SIZE`: Number of nodes for test graphs.
- `TEST_EDGE_PROBABILITY`: Edge probability for test graphs.
- `DEBUG`: Enable debug output.

## File Organization

### Test Graph Storage
Memory test graphs are stored in `test_graphs/memory_test_graph.pkl` directory with proper `.pkl` extension for pickle-serialized NetworkX graphs. This directory is created automatically and not tracked in version control.

### Output Files
- Performance graphs are saved to `graphs/` directory with `.png` extension
- Graph files use `.pkl` extension (pickle format) for reliable NetworkX graph serialization

## Project Structure

```
strongly-connected-components/
├── algorithms/              # SCC algorithm implementations
│   ├── __init__.py
│   ├── tarjan.py           # Tarjan's algorithm
│   ├── nuutila.py          # Nuutila's algorithm
│   └── pearce.py           # Pearce's algorithm
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── stack.py            # Custom stack implementation
│   ├── benchmarking.py     # Performance benchmarking and plotting
│   └── memory_tests.py     # Memory usage testing
├── tests/                   # Test modules
│   ├── __init__.py
│   └── correctness_tests.py # Correctness testing functions
├── config.py                # Configuration settings
├── main.py                  # Entry point for running tests or benchmarks
├── requirements.txt         # Python dependencies
├── graphs/                  # Directory for performance plot outputs
└── README.md                # This file
```

## Student

Guido Borrelli - 874451
