from dataclasses import dataclass, field
from math import cos, sin

import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.patches import Circle
from qiskit.quantum_info import Statevector

from .state import QubitState
from .utils import get_bar_color, is_optimal_iteration, sign


def plot_amplitudes(
    ax: Axes,
    bars: BarContainer,
    statevector: Statevector,
    basis_states: list[str],
    iteration_label: str,
    iteration: int,
    target_state: QubitState | None = None,
    optimal_iteration: int | None = None,
) -> None:
    amplitudes: npt.NDArray[np.float64] = statevector.data.real  # Real part of amplitudes
    mean = np.mean(amplitudes)

    for bar, state, amp in zip(bars, basis_states, amplitudes, strict=False):
        bar.set_height(amp)
        bar.set_color(get_bar_color(state, target_state, iteration, optimal_iteration))

    ax.set_title(f"Iteration {iteration}: {iteration_label}")
    ax.set_ylim(-1, 1)

    for l in ax.lines:  # Remove previous mean line(s)
        l.remove()

    # Draw axes and mean
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axhline(float(mean), color="red", linestyle="--", label="Mean")

    if not ax.get_legend():
        ax.legend(loc="upper right")


def plot_circle(
    ax: Axes,
    iteration: int,
    optimal_iterations: int,
    theta: float,
    state_angle: float,
) -> None:
    ax.clear()
    ax.set_aspect("equal")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("Unmarked amplitude")
    ax.set_ylabel("Target amplitude")
    ax.set_title("Grover State Vector Rotation")

    # Draw unit circle
    circle = Circle((0, 0), 1, color="gray", fill=False)
    ax.add_artist(circle)

    # Draw axes
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)

    # Draw labels
    ax.text(1.05, 0, "", va="center", ha="left", fontsize=10)
    ax.text(0, 1.05, "1", va="bottom", ha="center", fontsize=10)
    ax.text(-1.05, 0, "", va="center", ha="right", fontsize=10)
    ax.text(0, -1.05, "-1", va="top", ha="center", fontsize=10)

    angle = state_angle + iteration * theta
    x, y = cos(angle), sin(angle)
    is_optimal = is_optimal_iteration(iteration, optimal_iterations)

    # Arrow color: green at optimal, blue otherwise
    color = "green" if is_optimal else "blue"
    ax.arrow(0, 0, x, y, head_width=0.07, head_length=0.1, fc=color, ec=color, length_includes_head=True)

    # Probability of target state is y^2
    prob = y**2

    # Draw the value at the tip of the arrow
    ax.text(
        x,
        y,
        f"{prob * sign(y):.2f}",
        color=color,
        fontsize=10,
        ha="left" if x >= 0 else "right",
        va="bottom" if y >= 0 else "top",
        fontweight="bold",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.7, "boxstyle": "round,pad=0.2"},
    )

    ax.set_title(
        f"Grover State Vector Rotation\nIteration {iteration} | Probability of target: {prob}{' (optimal)' if is_optimal else ''}"
    )


@dataclass
class SinePlotData:
    x: list[float] = field(default_factory=list)
    y: list[float] = field(default_factory=list)

    def append(self, x: float, y: float) -> None:
        self.x.append(x)
        self.y.append(y)

    def calc_and_append_probability(self, iteration: int, theta: float) -> None:
        prob = sin((2 * iteration + 1) * theta / 2) ** 2
        self.append(iteration, prob)


def plot_sine(
    ax: Axes,
    sine_data: SinePlotData,
) -> None:
    ax.clear()
    ax.plot(sine_data.x, sine_data.y, marker="o", color="purple", label="Target Probability")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Probability")
    ax.set_title("Grover Target Probability vs. Iteration")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, max(10, max(sine_data.x) + 1))
    ax.legend()
