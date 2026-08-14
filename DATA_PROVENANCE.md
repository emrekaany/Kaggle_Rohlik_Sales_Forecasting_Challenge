# Competition data provenance

The data described in this repository belongs to the [Rohlik Sales Forecasting Challenge](https://www.kaggle.com/competitions/rohlik-sales-forecasting-challenge-v2/overview). Competition files are not included in this Git repository.

## Runner responsibilities

1. Sign in to Kaggle and accept the current competition rules.
2. Download files through your own authorized account.
3. Keep raw and derived competition data under ignored local directories such as `data/`.
4. Do not publish rows, submissions, weights, or artifacts unless the competition terms permit it.
5. Record the download date, competition version, split boundaries, feature schema, and code revision with every experiment.

## Expected source files

The legacy competition description refers to `sales_train.csv`, `sales_test.csv`, `inventory.csv`, `calendar.csv`, `solution.csv`, and `test_weights.csv`. Treat this list as historical repository documentation and verify the current canonical file names and rules on Kaggle before execution.

## Synthetic verification data

All automated tests and the local demo construct tiny synthetic item histories in memory. They do not use or approximate competition rows and are safe to run offline.
