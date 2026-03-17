# workflow-define-skill

**用途**: 定义 Workflow（基于需求生成 Workflow YAML）

**输入**: 需求、系统结构、Skills 列表

**输出**: Workflow YAML 定义

---

## 核心原则

1. **基于需求驱动** - Workflow 服务于具体需求
2. **复用 Skills** - 优先使用已有的 Skills
3. **遵循规范** - 严格遵循 workflow-spec.md
4. **清晰命名** - Workflow 和节点名称自解释
5. **适度复杂** - 避免过度设计，保持简单

---

## 输入格式

```yaml
input:
  requirement:                      # 需求描述
    name: string                    # Workflow 名称
    purpose: string                 # 用途
    trigger: object                 # 触发方式
    expected_flow: array            # 期望的步骤流程
    inputs: object                  # 输入参数
    outputs: object                 # 输出结果
  
  available_skills:                 # 可用的 Skills
    - name: string
      input: object
      output: object
  
  structure:                        # 系统结构（数据路径）
    data_paths: object
    output_paths: object
  
  domain: string                    # 领域（health / finance / learning）
```

---

## 输出格式

```yaml
output:
  workflow:                         # 完整的 Workflow 定义
    name: string
    description: string
    version: string
    
    input: object                   # Workflow 输入
    output: object                  # Workflow 输出
    
    nodes: object                   # 节点定义
    edges: array                    # 边定义
    
    entry: string                   # 入口节点
    exit: string                    # 出口节点
  
  metadata:                         # 元数据
    complexity: string              # simple / medium / complex
    estimated_duration: string      # 预计执行时间
    dependencies: array             # 依赖的 Skills
```

---

## 执行逻辑

### 1. 分析需求

从需求中提取关键信息：

```python
def analyze_requirement(requirement):
    """
    提取 Workflow 的关键特征
    """
    return {
        "type": identify_workflow_type(requirement.purpose),
        "steps": requirement.expected_flow,
        "trigger_type": requirement.trigger.type,  # manual / tick / event
        "has_loop": check_if_needs_loop(requirement),
        "has_condition": check_if_needs_condition(requirement),
        "complexity": estimate_complexity(requirement)
    }
```

**Workflow 类型**:
- **Sequential** - 顺序执行（最常见）
- **Iterative** - 包含循环（create → evaluate → iterate）
- **Conditional** - 包含分支（if-then-else）
- **Parallel** - 并行执行（少见）

---

### 2. 映射步骤到 Skills

将期望的步骤映射到具体的 Skills：

```python
def map_steps_to_skills(expected_flow, available_skills):
    """
    将抽象步骤映射到具体 Skills
    """
    mapping = {}
    
    for step in expected_flow:
        # 关键词匹配
        if "collect" in step.lower():
            mapping[step] = find_skill("data-collect", available_skills)
        elif "analyze" in step.lower():
            mapping[step] = find_skill("analyze", available_skills)
        elif "generate" in step.lower():
            mapping[step] = find_skill("generate", available_skills)
        elif "notify" in step.lower():
            mapping[step] = find_skill("notify", available_skills)
        # ... 更多模式
    
    return mapping
```

---

### 3. 构建节点和边

根据分析结果构建 Workflow 结构：

```python
def build_workflow(requirement, skill_mapping):
    """
    构建 Workflow 的 nodes 和 edges
    """
    workflow = {
        "name": requirement.name,
        "nodes": {},
        "edges": []
    }
    
    # 构建节点
    for i, (step, skill) in enumerate(skill_mapping.items()):
        node_id = f"step{i+1}"
        workflow["nodes"][node_id] = {
            "type": "skill",
            "skill": skill.name,
            "input": map_inputs(step, skill, requirement)
        }
    
    # 构建边（顺序执行）
    node_ids = list(workflow["nodes"].keys())
    for i in range(len(node_ids) - 1):
        workflow["edges"].append({
            "from": node_ids[i],
            "to": node_ids[i+1]
        })
    
    # 添加结束边
    workflow["edges"].append({
        "from": node_ids[-1],
        "to": "END"
    })
    
    return workflow
```

---

### 4. 添加控制流（如果需要）

**循环**:
```python
if analysis["has_loop"]:
    add_loop_controller(workflow, max_iterations=5)
```

**条件分支**:
```python
if analysis["has_condition"]:
    add_condition_node(workflow, condition_expression)
```

---

### 5. 验证和优化

```python
def validate_workflow(workflow, available_skills):
    """
    验证 Workflow 定义是否合法
    """
    checks = {
        "all_skills_exist": check_skills_exist(workflow, available_skills),
        "no_cycles": check_no_unintended_cycles(workflow),
        "variables_valid": check_variable_references(workflow),
        "entry_exit_valid": check_entry_exit(workflow)
    }
    
    if not all(checks.values()):
        return {"valid": False, "errors": checks}
    
    return {"valid": True}
```

---

## Workflow 模板库

### 模板 1: 数据处理流程（Sequential）

```yaml
workflow:
  name: data-processing-workflow
  description: 收集 → 分析 → 生成报告
  
  nodes:
    collect:
      type: skill
      skill: data-collect-skill
      input:
        date: $workflow.input.date
    
    analyze:
      type: skill
      skill: analyze-skill
      input:
        data: $collect.output
    
    report:
      type: skill
      skill: report-skill
      input:
        analysis: $analyze.output
  
  edges:
    - from: collect
      to: analyze
    - from: analyze
      to: report
    - from: report
      to: END
  
  entry: collect
  exit: END
```

---

### 模板 2: 迭代优化流程（Iterative）

```yaml
workflow:
  name: iterative-improvement-workflow
  description: 创建 → 评价 → 迭代（直到通过）
  
  nodes:
    loop_controller:
      type: loop
      max_iterations: 5
      condition: "$evaluate.output.pass == false"
    
    create:
      type: skill
      skill: create-skill
    
    evaluate:
      type: skill
      skill: evaluate-skill
      input:
        artifact: $create.output
    
    check:
      type: condition
      expression: "$evaluate.output.pass == true"
    
    iterate:
      type: skill
      skill: iterate-skill
      input:
        artifact: $create.output
        feedback: $evaluate.output
  
  edges:
    - from: loop_controller
      to: create
      condition: "$loop.should_continue"
    
    - from: create
      to: evaluate
    
    - from: evaluate
      to: check
    
    - from: check
      to: END
      condition: true
    
    - from: check
      to: iterate
      condition: false
    
    - from: iterate
      to: loop_controller
  
  entry: loop_controller
  exit: END
```

---

### 模板 3: 条件分支流程（Conditional）

```yaml
workflow:
  name: conditional-workflow
  description: 检查 → 条件判断 → 不同路径
  
  nodes:
    check:
      type: skill
      skill: check-skill
    
    decision:
      type: condition
      expression: "$check.output.status == 'success'"
    
    success_path:
      type: skill
      skill: success-handler-skill
    
    failure_path:
      type: skill
      skill: failure-handler-skill
  
  edges:
    - from: check
      to: decision
    
    - from: decision
      to: success_path
      condition: true
    
    - from: decision
      to: failure_path
      condition: false
    
    - from: success_path
      to: END
    
    - from: failure_path
      to: END
  
  entry: check
  exit: END
```

---

## 示例

### 输入: 健康管理系统 - daily-check workflow

```yaml
requirement:
  name: daily-check
  purpose: 每日健康检查，收集数据并生成报告
  
  trigger:
    type: tick
    schedule: "21:00"
  
  expected_flow:
    - "收集今日健康数据"
    - "分析健康指标"
    - "生成每日总结"
    - "通知用户"
  
  inputs:
    date: string                    # 日期（默认今天）
  
  outputs:
    report_path: string             # 报告路径

available_skills:
  - name: data-collect-skill
    input: {date, sources}
    output: {collected_data}
  
  - name: health-indicators-skill
    input: {indicators, profile}
    output: {analysis, alerts}
  
  - name: daily-review-skill
    input: {analysis, date}
    output: {report}
  
  - name: notify-user-skill
    input: {message, path}
    output: {notified}

structure:
  data_paths:
    profile: "data/profile/profile.json"
    indicators: "data/indicators/{date}.json"
  
  output_paths:
    reports: "outputs/reports/daily/"
```

---

### 输出: daily-check workflow

```yaml
workflow:
  name: daily-check
  description: 每日健康检查流程
  version: 1.0.0
  
  input:
    date: string                    # 默认为今天
  
  output:
    report_path: string
    alerts: array
  
  nodes:
    # 步骤 1: 收集数据
    collect_data:
      type: skill
      skill: data-collect-skill
      input:
        date: $workflow.input.date
        sources:
          - "data/indicators/$workflow.input.date.json"
          - "data/profile/profile.json"
      output_to: $collected_data
    
    # 步骤 2: 分析健康指标
    analyze_indicators:
      type: skill
      skill: health-indicators-skill
      input:
        indicators: $collected_data.indicators
        profile: $collected_data.profile
      output_to: $analysis
    
    # 步骤 3: 生成每日总结
    generate_review:
      type: skill
      skill: daily-review-skill
      input:
        analysis: $analysis
        date: $workflow.input.date
      output_to: $review
    
    # 步骤 4: 通知用户
    notify_user:
      type: skill
      skill: notify-user-skill
      input:
        message: "今日健康检查完成"
        path: $review.report_path
      output_to: $notification
  
  edges:
    - from: collect_data
      to: analyze_indicators
    
    - from: analyze_indicators
      to: generate_review
    
    - from: generate_review
      to: notify_user
    
    - from: notify_user
      to: END
  
  entry: collect_data
  exit: END

metadata:
  complexity: simple
  estimated_duration: "2-3 minutes"
  dependencies:
    - data-collect-skill
    - health-indicators-skill
    - daily-review-skill
    - notify-user-skill
  
  trigger:
    type: tick
    schedule: "21:00"
  
  notes: |
    这是一个简单的顺序 Workflow，无循环无分支。
    每天晚上 9 点自动执行。
```

---

## 设计决策指南

### 何时使用循环？

**使用循环的场景**:
- 需要迭代优化（create → evaluate → iterate）
- 需要重试（失败后重试，最多 N 次）
- 需要批处理（处理多个项目）

**不使用循环的场景**:
- 简单的顺序流程
- 一次性任务
- 确定性流程

---

### 何时使用条件分支？

**使用条件的场景**:
- 根据结果选择不同路径（成功/失败）
- 根据数据特征选择处理方式
- 需要跳过某些步骤

**不使用条件的场景**:
- 所有步骤都必须执行
- 顺序固定

---

### 何时使用并行？

**使用并行的场景**:
- 多个独立任务可以同时执行（如并行调研）
- 需要加速执行
- 任务之间无依赖

**不使用并行的场景**:
- 步骤有依赖关系
- 资源限制（内存、CPU）
- 简单流程（并行增加复杂度）

---

## 变量引用规则

### 输入变量

```yaml
# Workflow 的输入参数
$workflow.input.date
$workflow.input.user_id

# 示例
input:
  date: $workflow.input.date
```

---

### 节点输出

```yaml
# 直接引用节点输出
$collect_data.output
$analyze.output.alerts

# 使用 output_to 定义的变量
$collected_data          # 如果 collect_data 有 output_to: $collected_data
$analysis               # 如果 analyze 有 output_to: $analysis
```

---

### 特殊变量

```yaml
# 循环相关
$loop.iteration         # 当前循环次数
$loop.should_continue   # 是否继续循环
$loop.should_exit       # 是否退出循环

# 上一步输出（顺序执行时）
$prev.output
```

---

## 命名规范

### Workflow 命名

- 使用 kebab-case
- 动词开头（描述动作）
- 简洁明了

**示例**:
- ✅ `daily-check`
- ✅ `weekly-report`
- ✅ `checkup-analysis`
- ❌ `DailyCheck`
- ❌ `workflow_1`

---

### 节点命名

- 使用 snake_case
- 动词 + 名词
- 自解释

**示例**:
- ✅ `collect_data`
- ✅ `analyze_indicators`
- ✅ `generate_review`
- ❌ `step1`
- ❌ `node_a`

---

## 评价标准

见 `criteria.md`

---

## 实现注意事项

### 1. 遵循 workflow-spec.md

严格按照规范定义节点和边，确保：
- 节点类型正确（skill / workflow / condition / loop / parallel）
- 变量引用语法正确
- 边定义完整

### 2. 验证 Skills 存在

引用的所有 Skills 必须在 `available_skills` 中：

```python
for node in workflow.nodes:
    if node.type == "skill":
        assert node.skill in available_skills, f"Skill {node.skill} not found"
```

### 3. 检查变量引用

确保所有变量引用都有效：

```python
# 被引用的节点必须在当前节点之前执行
if "$collect_data.output" in node.input:
    assert "collect_data" in executed_nodes
```

### 4. 避免过度设计

**原则**: 从简单开始，需要时再增加复杂度

❌ **过度设计**:
```yaml
# 只需要顺序执行 3 步，却用了循环 + 条件
```

✅ **合适设计**:
```yaml
# 顺序执行即可
collect → analyze → report
```

---

## 常见模式

### 模式 1: ETL（Extract-Transform-Load）

```
extract → transform → load
```

### 模式 2: 分析报告

```
collect_data → analyze → generate_report → notify
```

### 模式 3: 迭代优化

```
loop: create → evaluate → (pass? exit : iterate)
```

### 模式 4: 审批流程

```
submit → review → (approved? publish : reject)
```

---

## 版本历史

- v1.0.0 (2026-01-19): 初始版本
