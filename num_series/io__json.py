import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

def save_series_to_json(data: List[float], filename: str, meta: Optional[Dict[str, Any]] = None) -> None:
    """
    Сохраняет числовой ряд в JSON-файл.
    
    Формат:
    {
      "meta": { ... },  # опционально
      "data": [ ... ]   # обязательно
    }
    """
    payload = {
        "data": data
    }
    
    # Если переданы метаданные, добавляем их
    if meta:
        payload["meta"] = meta
    
    # Создаем директорию, если её нет (например, папка output)
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def load_series_from_json(filename: str) -> List[float]:
    """
    Загружает числовой ряд из JSON-файла.
    Метаданные игнорируются (согласно требованию методички).
    Возвращает только список data.
    """
    path = Path(filename)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {filename}")
    
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    
    if "data" not in payload:
        raise ValueError("В JSON-файле отсутствует обязательный ключ 'data'")
    
    data = payload["data"]
    
    # Простая валидация, что это список чисел
    if not isinstance(data, list):
        raise ValueError("Поле 'data' должно быть списком")
        
    return data
