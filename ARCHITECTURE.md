# Architecture

## 架构定位

本项目适合采用“离线分析 + 模型预测 + 决策优化”的轻量分层架构，而不是先做复杂的在线业务系统。

原因很直接：

- 当前材料是论文型研究，不是现成业务平台。
- 核心价值在数据分析、预测模型和采购优化逻辑。
- 现阶段更需要保证结果可复现、结构清晰，而不是先做重前后端系统。

## 总体架构

```text
原始价格数据
    ->
数据清洗与标准化
    ->
波动特征分析与风险指标计算
    ->
价格预测模型
    ->
采购优化模型
    ->
图表、报表、采购建议输出
```

## 分层设计

### 1. 数据层

职责：

- 读取原始水果价格数据
- 统一字段格式、时间格式、计量单位
- 处理缺失值、重复值、异常值
- 输出标准化数据集

输入：

- 批发市场历史价格数据
- 可选的辅助数据，如市场、品类、时间维度

输出：

- 标准化后的时间序列数据表

建议模块：

- `src/data/loaders.py`
- `src/data/cleaning.py`
- `src/data/validation.py`

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

- 预测价格序列
- 模型评估指标

建议模块：

- `src/forecast/baseline.py`
- `src/forecast/arima.py`
- `src/forecast/evaluate.py`

### 4. 决策层

职责：

- 将预测价格与风险指标转化为采购决策输入
- 在需求、库存、风险约束下计算采购方案
- 输出各水果在各周期的建议采购量

核心目标：

- 降低采购成本
- 控制价格波动风险
- 保证供给稳定

典型约束：

- 需求满足约束
- 库存上下限约束
- 采购量非负约束
- 高风险水果采购上限约束

建议模块：

- `src/optimization/model.py`
- `src/optimization/constraints.py`
- `src/optimization/solve.py`

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

## 推荐运行流程

建议的执行链如下：

1. `clean_data`
2. `analyze_volatility`
3. `train_forecast_model`
4. `generate_forecast`
5. `optimize_procurement`
6. `export_reports`

## 当前仓库与目标架构的差距

当前仓库只有研究文档，尚未落地：

- 数据目录
- 源码目录
- 依赖清单
- 运行入口
- 测试

所以现在的架构文档描述的是“推荐目标架构”，不是现状代码架构。

## 后续演进建议

### 阶段一：最小可运行版本

- 建立基础目录结构
- 完成单品类数据清洗
- 完成 `ARIMA` 预测
- 输出单品类采购建议

### 阶段二：多品类分析版本

- 支持苹果、香蕉、橙子、葡萄、梨等多品类
- 输出品类对比分析和风险分类
- 输出分品类采购策略

### 阶段三：系统化展示版本

- 增加统一运行入口
- 增加仪表盘或 Web 界面
- 支持参数配置、批量运行和结果导出

