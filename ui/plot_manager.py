"""View: Управление графиками (единственная ответственность — отрисовка)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk


class PlotManager:
    """Инкапсулирует matplotlib, не знает об алгоритме."""

    def __init__(self, parent: tk.Widget, figsize: tuple = (7, 6)):
        self.fig = Figure(figsize=figsize, dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    # ui/plot_manager.py
    def draw_convergence(self, iterations: list, best_values: list, worst_values: list) -> None:
        """Отрисовка сходимости с автоматическим выбором шкалы."""
        self.ax1.clear()

        if not iterations:
            return

        # Проверяем, можно ли использовать логарифмическую шкалу
        has_negative = any(v <= 0 for v in best_values + worst_values)

        if has_negative:
            # Линейная шкала для функций с отрицательными значениями
            self.ax1.plot(iterations, best_values, 'b-', linewidth=2, label='Лучшая')
            self.ax1.plot(iterations, worst_values, 'r--', linewidth=1, label='Худшая')
        else:
            # Логарифмическая шкала для строго положительных функций (напр. x² + y²)
            self.ax1.semilogy(iterations, best_values, 'b-', linewidth=2, label='Лучшая')
            self.ax1.semilogy(iterations, worst_values, 'r--', linewidth=1, label='Худшая')

        self.ax1.set_title("Сходимость")
        self.ax1.set_ylabel("f(x)")
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)

        # Разброс значений
        if best_values and worst_values:
            spread = [w - b for b, w in zip(best_values, worst_values)]
            self.ax2.clear()
            self.ax2.plot(iterations, spread, 'g-', linewidth=1.5)
            self.ax2.set_title("Разброс в симплексе")
            self.ax2.set_xlabel("Итерация")
            self.ax2.set_ylabel("fh - fl")
            self.ax2.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def clear(self) -> None:
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()