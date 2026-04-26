import numpy as np
import pandas as pd
from scipy.optimize import linprog


BASE_DEMAND = {
    "Apple": 120,
    "Banana": 115,
    "Orange": 105,
    "Grape": 75,
    "Pear": 100,
}

RISK_PENALTY_FACTOR = 0.08
HOLDING_COST_FACTOR = 0.002
PURCHASE_CAP_MULTIPLIER = {
    "high": 1.1,
    "medium": 1.35,
    "low": 1.6,
}
INVENTORY_CAP_MULTIPLIER = {
    "high": 0.25,
    "medium": 0.6,
    "low": 1.0,
}


def _build_strategy(
    risk_level: str,
    purchased_kg: float,
    demand_kg: float,
    ending_inventory_kg: float,
) -> str:
    if purchased_kg <= demand_kg * 0.05:
        return "线性规划结果：优先消化前期库存，减少当期采购"
    if risk_level == "high" and purchased_kg <= demand_kg * 1.01:
        return "线性规划结果：高风险品类以按需分批采购为主"
    if ending_inventory_kg > demand_kg * 0.15:
        return "线性规划结果：在低风险或低价期前置采购并保留库存"
    if purchased_kg > demand_kg * 1.05:
        return "线性规划结果：适度前置采购以降低后续成本"
    return "线性规划结果：按周滚动采购并控制库存"


def _clean_numeric(value: float) -> float:
    if abs(value) < 1e-9:
        return 0.0
    return float(value)


def _fallback_plan(group: pd.DataFrame, risk_info: dict, demand: float) -> pd.DataFrame:
    rows = []
    risk_level = risk_info["risk_level"]
    cap = demand * PURCHASE_CAP_MULTIPLIER[risk_level]
    for row in group.itertuples():
        purchased_kg = min(demand, cap)
        rows.append(
            {
                "date": row.date,
                "fruit_name": row.fruit_name,
                "forecast_price": row.forecast_price,
                "risk_level": risk_level,
                "risk_percentile": round(float(risk_info["risk_percentile"]), 4),
                "composite_risk_score": round(float(risk_info["composite_risk_score"]), 4),
                "period_demand_kg": round(demand, 2),
                "purchase_cap_kg": round(cap, 2),
                "recommended_quantity_kg": round(purchased_kg, 2),
                "ending_inventory_kg": 0.0,
                "purchase_cost": round(float(purchased_kg * row.forecast_price), 2),
                "risk_penalty_cost": round(
                    float(
                        purchased_kg
                        * row.forecast_price
                        * RISK_PENALTY_FACTOR
                        * float(risk_info["risk_percentile"])
                    ),
                    2,
                ),
                "holding_cost": 0.0,
                "optimization_status": "fallback",
                "strategy": "回退方案：按需采购，未使用线性规划最优解",
            }
        )
    return pd.DataFrame(rows)


def _optimize_one_fruit(group: pd.DataFrame, risk_info: dict, demand: float) -> pd.DataFrame:
    ordered = group.sort_values("date").reset_index(drop=True)
    periods = len(ordered)
    risk_level = str(risk_info["risk_level"])
    risk_percentile = float(risk_info["risk_percentile"])
    purchase_cap = demand * PURCHASE_CAP_MULTIPLIER[risk_level]
    inventory_cap = demand * INVENTORY_CAP_MULTIPLIER[risk_level]
    avg_forecast_price = float(ordered["forecast_price"].mean())
    holding_cost_per_kg = avg_forecast_price * HOLDING_COST_FACTOR

    purchase_costs = ordered["forecast_price"].to_numpy(dtype=float)
    risk_penalty_per_kg = purchase_costs * RISK_PENALTY_FACTOR * risk_percentile
    inventory_costs = np.full(periods, holding_cost_per_kg, dtype=float)
    objective = np.concatenate([purchase_costs + risk_penalty_per_kg, inventory_costs])

    variable_count = periods * 2
    a_eq = np.zeros((periods, variable_count), dtype=float)
    b_eq = np.full(periods, demand, dtype=float)

    for idx in range(periods):
        purchase_idx = idx
        inventory_idx = periods + idx
        a_eq[idx, purchase_idx] = 1.0
        a_eq[idx, inventory_idx] = -1.0
        if idx > 0:
            previous_inventory_idx = periods + idx - 1
            a_eq[idx, previous_inventory_idx] = 1.0

    bounds = [(0.0, purchase_cap)] * periods + [(0.0, inventory_cap)] * periods
    result = linprog(c=objective, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not result.success:
        return _fallback_plan(ordered, risk_info, demand)

    purchases = result.x[:periods]
    inventories = result.x[periods:]
    rows = []
    for idx, row in enumerate(ordered.itertuples()):
        purchase_qty = _clean_numeric(purchases[idx])
        ending_inventory = _clean_numeric(inventories[idx])
        purchase_cost = float(purchase_qty * row.forecast_price)
        risk_penalty_cost = float(purchase_qty * risk_penalty_per_kg[idx])
        holding_cost = float(ending_inventory * holding_cost_per_kg)
        rows.append(
            {
                "date": row.date,
                "fruit_name": row.fruit_name,
                "forecast_price": row.forecast_price,
                "risk_level": risk_level,
                "risk_percentile": round(risk_percentile, 4),
                "composite_risk_score": round(float(risk_info["composite_risk_score"]), 4),
                "period_demand_kg": round(demand, 2),
                "purchase_cap_kg": round(purchase_cap, 2),
                "recommended_quantity_kg": round(purchase_qty, 2),
                "ending_inventory_kg": round(ending_inventory, 2),
                "purchase_cost": round(purchase_cost, 2),
                "risk_penalty_cost": round(risk_penalty_cost, 2),
                "holding_cost": round(holding_cost, 2),
                "optimization_status": "optimal",
                "strategy": _build_strategy(
                    risk_level=risk_level,
                    purchased_kg=purchase_qty,
                    demand_kg=demand,
                    ending_inventory_kg=ending_inventory,
                ),
            }
        )

    return pd.DataFrame(rows)


def build_procurement_plan(
    forecast_df: pd.DataFrame, risk_df: pd.DataFrame
) -> pd.DataFrame:
    risk_lookup = risk_df.set_index("fruit_name").to_dict("index")
    plan_frames = []

    for fruit_name, group in forecast_df.groupby("fruit_name"):
        risk_info = risk_lookup[fruit_name]
        demand = float(BASE_DEMAND.get(fruit_name, 80))
        plan_frames.append(_optimize_one_fruit(group, risk_info, demand))

    return pd.concat(plan_frames, ignore_index=True).sort_values(
        ["date", "fruit_name"]
    ).reset_index(drop=True)
