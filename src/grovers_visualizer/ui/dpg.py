import dearpygui.dearpygui as dpg

from grovers_visualizer.args import Args


def run_dearpygui_ui(_args: Args) -> None:
    dpg.create_context()
    dpg.create_viewport(title="Grover's Search Visualizer", width=900, height=600)
    dpg.setup_dearpygui()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
