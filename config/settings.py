"""DTO: Конфигурация и результаты (только данные, без логики)."""
from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np


@dataclass
class NelderMeadConfig:
    """Параметры алгоритма (согласно Википедии)."""
    alpha: float = 1.0  # коэффициент отражения
    beta: float = 0.5  # коэффициент сжатия
    gamma: float = 2.0  # коэффициент растяжения
    max_iter: int = 1000
    tolerance: float = 1e-8

    def validate(self) -> None:
        """Проверка инвариантов (вызывается при создании)."""
        if self.alpha <= 0:
            raise ValueError("alpha должен быть > 0")
        if self.beta <= 0:
            raise ValueError("beta должен быть > 0")
        if self.gamma <= 1:
            raise ValueError("gamma должен быть > 1")


@dataclass
class OptimizationResult:
    """Результат оптимизации."""
    x: np.ndarray
    f: float
    iterations: int
    converged: bool


@dataclass
class IterationState:
    """Состояние на одной итерации (для UI)."""
    iteration: int
    best_f: float
    worst_f: float
    operation: str