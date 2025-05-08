from math import cos, sin

from matplotlib.axes import Axes
from matplotlib.patches import Circle

from grovers_visualizer.utils import is_optimal_iteration


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
        f"{prob:.2f}",
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
