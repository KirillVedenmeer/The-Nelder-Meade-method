"""Facade: Координация алгоритма (единственная ответственность — поток выполнения)."""
from typing import Callable, Optional, Protocol
import numpy as np

from config.settings import NelderMeadConfig, OptimizationResult, IterationState
from core.simplex import Simplex, Vertex


class Callback(Protocol):
    def __call__(self, state: IterationState) -> bool: ...


class NelderMeadOptimizer:
    def __init__(self, config: NelderMeadConfig):
        config.validate()
        self._cfg = config
        self._last_op = "init"

    def run(
        self,
        objective: Callable[[np.ndarray], float],
        x0: np.ndarray,
        callback: Optional[Callback] = None
    ) -> OptimizationResult:
        simplex = Simplex.from_point(x0)
        for v in simplex._vertices:
            v.evaluate(objective)
        simplex._sort()

        for iteration in range(1, self._cfg.max_iter + 1):
            self._step(simplex, objective)

            if callback:
                state = IterationState(
                    iteration=iteration,
                    best_f=simplex.best.value,
                    worst_f=simplex.worst.value,
                    operation=self._last_op
                )
                if not callback(state):
                    break

            if self._has_converged(simplex):
                break

        return OptimizationResult(
            x=simplex.best.point.copy(),
            f=simplex.best.value,
            iterations=iteration,
            converged=self._has_converged(simplex)
        )

    def _step(self, simplex: Simplex, objective: Callable) -> None:
        """Один шаг алгоритма строго по Википедии."""
        # ИСПРАВЛЕНО: вызываем новое имя метода без аргумента
        xc = simplex.centroid_excluding_worst()

        xh, fh = simplex.worst.point, simplex.worst.value
        fg = simplex.second_worst.value
        fl = simplex.best.value

        # 1. Отражение
        xr = xc + self._cfg.alpha * (xc - xh)
        fr = objective(xr)

        # 2. Анализ отражения
        if fl <= fr < fg:
            simplex.replace_worst(Vertex(xr, fr))
            self._last_op = "reflect"
        elif fr < fl:
            # 3. Растяжение
            xe = xc + self._cfg.gamma * (xr - xc)
            fe = objective(xe)
            if fe < fr:
                simplex.replace_worst(Vertex(xe, fe))
                self._last_op = "expand"
            else:
                simplex.replace_worst(Vertex(xr, fr))
                self._last_op = "reflect"
        elif fg <= fr < fh:
            # 4. Внешнее сжатие
            xc_out = xc + self._cfg.beta * (xr - xc)
            fc = objective(xc_out)
            if fc < fr:
                simplex.replace_worst(Vertex(xc_out, fc))
                self._last_op = "contract_out"
            else:
                self._shrink(simplex, objective)
        else:  # fr >= fh
            # 5. Внутреннее сжатие
            xc_in = xc + self._cfg.beta * (xh - xc)
            fc = objective(xc_in)
            if fc < fh:
                simplex.replace_worst(Vertex(xc_in, fc))
                self._last_op = "contract_in"
            else:
                self._shrink(simplex, objective)

    def _shrink(self, simplex: Simplex, objective: Callable) -> None:
        """Глобальное сжатие симплекса к лучшей вершине."""
        xl = simplex.best.point
        sigma = 0.5  # Стандартный коэффициент редукции
        for i in range(1, len(simplex._vertices)):
            simplex._vertices[i].point = xl + sigma * (simplex._vertices[i].point - xl)
            simplex._vertices[i].value = objective(simplex._vertices[i].point)
        simplex._sort()
        self._last_op = "shrink"

    def _has_converged(self, simplex: Simplex) -> bool:
        """Сходимость по дисперсии ИЛИ по размеру симплекса."""
        values = simplex.get_values()
        std_converged = np.std(values) < self._cfg.tolerance
        size_converged = simplex.diameter() < self._cfg.tolerance * 100  # допуск по размеру
        return std_converged or size_converged