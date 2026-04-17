"""Тесты валидации конфигурации."""
import pytest
from config.settings import NelderMeadConfig

def test_valid_default_config():
    cfg = NelderMeadConfig()
    cfg.validate()  # Не должно выбрасывать исключений

def test_invalid_alpha():
    with pytest.raises(ValueError, match="alpha"):
        NelderMeadConfig(alpha=-0.5).validate()

def test_invalid_beta():
    with pytest.raises(ValueError, match="beta"):
        NelderMeadConfig(beta=0.0).validate()

def test_invalid_gamma():
    with pytest.raises(ValueError, match="gamma"):
        NelderMeadConfig(gamma=0.8).validate()