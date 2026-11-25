import pytest

from num_series.moving_average import (
    centered_moving_average,
    exponential_moving_average,
    simple_moving_average,
)


# ---------- simple_moving_average ----------

def test_sma_window_2():
    """Окно 2: средние соседних пар."""
    assert simple_moving_average([1, 2, 3, 4, 5], 2) == [1.5, 2.5, 3.5, 4.5]


def test_sma_window_3():
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_sma_window_equals_length():
    """Окно во всю длину ряда — одно значение, среднее всего ряда."""
    assert simple_moving_average([2, 4, 6, 8], 4) == [5.0]


def test_sma_result_length():
    """Длина результата: len(data) - window + 1."""
    data = list(range(50))
    for window in (1, 2, 5, 10):
        res = simple_moving_average(data, window)
        assert len(res) == len(data) - window + 1


def test_sma_window_1_returns_copy():
    assert simple_moving_average([3.5, 7.0, -1], 1) == [3.5, 7.0, -1]


def test_sma_constant_series():
    assert simple_moving_average([5, 5, 5, 5], 3) == [5.0, 5.0]


def test_sma_running_sum_matches_naive():
    """Бегущая сумма должна давать тот же результат, что и наивный расчёт."""
    data = [1.5, 2.2, -0.3, 4.7, 8.1, 2.0]
    window = 3
    naive = [sum(data[i:i + window]) / window for i in range(len(data) - window + 1)]
    assert simple_moving_average(data, window) == pytest.approx(naive)


def test_sma_bad_window():
    data = [1, 2, 3]
    with pytest.raises(ValueError):
        simple_moving_average(data, 0)
    with pytest.raises(ValueError):
        simple_moving_average(data, -2)
    with pytest.raises(ValueError):
        simple_moving_average(data, 4)  # больше длины ряда
    with pytest.raises(ValueError):
        simple_moving_average(data, True)  # bool не считается int-ом
    with pytest.raises(ValueError):
        simple_moving_average(data, 2.5)  # не целое


def test_sma_empty_data():
    with pytest.raises(ValueError):
        simple_moving_average([], 1)


# ---------- centered_moving_average ----------

def test_cma_window_3():
    """Окно 3 по центру: [1,2,3,4,5] -> [2, 3, 4]."""
    assert centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_cma_length():
    """len(data) - window + 1, как и у SMA."""
    data = list(range(20))
    res = centered_moving_average(data, 5)
    assert len(res) == 20 - 5 + 1


def test_cma_even_window_raises():
    with pytest.raises(ValueError):
        centered_moving_average([1, 2, 3, 4, 5], 2)
    with pytest.raises(ValueError):
        centered_moving_average([1, 2, 3, 4, 5], 4)


def test_cma_window_1():
    """Окно 1 (нечётное) — возвращается сам ряд."""
    assert centered_moving_average([4.0, 5.0, 6.0], 1) == [4.0, 5.0, 6.0]


def test_cma_constant_series():
    assert centered_moving_average([7, 7, 7, 7, 7], 3) == [7.0, 7.0, 7.0]


def test_cma_bad_window_and_empty():
    with pytest.raises(ValueError):
        centered_moving_average([1, 2, 3], 5)  # окно больше ряда
    with pytest.raises(ValueError):
        centered_moving_average([], 3)


# ---------- exponential_moving_average ----------

def test_ema_known_values():
    """EMA[0] = 1; далее 0.5*x + 0.5*prev."""
    res = exponential_moving_average([1, 2, 3], 0.5)
    assert res == pytest.approx([1.0, 1.5, 2.25])


def test_ema_alpha_1_is_copy():
    """При alpha = 1 EMA повторяет исходный ряд."""
    res = exponential_moving_average([3.0, -1.0, 4.5], 1.0)
    assert res == pytest.approx([3.0, -1.0, 4.5])


def test_ema_length_matches_input():
    data = list(range(10))
    assert len(exponential_moving_average(data, 0.3)) == 10


def test_ema_smoothness():
    """EMA с маленьким alpha должен сглаживать: колебания меньше исходных."""
    data = [0, 10, 0, 10, 0, 10]
    res = exponential_moving_average(data, 0.1)
    src_range = max(data) - min(data)          # 10
    ema_range = max(res) - min(res)
    assert ema_range < src_range


def test_ema_converges_to_constant():
    """При постоянном ряде EMA стремится к этому же значению."""
    res = exponential_moving_average([5.0] * 30, 0.5)
    assert res == pytest.approx([5.0] * 30)


def test_ema_bad_alpha():
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2, 3], 0.0)
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2, 3], -0.5)
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2, 3], 1.5)


def test_ema_empty_data():
    with pytest.raises(ValueError):
        exponential_moving_average([], 0.5)
