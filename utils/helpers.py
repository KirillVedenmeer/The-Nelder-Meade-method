"""Pure functions: утилиты без состояния (легко тестировать)."""
import numpy as np
from typing import List


def parse_vector(s: str, dtype=float) -> np.ndarray:
    """Парсит строку '1, 2, 3' в numpy-массив."""
    return np.array([dtype(v.strip()) for v in s.split(',')])


def format_vector(v: np.ndarray, precision: int = 6) -> str:
    """Форматирует вектор для вывода."""
    return ", ".join(f"{x:.{precision}f}" for x in v)


def clamp(value: float, min_v: float, max_v: float) -> float:
    """Ограничивает значение диапазоном."""
    return max(min_v, min(value, max_v))