# Configuration file for strongly connected components project

"""Configuration settings for the SCC project.

This module contains all configurable parameters used throughout the project,
including test settings, benchmarking parameters, and debug options.
"""

# Main settings
SIZE_BENCHMARK = 100  # Reduced for faster testing, original was 10000
TEST = True
MEMORY_TEST = False
TEST_NODE_SIZE = 50
TEST_EDGE_PROBABILITY = 0.05

# Debug settings
DEBUG = False
DIGITS_ACCURACY = 8

# Benchmark export settings
BENCHMARK_OUTPUT_DIR = "results"
BENCHMARK_SUITE_NAME = "scc-default"
BENCHMARK_BASE_SEED = 0

# Memory test settings
GRAPH = False
ALG_TEST = 1
