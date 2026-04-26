# Thesis Results Summary

## Abstract-Ready Paragraph

Using Taiwan Taipei Second Market data for five fruit categories, the analysis shows that Pear has the highest comprehensive risk score (1.8342) and is therefore classified as a high-risk fruit, while Apple has the lowest comprehensive risk score (-0.8992) and is classified as low risk. Under a fixed weekly evaluation window, the forecasting module selected arima_0_1_1 for Apple, achieving the lowest observed RMSE among the selected models (3.9899). After replacing the heuristic procurement rule with a linear-program optimization model, the largest cost reduction appeared in Apple, with a saving of 2840.24 and a saving rate of 9.09%. The optimized procurement results indicate that high-risk fruits should follow short-cycle rolling purchases, while low-risk fruits can shift part of procurement to lower-price periods and use inventory smoothing to reduce total cost.

## Risk Findings

- Highest risk fruit: Pear (high)
- Lowest risk fruit: Apple (low)
- Highest risk explanation: high risk because composite score 1.8342 is driven most by return_volatility being well above the cross-fruit average.

## Forecast Findings

- Best selected model by RMSE: Apple -> arima_0_1_1 [order=(0, 1, 1)]
- Evaluation frequency: weekly

## Procurement Findings

- Grape (high): 线性规划结果：高风险品类以按需分批采购为主
- Pear (high): 线性规划结果：高风险品类以按需分批采购为主
- Apple (low): 线性规划结果：按周滚动采购并控制库存
- Orange (low): 线性规划结果：在低风险或低价期前置采购并保留库存
- Banana (medium): 线性规划结果：按周滚动采购并控制库存
