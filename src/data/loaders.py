import zipfile
from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = ["date", "fruit_name", "commodity_name", "market", "price", "unit"]

ARCHIVE_MEMBERS = [
    "data  from June 2013 to May 2021.csv",
    "data from-may-2021-to-september-2023.csv",
]

FRUIT_KEYWORDS = {
    "apple": "Apple",
    "banana": "Banana",
    "orange": "Orange",
    "sweet orange": "Orange",
    "sweet lime": "Sweet Lime",
    "lime": "Lime",
    "lemon": "Lemon",
    "grapes": "Grapes",
    "grape": "Grapes",
    "guava": "Guava",
    "mango": "Mango",
    "papaya": "Papaya",
    "pear": "Pear",
    "pineapple": "Pineapple",
    "pomegranate": "Pomegranate",
    "water melon": "Watermelon",
    "watermelon": "Watermelon",
    "amla": "Amla",
    "avocado": "Avocado",
}


def _map_fruit_name(commodity_name: str) -> str | None:
    lower_name = commodity_name.lower()
    for keyword, fruit_name in sorted(FRUIT_KEYWORDS.items(), key=lambda item: -len(item[0])):
        if keyword in lower_name:
            return fruit_name
    return None


def _parse_price(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.replace(r"[^0-9.]+", "", regex=True)
    cleaned = cleaned.replace("", pd.NA)
    return pd.to_numeric(cleaned, errors="coerce")


def _load_archive(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        first = pd.read_csv(archive.open(ARCHIVE_MEMBERS[0]))
        second = pd.read_csv(
            archive.open(ARCHIVE_MEMBERS[1]),
            header=None,
            names=["Commodity", "Date", "Unit", "Minimum", "Maximum", "Average"],
        )

    first = first[["Commodity", "Date", "Unit", "Minimum", "Maximum", "Average"]].copy()
    second = second[["Commodity", "Date", "Unit", "Minimum", "Maximum", "Average"]].copy()

    first["Date"] = pd.to_datetime(first["Date"], errors="coerce")
    second["Date"] = pd.to_datetime(
        second["Date"], format="mixed", dayfirst=False, errors="coerce"
    )

    combined = pd.concat([first, second], ignore_index=True)
    combined["commodity_name"] = combined["Commodity"].astype(str).str.strip()
    combined["fruit_name"] = combined["commodity_name"].map(_map_fruit_name)
    combined = combined.dropna(subset=["fruit_name", "Date"]).copy()
    combined["market"] = "Kalimati Market"
    combined["unit"] = combined["Unit"].astype(str).str.strip()
    min_price = _parse_price(combined["Minimum"])
    max_price = _parse_price(combined["Maximum"])
    avg_price = _parse_price(combined["Average"])
    combined["price"] = avg_price.fillna((min_price + max_price) / 2)
    combined["date"] = combined["Date"]

    return combined[
        ["date", "fruit_name", "commodity_name", "market", "price", "unit"]
    ].reset_index(drop=True)


def _load_thesis_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    rename_map = {
        "trade_date": "date",
        "fruit_category": "fruit_name",
        "crop_name_zh": "commodity_name",
        "market_name": "market",
        "avg_price_twd_per_kg": "price",
        "volume_kg": "volume",
    }
    df = df.rename(columns=rename_map)
    df["date"] = pd.to_datetime(df["date"])
    df["fruit_name"] = df["fruit_name"].astype(str).str.strip().str.title()
    df["commodity_name"] = df["commodity_name"].astype(str).str.strip()
    df["market"] = df["market"].astype(str).str.strip()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["volume"] = pd.to_numeric(df.get("volume"), errors="coerce")
    df["unit"] = "kg"
    return df[
        ["date", "fruit_name", "commodity_name", "market", "price", "unit", "volume"]
    ].reset_index(drop=True)


def load_price_data(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".zip":
        df = _load_archive(path)
    else:
        df = pd.read_csv(path)
        if "trade_date" in df.columns and "fruit_category" in df.columns:
            df = _load_thesis_dataset(path)
        elif "commodity_name" not in df.columns:
            df["commodity_name"] = df.get("fruit_name", "")

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    return df
