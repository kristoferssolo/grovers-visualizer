#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def main() -> None:
    qc = QuantumCircuit(1, 1)

    qc.h(0)

    qc.measure(0, 0)

    print("Circuit Diagram:")
    print(qc.draw("text"))

    sim = AerSimulator()

    job = sim.run(qc, shots=1024)
    results = job.result()

    counts = results.get_counts()

    print(f"\nResults: {counts}")


if __name__ == "__main__":
    main()
