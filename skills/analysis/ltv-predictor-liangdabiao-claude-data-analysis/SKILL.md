---
name: ltv-predictor
description: 基于RFM模型和回归算法的客户生命周期价值(LTV)预测分析工具，支持电商和零售业务的客户价值预测。使用时需要客户交易数据、订单历史或消费记录，自动进行RFM特征工程、回归建模和价值预测。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch
---

# 客户生命周期价值预测技能

一个基于《数据分析咖哥十话》第3课理论的自动化LTV预测分析工具，提供从RFM特征工程到回归建模的完整解决方案。

## ✨ 核心功能

### 🔍 RFM特征工程
- **R值计算**: 最近一次消费时间间隔分析
- **F值计算**: 消费频率统计与分析
- **M值计算**: 消费金额汇总与分层
- **时间窗口**: 基于短期数据预测长期价值
- **客户分群**: 自动化客户价值分层

### 🤖 回归算法建模
- **线性回归**: 基础回归分析模型
- **随机森林**: 高性能集成学习算法
- **模型对比**: 多算法性能评估比较
- **交叉验证**: 可靠的模型性能评估
- **超参数优化**: 自动化模型调参

### 📊 LTV预测引擎
- **时间序列预测**: 基于历史数据预测未来LTV
- **批量预测**: 支持大规模客户批量处理
- **置信区间**: 提供预测结果的不确定性评估
- **特征重要性**: 解释影响LTV的关键因素

### 📈 可视化分析
- **RFM分布图**: 客户价值分布可视化
- **预测效果对比**: 实际值vs预测值散点图
- **特征重要性**: 关键特征贡献度分析
- **模型性能对比**: 多算法效果对比图

### 📋 专业报告
- **HTML报告**: 交互式分析报告
- **Markdown文档**: 轻量级分析总结
- **Excel导出**: 便于业务部门使用
- **API接口**: 支持系统集成调用

## 🚀 快速开始

### 1. 环境安装

```bash
# 安装基础依赖
pip install pandas numpy scikit-learn matplotlib seaborn

# 安装可选依赖（用于高级功能）
pip install xgboost lightgbm joblib openpyxl
```

### 2. 基础使用

```python
from scripts.ltv_predictor import LTVPredictor
from scripts.data_processor import DataProcessor

# 1. 初始化处理器
processor = DataProcessor()
predictor = LTVPredictor()

# 2. 加载和预处理数据
data = processor.load_order_data('your_orders.csv')
rfm_data = processor.calculate_rfm_features(data,
                                          feature_period='3M',
                                          prediction_period='12M')

# 3. 训练LTV预测模型
model_results = predictor.train_models(rfm_data)

# 4. 进行LTV预测
predictions = predictor.predict_ltv(new_customer_data)

# 5. 生成分析报告
report_path = predictor.generate_report(predictions, 'ltv_analysis_report.html')
```

### 3. 快速示例

```python
from scripts.quick_analysis import quick_ltv_analysis

# 一键完成完整LTV分析流程
results = quick_ltv_analysis(
    order_data_path='ecommerce_orders.csv',
    feature_period_months=3,
    prediction_period_months=12,
    output_dir='ltv_analysis_results'
)

print(f"最佳模型R²分数: {results['best_model_r2']:.4f}")
print(f"预测客户数: {len(results['predictions'])}")
print(f"分析报告: {results['report_path']}")
```

## 📁 技能结构

```
ltv-predictor/
├── scripts/                   # 核心功能模块
│   ├── data_processor.py     # 数据预处理和RFM计算
│   ├── ltv_predictor.py      # LTV预测核心引擎
│   ├── regression_models.py  # 回归算法实现
│   ├── visualizer.py         # 可视化生成器
│   └── report_generator.py   # 报告生成器
├── examples/                 # 示例脚本
│   ├── ecommerce_ltv_analysis.py   # 电商完整分析示例
│   ├── quick_ltv_prediction.py     # 快速预测示例
│   └── model_comparison.py         # 模型对比示例
├── data/                     # 示例数据
│   └── sample_orders.csv     # 示例订单数据
├── tests/                    # 测试脚本
│   ├── test_rfm_analysis.py  # RFM分析测试
│   └── test_prediction.py    # 预测功能测试
├── SKILL.md                  # 技能说明文档
└── README.md                 # 使用说明
```

## 🎯 应用场景

### 🛒 电商零售
- **客户价值分层**: 基于LTV对客户进行金/银/铜牌分层
- **营销预算分配**: 根据LTV预测结果优化营销投入
- **库存预测**: 基于客户价值预测进行商品库存规划
- **个性化推荐**: 为高价值客户提供精准推荐

### 💰 金融服务
- **信贷评估**: 结合LTV进行客户信用评级
- **产品设计**: 为不同价值客户设计差异化产品
- **客户维护**: 识别高价值客户进行重点维护
- **风险控制**: 基于客户价值进行风险评估

### 🎯 营销策略
- **获客成本分析**: 计算不同渠道的LTV/CAC比率
- **客户生命周期管理**: 制定全生命周期营销策略
- **复购率提升**: 识别低频客户制定提升策略
- **客户挽回**: 预测流失风险制定挽回方案

## ⚙️ 配置选项

### RFM分析配置
```python
config = {
    'feature_period_months': 3,      # 特征计算时间窗口（月）
    'prediction_period_months': 12,  # 预测时间窗口（月）
    'r_weight': 0.2,                 # R值权重
    'f_weight': 0.3,                 # F值权重
    'm_weight': 0.5,                 # M值权重
    'customer_segments': 5           # 客户分层数量
}
```

### 模型训练配置
```python
config = {
    'test_size': 0.2,               # 测试集比例
    'cv_folds': 5,                  # 交叉验证折数
    'random_state': 42,             # 随机种子
    'enable_hyperparameter_tuning': True,  # 是否调参
    'n_iter_search': 50,            # 超参数搜索次数
    'scoring_metric': 'r2'          # 评估指标
}
```

### 预测配置
```python
config = {
    'confidence_interval': 0.95,    # 置信区间
    'batch_size': 1000,             # 批处理大小
    'feature_importance_threshold': 0.01,  # 特征重要性阈值
    'prediction_uncertainty': True   # 是否计算预测不确定性
}
```

## 📊 数据格式要求

### 订单数据格式
```csv
订单号,产品码,消费日期,产品说明,数量,单价,用户码,城市
536374,21258,2022-06-01 09:09,绿联usb分线器,32,10.95,15100,北京
536376,22114,2022-06-01 09:32,加大男装T恤,48,50.45,15291,上海
```

**必需字段**:
- `用户码`: 客户唯一标识
- `消费日期`: 购买时间（支持多种日期格式）
- `数量`: 购买数量
- `单价`: 商品单价

**可选字段**:
- `订单号`: 订单唯一标识
- `产品码`: 商品标识
- `产品说明`: 商品描述
- `城市`: 客户城市信息

## 🧪 模型性能基准

基于第3课实测数据:
- **数据规模**: 37,060条订单记录，370个独立客户
- **时间窗口**: 3个月数据预测12个月LTV
- **线性回归**: R² = 0.4778 (测试集)
- **随机森林**: R² = 0.5899 (测试集)
- **性能提升**: 23.4% (相对线性回归)
- **特征重要性**: M值(金额)贡献78.53%，F值(频率)贡献16.32%

## 🔧 高级功能

### 自动特征工程
- 时间序列特征生成
- 滑动窗口计算
- 季节性模式识别
- 异常值检测和处理

### 模型可解释性
- SHAP值分析
- 部分依赖图
- 特征交互作用
- 预测路径追踪

### 业务洞察
- 客户价值趋势分析
- 产品关联度分析
- 地域价值分布
- 时间价值模式

## 📋 最佳实践

### 数据质量
- 确保订单数据时间连续性
- 处理缺失值和异常值
- 验证客户标识唯一性
- 检查数据时间覆盖度

### 模型选择
- 小数据集优先使用线性回归
- 大数据集推荐随机森林或XGBoost
- 注重模型可解释性时选择线性模型
- 追求预测精度时使用集成学习

### 业务应用
- 定期重新训练模型（建议每月）
- 结合业务规则调整预测结果
- 建立模型监控和预警机制
- 持续跟踪预测准确性

## 🔄 更新日志

### v1.0.0 (2025-01-19)
- 初始版本发布
- 完整的RFM分析功能
- 线性回归和随机森林算法
- 基础可视化和报告功能
- 电商订单数据支持

### 未来计划
- 支持更多回归算法（XGBoost、LightGBM）
- 增加深度学习模型
- 实时预测API
- 更多行业数据模板
- 自动化模型部署

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议：

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

- 《数据分析咖哥十话》提供的理论基础
- Scikit-learn提供的机器学习算法
- Pandas和NumPy提供的数据处理能力
- 数据科学社区的支持和反馈

---

通过这个技能，您可以：
✅ 快速进行客户RFM分析
✅ 构建准确的LTV预测模型
✅ 获得可解释的业务洞察
✅ 生成专业的分析报告
✅ 支持数据驱动的业务决策