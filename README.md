# Fruit Price Analysis

## 项目简介

本项目围绕“水果价格波动特征分析与采购方案设计”展开，目标是基于历史水果价格数据，完成以下三类工作：

1. 对水果价格进行数据清洗、统计分析和波动特征识别。
2. 构建价格预测模型，预测未来若干周期的价格走势。
3. 将预测结果用于采购决策优化，输出分品类、分周期的采购建议。

根据 `Document/水果初稿.docx` 当前内容，项目研究主线已经明确，可以概括为：

`数据处理 -> 特征分析 -> 价格预测 -> 采购优化`

## 这个项目是做什么的

这个项目本质上是一个面向水果采购管理的“数据分析与决策支持”项目，不只是做价格可视化，而是要把价格分析结果真正转成采购建议。

面向的核心问题包括：

- 哪些水果价格更稳定，哪些波动更大。
- 未来几个采购周期内价格大概率怎么变化。
- 在满足需求的前提下，如何降低采购成本并控制价格风险。
- 不同水果品类应该采取什么样的差异化采购策略。

## 当前文档中已确认的研究范围

从现有论文初稿可以确认的内容：

- 研究对象：台北二批发市场的 5 个水果品类历史价格数据。
- 分析维度：整体波动、季节性变化、异常波动、风险水平。
- 风险指标：变异系数、最大回撤等。
- 预测方法：时间序列分析，明确提到 `ARIMA`，并提到与指数平滑模型的组合预测思路。
- 决策目标：在采购成本、价格风险、供给稳定性之间权衡。
- 输出结果：按周输出价格预测和采购建议，高波动水果采用分批采购、缩短采购周期；稳定型水果采用提前采购或集中采购。

## 用什么做

当前仓库已经包含可运行源码、数据准备脚本和结果导出逻辑，当前实现使用如下技术栈：

- 语言：`Python 3.11+`
- 数据处理：`pandas`、`numpy`
- 可视化：`matplotlib`、`seaborn`
- 时间序列建模：`statsmodels`
- 优化求解：`scipy` 或 `pulp`
- 交互分析：`Jupyter Notebook`
- 工程化管理：`venv` 或 `conda`，配合 `requirements.txt`

如果后续要做成可演示系统，可以增加：

- Web 展示：`Streamlit`
- 数据接口：`FastAPI`

## 实现步骤

建议按下面顺序推进实现：

1. 数据准备
   - 收集水果历史价格数据。
   - 统一字段、时间粒度、单位和品类命名。
   - 处理缺失值、重复值和异常值。

2. 特征分析
   - 计算均值、标准差、波动率等基础统计指标。
   - 计算变异系数、最大回撤等风险指标。
   - 分析季节性、趋势性和异常波动。

3. 价格预测
   - 针对各水果品类建立时间序列模型。
   - 先做平稳性检验、差分和参数选择。
   - 使用 `ARIMA`、指数平滑等模型进行训练和预测。
   - 用误差指标评估模型效果。

4. 采购优化
   - 以预测价格作为输入。
   - 建立以“成本最小化 + 风险控制”为核心的采购决策模型。
   - 加入需求、库存、非负、单周期采购上限等约束。
   - 输出不同水果的分周期采购建议。

5. 结果展示
   - 输出价格趋势图、风险对比图、预测结果图。
   - 输出采购方案表和优化前后对比结果。
   - 汇总形成论文图表或系统展示页面。

## 当前目录结构

当前仓库已经落地为下面的工程结构：

```text
fruit-price-analysis/
├── Document/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── forecast/
│   ├── optimization/
│   └── visualization/
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── tables/
├── README.md
├── DEVELOPMENT.md
└── ARCHITECTURE.md
```

## 当前状态

当前仓库处于“论文主数据已接入、主流程可运行”的阶段：

- 已有内容：开题报告、论文初稿、可运行分析代码、数据准备脚本、论文友好型结果输出、最小测试集。
- 当前主数据：`data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv`
- 当前标准化数据：`data/processed/thesis_main_dataset_en.csv`
- 当前研究对象：台北二市场的 5 个水果品类 `Apple`、`Banana`、`Orange`、`Grape`、`Pear`
- 当前输出口径：周度预测与周度采购建议
- 当前采购模块：已升级为线性规划优化模型
- 仍缺少内容：更深入的论文论证和可选的展示层开发

因此，这个仓库现在更准确的状态是“论文研究已经工程化为可运行、可测试、可导出论文结果的分析流水线”。

## 统一运行方式

1. 安装依赖

```bash
conda run -n fruit pip install -r requirements.txt
```

2. 如果需要先重建论文主数据

```bash
conda run -n fruit python scripts/build_taiwan_thesis_dataset.py
```

3. 运行主流程

```bash
conda run -n fruit python main.py
```

4. 或者直接使用统一命令

```bash
make build-data
make run
make test
```

## 运行后会生成

- `data/processed/fruit_prices_cleaned.csv`
- `outputs/tables/descriptive_stats.csv`
- `outputs/tables/risk_metrics.csv`
- `outputs/tables/risk_analysis_table.csv`
- `outputs/tables/forecast_prices.csv`
- `outputs/tables/forecast_model_metrics.csv`
- `outputs/tables/forecast_model_selection.csv`
- `outputs/tables/model_evaluation_table.csv`
- `outputs/tables/forecast_results_table.csv`
- `outputs/tables/procurement_plan.csv`
- `outputs/tables/optimization_results_table.csv`
- `outputs/tables/optimization_cost_comparison.csv`
- `outputs/tables/procurement_strategy_comparison.csv`
- `outputs/figures/price_trends.png`
- `outputs/figures/risk_comparison.png`
- `outputs/reports/summary.md`
- `outputs/reports/thesis_main_dataset_summary.md`
- `outputs/reports/thesis_results.md`

输出文件的用途说明见 [OUTPUTS.md](/home/ethan/Project/fruit-price-analysis/OUTPUTS.md:1)。

## 当前实现做了什么

当前代码已经能跑通基于论文主数据的完整闭环：

- 读取 `data/processed/thesis_main_dataset_en.csv`
- 对台北二市场的 5 个水果品类做统一清洗与聚合
- 计算描述性统计、综合风险分数和风险分级
- 比较 `ExponentialSmoothing`、多组 `ARIMA` 和候选 `SARIMA` 的预测效果
- 生成未来 4 个周度周期的价格预测
- 用线性规划模型生成采购方案
- 导出论文可直接引用的图、表和结论摘要

说明：

- 当前预测模块已经具备周度评估窗口、参数搜索和模型选择结果。
- 当前采购模块已经切换到带需求、库存和采购上限约束的线性规划版本。
- 当前输出层已经补充季节性分析、模型论证、成本对比和结果章节草稿。

## 测试

当前仓库已包含 `tests/` 目录下的最小测试，覆盖：

- 风险分级输出关键字段
- 预测模块的非空输出与周度模型选择
- 采购优化模块的约束结果与基线方案生成

运行命令：

```bash
conda run -n fruit python -m unittest discover -s tests
```

## 当前数据口径

当前论文与工程统一采用以下数据口径：

- 原始抓取数据：`data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv`
- 标准化主数据：`data/processed/thesis_main_dataset_en.csv`
- 市场范围：台北二市场
- 水果范围：苹果、香蕉、柳橙、葡萄、梨
- 输出频率：周度预测、周度采购建议

`data/raw/archive.zip` 是项目早期用于快速搭建流程的 Kaggle 试验数据，现在保留为历史参考，不再作为当前主数据源。

## 真实数据去哪里找

我已经把数据源判断单独整理到：

- [DATA_SOURCES.md](/home/ethan/Project/fruit-price-analysis/DATA_SOURCES.md)

结论是：

- 论文文档只写了“农产品市场公开价格数据平台”，没有给出具体链接。
- 最匹配的官方数据源是农业农村部“全国农产品批发市场价格信息系统”。
- 如果原始系统抓取不方便，可以先整理农业农村部周度行情监测报告中的水果数据。

## 如何更新当前主数据

如果后续要刷新论文主数据，应继续保持与当前主流程一致的字段结构：

```text
date,fruit_name,market,price,unit
```

当前建议：

- `date` 使用 `YYYY-MM-DD`
- `price` 统一为数值价格
- `unit` 统一为 `kg`
- 保持同一市场口径，即台北二市场
- 保持当前 5 个水果品类的映射规则一致

当前流程对应的数据更新步骤是：

1. 用抓取脚本更新 `data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv`
2. 运行数据构建脚本生成 `data/processed/thesis_main_dataset_en.csv`
3. 重新运行 `conda run -n fruit python main.py`

## License

本项目使用 [MIT License](/home/ethan/Project/fruit-price-analysis/LICENSE:1)。

## 下一步建议

如果继续往论文最终稿推进，最值得优先做的是：

1. 把成本、风险和库存约束的业务口径进一步细化。
2. 增加对模型误差和采购收益的论文解释。
3. 在论文正文中直接引用 `outputs/reports/thesis_results.md` 和新增图表。
