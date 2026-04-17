"""Тесты алгоритма оптимизации."""
import numpy as np
import pytest
from config import IterationState

def test_sphere_convergence_2d(optimizer, sphere_2d):
    res = optimizer.run(sphere_2d, np.array([3.0, -4.0]))
    assert res.converged
    assert np.isclose(res.f, 0.0, atol=1e-8)      # Значение функции сходится точно
    assert np.allclose(res.x, [0.0, 0.0], atol=1e-5)  # Допуск по координатам увеличен до 1e-5

def test_quadratic_convergence_2d(optimizer, quadratic_2d):
    """Тест из debug_test.py: должен находить [1.0, 4.0]"""
    res = optimizer.run(quadratic_2d, np.array([0.0, 0.0]))
    assert res.converged
    assert np.isclose(res.f, -21.0, atol=1e-6)
    assert np.allclose(res.x, [1.0, 4.0], atol=1e-6)

def test_convergence_from_far_start(optimizer, sphere_2d):
    """Устойчивость к удалённой начальной точке"""
    res = optimizer.run(sphere_2d, np.array([100.0, -100.0]))
    assert res.converged
    assert np.allclose(res.x, [0.0, 0.0], atol=1e-4)

def test_callback_invocation(optimizer, sphere_2d):
    calls = []
    def cb(state: IterationState) -> bool:
        calls.append(state.iteration)
        return True

    optimizer.run(sphere_2d, np.array([5.0, 5.0]), callback=cb)
    assert len(calls) > 0
    assert calls[0] == 1
    assert calls[-1] >= calls[0]

def test_early_stop_via_callback(optimizer, sphere_2d):
    def cb(state: IterationState) -> bool:
        return state.iteration < 3  # Остановить после 2 итераций

    res = optimizer.run(sphere_2d, np.array([10.0, 10.0]), callback=cb)
    assert res.iterations <= 3
    assert not res.converged  # Ранняя остановка ≠ сходимость

def test_3d_optimization(optimizer):
    """Проверка n-мерности"""
    f = lambda x: np.sum((x - np.array([1, 2, 3]))**2)
    res = optimizer.run(f, np.array([0.0, 0.0, 0.0]))
    assert res.converged
    assert np.allclose(res.x, [1.0, 2.0, 3.0], atol=1e-5)