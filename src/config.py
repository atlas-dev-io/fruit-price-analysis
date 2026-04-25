from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = ROOT_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
REPORTS_DIR = OUTPUTS_DIR / "reports"

RAW_PRICE_FILE = RAW_DIR / "fruit_prices_sample.csv"
RAW_ARCHIVE_FILE = RAW_DIR / "archive.zip"
THESIS_MAIN_DATASET_FILE = PROCESSED_DIR / "thesis_main_dataset_en.csv"
PROCESSED_PRICE_FILE = PROCESSED_DIR / "fruit_prices_cleaned.csv"
FORECAST_FILE = TABLES_DIR / "forecast_prices.csv"
FORECAST_METRICS_FILE = TABLES_DIR / "forecast_model_metrics.csv"
FORECAST_SELECTION_FILE = TABLES_DIR / "forecast_model_selection.csv"
STATS_FILE = TABLES_DIR / "descriptive_stats.csv"
RISK_FILE = TABLES_DIR / "risk_metrics.csv"
PLAN_FILE = TABLES_DIR / "procurement_plan.csv"
SUMMARY_FILE = REPORTS_DIR / "summary.md"
PRICE_FIGURE = FIGURES_DIR / "price_trends.png"


def ensure_directories() -> None:
    for path in [
        RAW_DIR,
        PROCESSED_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        REPORTS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
