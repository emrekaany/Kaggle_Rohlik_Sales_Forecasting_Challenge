"""Past-only feature engineering for item-level sales histories."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def add_leakage_safe_features(
    frame: pd.DataFrame,
    *,
    group_columns: Sequence[str] = ("unique_id",),
    date_column: str = "date",
    target_column: str = "sales",
    lags: Sequence[int] = (1, 7, 14),
    rolling_windows: Sequence[int] = (7, 28),
) -> pd.DataFrame:
    """Return a sorted copy with calendar and strictly past target features.

    Rolling statistics are calculated from ``target.shift(1)`` inside each
    group. Therefore the feature for a row never includes that row's target.
    Duplicate group/date rows are rejected because their ordering is ambiguous.
    """

    groups = tuple(group_columns)
    if not groups:
        raise ValueError("group_columns must contain at least one column")
    if any(value <= 0 for value in (*lags, *rolling_windows)):
        raise ValueError("lags and rolling_windows must contain positive integers")

    required = {*groups, date_column, target_column}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")

    result = frame.copy()
    result[date_column] = pd.to_datetime(result[date_column], errors="raise")
    key_columns = [*groups, date_column]
    if result.duplicated(key_columns).any():
        raise ValueError("duplicate group/date rows make temporal ordering ambiguous")

    result = result.sort_values(key_columns, kind="mergesort").reset_index(drop=True)
    grouped_target = result.groupby(
        list(groups), sort=False, dropna=False
    )[target_column]

    for lag in lags:
        result[f"{target_column}_lag_{lag}"] = grouped_target.shift(lag)

    temporary_column = "__past_target_for_rolling"
    if temporary_column in result.columns:
        raise ValueError(f"reserved column already exists: {temporary_column}")
    result[temporary_column] = grouped_target.shift(1)

    for window in rolling_windows:
        result[f"{target_column}_rolling_mean_{window}"] = result.groupby(
            list(groups), sort=False, dropna=False
        )[temporary_column].transform(
            lambda values, size=window: values.rolling(
                window=size, min_periods=1
            ).mean()
        )

    result = result.drop(columns=temporary_column)
    dates = result[date_column].dt
    result["day_of_week"] = dates.dayofweek.astype("int8")
    result["day_of_month"] = dates.day.astype("int8")
    result["month"] = dates.month.astype("int8")
    result["iso_week"] = dates.isocalendar().week.astype("int16")
    return result
