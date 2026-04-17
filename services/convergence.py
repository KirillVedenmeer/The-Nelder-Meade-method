"""Strategy: Критерии остановки (открыто для добавления новых)."""
from abc import ABC, abstractmethod
import numpy as np

from core.simplex import Simplex


class ConvergenceStrategy(ABC):
    @abstractmethod
    def is_met(self, simplex: Simplex) -> bool:
        pass


class VarianceStrategy(ConvergenceStrategy):
    """Сходимость по дисперсии значений функции."""

    def __init__(self, tolerance: float):
        self.tolerance = tolerance

    def is_met(self, simplex: Simplex) -> bool:
        return np.std(simplex.get_values()) < self.tolerance


class DiameterStrategy(ConvergenceStrategy):
    """Сходимость по размеру симплекса."""

    def __init__(self, tolerance: float):
        self.tolerance = tolerance

    def is_met(self, simplex: Simplex) -> bool:
        return simplex.diameter() < self.tolerance


class ConvergenceChecker:
    """Facade для проверки сходимости."""

    def __init__(self, strategies: list[ConvergenceStrategy]):
        self._strategies = strategies

    def has_converged(self, simplex: Simplex) -> bool:
        return any(s.is_met(simplex) for s in self._strategies)

    @classmethod
    def default(cls, tolerance: float) -> 'ConvergenceChecker':
        return cls([
            VarianceStrategy(tolerance),
            DiameterStrategy(tolerance * 10)  # чуть мягче для диаметра
        ])