import unittest

import pandas as pd

from src.optimization.model import build_heuristic_procurement_plan, build_procurement_plan


class ProcurementOptimizationTests(unittest.TestCase):
    def setUp(self):
        self.forecast_df = pd.DataFrame(
            [
                {"date": pd.Timestamp("2026-05-02"), "fruit_name": "Orange", "market": "台北二", "forecast_price": 40.0},
                {"date": pd.Timestamp("2026-05-09"), "fruit_name": "Orange", "market": "台北二", "forecast_price": 42.0},
                {"date": pd.Timestamp("2026-05-16"), "fruit_name": "Orange", "market": "台北二", "forecast_price": 47.0},
                {"date": pd.Timestamp("2026-05-23"), "fruit_name": "Orange", "market": "台北二", "forecast_price": 43.0},
                {"date": pd.Timestamp("2026-05-02"), "fruit_name": "Pear", "market": "台北二", "forecast_price": 65.0},
                {"date": pd.Timestamp("2026-05-09"), "fruit_name": "Pear", "market": "台北二", "forecast_price": 64.8},
                {"date": pd.Timestamp("2026-05-16"), "fruit_name": "Pear", "market": "台北二", "forecast_price": 64.6},
                {"date": pd.Timestamp("2026-05-23"), "fruit_name": "Pear", "market": "台北二", "forecast_price": 64.4},
            ]
        )
        self.risk_df = pd.DataFrame(
            [
                {
                    "fruit_name": "Orange",
                    "risk_level": "low",
                    "risk_percentile": 0.4,
                    "composite_risk_score": -0.45,
                },
                {
                    "fruit_name": "Pear",
                    "risk_level": "high",
                    "risk_percentile": 1.0,
                    "composite_risk_score": 1.83,
                },
            ]
        )

    def test_optimized_plan_respects_constraints_and_is_not_empty(self):
        plan_df = build_procurement_plan(self.forecast_df, self.risk_df)

        self.assertFalse(plan_df.empty)
        self.assertTrue((plan_df["recommended_quantity_kg"] >= 0).all())
        self.assertTrue((plan_df["ending_inventory_kg"] >= 0).all())
        self.assertTrue((plan_df["optimization_status"] == "optimal").all())

        orange_plan = plan_df[plan_df["fruit_name"] == "Orange"]
        pear_plan = plan_df[plan_df["fruit_name"] == "Pear"]
        self.assertGreater(orange_plan["ending_inventory_kg"].max(), 0.0)
        self.assertTrue((pear_plan["recommended_quantity_kg"] <= pear_plan["purchase_cap_kg"]).all())

    def test_cost_comparison_baseline_is_available(self):
        optimized_df = build_procurement_plan(self.forecast_df, self.risk_df)
        heuristic_df = build_heuristic_procurement_plan(self.forecast_df, self.risk_df)

        self.assertEqual(len(optimized_df), len(heuristic_df))
        self.assertIn("heuristic_baseline", set(heuristic_df["optimization_status"]))


if __name__ == "__main__":
    unittest.main()
