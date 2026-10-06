import unittest
import pandas as pd

from price_list_merger.cleaning import (
    clean_string,
    clean_price,
    clean_dataframe,
    clean_quantity
)


class TestCleaning(unittest.TestCase):
    def test_clean_string(self):
        self.assertEqual(clean_string("  KB-001  "), "KB-001")
        self.assertEqual(clean_string(None), "")

    def test_clean_price(self):
        self.assertEqual(clean_price("12 500 T"), 12500.0)
        self.assertEqual(clean_price("15500,0"), 15500.0)
        self.assertEqual(clean_price("1,500.00"), 1500.0)
        self.assertEqual(clean_price(None), 0.0)

    def test_clean_quantity(self):
        self.assertEqual(clean_quantity("10 шт."), 10)
        self.assertEqual(clean_quantity("5.0"), 5)
        self.assertEqual(clean_quantity("-2"), -2)
        self.assertIsNone(clean_quantity(None))
        self.assertIsNone(clean_quantity("abc"))

    def test_clean_dataframe(self):
        df = pd.DataFrame({
            "sku": ["  A1  "],
            "name": ["  Товар 1  "],
            "price": ["1 000 т"],
            "quantity": ["15  шт."]
        })
        clean_df = clean_dataframe(df)
        self.assertEqual(clean_df["sku"].iloc[0], "A1")
        self.assertEqual(clean_df["price"].iloc[0], 1000.0)
        self.assertEqual(clean_df["quantity"].iloc[0], 15)

if __name__ == "__main__":
    unittest.main()