from grovers_visualizer.simulation import grover_evolver
from grovers_visualizer.visualization import GroverVisualizer

from .args import Args


def run_cli(args: Args) -> None:
    vis = GroverVisualizer(args.target, pause=args.speed)

    for it, sv in grover_evolver(vis.target, args.iterations, phase=args.phase):
        if not vis.is_running:
            break
        vis.update(it, sv)

    vis.finalize()
