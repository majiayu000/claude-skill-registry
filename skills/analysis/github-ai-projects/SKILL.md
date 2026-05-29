---
name: github-ai-projects
description: 这个skill专门用于监控GitHub上的热门AI项目，获取项目的简述信息和不同时间范围的更新状态。当用户需要了解GitHub AI项目动态时使用此skill。通过智能分析项目的活跃度、星标增长、提交频率等指标，为用户提供AI领域最具潜力和活跃度的开源项目洞察。
license: MIT
allowed-tools: [WebSearch, WebFetch, Write, Read]
---

## 使用时机
当用户提出以下需求时，使用此skill：
- "获取GitHub热门AI项目"
- "最近AI领域有什么值得关注的开源项目"
- "查看AI项目更新状态"
- "GitHub上AI项目活跃度分析"
- "最近一天/本周/最近一个月的AI项目动态"

## 执行流程

### 1. 项目搜索策略
使用GitHub API和搜索功能，重点关注：
- **AI/ML关键词**：artificial intelligence, machine learning, deep learning, neural network
- **热门框架**：pytorch, tensorflow, scikit-learn, huggingface, langchain
- **新兴技术**：llm, transformer, diffusion, stable diffusion, chatgpt
- **应用领域**：computer vision, nlp, reinforcement learning, generative ai

搜索参数：
- 按星标数量排序（stars:>100）
- 按最近更新时间排序
- 过滤低质量项目（要求有README、有代码提交）
- 限制编程语言（Python, JavaScript, C++, Rust等）

### 2. 时间范围分析
针对不同时间范围分析项目活跃度：

#### 最近1天（24小时）
- **活跃指标**：新的代码提交、issue讨论、PR合并
- **热度指标**：星标增长、fork增长
- **关注重点**：紧急bug修复、新功能发布、社区讨论热点

#### 本周（7天）
- **活跃指标**：提交频率、版本发布、重要合并
- **热度指标**：周星标增长率、社区参与度
- **关注重点**：功能迭代、技术债务清理、社区建设

#### 最近一个月（30天）
- **活跃指标**：版本发布周期、重要功能更新
- **热度指标**：月度增长趋势、长期活跃度
- **关注重点**：重大更新、架构改进、生态建设

### 3. 项目评估维度

#### 技术指标
- **代码质量**：提交频率、代码审查、测试覆盖率
- **文档完整性**：README质量、API文档、示例代码
- **依赖管理**：依赖更新频率、安全漏洞修复

#### 社区指标
- **活跃度**：issues讨论、PR参与、社区响应
- **增长性**：星标增长、fork数量、贡献者增加
- **多样性**：贡献者地理分布、使用场景多样性

#### 创新指标
- **技术新颖性**：是否采用前沿技术或方法
- **应用价值**：解决实际问题的能力
- **生态影响**：对相关项目或社区的影响

### 4. 项目简述生成
为每个项目生成简明扼要的简述：

#### 简述结构
```
📦 [项目名称]
⭐ [星标数] | 🍴 [Fork数] | 📅 [最后更新]
🏷️ [主要标签] [编程语言]
📝 [项目简介 - 50字以内]
🔥 [热度分析：为什么值得关注]
📊 [活跃度评分：1-10分]
🔗 [项目链接]
```

#### 热度分析要点
- **技术创新性**：是否采用了新的技术或方法
- **实用价值**：解决了什么实际问题
- **社区活跃度**：开发者参与程度
- **成长潜力**：未来发展趋势
- **学习价值**：对AI学习者的参考价值

### 5. 输出格式设计

#### 整体报告格式
```
🚀 GitHub AI热门项目监控报告
📅 更新时间：{当前日期时间}
🔍 监控范围：{搜索条件}

## 📈 热度排行榜（Top 10）

### 🥇 第1名：[项目名称]
⭐ [星标数] | 🍴 [Fork数] | 📅 [最后更新]
🏷️ [主要标签] [编程语言]
📝 [项目简介 - 50字以内]
🔥 [热度分析：为什么值得关注]
📊 [活跃度评分：1-10分]
🔗 [项目链接]

### 🥈 第2名：[项目名称]
⭐ [星标数] | 🍴 [Fork数] | 📅 [最后更新]
🏷️ [主要标签] [编程语言]
📝 [项目简介 - 50字以内]
🔥 [热度分析：为什么值得关注]
📊 [活跃度评分：1-10分]
🔗 [项目链接]

## ⏰ 时间维度分析

### 🔥 最近1天活跃项目
- [项目列表和简要分析]

### 📅 本周热门项目
- [项目列表和简要分析]

### 📊 最近一个月趋势
- [项目列表和简要分析]

## 🎯 重点推荐
[基于多个维度综合评估的重点推荐项目]

## 📋 数据洞察
[整体趋势分析和发现]
```

## 技术实现方案

### 1. GitHub API集成
- **搜索API**：使用GitHub搜索API查找相关项目
- **仓库API**：获取项目详细信息、统计数据
- **提交API**：分析提交历史和活跃度
- **Issue API**：监控社区讨论和问题反馈

### 2. 数据处理流程
```python
# 伪代码示例
def fetch_github_ai_projects():
    # 搜索AI相关项目
    projects = search_github_repos(
        query="artificial intelligence machine learning",
        sort="stars",
        order="desc"
    )
    
    # 获取项目详细信息
    detailed_projects = []
    for project in projects:
        details = get_repo_details(project['id'])
        metrics = calculate_activity_metrics(details)
        detailed_projects.append({
            'basic_info': project,
            'details': details,
            'metrics': metrics,
            'summary': generate_summary(project, details, metrics)
        })
    
    return rank_projects(detailed_projects)
```

### 3. 活跃度计算算法
```python
def calculate_activity_score(repo_details, timeframe):
    weights = {
        'commits': 0.4,
        'issues': 0.2,
        'pull_requests': 0.2,
        'stars_growth': 0.1,
        'forks_growth': 0.1
    }
    
    # 根据时间范围计算各项指标
    commits_score = normalize_commits(repo_details['commits'], timeframe)
    issues_score = normalize_issues(repo_details['issues'], timeframe)
    pr_score = normalize_prs(repo_details['pull_requests'], timeframe)
    stars_score = normalize_stars_growth(repo_details['stars'], timeframe)
    forks_score = normalize_forks_growth(repo_details['forks'], timeframe)
    
    # 加权计算总活跃度评分
    total_score = (
        commits_score * weights['commits'] +
        issues_score * weights['issues'] +
        pr_score * weights['pull_requests'] +
        stars_score * weights['stars_growth'] +
        forks_score * weights['forks_growth']
    )
    
    return min(10, max(1, total_score))
```

## 质量控制标准

### 项目筛选标准
- **最低要求**：至少100个星标，有README文档
- **活跃度要求**：最近一个月内有代码提交
- **质量标准**：有清晰的文档和许可证
- **相关性**：确实属于AI/ML领域

### 数据准确性
- **实时更新**：确保获取最新数据
- **多源验证**：交叉验证不同数据源
- **异常检测**：识别和处理异常数据
- **定期校准**：定期调整评估算法

## 使用示例

### 基本用法
```
用户："获取GitHub上最近的热门AI项目"
AI执行：
1. 搜索AI相关项目
2. 分析最近一周活跃度
3. 生成项目排行榜
4. 输出详细报告
```

### 高级用法
```
用户："重点关注计算机视觉领域的项目，最近一个月的更新"
AI执行：
1. 搜索computer vision相关项目
2. 过滤最近一个月有更新的项目
3. 分析CV领域的具体技术栈
4. 生成专业化的分析报告
```

## 扩展功能

### 1. 个性化推荐
- 基于用户兴趣标签推荐项目
- 学习路径建议
- 技术栈匹配分析

### 2. 趋势分析
- 长期趋势图表
- 技术热点变化
- 社区发展预测

### 3. 竞品分析
- 同类项目对比
- 技术方案比较
- 社区生态分析



  
## 注意事项
1. **API限制**：注意GitHub API的调用限制
2. **数据延迟**：GitHub数据可能有延迟，需要考虑时效性
3. **语言处理**：项目描述可能包含多语言，需要适当处理
4. **质量判断**：避免基于单一指标判断项目质量
5. **隐私保护**：不获取或分析用户私有仓库信息
6. **保存**：把内容以日期为分界,保存在根目录下的GitHubHot.md。

现在你可以开始为用户提供GitHub AI热门项目的监控和分析服务了！