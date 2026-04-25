import math
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA


FORECAST_HORIZON = 4


def _safe_mape(actual: pd.Series, predicted: pd.Series) -> float:
    mask = actual != 0
    if not mask.any():
        return 0.0
    return float((np.abs((actual[mask] - predicted[mask]) / actual[mask])).mean() * 100)


def _evaluate_predictions(actual: pd.Series, predicted: pd.Series) -> dict:
    error = actual - predicted
    return {
        "mae": float(np.abs(error).mean()),
        "rmse": float(math.sqrt((error**2).mean())),
        "mape": _safe_mape(actual, predicted),
    }


def _fit_exponential_smoothing(train: pd.Series, test_len: int, forecast_len: int):
    model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal=None,
        initialization_method="estimated",
    )
    fitted = model.fit(optimized=True)
    return fitted.forecast(test_len), fitted.forecast(forecast_len)


def _fit_arima(train: pd.Series, test_len: int, forecast_len: int):
    model = ARIMA(train, order=(1, 1, 1))
    fitted = model.fit()
    forecast = fitted.forecast(test_len)
    future = fitted.forecast(forecast_len)
    return forecast, future


def build_formal_forecast(
    df: pd.DataFrame, periods: int = FORECAST_HORIZON
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    forecast_rows = []
    metric_rows = []
    selection_rows = []

    for fruit_name, group in df.groupby("fruit_name"):
        ordered = group.sort_values("date").reset_index(drop=True)
        series = ordered["price"].astype(float)
        market = ordered["market"].iloc[-1]
        last_date = ordered["date"].max()

        if len(series) < 16:
            train = series.iloc[:-4]
            test = series.iloc[-4:]
        else:
            train = series.iloc[:-8]
            test = series.iloc[-8:]

        candidate_results = {}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            try:
                predicted_test, future = _fit_exponential_smoothing(train, len(test), periods)
                candidate_results["exponential_smoothing"] = (
                    _evaluate_predictions(test.reset_index(drop=True), predicted_test.reset_index(drop=True)),
                    future,
                )
            except Exception:
                pass

            try:
                predicted_test, future = _fit_arima(train, len(test), periods)
                candidate_results["arima_1_1_1"] = (
                    _evaluate_predictions(test.reset_index(drop=True), pd.Series(predicted_test).reset_index(drop=True)),
                    pd.Series(future),
                )
            except Exception:
                pass

        if not candidate_results:
            fallback = series.tail(3).mean()
            metrics = {"mae": 0.0, "rmse": 0.0, "mape": 0.0}
            best_model = "moving_average_fallback"
            future = pd.Series([fallback] * periods)
            candidate_results[best_model] = (metrics, future)

        best_model = min(candidate_results, key=lambda key: candidate_results[key][0]["rmse"])
        best_metrics, best_future = candidate_results[best_model]

        for model_name, (metrics, _) in candidate_results.items():
            metric_rows.append(
                {
                    "fruit_name": fruit_name,
                    "model_name": model_name,
                    "mae": round(metrics["mae"], 4),
                    "rmse": round(metrics["rmse"], 4),
                    "mape": round(metrics["mape"], 4),
                }
            )

        selection_rows.append(
            {
                "fruit_name": fruit_name,
                "selected_model": best_model,
                "rmse": round(best_metrics["rmse"], 4),
                "mae": round(best_metrics["mae"], 4),
                "mape": round(best_metrics["mape"], 4),
            }
        )

        for step in range(1, periods + 1):
            forecast_rows.append(
                {
                    "date": last_date + pd.Timedelta(days=7 * step),
                    "fruit_name": fruit_name,
                    "market": market,
                    "forecast_price": round(float(best_future.iloc[step - 1]), 4),
                    "selected_model": best_model,
                }
            )

    forecast_df = pd.DataFrame(forecast_rows).sort_values(["fruit_name", "date"]).reset_index(drop=True)
    metrics_df = pd.DataFrame(metric_rows).sort_values(["fruit_name", "rmse"]).reset_index(drop=True)
    selection_df = pd.DataFrame(selection_rows).sort_values(["fruit_name"]).reset_index(drop=True)
    return forecast_df, metrics_df, selection_df
