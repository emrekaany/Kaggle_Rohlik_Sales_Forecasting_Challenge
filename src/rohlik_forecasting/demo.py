"""Offline synthetic demonstration of the reference feature contracts."""

from __future__ import annotations

import pandas as pd

from .features import add_leakage_safe_features
from .split import chronological_split


def main() -> None:
    dates = pd.date_range("2025-01-01", periods=6, freq="D")
    raw = pd.DataFrame(
        {
            "unique_id": ["item-a"] * 6 + ["item-b"] * 6,
            "date": list(dates) * 2,
            "sales": [10, 12, 11, 15, 14, 16, 40, 42, 41, 45, 44, 46],
        }
    )
    features = add_leakage_safe_features(
        raw, lags=(1, 2), rolling_windows=(2, 3)
    )
    splits = chronological_split(
        features,
        validation_start="2025-01-05",
        test_start="2025-01-06",
    )

    columns = [
        "unique_id",
        "date",
        "sales",
        "sales_lag_1",
        "sales_rolling_mean_2",
    ]
    print(features[columns].to_string(index=False))
    print(
        "split_rows:"
        f" train={len(splits.train)}"
        f" validation={len(splits.validation)}"
        f" test={len(splits.test)}"
    )


if __name__ == "__main__":
    main()
