#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from itertools import product
from math import floor, pi, sqrt
from typing import Iterator

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from grovers_visualizer.gates import apply_phase_inversion, encode_target_state
from grovers_visualizer.state import QubitState


def oracle(qc: QuantumCircuit, target_state: QubitState) -> None:
    """Oracle that flips the sign of the target state."""
    n = len(target_state)
    encode_target_state(qc, target_state)
    apply_phase_inversion(qc, n)
    encode_target_state(qc, target_state)  # Undo


def diffusion(qc: QuantumCircuit, n: int) -> None:
    """Apply the Grovers diffusion operator"""
    qc.h(range(n))
    qc.x(range(n))
    apply_phase_inversion(qc, n)
    qc.x(range(n))
    qc.h(range(n))


def grover_search(n: int, target_state: QubitState) -> QuantumCircuit:
    """Construct a Grover search circuit for the given target state."""
    qc = QuantumCircuit(n, n)

    qc.h(range(n))

    num_states = 2**n

    iterations = floor(pi / 4 * sqrt(num_states))
    for _ in range(iterations):
        oracle(qc, target_state)
        diffusion(qc, n)

    qc.measure(range(n), range(n))
    return qc


def plot_counts(ax: Axes, counts: dict[str, int], target_state: QubitState) -> None:
    """Display a bar chart for the measurement results."""

    # Sort the states
    states = list(counts.keys())
    frequencies = [counts[s] for s in states]

    ax.clear()
    ax.bar(states, frequencies, color="skyblue")
    ax.set_xlabel("Measured State")
    ax.set_ylabel("Counts")
    ax.set_title(f"Measurement Counts for Target: {target_state}")
    ax.set_ylim(0, max(frequencies) * 1.2)


def all_states(n_qubits: int) -> Iterator[QubitState]:
    """Generate all possible QubitStates for n_qubits."""
    for bits in product("01", repeat=n_qubits):
        yield QubitState("".join(bits))


def main() -> None:
    n_qubits = 3
    shots = 1024

    _, ax = plt.subplots(figsize=(8, 4))
    plt.ion()

    for state in all_states(n_qubits):
        qc = grover_search(n_qubits, state)

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
