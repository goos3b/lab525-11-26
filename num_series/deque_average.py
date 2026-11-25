from __future__ import annotations

from collections import deque
from typing import Deque, List, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")


def _check_window(window: int, n: int) -> None:
    if isinstance(window, bool) or not isinstance(window, int):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(f"window ({window}) больше длины ряда ({n})")


def _check_alpha(alpha: float) -> None:
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должен быть в диапазоне (0, 1], получено: {alpha}")


def simple_moving_average_deque(data: Sequence[float], window: int) -> List[float]:
    """SMA через deque с бегущей суммой, O(n)."""
    _ensure_not_empty(data)
    _check_window(window, len(data))

    buf: Deque[float] = deque(maxlen=window)
    running_sum = 0.0
    result: List[float] = []

    for x in data:
        if len(buf) == window:
            running_sum -= buf[0]  # <-- было: running_sum -= buf (весь deque!)
        buf.append(x)
        running_sum += x

        if len(buf) == window:
            result.append(running_sum / window)

    return result


def centered_moving_average_deque(data: Sequence[float], window: int) -> List[float]:
    """Центрированное MA через deque, окно нечётное."""
    _ensure_not_empty(data)
    _check_window(window, len(data))

    if window % 2 == 0:
        raise ValueError(f"Центрированное MA требует нечётного window, получено: {window}")

    buf: Deque[float] = deque(maxlen=window)
    running_sum = 0.0
    result: List[float] = []

    for x in data:
        if len(buf) == window:
            running_sum -= buf[0]  # <-- было: running_sum -= buf (весь deque!)
        buf.append(x)
        running_sum += x

        if len(buf) == window:
            result.append(running_sum / window)

    return result


def exponential_moving_average_deque(data: Sequence[float], alpha: float) -> List[float]:
    """EMA через deque-подобный проход: EMA[0] = data[0]."""
    _ensure_not_empty(data)
    _check_alpha(alpha)

    prev = float(data[0])  # <-- было: float(data) — TypeError на списке!
    result: List[float] = [prev]

    for x in data[1:]:
        prev = alpha * x + (1.0 - alpha) * prev
        result.append(prev)

    return result


__all__ = [
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
]
