"""Сохранение и загрузка ряда в JSON (с метаданными)."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

PathLike = Union[str, Path]


def _validate_series(data: List[float]) -> None:
    """Проверяет, что ряд не пуст и состоит из чисел."""
    if not data:
        raise ValueError("Ряд пуст: сохранять нечего")
    for i, value in enumerate(data):
        # bool — подкласс int, поэтому проверяем его отдельно и отбрасываем
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"Элемент №{i} ({value!r}) не является числом"
            )


def save_series_json(
    data: List[float],
    file_path: PathLike,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    """Сохраняет ряд в JSON. При переданном meta добавляет блок метаданных."""
    _validate_series(data)

    payload: Dict[str, Any] = {"data": list(data)}
    if meta:
        meta_full = dict(meta)
        meta_full.setdefault("n", len(data))
        meta_full.setdefault("created", datetime.now().isoformat(timespec="seconds"))
        payload["meta"] = meta_full

    path = Path(file_path)
    # создаём вложенные папки автоматически (требование методички)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_series_json(
    file_path: PathLike,
    with_meta: bool = False,
) -> Union[List[float], Tuple[List[float], Dict[str, Any]]]:
    """Читает ряд из JSON. При with_meta=True возвращает кортеж (ряд, meta)."""
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"Файл {path} не найден")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Файл {path} не является корректным JSON: {exc}") from exc

    # голый список без метаданных
    if isinstance(payload, list):
        data = [float(x) for x in payload]
        return (data, {}) if with_meta else data

    if not isinstance(payload, dict) or "data" not in payload:
        raise ValueError("В JSON-файле нет поля data")

    raw_data = payload["data"]
    if not isinstance(raw_data, list):
        raise ValueError("Поле data должно быть списком чисел")
    if not raw_data:
        raise ValueError("Поле data пусто: ряд не содержит чисел")

    data = [float(x) for x in raw_data]
    meta = payload.get("meta", {})
    return (data, meta) if with_meta else data


# алиас для совместимости: если main.py или старые тесты звали функцию по-другому
load_series_from_json = load_series_json

save_series_to_json = save_series_json
