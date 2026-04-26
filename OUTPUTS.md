# Outputs Guide

This document explains what each generated file under `outputs/` is used for in the thesis workflow.

## Figures

- `outputs/figures/price_trends.png`: historical price trend chart for the five fruits.
- `outputs/figures/risk_comparison.png`: composite risk comparison chart used in the risk-analysis chapter.
- `outputs/figures/seasonality_patterns.png`: monthly seasonality chart used in the seasonality-analysis chapter.

## Tables

- `outputs/tables/descriptive_stats.csv`: descriptive statistics by fruit.
- `outputs/tables/seasonality_analysis.csv`: seasonality-strength summary by fruit.
- `outputs/tables/seasonality_profile.csv`: monthly average price profile table.
- `outputs/tables/risk_metrics.csv`: detailed risk-metric table with weighted score components.
- `outputs/tables/risk_classification.csv`: explainable risk classification output.
- `outputs/tables/risk_analysis_table.csv`: compact risk-analysis table for thesis insertion.
- `outputs/tables/forecast_model_metrics.csv`: all candidate forecast models and their errors.
- `outputs/tables/forecast_model_selection.csv`: selected model, rationale, and core metrics.
- `outputs/tables/stationarity_tests.csv`: stationarity checks and tested ARIMA/SARIMA grids.
- `outputs/tables/model_evaluation_table.csv`: baseline-versus-selected-model comparison.
- `outputs/tables/forecast_prices.csv`: forecast values used by the optimization layer.
- `outputs/tables/forecast_results_table.csv`: compact forecast-results table for the thesis.
- `outputs/tables/procurement_plan.csv`: full optimized procurement plan by week and fruit.
- `outputs/tables/optimization_results_table.csv`: thesis-friendly optimization result table.
- `outputs/tables/optimization_cost_comparison.csv`: cost comparison between heuristic and optimized procurement.
- `outputs/tables/procurement_strategy_comparison.csv`: strategy comparison across different risk levels.
- `outputs/tables/procurement_constraint_summary.csv`: summary of procurement caps, safety stock, and smoothing behavior.

## Reports

- `outputs/reports/summary.md`: short end-to-end pipeline summary.
- `outputs/reports/thesis_main_dataset_summary.md`: dataset coverage summary.
- `outputs/reports/seasonality_analysis.md`: seasonality-analysis subsection draft.
- `outputs/reports/model_justification.md`: forecasting-method justification notes.
- `outputs/reports/thesis_results.md`: expanded thesis results chapter draft.
