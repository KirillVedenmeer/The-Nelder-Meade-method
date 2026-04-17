"""Strategy: Операции над симплексом (открыто для расширения, закрыто для изменения)."""
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
import numpy as np

from .simplex import Simplex, Vertex


@runtime_checkable
class Operation(Protocol):
    """Интерфейс операции (легковесный, без ABC для гибкости)."""

    def execute(self, simplex: Simplex, config) -> Vertex:
        """Выполняет операцию, возвращает новую вершину."""
        ...

    @property
    def name(self) -> str:
        """Человекочитаемое имя операции."""
        ...


class ReflectOperation:
    """Отражение: xr = (1+α)xc - αxh"""
    name = "reflect"

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha

    def execute(self, simplex: Simplex, config) -> Vertex:
        xc = simplex.centroid_excluding(-1)
        xh = simplex.worst.point
        xr = (1 + self.alpha) * xc - self.alpha * xh
        return Vertex(xr)


class ExpandOperation:
    """Растяжение: xe = (1-γ)xc + γxr"""
    name = "expand"

    def __init__(self, gamma: float = 2.0):
        self.gamma = gamma

    def execute(self, simplex: Simplex, config) -> Vertex:
        # Предполагаем, что отражение уже вычислено и хранится во временной переменной
        # В реальном использовании передаётся xr через config или аргумент
        xc = simplex.centroid_excluding(-1)
        xr = getattr(config, '_xr', simplex.centroid_excluding(-1))  # fallback
        xe = (1 - self.gamma) * xc + self.gamma * xr
        return Vertex(xe)


class ContractOperation:
    """Сжатие: xs = βxh + (1-β)xc"""
    name = "contract"

    def __init__(self, beta: float = 0.5):
        self.beta = beta

    def execute(self, simplex: Simplex, config) -> Vertex:
        xc = simplex.centroid_excluding(-1)
        xh = simplex.worst.point
        xs = self.beta * xh + (1 - self.beta) * xc
        return Vertex(xs)  # ← Исправлено! Было Vertex(xe)


class ShrinkOperation:
    """Глобальное сжатие (не создаёт новую вершину, модифицирует симплекс)."""
    name = "shrink"

    def execute(self, simplex: Simplex, config) -> None:
        simplex.shrink_towards_best(0.5)
        return None