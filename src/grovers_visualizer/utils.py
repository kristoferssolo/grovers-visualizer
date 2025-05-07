import tomllib
from collections.abc import Iterator
from itertools import product
from math import floor, pi, sqrt
from pathlib import Path

from .state import QubitState


def all_states(n_qubits: int) -> Iterator[QubitState]:
    """Generate all possible QubitStates for n_qubits."""
    for bits in product((0, 1), repeat=n_qubits):
        yield QubitState(bits)


def optimal_grover_iterations(n_qubits: int) -> int:
    """Return the optimal number of Grover iterations for n qubits."""
    return floor(pi / 4 * sqrt(2**n_qubits))


def is_optimal_iteration(iteration: int, optimal_iteration: int) -> bool:
    return iteration == optimal_iteration


def get_bar_color(state: str, target_state: QubitState | None, iteration: int, optimal_iteration: int | None) -> str:
    """Return the color for a bar based on state and iteration."""
    if state != target_state:
        return "skyblue"
    if optimal_iteration and is_optimal_iteration(iteration, optimal_iteration):
        return "green"
    return "orange"


def get_app_version(pyproject_path: str = "pyproject.toml") -> str:
    """Reads the version from the [project] section of pyproject.toml."""
    path = Path(pyproject_path)
    if not path.is_file():
        raise FileNotFoundError(f"{pyproject_path} not found.")
    with path.open("rb") as f:
        data = tomllib.load(f)
    try:
        return str(data["project"]["version"])
    except KeyError:
        raise KeyError("Version not found in [project] section of pyproject.toml.")
