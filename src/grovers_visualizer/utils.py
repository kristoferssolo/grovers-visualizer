from collections.abc import Iterator
from importlib.metadata import PackageNotFoundError, version
from itertools import product
from math import floor, pi, sqrt

from .state import QubitState


def all_states(n_qubits: int) -> Iterator[QubitState]:
    """Generate all possible QubitStates for n_qubits."""
    for bits in product((0, 1), repeat=n_qubits):
        yield QubitState(bits)


def optimal_grover_iterations(n_qubits: int) -> int:
    """Return the optimal number of Grover iterations for n qubits."""
    return floor(pi / 4 * sqrt(2.0**n_qubits))


def is_optimal_iteration(iteration: int, optimal_iteration: int) -> bool:
    return iteration == optimal_iteration


def get_bar_color(state: str, target_state: QubitState | None, iteration: int, optimal_iteration: int | None) -> str:
    """Return the color for a bar based on state and iteration."""
    if state != target_state:
        return "skyblue"
    if optimal_iteration and is_optimal_iteration(iteration, optimal_iteration):
        return "green"
    return "orange"


def get_app_version() -> str:
    """Return the installed package version, e.g. '0.4.0'.

    Falls back to 'unknown' if not installed as a distribution.
    """
    try:
        return version("grovers-visualizer")
    except PackageNotFoundError:
        return "unknown"
