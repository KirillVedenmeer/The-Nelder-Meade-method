"""View: Управление графиками."""

import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PlotManager:
    """Инкапсулирует matplotlib, не знает об алгоритме."""

    def __init__(self, parent: tk.Widget, figsize: tuple = (7, 6)):
        self.fig = Figure(figsize=figsize, dpi=100)

        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_convergence(
        self,
        iterations: list,
        best_values: list,
        worst_values: list,
        simplex_history=None
    ) -> None:
        """Верхний график: точки симплекса. Нижний график: разброс."""

        self.ax1.clear()
        self.ax2.clear()

        if not iterations:
            self.canvas.draw()
            return

        if simplex_history:
            self.draw_simplex_path(simplex_history)
        else:
            self.ax1.text(
                0.5,
                0.5,
                "Нет данных о точках симплекса",
                ha="center",
                va="center",
                transform=self.ax1.transAxes
            )
            self.ax1.set_title("Изменение точек симплекса")

        self.draw_spread(iterations, best_values, worst_values)

        self.fig.tight_layout()
        self.canvas.draw()

    def draw_simplex_path(self, simplex_history: list) -> None:
        """Рисует изменение симплекса по шагам на верхнем графике."""

        self.ax1.clear()

        first_simplex = np.asarray(simplex_history[0])

        if first_simplex.ndim != 2 or first_simplex.shape[1] != 2:
            self.ax1.text(
                0.5,
                0.5,
                "График симплекса доступен только для функции двух переменных",
                ha="center",
                va="center",
                transform=self.ax1.transAxes
            )
            self.ax1.set_title("Изменение точек симплекса")
            return

        step = max(1, len(simplex_history) // 25)

        for i, simplex in enumerate(simplex_history):
            simplex = np.asarray(simplex)

            if i % step != 0 and i != len(simplex_history) - 1:
                continue

            points = np.vstack([simplex, simplex[0]])

            self.ax1.plot(
                points[:, 0],
                points[:, 1],
                marker="o",
                linewidth=1,
                alpha=0.5)

            center = simplex.mean(axis=0)
            self.ax1.text(center[0], center[1], str(i), fontsize=7)

        self.ax1.set_title("Изменение точек симплекса по шагам")
        self.ax1.set_xlabel("x₁")
        self.ax1.set_ylabel("x₂")
        self.ax1.grid(True, alpha=0.3)

    def draw_spread(
        self,
        iterations: list,
        best_values: list,
        worst_values: list
    ) -> None:
        """Рисует разброс значений в симплексе на нижнем графике."""

        spread = [w - b for b, w in zip(best_values, worst_values)]

        self.ax2.plot(iterations, spread, "g-", linewidth=1.5)
        self.ax2.set_title("Разброс в симплексе")
        self.ax2.set_xlabel("Итерация")
        self.ax2.set_ylabel("fh - fl")
        self.ax2.grid(True, alpha=0.3)

    def clear(self) -> None:
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()