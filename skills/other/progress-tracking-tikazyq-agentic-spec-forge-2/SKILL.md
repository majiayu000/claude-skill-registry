---
name: progress-tracking
description: 监控执行计划的进度和健康状态，跟踪 SubPlan 完成度和 Round 执行状态，识别阻塞点并同步 Dashboard。当需要检查执行进度、更新 Round 状态、记录阻塞项、生成进度报告、计算进度偏差、分析趋势、预测完成日期时使用。支持资源消耗跟踪、风险状态更新、燃尽图分析和利益相关者报告生成。
stage: EXECSPEC_COMPILE
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Progress Tracking Skill

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
>
> **版本**: 0.1.0（占位）| **创建日期**: 2025-11-27

---

## 概述

Progress Tracking 监控执行计划的进度和健康状态：

```
┌─────────────────────────────────────────────────────┐
│              📈 Progress Tracking                   │
├─────────────────────────────────────────────────────┤
│  SubPlan 状态 → Round 进度 → 阻塞识别 → 报告生成   │
│  (Completion)  (TDD Status) (Blockers)  (Dashboard)│
└─────────────────────────────────────────────────────┘
```

**核心职责**：
- 监控 SubPlan 完成度 (`{{COMPLETED}}/{{TOTAL}}`)
- 跟踪 Round 执行状态 (RED/GREEN/REFACTOR)
- 识别阻塞点和风险项
- 同步 Dashboard Progress Snapshot

---

## L1-STREAMLINED

### 检查清单

- [ ] SubPlan 完成数量与 MasterPlan 索引一致
- [ ] 每个 SubPlan 的 Round 状态已更新
- [ ] 阻塞项已记录到 Dashboard（状态标记为 blocked）
- [ ] Dashboard Progress Snapshot 已同步

### 通过标准

- 4 项全部通过（100%）
- 或 4 项中 3 项通过（≥75%）

---

## L2-BALANCED

### 检查清单

- [ ] SubPlan 完成数量与 MasterPlan 索引一致
- [ ] 每个 SubPlan 的 Round 状态已更新
- [ ] 阻塞项已记录到 Dashboard（状态标记为 blocked）
- [ ] Dashboard Progress Snapshot 已同步
- [ ] 进度偏差已计算（实际 vs 计划）
- [ ] 资源消耗已跟踪（人力/时间）
- [ ] 风险项已更新状态

### 通过标准

- 7 项全部通过（100%）
- 或 7 项中 6 项通过（≥85.7%）

---

## L3-RIGOROUS

### 检查清单

- [ ] SubPlan 完成数量与 MasterPlan 索引一致
- [ ] 每个 SubPlan 的 Round 状态已更新
- [ ] 阻塞项已记录到 Dashboard（状态标记为 blocked）
- [ ] Dashboard Progress Snapshot 已同步
- [ ] 进度偏差已计算（实际 vs 计划）
- [ ] 资源消耗已跟踪（人力/时间/成本）
- [ ] 风险项已更新状态
- [ ] 趋势分析已生成（燃尽图/速度图）
- [ ] 预测完成日期已更新
- [ ] 利益相关者报告已生成
- [ ] 偏差根因分析已完成（如适用）

### 通过标准

- 11 项全部通过（100%）
- 或 11 项中 10 项通过（≥90.9%）

---

## `///` 命令

```
///progress-tracking
```

---

## 阻塞点识别规则

### 阻塞信号

| 信号 | 严重度 | 行动 |
|------|--------|------|
| Round 停留 RED > 2 小时 | 🟡 警告 | 检查测试设计 |
| SubPlan 进度 < 50% 但时间 > 70% | 🔴 严重 | 立即评审 |
| 依赖 SubPlan 未完成 | 🔴 阻塞 | 调整顺序 |
| 集成测试持续失败 | 🔴 严重 | 回滚检查 |

### 报告模板

```markdown
## Progress Snapshot - {{DATE}}

### 总体进度
- Phase: {{CURRENT_PHASE}}/{{TOTAL_PHASE}}
- SubPlan: {{COMPLETED_SUBPLAN}}/{{TOTAL_SUBPLAN}}

### 当前状态
- 活跃 SubPlan: {{ACTIVE_SUBPLAN}}
- Round 状态: {{RED|GREEN|REFACTOR}}

### 阻塞项
- [ ] {{BLOCKER_DESCRIPTION}}

### 下一步
- {{NEXT_ACTION}}
```

---

## 相关 Skills

- **前置**: phase-planning（Phase 已规划）
- **并行**: tdd-cycle（TDD 执行中）
- **工具**: milestone-planning（里程碑检查）

---

**TODO**: 待细化检查逻辑和自动化报告生成
