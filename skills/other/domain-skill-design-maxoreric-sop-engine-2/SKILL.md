# domain-skill-design

**用途**: 设计领域专用的 Skills（区别于 Core Skills）

**输入**: 
- Workflows 列表（需要什么能力）
- 系统结构（数据在哪）
- 领域特点（health / finance / learning...）

**输出**: Skills 列表及其规格说明

---

## 核心原则

1. **基于 Workflow 需求** - Skill 是为了支撑 Workflow
2. **单一职责** - 每个 Skill 只做一件事
3. **可复用** - 在不同 Workflow 中复用
4. **明确输入输出** - 参数清晰
5. **可评价** - 每个 Skill 都要有评价标准

---

## 输入格式

```yaml
input:
  workflows:                    # Workflow 列表
    - name: string
      steps: array              # 步骤描述
      required_skills: array    # 需要的能力
  
  structure:                    # 系统结构
    data_locations: object      # 数据在哪
    output_locations: object    # 产出在哪
  
  domain: string                # 领域
  requirements: object          # 需求细节
```

---

## 输出格式

```yaml
output:
  skills:                       # Skills 列表
    - name: string              # Skill 名称（kebab-case）
      purpose: string           # 用途
      input: object             # 输入参数
      output: object            # 输出
      dependencies: array       # 依赖的 Core Skills
      complexity: string        # 复杂度（simple/medium/complex）
      priority: string          # 优先级（high/medium/low）
      
      # 实现提示
      implementation_hints:
        approach: string        # 实现思路
        key_logic: string       # 核心逻辑
        edge_cases: array       # 边缘情况
      
      # 评价维度
      evaluation_dimensions:
        - name: string
          weight: number
          criteria: string
```

---

## 设计流程

### 1. 分析 Workflows，提取能力需求

```python
def extract_required_skills(workflows):
    """
    从 Workflow 步骤中提取需要的 Skills
    """
    skills = set()
    
    for workflow in workflows:
        for step in workflow.steps:
            # 识别动词 → 能力
            if "collect" in step:
                skills.add("data-collect-skill")
            if "analyze" in step:
                skills.add("analysis-skill")
            if "generate" in step:
                skills.add("generate-skill")
            if "notify" in step:
                skills.add("notify-skill")
    
    return list(skills)
```

### 2. 按领域细化 Skills

根据领域特点，细化通用能力为具体 Skills：

**示例：健康管理系统**

```yaml
# 通用能力 → 领域 Skills
analyze → 
  - checkup-analysis-skill（体检报告分析）
  - health-indicators-skill（健康指标分析）
  - risk-assessment-skill（风险评估）
  - trend-analysis-skill（趋势分析）

generate →
  - daily-review-skill（生成每日总结）
  - weekly-report-skill（生成每周报告）
  - recommendation-skill（生成健康建议）

notify →
  - notify-user-skill（通知用户）
  - alert-skill（风险预警）
```

### 3. 定义每个 Skill 的规格

```yaml
# 示例：checkup-analysis-skill
name: checkup-analysis-skill
purpose: 分析体检报告，提取关键指标和异常项

input:
  report_path: string           # 体检报告路径（PDF）
  profile_path: string          # 用户健康档案
  history_path: string          # 历史体检记录（可选）

output:
  parsed_data: object           # 解析后的结构化数据
  abnormal_items: array         # 异常指标
  risk_factors: array           # 风险因素
  trends: object                # 与历史对比的趋势
  recommendations: array        # 建议

dependencies:
  - research-skill              # 调研医学知识
  - plan-skill                  # 规划分析步骤

complexity: complex             # 复杂（需要 OCR + NLP + 医学知识）

priority: high                  # 高优先级（核心功能）

implementation_hints:
  approach: |
    1. 使用 OCR 提取 PDF 文本
    2. 使用 NLP 识别指标名称和数值
    3. 与标准范围对比，找出异常项
    4. 结合历史数据，分析趋势
    5. 基于医学知识，评估风险
  
  key_logic: |
    - OCR: pypdf + pytesseract
    - NLP: 正则表达式 + 模式匹配
    - 医学知识: 预定义的指标范围表
    - 趋势分析: 简单统计（增长/下降）
  
  edge_cases:
    - 扫描件质量差，OCR 失败
    - 不同医院的报告格式不同
    - 某些指标缺失
    - 用户没有历史记录

evaluation_dimensions:
  - name: 提取准确度
    weight: 40%
    criteria: 指标和数值提取的正确率
  
  - name: 异常识别准确度
    weight: 30%
    criteria: 异常指标识别的准确率
  
  - name: 建议合理性
    weight: 20%
    criteria: 建议是否科学、可行
  
  - name: 鲁棒性
    weight: 10%
    criteria: 处理各种格式和边缘情况的能力
```

### 4. 识别可复用的 Skills

有些 Skills 可以在多个 Workflow 中复用：

```yaml
# 复用示例
notify-user-skill:
  used_in:
    - daily-check workflow
    - weekly-report workflow
    - checkup-analysis workflow
  
  # 通用设计
  input:
    message: string
    priority: string (normal/high/urgent)
    channel: string (file/email/...)
  
  output:
    notified: boolean
    timestamp: string
```

---

## 示例

### 输入: 健康管理系统

```yaml
workflows:
  - name: daily-check
    steps:
      - collect_today_data
      - analyze_indicators
      - generate_report
      - notify_user
    required_skills:
      - data-collect-skill
      - health-indicators-skill
      - daily-review-skill
      - notify-user-skill
  
  - name: weekly-report
    steps:
      - aggregate_week_data
      - analyze_trends
      - generate_insights
      - notify_user
    required_skills:
      - data-collect-skill
      - trend-analysis-skill
      - weekly-report-skill
      - notify-user-skill
  
  - name: checkup-analysis
    steps:
      - parse_report
      - compare_history
      - assess_risks
      - generate_recommendations
    required_skills:
      - checkup-analysis-skill
      - risk-assessment-skill
      - recommendation-skill
      - notify-user-skill

structure:
  data_locations:
    profile: data/profile/profile.json
    indicators: data/indicators/{date}.json
    checkups: data/checkups/
  
  output_locations:
    reports: outputs/reports/

domain: health
focus: disease_prevention
```

---

### 输出: Skills 列表

```yaml
skills:
  # ────────────────────────────────────
  # 数据相关
  # ────────────────────────────────────
  - name: data-collect-skill
    purpose: 收集和聚合数据
    complexity: simple
    priority: high
    input:
      date: string
      sources: array
    output:
      collected_data: object
    dependencies: []
  
  # ────────────────────────────────────
  # 分析相关
  # ────────────────────────────────────
  - name: checkup-analysis-skill
    purpose: 分析体检报告
    complexity: complex
    priority: high
    input:
      report_path: string
      profile_path: string
    output:
      parsed_data: object
      abnormal_items: array
      risk_factors: array
    dependencies:
      - research-skill
    implementation_hints:
      approach: "OCR + NLP + 医学知识库"
      key_logic: "pypdf + pytesseract + 规则引擎"
      edge_cases:
        - "不同医院格式"
        - "扫描质量差"
    evaluation_dimensions:
      - name: 提取准确度
        weight: 40%
      - name: 异常识别准确度
        weight: 30%
  
  - name: health-indicators-skill
    purpose: 分析每日健康指标
    complexity: medium
    priority: high
    input:
      indicators: object
      profile: object
    output:
      analysis: object
      alerts: array
    dependencies: []
  
  - name: risk-assessment-skill
    purpose: 评估健康风险
    complexity: medium
    priority: high
    input:
      indicators: object
      checkup_data: object
      profile: object
    output:
      risk_level: string
      risk_factors: array
      suggestions: array
    dependencies:
      - research-skill
  
  - name: trend-analysis-skill
    purpose: 分析健康指标趋势
    complexity: medium
    priority: medium
    input:
      historical_data: array
      timeframe: string
    output:
      trends: object
      insights: array
    dependencies: []
  
  # ────────────────────────────────────
  # 报告生成相关
  # ────────────────────────────────────
  - name: daily-review-skill
    purpose: 生成每日健康总结
    complexity: simple
    priority: high
    input:
      analysis: object
      date: string
    output:
      report: string (Markdown)
    dependencies: []
  
  - name: weekly-report-skill
    purpose: 生成每周健康报告
    complexity: medium
    priority: medium
    input:
      week_data: object
      trends: object
    output:
      report: string (Markdown)
    dependencies: []
  
  - name: recommendation-skill
    purpose: 生成健康建议
    complexity: medium
    priority: high
    input:
      analysis: object
      risks: array
    output:
      recommendations: array
    dependencies:
      - research-skill
  
  # ────────────────────────────────────
  # 通知相关
  # ────────────────────────────────────
  - name: notify-user-skill
    purpose: 通知用户
    complexity: simple
    priority: high
    input:
      message: string
      priority: string
      path: string (可选)
    output:
      notified: boolean
      method: string
    dependencies: []
    implementation_hints:
      approach: "第一版：写文件到 outputs/；后续扩展：邮件、Slack"
      key_logic: "简单文件写入"
```

---

## 设计模式

### 1. 数据处理 Skills

```yaml
# 模式：collect → parse → validate → transform
- collect-skill:    收集原始数据
- parse-skill:      解析格式
- validate-skill:   验证数据
- transform-skill:  转换格式
```

### 2. 分析 Skills

```yaml
# 模式：analyze → interpret → assess → recommend
- analyze-skill:     分析数据
- interpret-skill:   解释结果
- assess-skill:      评估风险
- recommend-skill:   生成建议
```

### 3. 报告 Skills

```yaml
# 模式：aggregate → visualize → format → output
- aggregate-skill:   聚合信息
- visualize-skill:   可视化（可选）
- format-skill:      格式化
- output-skill:      输出
```

---

## 领域 Skills 库

### health（健康管理）

常见 Skills：
- checkup-analysis-skill
- health-indicators-skill
- risk-assessment-skill
- trend-analysis-skill
- diet-analysis-skill
- exercise-tracking-skill
- medication-reminder-skill
- symptom-checker-skill

### finance（财务管理）

常见 Skills：
- transaction-categorize-skill
- budget-tracking-skill
- investment-analysis-skill
- tax-calculation-skill
- expense-forecast-skill
- portfolio-rebalance-skill

### learning（学习管理）

常见 Skills：
- progress-tracking-skill
- quiz-generation-skill
- note-summarize-skill
- spaced-repetition-skill
- goal-tracking-skill

---

## 评价标准

见 `criteria.md`

---

## 版本历史

- v1.0.0 (2026-01-19): 初始版本
