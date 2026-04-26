# Outputs Guide

This document explains what each generated file under `outputs/` is used for.

## Figures

- `outputs/figures/price_trends.png`: historical price trend chart for the five fruits.
- `outputs/figures/risk_comparison.png`: composite risk comparison chart.
- `outputs/figures/seasonality_patterns.png`: monthly seasonality chart.

## Tables

- `outputs/tables/descriptive_stats.csv`: descriptive statistics by fruit.
- `outputs/tables/seasonality_analysis.csv`: seasonality-strength summary by fruit.
- `outputs/tables/seasonality_profile.csv`: monthly average price profile table.
- `outputs/tables/risk_metrics.csv`: detailed risk-metric table with weighted score components.
- `outputs/tables/risk_classification.csv`: explainable risk classification output.
- `outputs/tables/risk_analysis_table.csv`: compact risk-analysis table.
- `outputs/tables/forecast_model_metrics.csv`: all candidate forecast models and their errors.
- `outputs/tables/forecast_model_selection.csv`: selected model, rationale, and core metrics.
- `outputs/tables/stationarity_tests.csv`: stationarity checks and tested ARIMA/SARIMA grids.
- `outputs/tables/model_evaluation_table.csv`: baseline-versus-selected-model comparison.
- `outputs/tables/forecast_prices.csv`: forecast values used by the optimization layer.
- `outputs/tables/forecast_results_table.csv`: compact forecast-results table.
- `outputs/tables/procurement_plan.csv`: full optimized procurement plan by week and fruit.
- `outputs/tables/optimization_results_table.csv`: compact optimization result table.
- `outputs/tables/optimization_cost_comparison.csv`: cost comparison between heuristic and optimized procurement.
- `outputs/tables/procurement_strategy_comparison.csv`: strategy comparison across different risk levels.
- `outputs/tables/procurement_constraint_summary.csv`: summary of procurement caps, safety stock, and smoothing behavior.

## Reports

- `outputs/reports/summary.md`: short end-to-end pipeline summary.
- `outputs/reports/dataset_summary.md`: dataset coverage summary.
- `outputs/reports/seasonality_analysis.md`: seasonality analysis notes.
- `outputs/reports/model_justification.md`: forecast-method justification notes.
- `outputs/reports/project_results.md`: expanded results chapter draft.
