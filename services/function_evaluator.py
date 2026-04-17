"""Service: Безопасное вычисление целевой функции."""
from typing import Callable
import numpy as np
import math


class FunctionEvaluator:
    """
    Инкапсулирует логику вычисления функции.
    Позволяет добавить кэширование, логирование, валидацию.
    """

    def __init__(self, func: Callable[[np.ndarray], float]):
        self._func = func
        self._eval_count = 0

    def evaluate(self, x: np.ndarray) -> float:
        self._eval_count += 1
        return self._func(x)

    @property
    def eval_count(self) -> int:
        return self._eval_count

    @staticmethod
    def safe_eval(expression: str) -> Callable[[np.ndarray], float]:
        """
        Создаёт функцию из строки с ограниченным окружением.
        YAGNI: не добавляем парсинг, пока не потребуется.
        """
        safe_globals = {
            'x': None, 'np': np, 'math': math,
            'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'sqrt': np.sqrt,
            'sum': sum, 'abs': abs, '__builtins__': {}
        }

        def evaluator(x: np.ndarray) -> float:
            safe_globals['x'] = x
            return eval(expression, safe_globals)

        return evaluator