"""Тесты по заданию Варианта 1."""
import pytest

from num_series.generator import random_series
from num_series.stats import mean, stdev, variance
from num_series.moving_average import (
    exponential_moving_average,
    simple_moving_average,
)


# ---------- Ряд: 1000 чисел, равномерное [0, 100], float, seed ----------

def test_series_size_and_bounds():
    data = random_series(1000, seed=1)
    assert len(data) == 1000
    assert all(0.0 <= x <= 100.0 for x in data)
    assert all(isinstance(x, float) for x in data)


def test_series_reproducible_with_seed():
    """Seed фиксирует ряд: две генерации с одинаковым seed совпадают."""
    assert random_series(1000, seed=7) == random_series(1000, seed=7)


def test_series_different_seeds_differ():
    assert random_series(1000, seed=1) != random_series(1000, seed=2)


def test_series_uniform_mean():
    """Статистическая проверка: среднее равномерного [0, 100] близко к 50."""
    data = random_series(10_000, seed=42)
    assert mean(data) == pytest.approx(50.0, abs=1.0)


# ---------- Показатели: выборочная дисперсия и СКО ----------

def test_variance_sample_formula():
    """Выборочная дисперсия: делим на (n-1), а не на n. Контрольный расчёт."""
    data = [2.0, 4.0, 6.0, 8.0]
    m = mean(data)  # 5.0
    expected = sum((x - m) ** 2 for x in data) / (len(data) - 1)  # 13.333...
    assert variance(data) == pytest.approx(expected)


def test_stdev_is_sqrt_variance():
    data = random_series(100, seed=3)
    assert stdev(data) == pytest.approx(variance(data) ** 0.5)


# ---------- Краевой кейс: ряд с отрицательными числами ----------

def test_negative_series_stats_correct():
    """Статистика корректна и для отрицательных значений (выборочная дисперсия, n-1)."""
    data = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]
    assert mean(data) == pytest.approx(0.0)
    # сумма квадратов 70, делённая на (n-1)=5 -> 14.0
    assert variance(data) == pytest.approx(14.0)
    assert stdev(data) == pytest.approx(14.0 ** 0.5)


def test_negative_series_moving_averages():
    data = [-10.0, -20.0, -30.0, -40.0, -50.0]
    assert simple_moving_average(data, 3) == pytest.approx([-20.0, -30.0, -40.0])


# ---------- Скользящие средние по варианту: EMA с alpha = 2/(k+1) ----------

def test_ema_alpha_formula_2_over_k_plus_1():
    """EMA по варианту: alpha = 2/(k+1). Для окна k=4 -> alpha = 0.4.

    Контрольный расчёт: ряд [1, 2, 3]
    EMA[0] = 1
    EMA[1] = 0.4*2 + 0.6*1 = 1.4
    EMA[2] = 0.4*3 + 0.6*1.4 = 2.04
    """
    alpha = 2 / (4 + 1)
    assert exponential_moving_average([1.0, 2.0, 3.0], alpha) == pytest.approx(
        [1.0, 1.4, 2.04]
    )


def test_full_pipeline_variant1():
    """Сквозной прогон как в задании: ряд 1000 -> статистика -> средние."""
    data = random_series(1000, seed=11)
    assert len(simple_moving_average(data, 5)) == 996
    alpha = 2 / (5 + 1)
    assert len(exponential_moving_average(data, alpha)) == 1000
    # СКО равномерного [0, 100]: 100/sqrt(12) ~ 28.87
    assert stdev(data) == pytest.approx(28.87, abs=1.0)
