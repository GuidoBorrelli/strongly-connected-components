# A reproducible small benchmark

This is an executed example of the measurement pipeline, using generated graphs only. It is intended to make the experiment inspectable, not to establish a universal algorithm ranking.

## Recorded run

- Date: 14 November 2026 (UTC timestamp in the metadata).
- Runtime: Python 3.14.3, macOS arm64; exact platform and package versions are recorded in [metadata.json](benchmarks/portfolio-small/metadata.json).
- Algorithm/runner source: [9f9d062](https://github.com/GuidoBorrelli/strongly-connected-components/tree/9f9d06275c7f5b73daf2d74810f976329bbc610e); the portfolio changes do not alter those implementations.
- Inputs: 50 and 100 nodes at each of three edge probabilities: `1/n`, `3/n`, and `1/(n**0.1)`.
- Sampling: five independently seeded graph instances per case, starting from seed 42. Each instance is shared by all three algorithms.
- Output: **90 timed executions**, **18 summary rows**. All 30 generated graph instances were additionally checked against NetworkX for all three algorithms, outside the timed measurements.

Mean milliseconds per execution:

| Case | Pearce | Nuutila | Tarjan |
| --- | ---: | ---: | ---: |
| dense-100 | 2.132 | 2.631 | 2.321 |
| dense-50 | 0.530 | 0.538 | 0.363 |
| medium-100 | 0.724 | 0.633 | 0.590 |
| medium-50 | 0.190 | 0.168 | 0.268 |
| sparse-100 | 0.944 | 0.209 | 0.282 |
| sparse-50 | 0.287 | 0.280 | 0.186 |

Inspect [all raw runs](benchmarks/portfolio-small/runs.csv), [unrounded summaries](benchmarks/portfolio-small/summary.csv), and [metadata](benchmarks/portfolio-small/metadata.json). The observed means range from approximately 0.168 to 2.631 ms. That range describes this run only.

## Reproduce

From the repository root in the documented Python 3.14 environment:

```bash
python - <<'PY'
from benchmarks.exporters import export_benchmark_results
from benchmarks.runner import run_benchmark_suite
from benchmarks.suites import build_default_scc_suite

runs, summaries, metadata = run_benchmark_suite(
    build_default_scc_suite(node_counts=(50, 100)),
    repeat_count=5,
    suite_name="portfolio-small",
    base_seed=42,
)
output = export_benchmark_results(runs, summaries, metadata)
print(f"{len(runs)} runs; {len(summaries)} summaries; {output}")
PY
```

On Windows, execute the Python body in a Python session or save it to a script; the shell heredoc syntax above is for Bash/Zsh. New runs are written to unique directories under `results/` and do not overwrite this recorded sample.

For the recorded direct dependency versions, install `networkx==3.6.1 numpy==2.4.4 pandas==3.0.2 matplotlib==3.10.8 psutil==7.2.2`. This is not a complete transitive dependency lock; interpreter, operating system and dependencies can still affect results.

## How to read the results

- Timing begins before registry validation and ends after component counting. It includes those costs and excludes graph generation and export.
- A repeat is a new seeded graph, not repeated execution of one identical graph. The mean combines variation in graph structure and runtime noise.
- Algorithm order is fixed (Pearce, Nuutila, Tarjan), without warm-up or CPU isolation. Small measurements are sensitive to scheduling and cache effects. Five repeats do not support strong statistical performance claims.
- `component_count` in each summary is the **last repeat's** count; use raw rows for per-graph counts. `avg_edge_count` and `avg_density` are averages across repeats.
- Variance columns use squared units. The conversion from seconds² to milliseconds² is a factor of 1,000,000.
- No memory ranking follows from these timing results. The separate RSS experiment measures a post-execution delta, not peak allocations.

A larger performance study should randomize execution order, define warm-up, repeat fixed inputs as well as graph samples, measure peak memory separately, and include graphs close to the recursion limit. Those changes are outside this small presentation update.
