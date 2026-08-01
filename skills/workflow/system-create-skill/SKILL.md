---
name: system-create-skill
description: '用途: 创建一个完整的 System/Project'
---

# system-create-skill

**用途**: 创建一个完整的 System/Project

**触发**: 当用户表达想要创建一个系统时（如："创建一个健康管理系统"）

**核心理念**:
- 人只说意图，AI 自己设计
- 做选择题，不做填空题
- 问最关键的一题（最大信息增益）

---

## Workflow 定义

这是一个完整的 Workflow，演示了：
- 条件分支
- 循环迭代
- Workflow 嵌套
- 判别式交互

```yaml
workflow:
  name: system-create-skill
  description: 创建一个完整的 System/Project
  version: 1.0.0

  input:
    user_intent: string  # 用户的模糊意图

  output:
    system_path: string  # 创建的系统路径
    summary: object      # 系统摘要

  # ========================================
  # 节点定义
  # ========================================
  nodes:

    # ────────────────────────────────────
    # 阶段 1: 快速澄清（最大信息增益）
    # ────────────────────────────────────
    clarify_intent:
      type: skill
      skill: clarify-skill
      input:
        question: $workflow.input.user_intent
        mode: "multiple_choice"
        strategy: "max_information_gain"
      output_to: $clarified_requirements

    # ────────────────────────────────────
    # 阶段 2: 自主设计
    # ────────────────────────────────────
    design_system:
      type: workflow
      workflow: system-design-workflow
      input:
        requirements: $clarified_requirements
      output_to: $design_plan

    # ────────────────────────────────────
    # 阶段 3: 展示方案（判别式确认）
    # ────────────────────────────────────
    show_plan:
      type: skill
      skill: user-confirm-skill
      input:
        content: $design_plan
        format: "visual_summary"
        question: "这个方案符合你的预期吗？需要调整哪里？"
      output_to: $user_feedback

    # ────────────────────────────────────
    # 条件判断：是否通过
    # ────────────────────────────────────
    check_approval:
      type: condition
      expression: "$user_feedback.approved == true"

    # ────────────────────────────────────
    # 分支 A: 执行创建
    # ────────────────────────────────────
    execute_creation:
      type: workflow
      workflow: system-execute-workflow
      input:
        plan: $design_plan
      output_to: $execution_result

    # ────────────────────────────────────
    # 分支 B: 调整设计
    # ────────────────────────────────────
    adjust_design:
      type: skill
      skill: iterate-skill
      input:
        artifact: $design_plan
        feedback: $user_feedback.comments
      output_to: $adjusted_plan

    # ────────────────────────────────────
    # 循环控制器
    # ────────────────────────────────────
    iteration_controller:
      type: loop
      max_iterations: 3
      condition: "$user_feedback.approved == false"

    # ────────────────────────────────────
    # 阶段 5: 验证结果
    # ────────────────────────────────────
    validate_result:
      type: skill
      skill: user-confirm-skill
      input:
        content: $execution_result
        format: "file_list_with_summary"
        question: "试用一下，有没有不符合预期的地方？"
      output_to: $validation_feedback

    # ────────────────────────────────────
    # 最终检查
    # ────────────────────────────────────
    final_check:
      type: condition
      expression: "$validation_feedback.satisfied == true"

    # ────────────────────────────────────
    # 如果不满意：记录反馈
    # ────────────────────────────────────
    log_feedback:
      type: skill
      skill: log-skill
      input:
        message: "System created but user requested improvements"
        data: $validation_feedback

  # ========================================
  # 边定义（控制流）
  # ========================================
  edges:
    # 主流程
    - from: clarify_intent
      to: design_system

    - from: design_system
      to: show_plan

    - from: show_plan
      to: check_approval

    # 条件分支
    - from: check_approval
      to: execute_creation
      condition: true

    - from: check_approval
      to: adjust_design
      condition: false

    # 循环：调整后重新进入设计
    - from: adjust_design
      to: iteration_controller

    - from: iteration_controller
      to: design_system
      condition: "$loop.should_continue"

    - from: iteration_controller
      to: execute_creation
      condition: "$loop.should_exit"  # 超过最大次数，强制执行

    # 验证流程
    - from: execute_creation
      to: validate_result

    - from: validate_result
      to: final_check

    - from: final_check
      to: END
      condition: true

    - from: final_check
      to: log_feedback
      condition: false

    - from: log_feedback
      to: END

  # ========================================
  # 入口和出口
  # ========================================
  entry: clarify_intent
  exit: END
```

---

## 子 Workflow: system-design-workflow

```yaml
workflow:
  name: system-design-workflow
  description: 设计系统的详细方案

  input:
    requirements: object  # 澄清后的需求

  output:
    design_plan: object   # 设计方案

  nodes:
    # 调研最佳实践
    research:
      type: skill
      skill: research-skill
      input:
        topic: $workflow.input.requirements.domain
        focus: "best_practices, patterns, tools"

    # 制定计划
    plan:
      type: skill
      skill: plan-skill
      input:
        goal: $workflow.input.requirements
        knowledge: $research.output

    # 设计目录结构
    design_structure:
      type: skill
      skill: structure-design-skill
      input:
        plan: $plan.output

    # 设计 Workflows
    design_workflows:
      type: skill
      skill: workflow-define-skill
      input:
        requirements: $workflow.input.requirements
        structure: $design_structure.output

    # 设计 Skills
    design_skills:
      type: skill
      skill: domain-skill-design
      input:
        workflows: $design_workflows.output
        structure: $design_structure.output

    # 设计 Agents（如果需要）
    design_agents:
      type: skill
      skill: agent-define-skill
      input:
        skills: $design_skills.output
        workflows: $design_workflows.output

    # 汇总方案
    synthesize:
      type: skill
      skill: synthesize-skill
      input:
        structure: $design_structure.output
        workflows: $design_workflows.output
        skills: $design_skills.output
        agents: $design_agents.output

  edges:
    - from: research
      to: plan
    - from: plan
      to: design_structure
    - from: design_structure
      to: design_workflows
    - from: design_workflows
      to: design_skills
    - from: design_skills
      to: design_agents
    - from: design_agents
      to: synthesize
    - from: synthesize
      to: END

  entry: research
  exit: END
```

---

## 子 Workflow: system-execute-workflow

```yaml
workflow:
  name: system-execute-workflow
  description: 执行创建系统的文件和代码

  input:
    plan: object  # 设计方案

  output:
    result: object  # 执行结果

  nodes:
    # 创建目录结构
    create_structure:
      type: skill
      skill: create-file
      input:
        plan: $workflow.input.plan.structure

    # 创建 Workflows
    create_workflows:
      type: skill
      skill: create-file
      input:
        files: $workflow.input.plan.workflows

    # 创建 Skills
    create_skills:
      type: skill
      skill: create-skill
      input:
        specs: $workflow.input.plan.skills

    # 创建 Agents
    create_agents:
      type: skill
      skill: create-file
      input:
        files: $workflow.input.plan.agents

    # 创建 README 和文档
    create_docs:
      type: skill
      skill: create-file
      input:
        files: $workflow.input.plan.docs

    # 汇总结果
    summarize:
      type: skill
      skill: summarize-skill
      input:
        created_files:
          - $create_structure.output
          - $create_workflows.output
          - $create_skills.output
          - $create_agents.output
          - $create_docs.output

  edges:
    - from: create_structure
      to: create_workflows
    - from: create_workflows
      to: create_skills
    - from: create_skills
      to: create_agents
    - from: create_agents
      to: create_docs
    - from: create_docs
      to: summarize
    - from: summarize
      to: END

  entry: create_structure
  exit: END
```

---

## 执行示例

### 用户输入
```
"我想要一个健康管理系统"
```

### 执行流程

#### 1. clarify_intent（澄清意图）

**Claude 输出**:
```
我理解你想要健康管理系统。为了给你最合适的方案，我需要了解:

你想要的健康管理系统，最核心的目标是什么？

A. 预防疾病
   - 定期体检报告分析
   - 健康指标追踪
   - 风险预警

B. 提升体能
   - 运动计划和追踪
   - 进度可视化
   - 目标管理

C. 改善习惯
   - 饮食记录和分析
   - 睡眠质量追踪
   - 行为养成提醒

D. 慢病管理
   - 血糖/血压监测
   - 用药提醒
   - 医生沟通记录

你倾向哪个？或者需要组合？
```

**用户回答**: `A`

**澄清结果**:
```json
{
  "domain": "health_management",
  "focus": "disease_prevention",
  "key_features": [
    "checkup_analysis",
    "health_indicators_tracking",
    "risk_assessment"
  ],
  "interaction_frequency": "daily"
}
```

---

#### 2. design_system（自主设计）

**执行**:
- research-skill: 调研健康管理最佳实践
- plan-skill: 制定实施计划
- design_structure: 设计目录结构
- design_workflows: 设计 3 个核心 Workflows
- design_skills: 设计 8 个 Skills
- design_agents: 设计 1 个 Agent

**设计方案**:
```yaml
system_name: health-system
structure:
  - .claude/
    - agents/
      - health-advisor.md
    - skills/
      - checkup-analysis/
      - health-indicators/
      - risk-assessment/
      - daily-review/
      - weekly-report/
    - workflows/
      - daily-check.yaml
      - weekly-report.yaml
      - checkup-analysis.yaml
  - data/
    - profile.json
    - indicators/
    - checkups/
  - outputs/
    - reports/

workflows:
  - name: daily-check
    trigger: tick (21:00)
    steps: [collect_data, analyze, generate_report, notify]

  - name: weekly-report
    trigger: tick (Sunday 20:00)
    steps: [aggregate_week, analyze_trends, generate_insights, notify]

  - name: checkup-analysis
    trigger: event (file_uploaded)
    steps: [parse_report, compare_history, assess_risks, generate_recommendations]

skills:
  - checkup-analysis-skill
  - health-indicators-skill
  - risk-assessment-skill
  - daily-review-skill
  - weekly-report-skill
  - data-collect-skill
  - trend-analysis-skill
  - notify-user-skill

agents:
  - health-advisor (专长: checkup-analysis, risk-assessment, health-indicators)
```

---

#### 3. show_plan（展示方案）

**Claude 输出**:
```
我已经完成设计！这是方案摘要：

📁 系统结构:
  - 1 个 Agent（健康顾问）
  - 8 个 Skills（体检分析、指标追踪等）
  - 3 个 Workflows（每日检查、每周报告、体检分析）

🔄 核心流程:
  ① 每天 21:00 自动检查当日数据，生成健康提醒
  ② 每周日汇总本周情况，分析趋势
  ③ 上传体检报告时，自动分析并更新健康档案

📊 数据管理:
  - 个人档案：基础信息、病史
  - 指标记录：按日期存储
  - 报告输出：Markdown 格式

这个方案符合你的预期吗？需要调整哪里？

[详细设计方案已保存到: .sop-engine/temp/design-plan.yaml]
```

**用户回答**: `看起来不错，可以开始创建`

---

#### 4. execute_creation（执行创建）

**执行**:
- 创建目录结构
- 创建 3 个 Workflow YAML 文件
- 创建 8 个 Skill（每个包含 SKILL.md + criteria.md）
- 创建 1 个 Agent
- 创建 README.md 和 DESIGN.md

**结果**:
```
✅ 系统创建完成！

📁 health-system/
  ├── .claude/
  │   ├── agents/health-advisor.md
  │   ├── skills/ (8 个)
  │   └── workflows/ (3 个)
  ├── data/
  │   ├── profile.json (示例)
  │   └── indicators/
  ├── outputs/
  └── README.md

🚀 下一步:
  1. 填写 data/profile.json（你的基本信息）
  2. 试用: "执行每日健康检查"
  3. 上传体检报告测试分析功能
```

---

#### 5. validate_result（验证）

**Claude**:
```
试用一下，有没有不符合预期的地方？

如果需要调整，告诉我具体哪里需要改进。
```

---

## 需要的新 Skills

为了让这个 Workflow 工作，我们需要创建以下新 Skills：

### 高优先级
1. **user-confirm-skill** - 判别式确认
2. **structure-design-skill** - 设计目录结构
3. **domain-skill-design** - 设计领域 Skills
4. **synthesize-skill** - 汇总信息
5. **summarize-skill** - 总结结果

### 中优先级
6. **workflow-define-skill** - 定义 Workflow（已在 TODO）
7. **agent-define-skill** - 定义 Agent（已在 TODO）

---

## 评价标准

见 `criteria.md`

---

## 使用方式

### 触发
```
用户: "创建一个健康管理系统"
Claude: [自动触发 system-create-skill]
```

### 预期时长
- 快速澄清: 1-2 轮对话
- 自主设计: 自动执行（2-3 分钟）
- 展示确认: 1 轮对话
- 执行创建: 自动执行（1-2 分钟）
- 验证: 1 轮对话

总计: **约 5-10 分钟，3-5 轮对话**

---

## 实现策略

### 使用 loop-skill

由于我们遵循 **"skill 和文件是一等公民"** 原则，实际执行时：

1. **system-create-skill** 本身是一个 Skill
2. 它内部调用 **loop-skill** 来实现循环
3. 使用文件存储状态（.sop-engine/running/）

### 状态文件

```
.sop-engine/running/system-create-20260119-001/
├── state.json          # 当前阶段
├── context.json        # 所有变量
└── logs/
    ├── clarify.log
    ├── design.log
    └── execute.log
```

---

## 版本历史

- v1.0.0 (2026-01-19): 初始版本
