"""Controller: Главный контроллер приложения (координация, без бизнес-логики)."""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import threading

from config.settings import NelderMeadConfig, IterationState
from core.optimizer import NelderMeadOptimizer
from services.function_evaluator import FunctionEvaluator
from ui.widgets import LabeledEntry, StatusLabel
from ui.plot_manager import PlotManager


class NelderMeadApp:
    """
    MVC Controller: связывает UI, модель и сервисы.
    Не содержит алгоритм оптимизации — делегирует optimizer.py.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Метод Нелдера-Мида")
        self.root.geometry("1100x750")

        self._is_running = False
        self._stop_flag = False
        self._history = []

        self._build_ui()
        self._plot_manager = PlotManager(self._plot_frame)

    def _build_ui(self) -> None:
        """Сборка интерфейса (только компоновка, без логики)."""
        # Панель управления
        panel = ttk.Frame(self.root, padding=10)
        panel.pack(side='left', fill='y')

        # Параметры
        self._n_entry = LabeledEntry(panel, "Размерность n:", width=10)
        self._n_entry.set("2")
        self._n_entry.pack(anchor='w', pady=5)

        self._x0_entry = LabeledEntry(panel, "x0 (через запятую):", width=25)
        self._x0_entry.set("-1.5, 2.0")
        self._x0_entry.pack(anchor='w', pady=5)

        self._func_entry = LabeledEntry(panel, "Функция f(x):", width=40)
        self._func_entry.set("(1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2")
        self._func_entry.pack(anchor='w', pady=5)

        # Кнопки
        btn_frame = ttk.Frame(panel)
        btn_frame.pack(pady=15)

        self._btn_start = ttk.Button(btn_frame, text="▶ Запуск", command=self._start)
        self._btn_start.pack(side='left', padx=5)

        self._btn_stop = ttk.Button(btn_frame, text="⏹ Стоп", command=self._stop, state='disabled')
        self._btn_stop.pack(side='left', padx=5)

        # Статус
        self._status = StatusLabel(panel, font=("Arial", 11, "bold"))
        self._status.pack(pady=10)

        self._result_label = ttk.Label(panel, text="", wraplength=280, font=("Consolas", 9))
        self._result_label.pack(anchor='w')

        # Область графиков
        self._plot_frame = ttk.Frame(self.root)
        self._plot_frame.pack(side='right', fill='both', expand=True)

    def _parse_config(self) -> tuple:
        """Парсинг и валидация входных данных."""
        n = int(self._n_entry.get())
        x0 = np.array([float(v.strip()) for v in self._x0_entry.get().split(',')])

        if len(x0) != n:
            raise ValueError(f"Длина x0 ({len(x0)}) ≠ n ({n})")

        objective = FunctionEvaluator.safe_eval(self._func_entry.get())

        config = NelderMeadConfig()
        config.validate()

        return n, x0, objective, config

    def _start(self) -> None:
        """Обработчик запуска."""
        if self._is_running:
            return

        try:
            self._n, self._x0, self._objective, self._config = self._parse_config()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return

        self._is_running = True
        self._stop_flag = False
        self._history = []

        self._btn_start.config(state='disabled')
        self._btn_stop.config(state='normal')
        self._status.set_status('running', "⚙️ Вычисление...")
        self._result_label.config(text="")

        # Фоновый поток
        thread = threading.Thread(target=self._worker, daemon=True)
        thread.start()

        # Обновление UI
        self._update_loop()

    def _worker(self) -> None:
        """Фоновая работа (не блокирует UI)."""
        optimizer = NelderMeadOptimizer(self._config)

        def callback(state: IterationState) -> bool:
            self._history.append(state)
            return not self._stop_flag

        result = optimizer.run(self._objective, self._x0, callback)

        # Возврат в главный поток
        self.root.after(0, self._on_finish, result)

    def _update_loop(self) -> None:
        """Цикл обновления графиков."""
        if self._history:
            iterations = [s.iteration for s in self._history]
            best = [s.best_f for s in self._history]
            worst = [s.worst_f for s in self._history]
            self._plot_manager.draw_convergence(iterations, best, worst)

        if self._is_running or self._history:
            self.root.after(50, self._update_loop)

    def _on_finish(self, result) -> None:
        """Завершение оптимизации."""
        self._is_running = False
        self._btn_start.config(state='normal')
        self._btn_stop.config(state='disabled')
        self._status.set_status('done', "✅ Завершено")

        x_str = ", ".join(f"{v:.6f}" for v in result.x)
        self._result_label.config(
            text=f"x* = [{x_str}]\n"
                 f"f(x*) = {result.f:.6e}\n"
                 f"Итераций: {result.iterations}"
        )

    def _stop(self) -> None:
        """Остановка."""
        self._stop_flag = True
        self._is_running = False
        self._status.set_status('stopped', "⏹ Остановлено")