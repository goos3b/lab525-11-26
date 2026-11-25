import pytest

from num_series.io_file import (
    load_series_auto,
    load_series_csv,
    load_series_txt,
    save_series_txt,
)


# ---------- save + load TXT (круговорот данных) ----------

def test_txt_roundtrip(tmp_path):
    """Сохраняем ряд, читаем обратно — значения совпадают."""
    path = tmp_path / "series.txt"
    data = [1.5, -2.25, 3.0, 0.0]
    save_series_txt(str(path), data)
    assert load_series_txt(str(path)) == data


def test_txt_roundtrip_precision(tmp_path):
    """Со значением по умолчанию 6 знаков после запятой 1/3 читается как 0.333333."""
    path = tmp_path / "prec.txt"
    save_series_txt(str(path), [1 / 3])
    assert load_series_txt(str(path)) == [0.333333]


def test_txt_precision_arg(tmp_path):
    path = tmp_path / "prec2.txt"
    save_series_txt(str(path), [1 / 3], precision=3)
    assert load_series_txt(str(path)) == [0.333]


def test_txt_skip_comments_and_empty_lines(tmp_path):
    path = tmp_path / "comments.txt"
    path.write_text("# комментарий\n\n1.0\n# ещё\n2.5\n\n", encoding="utf-8")
    assert load_series_txt(str(path)) == [1.0, 2.5]


def test_txt_empty_file_returns_empty_list(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("", encoding="utf-8")
    assert load_series_txt(str(path)) == []


def test_txt_bad_line_raises(tmp_path):
    path = tmp_path / "bad.txt"
    path.write_text("1.0\nabc\n", encoding="utf-8")
    with pytest.raises(ValueError, match="разобрать строку"):
        load_series_txt(str(path))


def test_txt_missing_file_raises():
    with pytest.raises(ValueError, match="прочитать"):
        load_series_txt("нет_такого_файла_12345.txt")


# ---------- load TXT: разные записи чисел ----------

def test_txt_integers_and_scientific(tmp_path):
    path = tmp_path / "nums.txt"
    path.write_text("1\n-2\n1e-3\n+4.5\n", encoding="utf-8")
    assert load_series_txt(str(path)) == [1.0, -2.0, 0.001, 4.5]


# ---------- load CSV ----------

def test_csv_simple(tmp_path):
    path = tmp_path / "s.csv"
    path.write_text("1.0;2.0;3.0\n4.0;5.0;6.0\n", encoding="utf-8")
    assert load_series_csv(str(path)) == [3.0, 6.0]  # берём последнюю колонку


def test_csv_with_header(tmp_path):
    path = tmp_path / "h.csv"
    path.write_text("time;value\n0;1.5\n1;2.5\n", encoding="utf-8")
    assert load_series_csv(str(path)) == [1.5, 2.5]


def test_csv_comma_separator(tmp_path):
    path = tmp_path / "c.csv"
    path.write_text("1,2,3\n", encoding="utf-8")
    assert load_series_csv(str(path)) == [3.0]


def test_csv_single_column(tmp_path):
    path = tmp_path / "one.csv"
    path.write_text("1.5\n2.5\n3.5\n", encoding="utf-8")
    assert load_series_csv(str(path)) == [1.5, 2.5, 3.5]


def test_csv_empty_raises(tmp_path):
    path = tmp_path / "e.csv"
    path.write_text("\n\n", encoding="utf-8")
    with pytest.raises(ValueError, match="пуст"):
        load_series_csv(str(path))


def test_csv_bad_row_raises(tmp_path):
    """Ошибка должна возникать, если битая строка идет ПОСЛЕ валидной (не заголовок)."""
    path = tmp_path / "b.csv"
    # Первая строка валидна -> она не считается заголовком. Вторая - мусор -> ошибка.
    path.write_text("1.0;2.0\n3.0;abc\n", encoding="utf-8")
    with pytest.raises(ValueError, match="CSV-строку"):
        load_series_csv(str(path))


def test_csv_missing_file_raises():
    with pytest.raises(ValueError):
        load_series_csv("нет_такого_файла_12345.csv")


# ---------- load_series_auto ----------

def test_auto_detects_csv_without_header(tmp_path):
    """Авто-детект должен распознать CSV без заголовка и вернуть последнюю колонку."""
    path = tmp_path / "plain.csv"
    path.write_text("1.0;2.0;3.0\n4.0;5.0;6.0\n", encoding="utf-8")
    # Ожидаем [3.0, 6.0] - последняя колонка, как в твоей логике load_series_csv
    assert load_series_auto(str(path)) == [3.0, 6.0]


def test_auto_detects_csv_with_header(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("time;value\n1;2.0\n", encoding="utf-8")
    assert load_series_auto(str(path)) == [2.0]


def test_auto_detects_csv_without_header(tmp_path):
    path = tmp_path / "plain.csv"
    path.write_text("1.0;2.0;3.0\n", encoding="utf-8")
    assert load_series_auto(str(path)) == [3.0]


def test_auto_detects_txt(tmp_path):
    path = tmp_path / "data.txt"
    path.write_text("1.5\n2.5\n3.5\n", encoding="utf-8")
    assert load_series_auto(str(path)) == [1.5, 2.5, 3.5]


def test_auto_missing_file_raises():
    with pytest.raises(ValueError):
        load_series_auto("нет_такого_файла_12345.txt")
