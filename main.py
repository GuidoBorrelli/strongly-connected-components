"""Entry point for correctness checks, benchmarks, and memory tests."""

import config
from benchmarks.exporters import export_benchmark_results
from benchmarks.runner import run_benchmark_suite
from benchmarks.suites import build_default_scc_suite
from tests import correctness_tests
from utils import benchmarking, memory_tests

SIZE_BENCHMARK = config.SIZE_BENCHMARK
TEST = config.TEST
MEMORY_TEST = config.MEMORY_TEST
TEST_NODE_SIZE = config.TEST_NODE_SIZE
TEST_EDGE_PROBABILITY = config.TEST_EDGE_PROBABILITY
DEBUG = config.DEBUG
BENCHMARK_OUTPUT_DIR = config.BENCHMARK_OUTPUT_DIR
BENCHMARK_SUITE_NAME = config.BENCHMARK_SUITE_NAME
BENCHMARK_BASE_SEED = config.BENCHMARK_BASE_SEED


def run_benchmarks() -> int:
    """Run the default SCC benchmark suite, export results, and generate plots."""
    print("Start")
    benchmark_cases = build_default_scc_suite()
    run_records, summary_records, metadata = run_benchmark_suite(
        benchmark_cases,
        repeat_count=SIZE_BENCHMARK,
        suite_name=BENCHMARK_SUITE_NAME,
        base_seed=BENCHMARK_BASE_SEED,
    )
    export_dir = export_benchmark_results(
        run_records,
        summary_records,
        metadata,
        output_root=BENCHMARK_OUTPUT_DIR,
    )
    benchmarking.plot_summary(summary_records)
    if DEBUG:
        print(f"Exported {len(run_records)} benchmark runs.")
    print(f"Benchmark export written to {export_dir}")
    print("End")
    return 0


def main() -> int:
    """Run the selected repository mode and return an exit status."""
    if not TEST:
        return run_benchmarks()

    if MEMORY_TEST:
        try:
            return memory_tests.memory_test()
        except (FileNotFoundError, ValueError) as error:
            print(error)
            return 1

    results = correctness_tests.test_algorithms(TEST_NODE_SIZE, TEST_EDGE_PROBABILITY)
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
