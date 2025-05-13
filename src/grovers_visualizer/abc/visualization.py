import math
from abc import ABC, abstractmethod
from math import asin, sqrt
from typing import Self

from grovers_visualizer.args import Args
from grovers_visualizer.plot import SinePlotData
from grovers_visualizer.state import QubitState
from grovers_visualizer.utils import all_states, optimal_grover_iterations


class BaseGroverVisualizer(ABC):
    def __init__(self, target: QubitState, *, iterations: int = 0, pause: float = 0.5, phase: float = math.pi) -> None:
        self.target: QubitState = target
        self.n: int = len(self.target)
        self.basis_states: list[str] = [str(b) for b in all_states(self.n)]
        self.optimal: int = optimal_grover_iterations(self.n)
        self.theta: float = 2 * asin(1 / sqrt(2.0**self.n))
        self.state_angle: float = 0.5 * self.theta
        self.sine_data: SinePlotData = SinePlotData()
        self.is_running: bool = True
        self.pause: float = pause
        self.iterations: int = iterations
        self.phase: float = phase
        self._init_figure()

    @abstractmethod
    def _init_figure(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Given (iteration, Statevector), update all three plots."""
        raise NotImplementedError

    @abstractmethod
    def finalize(self) -> None:
        raise NotImplementedError

    @classmethod
    def from_args(cls, args: Args) -> Self:
        return cls(
            args.target,
            iterations=args.iterations,
            pause=args.speed,
            phase=args.phase,
        )
