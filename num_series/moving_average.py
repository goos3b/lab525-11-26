from typing import Sequence


def check_window(window: int, n: int) -> None:
    """Window — целое >= 1; window <= n (иначе окно больше длины ряда)."""
    if isinstance(window, bool) or not isinstance(window, int):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(f"window ({window}) больше длины ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> list:
    """SMA через бегущую сумму, O(n). Длина результата: len(data) - window + 1."""
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")
    check_window(window, len(data))

    running = sum(data[:window])
    result = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def centered_moving_average(data: Sequence[float], window: int) -> list:
    """Центрированная скользящая средняя: окно нечётное, выход выровнен по центру."""
    if not data:
        raise ValueError("Ряд пуст: расчёт центрированной скользящей средней невозможен")
    check_window(window, len(data))
    if window % 2 == 0:
        raise ValueError(f"Центрированное MA требует нечётного window, получено: {window}")

    half = window // 2
    return [
        sum(data[i - half:i + half + 1]) / window
        for i in range(half, len(data) - half)
    ]


def exponential_moving_average(data: Sequence[float], alpha: float) -> list:
    """EMA: EMA[0] = data[0]; EMA[i] = alpha * data[i] + (1 - alpha) * EMA[i-1]."""
    if not data:
        raise ValueError("Ряд пуст: расчёт экспоненциальной скользящей средней невозможен")
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должен быть в диапазоне (0, 1], получено: {alpha}")

    result = [float(data[0])]
    for x in data[1:]:
        result.append(alpha * x + (1 - alpha) * result[-1])
    return result
