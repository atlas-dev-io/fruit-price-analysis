import pandas as pd


def build_forecast(df: pd.DataFrame, periods: int = 4) -> pd.DataFrame:
    forecast_rows = []

    for fruit_name, group in df.groupby("fruit_name"):
        ordered = group.sort_values("date").reset_index(drop=True)
        recent_prices = ordered["price"].tail(3)
        forecast_price = float(recent_prices.mean())
        last_date = ordered["date"].max()
        market = ordered["market"].iloc[-1]

        for step in range(1, periods + 1):
            forecast_rows.append(
                {
                    "date": last_date + pd.Timedelta(days=7 * step),
                    "fruit_name": fruit_name,
                    "market": market,
                    "forecast_price": round(forecast_price, 4),
                }
            )

    return pd.DataFrame(forecast_rows).sort_values(["fruit_name", "date"]).reset_index(drop=True)

