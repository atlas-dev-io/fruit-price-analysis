# Architecture

## Overview

This project uses a lightweight offline analytics architecture:

```text
source market data
    ->
dataset standardization
    ->
cleaning and aggregation
    ->
risk and seasonality analysis
    ->
forecast model selection
    ->
procurement optimization
    ->
tables, figures, and reports
```

The design goal is reproducibility. Raw data stays in `data/raw/`, standardized data stays in `data/processed/`, and every downstream artifact is generated from code.

## Layers

### Data

- `src/data/loaders.py`
- `src/data/cleaning.py`
- `scripts/download_taiwan_main_data_taipei2.py`
- `scripts/build_market_dataset.py`

Responsibilities:

- read raw market data
- standardize schema and units
- aggregate daily observations into stable analysis inputs

### Analysis

- `src/features/descriptive_stats.py`
- `src/features/volatility.py`
- `src/features/seasonality.py`

Responsibilities:

- descriptive statistics
- explainable risk scoring
- monthly seasonality analysis

### Forecasting

- `src/forecast/formal.py`
- `src/forecast/baseline.py`

Responsibilities:

- weekly train/test split
- candidate comparison across ETS, ARIMA, and targeted SARIMA
- stationarity checks and model rationale

### Optimization

- `src/optimization/model.py`

Responsibilities:

- convert forecast and risk outputs into procurement decisions
- optimize purchase quantity and inventory under demand, cap, safety-stock, and smoothing constraints

### Output

- `src/visualization/charts.py`
- `src/visualization/export.py`

Responsibilities:

- export figures
- export thesis-neutral project tables
- generate narrative markdown reports

## Data Flow

```text
data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv
    ->
data/processed/market_fruit_dataset_en.csv
    ->
data/processed/fruit_prices_cleaned.csv
    ->
outputs/tables/*.csv
    ->
outputs/figures/*.png and outputs/reports/*.md
```

## Current State

The current codebase already supports:

- market dataset standardization
- cleaning and aggregation
- risk scoring and seasonality outputs
- weekly model selection
- linear-program procurement optimization
- report, table, and figure generation

The main remaining work is analytical refinement, not missing architecture.
