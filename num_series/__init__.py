from .generator import random_series, sine_series, trend_series, uniform_series
from .stats import mean, median, spread, summarize, variance, stdev
from .io_json import save_series_to_json, load_series_from_json, save_series_json, load_series_json
from .io_file import load_series_txt, load_series_csv, load_series_auto
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

__all__ = [
    "random_series", "sine_series", "trend_series", "uniform_series",
    "mean", "median", "spread", "summarize",
    "variance", "stdev",
    "simple_moving_average",
    "centered_moving_average",
    "exponential_moving_average",
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
    "benchmark_moving_average",
    "save_series_to_json",
    "load_series_from_json",
    "save_series_json",
    "load_series_json",
    "load_series_txt", "load_series_csv", "load_series_auto",
]

__version__ = "1.0.0"
