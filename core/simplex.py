"""Domain Model: Симплекс (управление геометрией вершин)."""
from dataclasses import dataclass
from typing import List, Callable
import numpy as np


@dataclass
class Vertex:
    point: np.ndarray
    value: float = float('inf')

    def evaluate(self, func: Callable) -> None:
        self.value = func(self.point)


class Simplex:
    def __init__(self, vertices: List[Vertex]):
        self._vertices = vertices
        self._sort()

    @classmethod
    def from_point(cls, x0: np.ndarray, step: float = 0.1) -> 'Simplex':
        """Создаёт начальный симплекс с адаптивным масштабом."""
        n = len(x0)
        vertices = [Vertex(x0.copy())]
        for i in range(n):
            point = x0.copy()
            # Адаптивный шаг: 10% от масштаба координаты или минимум 0.1
            delta = step * max(1.0, abs(x0[i]))
            point[i] += delta
            vertices.append(Vertex(point))
        return cls(vertices)

    def _sort(self) -> None:
        self._vertices.sort(key=lambda v: v.value)

    @property
    def best(self) -> Vertex: return self._vertices[0]
    @property
    def worst(self) -> Vertex: return self._vertices[-1]
    @property
    def second_worst(self) -> Vertex: return self._vertices[-2]

    def centroid_excluding_worst(self) -> np.ndarray:
        """Центроид без худшей вершины (индекс -1 после сортировки)."""
        return np.mean([v.point for v in self._vertices[:-1]], axis=0)

    def replace_worst(self, vertex: Vertex) -> None:
        self._vertices[-1] = vertex
        self._sort()

    def shrink_towards_best(self, func: Callable, factor: float = 0.5) -> None:
        """Глобальное сжатие к лучшей вершине с пересчётом значений."""
        xl = self.best.point
        for i in range(1, len(self._vertices)):
            self._vertices[i].point = xl + factor * (self._vertices[i].point - xl)
            self._vertices[i].evaluate(func)
        self._sort()

    def get_values(self) -> List[float]:
        return [v.value for v in self._vertices]

    def diameter(self) -> float:
        best = self.best.point
        return max(np.linalg.norm(v.point - best) for v in self._vertices[1:])