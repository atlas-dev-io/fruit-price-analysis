from src.config import (
    FORECAST_FILE,
    FORECAST_METRICS_FILE,
    FORECAST_SELECTION_FILE,
    FORECAST_RESULTS_TABLE_FILE,
    MODEL_EVALUATION_TABLE_FILE,
    OPTIMIZATION_COST_COMPARISON_FILE,
    OPTIMIZATION_RESULTS_TABLE_FILE,
    PLAN_FILE,
    PRICE_FIGURE,
    PROCESSED_PRICE_FILE,
    PROCUREMENT_CONSTRAINT_SUMMARY_FILE,
    PROCUREMENT_STRATEGY_COMPARISON_FILE,
    RISK_ANALYSIS_TABLE_FILE,
    RISK_FIGURE,
    RISK_CLASSIFICATION_FILE,
    RISK_FILE,
    SEASONALITY_FIGURE,
    SEASONALITY_FILE,
    SEASONALITY_PROFILE_FILE,
    SEASONALITY_REPORT_FILE,
    STATS_FILE,
    SUMMARY_FILE,
    THESIS_RESULTS_FILE,
    THESIS_MAIN_DATASET_FILE,
    ensure_directories,
)
from src.data.cleaning import clean_price_data
from src.data.loaders import load_price_data
from src.features.descriptive_stats import build_descriptive_stats
from src.features.seasonality import (
    build_seasonality_profile,
    build_seasonality_report,
    build_seasonality_table,
)
from src.features.volatility import build_risk_classification_table, build_risk_metrics
from src.forecast.formal import build_formal_forecast
from src.optimization.model import (
    build_heuristic_procurement_plan,
    build_procurement_constraint_summary,
    build_procurement_plan,
)
from src.visualization.charts import (
    save_price_chart,
    save_risk_comparison_chart,
    save_seasonality_chart,
)
from src.visualization.export import (
    build_cost_comparison_table,
    build_forecast_results_table,
    build_model_evaluation_table,
    build_optimization_results_table,
    build_risk_analysis_table,
    build_strategy_comparison_table,
    build_thesis_results_report,
    export_csv,
    export_summary,
)


def _build_summary(stats_df, risk_df, plan_df, selection_df) -> str:
    stable = risk_df.sort_values("composite_risk_score").iloc[0]["fruit_name"]
    volatile = risk_df.sort_values("composite_risk_score", ascending=False).iloc[0]["fruit_name"]
    avg_price = round(float(stats_df["avg_price"].mean()), 2)
    fruit_count = int(stats_df["fruit_name"].nunique())
    forecast_start = str(plan_df["date"].min().date())
    forecast_end = str(plan_df["date"].max().date())
    model_summary = ", ".join(
        f"{row.fruit_name}:{row.selected_model}[{row.selected_params}]"
        for row in selection_df.itertuples()
    )
    eval_window = ", ".join(
        f"{row.fruit_name}:{row.test_start_date} to {row.test_end_date}"
        for row in selection_df.itertuples()
    )

    return f"""# Pipeline Summary

- Average observed price across fruits: {avg_price} TWD/kg
- Fruit categories included: {fruit_count}
- Most stable fruit in the sample: {stable}
- Highest-volatility fruit in the sample: {volatile}
- Forecast window: {forecast_start} to {forecast_end}
- Weekly evaluation window by fruit: {eval_window}
- Selected forecast model by fruit: {model_summary}
- Data note: this run uses the thesis dataset in `data/processed/thesis_main_dataset_en.csv`
"""


def run_pipeline() -> None:
    ensure_directories()

    raw_df = load_price_data(THESIS_MAIN_DATASET_FILE)
    clean_df = clean_price_data(raw_df)
    stats_df = build_descriptive_stats(clean_df)
    seasonality_df = build_seasonality_table(clean_df)
    seasonality_profile_df = build_seasonality_profile(clean_df)
    risk_df = build_risk_metrics(clean_df)
    risk_classification_df = build_risk_classification_table(risk_df)
    forecast_df, metrics_df, selection_df = build_formal_forecast(clean_df, periods=4)
    plan_df = build_procurement_plan(forecast_df, risk_df)
    heuristic_plan_df = build_heuristic_procurement_plan(forecast_df, risk_df)
    risk_analysis_df = build_risk_analysis_table(risk_df)
    model_evaluation_df = build_model_evaluation_table(metrics_df, selection_df)
    forecast_results_df = build_forecast_results_table(forecast_df)
    optimization_results_df = build_optimization_results_table(plan_df)
    cost_comparison_df = build_cost_comparison_table(plan_df, heuristic_plan_df)
    strategy_comparison_df = build_strategy_comparison_table(plan_df)
    constraint_summary_df = build_procurement_constraint_summary(plan_df)

    export_csv(clean_df, PROCESSED_PRICE_FILE)
    export_csv(stats_df, STATS_FILE)
    export_csv(seasonality_df, SEASONALITY_FILE)
    export_csv(seasonality_profile_df, SEASONALITY_PROFILE_FILE)
    export_csv(risk_df, RISK_FILE)
    export_csv(risk_classification_df, RISK_CLASSIFICATION_FILE)
    export_csv(risk_analysis_df, RISK_ANALYSIS_TABLE_FILE)
    export_csv(forecast_df, FORECAST_FILE)
    export_csv(metrics_df, FORECAST_METRICS_FILE)
    export_csv(selection_df, FORECAST_SELECTION_FILE)
    export_csv(model_evaluation_df, MODEL_EVALUATION_TABLE_FILE)
    export_csv(forecast_results_df, FORECAST_RESULTS_TABLE_FILE)
    export_csv(plan_df, PLAN_FILE)
    export_csv(optimization_results_df, OPTIMIZATION_RESULTS_TABLE_FILE)
    export_csv(cost_comparison_df, OPTIMIZATION_COST_COMPARISON_FILE)
    export_csv(strategy_comparison_df, PROCUREMENT_STRATEGY_COMPARISON_FILE)
    export_csv(constraint_summary_df, PROCUREMENT_CONSTRAINT_SUMMARY_FILE)
    save_price_chart(clean_df, PRICE_FIGURE)
    save_risk_comparison_chart(risk_df, RISK_FIGURE)
    save_seasonality_chart(seasonality_profile_df, SEASONALITY_FIGURE)
    export_summary(_build_summary(stats_df, risk_df, plan_df, selection_df), SUMMARY_FILE)
    export_summary(build_seasonality_report(seasonality_df), SEASONALITY_REPORT_FILE)
    export_summary(
        build_thesis_results_report(
            risk_analysis_df,
            model_evaluation_df,
            cost_comparison_df,
            strategy_comparison_df,
        ),
        THESIS_RESULTS_FILE,
    )

    print("Pipeline finished.")
    print(f"Processed data: {PROCESSED_PRICE_FILE}")
    print(f"Descriptive stats: {STATS_FILE}")
    print(f"Seasonality analysis: {SEASONALITY_FILE}")
    print(f"Seasonality profile: {SEASONALITY_PROFILE_FILE}")
    print(f"Risk metrics: {RISK_FILE}")
    print(f"Risk classifications: {RISK_CLASSIFICATION_FILE}")
    print(f"Risk analysis table: {RISK_ANALYSIS_TABLE_FILE}")
    print(f"Forecasts: {FORECAST_FILE}")
    print(f"Forecast metrics: {FORECAST_METRICS_FILE}")
    print(f"Forecast selections: {FORECAST_SELECTION_FILE}")
    print(f"Model evaluation table: {MODEL_EVALUATION_TABLE_FILE}")
    print(f"Forecast results table: {FORECAST_RESULTS_TABLE_FILE}")
    print(f"Procurement plan: {PLAN_FILE}")
    print(f"Optimization results table: {OPTIMIZATION_RESULTS_TABLE_FILE}")
    print(f"Optimization cost comparison: {OPTIMIZATION_COST_COMPARISON_FILE}")
    print(f"Procurement strategy comparison: {PROCUREMENT_STRATEGY_COMPARISON_FILE}")
    print(f"Procurement constraint summary: {PROCUREMENT_CONSTRAINT_SUMMARY_FILE}")
    print(f"Chart: {PRICE_FIGURE}")
    print(f"Risk chart: {RISK_FIGURE}")
    print(f"Seasonality chart: {SEASONALITY_FIGURE}")
    print(f"Summary: {SUMMARY_FILE}")
    print(f"Seasonality report: {SEASONALITY_REPORT_FILE}")
    print(f"Thesis results report: {THESIS_RESULTS_FILE}")
