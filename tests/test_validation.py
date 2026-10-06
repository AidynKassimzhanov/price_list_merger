import pandas as pd
from price_list_merger.validation import validate_dataframe


def test_validate_dataframe_filtering():
    df = pd.DataFrame({
        "sku": ["A1", "", "A3", "A4", "A5", "A6", "A7"],
        "name": ["Товар 1", "Товар 2", "", "Товар 4",
                 "Товар 5", "Товар 6", "Товар 7"],
        "price": [1000.0, 500.0, 300.0, 0.0, 100.0, 100.0, None],
        "quantity": [10, 5, 1, 0, None, -2, 3],
    })

    valid_df, invalid_df = validate_dataframe(df)
    reasons = invalid_df.set_index("sku")["errors"]

    assert valid_df["sku"].tolist() == ["A1"]
    assert len(invalid_df) == 6
    assert "артикул" in reasons[""].lower()
    assert "название" in reasons["A3"].lower()
    assert "цена" in reasons["A4"].lower()
    assert "количество" in reasons["A5"].lower()
    assert "отрицательным" in reasons["A6"].lower()
    assert "цена" in reasons["A7"].lower()


def test_empty_dataframe():
    df = pd.DataFrame(columns=["sku", "name", "price", "quantity"])
    valid_df, invalid_df = validate_dataframe(df)

    assert valid_df.empty
    assert invalid_df.empty