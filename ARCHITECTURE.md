# Architecture

## 架构定位

本项目适合采用“离线分析 + 模型预测 + 决策优化”的轻量分层架构，而不是先做复杂的在线业务系统。

原因很直接：

- 当前材料是论文型研究，不是现成业务平台。
- 核心价值在数据分析、预测模型和采购优化逻辑。
- 现阶段更需要保证结果可复现、结构清晰，而不是先做重前后端系统。
- 当前主数据已经固定为台北二市场 5 个水果品类的历史交易数据。

## 总体架构

```text
台北二市场原始交易数据
    ->
论文主数据集构建
    ->
数据清洗与标准化
    ->
波动特征分析与风险指标计算
    ->
周度价格预测模型
    ->
周度采购建议/采购优化模型
    ->
图表、报表、采购建议输出
```

## 当前实现口径

当前代码、文档和输出统一采用如下口径：

- 原始数据：`data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv`
- 标准化主数据：`data/processed/thesis_main_dataset_en.csv`
- 市场范围：台北二市场
- 水果范围：`Apple`、`Banana`、`Orange`、`Grape`、`Pear`
- 输出频率：周度预测与周度采购建议

`data/raw/archive.zip` 仅用于项目早期的 Kaggle 流程验证，当前保留为历史参考数据，不再作为主流程输入。

## 分层设计

### 1. 数据层

职责：

- 读取原始水果价格数据
- 统一字段格式、时间格式、计量单位
- 处理缺失值、重复值、异常值
- 输出标准化数据集

输入：

- 台北二市场水果历史交易数据
- 当前主流程使用已标准化的论文主数据集

输出：

- 标准化后的论文主数据表

建议模块：

- `src/data/loaders.py`
- `src/data/cleaning.py`
- `scripts/build_taiwan_thesis_dataset.py`

### 2. 分析层

职责：

- 计算描述性统计指标
- 识别趋势、季节性、异常波动
- 计算风险指标，如变异系数、最大回撤
- 输出分水果品类的波动特征结论

输入：

- 清洗后的标准化价格数据

输出：

- 波动特征表
- 风险评估表
- 可视化图表

建议模块：

- `src/features/descriptive_stats.py`
- `src/features/volatility.py`
- `src/features/seasonality.py`

### 3. 预测层

职责：

- 对单个水果品类建立时间序列预测模型
- 输出未来若干周期的价格预测结果
- 评估不同模型的误差表现

当前文档中明确提到的模型：

- 指数平滑
- `ARIMA`

可扩展模型：

- `SARIMA`
- `Prophet`
- `LSTM`

输入：

- 单品类历史价格时间序列

输出：

- 未来 4 周的价格预测序列
- 模型评估指标与模型选择结果

当前模块：

- `src/forecast/formal.py`
- `src/forecast/baseline.py`

### 4. 决策层

职责：

- 将预测价格与风险指标转化为采购决策输入
- 当前先输出规则化周度采购建议
- 后续升级为带约束的正式采购优化模型

核心目标：

- 降低采购成本
- 控制价格波动风险
- 保证供给稳定

目标状态下的典型约束：

- 需求满足约束
- 库存上下限约束
- 采购量非负约束
- 高风险水果采购上限约束

当前模块：

- `src/optimization/model.py`

### 5. 输出层

职责：

- 输出研究图表
- 输出预测结果表
- 输出采购建议表
- 生成论文可引用的结果摘要

建议模块：

- `src/visualization/charts.py`
- `src/visualization/export.py`

## 数据流

项目的数据流应保持单向，避免中间结果被手工改坏：

```text
data/raw
    ->
data/processed
    ->
features outputs
    ->
forecast outputs
    ->
optimization outputs
    ->
reports and figures
```

当前主流程对应的实际文件流为：

```text
data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv
    ->
data/processed/thesis_main_dataset_en.csv
    ->
data/processed/fruit_prices_cleaned.csv
    ->
outputs/tables/*.csv
    ->
outputs/reports/*.md + outputs/figures/*.png
```

## 推荐运行流程

建议的执行链如下：

1. `clean_data`
2. `analyze_volatility`
3. `train_forecast_model`
4. `generate_forecast`
5. `optimize_procurement`
6. `export_reports`

当前入口由 `main.py` 调用 `src/pipeline.py`，主流程已经可以完整执行。

## 当前仓库与目标架构的差距

当前仓库已经完成基础落地，但与论文最终目标仍有差距：

- 风险分级仍较粗，差异化策略不够强
- 采购层还是规则化建议，不是正式优化求解
- 预测层仍可继续强化参数搜索和季节性建模
- 尚未补齐测试

所以这份文档同时描述“当前已落地架构”和“后续目标架构”。

## 后续演进建议

### 阶段一：最小可运行版本

- 建立基础目录结构
- 接入论文主数据
- 完成 5 个水果品类的数据清洗
- 完成周度预测与采购建议输出

### 阶段二：多品类分析版本

- 支持苹果、香蕉、橙子、葡萄、梨等多品类
- 输出品类对比分析和风险分类
- 输出分品类采购策略

### 阶段三：系统化展示版本

- 增加统一运行入口
- 增加仪表盘或 Web 界面
- 支持参数配置、批量运行和结果导出
