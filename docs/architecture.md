# Leakage-safe forecasting architecture

## Invariant

For a row at item `i` and time `t`, every target-derived feature must be a function only of observations strictly earlier than `t` for the same item.

```text
feature(i, t) = f({sales(i, u) where u < t})
```

The reference implementation enforces this invariant through sorting, duplicate-date rejection, `shift(lag)`, and `shift(1)` before every rolling aggregation.

## Components

### `add_leakage_safe_features`

Input contract:

- one row per group/date pair;
- parseable date column;
- target column present;
- positive lag and rolling-window definitions.

Output contract:

- rows are stably sorted by group and date;
- `sales_lag_N` uses only the same group’s target at `t-N`;
- `sales_rolling_mean_N` first shifts the target by one row, then computes the group-local rolling mean;
- calendar features are derived from the row date and do not use the target.

### `chronological_split`

Given `validation_start < test_start`:

```text
train:      date < validation_start
validation: validation_start <= date < test_start
test:       date >= test_start
```

The function fails if a boundary is invalid or any partition is empty. This makes accidental random splitting or silent empty validation periods harder.

## Extending the pipeline

A model implementation should add these stages without weakening the invariant:

1. Attach calendar, price, inventory, and availability features using the time at which they would have been known.
2. Fit imputers, encoders, scalers, and target statistics on the training partition only.
3. Tune on rolling-origin or expanding-window validation folds.
4. Report WMAE per horizon, warehouse, and important product segment.
5. Persist the feature schema, data interval, code revision, random seed, and metric artifact.
6. Generate a submission only after row-count, ID uniqueness, null, and range checks pass.

## Multi-step forecast boundary

The competition horizon is longer than one day. Later target lags are not naturally available for every future row. A production design must explicitly choose and test one of these strategies:

- recursive prediction, feeding earlier predictions into later horizons;
- direct models per horizon;
- a multi-output sequence model;
- target-independent features for the full horizon.

The current reference layer does not silently fill future sales or use true future targets.

## What CI proves

CI runs offline unit tests against synthetic data and parses the legacy notebooks as JSON. It does not download competition files, train CatBoost, use a GPU, submit predictions, or verify a Kaggle score.
