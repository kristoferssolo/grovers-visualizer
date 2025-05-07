#!/usr/bin/env python
"""Grover's Algorithm Visualizer.

This script builds a Grover search circuit based on user input, runs the
simulation using Qiskit's Aer simulator, and visualizes the results
using matplotlib.
"""

from .args import parse_args
from .cli import run_cli
from .ui import run_dpg_ui


def main() -> None:
    args = parse_args()
    if args.ui:
        run_dpg_ui(args)
    else:
        run_cli(args)


if __name__ == "__main__":
    main()
