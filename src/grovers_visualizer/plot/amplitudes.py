import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from qiskit.quantum_info import Statevector

from grovers_visualizer.state import QubitState
from grovers_visualizer.utils import get_bar_color


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
