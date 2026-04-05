"""Benchmarking utilities for SCC algorithms.

This module provides functions for statistical analysis of algorithm performance
and visualization of results through plots.
"""

import matplotlib.pyplot as plt
from statistics import mean, variance, StatisticsError
import numpy as np
import config

DEBUG = config.DEBUG
DIGITS_ACCURACY = config.DIGITS_ACCURACY


def extract_statistics(perf_list: list) -> tuple:
    """Extract statistical measures from performance data.

    Args:
        perf_list: List of performance measurements (execution times).

    Returns:
        Tuple of (mean_time, variance) in milliseconds.
    """
    avg = round(mean(perf_list), DIGITS_ACCURACY)
    try:
        var = round(variance(perf_list, avg), DIGITS_ACCURACY)
    except StatisticsError:
        var = 0
    return avg * 1000, var * 1000


def get_values(performance_dict: dict, graph_type: str) -> tuple:
    """Extract performance values for plotting.

    Args:
        performance_dict: Dictionary containing performance data for all algorithms.
        graph_type: Type of graph ('Sparse', 'Medium', or 'Dense').

    Returns:
        Tuple of (x_values, y_values, error_values) for plotting.
    """
    tarjan_times = performance_dict['Tarjan'][graph_type]
    nuutila_times = performance_dict['Nuutila'][graph_type]
    pearce_times = performance_dict['Pearce'][graph_type]
    y, e = [], []
    e_0, e_1, e_2 = [], [], []
    y_0, y_1, y_2 = [], [], []
    x = np.array(tarjan_times.index)
    # Fill performance of each algorithm
    for i in range(0, len(tarjan_times.index)):
        avg_1, var_1 = extract_statistics(tarjan_times.iloc[i])
        y_0.append(avg_1)
        e_0.append(var_1)
        avg_2, var_2 = extract_statistics(nuutila_times.iloc[i])
        y_1.append(avg_2)
        e_1.append(var_2)
        avg_3, var_3 = extract_statistics(pearce_times.iloc[i])
        y_2.append(avg_3)
        e_2.append(var_3)
    # Merge in a single list of lists algorithms' performance
    y.append(np.array(y_0))
    e.append(np.array(e_0))
    y.append(np.array(y_1))
    e.append(np.array(e_1))
    y.append(np.array(y_2))
    e.append(np.array(e_2))
    return x, y, e


def plot_graph(x, y, e, graph_type: str):
    """Plot performance graphs for a specific graph type.

    Args:
        x: X-axis values (node counts).
        y: Y-axis values (mean times for each algorithm).
        e: Error values (variances for each algorithm).
        graph_type: Type of graph being plotted.
    """
    # One color per each algorithm
    colors = ['red', 'green', 'blue']
    for k in range(3):
        plt.figure(1)
        plt.plot(x, y[k], mfc=colors[k], linestyle=':', marker='o', color=colors[k])
        plt.figure(2)
        plt.plot(x, e[k], mfc=colors[k], linestyle='-.', marker='o', color=colors[k])
    plt.figure(1)
    plt.legend(['Tarjan', 'Nuutila', 'Pearce'], loc='upper left')
    plt.title(f"{graph_type} graph - Mean time")
    plt.xlabel('Number Of Nodes')
    plt.ylabel('Mean time value [millisecs]')
    plt.ylim(0)
    plt.figure(2)
    plt.legend(['Tarjan', 'Nuutila', 'Pearce'], loc='upper left')
    plt.title(f"{graph_type} graph - Variance")
    plt.xlabel('Number Of Nodes')
    plt.ylabel('Variance')
    plt.ylim(0)
    plt.figure(1)
    plt.savefig(f"./graphs/{graph_type}-results.png")
    plt.figure(2)
    plt.savefig(f"./graphs/{graph_type}-variance.png")
    plt.show()
    return


def plot_result(performance_dict: dict):
    """Generate performance plots for all graph types.

    Args:
        performance_dict: Dictionary containing performance data for all algorithms
                         and graph types.
    """
    # This function let get data in a format useful to plot
    x_sp, y_sp, e_sp = get_values(performance_dict, 'Sparse')
    x_md, y_md, e_md = get_values(performance_dict, 'Medium')
    x_de, y_de, e_de = get_values(performance_dict, 'Dense')
    # This function plot the data for each category
    plot_graph(x_sp, y_sp, e_sp, 'Sparse')
    plot_graph(x_md, y_md, e_md, 'Medium')
    plot_graph(x_de, y_de, e_de, 'Dense')
    return
