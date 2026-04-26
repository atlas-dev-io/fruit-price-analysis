# Fruit Price Analysis

## 项目简介

本项目是一个面向水果采购场景的数据分析与决策支持项目，核心目标是把市场价格数据转成可执行的分析结果和采购建议。

当前主线可以概括为：

`数据标准化 -> 风险与季节性分析 -> 周度价格预测 -> 采购优化`

## 这个项目解决什么问题

项目关注的问题包括：

1. 哪些水果价格更稳定，哪些波动更大。
2. 未来几个采购周期内价格大概率怎么变化。
3. 在满足需求的前提下，如何降低采购成本并控制价格风险。
4. 不同水果品类应该采用什么样的采购策略。

## 当前范围

当前实现范围如下：

- 市场：台北二市场
- 品类：`Apple`、`Banana`、`Orange`、`Grape`、`Pear`
- 数据频率：原始日度数据，建模阶段聚合到周度
- 输出：分析表、图、模型比较结果、采购优化结果

## 技术栈

- `Python 3.11+`
- `pandas`
- `numpy`
- `matplotlib`
- `statsmodels`
- `scipy`
- `unittest`
- `conda`

## 项目结构

```text
fruit-price-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── tables/
├── scripts/
├── src/
├── tests/
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```

## 运行方式

1. 安装依赖

```bash
conda run -n fruit pip install -r requirements.txt
```

2. 重建标准化数据集

```bash
conda run -n fruit python scripts/build_market_dataset.py
```

3. 运行主流程

```bash
conda run -n fruit python main.py
```

4. 或者使用统一命令

```bash
make build-data
make run
make test
```

## 主要产物

运行后会生成以下几类结果：

- 标准化与清洗后的数据
- 风险分析表和风险分级
- 季节性分析表和季节性图
- 预测模型比较结果
- 周度预测结果
- 采购优化结果
- 对比性报告和说明文档

完整说明见：

- [Outputs Guide](docs/outputs.md)

## 数据来源与获取

项目当前使用的原始数据和获取方式说明见：

- [Data Sources](docs/data_sources.md)

## 设计与开发文档

- [Architecture](docs/architecture.md)
- [Development Guide](docs/development.md)

## 当前状态

当前代码已经支持：

- 原始数据读取与标准化
- 清洗、聚合与统计分析
- 季节性分析与风险分级
- 周度模型比较与预测结果导出
- 带约束的采购优化
- 图表、表格和说明报告导出

## 测试

```bash
conda run -n fruit python -m unittest discover -s tests
```

## License

本项目使用 [MIT License](LICENSE)。
