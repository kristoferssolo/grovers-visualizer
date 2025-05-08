from collections.abc import Iterator
from itertools import count

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from grovers_visualizer.circuit import diffusion, oracle
from grovers_visualizer.state import QubitState


def grover_evolver(target: QubitState, max_iterations: int = 0) -> Iterator[tuple[int, Statevector]]:
    """Yields (iteration, statevector) pairs.

    iteration=0 is the uniform-Hadamard initialization. If
    max_iterations > 0, stop after that many iterations. If
    max_iterations == 0, run indefinitely (until the consumer breaks).
    """
    n_qubits = len(target)
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))

    # initial statevector
    yield 0, Statevector.from_instruction(qc)

    # pick an iterator for subsequent steps
    iter = range(1, max_iterations + 1) if max_iterations > 0 else count(1)

    for i in iter:
        oracle(qc, target)
        diffusion(qc, n_qubits)
        yield i, Statevector.from_instruction(qc)
