#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from itertools import product

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def grover_search(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n, n)

    qc.h(range(n))

    qc.measure(range(n), range(n))
    return qc


def plot_counts(ax: Axes, counts: dict[str, int], target_state: str) -> None:
    """Create and display a bar chart for the measurement results.

    Parameters:
      counts       - A dictionary mapping output states to counts.
      target_state - The target state used in the Grover circuit.
    """
    # Sort the states (optional: you can sort by state or by count)
    states = list(counts.keys())
    frequencies = [counts[s] for s in states]

    ax.clear()
    ax.bar(states, frequencies, color="skyblue")
    ax.set_xlabel("Measured State")
    ax.set_ylabel("Counts")
    ax.set_title(f"Measurement Counts for Target: {target_state}")
    ax.set_ylim(0, max(frequencies) * 1.2)


def main() -> None:
    n_qubits = 3
    combinations = product(["0", "1"], repeat=n_qubits)
    states = ["".join(x) for x in combinations]
    shots = 1024

    _, ax = plt.subplots(figsize=(8, 4))
    plt.ion()

    for state in states:
        qc = grover_search(n_qubits)

        print(qc.draw("text"))

        simulator = AerSimulator()
        job = simulator.run(qc, shots=shots)
        result = job.result()
        counts: dict[str, int] = result.get_counts(qc)
        sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

        print(f"Target: {state}")
        print("\n".join(f"'{k}': {v}" for k, v in sorted_counts.items()))

        plot_counts(ax, sorted_counts, state)
        plt.pause(1)

    # plt.ioff()  # Do not close automatically
    plt.show()


if __name__ == "__main__":
    main()
