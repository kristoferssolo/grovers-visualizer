#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from collections.abc import Iterator
from itertools import product
from math import floor, pi, sqrt

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
    """Apply the Grovers diffusion operator."""
    qc.h(range(n))
    qc.x(range(n))
    apply_phase_inversion(qc, n)
    qc.x(range(n))
    qc.h(range(n))


def grover_search(target_state: QubitState, iterations: int | None = None) -> QuantumCircuit:
    """Construct a Grover search circuit for the given target state."""
    n = len(target_state)
    qc = QuantumCircuit(n, n)

    qc.h(range(n))

    if iterations is None or iterations < 0:
        iterations = floor(pi / 4 * sqrt(2**n))

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
    shots = 128
    target = QubitState("1" * 4)
    n_qubits = len(target)

    qc = grover_search(target, iterations=1)
    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots, memory=True)
    result = job.result()
    memory = result.get_memory(qc)  # List of measurement results, one per shot

    print(qc)  # draw scheme

    print(f"Target: {target}")

    # Ensure all possible states are present in the bar chart
    all_states = ["".join(bits) for bits in product("01", repeat=n_qubits)]
    counts = dict.fromkeys(all_states, 0)

    plt.ion()
    _, ax = plt.subplots(figsize=(6, 2))
    bars = ax.bar(all_states, [0] * len(all_states), color="skyblue")
    ax.set_xlabel("Measured State")
    ax.set_ylabel("Counts")
    ax.set_title(f"Measurement Variability for Target: {target}")
    ax.set_ylim(0, shots)

    for i, measured in enumerate(memory, 1):
        measured_be = measured[::-1]  # Qiskit returns little-endian
        counts[measured_be] += 1
        for bar, state in zip(bars, all_states, strict=False):
            bar.set_height(counts[state])
            bar.set_color("orange" if state == str(target) else "skyblue")
        ax.set_title(f"Measurement Variability (Shot {i}/{shots})\nTarget: {target}")
        plt.pause(0.5)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
