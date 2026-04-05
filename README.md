# Strongly Connected Components

This repository compares three algorithms for finding strongly connected components (SCCs) in directed graphs:

- Tarjan in `algorithms/tarjan.py`
- Nuutila in `algorithms/nuutila.py`
- Pearce in `algorithms/pearce.py`

It started as a 2017/2018 Politecnico di Milano course project and now serves as a small test and benchmarking harness built on NetworkX.

## Python Target

This repository now targets Python 3.14 only.

- Local development is pinned to Python 3.14.3 in `.python-version`
- CI runs on the latest available Python 3.14 patch release
- Dependency floors in `requirements.txt` were raised to versions known to support the 3.14 target
- Python versions earlier than 3.14 are unsupported and should be considered deprecated for this repository

## Quick Start

```bash
git clone https://github.com/GuidoBorrelli/strongly-connected-components.git
cd strongly-connected-components
conda create -n scc python=3.14.3 -y
conda activate scc
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p 'test_*.py'
python main.py
```

`python main.py` still runs the repository's correctness harness and now exits non-zero if any implementation disagrees with `networkx.strongly_connected_components`.

## Platform Layers

The repository now includes a small graph algorithms platform around the SCC implementations:

- `algorithms/registry.py`: algorithm metadata, registry lookup, and normalized results
- `graph_io/loaders.py`: reusable graph file loaders and generated graph helpers
- `benchmarks/`: reproducible benchmark suites plus CSV/JSON export
- `notebooks/`: tutorial notebooks that reuse the same library code

## Run Modes

All runtime switches live in `config.py`.

- Correctness check: `TEST = True`, `MEMORY_TEST = False`
- Benchmarks and plots: `TEST = False`
  - writes `runs.csv`, `summary.csv`, and `metadata.json` to `results/`
- Memory test:
  1. Set `TEST = True`, `MEMORY_TEST = True`, `GRAPH = True`
  2. Run `python main.py` once to create `test_graphs/memory_test_graph.pkl`
  3. Set `GRAPH = False`
  4. Choose `ALG_TEST` (`1` Pearce, `2` Nuutila, `3` Tarjan)
  5. Run `python main.py` again

Benchmark plots are written to `graphs/`.

## Test Suite

- Automated tests: `python -m unittest discover -s tests -p 'test_*.py'`
- CLI smoke test: `python main.py`
- Platform tests cover the registry, graph loaders, benchmark export, and SCC correctness

## Examples

Curated input graphs are available under `data/examples/`.

```python
from algorithms.registry import list_algorithms, run_algorithm
from graph_io.examples import load_example_graph

graph = load_example_graph("two_sccs")
print([algorithm.key for algorithm in list_algorithms(category="scc")])
result = run_algorithm("tarjan", graph)
print(result.component_count)
```

## Project Layout

```text
algorithms/   SCC implementations
benchmarks/   suites, runner, and export helpers
data/         curated example graphs
graph_io/     file loaders and generated graph helpers
notebooks/    tutorial notebooks
tests/        correctness helpers and unit tests
utils/        benchmarking, memory tests, and stack utilities
config.py     runtime configuration
main.py       entry point
docs/         extra notes on algorithms and GitHub Actions
graphs/       sample benchmark outputs
```

## Notes

- The implementations expect directed NetworkX graphs whose nodes are integer-labeled from `0` to `n - 1`.
- Use `graph_io.loaders.load_graph(..., relabel=True)` for file-based inputs that do not already satisfy that constraint.
- Benchmarking imports NumPy directly, so it is listed explicitly in `requirements.txt`.
- Detailed algorithm notes are in `docs/ALGORITHMS.md`.
- GitHub Actions setup notes are in `docs/GITHUB_ACTIONS_SETUP.md`.
- Contribution guidelines are in `CONTRIBUTING.md`.
