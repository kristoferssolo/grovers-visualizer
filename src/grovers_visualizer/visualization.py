from math import asin, sqrt
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event, KeyEvent
from matplotlib.gridspec import GridSpec
from qiskit.quantum_info import Statevector

from grovers_visualizer.plot import SinePlotData, plot_amplitudes, plot_circle, plot_sine
from grovers_visualizer.state import QubitState
from grovers_visualizer.utils import all_states, optimal_grover_iterations

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.container import BarContainer
    from matplotlib.figure import Figure


class GroverVisualizer:
    def __init__(self, target: QubitState, pause: float = 0.5) -> None:
        self.target: QubitState = target
        self.n: int = len(self.target)
        self.basis_states: list[str] = [str(b) for b in all_states(self.n)]
        self.optimal: int = optimal_grover_iterations(self.n)
        self.theta: float = 2 * asin(1 / sqrt(2.0**self.n))
        self.state_angle: float = 0.5 * self.theta
        self.sine_data: SinePlotData = SinePlotData()
        self.is_running: bool = True
        self.pause: float = pause
        self._build_figure()

    def _build_figure(self) -> None:
        plt.ion()
        self.fig: Figure = plt.figure(figsize=(14, 6))
        gs = GridSpec(2, 2, width_ratios=(3, 1), figure=self.fig)
        self.ax_bar: Axes = self.fig.add_subplot(gs[0, 0])
        self.ax_sine: Axes = self.fig.add_subplot(gs[1, 0])
        self.ax_circle: Axes = self.fig.add_subplot(gs[:, 1])

        # bars
        self.bars: BarContainer = self.ax_bar.bar(self.basis_states, [0] * len(self.basis_states), color="skyblue")
        self.ax_bar.set_ylim(-1, 1)
        self.ax_bar.set_title("Amplitudes (example)")

        # key handler to quit
        self.cid: int = self.fig.canvas.mpl_connect("key_press_event", self._on_key)

    def _on_key(self, event: Event) -> None:
        if isinstance(event, KeyEvent) and event.key == "q":
            self.is_running = False

    def update(self, iteration: int, sv: Statevector) -> None:
        """Given (iteration, Statevector), update all three plots."""
        # amplitudes
        plot_amplitudes(
            self.ax_bar,
            self.bars,
            sv,
            self.basis_states,
            "Grover Iteration",
            iteration,
            self.target,
            self.optimal,
        )

        # circle
        plot_circle(
            self.ax_circle,
            iteration,
            self.optimal,
            self.theta,
            self.state_angle,
        )

        # sine curve
        self.sine_data.calc_and_append_probability(iteration, self.theta)

        plot_sine(self.ax_sine, self.sine_data)
        plt.pause(self.pause)

    def finalize(self) -> None:
        """Clean up after loop ends."""
        self.fig.canvas.mpl_disconnect(self.cid)
        plt.ioff()
