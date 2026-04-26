# Pipeline Summary

- Average observed price across fruits: 63.1 TWD/kg
- Fruit categories included: 5
- Most stable fruit in the sample: Apple
- Highest-volatility fruit in the sample: Pear
- Forecast window: 2026-05-01 to 2026-05-22
- Weekly evaluation window by fruit: Apple:2026-03-06 to 2026-04-24, Banana:2026-03-06 to 2026-04-24, Grape:2026-03-06 to 2026-04-24, Orange:2026-03-06 to 2026-04-24, Pear:2026-03-06 to 2026-04-24
- Selected forecast model by fruit: Apple:arima_0_1_1[order=(0, 1, 1)], Banana:arima_0_1_1[order=(0, 1, 1)], Grape:arima_2_1_0[order=(2, 1, 0)], Orange:sarima_1_1_1_0_1_1_4[order=(1, 1, 1);seasonal_order=(0, 1, 1, 4)], Pear:exponential_smoothing[trend=add;seasonal=None]
- Data note: this run uses the thesis dataset in `data/processed/thesis_main_dataset_en.csv`
