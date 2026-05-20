---
name: analysis-framework
description: 中书省规划框架与门下省审议/简审清单。适用：中书接旨规划时、门下审议时
---

# Skill: 分析决策指南

> **适用 Agent**：中书省、门下省、尚书省
> **加载时机**：中书接到旨意时；门下准备审议时

## 中书省分析框架

中书省收到旨意后，必须按以下步骤分析：

```
1. 【意图识别】皇上真正想要什么？ → 区分表面需求与深层目标
2. 【范围界定】涉及哪些模块/系统？ → 画出影响范围
3. 【路径选择】有哪些实现方案？    → 列出至少两种方案并对比
4. 【复杂度评估】工作量与难度？    → 标注优先级与资源需求
5. 【风险预判】可能出什么问题？    → 识别技术风险与依赖风险
6. 【任务拆解】怎么分步执行？      → 拆解为原子任务，标注依赖
7. 【并行分组】哪些任务可同时进行？→ 分析依赖关系，标注 parallel_group 与 depends_on
8. 【验收定义】怎么算完成？        → 为每个子任务定义 Done 标准
```

## 中书省草案输出格式

```json
{
  "plan_id": "PLAN-...",
  "objective": "...",
  "subtasks": [
    { "id": "T-001", "assigned_to": "gongbu", "parallel_group": "A", "description": "..." },
    { "id": "T-002", "assigned_to": "xingbu", "depends_on": ["T-001"], "parallel_group": "B", "description": "..." }
  ],
  "acceptance_criteria": [],
  "risk_notes": "..."
}
```

- 同一 `parallel_group` 的任务可跨部门并行启动
- `depends_on` 标注串行依赖，必须前序完成后才派发
- 并行分组的分析粒度：**任务级**——哪些任务可以同时开始

## 门下省审议清单

门下省审议以**结构化检查为主、主观判断为辅**，分结构化检查（必查）、判断性检查（按需）、fast_track 简审三类。

> 📎 详细规则见 `analysis-checklists.md`
