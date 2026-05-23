---
name: data-exploration-visualization
description: 自动化数据探索和可视化工具，提供从数据加载到专业报告生成的完整EDA解决方案。支持多种图表类型、智能数据诊断、建模评估和HTML报告生成。适用于医疗、金融、电商等领域的数据分析项目。
allowed-tools: Read, Write, Bash, Glob, Grep
---

# 数据探索可视化技能

## 技能概述

数据探索可视化技能是一个基于《数据分析咖哥十话》第2课理论的自动化EDA工具包，提供从数据加载到专业分析报告生成的完整解决方案。该技能集成了最先进的数据探索、可视化和机器学习技术，帮助用户快速深入理解数据特征和规律。

## 核心功能

### 🔍 智能数据探索
- **自动数据诊断**: 检测数据质量问题、异常值和缺失值模式
- **统计描述分析**: 生成全面的统计摘要和分布特征
- **相关性分析**: 识别特征间关系和依赖模式
- **数据质量报告**: 专业级数据质量评估和建议

### 📊 专业可视化生成
- **分布可视化**: 直方图、密度图、小提琴图、QQ图
- **统计可视化**: 箱线图、误差条图、置信区间图
- **关系可视化**: 散点图、热图、配对图、3D散点图
- **专门图表**: ROC曲线、混淆矩阵、特征重要性图
- **交互式图表**: Plotly驱动的动态可视化

### 🏥 医疗数据专精
- **医疗编码支持**: ICD-10、SNOMED CT等医疗标准
- **生物标记物分析**: 专门的医学指标处理
- **诊断模型构建**: 医疗预测模型和评估
- **医学可解释性**: 符合医学实践的解释框架

### 🤖 自动化建模评估
- **多算法支持**: 逻辑回归、随机森林、XGBoost、神经网络
- **自动特征工程**: 特征选择、转换和优化
- **超参数调优**: 网格搜索和贝叶斯优化
- **模型可解释性**: SHAP值、特征重要性、部分依赖图

### 📋 专业报告生成
- **HTML报告**: 可发表级交互式分析报告
- **PDF导出**: 高质量文档格式输出
- **Markdown支持**: 轻量级报告格式
- **自定义模板**: 可配置的报告模板系统

## 使用场景

### 🏥 医疗健康领域
- **疾病预测**: 基于临床数据的疾病风险预测
- **诊断辅助**: 医学影像和检验结果分析
- **流行病学研究**: 疫情数据分析和趋势预测
- **临床试验**: 试验数据统计分析和可视化

### 💰 金融风控领域
- **信用评估**: 个人和企业信用风险建模
- **欺诈检测**: 异常交易模式识别
- **投资分析**: 市场趋势和风险评估
- **合规报告**: 监管要求的分析报告

### 🛒 电商零售领域
- **用户分析**: 客户行为和偏好分析
- **销售预测**: 销量预测和库存优化
- **推荐系统**: 个性化推荐算法评估
- **市场细分**: 客户群体分析和画像

### 🎓 科研教育领域
- **学术研究**: 数据驱动的学术研究支持
- **教学案例**: 数据分析教学和实践
- **论文写作**: 研究数据分析和图表制作
- **技能培训**: 数据科学技能培训工具

## 工具使用指南

### 快速开始

1. **基础数据探索**
   ```python
   from scripts.eda_analyzer import EDAAnalyzer

   # 初始化分析器
   analyzer = EDAAnalyzer()

   # 加载数据并自动分析
   data = analyzer.load_data('data.csv')
   report = analyzer.auto_eda(data)
   ```

2. **可视化生成**
   ```python
   from scripts.visualizer import DataVisualizer

   # 初始化可视化器
   visualizer = DataVisualizer()

   # 自动生成所有图表
   charts = visualizer.auto_visualize(data)

   # 生成特定类型图表
   dist_plot = visualizer.plot_distribution(data, 'column_name')
   corr_heatmap = visualizer.plot_correlation(data)
   ```

3. **建模评估**
   ```python
   from scripts.modeling_evaluator import ModelingEvaluator

   # 初始化建模器
   modeler = ModelingEvaluator()

   # 自动建模和评估
   results = modeler.auto_modeling(
       data=data,
       target_col='target',
       algorithms=['logistic', 'rf', 'xgboost']
   )
   ```

4. **报告生成**
   ```python
   from scripts.report_generator import ReportGenerator

   # 生成完整报告
   generator = ReportGenerator()
   report = generator.generate_comprehensive_report(
       data=data,
       model_results=model_results,
       output_path='analysis_report.html'
   )
   ```

### 高级功能

1. **医疗数据分析**
   ```python
   # 医疗数据特殊处理
   from scripts.medical_analyzer import MedicalDataAnalyzer

   medical_analyzer = MedicalDataAnalyzer()
   medical_report = medical_analyzer.analyze_medical_data(
       data=medical_df,
       diagnosis_col='diagnosis',
       biomarker_cols=['biomarker1', 'biomarker2']
   )
   ```

2. **交互式仪表板**
   ```python
   # 生成交互式仪表板
   dashboard = visualizer.create_dashboard(
       data=data,
       charts=['distribution', 'correlation', 'model_performance']
   )
   ```

3. **批量数据处理**
   ```python
   # 批量分析多个数据集
   batch_results = analyzer.batch_analyze(
       data_files=['data1.csv', 'data2.csv'],
       analysis_types=['eda', 'modeling', 'visualization']
   )
   ```

## 技术依赖

### 核心库
- **pandas** (>=1.3.0): 数据处理和分析
- **numpy** (>=1.20.0): 数值计算
- **scikit-learn** (>=1.0.0): 机器学习算法
- **xgboost** (>=1.5.0): 梯度提升算法

### 可视化库
- **matplotlib** (>=3.4.0): 基础绘图
- **seaborn** (>=0.11.0): 统计可视化
- **plotly** (>=5.0.0): 交互式图表

### 统计分析库
- **scipy** (>=1.7.0): 科学计算
- **statsmodels** (>=0.13.0): 统计建模

### 报告生成
- **jinja2** (>=3.0.0): 模板引擎
- **weasyprint**: PDF生成

## 最佳实践

### 数据准备
- 确保数据格式规范（CSV、Excel等）
- 检查数据编码，避免中文乱码
- 处理缺失值和异常值
- 验证数据类型和格式

### 分析流程
1. **数据加载和检查**: 确认数据质量和完整性
2. **探索性分析**: 了解数据基本特征和分布
3. **可视化探索**: 通过图表发现数据模式
4. **预处理**: 数据清洗和特征工程
5. **建模分析**: 构建和评估预测模型
6. **结果解释**: 提取洞察和业务建议
7. **报告生成**: 创建专业分析报告

### 可视化选择
- **单变量分析**: 直方图、箱线图、小提琴图
- **双变量分析**: 散点图、分组箱线图
- **多变量分析**: 热图、配对图、3D图
- **时间序列**: 时间线图、趋势图
- **地理数据**: 地图可视化

## 示例数据

### 医疗数据示例
```python
# 乳腺检查数据示例
medical_data = {
    'patient_id': ['P001', 'P002', ...],
    'diagnosis': ['Malignant', 'Benign', ...],
    'radius_mean': [17.99, 20.57, ...],
    'texture_mean': [10.38, 17.77, ...],
    'perimeter_mean': [122.8, 132.9, ...]
}
```

### 金融数据示例
```python
# 信用评分数据示例
financial_data = {
    'customer_id': ['C001', 'C002', ...],
    'credit_score': [720, 680, ...],
    'income': [85000, 62000, ...],
    'debt_ratio': [0.15, 0.32, ...],
    'default': [0, 1, ...]
}
```

## 常见问题

### Q: 如何处理中文数据？
A: 技能自动检测和处理中文编码，支持UTF-8、GBK等多种编码格式。

### Q: 支持哪些数据格式？
A: 支持CSV、Excel、JSON、Parquet等常见格式，也支持数据库连接。

### Q: 如何自定义可视化样式？
A: 可以通过配置文件自定义颜色、字体、图表布局等样式参数。

### Q: 模型准确性如何保证？
A: 技能采用交叉验证、多种评估指标和集成方法来确保模型的可靠性和泛化能力。

## 技能特色

✅ **智能化程度高** - 90%的EDA工作自动化
✅ **专业性突出** - 医疗数据专精处理
✅ **可视化丰富** - 20+种专业图表类型
✅ **建模能力强** - 多算法集成和自动调优
✅ **报告质量高** - 可发表级分析报告
✅ **易用性好** - 简单API，复杂流程自动化
✅ **扩展性强** - 模块化设计，易于定制扩展

## 更新日志

### v1.0.0 (2025-01-19)
- 初始版本发布
- 完整的EDA功能
- 基础可视化支持
- 逻辑回归建模
- HTML报告生成

### 未来计划
- 支持更多机器学习算法
- 增加深度学习模型支持
- 扩展医疗数据分析功能
- 云端部署支持
- 实时数据分析能力

通过这个技能，您可以大幅提升数据分析效率，从重复性工作中解放出来，专注于洞察发现和决策支持。