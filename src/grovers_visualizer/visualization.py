from typing import TYPE_CHECKING, final, override

import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event, KeyEvent
from matplotlib.gridspec import GridSpec

from grovers_visualizer.simulation import grover_evolver

from .abc.visualization import BaseGroverVisualizer
from .plot import plot_amplitudes, plot_circle, plot_sine

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.container import BarContainer
    from matplotlib.figure import Figure


@final
class GroverVisualizer(BaseGroverVisualizer):
    @override
    def _init_figure(self) -> None:
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

    @override
    def update(self) -> None:
        """Given (iteration, Statevector), update all three plots."""
        for it, sv in grover_evolver(self.target, self.iterations, phase=self.phase):
            if not self.is_running:
                break
            # amplitudes
            plot_amplitudes(
                self.ax_bar,
                self.bars,
                sv,
                self.basis_states,
                "Grover Iteration",
                it,
                self.target,
                self.optimal,
            )

            # circle
            plot_circle(
                self.ax_circle,
                it,
                self.optimal,
                self.theta,
                self.state_angle,
            )

            # sine curve
            self.sine_data.calc_and_append_probability(it, self.theta)

            plot_sine(self.ax_sine, self.sine_data)
            plt.pause(self.pause)

    @override
    def finalize(self) -> None:
        """Clean up after loop ends."""
        self.fig.canvas.mpl_disconnect(self.cid)
        plt.ioff()
