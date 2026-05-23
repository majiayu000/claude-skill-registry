---
name: growth-model-analyzer
description: 增长模型分析技能 - 提供全面的增长黑客分析工具，包括裂变策略评估、用户细分、Uplift建模、ROI优化等。支持多种增长场景的机器学习建模和智能决策建议。适用于用户增长、营销优化、产品迭代等增长分析场景。
allowed-tools: Read, Write, Bash, Glob, Grep
---

# 增长模型分析技能

## 技能概述

增长模型分析技能是一个全面的增长黑客工具包，基于《数据分析咖哥十话》第10话的增长模型理论，提供从基础效果评估到高级机器学习建模的完整增长分析解决方案。

该技能专注于通过数据驱动的方法，帮助企业理解和优化用户增长策略，实现可持续的商业增长。

## 核心功能

### 🎯 裂变策略效果评估
- **转化率分析**: 计算和比较不同裂变策略的转化效果
- **统计显著性检验**: 使用卡方检验等方法验证策略效果
- **效果可视化**: 生成直观的策略对比图表和报告

### 👥 用户细分与个性化策略
- **RFM用户分群**: 基于近度、频度、金额的用户价值分析
- **行为画像分析**: 深度分析用户行为模式和偏好
- **个性化推荐**: 为不同用户群体推荐最优增长策略

### 🤖 智能Uplift建模
- **XGBoost增长建模**: 使用机器学习识别高增量价值用户
- **增量分数计算**: 精确计算用户对营销策略的响应概率
- **Qini曲线分析**: 评估增长模型的预测效果和商业价值

### 💰 成本效益分析与ROI优化
- **ROI计算**: 全面的投资回报率分析
- **预算分配优化**: 智能化的营销预算分配建议
- **LTV预测**: 用户生命周期价值预测和优化

### 📈 增长策略优化
- **协同效应分析**: 识别策略间的协同和冲突效应
- **疲劳效应监测**: 监控和预防用户对策略的疲劳
- **自动化建议**: 基于数据驱动提供策略优化建议

## 工具使用指南

### 基础使用流程

1. **数据准备**
   ```python
   # 加载增长数据
   analyzer = GrowthModelAnalyzer()
   data = analyzer.load_data('growth_data.csv')
   ```

2. **策略效果评估**
   ```python
   # 评估裂变策略效果
   results = analyzer.analyze_campaign_effectiveness(
       data,
       campaign_col='裂变类型',
       conversion_col='是否转化'
   )
   ```

3. **用户细分分析**
   ```python
   # RFM用户分群
   segments = analyzer.rfm_segmentation(
       data,
       user_col='用户码',
       recency_col='R值',
       frequency_col='曾助力',
       monetary_col='M值'
   )
   ```

4. **Uplift建模**
   ```python
   # 构建增长模型
   uplift_model = UpliftModeler()
   model_results = uplift_model.build_model(
       data,
       treatment_col='裂变类型',
       outcome_col='是否转化'
   )
   ```

### 高级分析功能

1. **Qini曲线分析**
   ```python
   # 评估模型效果
   qini_results = uplift_model.analyze_qini_curve(
       test_data,
       model_predictions
   )
   ```

2. **ROI优化**
   ```python
   # 营销ROI分析
   roi_analyzer = ROIAnalyzer()
   optimization_results = roi_analyzer.optimize_budget_allocation(
       campaign_data,
       budget_constraints
   )
   ```

## 最佳实践

### 数据要求
- 用户标识符 (用户码)
- 营销策略标识 (裂变类型)
- 转化结果 (是否转化)
- 用户行为数据 (R值、F值、M值)
- 人口统计学信息 (城市类型、设备类型)

### 模型选择指导
- **新用户获取**: 优先使用Uplift建模识别高潜力用户
- **用户激活**: 使用RFM分析定位低活跃度用户
- **用户留存**: 采用行为分析预测流失风险
- **营收增长**: 应用ROI分析优化预算分配

### 策略优化建议
- 定期更新模型以适应用户行为变化
- 结合定性分析完善数据洞察
- 建立A/B测试框架验证策略效果
- 关注长期用户价值而非短期转化

## 技术依赖

### 核心依赖
- **pandas**: 数据处理和分析
- **numpy**: 数值计算
- **scikit-learn**: 机器学习工具
- **xgboost**: 梯度提升框架

### 可视化依赖
- **matplotlib**: 基础图表绘制
- **seaborn**: 统计图表美化
- **plotly**: 交互式可视化

### 统计分析依赖
- **scipy**: 科学计算和统计分析
- **statsmodels**: 高级统计建模

## 使用场景示例

### 场景1: 裂变策略优化
当您需要评估不同裂变策略（如助力砍价、拼团狂买）的效果时，使用策略效果评估功能快速识别最优策略。

### 场景2: 用户价值挖掘
通过RFM分析和用户画像，深入了解高价值用户的特征，指导精准营销。

### 场景3: 增长预算分配
使用ROI优化功能，科学分配营销预算，最大化投资回报率。

### 场景4: 用户增长预测
利用Uplift建模预测用户对不同增长策略的响应，制定个性化增长方案。

## 示例命令

```bash
# 运行完整增长分析示例
python examples/growth_analysis_example.py

# 快速测试核心功能
python quick_test.py

# 运行Uplift建模示例
python examples/uplift_modeling_example.py

# 生成Qini曲线分析
python examples/qini_curve_example.py
```

## 技能特色

✅ **业界领先的增长建模方法** - 集成最新的增长黑客理论和实践
✅ **完整的工具链** - 从数据清洗到策略部署的全流程支持
✅ **机器学习驱动** - 智能化的用户洞察和策略优化
✅ **商业价值导向** - 专注于ROI和业务增长的实用工具
✅ **易于使用** - 简洁的API设计和丰富的使用示例
✅ **可扩展架构** - 支持自定义模型和策略扩展

## 注意事项

- 确保数据质量和完整性，避免垃圾进垃圾出
- 定期验证模型效果，防止模型漂移
- 结合业务理解解释分析结果
- 关注用户隐私和数据安全合规要求

通过这个技能，您可以构建科学、高效、可衡量的用户增长体系，实现可持续的商业增长。