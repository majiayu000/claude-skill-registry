# agent-define-skill

**用途**: 定义 Agent（Subagent）的职责、擅长领域和配置

**输入**: Skills 列表、Workflows 列表、系统需求

**输出**: Agent 定义文件（.md）

---

## 核心原则

1. **职责明确** - Agent 的职责要清晰
2. **技能匹配** - Agent 擅长的 Skills 要与职责匹配
3. **领域专精** - 每个 Agent 专注于特定领域
4. **可协作** - Agent 之间可以通过 handoff 协作
5. **适度数量** - 不要创建过多 Agent

---

## 输入格式

```yaml
input:
  system_info:
    name: string                    # 系统名称
    domain: string                  # 领域
    purpose: string                 # 系统目标
  
  skills:                           # 可用的 Skills
    - name: string
      purpose: string
      complexity: string
  
  workflows:                        # Workflows 列表
    - name: string
      purpose: string
      main_skills: array            # 主要使用的 Skills
  
  requirements:
    collaboration_needed: boolean   # 是否需要多 Agent 协作
    specialization_level: string    # 专业化程度（low/medium/high）
```

---

## 输出格式

```yaml
output:
  agents:                           # Agent 列表
    - name: string                  # Agent 名称
      role: string                  # 角色描述
      responsibilities: array       # 职责列表
      skills: array                 # 擅长的 Skills
      workflows: array              # 负责的 Workflows
      personality: string           # 性格特点（可选）
      
      # Agent 文件内容
      file_content: string          # 完整的 .md 文件内容
```

---

## 执行逻辑

### 1. 分析系统需求

确定是否需要多个 Agent：

```python
def should_create_multiple_agents(system_info, skills, workflows):
    """
    判断是否需要创建多个 Agent
    """
    # 简单系统：1 个 Agent
    if len(skills) <= 5 and len(workflows) <= 3:
        return False
    
    # 复杂系统但领域单一：1 个 Agent
    if system_info.specialization_level == "low":
        return False
    
    # 多领域系统：多个 Agent
    skill_domains = identify_skill_domains(skills)
    if len(skill_domains) >= 2:
        return True
    
    return False
```

---

### 2. 识别领域和角色

将 Skills 和 Workflows 按领域分组：

```python
def identify_domains(skills, workflows):
    """
    识别不同的领域
    """
    # 健康管理系统示例
    domains = {
        "analysis": [],      # 分析类
        "reporting": [],     # 报告类
        "data_management": [] # 数据管理类
    }
    
    for skill in skills:
        if "analysis" in skill.name or "assess" in skill.name:
            domains["analysis"].append(skill)
        elif "report" in skill.name or "review" in skill.name:
            domains["reporting"].append(skill)
        elif "collect" in skill.name or "data" in skill.name:
            domains["data_management"].append(skill)
    
    return domains
```

---

### 3. 为每个领域创建 Agent

```python
def create_agent_for_domain(domain_name, skills, workflows, system_info):
    """
    为特定领域创建 Agent
    """
    # 健康管理系统 - 分析领域示例
    if domain_name == "analysis":
        return {
            "name": "health-advisor",
            "role": "健康顾问",
            "responsibilities": [
                "分析体检报告",
                "评估健康风险",
                "追踪健康指标",
                "提供健康建议"
            ],
            "skills": [
                "checkup-analysis-skill",
                "health-indicators-skill",
                "risk-assessment-skill"
            ],
            "workflows": [
                "checkup-analysis",
                "daily-check"
            ]
        }
```

---

### 4. 生成 Agent 文件

Agent 文件格式（基于 Claude Code Subagent 规范）：

```markdown
# Agent Name

**Role**: <简短描述>

---

## Responsibilities

<职责列表>

---

## Skills

<擅长的 Skills 列表及说明>

---

## Working Style

<工作风格、性格特点>

---

## Collaboration

<与其他 Agent 如何协作>
```

---

## Agent 模板库

### 模板 1: 单一通用 Agent

适用于简单系统（<= 5 Skills, <= 3 Workflows）

```markdown
# system-assistant

**Role**: 系统助手 - 负责系统的所有任务

---

## Responsibilities

- 执行所有 Workflows
- 使用所有 Skills
- 与用户交互

---

## Skills

- skill-1
- skill-2
- skill-3
- ...

---

## Working Style

全能型助手，什么都能做。

---

## Collaboration

单一 Agent，不需要协作。
```

---

### 模板 2: 专业化 Agent（健康顾问）

适用于需要专业知识的领域

```markdown
# health-advisor

**Role**: 健康顾问 - 分析健康数据，提供专业建议

---

## Responsibilities

- 分析体检报告，提取关键指标和异常项
- 评估健康风险，识别潜在问题
- 追踪健康指标趋势，发现变化
- 提供个性化的健康建议

---

## Skills

擅长以下 Skills：

### 1. checkup-analysis-skill
分析体检报告，识别异常指标

### 2. health-indicators-skill
追踪和分析每日健康指标

### 3. risk-assessment-skill
评估健康风险，预警潜在问题

### 4. recommendation-skill
基于分析结果，生成健康建议

---

## Working Style

- **专业**: 具有医学知识背景，能理解各种健康指标
- **细致**: 仔细分析每个数据点，不遗漏异常
- **关怀**: 以用户健康为第一优先级，提供温暖的建议
- **循证**: 所有建议都基于医学证据和标准

---

## Collaboration

- **与数据管理员协作**: 接收整理好的健康数据
- **与报告生成器协作**: 提供分析结果用于生成报告
- **与用户交互**: 直接解答用户关于健康的疑问

---

## Knowledge Base

- 常见健康指标的正常范围
- 体检项目的临床意义
- 常见慢性疾病的风险因素
- 健康生活方式建议

---

## Limitations

- 不能替代医生诊断
- 不能开具处方
- 遇到严重异常时，建议用户就医
```

---

### 模板 3: 协作型 Agent（数据管理员）

适用于需要多 Agent 协作的系统

```markdown
# data-manager

**Role**: 数据管理员 - 负责数据收集、整理和存储

---

## Responsibilities

- 收集来自不同源的健康数据
- 验证数据完整性和准确性
- 整理数据为标准格式
- 存储数据到正确的位置

---

## Skills

擅长以下 Skills：

### 1. data-collect-skill
从各种源收集数据（文件、API、用户输入）

### 2. data-validate-skill
验证数据的完整性和准确性

### 3. data-transform-skill
转换数据为标准格式

---

## Working Style

- **细心**: 不遗漏任何数据点
- **严谨**: 确保数据准确无误
- **有序**: 数据存储井井有条
- **高效**: 快速处理大量数据

---

## Collaboration

### Handoff to health-advisor
```
任务: 分析今日健康数据
输入:
  - data/indicators/2026-01-19.json
  - data/profile/profile.json
状态: 数据已收集和验证
```

### Receive from external-data-fetcher
```
任务: 获取体检报告
输出:
  - data/checkups/raw/2025-annual.pdf
```

---

## Data Standards

- 所有日期使用 ISO 8601 格式
- 所有数值保留 2 位小数
- 所有文件使用 UTF-8 编码
- JSON 文件使用 2 空格缩进
```

---

## 示例

### 输入: 健康管理系统

```yaml
system_info:
  name: health-system
  domain: health
  purpose: 预防疾病，追踪健康指标

skills:
  - name: checkup-analysis-skill
    purpose: 分析体检报告
    complexity: complex
  
  - name: health-indicators-skill
    purpose: 分析每日指标
    complexity: medium
  
  - name: risk-assessment-skill
    purpose: 评估健康风险
    complexity: medium
  
  - name: data-collect-skill
    purpose: 收集数据
    complexity: simple
  
  - name: daily-review-skill
    purpose: 生成每日总结
    complexity: simple
  
  - name: weekly-report-skill
    purpose: 生成每周报告
    complexity: medium

workflows:
  - name: daily-check
    purpose: 每日健康检查
    main_skills:
      - data-collect-skill
      - health-indicators-skill
      - daily-review-skill
  
  - name: checkup-analysis
    purpose: 体检报告分析
    main_skills:
      - checkup-analysis-skill
      - risk-assessment-skill

requirements:
  collaboration_needed: false
  specialization_level: medium
```

---

### 输出: 单个专业化 Agent

```yaml
agents:
  - name: health-advisor
    role: 健康顾问
    
    responsibilities:
      - 分析体检报告，提取关键指标和异常项
      - 评估健康风险，识别潜在问题
      - 追踪健康指标趋势，发现变化
      - 生成每日健康总结和每周报告
      - 提供个性化的健康建议
    
    skills:
      - checkup-analysis-skill      # 复杂
      - health-indicators-skill      # 中等
      - risk-assessment-skill        # 中等
      - daily-review-skill           # 简单
      - weekly-report-skill          # 中等
    
    workflows:
      - daily-check
      - checkup-analysis
    
    personality: 专业、细致、关怀
    
    file_content: |
      # health-advisor
      
      **Role**: 健康顾问 - 分析健康数据，提供专业建议
      
      [完整内容见上面的模板 2]
```

---

## 设计决策指南

### 何时创建单个 Agent？

**适用场景**:
- 简单系统（<= 5 Skills）
- 领域单一
- 不需要专业化分工

**优点**:
- 简单
- 无协作开销
- 易于理解

---

### 何时创建多个 Agent？

**适用场景**:
- 复杂系统（> 10 Skills）
- 多个明确的领域
- 需要专业化分工

**优点**:
- 职责清晰
- 专业化
- 可并行工作

**缺点**:
- 需要协作机制
- 复杂度增加

---

### Agent 数量建议

| 系统规模 | Skills 数量 | 建议 Agent 数量 |
|---------|------------|---------------|
| 小型 | 1-5 | 1 个 |
| 中型 | 6-10 | 1-2 个 |
| 大型 | 11-20 | 2-3 个 |
| 超大型 | 20+ | 3-5 个 |

**原则**: 宁少勿多，从 1 个开始，需要时再拆分

---

## Agent 命名规范

### 名称格式

- 使用 kebab-case
- 名词或角色名
- 简洁明了

**示例**:
- ✅ `health-advisor`
- ✅ `data-manager`
- ✅ `report-generator`
- ❌ `Agent1`
- ❌ `my_agent`

---

### 角色描述

- 1-2 个词
- 说明职责
- 易于理解

**示例**:
- ✅ "健康顾问 - 分析健康数据，提供专业建议"
- ✅ "数据管理员 - 负责数据收集和整理"
- ❌ "Agent that does stuff"

---

## 评价标准

见 `criteria.md`

---

## 实现注意事项

### 1. Skills 分配合理

每个 Agent 的 Skills 应该：
- 相关性强（都属于同一领域）
- 覆盖完整（该领域的所有 Skills）
- 数量适中（3-8 个）

### 2. 职责不重叠

多个 Agent 的职责应该：
- 互不重叠
- 边界清晰
- 互补完整

### 3. 协作机制清晰

如果有多个 Agent：
- 定义清晰的 handoff 流程
- 说明何时协作
- 说明如何协作

### 4. 性格和风格

可以给 Agent 定义性格：
- 专业型（健康顾问、财务分析师）
- 效率型（数据管理员、自动化助手）
- 创意型（内容创作者、设计师）

---

## 常见模式

### 模式 1: 单一全能 Agent

```
[所有 Skills] → single-agent
```

### 模式 2: 分析 + 执行

```
analyzer-agent → [分析类 Skills]
executor-agent → [执行类 Skills]
```

### 模式 3: 前台 + 后台

```
frontend-agent → [与用户交互]
backend-agent → [数据处理]
```

### 模式 4: 领域专家团队

```
domain-expert-1 → [领域 A Skills]
domain-expert-2 → [领域 B Skills]
coordinator → [协调]
```

---

## 版本历史

- v1.0.0 (2026-01-19): 初始版本
