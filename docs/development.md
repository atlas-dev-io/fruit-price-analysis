# Development Guide

## Purpose

This document defines how to extend the project without breaking reproducibility or mixing analysis stages together.

## Working Rules

- Keep raw data immutable.
- Keep standardized data reproducible from scripts.
- Keep analysis, forecasting, optimization, and export logic separated.
- Avoid hardcoding one-off transformations in multiple places.
- Regenerate outputs from code instead of editing exported files manually.

## Environment

- Python `3.11+`
- Conda environment: `fruit`

Recommended commands:

```bash
conda run -n fruit pip install -r requirements.txt
make build-data
make run
make test
```

## Directory Rules

```text
data/raw/           raw source data
data/processed/     standardized and cleaned datasets
src/data/           loading and cleaning
src/features/       statistics, risk, seasonality
src/forecast/       forecasting
src/optimization/   procurement optimization
src/visualization/  export helpers
outputs/figures/    generated figures
outputs/tables/     generated tables
outputs/reports/    generated markdown reports
docs/               project documentation
tests/              minimal regression tests
```

## Key Files

- `data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv`: raw market data
- `data/processed/market_fruit_dataset_en.csv`: standardized dataset
- `scripts/build_market_dataset.py`: rebuilds the standardized dataset
- `main.py`: runs the full pipeline

## Output Discipline

- Figures belong in `outputs/figures/`
- Tables belong in `outputs/tables/`
- Narrative reports belong in `outputs/reports/`
- Output descriptions belong in [outputs.md](outputs.md)

## Validation

Minimum validation before committing:

1. Run `conda run -n fruit python main.py`
2. Run `conda run -n fruit python -m unittest discover -s tests`
3. Check that expected output files were regenerated

## Extension Priorities

If the project is extended later, focus on:

- stronger business assumptions for procurement constraints
- broader forecasting diagnostics
- optional dashboard or service layer
