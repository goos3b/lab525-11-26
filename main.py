from __future__ import annotations

import argparse
import random
import statistics
import sys
from datetime import datetime
from typing import List, Optional

from num_series import (
    random_series, sine_series, trend_series,
    mean, median, summarize,
    simple_moving_average, centered_moving_average, exponential_moving_average,
    simple_moving_average_deque, benchmark_moving_average,
    save_series_to_json, load_series_from_json,
)

# -------------------------------------------------------------------
# Генерация ряда (включая вариант 1 — равномерное распределение [0, 100))
# -------------------------------------------------------------------

def build_series(kind: str, n: int, seed: int) -> List[float]:
    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10, frequency=2, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0, step=1.0, noise=0.5, seed=seed)
    if kind == "uniform":
        # Вариант 1: n=1000 чисел из равномерного распределения [0, 100)
        rng = random.Random(seed)
        return [rng.uniform(0.0, 100.0) for _ in range(n)]
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")

# -------------------------------------------------------------------
# Печать
# -------------------------------------------------------------------

def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    if not values:
        print(f"\n{title}: (пусто)")
        return
    print(f"\n{title} (n={len(values)}):")
    for i in range(0, len(values), 10):
        chunk = values[i:i + 10]
        print(" " + " ".join(fmt.format(v) for v in chunk))

def print_header(kind: str, n: int) -> None:
    print("=" * 60)
    print(f"Тип ряда: {kind}, n = {n}")
    print("-" * 60)

def print_stats(stats: dict) -> None:
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана                : {stats['median']:>10.4f}")
    print(f"Размах (max - min)     : {stats['spread']:>10.4f}")
    print(f"min / max              : {stats['min']:>10.4f} / {stats['max']:.4f}")

def print_footer() -> None:
    print("=" * 60)

# -------------------------------------------------------------------
# Разбор аргументов
# -------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов (лаба 5.1)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--kind", choices=["random", "sine", "trend", "uniform"],
                        default="sine", help="тип генерируемого ряда")
    parser.add_argument("--n", type=int, default=20, help="количество точек в ряде")
    parser.add_argument("--window", type=int, default=3, help="размер окна (k)")
    parser.add_argument("--alpha", type=float, default=0.3, help="коэффициент EMA")
    parser.add_argument("--seed", type=int, default=42, help="зерно ГПСЧ")
    parser.add_argument("--benchmark", action="store_true",
                        help="замер времени SMA: list vs deque")
    parser.add_argument("--export", metavar="FILE", help="экспорт ряда в CSV")
    parser.add_argument("--json", action="store_true", help="вывод результата в JSON")
    return parser

# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        data = build_series(args.kind, args.n, args.seed)
        window = args.window

        # 1. Бенчмарк: считаем и выходим (запуск: --kind sine --n 1000 --window 10 --benchmark)
        if args.benchmark:
            timings = benchmark_moving_average(data, window, repeats=1000)
            print("=" * 60)
            print(f"Замер SMA: n={len(data)}, window={window}, повторов=1000")
            print("-" * 60)
            print(f"  list  : {timings['list']:.8f} c")
            print(f"  deque : {timings['deque']:.8f} c")
            print(f"  отношение (list/deque): {timings['list'] / timings['deque']:.2f}")
            print("=" * 60)
            return 0

        # 2. Обычные расчёты
        stats = summarize(data)
        sma = simple_moving_average(data, window)
        sma_deque = simple_moving_average_deque(data, window)
        ema = exponential_moving_average(data, args.alpha)
        cma = centered_moving_average(data, window) if window % 2 == 1 else None

        # 3. Вывод в консоль
        print_header(args.kind, len(data))
        print_stats(stats)

        # Вариант 1: равномерное распределение -> доп. показатели дисперсия и СКО
        if args.kind == "uniform":
            print(f"Выборочная дисперсия   : {statistics.variance(data):>10.4f}")
            print(f"Выборочное СКО         : {statistics.stdev(data):>10.4f}")
            print("-" * 60)

        print_series("Исходный ряд", data)
        print_series(f"SMA (window={window})", sma)
        print_series(f"SMA deque (window={window})", sma_deque)
        print_series(f"EMA (alpha={args.alpha})", ema)
        if cma is not None:
            print_series(f"Центрированное MA (window={window})", cma)
        print_footer()

        # 4. Экспорт в CSV
        if args.export:
            import csv
            with open(args.export, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["i", "value"])
                for i, v in enumerate(data):
                    writer.writerow([i, v])
            print(f"Экспортировано в {args.export}")

    except ValueError as err:
        print(f"Ошибка: {err}.", file=sys.stderr)
        return 1
    except Exception as err:
        print(f"Критическая ошибка: {err}.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
