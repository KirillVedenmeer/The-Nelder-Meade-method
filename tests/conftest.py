"""Общие фикстуры для всех тестов."""
import pytest
import numpy as np
from config.settings import NelderMeadConfig
from core.optimizer import NelderMeadOptimizer

@pytest.fixture
def optimizer():
    """Готовый оптимизатор со строгими параметрами для тестов."""
    cfg = NelderMeadConfig(max_iter=500, tolerance=1e-10)
    return NelderMeadOptimizer(cfg)

@pytest.fixture
def sphere_2d():
    """f(x,y) = x² + y², min в (0,0) = 0"""
    return lambda x: x[0]**2 + x[1]**2

@pytest.fixture
def quadratic_2d():
    """f(x,y) = x² + xy + y² - 6x - 9y, min в (1,4) = -21"""
    return lambda x: x[0]**2 + x[0]*x[1] + x[1]**2 - 6*x[0] - 9*x[1]