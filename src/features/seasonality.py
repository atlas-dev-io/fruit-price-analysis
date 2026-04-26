import pandas as pd


def build_seasonality_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for fruit_name, group in df.groupby("fruit_name"):
        ordered = group.sort_values("date").copy()
        ordered["month"] = ordered["date"].dt.month
        monthly_avg = ordered.groupby("month")["price"].mean()
        overall_mean = float(ordered["price"].mean())
        total_std = float(ordered["price"].std(ddof=0))
        seasonal_component_std = float(monthly_avg.std(ddof=0))
        seasonality_strength = (
            seasonal_component_std / total_std if total_std and not pd.isna(total_std) else 0.0
        )
        peak_month = int(monthly_avg.idxmax())
        trough_month = int(monthly_avg.idxmin())
        peak_price = float(monthly_avg.loc[peak_month])
        trough_price = float(monthly_avg.loc[trough_month])

        rows.append(
            {
                "fruit_name": fruit_name,
                "overall_avg_price": round(overall_mean, 4),
                "seasonality_strength": round(seasonality_strength, 4),
                "peak_month": peak_month,
                "peak_month_avg_price": round(peak_price, 4),
                "trough_month": trough_month,
                "trough_month_avg_price": round(trough_price, 4),
                "seasonal_range": round(peak_price - trough_price, 4),
            }
        )

    return pd.DataFrame(rows).sort_values("seasonality_strength", ascending=False).reset_index(drop=True)


def build_seasonality_profile(df: pd.DataFrame) -> pd.DataFrame:
    profile = (
        df.assign(month=df["date"].dt.month)
        .groupby(["fruit_name", "month"], as_index=False)
        .agg(avg_price=("price", "mean"))
        .sort_values(["fruit_name", "month"])
        .reset_index(drop=True)
    )
    profile["avg_price"] = profile["avg_price"].round(4)
    return profile


def build_seasonality_report(seasonality_df: pd.DataFrame) -> str:
    strongest = seasonality_df.iloc[0]
    weakest = seasonality_df.sort_values("seasonality_strength").iloc[0]

    lines = [
        "# Seasonality Analysis",
        "",
        "## Chapter-Ready Summary",
        "",
        (
            f"The monthly seasonality analysis shows that {strongest['fruit_name']} has the strongest "
            f"seasonal pattern, with a seasonality strength of {strongest['seasonality_strength']:.4f}, "
            f"peaking in month {int(strongest['peak_month'])} and bottoming in month "
            f"{int(strongest['trough_month'])}. By contrast, {weakest['fruit_name']} shows the weakest "
            f"seasonal structure, with a seasonality strength of {weakest['seasonality_strength']:.4f}. "
            "This result can be used to support the thesis discussion on seasonal fluctuations and to "
            "justify why seasonal candidates such as SARIMA are only retained for selected fruit series."
        ),
        "",
        "## Per-Fruit Findings",
        "",
    ]

    for row in seasonality_df.itertuples():
        lines.append(
            f"- {row.fruit_name}: strength={row.seasonality_strength:.4f}, "
            f"peak_month={row.peak_month}, trough_month={row.trough_month}, "
            f"seasonal_range={row.seasonal_range:.4f}"
        )

    return "\n".join(lines) + "\n"
