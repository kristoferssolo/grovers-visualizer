from qiskit import QuantumCircuit

from grovers_visualizer.state import QubitState


def encode_target_state(qc: QuantumCircuit, target_state: QubitState) -> None:
    """Apply X gates to qubits where the target state bit is '0'."""
    for i, bit in enumerate(reversed(target_state)):
        if bit == "0":
            qc.x(i)


def apply_phase_inversion(qc: QuantumCircuit, n: int) -> None:
    """Apply a multi-controlled phase inversion (Z) to the marked state."""
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.cz(0, 1)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)  # multi-controlled X (Toffoli for 3 qubits)
        qc.h(n - 1)
