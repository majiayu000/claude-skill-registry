---
name: special-directives
description: 紧急旨意与皇上直令(imperial_direct)处理流程。适用：太子收到加急旨意或皇上直令时
---

# Skill: 特殊指令处理

> **适用 Agent**：太子、中书省、尚书省、被指定 Agent
> **加载时机**：加急旨意到达时；皇上下达 `imperial_direct` 时

## 紧急旨意（加急件）

皇上标注为紧急（或太子判断为紧急）的旨意：

- 中书省简化方案，门下省快速审议（可合并为中书直审）
- 尚书省即刻派发，六部优先处理
- 回奏频率提高，可阶段性回奏而非等全部完成

## 皇上直令

皇上可绕过三省流程，直接对特定 Agent 下达指令：

- 此类指令标记为 `imperial_direct`，由太子（Lead）通过 SendMessage 转发至目标 Teammate
- 对应 Teammate 必须立即执行
- 执行完成后仍需回奏尚书省备案

### imperial_direct 临时通信授权

常规通信权限矩阵（governance-core §三）中，太子对六部的通信路径为 —（禁止）。`imperial_direct` 场景下需临时开通，核心原则：太子确认指令合法性后激活，授权仅限太子与被指定 Agent 之间，默认超时 30 分钟（上限 60 分钟），终止后须向尚书省备案供门下审计。

> 超时处置规则详见 `fault-tolerance-tables.md`（三省间超时处置表）

> 📎 完整授权规则（触发条件、授权范围、时效、恢复与备案）见 `imperial-direct-protocol.md`
