import math
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX


FORECAST_HORIZON = 4
TEST_HORIZON = 8
MIN_REQUIRED_POINTS = 40
WEEKLY_FREQUENCY = "W-FRI"
ARIMA_ORDERS = [
    (0, 1, 1),
    (1, 1, 0),
    (1, 1, 1),
    (2, 1, 0),
    (2, 1, 1),
]
SARIMA_CONFIGS = [
    ((1, 1, 1), (0, 1, 1, 4)),
    ((1, 1, 1), (1, 0, 0, 13)),
]


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


def _build_weekly_series(group: pd.DataFrame) -> pd.Series:
    weekly = (
        group.sort_values("date")
        .set_index("date")["price"]
        .astype(float)
        .resample(WEEKLY_FREQUENCY)
        .mean()
        .interpolate(limit_direction="both")
        .dropna()
    )
    weekly.index.name = "date"
    return weekly


def _split_train_test(series: pd.Series) -> tuple[pd.Series, pd.Series]:
    test_len = TEST_HORIZON
    if len(series) < MIN_REQUIRED_POINTS:
        test_len = max(4, min(TEST_HORIZON, len(series) // 4))
    train = series.iloc[:-test_len]
    test = series.iloc[-test_len:]
    return train, test


def _fit_exponential_smoothing(train: pd.Series, test_len: int, forecast_len: int):
    model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal=None,
        initialization_method="estimated",
    )
    fitted = model.fit(optimized=True)
    return pd.Series(fitted.forecast(test_len)), pd.Series(fitted.forecast(forecast_len))


def _fit_arima(
    train: pd.Series,
    order: tuple[int, int, int],
    test_len: int,
    forecast_len: int,
):
    model = ARIMA(train, order=order)
    fitted = model.fit()
    return pd.Series(fitted.forecast(test_len)), pd.Series(fitted.forecast(forecast_len))


def _fit_sarima(
    train: pd.Series,
    order: tuple[int, int, int],
    seasonal_order: tuple[int, int, int, int],
    test_len: int,
    forecast_len: int,
):
    model = SARIMAX(
        train,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    fitted = model.fit(disp=False, maxiter=200)
    return pd.Series(fitted.forecast(test_len)), pd.Series(fitted.forecast(forecast_len))


def _fallback_forecast(series: pd.Series, periods: int) -> tuple[dict, pd.Series]:
    fallback = float(series.tail(4).mean())
    metrics = {"mae": 0.0, "rmse": 0.0, "mape": 0.0}
    return metrics, pd.Series([fallback] * periods)


def build_formal_forecast(
    df: pd.DataFrame, periods: int = FORECAST_HORIZON
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    forecast_rows = []
    metric_rows = []
    selection_rows = []

    for fruit_name, group in df.groupby("fruit_name"):
        weekly_series = _build_weekly_series(group)
        market = group["market"].iloc[-1]
        last_date = weekly_series.index.max()
        train, test = _split_train_test(weekly_series)

        candidate_results = {}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            try:
                predicted_test, future = _fit_exponential_smoothing(train, len(test), periods)
                candidate_results["exponential_smoothing"] = {
                    "metrics": _evaluate_predictions(test.reset_index(drop=True), predicted_test.reset_index(drop=True)),
                    "future": future,
                    "params": "trend=add;seasonal=None",
                    "family": "ETS",
                }
            except Exception:
                pass

            for order in ARIMA_ORDERS:
                model_name = f"arima_{order[0]}_{order[1]}_{order[2]}"
                try:
                    predicted_test, future = _fit_arima(train, order, len(test), periods)
                    candidate_results[model_name] = {
                        "metrics": _evaluate_predictions(
                            test.reset_index(drop=True),
                            predicted_test.reset_index(drop=True),
                        ),
                        "future": future,
                        "params": f"order={order}",
                        "family": "ARIMA",
                    }
                except Exception:
                    continue

            if len(train) >= 104:
                for order, seasonal_order in SARIMA_CONFIGS:
                    model_name = (
                        f"sarima_{order[0]}_{order[1]}_{order[2]}_"
                        f"{seasonal_order[0]}_{seasonal_order[1]}_{seasonal_order[2]}_{seasonal_order[3]}"
                    )
                    try:
                        predicted_test, future = _fit_sarima(
                            train,
                            order,
                            seasonal_order,
                            len(test),
                            periods,
                        )
                        candidate_results[model_name] = {
                            "metrics": _evaluate_predictions(
                                test.reset_index(drop=True),
                                predicted_test.reset_index(drop=True),
                            ),
                            "future": future,
                            "params": f"order={order};seasonal_order={seasonal_order}",
                            "family": "SARIMA",
                        }
                    except Exception:
                        continue

        if not candidate_results:
            fallback_metrics, future = _fallback_forecast(weekly_series, periods)
            candidate_results["moving_average_fallback"] = {
                "metrics": fallback_metrics,
                "future": future,
                "params": "window=4",
                "family": "Fallback",
            }

        best_model = min(candidate_results, key=lambda key: candidate_results[key]["metrics"]["rmse"])
        best_result = candidate_results[best_model]
        best_metrics = best_result["metrics"]

        for model_name, result in candidate_results.items():
            metrics = result["metrics"]
            metric_rows.append(
                {
                    "fruit_name": fruit_name,
                    "data_frequency": "weekly",
                    "train_points": len(train),
                    "test_points": len(test),
                    "test_start_date": test.index.min().date(),
                    "test_end_date": test.index.max().date(),
                    "model_family": result["family"],
                    "model_name": model_name,
                    "model_params": result["params"],
                    "mae": round(metrics["mae"], 4),
                    "rmse": round(metrics["rmse"], 4),
                    "mape": round(metrics["mape"], 4),
                }
            )

        selection_rows.append(
            {
                "fruit_name": fruit_name,
                "data_frequency": "weekly",
                "train_points": len(train),
                "test_points": len(test),
                "test_start_date": test.index.min().date(),
                "test_end_date": test.index.max().date(),
                "selected_model": best_model,
                "selected_family": best_result["family"],
                "selected_params": best_result["params"],
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
                    "forecast_price": round(float(best_result["future"].iloc[step - 1]), 4),
                    "selected_model": best_model,
                    "selected_family": best_result["family"],
                    "selected_params": best_result["params"],
                    "data_frequency": "weekly",
                }
            )

    forecast_df = pd.DataFrame(forecast_rows).sort_values(["fruit_name", "date"]).reset_index(drop=True)
    metrics_df = pd.DataFrame(metric_rows).sort_values(["fruit_name", "rmse"]).reset_index(drop=True)
    selection_df = pd.DataFrame(selection_rows).sort_values(["fruit_name"]).reset_index(drop=True)
    return forecast_df, metrics_df, selection_df
