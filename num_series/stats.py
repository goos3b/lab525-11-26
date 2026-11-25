import math
from typing import Sequence


def _ensure_not_empty(data) -> None:
    if not isinstance(data, (list, tuple)):
        raise ValueError(f"Входные данные не являются списком: {type(data).__name__}")
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")
    for x in data:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise ValueError(f"Нечисловое значение в ряде: {x!r}")


def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0


def spread(data):
    """Размах: max - min."""
    _ensure_not_empty(data)
    return max(data) - min(data)


def variance(data: Sequence[float]) -> float:
    """Выборочная дисперсия (несмещённая, делим на n - 1)."""
    n = len(data)
    if n < 2:
        raise ValueError("Для дисперсии нужно минимум 2 значения")
    m = mean(data)
    return sum((x - m) ** 2 for x in data) / (n - 1)


def stdev(data: Sequence[float]) -> float:
    """Выборочное СКО — корень из выборочной дисперсии."""
    return math.sqrt(variance(data))


def summarize(data):
    _ensure_not_empty(data)
    result = {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": min(data),
        "max": max(data),
    }
    if len(data) >= 2:  # доп. показатели варианта 1
        result["variance"] = variance(data)
        result["stdev"] = stdev(data)
    return result
