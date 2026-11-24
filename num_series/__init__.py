from .generator import random_series, sine_series, trend_series
from .stats import mean, median, spread, summarize
from .moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)
from .deque_average import (
    simple_moving_average_deque,
    centered_moving_average_deque,
    exponential_moving_average_deque,
)
from .benchmark import benchmark_moving_average
from .io__json import save_series_to_json, load_series_from_json

__all__ = [
    "random_series", "sine_series", "trend_series",
    "mean", "median", "spread", "summarize",
    "simple_moving_average",
    "centered_moving_average",
    "exponential_moving_average",
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
    "benchmark_moving_average",
    "save_series_to_json",
    "load_series_from_json",
]

__version__ = "1.0.0"
