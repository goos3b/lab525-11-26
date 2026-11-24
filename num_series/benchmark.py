import time
from typing import Sequence, Dict
from .deque_average import simple_moving_average_deque
from .moving_average import simple_moving_average

def benchmark_moving_average(
    data: Sequence[float],
    window: int,
    repeats: int = 1000,
) -> Dict[str, float]:
    """
    Замеряет среднее время выполнения простой скользящей средней (SMA)
    двумя способами: через list и через deque.

    Args:
        data: входной числовой ряд
        window: размер окна скользящего среднего
        repeats: количество повторов для усреднения времени

    Returns:
        Словарь с временем выполнения для каждого метода:
        {"list": время_в_секундах, "deque": время_в_секундах}
    """
    # Замер времени для реализации на list
    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average(data, window)
    t_list = (time.perf_counter() - t0) / repeats

    # Замер времени для реализации на deque
    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average_deque(data, window)
    t_deque = (time.perf_counter() - t0) / repeats

    return {"list": t_list, "deque": t_deque}
