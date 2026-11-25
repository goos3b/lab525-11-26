"""Загрузка/сохранение ряда в TXT и CSV, автоопределение формата."""
from __future__ import annotations

from typing import List, Sequence


def load_series_txt(path: str) -> List[float]:
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл: {err}") from err
    out: List[float] = []
    for ln in lines:
        text = ln.strip()
        if not text or text.startswith("#"):
            continue
        try:
            out.append(float(text))
        except ValueError:
            raise ValueError(f"Не удалось разобрать строку: {text!r}") from None
    return out


def save_series_txt(path: str, data: Sequence[float], precision: int = 6) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            for x in data:
                f.write(f"{x:.{precision}f}\n")
    except OSError as err:
        raise ValueError(f"Не удалось записать файл: {err}") from err


def _split_row(row: str) -> List[str]:
    for sep in (";", ","):
        if sep in row:
            return [c.strip() for c in row.split(sep)]
    return [row.strip()]


def load_series_csv(path: str) -> List[float]:
    try:
        with open(path, encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f]
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл: {err}") from err
    lines = [ln for ln in lines if ln.strip()]
    if not lines:
        raise ValueError("CSV-файл пуст")
    # Первая строка без числа — заголовок, пропускаем
    try:
        float(_split_row(lines[0])[-1])
        start = 0
    except ValueError:
        start = 1
    out: List[float] = []
    for ln in lines[start:]:
        cells = _split_row(ln)
        token = cells[-1] if len(cells) > 1 else cells[0]
        try:
            out.append(float(token))
        except ValueError:
            raise ValueError(f"Не удалось разобрать CSV-строку: {ln!r}") from None
    return out


def load_series_auto(path: str) -> List[float]:
    """Определяет формат по содержимому: JSON, CSV или TXT."""
    try:
        with open(path, encoding="utf-8") as f:
            head = f.read(512).lstrip()
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл: {err}") from err

    # 1. JSON проверяем по структуре (скобки)
    if head.startswith("[") or head.startswith("{"):
        return load_series_json(path)

    # 2. Пытаемся прочитать как TXT. Если не вышло (ValueError) — пробуем CSV.
    # Это решает проблему файлов вида "1.0;2.0;3.0", которые TXT не съест.
    try:
        return load_series_txt(path)
    except ValueError:
        return load_series_csv(path)


# Локальный импорт в конце файла, чтобы избежать циклического импорта
from num_series.io_json import load_series_json  # noqa: E402
