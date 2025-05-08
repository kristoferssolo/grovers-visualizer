# Grover’s Search Visualizer

A tiny Python package that steps through Grover’s Search algorithm and shows you, after each iteration:

- A bar‐chart of amplitudes (or probabilities)  
- A sine‐curve of success‐probability vs. iteration  
- A geometric "rotation" on the unit circle  

Choose between a Matplotlib-based CLI or an optional DearPyGui GUI (WIP).

---

![Demo of Grover’s Visualizer](media/demo.gif)

---

## Installation

### Via [pipx](https://pipx.pypa.io/stable/installation/)

Basic (CLI only):

```bash
pipx install grovers-visualizer
grovers-visualizer 1111
```

With the optional DearPyGui UI (WIP):

```bash
pipx "grovers-visualizer[ui]"
grovers-visualizer --ui
```

### Via [uvx](https://docs.astral.sh/uv/guides/tools/)

Basic (CLI only):

```bash
uvx grovers-visualizer 1111
```

With the optional UI extra:

```bash
uvx "grovers-visualizer[ui]" --ui
```

---

## Usage

### CLI Mode

Flags:

• `-t, --target`  
 Target bit‐string (e.g. `010`). Length determines number of qubits.  
• `-s, --speed`  
 Delay between iterations (seconds). Default `0.5`.  
• `-i, --iterations`  
 Max iterations; `0` means use the optimal $\lfloor\frac\pi4\sqrt{2^n}\rfloor$.  
• `--ui`  
 Launch the optional DearPyGui GUI (requires the `[ui]` extra) (WIP).

### GUI Mode (WIP)

If you installed with `"[ui]"`, launch the DearPyGui window:

```
grovers-visualizer --ui
```

In the UI you can:

- Set number of qubits  
- Enter the target bit‐string  
- Choose max iterations or leave at 0 for optimal  
- Control the animation speed  

Hit **Start** to watch the bar chart, sine plot, and rotation‐circle update in real time.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
