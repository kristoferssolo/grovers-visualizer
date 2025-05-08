import math

from qiskit import QuantumCircuit
from qiskit.circuit.library import PhaseGate

from .state import QubitState


def oracle(qc: QuantumCircuit, target_state: QubitState, /, *, phase: float = math.pi) -> None:
    """Oracle that flips the sign of the target state."""
    n = len(target_state)
    encode_target_state(qc, target_state)
    apply_phase_inversion(qc, n, phase=phase)
    encode_target_state(qc, target_state)  # Undo


def oracle_circuit(target: QubitState, /, *, phase: float = math.pi) -> QuantumCircuit:
    n = len(target)
    qc = QuantumCircuit(n)
    oracle(qc, target, phase=phase)
    return qc


def diffusion(qc: QuantumCircuit, n: int, /, *, phase: float = math.pi) -> None:
    """Apply the Grovers diffusion operator."""
    qc.h(range(n))
    qc.x(range(n))
    apply_phase_inversion(qc, n, phase=phase)
    qc.x(range(n))
    qc.h(range(n))


def diffusion_circuit(n: int, /, *, phase: float = math.pi) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    diffusion(qc, n, phase=phase)
    return qc


def encode_target_state(qc: QuantumCircuit, target_state: QubitState) -> None:
    """Apply X gates to qubits where the target state bit is '0'."""
    for i, bit in enumerate(reversed(target_state)):
        if bit == 0:
            qc.x(i)


def apply_phase_inversion(qc: QuantumCircuit, n: int, /, *, phase: float = math.pi) -> None:
    """Apply a multi-controlled phase inversion (Z) to the marked state."""
    if n == 1:
        qc.p(phase, 0)
        return
    mc_phase = PhaseGate(phase).control(n - 1)
    qc.append(mc_phase, list(range(n)))
