from importlib.util import find_spec

from grovers_visualizer.parse import Args


def is_dearpygui_available() -> bool:
    try:
        return find_spec("dearpygui.dearpygui") is not None
    except ModuleNotFoundError:
        return False


def run_dpg_ui(_args: Args) -> None:
    if not is_dearpygui_available():
        print("DearPyGui is not installed. Install with: pip install .[ui]")
        return

    from .dpg import run_dearpygui_ui

    run_dearpygui_ui()
