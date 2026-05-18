import numpy as np
import pytest
from config import IterationState

def test_sphere_2d_simple(optimizer, sphere_2d):
    """Сходимость на простой 2D сфере"""
    res = optimizer.run(sphere_2d, np.array([3.0, -4.0]))
    assert res.converged
    assert np.allclose(res.x, [0.0, 0.0], atol=1e-5)

def test_quadratic_2d_simple(optimizer, quadratic_2d):
    """Сходимость на квадратичной функции 2D"""
    res = optimizer.run(quadratic_2d, np.array([0.0, 0.0]))
    assert res.converged
    assert np.allclose(res.x, [1.0, 4.0], atol=1e-5)

def test_far_start_simple(optimizer, sphere_2d):
    """Начало из удалённой точки"""
    res = optimizer.run(sphere_2d, np.array([100.0, -100.0]))
    assert res.converged
    assert np.allclose(res.x, [0.0, 0.0], atol=1e-4)

def test_callback_simple(optimizer, sphere_2d):
    """Проверка вызова callback"""
    calls = []
    def cb(state: IterationState):
        calls.append(state.iteration)
        return True
    optimizer.run(sphere_2d, np.array([5.0, 5.0]), callback=cb)
    assert calls  # хотя бы один вызов

def test_early_stop_simple(optimizer, sphere_2d):
    """Преждевременная остановка через callback"""
    def cb(state: IterationState):
        return state.iteration < 3
    res = optimizer.run(sphere_2d, np.array([10.0, 10.0]), callback=cb)
    assert res.iterations <= 3
    assert not res.converged

def test_3d_simple(optimizer):
    """Сходимость в 3D"""
    f = lambda x: np.sum((x - np.array([1,2,3]))**2)
    res = optimizer.run(f, np.array([0.0,0.0,0.0]))
    assert res.converged
    assert np.allclose(res.x, [1,2,3], atol=1e-5)