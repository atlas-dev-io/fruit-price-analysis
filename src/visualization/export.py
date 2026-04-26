from pathlib import Path

import pandas as pd


def export_csv(df: pd.DataFrame, output_path: Path) -> None:
    df.to_csv(output_path, index=False)


def export_summary(summary_text: str, output_path: Path) -> None:
    output_path.write_text(summary_text, encoding="utf-8")


def build_risk_analysis_table(risk_df: pd.DataFrame) -> pd.DataFrame:
    return risk_df[
        [
            "fruit_name",
            "coefficient_of_variation",
            "max_drawdown",
            "return_volatility",
            "composite_risk_score",
            "risk_percentile",
            "risk_level",
            "risk_reason",
        ]
    ].copy()


def build_model_evaluation_table(
    metrics_df: pd.DataFrame, selection_df: pd.DataFrame
) -> pd.DataFrame:
    baseline_df = metrics_df[metrics_df["model_name"] == "exponential_smoothing"][
        ["fruit_name", "rmse", "mae", "mape"]
    ].rename(
        columns={
            "rmse": "baseline_rmse",
            "mae": "baseline_mae",
            "mape": "baseline_mape",
        }
    )
    merged = selection_df.merge(baseline_df, on="fruit_name", how="left")
    merged["rmse_improvement_vs_baseline"] = (
        merged["baseline_rmse"] - merged["rmse"]
    ).round(4)
    merged["mae_improvement_vs_baseline"] = (
        merged["baseline_mae"] - merged["mae"]
    ).round(4)
    merged["mape_improvement_vs_baseline"] = (
        merged["baseline_mape"] - merged["mape"]
    ).round(4)
    return merged


def build_forecast_results_table(forecast_df: pd.DataFrame) -> pd.DataFrame:
    return forecast_df[
        [
            "date",
            "fruit_name",
            "forecast_price",
            "selected_model",
            "selected_family",
            "selected_params",
            "data_frequency",
        ]
    ].copy()


def build_optimization_results_table(plan_df: pd.DataFrame) -> pd.DataFrame:
    return plan_df[
        [
            "date",
            "fruit_name",
            "risk_level",
            "forecast_price",
            "period_demand_kg",
            "purchase_cap_kg",
            "safety_stock_target_kg",
            "recommended_quantity_kg",
            "ending_inventory_kg",
            "procurement_change_kg",
            "purchase_cost",
            "risk_penalty_cost",
            "holding_cost",
            "stability_penalty_cost",
            "strategy",
        ]
    ].copy()


def build_cost_comparison_table(
    optimized_plan_df: pd.DataFrame, heuristic_plan_df: pd.DataFrame
) -> pd.DataFrame:
    def _summarize(df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.assign(total_cost=df["purchase_cost"] + df["risk_penalty_cost"] + df["holding_cost"])
            .groupby("fruit_name", as_index=False)
            .agg(
                total_purchase_cost=("purchase_cost", "sum"),
                total_risk_penalty=("risk_penalty_cost", "sum"),
                total_holding_cost=("holding_cost", "sum"),
                total_cost=("total_cost", "sum"),
            )
        )

    optimized = _summarize(optimized_plan_df).add_suffix("_optimized")
    heuristic = _summarize(heuristic_plan_df).add_suffix("_heuristic")
    optimized = optimized.rename(columns={"fruit_name_optimized": "fruit_name"})
    heuristic = heuristic.rename(columns={"fruit_name_heuristic": "fruit_name"})
    comparison = optimized.merge(heuristic, on="fruit_name")
    comparison["cost_saving"] = (
        comparison["total_cost_heuristic"] - comparison["total_cost_optimized"]
    ).round(2)
    comparison["cost_saving_rate"] = (
        comparison["cost_saving"] / comparison["total_cost_heuristic"]
    ).round(4)
    return comparison


def build_strategy_comparison_table(plan_df: pd.DataFrame) -> pd.DataFrame:
    return (
        plan_df.groupby(["fruit_name", "risk_level"], as_index=False)
        .agg(
            avg_forecast_price=("forecast_price", "mean"),
            total_purchase_kg=("recommended_quantity_kg", "sum"),
            max_inventory_kg=("ending_inventory_kg", "max"),
            avg_purchase_cost=("purchase_cost", "mean"),
            representative_strategy=("strategy", "first"),
        )
        .sort_values(["risk_level", "fruit_name"])
        .reset_index(drop=True)
    )


def build_thesis_results_report(
    risk_table_df: pd.DataFrame,
    model_eval_df: pd.DataFrame,
    cost_comparison_df: pd.DataFrame,
    strategy_df: pd.DataFrame,
    seasonality_df: pd.DataFrame,
    constraint_summary_df: pd.DataFrame,
) -> str:
    highest_risk = risk_table_df.sort_values("composite_risk_score", ascending=False).iloc[0]
    lowest_risk = risk_table_df.sort_values("composite_risk_score").iloc[0]
    best_model = model_eval_df.sort_values("rmse").iloc[0]
    best_saving = cost_comparison_df.sort_values("cost_saving", ascending=False).iloc[0]
    strongest_seasonality = seasonality_df.sort_values("seasonality_strength", ascending=False).iloc[0]
    weakest_seasonality = seasonality_df.sort_values("seasonality_strength").iloc[0]
    strongest_stability = constraint_summary_df.sort_values("avg_safety_stock_target_kg", ascending=False).iloc[0]
    strategy_lines = "\n".join(
        f"- {row.fruit_name} ({row.risk_level}): {row.representative_strategy}"
        for row in strategy_df.itertuples()
    )

    return f"""# Thesis Results Summary

## Abstract-Ready Paragraph

Using Taiwan Taipei Second Market data for five fruit categories, the analysis shows that {highest_risk['fruit_name']} has the highest comprehensive risk score ({highest_risk['composite_risk_score']:.4f}) and is therefore classified as a high-risk fruit, while {lowest_risk['fruit_name']} has the lowest comprehensive risk score ({lowest_risk['composite_risk_score']:.4f}) and is classified as low risk. Under a fixed weekly evaluation window, the forecasting module selected {best_model['selected_model']} for {best_model['fruit_name']}, achieving the lowest observed RMSE among the selected models ({best_model['rmse']:.4f}). After replacing the heuristic procurement rule with a linear-program optimization model, the largest cost reduction appeared in {best_saving['fruit_name']}, with a saving of {best_saving['cost_saving']:.2f} and a saving rate of {best_saving['cost_saving_rate']:.2%}. The optimized procurement results indicate that high-risk fruits should follow short-cycle rolling purchases, while low-risk fruits can shift part of procurement to lower-price periods and use inventory smoothing to reduce total cost.

## 4.1 Risk Analysis

- Highest risk fruit: {highest_risk['fruit_name']} ({highest_risk['risk_level']})
- Lowest risk fruit: {lowest_risk['fruit_name']} ({lowest_risk['risk_level']})
- Highest risk explanation: {highest_risk['risk_reason']}
- Interpretation: the cross-fruit risk ranking confirms that pears and grapes require more conservative procurement decisions, while apples and oranges provide more room for inventory-based smoothing.

## 4.2 Seasonality Analysis

- Strongest seasonality: {strongest_seasonality['fruit_name']} with strength {strongest_seasonality['seasonality_strength']:.4f}
- Weakest seasonality: {weakest_seasonality['fruit_name']} with strength {weakest_seasonality['seasonality_strength']:.4f}
- Interpretation: fruits with stronger monthly seasonality are better candidates for seasonal model comparison, while weaker series can remain in simpler weekly model families.

## 4.3 Forecast Model Results

- Best selected model by RMSE: {best_model['fruit_name']} -> {best_model['selected_model']} [{best_model['selected_params']}]
- Evaluation frequency: weekly
- Interpretation: the final model set is not forced into one family; the code preserves interpretability by selecting among ETS, ARIMA and SARIMA according to out-of-sample error.

## 4.4 Procurement Optimization Results

- Largest cost saving versus heuristic baseline: {best_saving['fruit_name']} ({best_saving['cost_saving']:.2f}, {best_saving['cost_saving_rate']:.2%})
- Strongest explicit safety-stock setting: {strongest_stability['fruit_name']} with average safety stock target {strongest_stability['avg_safety_stock_target_kg']:.2f} kg
- Interpretation: the optimization model now combines cost, risk, holding, and supply-stability considerations instead of only mapping risk levels to fixed procurement multipliers.

## 4.5 Strategy Comparison

{strategy_lines}

## 4.6 Writing Notes

- `outputs/tables/risk_analysis_table.csv` can support the risk-analysis subsection.
- `outputs/tables/model_evaluation_table.csv` and `outputs/tables/stationarity_tests.csv` can support the forecasting-method subsection.
- `outputs/tables/optimization_cost_comparison.csv` and `outputs/tables/procurement_constraint_summary.csv` can support the procurement-optimization subsection.
- `outputs/figures/risk_comparison.png` and `outputs/figures/seasonality_patterns.png` can be inserted directly into the results chapter.
"""


def build_outputs_guide() -> str:
    return """# Outputs Guide

## Figures

- `outputs/figures/price_trends.png`: historical price trend figure for all fruits.
- `outputs/figures/risk_comparison.png`: composite risk comparison chart for cross-fruit risk discussion.
- `outputs/figures/seasonality_patterns.png`: month-level seasonality profile chart for seasonal analysis.

## Tables

- `outputs/tables/descriptive_stats.csv`: descriptive statistics for each fruit.
- `outputs/tables/seasonality_analysis.csv`: per-fruit seasonality strength, peak month, and trough month.
- `outputs/tables/seasonality_profile.csv`: month-by-month average price profile.
- `outputs/tables/risk_metrics.csv`: full risk metric output with z-scores and weighted components.
- `outputs/tables/risk_classification.csv`: explainable risk grading table.
- `outputs/tables/risk_analysis_table.csv`: compact risk-analysis table for the thesis.
- `outputs/tables/forecast_model_metrics.csv`: all candidate forecast model errors.
- `outputs/tables/forecast_model_selection.csv`: final selected model and rationale by fruit.
- `outputs/tables/stationarity_tests.csv`: ADF-based stationarity checks and tested model grids.
- `outputs/tables/model_evaluation_table.csv`: thesis-friendly summary of selected models versus baseline.
- `outputs/tables/forecast_prices.csv`: raw forecast output used by the procurement layer.
- `outputs/tables/forecast_results_table.csv`: compact forecast-results table for the thesis.
- `outputs/tables/procurement_plan.csv`: full linear-program procurement output by period.
- `outputs/tables/optimization_results_table.csv`: compact optimization-results table for the thesis.
- `outputs/tables/optimization_cost_comparison.csv`: optimized-versus-heuristic cost comparison.
- `outputs/tables/procurement_strategy_comparison.csv`: cross-fruit strategy comparison by risk level.
- `outputs/tables/procurement_constraint_summary.csv`: procurement-cap, safety-stock, and smoothing summary.

## Reports

- `outputs/reports/summary.md`: short pipeline summary.
- `outputs/reports/thesis_main_dataset_summary.md`: dataset coverage summary.
- `outputs/reports/seasonality_analysis.md`: chapter-ready seasonality notes.
- `outputs/reports/model_justification.md`: forecasting justification notes.
- `outputs/reports/thesis_results.md`: expanded thesis results chapter draft.
"""


def build_model_justification_report(stationarity_df: pd.DataFrame, selection_df: pd.DataFrame) -> str:
    lines = [
        "# Forecast Model Justification",
        "",
        "## Modeling Scope",
        "",
        (
            "The ARIMA search space is limited to low-order weekly models: (0,1,1), (1,1,0), "
            "(1,1,1), (2,1,0), and (2,1,1). This keeps the thesis model set interpretable while "
            "still allowing short-memory autoregressive and moving-average structures. SARIMA is not "
            "searched exhaustively; it is only evaluated for series with stronger measured seasonality, "
            "using two targeted weekly seasonal candidates."
        ),
        "",
        "## Stationarity And Selection Notes",
        "",
    ]

    merged = selection_df.merge(
        stationarity_df[
            [
                "fruit_name",
                "level_adf_pvalue",
                "diff1_adf_pvalue",
                "seasonality_candidate",
            ]
        ],
        on="fruit_name",
        how="left",
        suffixes=("", "_stationarity"),
    )

    for row in merged.itertuples():
        seasonality_flag = getattr(row, "seasonality_candidate_stationarity", row.seasonality_candidate)
        seasonality_text = "yes" if seasonality_flag else "no"
        lines.append(
            f"- {row.fruit_name}: selected {row.selected_model} [{row.selected_params}], "
            f"ADF(level)={row.level_adf_pvalue}, ADF(diff1)={row.diff1_adf_pvalue}, "
            f"seasonality_candidate={seasonality_text}."
        )

    return "\n".join(lines) + "\n"
