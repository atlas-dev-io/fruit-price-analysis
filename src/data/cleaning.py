import pandas as pd


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["fruit_name"] = cleaned["fruit_name"].str.strip()
    cleaned["commodity_name"] = cleaned["commodity_name"].astype(str).str.strip()
    cleaned["market"] = cleaned["market"].str.strip()
    cleaned["unit"] = cleaned["unit"].astype(str).str.strip().str.lower()
    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    if "volume" not in cleaned.columns:
        cleaned["volume"] = pd.NA
    cleaned["volume"] = pd.to_numeric(cleaned["volume"], errors="coerce")
    cleaned = cleaned.dropna(subset=["date", "fruit_name", "price"])
    cleaned = cleaned[cleaned["price"] > 0]
    cleaned = cleaned[
        cleaned["unit"].isin(["kg", "kg ", "kg.", "kgs", "kgs.", "twd/kg"]) | (cleaned["unit"] == "kg")
    ]
    cleaned["unit"] = "kg"
    cleaned = cleaned.sort_values(["fruit_name", "date"]).reset_index(drop=True)

    def _aggregate(group: pd.DataFrame) -> pd.Series:
        valid_volume = group["volume"].fillna(0)
        weighted = float((group["price"] * valid_volume).sum())
        total_volume = float(valid_volume.sum())
        if total_volume > 0:
            price = weighted / total_volume
        else:
            price = float(group["price"].mean())
        return pd.Series(
            {
                "commodity_name": "aggregated_daily_price",
                "market": group["market"].iloc[0],
                "price": price,
                "unit": "kg",
                "volume": total_volume if total_volume > 0 else pd.NA,
            }
        )

    cleaned = (
        cleaned.groupby(["fruit_name", "date"], as_index=False)
        .apply(_aggregate, include_groups=False)
        .reset_index()
    )
    if "level_2" in cleaned.columns:
        cleaned = cleaned.drop(columns=["level_2"])
    cleaned = cleaned.sort_values(["fruit_name", "date"]).reset_index(drop=True)

    # Fill sparse gaps within each fruit series to keep the demo pipeline runnable.
    cleaned["price"] = cleaned.groupby("fruit_name")["price"].transform(
        lambda series: series.interpolate(limit_direction="both")
    )
    return cleaned
