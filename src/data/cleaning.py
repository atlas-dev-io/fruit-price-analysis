import pandas as pd


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["fruit_name"] = cleaned["fruit_name"].str.strip()
    cleaned["commodity_name"] = cleaned["commodity_name"].astype(str).str.strip()
    cleaned["market"] = cleaned["market"].str.strip()
    cleaned["unit"] = cleaned["unit"].astype(str).str.strip().str.lower()
    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    cleaned = cleaned.dropna(subset=["date", "fruit_name", "price"])
    cleaned = cleaned[cleaned["price"] > 0]
    cleaned = cleaned[cleaned["unit"].isin(["kg", "kg ", "kg.", "kgs", "kgs."]) | (cleaned["unit"] == "kg")]
    cleaned["unit"] = "kg"
    cleaned = cleaned.sort_values(["fruit_name", "date"]).reset_index(drop=True)

    # Fill sparse gaps within each fruit series to keep the demo pipeline runnable.
    cleaned["price"] = cleaned.groupby("fruit_name")["price"].transform(
        lambda series: series.interpolate(limit_direction="both")
    )
    return cleaned
