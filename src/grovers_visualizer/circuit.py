from math import floor, pi, sqrt

from qiskit import QuantumCircuit

from .state import QubitState


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


def encode_target_state(qc: QuantumCircuit, target_state: QubitState) -> None:
    """Apply X gates to qubits where the target state bit is '0'."""
    for i, bit in enumerate(reversed(target_state)):
        if bit == 0:
            qc.x(i)


def apply_phase_inversion(qc: QuantumCircuit, n: int) -> None:
    """Apply a multi-controlled phase inversion (Z) to the marked state."""
    if n == 1:
        qc.z(0)
        return
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
