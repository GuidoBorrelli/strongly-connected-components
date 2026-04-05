"""Benchmark plotting utilities built on exported benchmark summaries."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from benchmarks.runner import BenchmarkSummaryRecord


def summary_frame(summary_records: list[BenchmarkSummaryRecord]) -> pd.DataFrame:
    """Convert benchmark summary records into a DataFrame."""
    return pd.DataFrame([record.to_row() for record in summary_records])


def plot_summary(
    summary_records: list[BenchmarkSummaryRecord],
    *,
    output_dir: str | Path = "graphs",
) -> pd.DataFrame:
    """Plot mean time and variance for each density class from summary records."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary = summary_frame(summary_records)
    colors = {"Tarjan": "red", "Nuutila": "green", "Pearce": "blue"}

    for density_label in ("Sparse", "Medium", "Dense"):
        subset = summary[summary["density_label"] == density_label].sort_values(
            ["node_count", "algorithm_name"]
        )

        plt.figure(1)
        plt.clf()
        plt.figure(2)
        plt.clf()

        for algorithm_name, color in colors.items():
            algorithm_subset = subset[subset["algorithm_name"] == algorithm_name]
            plt.figure(1)
            plt.plot(
                algorithm_subset["node_count"],
                algorithm_subset["mean_runtime_milliseconds"],
                mfc=color,
                linestyle=":",
                marker="o",
                color=color,
            )
            plt.figure(2)
            plt.plot(
                algorithm_subset["node_count"],
                algorithm_subset["variance_runtime_milliseconds"],
                mfc=color,
                linestyle="-.",
                marker="o",
                color=color,
            )

        plt.figure(1)
        plt.legend(list(colors), loc="upper left")
        plt.title(f"{density_label} graph - Mean time")
        plt.xlabel("Number of nodes")
        plt.ylabel("Mean time [ms]")
        plt.ylim(0)
        plt.savefig(output_path / f"{density_label}-results.png")

        plt.figure(2)
        plt.legend(list(colors), loc="upper left")
        plt.title(f"{density_label} graph - Variance")
        plt.xlabel("Number of nodes")
        plt.ylabel("Variance [ms]")
        plt.ylim(0)
        plt.savefig(output_path / f"{density_label}-variance.png")

    return summary
