---
name: recommender-system
description: 智能推荐系统分析工具，提供多种推荐算法实现、评估框架和可视化分析。使用时需要用户行为数据、商品信息或评分数据，支持协同过滤、矩阵分解等推荐算法，生成个性化推荐结果和评估报告。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# 推荐系统分析技能 (Recommender System Skill)

推荐系统分析技能是一个综合性的智能推荐分析工具，基于"数据分析咖哥十话"的推荐系统模块开发，提供多种推荐算法实现、评估框架和可视化分析功能。

## 🎯 技能概述

本技能专注于构建、评估和可视化智能推荐系统，涵盖从基础协同过滤到高级矩阵分解的完整推荐技术栈。无论是电商产品推荐、游戏推荐还是内容推荐，都能提供专业的分析支持。

## ✨ 核心特性

### 🔧 推荐算法引擎
- **协同过滤算法**：基于用户的协同过滤 (UBCF) 和基于物品的协同过滤 (IBCF)
- **矩阵分解技术**：SVD奇异值分解，挖掘用户和商品的隐含特征
- **混合推荐策略**：结合多种算法，提高推荐准确性和覆盖率
- **相似度计算**：余弦相似度、皮尔逊相关系数等多种相似度度量

### 📊 智能评估框架
- **离线评估指标**：Precision@K、Recall@K、MAE、RMSE等标准评估指标
- **评估方法**：留一法交叉验证、K折交叉验证、时间序列验证
- **多维度评估**：准确性、多样性、新颖性、惊喜度等综合评估
- **算法比较**：多种推荐算法的性能对比和分析

### 📈 可视化分析
- **推荐结果展示**：个性化推荐列表可视化，推荐解释展示
- **性能评估图表**：算法性能对比图、评估指标趋势图
- **数据洞察分析**：用户行为模式图、商品分布图、评分热力图
- **交互式图表**：支持动态筛选和交互分析

## 🚀 主要功能模块

### 1. 推荐算法实现 (`scripts/recommendation_engine.py`)
```python
# 主要类和方法
class RecommendationEngine:
    def user_based_cf(self, user_id, top_k=5)       # 基于用户的协同过滤
    def item_based_cf(self, user_id, top_k=5)       # 基于物品的协同过滤
    def svd_recommend(self, user_id, n_components=50) # SVD矩阵分解推荐
    def hybrid_recommend(self, user_id, weights=None) # 混合推荐策略
```

### 2. 推荐系统评估器 (`scripts/recommender_evaluator.py`)
```python
# 主要评估功能
class RecommenderEvaluator:
    def precision_at_k(self, recommendations, ground_truth, k)
    def recall_at_k(self, recommendations, ground_truth, k)
    def leave_one_out_evaluation(self, model, test_data)
    def cross_validate(self, model, data, cv_folds=5)
```

### 3. 数据分析器 (`scripts/data_analyzer.py`)
```python
# 数据分析功能
class DataAnalyzer:
    def analyze_user_behavior(self, user_data)        # 用户行为分析
    def analyze_item_popularity(self, item_data)      # 商品热度分析
    def calculate_sparsity(self, interaction_matrix)  # 数据稀疏性分析
    def detect_cold_start(self, user_data, item_data) # 冷启动问题检测
```

### 4. 可视化展示器 (`scripts/recommender_visualizer.py`)
```python
# 可视化功能
class RecommenderVisualizer:
    def plot_recommendation_results(self, recommendations) # 推荐结果可视化
    def plot_evaluation_metrics(self, evaluation_results)  # 评估指标图表
    def create_user_item_heatmap(self, interaction_matrix) # 用户-商品热力图
    def plot_algorithm_comparison(self, comparison_data)   # 算法对比图
```

## 📋 支持的数据格式

### 输入数据
- **用户行为数据**：CSV、JSON格式，包含用户ID、商品ID、评分、时间戳等
- **商品信息数据**：CSV、JSON格式，包含商品ID、名称、类别、价格等
- **用户画像数据**：可选的用户年龄、性别、地域等人口统计学信息
- **评分矩阵**：用户-商品评分的稀疏矩阵格式

### 输出结果
- **推荐列表**：CSV、JSON格式的个性化推荐结果
- **评估报告**：HTML、Markdown格式的详细评估分析
- **可视化图表**：PNG、SVG格式的高质量图表
- **分析洞察**：文本形式的数据洞察和建议

## 🎯 典型应用场景

### 电商推荐
- 基于用户购买历史的商品推荐
- 相似商品推荐和交叉销售
- 个性化首页和购物车推荐
- 新用户的冷启动推荐

### 游戏推荐
- 基于游戏时间和偏好的游戏推荐
- 相似游戏玩家推荐
- 游戏内容推荐和社区推荐
- 新游戏测试用户推荐

### 内容推荐
- 新闻文章和视频内容推荐
- 音乐和播客推荐
- 学习课程推荐
- 社交媒体内容推荐

## 🛠️ 使用流程

### 基础使用流程
1. **数据准备**：加载用户行为数据和商品信息数据
2. **数据探索**：分析用户行为模式和商品分布
3. **算法选择**：选择适合的推荐算法并配置参数
4. **模型训练**：训练推荐模型并进行参数调优
5. **生成推荐**：为目标用户生成个性化推荐列表
6. **效果评估**：评估推荐效果并进行算法对比
7. **结果可视化**：生成推荐结果和评估分析的可视化报告

### 高级分析流程
1. **深度数据挖掘**：用户分群、商品分类、模式识别
2. **多算法集成**：组合多种推荐算法，构建混合推荐系统
3. **实时推荐**：构建在线推荐服务，支持实时个性化推荐
4. **A/B测试**：设计推荐系统A/B测试，评估业务效果
5. **持续优化**：基于用户反馈持续优化推荐算法

## 📚 示例代码

### 快速开始示例
```python
from scripts.recommendation_engine import RecommendationEngine
from scripts.recommender_evaluator import RecommenderEvaluator
from scripts.data_analyzer import DataAnalyzer

# 初始化推荐引擎
engine = RecommendationEngine()
evaluator = RecommenderEvaluator()
analyzer = DataAnalyzer()

# 加载数据
user_data, item_data = engine.load_data('user_behavior.csv', 'product_info.csv')

# 数据分析
user_activity = analyzer.analyze_user_behavior(user_data)
item_popularity = analyzer.analyze_item_popularity(item_data)

# 训练推荐模型
engine.train_item_based_cf(user_data)

# 生成推荐
recommendations = engine.recommend('U001', top_k=10)

# 评估推荐效果
precision = evaluator.precision_at_k(recommendations, ground_truth, k=5)

print(f"推荐结果: {recommendations}")
print(f"Precision@5: {precision:.4f}")
```

## 🔧 配置参数

### 推荐算法参数
- **协同过滤**：相似度阈值、邻居数量、评分归一化方式
- **矩阵分解**：组件数量、正则化参数、学习率、迭代次数
- **混合推荐**：各算法权重、融合策略、推荐列表长度

### 评估参数
- **评估指标**：K值选择、评估数据比例、交叉验证折数
- **数据分割**：训练集/测试集比例、时间分割点
- **性能基准**：基线算法选择、性能阈值设定

## 🎯 技能优势

### 专业性
- 基于权威推荐系统理论，涵盖经典和前沿算法
- 提供完整的推荐系统开发流程和最佳实践
- 支持多种推荐场景和业务需求

### 实用性
- 开箱即用的推荐算法实现，无需复杂的机器学习背景
- 丰富的示例和模板，快速上手和应用
- 详细的文档和注释，便于理解和定制

### 可扩展性
- 模块化设计，易于扩展新的推荐算法
- 灵活的配置系统，支持参数调优和算法组合
- 标准化接口，便于集成到现有系统

### 科学性
- 严格的评估框架，确保推荐效果的科学性
- 多维度评估指标，全面评估推荐系统性能
- 可视化分析，直观展示推荐结果和评估效果

---

通过推荐系统分析技能，用户可以快速构建专业的智能推荐系统，深入理解推荐算法原理，掌握推荐系统评估方法，并将推荐技术应用到实际业务场景中。