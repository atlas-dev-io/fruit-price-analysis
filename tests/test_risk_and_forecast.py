import unittest

import numpy as np
import pandas as pd

from src.features.volatility import build_risk_metrics
from src.forecast.formal import build_formal_forecast


def build_sample_history() -> pd.DataFrame:
    dates = pd.date_range("2024-01-05", periods=72, freq="W-FRI")
    fruit_specs = {
        "Apple": {"base": 55, "amp": 2.0, "trend": 0.05},
        "Banana": {"base": 62, "amp": 6.0, "trend": 0.02},
        "Orange": {"base": 38, "amp": 3.5, "trend": 0.08},
    }

    rows = []
    for fruit_name, spec in fruit_specs.items():
        for idx, date in enumerate(dates):
            seasonal = spec["amp"] * np.sin(idx / 4)
            price = spec["base"] + seasonal + spec["trend"] * idx
            rows.append(
                {
                    "date": date,
                    "fruit_name": fruit_name,
                    "commodity_name": f"{fruit_name.lower()}_sample",
                    "market": "台北二",
                    "price": round(float(price), 4),
                    "unit": "kg",
                    "volume": 100 + idx,
                }
            )
    return pd.DataFrame(rows)


class RiskAndForecastTests(unittest.TestCase):
    def test_risk_metrics_include_explainable_fields(self):
        sample_df = build_sample_history()

        risk_df = build_risk_metrics(sample_df)

        self.assertIn("composite_risk_score", risk_df.columns)
        self.assertIn("risk_level", risk_df.columns)
        self.assertIn("risk_reason", risk_df.columns)
        self.assertEqual(len(risk_df), 3)
        self.assertEqual(set(risk_df["risk_level"]), {"high", "medium", "low"})

    def test_formal_forecast_outputs_weekly_model_selection(self):
        sample_df = build_sample_history()

        forecast_df, metrics_df, selection_df = build_formal_forecast(sample_df, periods=4)

        self.assertFalse(forecast_df.empty)
        self.assertFalse(metrics_df.empty)
        self.assertFalse(selection_df.empty)
        self.assertTrue((forecast_df["data_frequency"] == "weekly").all())
        self.assertEqual(selection_df["fruit_name"].nunique(), 3)
        self.assertTrue(selection_df["selected_model"].notna().all())


if __name__ == "__main__":
    unittest.main()
