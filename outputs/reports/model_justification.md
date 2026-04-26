# Forecast Model Justification

## Modeling Scope

The ARIMA search space is limited to low-order weekly models: (0,1,1), (1,1,0), (1,1,1), (2,1,0), and (2,1,1). This keeps the thesis model set interpretable while still allowing short-memory autoregressive and moving-average structures. SARIMA is not searched exhaustively; it is only evaluated for series with stronger measured seasonality, using two targeted weekly seasonal candidates.

## Stationarity And Selection Notes

- Apple: selected arima_0_1_1 [order=(0, 1, 1)], ADF(level)=0.0, ADF(diff1)=0.0, seasonality_candidate=yes.
- Banana: selected arima_0_1_1 [order=(0, 1, 1)], ADF(level)=0.0003, ADF(diff1)=0.0, seasonality_candidate=yes.
- Grape: selected arima_2_1_0 [order=(2, 1, 0)], ADF(level)=0.0, ADF(diff1)=0.0, seasonality_candidate=yes.
- Orange: selected sarima_1_1_1_0_1_1_4 [order=(1, 1, 1);seasonal_order=(0, 1, 1, 4)], ADF(level)=0.0, ADF(diff1)=0.0, seasonality_candidate=yes.
- Pear: selected exponential_smoothing [trend=add;seasonal=None], ADF(level)=0.0, ADF(diff1)=0.0, seasonality_candidate=no.
