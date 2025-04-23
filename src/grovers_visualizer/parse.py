from argparse import ArgumentParser
from dataclasses import dataclass

from grovers_visualizer.state import QubitState


@dataclass
class Args:
    target: QubitState
    iterations: int
    speed: float


def parse_args() -> Args:
    parser = ArgumentParser(description="Grover's Algorithm Visualizer")
    parser.add_argument(
        "target",
        type=str,
        help="Target bitstring (e.g., 1010)",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=0,
        help="Number of Grover iterations (default: 0 (infinite))",
    )
    parser.add_argument(
        "-s",
        "--speed",
        type=float,
        default=0.5,
        help="Pause duration (seconds) between steps (deafult: 0.5)",
    )
    ns = parser.parse_args()
    return Args(
        target=QubitState.from_str(ns.target),
        iterations=ns.iterations,
        speed=ns.speed,
    )
