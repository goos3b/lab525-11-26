import pytest

from num_series.deque_average import (
    centered_moving_average_deque,
    exponential_moving_average_deque,
    simple_moving_average_deque,
)
from num_series.generator import random_series
from num_series.moving_average import (
    centered_moving_average,
    exponential_moving_average,
    simple_moving_average,
)


# ---------- совпадение с обычными версиями ----------

def test_sma_deque_matches_sma():
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    for window in (1, 2, 3, 5, 10):
        assert simple_moving_average_deque(data, window) == pytest.approx(
            simple_moving_average(data, window)
        )


def test_sma_deque_matches_sma_on_random_series():
    data = random_series(200, seed=42)
    for window in (1, 3, 7, 50, 200):
        assert simple_moving_average_deque(data, window) == pytest.approx(
            simple_moving_average(data, window)
        )


def test_cma_deque_matches_cma():
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    for window in (1, 3, 5, 7):
        assert centered_moving_average_deque(data, window) == pytest.approx(
            centered_moving_average(data, window)
        )


def test_cma_deque_known_values():
    assert centered_moving_average_deque([1, 2, 3, 4, 5], 3) == pytest.approx([2.0, 3.0, 4.0])


def test_ema_deque_matches_ema():
    data = [1.0, 2.0, -3.0, 4.0, 5.5, 0.0]
    for alpha in (0.1, 0.5, 1.0):
        assert exponential_moving_average_deque(data, alpha) == pytest.approx(
            exponential_moving_average(data, alpha)
        )


def test_ema_deque_known_values():
    res = exponential_moving_average_deque([1, 2, 3], 0.5)
    assert res == pytest.approx([1.0, 1.5, 2.25])


# ---------- длины и крайние случаи ----------

def test_sma_deque_result_length():
    data = list(range(30))
    for window in (1, 5, 10, 30):
        assert len(simple_moving_average_deque(data, window)) == 30 - window + 1


def test_sma_deque_window_equals_length():
    assert simple_moving_average_deque([2, 4, 6, 8], 4) == pytest.approx([5.0])


def test_sma_deque_constant_series():
    assert simple_moving_average_deque([5, 5, 5, 5, 5], 3) == pytest.approx([5.0, 5.0, 5.0])


# ---------- обработка ошибок ----------

def test_sma_deque_empty_data():
    with pytest.raises(ValueError):
        simple_moving_average_deque([], 1)


def test_sma_deque_bad_window():
    data = [1, 2, 3]
    with pytest.raises(ValueError):
        simple_moving_average_deque(data, 0)
    with pytest.raises(ValueError):
        simple_moving_average_deque(data, 4)     # окно больше ряда
    with pytest.raises(ValueError):
        simple_moving_average_deque(data, 2.5)   # не целое
    with pytest.raises(ValueError):
        simple_moving_average_deque(data, True)  # bool не считается целым


def test_cma_deque_even_window_raises():
    with pytest.raises(ValueError):
        centered_moving_average_deque([1, 2, 3, 4, 5], 2)


def test_cma_deque_empty_data():
    with pytest.raises(ValueError):
        centered_moving_average_deque([], 3)


def test_ema_deque_bad_alpha():
    with pytest.raises(ValueError):
        exponential_moving_average_deque([1, 2, 3], 0.0)
    with pytest.raises(ValueError):
        exponential_moving_average_deque([1, 2, 3], -0.5)
    with pytest.raises(ValueError):
        exponential_moving_average_deque([1, 2, 3], 1.5)


def test_ema_deque_empty_data():
    with pytest.raises(ValueError):
        exponential_moving_average_deque([], 0.5)
