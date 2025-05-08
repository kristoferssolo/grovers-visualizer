import math
from collections.abc import Iterator
from itertools import count

from qiskit import QuantumCircuit
from qiskit.qasm2.parse import Operator
from qiskit.quantum_info import Statevector

from grovers_visualizer.circuit import diffusion_circuit, oracle_circuit
from grovers_visualizer.state import QubitState


def grover_evolver(
    target: QubitState,
    max_iterations: int = 0,
    *,
    phase: float = math.pi,
) -> Iterator[tuple[int, Statevector]]:
    """Yields (iteration, statevector) pairs.

    - iteration=0 is the uniform-Hadamard initialization
    - max_iterations > 0, stop after that many iterations
    - max_iterations == 0, run indefinitely (until the consumer breaks)
    """
    n_qubits = len(target)
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))

    # initial statevector
    sv = Statevector.from_instruction(qc)
    yield 0, sv

    oracle_op = Operator(oracle_circuit(target, phase=phase))
    diffusion_op = Operator(diffusion_circuit(n_qubits, phase=phase))

    iters = range(1, max_iterations + 1) if max_iterations > 0 else count(1)
    for i in iters:
        sv = sv.evolve(oracle_op).evolve(diffusion_op)
        yield i, sv
