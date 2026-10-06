# Тесты для модуля merger.py.

import pandas as pd
from price_list_merger.merger import merge_price_lists


def test_merge_price_lists_min_price_strategy():
    supplier_a = pd.DataFrame({
        "sku": ["A1", "B2"],
        "name": ["Товар 1", "Товар 2"],
        "price": [1000.0, 2000.0],
        "quantity": [10, 5],
        "supplier": ["Supplier_A", "Supplier_A"],
    })

    supplier_b = pd.DataFrame({
        "sku": ["A1", "C3"],
        "name": ["Товар 1", "Товар 3"],
        "price": [850.0, 1500.0],  # У Поставщика B цена на A1 ниже!
        "quantity": [3, 12],
        "supplier": ["Supplier_B", "Supplier_B"],
    })

    result = merge_price_lists([supplier_a, supplier_b], strategy="min_price")

    # В итоговом прайсе должно быть 3 уникальных товара (A1, B2, C3)
    assert len(result) == 3

    # Для товара A1 должна выбраться минимальная цена (850.0 от Supplier_B)
    a1_row = result[result["sku"] == "A1"].iloc[0]
    assert a1_row["price"] == 850.0
    assert a1_row["supplier"] == "Supplier_B"


def test_merge_empty_list():
    result = merge_price_lists([])
    assert result.empty