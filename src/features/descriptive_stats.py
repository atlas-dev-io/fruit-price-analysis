import pandas as pd


def build_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = (
        df.groupby("fruit_name")["price"]
        .agg(["count", "mean", "min", "max", "std"])
        .reset_index()
        .rename(
            columns={
                "count": "sample_count",
                "mean": "avg_price",
                "min": "min_price",
                "max": "max_price",
                "std": "std_price",
            }
        )
    )
    return stats.round(4)

