# Модуль для валидации и фильтрации данных прайс-листов.

import pandas as pd


def validate_dataframe(
    df: pd.DataFrame, min_price: float = 0.0
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Разделяет строки на корректные и некорректные.

    В некорректной таблице добавляет колонку errors с причинами.
    """
    errors = []

    for _, row in df.iterrows():
        row_errors = []

        sku = row.get("sku")
        if pd.isna(sku) or not str(sku).strip():
            row_errors.append("Не указан артикул")

        name = row.get("name")
        if pd.isna(name) or not str(name).strip():
            row_errors.append("Не указано название")

        price = row.get("price")
        if pd.isna(price) or price <= min_price:
            row_errors.append("Цена отсутствует или не больше нуля")

        quantity = row.get("quantity")
        if pd.isna(quantity):
            row_errors.append("Не указано количество")
        elif quantity < 0:
            row_errors.append("Количество не может быть отрицательным")

        errors.append("; ".join(row_errors))

    result_df = df.copy()
    result_df["errors"] = errors

    invalid_mask = result_df["errors"] != ""

    valid_df = result_df.loc[~invalid_mask].drop(columns="errors").copy()
    invalid_df = result_df.loc[invalid_mask].copy()

    return valid_df, invalid_df
    