import pandas as pd


BASE_DEMAND = {
    "Apple": 120,
    "Banana": 115,
    "Orange": 105,
    "Grape": 75,
    "Pear": 100,
}


def build_procurement_plan(
    forecast_df: pd.DataFrame, risk_df: pd.DataFrame
) -> pd.DataFrame:
    risk_lookup = risk_df.set_index("fruit_name").to_dict("index")
    rows = []

    for _, row in forecast_df.iterrows():
        fruit_name = row["fruit_name"]
        risk_info = risk_lookup[fruit_name]
        risk_level = risk_info["risk_level"]
        demand = BASE_DEMAND.get(fruit_name, 80)

        if risk_level == "high":
            strategy = "分批采购，缩短采购周期"
            multiplier = 0.85
        elif risk_level == "medium":
            strategy = "按预测价格灵活调整采购"
            multiplier = 1.0
        else:
            strategy = "稳定采购，低价期可适度多采"
            multiplier = 1.1

        rows.append(
            {
                "date": row["date"],
                "fruit_name": fruit_name,
                "forecast_price": row["forecast_price"],
                "risk_level": risk_level,
                "composite_risk_score": round(float(risk_info["composite_risk_score"]), 4),
                "recommended_quantity_kg": round(demand * multiplier, 2),
                "strategy": strategy,
            }
        )

    return pd.DataFrame(rows).sort_values(["date", "fruit_name"]).reset_index(drop=True)
