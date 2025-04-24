#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from math import asin, sqrt
from typing import Callable

import matplotlib.pyplot as plt
from matplotlib.backend_bases import KeyEvent
from matplotlib.gridspec import GridSpec
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from grovers_visualizer.circuit import diffusion, oracle
from grovers_visualizer.parse import parse_args
from grovers_visualizer.plot import SinePlotData, plot_amplitudes, plot_circle, plot_sine
from grovers_visualizer.utils import all_states, optimal_grover_iterations


def main() -> None:
    args = parse_args()

    target_state = args.target
    n_qubits = len(target_state)
    basis_states = [str(bit) for bit in all_states(n_qubits)]
    optimal_iterations = optimal_grover_iterations(n_qubits)
    theta = 2 * asin(1 / sqrt(2**n_qubits))
    state_angle = 0.5 * theta

    plt.ion()
    fig = plt.figure(figsize=(14, 6))
    gs = GridSpec(2, 2, width_ratios=(3, 1), figure=fig)
    ax_bar = fig.add_subplot(gs[0, 0])
    ax_sine = fig.add_subplot(gs[1, 0])
    ax_circle = fig.add_subplot(gs[:, 1])
    bars = ax_bar.bar(basis_states, [0] * len(basis_states), color="skyblue")
    ax_bar.set_ylim(-1, 1)
    ax_bar.set_title("Amplitudes (example)")

    sine_data = SinePlotData()

    def plot_bar(
        operation: Callable[[QuantumCircuit], None] | None,
        step_label: str,
        iteration: int,
    ) -> None:
        if operation is not None:
            operation(qc)
        sv = Statevector.from_instruction(qc)
        plot_amplitudes(ax_bar, bars, sv, basis_states, step_label, iteration, target_state, optimal_iterations)

    # Start with Hadamard
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    plot_bar(None, "Hadamard (Initialization)", 0)

    iteration = 1
    running = True

    def on_key(event: KeyEvent) -> None:
        nonlocal running
        if event.key == "q":
            running = False

    cid = fig.canvas.mpl_connect("key_press_event", on_key)
    while plt.fignum_exists(fig.number) and running:
        plot_bar(lambda qc: oracle(qc, target_state), "Oracle (Query Phase)", iteration)
        plot_bar(lambda qc: diffusion(qc, n_qubits), "Diffusion (Inversion Phase)", iteration)

        plot_circle(ax_circle, iteration, optimal_iterations, theta, state_angle)
        sine_data.calc_and_append_probability(iteration, theta)
        plot_sine(ax_sine, sine_data)

        plt.pause(args.speed)

        iteration += 1
        if args.iterations > 0 and iteration > args.iterations:
            break

    fig.canvas.mpl_disconnect(cid)
    plt.ioff()


if __name__ == "__main__":
    main()
