from __future__ import annotations

from collections import deque
from typing import Deque, List, Sequence

# ---------------------------------------------------------------
# Вспомогательные функции валидации
# ---------------------------------------------------------------

def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")

def _check_window(window: int, n: int) -> None:
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(f"window ({window}) больше длины ряда ({n})")

def _check_alpha(alpha: float) -> None:
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должен быть в диапазоне (0, 1], получено: {alpha}")

# ---------------------------------------------------------------
# Простая скользящая средняя (SMA) через deque
# ---------------------------------------------------------------

def simple_moving_average_deque(
    data: Sequence[float],
    window: int,
) -> List[float]:
    _ensure_not_empty(data)
    _check_window(window, len(data))

    buf: Deque[float] = deque(maxlen=window)
    running_sum: float = 0.0
    result: List[float] =[]   # <-- ИСПРАВЛЕНО: теперь здесь пустой список

    for x in data:
        # Если буфер полон, вычитаем самый старый элемент (buf) ПЕРЕД добавлением нового
        if len(buf) == window:
            running_sum -= buf[0]  # <-- ИСПРАВЛЕНО: вычитаем buf, а не весь deque
        
        buf.append(x)
        running_sum += x

        # Добавляем результат только когда окно полностью набралось
        if len(buf) == window:
            result.append(running_sum / window)

    return result

# ---------------------------------------------------------------
# Центрированное MA через deque
# ---------------------------------------------------------------

def centered_moving_average_deque(
    data: Sequence[float],
    window: int,
) -> List[float]:
    _ensure_not_empty(data)
    _check_window(window, len(data))
    
    if window % 2 == 0:
        raise ValueError(f"Центрированное MA требует нечётного window, получено: {window}")

    buf: Deque[float] = deque(maxlen=window)
    running_sum: float = 0.0
    result: List[float] = []

    for x in data:
        if len(buf) == window:
            running_sum -= buf
        
        buf.append(x)
        running_sum += x

        if len(buf) == window:
            result.append(running_sum / window)

    return result

# ---------------------------------------------------------------
# Экспоненциальная скользящая средняя (EMA) через deque
# ---------------------------------------------------------------

def exponential_moving_average_deque(
    data: Sequence[float],
    alpha: float,
) -> List[float]:
    _ensure_not_empty(data)
    _check_alpha(alpha)

    prev: float = float(data)
    result: List[float] = [prev]

    for x in data[1:]:
        prev = alpha * x + (1.0 - alpha) * prev
        result.append(prev)

    return result

# ---------------------------------------------------------------
# Публичный интерфейс модуля
# ---------------------------------------------------------------

__all__ = [
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
]
