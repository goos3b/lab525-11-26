import pytest

from num_series.generator import (
    random_series,
    sine_series,
    trend_series,
    uniform_series,
    validate_n,
)


# ---------- validate_n ----------

def test_validate_n_ok():
    """Корректные значения не должны вызывать исключений."""
    for n in (1, 5, 100, 1000):
        validate_n(n)  # если дойдёт до конца — тест пройден


@pytest.mark.parametrize("bad", [0, -1, -100, 2.5, "10", None])
def test_validate_n_bad(bad):
    """Некорректные n должны вызывать ValueError."""
    with pytest.raises(ValueError):
        validate_n(bad)


# ---------- random_series ----------

def test_random_series_length():
    assert len(random_series(10, seed=42)) == 10
    assert len(random_series(100, low=-5, high=5, seed=1)) == 100


def test_random_series_range():
    data = random_series(1000, low=10.0, high=20.0, seed=7)
    assert all(10.0 <= x <= 20.0 for x in data)


def test_random_series_reproducible():
    """Одинаковый seed — одинаковый ряд."""
    assert random_series(50, seed=123) == random_series(50, seed=123)


def test_random_series_different_seed():
    """Разные seed — разные ряды (почти наверняка)."""
    assert random_series(50, seed=1) != random_series(50, seed=2)


def test_random_series_bad_n():
    with pytest.raises(ValueError):
        random_series(0)
    with pytest.raises(ValueError):
        random_series(-3)


def test_random_series_low_not_less_high():
    with pytest.raises(ValueError):
        random_series(10, low=5.0, high=5.0)
    with pytest.raises(ValueError):
        random_series(10, low=10.0, high=1.0)


# ---------- uniform_series ----------

def test_uniform_series_length_and_range():
    data = uniform_series(500, low=-1.0, high=1.0, seed=99)
    assert len(data) == 500
    assert all(-1.0 <= x <= 1.0 for x in data)


def test_uniform_series_reproducible():
    assert uniform_series(20, seed=5) == uniform_series(20, seed=5)


def test_uniform_series_bad_range():
    with pytest.raises(ValueError):
        uniform_series(10, low=3.0, high=3.0)


# ---------- sine_series ----------

def test_sine_series_length():
    assert len(sine_series(30, seed=0)) == 30


def test_sine_series_clean_no_noise_within_amplitude():
    """Без шума значения не выходят за амплитуду."""
    data = sine_series(200, amplitude=2.0, frequency=3.0, noise=0.0)
    assert all(-2.0 <= x <= 2.0 for x in data)


def test_sine_series_reproducible_with_noise():
    assert sine_series(50, noise=0.5, seed=11) == sine_series(50, noise=0.5, seed=11)


def test_sine_series_bad_params():
    with pytest.raises(ValueError):
        sine_series(10, amplitude=-1.0)
    with pytest.raises(ValueError):
        sine_series(10, frequency=0)
    with pytest.raises(ValueError):
        sine_series(10, noise=-0.1)


# ---------- trend_series ----------

def test_trend_series_exact_values():
    """Без шума тренд — точная арифметическая прогрессия."""
    assert trend_series(5, start=0, step=2) == [0.0, 2.0, 4.0, 6.0, 8.0]


def test_trend_series_with_noise_stays_close():
    """С небольшим шумом точки близки к идеальному тренду."""
    ideal = trend_series(100, start=0, step=1, noise=0.0)
    noisy = trend_series(100, start=0, step=1, noise=0.1, seed=3)
    assert all(abs(a - b) <= 0.1 for a, b in zip(ideal, noisy))


def test_trend_series_reproducible():
    assert trend_series(20, noise=1.0, seed=8) == trend_series(20, noise=1.0, seed=8)


def test_trend_series_bad_n():
    with pytest.raises(ValueError):
        trend_series(0)
