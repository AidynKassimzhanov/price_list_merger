# Модуль для объединения и дедупликации прайс-листов.

import pandas as pd


def merge_price_lists(
        dfs: list[pd.DataFrame], strategy: str = "min_price"
) -> pd.DataFrame:
    """
    Объединяет список очищенных DataFrame в один.

    :param dfs: Список DataFrame от разных поставщиков.
    :param strategy: Стратегия дедупликации ('min_price' или 'keep_all').
    :return: Объединенный и сгруппированный DataFrame.
    """
    if not dfs:
        return pd.DataFrame(
            columns=["sku", "name", "price", "quantity", "supplier"]
        )

    # Объединяем все таблицы
    merged_df = pd.concat(dfs, ignore_index=True)

    if merged_df.empty or strategy == "keep_all":
        return merged_df

    if strategy == "min_price":
        # Сортируем по цене, чтобы при наличии одинаковых sku/name первой шла минимальная цена
        merged_df = merged_df.sort_values(by="price", ascending=True)

        # Группируем по SKU (если заполнен), иначе по Name
        # При отсутствии SKU используем fallback на name
        merged_df["dedup_key"] = merged_df["sku"].where(
            merged_df["sku"] != "", merged_df["name"]
        )

        # Оставляем первую запись (с минимальной ценой) для каждого ключа
        result_df = merged_df.drop_duplicates(
            subset=["dedup_key"], keep="first"
        ).copy()
        result_df.drop(columns=["dedup_key"], inplace=True)

        return result_df.reset_index(drop=True)

    return merged_df
