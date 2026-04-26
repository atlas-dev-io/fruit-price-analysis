# Thesis Results Summary

## Abstract-Ready Paragraph

Using Taiwan Taipei Second Market data for five fruit categories, the analysis shows that Pear has the highest comprehensive risk score (1.8342) and is therefore classified as a high-risk fruit, while Apple has the lowest comprehensive risk score (-0.8992) and is classified as low risk. Under a fixed weekly evaluation window, the forecasting module selected arima_0_1_1 for Apple, achieving the lowest observed RMSE among the selected models (3.9899). After replacing the heuristic procurement rule with a linear-program optimization model, the largest cost reduction appeared in Apple, with a saving of 2829.76 and a saving rate of 9.06%. The optimized procurement results indicate that high-risk fruits should follow short-cycle rolling purchases, while low-risk fruits can shift part of procurement to lower-price periods and use inventory smoothing to reduce total cost.

## 4.1 Risk Analysis

- Highest risk fruit: Pear (high)
- Lowest risk fruit: Apple (low)
- Highest risk explanation: high risk because composite score 1.8342 is driven most by return_volatility being well above the cross-fruit average.
- Interpretation: the cross-fruit risk ranking confirms that pears and grapes require more conservative procurement decisions, while apples and oranges provide more room for inventory-based smoothing.

## 4.2 Seasonality Analysis

- Strongest seasonality: Grape with strength 0.6870
- Weakest seasonality: Pear with strength 0.2217
- Interpretation: fruits with stronger monthly seasonality are better candidates for seasonal model comparison, while weaker series can remain in simpler weekly model families.

## 4.3 Forecast Model Results

- Best selected model by RMSE: Apple -> arima_0_1_1 [order=(0, 1, 1)]
- Evaluation frequency: weekly
- Interpretation: the final model set is not forced into one family; the code preserves interpretability by selecting among ETS, ARIMA and SARIMA according to out-of-sample error.

## 4.4 Procurement Optimization Results

- Largest cost saving versus heuristic baseline: Apple (2829.76, 9.06%)
- Strongest explicit safety-stock setting: Apple with average safety stock target 22.50 kg
- Interpretation: the optimization model now combines cost, risk, holding, and supply-stability considerations instead of only mapping risk levels to fixed procurement multipliers.

## 4.5 Strategy Comparison

- Grape (high): 线性规划结果：高风险品类以按需分批采购为主
- Pear (high): 线性规划结果：高风险品类以按需分批采购为主
- Apple (low): 线性规划结果：在低风险或低价期前置采购并保留库存
- Orange (low): 线性规划结果：在低风险或低价期前置采购并保留库存
- Banana (medium): 线性规划结果：适度前置采购以降低后续成本

## 4.6 Writing Notes

- `outputs/tables/risk_analysis_table.csv` can support the risk-analysis subsection.
- `outputs/tables/model_evaluation_table.csv` and `outputs/tables/stationarity_tests.csv` can support the forecasting-method subsection.
- `outputs/tables/optimization_cost_comparison.csv` and `outputs/tables/procurement_constraint_summary.csv` can support the procurement-optimization subsection.
- `outputs/figures/risk_comparison.png` and `outputs/figures/seasonality_patterns.png` can be inserted directly into the results chapter.
