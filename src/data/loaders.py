import pandas as pd
import zipfile
from pathlib import Path


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


def load_price_data(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".zip":
        df = _load_archive(path)
    else:
        df = pd.read_csv(path)
        if "commodity_name" not in df.columns:
            df["commodity_name"] = df.get("fruit_name", "")

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    return df
