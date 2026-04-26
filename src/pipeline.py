from src.config import (
    FORECAST_FILE,
    FORECAST_METRICS_FILE,
    FORECAST_SELECTION_FILE,
    PLAN_FILE,
    PRICE_FIGURE,
    PROCESSED_PRICE_FILE,
    RISK_CLASSIFICATION_FILE,
    RISK_FILE,
    STATS_FILE,
    SUMMARY_FILE,
    THESIS_MAIN_DATASET_FILE,
    ensure_directories,
)
from src.data.cleaning import clean_price_data
from src.data.loaders import load_price_data
from src.features.descriptive_stats import build_descriptive_stats
from src.features.volatility import build_risk_classification_table, build_risk_metrics
from src.forecast.formal import build_formal_forecast
from src.optimization.model import build_procurement_plan
from src.visualization.charts import save_price_chart
from src.visualization.export import export_csv, export_summary


def _build_summary(stats_df, risk_df, plan_df, selection_df) -> str:
    stable = risk_df.sort_values("composite_risk_score").iloc[0]["fruit_name"]
    volatile = risk_df.sort_values("composite_risk_score", ascending=False).iloc[0]["fruit_name"]
    avg_price = round(float(stats_df["avg_price"].mean()), 2)
    fruit_count = int(stats_df["fruit_name"].nunique())
    forecast_start = str(plan_df["date"].min().date())
    forecast_end = str(plan_df["date"].max().date())
    model_summary = ", ".join(
        f"{row.fruit_name}:{row.selected_model}"
        for row in selection_df.itertuples()
    )

    return f"""# Pipeline Summary

- Average observed price across fruits: {avg_price} TWD/kg
- Fruit categories included: {fruit_count}
- Most stable fruit in the sample: {stable}
- Highest-volatility fruit in the sample: {volatile}
- Forecast window: {forecast_start} to {forecast_end}
- Selected forecast model by fruit: {model_summary}
- Data note: this run uses the thesis dataset in `data/processed/thesis_main_dataset_en.csv`
"""


def run_pipeline() -> None:
    ensure_directories()

    raw_df = load_price_data(THESIS_MAIN_DATASET_FILE)
    clean_df = clean_price_data(raw_df)
    stats_df = build_descriptive_stats(clean_df)
    risk_df = build_risk_metrics(clean_df)
    risk_classification_df = build_risk_classification_table(risk_df)
    forecast_df, metrics_df, selection_df = build_formal_forecast(clean_df, periods=4)
    plan_df = build_procurement_plan(forecast_df, risk_df)

    export_csv(clean_df, PROCESSED_PRICE_FILE)
    export_csv(stats_df, STATS_FILE)
    export_csv(risk_df, RISK_FILE)
    export_csv(risk_classification_df, RISK_CLASSIFICATION_FILE)
    export_csv(forecast_df, FORECAST_FILE)
    export_csv(metrics_df, FORECAST_METRICS_FILE)
    export_csv(selection_df, FORECAST_SELECTION_FILE)
    export_csv(plan_df, PLAN_FILE)
    save_price_chart(clean_df, PRICE_FIGURE)
    export_summary(_build_summary(stats_df, risk_df, plan_df, selection_df), SUMMARY_FILE)

    print("Pipeline finished.")
    print(f"Processed data: {PROCESSED_PRICE_FILE}")
    print(f"Descriptive stats: {STATS_FILE}")
    print(f"Risk metrics: {RISK_FILE}")
    print(f"Risk classifications: {RISK_CLASSIFICATION_FILE}")
    print(f"Forecasts: {FORECAST_FILE}")
    print(f"Forecast metrics: {FORECAST_METRICS_FILE}")
    print(f"Forecast selections: {FORECAST_SELECTION_FILE}")
    print(f"Procurement plan: {PLAN_FILE}")
    print(f"Chart: {PRICE_FIGURE}")
    print(f"Summary: {SUMMARY_FILE}")
