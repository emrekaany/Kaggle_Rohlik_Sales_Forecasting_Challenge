"""Explicit chronological partitioning for forecasting experiments."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TimeSplit:
    """Non-overlapping train, validation, and test partitions."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def chronological_split(
    frame: pd.DataFrame,
    *,
    validation_start: str | pd.Timestamp,
    test_start: str | pd.Timestamp,
    date_column: str = "date",
) -> TimeSplit:
    """Split rows at fixed time boundaries without shuffling."""

    if date_column not in frame.columns:
        raise ValueError(f"missing required date column: {date_column}")

    validation_boundary = pd.Timestamp(validation_start)
    test_boundary = pd.Timestamp(test_start)
    if validation_boundary >= test_boundary:
        raise ValueError("validation_start must be earlier than test_start")

    result = frame.copy()
    result[date_column] = pd.to_datetime(result[date_column], errors="raise")
    result = result.sort_values(date_column, kind="mergesort").reset_index(drop=True)

    train = result.loc[result[date_column] < validation_boundary].copy()
    validation = result.loc[
        (result[date_column] >= validation_boundary)
        & (result[date_column] < test_boundary)
    ].copy()
    test = result.loc[result[date_column] >= test_boundary].copy()

    empty = [
        name
        for name, partition in (
            ("train", train),
            ("validation", validation),
            ("test", test),
        )
        if partition.empty
    ]
    if empty:
        raise ValueError(f"time boundaries produced empty partitions: {', '.join(empty)}")

    return TimeSplit(train=train, validation=validation, test=test)
