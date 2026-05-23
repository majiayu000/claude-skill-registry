---
name: integration-window-planner
description: 规划集成窗口位置和验证策略。当需要在Phase之间或SubPlan之间安排集成窗口、定义集成验证策略、生成集成清单（API契约/数据流/E2E测试）时使用。主要用于L2/L3项目。
stage: EXECSPEC_COMPILE
level_supported: [L2-BALANCED, L3-RIGOROUS]
---

# Integration Window Planner

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
> **版本**: 1.0.0 | **创建日期**: 2025-02-03

---

## 1. 描述

规划集成窗口位置和验证策略，确保模块间集成质量。

**核心职责**：规划集成窗口位置、定义集成验证策略、生成集成清单

---

## 2. 适用场景

- **WORKFLOW Step 3 Task 3-7**: Phase规划时安排集成窗口（L2/L3）
- **场景A**: 多模块项目需要集成验证
- **场景B**: 外部API集成需要专门窗口

**对应**: Build_Exec_Spec_Plans Step 4 (Phase规划，集成窗口安排)

---

## 3. 输入

- `spec/build/dependency_graph.md` - Phase划分
- SPEC级别 (L2/L3)

---

## 4. 输出

- `spec/build/integration_windows.md` - 集成窗口规划
- 集成清单（API契约、数据流、E2E测试）

---

## 5. 执行步骤

1. Read dependency_graph.md, identify Phase boundaries
2. Based on SPEC level:
   - L2: Plan 1-2 integration windows (after major phases)
   - L3: Plan 3-4 integration windows (after each phase)
3. For each integration window:
   - Define position (after which Phase)
   - Define validation strategy (regression tests, E2E tests)
   - Generate integration checklist (API contracts, data flow, external services)
4. Write integration_windows.md

---

## 6. 快速开始

1. 开发者确保dependency_graph.md已生成
2. 调用: `///integration-window-planner`（并明确 Level: L2）
3. 查看: `spec/build/integration_windows.md`
4. 预计耗时: 3-5分钟

---

## 7. 使用说明

**输入要求**: dependency_graph.md需包含Phase划分

**输出格式** (`spec/build/integration_windows.md`包含):
- **每个窗口**: Position（在哪个Phase后）、Validation清单（API契约/数据流/E2E测试）、Duration估算
- **数量**: L2推荐1-2个窗口，L3推荐3-4个窗口

---

## 8. 价值

- **SPEC组织**: 明确集成验证策略
- **PM/BA**: 了解集成风险点
- **Dev**: 集成清单指导，避免遗漏

---

## 9. 质量检查

- [ ] 集成窗口数量合理（L2: 1-2, L3: 3-4）
- [ ] 每个窗口有明确validation清单
- [ ] Duration估算已提供

---

## 10. 限制条件

- **仅L2/L3**: L1不需要集成窗口（持续集成）
- **依赖**: 需要dependency_graph.md已生成

---

## 相关 SKILLs

- **前置**: dependency-graph-generator
- **并行**: round-planning
- **后续**: progress-tracking

---
