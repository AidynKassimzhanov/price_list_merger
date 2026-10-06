import pandas as pd
from price_list_merger.validation import validate_dataframe


def test_validate_dataframe_filtering():
    df = pd.DataFrame({
        "sku": ["A1", "", "A3", "A4"],
        "name": ["Товар 1", "Товар 2", "", "Товар 4"],
        "price": [1000.0, 500.0, 300.0, 0.0],
        "quantity": [10, 5, 1, 0],
    })

    valid_df, invalid_df = validate_dataframe(df)

    assert len(valid_df) == 2
    assert len(invalid_df) == 2
    assert "A1" in valid_df["sku"].values
    assert 0.0 not in valid_df["price"].values


def test_empty_dataframe():
    df = pd.DataFrame(columns=["sku", "name", "price", "quantity"])
    valid_df, invalid_df = validate_dataframe(df)

    assert valid_df.empty
    assert invalid_df.empty