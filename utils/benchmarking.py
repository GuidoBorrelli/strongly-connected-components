"""Benchmarking utilities for SCC algorithms."""

from statistics import StatisticsError, mean, variance

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config

DEBUG = config.DEBUG
DIGITS_ACCURACY = config.DIGITS_ACCURACY

type BenchmarkFrames = dict[str, pd.DataFrame]


def extract_statistics(performance_samples: list[float]) -> tuple[float, float]:
    """Extract mean time and variance from performance samples."""
    average = round(mean(performance_samples), DIGITS_ACCURACY)
    try:
        sample_variance = round(variance(performance_samples, average), DIGITS_ACCURACY)
    except StatisticsError:
        sample_variance = 0
    return average * 1000, sample_variance * 1000


def get_values(
    performance_dict: BenchmarkFrames,
    graph_type: str,
) -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray]]:
    """Extract performance values for plotting."""
    tarjan_times = performance_dict["Tarjan"][graph_type]
    nuutila_times = performance_dict["Nuutila"][graph_type]
    pearce_times = performance_dict["Pearce"][graph_type]

    average_series: list[np.ndarray] = []
    variance_series: list[np.ndarray] = []
    tarjan_averages: list[float] = []
    nuutila_averages: list[float] = []
    pearce_averages: list[float] = []
    tarjan_variances: list[float] = []
    nuutila_variances: list[float] = []
    pearce_variances: list[float] = []
    x_values = np.array(tarjan_times.index)

    for index in range(len(tarjan_times.index)):
        tarjan_average, tarjan_variance = extract_statistics(tarjan_times.iloc[index])
        tarjan_averages.append(tarjan_average)
        tarjan_variances.append(tarjan_variance)

        nuutila_average, nuutila_variance = extract_statistics(
            nuutila_times.iloc[index]
        )
        nuutila_averages.append(nuutila_average)
        nuutila_variances.append(nuutila_variance)

        pearce_average, pearce_variance = extract_statistics(pearce_times.iloc[index])
        pearce_averages.append(pearce_average)
        pearce_variances.append(pearce_variance)

    average_series.append(np.array(tarjan_averages))
    variance_series.append(np.array(tarjan_variances))
    average_series.append(np.array(nuutila_averages))
    variance_series.append(np.array(nuutila_variances))
    average_series.append(np.array(pearce_averages))
    variance_series.append(np.array(pearce_variances))
    return x_values, average_series, variance_series


def plot_graph(
    x_values: np.ndarray,
    mean_series: list[np.ndarray],
    variance_series: list[np.ndarray],
    graph_type: str,
) -> None:
    """Plot performance graphs for a specific graph type."""
    colors = ["red", "green", "blue"]
    for index, color in enumerate(colors):
        plt.figure(1)
        plt.plot(
            x_values,
            mean_series[index],
            mfc=color,
            linestyle=":",
            marker="o",
            color=color,
        )
        plt.figure(2)
        plt.plot(
            x_values,
            variance_series[index],
            mfc=color,
            linestyle="-.",
            marker="o",
            color=color,
        )

    plt.figure(1)
    plt.legend(["Tarjan", "Nuutila", "Pearce"], loc="upper left")
    plt.title(f"{graph_type} graph - Mean time")
    plt.xlabel("Number of nodes")
    plt.ylabel("Mean time [ms]")
    plt.ylim(0)

    plt.figure(2)
    plt.legend(["Tarjan", "Nuutila", "Pearce"], loc="upper left")
    plt.title(f"{graph_type} graph - Variance")
    plt.xlabel("Number of nodes")
    plt.ylabel("Variance")
    plt.ylim(0)

    plt.figure(1)
    plt.savefig(f"./graphs/{graph_type}-results.png")
    plt.figure(2)
    plt.savefig(f"./graphs/{graph_type}-variance.png")
    plt.show()


def plot_result(performance_dict: BenchmarkFrames) -> None:
    """Generate performance plots for all graph types."""
    sparse_values = get_values(performance_dict, "Sparse")
    medium_values = get_values(performance_dict, "Medium")
    dense_values = get_values(performance_dict, "Dense")

    plot_graph(*sparse_values, "Sparse")
    plot_graph(*medium_values, "Medium")
    plot_graph(*dense_values, "Dense")
