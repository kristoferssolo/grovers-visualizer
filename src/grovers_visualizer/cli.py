from grovers_visualizer.visualization import GroverVisualizer

from .args import Args


def run_cli(args: Args) -> None:
    vis = GroverVisualizer.from_args(args)
    vis.update()
    vis.finalize()
