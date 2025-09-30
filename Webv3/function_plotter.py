"""Interactive function plotter with default heart curve.

This script mirrors the browser-based Function Sketcher, allowing users to plot
f(x) and f(y) concurrently with shorthand math notation (sin, cos, tan, etc.).
"""

from __future__ import annotations

import math
import re
import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

CanvasPoint = Tuple[float, float]
BOUNDS = {
    "x_min": -18.0,
    "x_max": 18.0,
    "y_min": -18.0,
    "y_max": 18.0,
}
CANVAS_SIZE = 520
GRID_STEP = 3
DEFAULT_SAMPLES = CANVAS_SIZE
HEART_COLOR = "#ffffff"
FY_COLOR = "#ff4f6b"

SAFE_FUNCTIONS: Dict[str, Callable[[float], float]] = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_") and callable(getattr(math, name))
}
SAFE_CONSTANTS: Dict[str, float] = {
    name: getattr(math, name)
    for name in dir(math)
    if name in {"pi", "e", "tau"}
}


class FunctionPlotter:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Function Sketcher")
        self.root.configure(background="black")

        self.frame = ttk.Frame(self.root, padding=18)
        self.frame.grid(column=0, row=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._configure_styles()
        self._build_controls()
        self._build_canvas()

        self.heart_points: List[CanvasPoint] = []
        self.error_var = tk.StringVar(value="")
        self.error_label = ttk.Label(
            self.frame,
            textvariable=self.error_var,
            foreground="#ff4f6b",
            background="black",
        )
        self.error_label.grid(column=0, row=3, columnspan=2, sticky="w", pady=(8, 0))

        self._animation_id: Optional[str] = None

        self.draw_heart()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TFrame", background="black")
        style.configure("TLabel", background="black", foreground="#f9f9f9")
        style.configure("TButton", background="#111111", foreground="#f9f9f9", padding=6)
        style.configure(
            "Accent.TButton",
            background="#111111",
            foreground="#f9f9f9",
            padding=6,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#222222"), ("!active", "#111111")],
        )
        style.configure(
            "TEntry",
            fieldbackground="#1b1b1b",
            foreground="#f9f9f9",
            insertcolor="#f9f9f9",
        )

    def _build_controls(self) -> None:
        header = ttk.Label(
            self.frame,
            text="Function Sketcher",
            font=("Segoe UI", 20, "bold"),
        )
        header.grid(column=0, row=0, columnspan=2, sticky="w")

        subtitle = ttk.Label(
            self.frame,
            text="Plot f(x) and f(y) simultaneously. Try sin(x), cos(y/2), x2-1, etc.",
            foreground="#cccccc",
        )
        subtitle.grid(column=0, row=1, columnspan=2, sticky="w", pady=(4, 12))

        control_frame = ttk.Frame(self.frame)
        control_frame.grid(column=0, row=2, sticky="w")

        self.fx_var = tk.StringVar()
        self.fy_var = tk.StringVar()

        fx_row = ttk.Frame(control_frame)
        fx_row.grid(column=0, row=0, sticky="w", pady=4)
        ttk.Label(fx_row, text="f(x) =").grid(column=0, row=0, padx=(0, 6))
        self.fx_entry = ttk.Entry(fx_row, width=32, textvariable=self.fx_var)
        self.fx_entry.grid(column=1, row=0)

        fy_row = ttk.Frame(control_frame)
        fy_row.grid(column=0, row=1, sticky="w", pady=4)
        ttk.Label(fy_row, text="f(y) =").grid(column=0, row=0, padx=(0, 6))
        self.fy_entry = ttk.Entry(fy_row, width=32, textvariable=self.fy_var)
        self.fy_entry.grid(column=1, row=0)

        button_row = ttk.Frame(control_frame)
        button_row.grid(column=0, row=2, sticky="w", pady=(12, 0))
        draw_btn = ttk.Button(button_row, text="Draw", command=self.on_draw)
        draw_btn.grid(column=0, row=0)

        heart_btn = ttk.Button(
            button_row, text="Heart", command=self.on_heart, style="Accent.TButton"
        )
        heart_btn.grid(column=1, row=0, padx=(8, 0))

    def _build_canvas(self) -> None:
        canvas_frame = ttk.Frame(self.frame)
        canvas_frame.grid(column=1, row=2, rowspan=2, padx=(20, 0))

        self.canvas = tk.Canvas(
            canvas_frame,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            background="black",
            highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def to_canvas(self, x: float, y: float) -> CanvasPoint:
        x_norm = (x - BOUNDS["x_min"]) / (BOUNDS["x_max"] - BOUNDS["x_min"])
        y_norm = (y - BOUNDS["y_min"]) / (BOUNDS["y_max"] - BOUNDS["y_min"])
        return (
            x_norm * CANVAS_SIZE,
            CANVAS_SIZE - y_norm * CANVAS_SIZE,
        )

    def clear_canvas(self) -> None:
        self.canvas.delete("all")
        self.draw_background()

    def draw_background(self) -> None:
        self.canvas.configure(background="black")
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill="black", outline="")

        start_x = math.ceil(BOUNDS["x_min"] / GRID_STEP) * GRID_STEP
        for x in range(start_x, int(BOUNDS["x_max"]) + GRID_STEP, GRID_STEP):
            cx, _ = self.to_canvas(x, 0)
            self.canvas.create_line(cx, 0, cx, CANVAS_SIZE, fill="#222222")

        start_y = math.ceil(BOUNDS["y_min"] / GRID_STEP) * GRID_STEP
        for y in range(start_y, int(BOUNDS["y_max"]) + GRID_STEP, GRID_STEP):
            _, cy = self.to_canvas(0, y)
            self.canvas.create_line(0, cy, CANVAS_SIZE, cy, fill="#222222")

        axis_x, axis_y = self.to_canvas(0, 0)
        self.canvas.create_line(0, axis_y, CANVAS_SIZE, axis_y, fill="#888888")
        self.canvas.create_line(axis_x, 0, axis_x, CANVAS_SIZE, fill="#888888")

    def normalize_expression(self, expression: str, variable: str) -> str:
        expr = expression.strip()
        if not expr:
            return expr

        expr = expr.replace("^", "**")
        power_pattern = re.compile(rf"\\b{variable}(\\d+(?:\\.\\d+)?)\\b", re.IGNORECASE)
        expr = power_pattern.sub(lambda m: f"{variable}**{m.group(1)}", expr)
        expr = re.sub(rf"(\d)({variable})", r"\1*\2", expr, flags=re.IGNORECASE)
        expr = re.sub(r"(\d)\(", r"\1*(", expr)
        expr = re.sub(rf"([{variable}0-9\)])\(", r"\1*(", expr, flags=re.IGNORECASE)
        expr = re.sub(rf"\)([{variable}0-9])", r")*\1", expr, flags=re.IGNORECASE)
        expr = re.sub(r"\bpi\b", "pi", expr, flags=re.IGNORECASE)
        expr = re.sub(r"\be\b", "e", expr, flags=re.IGNORECASE)

        return expr

    def build_environment(self, variable: str, value: float) -> Dict[str, float]:
        env: Dict[str, float] = {variable: value}
        env.update(SAFE_FUNCTIONS)
        env.update(SAFE_CONSTANTS)
        env["abs"] = abs
        env["math"] = math
        return env

    def eval_expression(self, expression: str, variable: str, value: float) -> float:
        env = self.build_environment(variable, value)
        return eval(expression, {"__builtins__": {}}, env)

    def plot_function(self, expression: str, variable: str, color: str) -> Optional[str]:
        normalized = self.normalize_expression(expression, variable)
        if not normalized:
            return ""

        step_min = BOUNDS["x_min"] if variable == "x" else BOUNDS["y_min"]
        step_max = BOUNDS["x_max"] if variable == "x" else BOUNDS["y_max"]
        step = (step_max - step_min) / DEFAULT_SAMPLES

        last_valid: Optional[CanvasPoint] = None
        points_drawn = 0
        for i in range(DEFAULT_SAMPLES + 1):
            independent = step_min + i * step
            try:
                dependent = self.eval_expression(normalized, variable, independent)
            except Exception:
                last_valid = None
                continue

            if not math.isfinite(dependent):
                last_valid = None
                continue

            x_val, y_val = (
                (independent, dependent)
                if variable == "x"
                else (dependent, independent)
            )
            if not (BOUNDS["x_min"] <= x_val <= BOUNDS["x_max"] and BOUNDS["y_min"] <= y_val <= BOUNDS["y_max"]):
                last_valid = None
                continue

            cx, cy = self.to_canvas(x_val, y_val)
            if last_valid is not None:
                self.canvas.create_line(last_valid[0], last_valid[1], cx, cy, fill=color, width=2)
            last_valid = (cx, cy)
            points_drawn += 1

        if points_drawn == 0:
            return "returned no values in range"

        self.heart_points = []
        return None

    def draw_heart(self) -> None:
        self.clear_error()
        self.fx_var.set("heart")
        self.fy_var.set("")
        self.clear_canvas()
        total = 400
        points: List[CanvasPoint] = []
        for i in range(total + 1):
            t = (i / total) * math.tau
            x = 16 * (math.sin(t) ** 3)
            y = (
                13 * math.cos(t)
                - 5 * math.cos(2 * t)
                - 2 * math.cos(3 * t)
                - math.cos(4 * t)
            )
            points.append(self.to_canvas(x, y))

        for start, end in zip(points, points[1:]):
            self.canvas.create_line(start[0], start[1], end[0], end[1], fill=HEART_COLOR, width=2)

        self.heart_points = points

    def on_draw(self) -> None:
        raw_fx = self.fx_var.get().strip()
        raw_fy = self.fy_var.get().strip()
        self.clear_error()

        if (not raw_fx and not raw_fy) or raw_fx.lower() == "heart" or raw_fy.lower() == "heart":
            self.draw_heart()
            return

        self.clear_canvas()
        errors: List[str] = []

        if raw_fx:
            fx_error = self.plot_function(raw_fx, "x", HEART_COLOR)
            if fx_error:
                errors.append(f"f(x) {fx_error}")

        if raw_fy:
            fy_error = self.plot_function(raw_fy, "y", FY_COLOR)
            if fy_error:
                errors.append(f"f(y) {fy_error}")

        if not raw_fx and not raw_fy:
            self.draw_heart()

        if errors:
            self.show_error(" | ".join(errors))

    def on_heart(self) -> None:
        self.draw_heart()
        self.fx_entry.focus_set()

    def show_error(self, message: str) -> None:
        self.error_var.set(message)

    def clear_error(self) -> None:
        self.error_var.set("")

    def on_canvas_click(self, _event: tk.Event) -> None:
        if not self.heart_points:
            return
        if self._animation_id is not None:
            self.canvas.after_cancel(self._animation_id)
        self.animate_heart([1.05, 0.95, 1.02, 1.0])

    def animate_heart(self, scale_steps: Sequence[float], index: int = 0) -> None:
        if index >= len(scale_steps):
            self._animation_id = None
            return

        scale = scale_steps[index]
        self.clear_canvas()
        scaled_points = self._scale_points(self.heart_points, scale)
        for start, end in zip(scaled_points, scaled_points[1:]):
            self.canvas.create_line(start[0], start[1], end[0], end[1], fill=HEART_COLOR, width=2)
        self._animation_id = self.canvas.after(90, self.animate_heart, scale_steps, index + 1)

    def _scale_points(self, points: Iterable[CanvasPoint], scale: float) -> List[CanvasPoint]:
        pts = list(points)
        if not pts:
            return []
        xs, ys = zip(*pts)
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        return [((x - cx) * scale + cx, (y - cy) * scale + cy) for x, y in pts]

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    FunctionPlotter().run()


if __name__ == "__main__":
    main()
