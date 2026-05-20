---
name: token-optimization
description: 尚书省首次调用时加载的 Token 优化策略，定义运行模式拆分、会话复用与上下文管理
---

# Skill: Token 优化策略

> **适用 Agent**：尚书省、系统层
> **加载时机**：尚书省首次调用时（了解自身运行模式）

## 尚书省运行模式

尚书省按职责阶段切换运行模式，每种模式仅加载当前阶段所需的系统提示：

| 运行模式 | 触发条件 | 加载内容 |
|---------|---------|---------|
| **dispatch** | 收到 `approved_plan` | 核心身份 + Skill `dispatch_rules` |
| **coordinate** | 六部执行中，需协调或汇总 | 核心身份 + Skill `communication_protocols` + Skill `fault_tolerance` |
| **report** | 门下覆奏通过 | 核心身份 + Skill `report_format` |

## 会话复用

同一 `plan_id` 生命周期内，Agent 多次调用复用同一会话，后续调用以追加消息继续对话。

## 上下文摘要

会话上下文 ≥ 模型窗口 70% 时，Agent 自动生成摘要，以「核心身份 + 摘要」开启新会话。摘要须包含：当前阶段、关键决策、待办事项、阻塞项、各子任务状态。

## 约束

1. 会话复用仅限同一 `plan_id`
2. 摘要由 Agent 自身生成
3. 异常时回退为独立会话模式
