import time

import pytest

from num_series.deque_average import simple_moving_average_deque
from num_series.generator import random_series


def _naive_moving_average(data, window):
    """Наивный вариант O(n*window): сумма среза на каждом шаге. Эталон для сравнения."""
    return [sum(data[i:i + window]) / window for i in range(len(data) - window + 1)]


def test_deque_benchmark():
    """Сравнение наивного подхода и deque-версии через time.perf_counter."""
    n, window = 100_000, 50
    data = random_series(n, seed=42)

    start = time.perf_counter()
    res_naive = _naive_moving_average(data, window)
    t_naive = time.perf_counter() - start

    start = time.perf_counter()
    res_deque = simple_moving_average_deque(data, window)
    t_deque = time.perf_counter() - start

    # 1. Корректность: результаты совпадают
    assert res_deque == pytest.approx(res_naive, rel=1e-9)

    # 2. Производительность: deque-версия не медленнее наивной
    assert t_deque <= t_naive, (
        f"deque: {t_deque:.4f} с, наивный: {t_naive:.4f} с"
    )

    # Вывод для отчёта (виден при запуске pytest с -s)
    print(f"\nНаивный O(n*window): {t_naive:.4f} с")
    print(f"Deque O(n):          {t_deque:.4f} с")
    print(f"Ускорение:           {t_naive / max(t_deque, 1e-9):.1f}x")
