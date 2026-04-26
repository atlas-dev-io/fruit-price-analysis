import numpy as np
import pandas as pd


RISK_WEIGHTS = {
    "coefficient_of_variation": 0.4,
    "max_drawdown": 0.3,
    "return_volatility": 0.3,
}


def _max_drawdown(prices: pd.Series) -> float:
    running_max = prices.cummax()
    drawdown = (prices - running_max) / running_max
    return float(abs(drawdown.min()))


def _zscore(series: pd.Series) -> pd.Series:
    std = float(series.std(ddof=0))
    if std == 0:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return (series - float(series.mean())) / std


def _assign_risk_levels(score_series: pd.Series) -> pd.Series:
    ranked = score_series.rank(method="first")
    return pd.qcut(ranked, q=3, labels=["low", "medium", "high"]).astype(str)


def _explain_risk_row(row: pd.Series) -> str:
    contributors = [
        ("variation", row["coefficient_of_variation_zscore"]),
        ("drawdown", row["max_drawdown_zscore"]),
        ("return_volatility", row["return_volatility_zscore"]),
    ]
    contributors.sort(key=lambda item: item[1], reverse=True)
    top_name, top_score = contributors[0]
    if top_score > 0.75:
        intensity = "well above the cross-fruit average"
    elif top_score > 0:
        intensity = "above the cross-fruit average"
    elif top_score < -0.75:
        intensity = "well below the cross-fruit average"
    else:
        intensity = "close to the cross-fruit average"

    return (
        f"{row['risk_level']} risk because composite score {row['composite_risk_score']:.4f} "
        f"is driven most by {top_name} being {intensity}."
    )


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

    risk_df = pd.DataFrame(rows).sort_values("fruit_name").reset_index(drop=True)

    for metric_name, weight in RISK_WEIGHTS.items():
        zscore_column = f"{metric_name}_zscore"
        weighted_column = f"{metric_name}_weighted"
        risk_df[zscore_column] = _zscore(risk_df[metric_name]).round(4)
        risk_df[weighted_column] = (risk_df[zscore_column] * weight).round(4)

    weighted_columns = [f"{metric_name}_weighted" for metric_name in RISK_WEIGHTS]
    risk_df["composite_risk_score"] = risk_df[weighted_columns].sum(axis=1).round(4)
    risk_df["risk_percentile"] = (
        risk_df["composite_risk_score"].rank(method="average", pct=True).round(4)
    )
    risk_df["risk_level"] = _assign_risk_levels(risk_df["composite_risk_score"])
    risk_df = risk_df.sort_values("composite_risk_score", ascending=False).reset_index(drop=True)
    risk_df["risk_reason"] = risk_df.apply(_explain_risk_row, axis=1)
    return risk_df


def build_risk_classification_table(risk_df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "fruit_name",
        "coefficient_of_variation",
        "max_drawdown",
        "return_volatility",
        "coefficient_of_variation_zscore",
        "max_drawdown_zscore",
        "return_volatility_zscore",
        "composite_risk_score",
        "risk_percentile",
        "risk_level",
        "risk_reason",
    ]
    return risk_df[columns].copy()
