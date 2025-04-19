#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from grovers_visualizer.state import QubitState


def x(qc: QuantumCircuit, target_state: QubitState) -> None:
    for i, bit in enumerate(reversed(target_state)):
        if bit == "0":
            qc.x(i)


def ccz(qc: QuantumCircuit, n: int) -> None:
    """Multi-controlled Z (for 3 qubits, this is a CCZ)"""
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.cz(0, 1)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)  # multi-controlled X (Toffoli for 3 qubits)
        qc.h(n - 1)


def oracle(qc: QuantumCircuit, target_state: QubitState) -> None:
    n = len(target_state)

    x(qc, target_state)

    ccz(qc, n)

    # Undo the X gates
    x(qc, target_state)


def diffusion(qc: QuantumCircuit, n: int) -> None:
    """Apply the Grovers diffusion operator"""

    qc.h(range(n))
    qc.x(range(n))

    ccz(qc, n)

    qc.x(range(n))
    qc.h(range(n))


def grover_search(n: int, target_state: QubitState) -> QuantumCircuit:
    qc = QuantumCircuit(n, n)

    qc.h(range(n))

    num_states = 2**n

    iterations = int(np.floor(np.pi / 4 * np.sqrt(num_states)))
    for _ in range(iterations):
        oracle(qc, target_state)
        diffusion(qc, n)

    qc.measure(range(n), range(n))
    return qc


def plot_counts(ax: Axes, counts: dict[str, int], target_state: str) -> None:
    """Create and display a bar chart for the measurement results."""

    # Sort the states
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
        qc = grover_search(n_qubits, QubitState(state))

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

    plt.show()


if __name__ == "__main__":
    main()
