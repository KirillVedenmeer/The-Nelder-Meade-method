"""Тесты геометрии симплекса."""
import numpy as np
import pytest
from core.simplex import Simplex, Vertex

@pytest.fixture
def simple_1d():
    """1D симплекс: точки 2.0 (f=4), -1.0 (f=1), 0.0 (f=0)"""
    v1 = Vertex(np.array([2.0]), 4.0)
    v2 = Vertex(np.array([-1.0]), 1.0)
    v3 = Vertex(np.array([0.0]), 0.0)
    return Simplex([v1, v2, v3])

def test_sorting(simple_1d):
    assert simple_1d.best.value == 0.0
    assert simple_1d.second_worst.value == 1.0
    assert simple_1d.worst.value == 4.0
    assert np.array_equal(simple_1d.best.point, [0.0])

def test_centroid_excluding_worst(simple_1d):
    # Центроид без худшей (4.0) = среднее от [0.0, -1.0]
    c = simple_1d.centroid_excluding_worst()
    assert np.isclose(c[0], -0.5)

def test_replace_worst_resorts(simple_1d):
    new_v = Vertex(np.array([-0.1]), 0.01)
    simple_1d.replace_worst(new_v)
    # Старая вторая худшая (1.0) становится худшей
    assert simple_1d.worst.value == 1.0
    assert simple_1d.best.value == 0.0

def test_shrink_reduces_diameter(simple_1d):
    initial_diam = simple_1d.diameter()
    simple_1d.shrink_towards_best(lambda x: x[0]**2, factor=0.5)
    assert simple_1d.diameter() < initial_diam

def test_from_point_adaptive_scale():
    x0 = np.array([10.0, -20.0])
    s = Simplex.from_point(x0, step=0.1)
    # Проверка адаптивного шага
    assert not np.allclose(s._vertices[1].point - x0, 0.05)
    # Проверка размерности и количества вершин
    assert len(s.best.point) == 2
    assert len(s._vertices) == 3  # ← Исправлено: используем len() вместо s.size