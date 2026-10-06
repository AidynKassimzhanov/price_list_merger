"""Модуль для очистки и приведения типов данных прайс-листов."""

import re
import pandas as pd


def clean_string(value: str) -> str:
    # Очищает текстовые поля (sku, name) от лишних пробелов.
    if pd.isna(value) or value is None:
        return ""
    return str(value).strip()


def clean_price(value: str | float | int) -> float:
    """Преобразует значение цены в число с плавающей точкой (float).

    Удаляет знаки валют, пробелы, меняет запятую на точку.
    """
    if pd.isna(value) or value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    val_str = str(value).strip()

    # 1. Заменяем обычные и неразрывные пробелы (\xa0)
    val_str = val_str.replace("\xa0", "").replace(" ", "")

    # 2. Оставляем только цифры, точки, запятые и знак минус
    val_str = re.sub(r"[^\d.,-]", "", val_str)

    if not val_str:
        return 0.0

    # 3. Нормализуем десятичный разделитель
    if "," in val_str and "." in val_str:
        val_str = val_str.replace(",", "")
    else:
        val_str = val_str.replace(",", ".")

    try:
        return float(val_str)
    except ValueError:
        return 0.0


def clean_quantity(value: str | float | int) -> float:
    # Преобразует значение количества в целое число (int).
    if pd.isna(value) or value is None:
        return 0

    if isinstance(value, (int, float)):
        return int(value)

    # Извлекаем первое попавшееся число из строки (например, "10 шт." -> 10)
    match = re.search(r"\d+", str(value))
    if match:
        return int(match.group())

    return 0


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Применяет очистку ко всем каноническим колонкам DataFrame.

    :param df: DataFrame с колонками ['sku', 'name', 'price', 'quantity', 'supplier'].
    :return: Новый очищенный DataFrame."""
    df_clean = df.copy()

    if "sku" in df_clean.columns:
        df_clean["sku"] = df_clean["sku"].apply(clean_string)

    if "name" in df_clean.columns:
        df_clean["name"] = df_clean["name"].apply(clean_string)

    if "price" in df_clean.columns:
        df_clean["price"] = df_clean["price"].apply(clean_price)

    if "quantity" in df_clean.columns:
        df_clean["quantity"] = df_clean["quantity"].apply(clean_quantity)

    return df_clean



    