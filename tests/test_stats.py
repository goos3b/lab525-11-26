import math

import pytest

from num_series.stats import (
    mean,
    median,
    spread,
    stdev,
    summarize,
    variance,
)


# ---------- mean ----------

def test_mean_simple():
    assert mean([1, 2, 3, 4]) == 2.5


def test_mean_single_element():
    assert mean([5]) == 5.0


def test_mean_negative():
    assert mean([-1, -2, -3]) == -2.0


# ---------- median ----------

def test_median_odd_count():
    assert median([3, 1, 2]) == 2.0


def test_median_odd_count_unsorted():
    """Вход не обязан быть отсортированным."""
    assert median([10, 30, 20, 50, 40]) == 30.0


def test_median_even_count():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_single():
    assert median([7]) == 7.0


# ---------- spread ----------

def test_spread_simple():
    assert spread([1, 5]) == 4.0


def test_spread_all_equal():
    assert spread([3.0, 3.0, 3.0]) == 0.0


def test_spread_negative_values():
    assert spread([-10, -2]) == 8.0


# ---------- variance и stdev ----------

def test_variance_known_value():
    """Контрольный пример: [1, 2, 3, 4], несмещённая дисперсия = 5/3."""
    assert math.isclose(variance([1, 2, 3, 4]), 5 / 3)


def test_variance_needs_two_values():
    with pytest.raises(ValueError):
        variance([1])


def test_stdev_is_sqrt_of_variance():
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    assert math.isclose(stdev(data), math.sqrt(variance(data)))


def test_stdev_known_value():
    """Классический пример: СКО этого ряда = 2."""
    assert math.isclose(stdev([2, 4, 4, 4, 5, 5, 7, 9]), 2.0)


# ---------- summarize ----------

def test_summarize_keys_and_values():
    result = summarize([1, 2, 3, 4])
    assert result["count"] == 4
    assert result["mean"] == 2.5
    assert result["median"] == 2.5
    assert result["spread"] == 3.0
    assert result["min"] == 1
    assert result["max"] == 4
    # при len >= 2 есть дисперсия и СКО
    assert "variance" in result
    assert "stdev" in result


def test_summarize_single_element_no_variance():
    result = summarize([42])
    assert result["count"] == 1
    assert result["mean"] == 42
    assert "variance" not in result
    assert "stdev" not in result


# ---------- обработка некорректного ввода ----------

@pytest.mark.parametrize("bad", [None, "abc", 123, {"a": 1}])
def test_rejects_non_list_input(bad):
    with pytest.raises(ValueError):
        mean(bad)


def test_rejects_empty_series():
    for func in (mean, median, spread, summarize):
        with pytest.raises(ValueError):
            func([])


def test_rejects_non_numeric_values():
    with pytest.raises(ValueError):
        mean([1, 2, "3"])


def test_rejects_booleans():
    """True/False — это bool, в твоей проверке они не считаются числами."""
    with pytest.raises(ValueError):
        mean([True, False])
import math

import pytest

from num_series.stats import (
    mean,
    median,
    spread,
    stdev,
    summarize,
    variance,
)


# ---------- mean ----------

def test_mean_simple():
    assert mean([1, 2, 3, 4]) == 2.5


def test_mean_single_element():
    assert mean([5]) == 5.0


def test_mean_negative():
    assert mean([-1, -2, -3]) == -2.0


# ---------- median ----------

def test_median_odd_count():
    assert median([3, 1, 2]) == 2.0


def test_median_odd_count_unsorted():
    """Вход не обязан быть отсортированным."""
    assert median([10, 30, 20, 50, 40]) == 30.0


def test_median_even_count():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_single():
    assert median([7]) == 7.0


# ---------- spread ----------

def test_spread_simple():
    assert spread([1, 5]) == 4.0


def test_spread_all_equal():
    assert spread([3.0, 3.0, 3.0]) == 0.0


def test_spread_negative_values():
    assert spread([-10, -2]) == 8.0


# ---------- variance и stdev ----------

def test_variance_known_value():
    """Контрольный пример: [1, 2, 3, 4], несмещённая дисперсия = 5/3."""
    assert math.isclose(variance([1, 2, 3, 4]), 5 / 3)


def test_variance_needs_two_values():
    with pytest.raises(ValueError):
        variance([1])


def test_stdev_is_sqrt_of_variance():
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    assert math.isclose(stdev(data), math.sqrt(variance(data)))


def test_stdev_known_value():
    """Ряд [0, 2, 4]: среднее = 2, сумма квадратов отклонений = 8,
    выборочная дисперсия = 8 / (3 - 1) = 4, СКО = 2.0."""
    assert math.isclose(stdev([0, 2, 4]), 2.0)
# ---------- summarize ----------

def test_summarize_keys_and_values():
    result = summarize([1, 2, 3, 4])
    assert result["count"] == 4
    assert result["mean"] == 2.5
    assert result["median"] == 2.5
    assert result["spread"] == 3.0
    assert result["min"] == 1
    assert result["max"] == 4
    # при len >= 2 есть дисперсия и СКО
    assert "variance" in result
    assert "stdev" in result


def test_summarize_single_element_no_variance():
    result = summarize([42])
    assert result["count"] == 1
    assert result["mean"] == 42
    assert "variance" not in result
    assert "stdev" not in result


# ---------- обработка некорректного ввода ----------

@pytest.mark.parametrize("bad", [None, "abc", 123, {"a": 1}])
def test_rejects_non_list_input(bad):
    with pytest.raises(ValueError):
        mean(bad)


def test_rejects_empty_series():
    for func in (mean, median, spread, summarize):
        with pytest.raises(ValueError):
            func([])


def test_rejects_non_numeric_values():
    with pytest.raises(ValueError):
        mean([1, 2, "3"])


def test_rejects_booleans():
    """True/False — это bool, в твоей проверке они не считаются числами."""
    with pytest.raises(ValueError):
        mean([True, False])
