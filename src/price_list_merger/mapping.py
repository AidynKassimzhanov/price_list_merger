"""Модуль для сопоставления и переименования колонок прайс-листов."""

import json
from pathlib import Path
import pandas as pd


def load_mapping_config(config_path: Path) -> dict:
    """Загружает конфигурацию сопоставления колонок из JSON-файла.

    :param config_path: Путь к файлу mapping.json.
    :return: Словарь с конфигурацией поставщиков.
    :raises FileNotFoundError: Если файл конфигурации не найден.
    :raises ValueError: Если JSON содержит невалидную структуру.
    """
    if not isinstance(config_path, Path):
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения JSON-конфигурации: {e}")

    if "suppliers" not in data or not isinstance(data["suppliers"], dict):
        raise ValueError("Файл конфигурации должен содержать корневой ключ 'suppliers'.")

    return data["suppliers"]


def apply_column_mapping(df: pd.DataFrame, supplier_name: str, mapping_config: dict) -> pd.DataFrame:
    """Приводит наименования столбцов DataFrame к каноническому виду на основе конфига.

    Канонические поля: 'sku', 'name', 'price', 'quantity'.

    :param df: Исходный DataFrame поставщика.
    :param supplier_name: Идентификатор поставщика (например, 'supplier_a').
    :param mapping_config: Словарь конфигурации поставщиков (из load_mapping_config).
    :return: Новый DataFrame с переименованными столбцами.
    :raises ValueError: Если конфигурация для поставщика не найдена.
    """

    if supplier_name not in mapping_config:
        raise ValueError(f"Конфигурация для поставщика '{supplier_name}' не найдена в mapping.json")

    supplier_mapping = mapping_config[supplier_name]

    rename_dict = {orig_col: canonical for canonical, orig_col in supplier_mapping.items()}

    df_mapped = df.copy()
    df_mapped = df_mapped.rename(columns=rename_dict)

    df_mapped["supplier"] = supplier_name

    return df_mapped