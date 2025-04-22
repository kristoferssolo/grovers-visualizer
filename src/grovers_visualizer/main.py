#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from collections.abc import Iterator
from itertools import product
from math import asin, cos, floor, pi, sin, sqrt
from typing import TYPE_CHECKING, Callable

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.patches import Circle
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from grovers_visualizer.gates import apply_phase_inversion, encode_target_state
from grovers_visualizer.state import QubitState

if TYPE_CHECKING:
    from matplotlib.figure import Figure


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


def optimal_grover_iterations(n_qubits: int) -> int:
    """Return the optimal number of Grover iterations for n qubits."""
    return floor(pi / 4 * sqrt(2**n_qubits))


def is_optimal_iteration(iteration: int, optimal_iteration: int) -> bool:
    return iteration % optimal_iteration == 0 and iteration != 0


def get_bar_color(state: str, target_state: QubitState | None, iteration: int, optimal_iteration: int | None) -> str:
    """Return the color for a bar based on state and iteration."""
    if state != target_state:
        return "skyblue"
    if optimal_iteration and is_optimal_iteration(iteration, optimal_iteration):
        return "green"
    return "orange"


def plot_amplitudes_live(
    ax: Axes,
    bars: BarContainer,
    statevector: Statevector,
    basis_states: list[str],
    iteration_label: str,
    iteration: int,
    target_state: QubitState | None = None,
    optimal_iteration: int | None = None,
) -> None:
    amplitudes: npt.NDArray[np.float64] = statevector.data.real  # Real part of amplitudes
    mean = np.mean(amplitudes)

    for bar, state, amp in zip(bars, basis_states, amplitudes, strict=False):
        bar.set_height(amp)
        bar.set_color(get_bar_color(state, target_state, iteration, optimal_iteration))

    ax.set_title(f"Iteration {iteration}: {iteration_label}")
    ax.set_ylim(-1, 1)

    for l in ax.lines:  # Remove previous mean line(s)
        l.remove()

    ax.axhline(float(mean), color="red", linestyle="--", label="Mean")

    if not ax.get_legend():
        ax.legend(loc="upper right")


def draw_grover_circle(
    ax: Axes,
    iteration: int,
    optimal_iterations: int,
    theta: float,
    state_angle: float,
) -> None:
    ax.clear()
    ax.set_aspect("equal")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("Unmarked amplitude")
    ax.set_ylabel("Target amplitude")
    ax.set_title("Grover State Vector Rotation")

    # Draw unit circle
    circle = Circle((0, 0), 1, color="gray", fill=False)
    ax.add_artist(circle)

    # Draw axes
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)

    # Draw labels
    ax.text(1.05, 0, "", va="center", ha="left", fontsize=10)
    ax.text(0, 1.05, "1", va="bottom", ha="center", fontsize=10)
    ax.text(-1.05, 0, "", va="center", ha="right", fontsize=10)
    ax.text(0, -1.05, "-1", va="top", ha="center", fontsize=10)

    angle = state_angle + iteration * theta
    x, y = cos(angle), sin(angle)
    is_optimal = optimal_iterations and is_optimal_iteration(iteration, optimal_iterations)

    # Arrow color: green at optimal, blue otherwise
    color = "green" if is_optimal else "blue"
    ax.arrow(0, 0, x, y, head_width=0.07, head_length=0.1, fc=color, ec=color, length_includes_head=True)

    # Probability of target state is y^2
    prob = y**2
    ax.set_title(
        f"Grover State Vector Rotation\nIteration {iteration} | Probability of target: {prob:.2f}{' (optimal)' if is_optimal else ''}"
    )


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
