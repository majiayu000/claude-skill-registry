# structure-design-skill

**用途**: 设计系统的目录结构

**输入**: 计划（plan）包含系统需求、功能模块等

**输出**: 完整的目录结构定义

---

## 核心原则

1. **遵循 sop-engine 标准** - 所有系统都应遵循标准目录结构
2. **按功能分层** - .claude/ 存配置，data/ 存数据，outputs/ 存产出
3. **可扩展** - 预留扩展空间
4. **清晰命名** - 目录和文件名要自解释

---

## 标准目录结构模板

```
<system-name>/
├── .claude/                    # Claude Code 配置
│   ├── agents/                 # Subagents
│   ├── skills/                 # Skills
│   ├── commands/               # Slash commands（可选）
│   └── hooks/                  # Hooks（可选）
├── .sop-engine/                # sop-engine 运行时
│   ├── skills/                 # Skill 运行数据
│   ├── workflows/              # Workflow 定义
│   └── running/                # 运行中的实例
├── agents/                     # Agent 工作空间
│   └── <agent-name>/
│       ├── knowledge/          # 知识库
│       └── handoff/            # 交接记录
├── data/                       # 系统数据
│   ├── <domain-specific>/      # 领域特定数据
│   └── ...
├── outputs/                    # 产出
│   └── <output-type>/
├── README.md                   # 使用说明
└── DESIGN.md                   # 设计文档
```

---

## 输入格式

```yaml
plan:
  system_name: string           # 系统名称
  domain: string                # 领域（health, finance, learning...）
  agents:                       # Agent 列表
    - name: string
      responsibilities: array
  skills:                       # Skill 列表
    - name: string
      purpose: string
  workflows:                    # Workflow 列表
    - name: string
      steps: array
  data_requirements:            # 数据需求
    - type: string              # 数据类型
      structure: string         # 存储方式
  outputs:                      # 产出类型
    - type: string              # 报告、图表等
```

---

## 输出格式

```yaml
structure:
  root: string                  # 根目录名
  directories:                  # 目录列表
    - path: string              # 相对路径
      purpose: string           # 用途说明
      required: boolean         # 是否必需
      examples: array           # 示例文件
  
  files:                        # 必需的文件
    - path: string
      purpose: string
      template: string          # 模板内容（可选）
  
  data_structure:               # 数据结构说明
    - category: string
      location: string
      format: string
```

---

## 执行逻辑

### 1. 分析需求

从 plan 中提取：
- 系统类型（health / finance / learning / ...）
- Agent 数量
- Skill 数量
- Workflow 数量
- 数据类型
- 产出类型

### 2. 确定目录

基于标准模板 + 领域特定需求：

```python
def design_structure(plan):
    structure = {
        "root": plan.system_name,
        "directories": [],
        "files": []
    }
    
    # 标准目录（必需）
    structure["directories"].extend([
        {"path": ".claude/agents/", "required": True},
        {"path": ".claude/skills/", "required": True},
        {"path": ".sop-engine/workflows/", "required": True},
        {"path": "data/", "required": True},
        {"path": "outputs/", "required": True}
    ])
    
    # 领域特定目录
    if plan.domain == "health":
        structure["directories"].extend([
            {"path": "data/profile/", "purpose": "用户健康档案"},
            {"path": "data/indicators/", "purpose": "健康指标记录"},
            {"path": "data/checkups/", "purpose": "体检报告"},
            {"path": "outputs/reports/", "purpose": "健康报告"}
        ])
    
    elif plan.domain == "finance":
        structure["directories"].extend([
            {"path": "data/accounts/", "purpose": "账户信息"},
            {"path": "data/transactions/", "purpose": "交易记录"},
            {"path": "outputs/analysis/", "purpose": "财务分析"}
        ])
    
    # ... 更多领域
    
    return structure
```

### 3. 添加必需文件

```yaml
files:
  - path: README.md
    purpose: 系统使用说明
    template: |
      # {system_name}
      
      ## 概述
      
      ## 快速开始
      
      ## 功能说明
  
  - path: DESIGN.md
    purpose: 设计文档
    template: |
      # {system_name} 设计文档
      
      ## 系统目标
      
      ## 架构设计
      
      ## 数据流
  
  - path: data/.gitkeep
    purpose: 保留空目录
```

### 4. 生成数据结构说明

```yaml
data_structure:
  - category: 个人档案
    location: data/profile/profile.json
    format: |
      {
        "name": "string",
        "age": "number",
        "health_history": []
      }
  
  - category: 健康指标
    location: data/indicators/{date}.json
    format: |
      {
        "date": "YYYY-MM-DD",
        "weight": "number",
        "blood_pressure": "string",
        ...
      }
```

---

## 示例

### 输入: 健康管理系统

```yaml
plan:
  system_name: health-system
  domain: health
  focus: disease_prevention
  
  agents:
    - name: health-advisor
      responsibilities:
        - 分析体检报告
        - 评估健康风险
        - 提供建议
  
  skills:
    - name: checkup-analysis-skill
      purpose: 分析体检报告
    - name: health-indicators-skill
      purpose: 追踪健康指标
    - name: risk-assessment-skill
      purpose: 评估风险
    # ... 更多
  
  workflows:
    - name: daily-check
      trigger: "21:00"
    - name: weekly-report
      trigger: "Sunday 20:00"
    - name: checkup-analysis
      trigger: "file_upload"
  
  data_requirements:
    - type: profile
      structure: JSON
    - type: indicators
      structure: daily JSON files
    - type: checkups
      structure: PDF + parsed JSON
  
  outputs:
    - type: reports
      format: Markdown
```

---

### 输出: 目录结构

```yaml
structure:
  root: health-system
  
  directories:
    # 标准目录
    - path: .claude/agents/
      purpose: Agent 定义
      required: true
      examples:
        - health-advisor.md
    
    - path: .claude/skills/
      purpose: Skill 定义
      required: true
      examples:
        - checkup-analysis/
        - health-indicators/
        - risk-assessment/
    
    - path: .sop-engine/workflows/
      purpose: Workflow 定义
      required: true
      examples:
        - daily-check.yaml
        - weekly-report.yaml
        - checkup-analysis.yaml
    
    - path: .sop-engine/running/
      purpose: 运行中的 Workflow 实例
      required: true
    
    - path: agents/health-advisor/
      purpose: health-advisor 的工作空间
      required: true
    
    - path: agents/health-advisor/knowledge/
      purpose: 积累的健康知识
      required: true
    
    - path: agents/health-advisor/handoff/
      purpose: 任务交接记录
      required: true
    
    # 领域特定目录
    - path: data/profile/
      purpose: 用户健康档案
      required: true
      examples:
        - profile.json
    
    - path: data/indicators/
      purpose: 每日健康指标
      required: true
      examples:
        - 2026-01-19.json
        - 2026-01-20.json
    
    - path: data/checkups/
      purpose: 体检报告（原始 + 解析后）
      required: true
      examples:
        - raw/2025-annual-checkup.pdf
        - parsed/2025-annual-checkup.json
    
    - path: outputs/reports/
      purpose: 生成的健康报告
      required: true
      examples:
        - daily/2026-01-19-daily.md
        - weekly/2026-W03-weekly.md
  
  files:
    - path: README.md
      purpose: 系统使用说明
      template: |
        # health-system
        
        健康管理系统 - 预防疾病、追踪指标、评估风险
        
        ## 快速开始
        
        1. 填写个人档案: `data/profile/profile.json`
        2. 记录今日数据: `data/indicators/{今天日期}.json`
        3. 触发每日检查: "执行每日健康检查"
        
        ## 核心功能
        
        - 每日健康检查（21:00 自动触发）
        - 每周健康报告（周日 20:00 自动触发）
        - 体检报告分析（上传文件后触发）
    
    - path: DESIGN.md
      purpose: 设计文档
    
    - path: data/profile/profile.json
      purpose: 个人健康档案（示例）
      template: |
        {
          "name": "张三",
          "age": 35,
          "gender": "male",
          "height": 175,
          "health_history": [
            "无重大疾病史"
          ],
          "allergies": [],
          "medications": []
        }
    
    - path: data/indicators/2026-01-19.json
      purpose: 健康指标示例
      template: |
        {
          "date": "2026-01-19",
          "weight": 70.5,
          "blood_pressure": "120/80",
          "heart_rate": 72,
          "sleep_hours": 7.5,
          "exercise_minutes": 30,
          "water_intake_ml": 2000,
          "notes": "感觉良好"
        }
  
  data_structure:
    - category: 个人档案
      location: data/profile/profile.json
      format: |
        {
          "name": "string",
          "age": "number",
          "gender": "male | female",
          "height": "number (cm)",
          "health_history": ["string"],
          "allergies": ["string"],
          "medications": ["string"]
        }
    
    - category: 每日指标
      location: data/indicators/{YYYY-MM-DD}.json
      format: |
        {
          "date": "YYYY-MM-DD",
          "weight": "number (kg)",
          "blood_pressure": "string (120/80)",
          "heart_rate": "number (bpm)",
          "sleep_hours": "number",
          "exercise_minutes": "number",
          "water_intake_ml": "number",
          "notes": "string"
        }
    
    - category: 体检报告
      location: data/checkups/parsed/{name}.json
      format: |
        {
          "date": "YYYY-MM-DD",
          "source": "string (医院名)",
          "indicators": {
            "血常规": {...},
            "肝功能": {...},
            "肾功能": {...}
          },
          "abnormal_items": ["string"],
          "risk_factors": ["string"]
        }
```

---

## 领域模板库

### health（健康管理）

```yaml
directories:
  - data/profile/           # 健康档案
  - data/indicators/        # 每日指标
  - data/checkups/          # 体检报告
  - data/medications/       # 用药记录（如果是慢病管理）
  - data/diet/              # 饮食记录（如果需要）
  - data/exercise/          # 运动记录（如果需要）
  - outputs/reports/daily/  # 每日报告
  - outputs/reports/weekly/ # 每周报告
```

### finance（财务管理）

```yaml
directories:
  - data/accounts/          # 账户信息
  - data/transactions/      # 交易记录
  - data/budgets/           # 预算
  - data/investments/       # 投资
  - outputs/analysis/       # 财务分析
  - outputs/tax/            # 税务文档
```

### learning（学习管理）

```yaml
directories:
  - data/goals/             # 学习目标
  - data/progress/          # 学习进度
  - data/notes/             # 笔记
  - data/resources/         # 学习资源
  - outputs/summaries/      # 总结
  - outputs/plans/          # 学习计划
```

---

## 评价标准

见 `criteria.md`

---

## 版本历史

- v1.0.0 (2026-01-19): 初始版本
