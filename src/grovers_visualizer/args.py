import math
from argparse import ArgumentParser
from dataclasses import dataclass

from grovers_visualizer.state import QubitState
from grovers_visualizer.utils import get_app_version


@dataclass
class Args:
    target: QubitState
    iterations: int
    speed: float
    ui: bool
    phase: float


def parse_args() -> Args:
    parser = ArgumentParser(description="Grover's Algorithm Visualizer")

    parse_opts(parser)
    parse_cli(parser)

    ns = parser.parse_args()

    return Args(
        target=ns.target,
        iterations=ns.iterations,
        speed=ns.speed,
        ui=ns.ui,
        phase=ns.phase,
    )


def parse_opts(base_parser: ArgumentParser) -> None:
    parser = base_parser

    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {get_app_version()}")


def parse_cli(base_parser: ArgumentParser) -> None:
    parser = base_parser.add_argument_group("cli")

    parser.register("type", "qubit state", QubitState.from_str)

    parser.add_argument(
        "target",
        type="qubit state",
        default=QubitState.from_str("1111"),
        nargs="?",
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
    parser.add_argument(
        "-p",
        "--phase",
        type=float,
        default=math.pi,
        help=(
            "The phase φ (in radians) used for the oracle and diffusion steps. "
            "Defaults to π, which implements the usual sign flip e^(iπ) = -1."
        ),
    )

    parser.add_argument("--ui", action="store_true", help="Run with DearPyGui UI")
