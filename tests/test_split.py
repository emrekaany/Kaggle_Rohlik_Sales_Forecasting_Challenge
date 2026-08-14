from __future__ import annotations

import unittest

import pandas as pd

from rohlik_forecasting import chronological_split


class ChronologicalSplitTests(unittest.TestCase):
    def test_partitions_are_nonempty_and_strictly_ordered(self) -> None:
        frame = pd.DataFrame(
            {
                "date": pd.date_range("2025-01-01", periods=6, freq="D"),
                "sales": [1, 2, 3, 4, 5, 6],
            }
        )
        result = chronological_split(
            frame,
            validation_start="2025-01-04",
            test_start="2025-01-06",
        )

        self.assertEqual((len(result.train), len(result.validation), len(result.test)), (3, 2, 1))
        self.assertLess(result.train["date"].max(), result.validation["date"].min())
        self.assertLess(result.validation["date"].max(), result.test["date"].min())

    def test_invalid_boundary_order_is_rejected(self) -> None:
        frame = pd.DataFrame({"date": ["2025-01-01"], "sales": [1]})
        with self.assertRaisesRegex(ValueError, "validation_start"):
            chronological_split(
                frame,
                validation_start="2025-01-06",
                test_start="2025-01-06",
            )


if __name__ == "__main__":
    unittest.main()
