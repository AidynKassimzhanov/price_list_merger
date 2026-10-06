# Модуль для валидации и фильтрации данных прайс-листов.

import pandas as pd


def validate_dataframe(
    df: pd.DataFrame, min_price: float = 0.0
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Разделяет DataFrame на валидные и невалидные строки.

    Критерии валидности:
    1. Название (`name`) не пустое.
    2. Цена больше `min_price`.
    """
    if df.empty:
        return df.copy(), df.copy()

    # Обязательное условие: non-empty name
    has_name = df["name"].astype(str).str.strip() != "" if "name" in df.columns else False

    # Цена должна быть строго больше min_price
    valid_price = df["price"] > min_price if "price" in df.columns else True

    valid_mask = has_name & valid_price

    valid_df = df[valid_mask].copy()
    invalid_df = df[~valid_mask].copy()

    return valid_df, invalid_df
    
    