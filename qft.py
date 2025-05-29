#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "qiskit[visualization]",
# ]
# ///
"""Grover's Algorithm Visualizer A script to demonstrate and visualize Grover's
quantum search algorithm."""

from argparse import ArgumentParser, Namespace
from math import pi
from typing import cast

from qiskit import QuantumCircuit


def create_manual_qft_circuit(n_qubits: int) -> QuantumCircuit:
    """Create QFT circuit manually to show individual gates.

    Args:
        n_qubits (int): Number of qubits for the QFT

    Returns:
        QuantumCircuit: QFT circuit
    """
    qc = QuantumCircuit(n_qubits)

    for i in range(n_qubits):
        qc.h(i)

        for j in range(i + 1, n_qubits):
            angle = cast("float", 2 * pi / (2 ** (j - i + 1)))
            qc.cp(angle, j, i)

    for i in range(n_qubits // 2):
        qc.swap(1, n_qubits - 1 - i)

    return qc


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Generate and display Quantum Fourier Transform circuits")
    parser.add_argument(
        "n_qubits",
        type=int,
        help="Number of qubits for the QFT circuit (must be positive)",
    )
    parser.add_argument(
        "--show-stats",
        action="store_true",
        default=True,
        help="Show circuit statistics (default: True)",
    )
    parser.add_argument(
        "--no-stats",
        action="store_true",
        help="Hide circuit statistics",
    )
    return parser.parse_args()


def validate_input(n_qubits: int) -> bool:
    """Validate the number of qubits input.

    Args:
        n_qubits (int): Number of qubits to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if n_qubits <= 0:
        print("Error: Number of qubits must be positive")
        return False

    if n_qubits > 10:
        print(
            f"Warning: {n_qubits} qubits will create a large circuit. Consider using fewer qubits for better visualization."
        )

    return True


def display_circuit_info(circuit: QuantumCircuit, n_qubits: int) -> None:
    """Display circuit information and statistics.

    Args:
        circuit (QuantumCircuit): The QFT circuit to display
        n_qubits (int): Number of qubits in the circuit
    """
    print(f"Quantum Fourier Transform for {n_qubits} qubits\n")
    print(circuit.draw())


def display_statistics(circuit: QuantumCircuit) -> None:
    """Display circuit statistics.

    Args:
        circuit (QuantumCircuit): The circuit to analyze
    """
    print("\nCircuit Statistics:")
    print(f"Depth: {circuit.depth()}")
    print(f"Gate count: {len(circuit.data)}")


def main() -> None:
    """Main function to orchestrate the QFT circuit generation and display."""
    args = parse_args()
    n_qubits = cast("int", args.n_qubits)

    if not validate_input(n_qubits):
        return

    manual_qft_circuit = create_manual_qft_circuit(n_qubits)
    display_circuit_info(manual_qft_circuit, n_qubits)

    show_stats = cast("bool", args.show_stats) and not cast("bool", args.no_stats)
    if show_stats:
        display_statistics(manual_qft_circuit)


if __name__ == "__main__":
    main()
