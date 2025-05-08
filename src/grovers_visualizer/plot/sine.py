from dataclasses import dataclass, field
from math import sin

from matplotlib.axes import Axes


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
