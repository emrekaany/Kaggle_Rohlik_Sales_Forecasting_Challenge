from __future__ import annotations

import unittest

import pandas as pd

from rohlik_forecasting import add_leakage_safe_features


class LeakageSafeFeatureTests(unittest.TestCase):
    def test_shifted_rolling_mean_excludes_current_target(self) -> None:
        frame = pd.DataFrame(
            {
                "unique_id": ["a"] * 4,
                "date": pd.date_range("2025-01-01", periods=4, freq="D"),
                "sales": [10.0, 20.0, 30.0, 40.0],
            }
        )
        result = add_leakage_safe_features(
            frame, lags=(1,), rolling_windows=(2,)
        )

        self.assertTrue(pd.isna(result.loc[0, "sales_rolling_mean_2"]))
        self.assertEqual(
            result.loc[1:, "sales_rolling_mean_2"].tolist(),
            [10.0, 15.0, 25.0],
        )

    def test_current_target_mutation_cannot_change_current_features(self) -> None:
        frame = pd.DataFrame(
            {
                "unique_id": ["a"] * 4,
                "date": pd.date_range("2025-01-01", periods=4, freq="D"),
                "sales": [10.0, 20.0, 30.0, 40.0],
            }
        )
        changed = frame.copy()
        changed.loc[3, "sales"] = 4_000.0

        baseline = add_leakage_safe_features(
            frame, lags=(1,), rolling_windows=(2,)
        )
        mutated = add_leakage_safe_features(
            changed, lags=(1,), rolling_windows=(2,)
        )

        columns = ["sales_lag_1", "sales_rolling_mean_2"]
        pd.testing.assert_series_equal(
            baseline.loc[3, columns],
            mutated.loc[3, columns],
            check_names=False,
        )

    def test_lags_do_not_cross_item_boundaries(self) -> None:
        frame = pd.DataFrame(
            {
                "unique_id": ["a", "b", "a", "b"],
                "date": ["2025-01-01", "2025-01-01", "2025-01-02", "2025-01-02"],
                "sales": [10.0, 100.0, 20.0, 200.0],
            }
        )
        result = add_leakage_safe_features(
            frame, lags=(1,), rolling_windows=(2,)
        )

        a_lag = result.loc[result["unique_id"] == "a", "sales_lag_1"].iloc[1]
        b_lag = result.loc[result["unique_id"] == "b", "sales_lag_1"].iloc[1]
        self.assertEqual(a_lag, 10.0)
        self.assertEqual(b_lag, 100.0)

    def test_duplicate_item_date_is_rejected(self) -> None:
        frame = pd.DataFrame(
            {
                "unique_id": ["a", "a"],
                "date": ["2025-01-01", "2025-01-01"],
                "sales": [10.0, 20.0],
            }
        )
        with self.assertRaisesRegex(ValueError, "duplicate group/date"):
            add_leakage_safe_features(frame)


if __name__ == "__main__":
    unittest.main()
