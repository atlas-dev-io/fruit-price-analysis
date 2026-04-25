import pandas as pd
from pathlib import Path


INPUT_PATH = Path("data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv")
OUTPUT_PATH = Path("data/processed/thesis_main_dataset_en.csv")
SUMMARY_PATH = Path("outputs/reports/thesis_main_dataset_summary.md")


def roc_to_gregorian(date_text: str) -> str:
    year_text, month_text, day_text = str(date_text).split(".")
    year = int(year_text) + 1911
    return f"{year:04d}-{int(month_text):02d}-{int(day_text):02d}"


def map_fruit_category(crop_name: str) -> str | None:
    crop_name = str(crop_name).strip()

    if crop_name.startswith("蘋果-"):
        return "apple"
    if crop_name.startswith("香蕉"):
        return "banana"
    if crop_name in {"甜橙-柳橙", "甜橙-紅肉柳橙"}:
        return "orange"
    if crop_name.startswith("葡萄-"):
        return "grape"
    if crop_name.startswith("梨-"):
        return "pear"
    return None


def build_summary(df: pd.DataFrame) -> str:
    overview = (
        df.groupby("fruit_category")
        .agg(
            rows=("fruit_category", "size"),
            start_date=("trade_date", "min"),
            end_date=("trade_date", "max"),
            avg_price_twd_per_kg=("avg_price_twd_per_kg", "mean"),
        )
        .reset_index()
    )

    lines = [
        "# Thesis Main Dataset Summary",
        "",
        f"- Source file: `{INPUT_PATH}`",
        f"- Output file: `{OUTPUT_PATH}`",
        f"- Total rows: {len(df)}",
        f"- Date range: {df['trade_date'].min().date()} to {df['trade_date'].max().date()}",
        f"- Market: {', '.join(sorted(df['market_name'].unique()))}",
        "",
        "## Fruit Coverage",
        "",
        "| fruit_category | rows | start_date | end_date | avg_price_twd_per_kg |",
        "| --- | ---: | --- | --- | ---: |",
    ]

    for _, row in overview.iterrows():
        lines.append(
            f"| {row['fruit_category']} | {int(row['rows'])} | {row['start_date'].date()} | "
            f"{row['end_date'].date()} | {row['avg_price_twd_per_kg']:.2f} |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    df = pd.read_csv(INPUT_PATH)

    df["fruit_category"] = df["作物名稱"].map(map_fruit_category)
    cleaned = df.dropna(subset=["fruit_category"]).copy()

    cleaned["trade_date"] = pd.to_datetime(cleaned["交易日期"].map(roc_to_gregorian))
    cleaned["market_code"] = cleaned["市場代號"].astype(str)
    cleaned["market_name"] = cleaned["市場名稱"].astype(str)
    cleaned["crop_code"] = cleaned["作物代號"].astype(str)
    cleaned["crop_name_zh"] = cleaned["作物名稱"].astype(str)
    cleaned["high_price_twd_per_kg"] = pd.to_numeric(cleaned["上價"], errors="coerce")
    cleaned["mid_price_twd_per_kg"] = pd.to_numeric(cleaned["中價"], errors="coerce")
    cleaned["low_price_twd_per_kg"] = pd.to_numeric(cleaned["下價"], errors="coerce")
    cleaned["avg_price_twd_per_kg"] = pd.to_numeric(cleaned["平均價"], errors="coerce")
    cleaned["volume_kg"] = pd.to_numeric(cleaned["交易量"], errors="coerce")
    cleaned["price_unit"] = "TWD/kg"
    cleaned["volume_unit"] = "kg"

    cleaned = cleaned[
        [
            "trade_date",
            "fruit_category",
            "crop_name_zh",
            "crop_code",
            "market_code",
            "market_name",
            "high_price_twd_per_kg",
            "mid_price_twd_per_kg",
            "low_price_twd_per_kg",
            "avg_price_twd_per_kg",
            "volume_kg",
            "price_unit",
            "volume_unit",
        ]
    ].sort_values(["fruit_category", "trade_date", "crop_name_zh"]).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    cleaned.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    SUMMARY_PATH.write_text(build_summary(cleaned), encoding="utf-8")

    print(f"wrote {len(cleaned)} rows to {OUTPUT_PATH}")
    print(f"wrote summary to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
