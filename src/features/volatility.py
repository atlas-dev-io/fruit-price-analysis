import numpy as np
import pandas as pd


def _max_drawdown(prices: pd.Series) -> float:
    running_max = prices.cummax()
    drawdown = (prices - running_max) / running_max
    return float(abs(drawdown.min()))


def build_risk_metrics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for fruit_name, group in df.groupby("fruit_name"):
        prices = group.sort_values("date")["price"].reset_index(drop=True)
        avg_price = float(prices.mean())
        std_price = float(prices.std(ddof=1)) if len(prices) > 1 else 0.0
        cv = std_price / avg_price if avg_price else 0.0
        returns = prices.pct_change().dropna()
        rows.append(
            {
                "fruit_name": fruit_name,
                "avg_price": round(avg_price, 4),
                "std_price": round(std_price, 4),
                "coefficient_of_variation": round(cv, 4),
                "max_drawdown": round(_max_drawdown(prices), 4),
                "avg_return": round(float(returns.mean()) if not returns.empty else 0.0, 4),
                "return_volatility": round(
                    float(returns.std(ddof=1)) if len(returns) > 1 else 0.0, 4
                ),
            }
        )

    return pd.DataFrame(rows).sort_values("coefficient_of_variation", ascending=False)


def classify_risk(cv: float) -> str:
    if cv >= 0.12:
        return "high"
    if cv >= 0.07:
        return "medium"
    return "stable"

