#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from math import asin, sqrt
from typing import TYPE_CHECKING, Callable

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from grovers_visualizer.circuit import diffusion, oracle
from grovers_visualizer.plot import draw_grover_circle, plot_amplitudes_live
from grovers_visualizer.state import QubitState
from grovers_visualizer.utils import all_states, optimal_grover_iterations

if TYPE_CHECKING:
    from matplotlib.figure import Figure


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


def main() -> None:
    target_state = QubitState("1010")
    n_qubits = len(target_state)
    basis_states = [str(bit) for bit in all_states(n_qubits)]
    optimal_iterations = optimal_grover_iterations(n_qubits)
    theta = 2 * asin(1 / sqrt(2**n_qubits))
    state_angle = 0.5 * theta

    plt.ion()
    fig: Figure
    ax_bar: Axes
    ax_circle: Axes
    fig, (ax_bar, ax_circle) = plt.subplots(1, 2, figsize=(12, 4))
    bars = ax_bar.bar(basis_states, [0] * len(basis_states), color="skyblue")
    ax_bar.set_ylim(-1, 1)
    ax_bar.set_title("Amplitudes (example)")

    def iterate_and_plot(
        operation: Callable[[QuantumCircuit], None] | None,
        step_label: str,
        iteration: int,
    ) -> None:
        if operation is not None:
            operation(qc)
        sv = Statevector.from_instruction(qc)
        plot_amplitudes_live(ax_bar, bars, sv, basis_states, step_label, iteration, target_state, optimal_iterations)
        draw_grover_circle(ax_circle, iteration, optimal_iterations, theta, state_angle)

        plt.pause(1)

    # Start with Hadamard
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    iterate_and_plot(None, "Hadamard (Initialization)", 0)

    iteration = 1
    while plt.fignum_exists(fig.number):
        iterate_and_plot(lambda qc: oracle(qc, target_state), "Oracle (Query Phase)", iteration)
        iterate_and_plot(lambda qc: diffusion(qc, n_qubits), "Diffusion (Inversion Phase)", iteration)

        iteration += 1

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
