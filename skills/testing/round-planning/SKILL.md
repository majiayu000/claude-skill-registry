---
name: round-planning
description: 规划Red/Green/Refactor Round节奏，估算Round数量和执行时间。当需要规划TDD周期、估算Round数、分配测试用例到Round、评估执行时长时使用。基于TS数量和复杂度进行启发式估算。
stage: EXECSPEC_COMPILE
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Round Planning

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
> **版本**: 1.0.0 | **创建日期**: 2025-02-03

---

## 1. 描述

规划TDD Round节奏和执行时长，基于测试场景数量和复杂度进行估算。

**核心职责**：估算Round数量、规划Red/Green/Refactor比例、估算执行时间、建议容量分配

---

## 2. 适用场景

- **WORKFLOW Step 3 Task 3-5**: Round Plan生成
- **场景A**: 需要估算项目执行时长
- **场景B**: 需要分配测试场景到Round

**对应**: Build_Exec_Spec_Plans Step 7 (Round Plan生成)

---

## 3. 输入

- `spec/implementation/bdd_test_scenarios_file` - 测试场景清单
- SPEC级别 (L1/L2/L3)
- `spec/build/dependency_graph.md` (SubPlan划分)

---

## 4. 输出

- `spec/build/round_estimation.md` - Round估算报告
- 每SubPlan的Round数量
- 预估总执行时间

---

## 5. 执行步骤

1. Read bdd_test_scenarios_file, count total TS (Test Scenarios)
2. Calculate Avg_TS_Per_Round based on SPEC level (L1: 8-12, L2: 5-8, L3: 3-5)
3. Calculate Round_Count = ceil(TS_Count / Avg_TS_Per_Round)
4. Estimate time per Round (L1: 30-60min, L2: 45-90min, L3: 60-120min)
5. Calculate total execution time = Round_Count × Avg_Time_Per_Round
6. Generate Red/Green/Refactor ratio (40%/40%/20%)
7. Write round_estimation.md

---

## 6. 快速开始

1. 开发者确保bdd_test_scenarios_file已生成
2. 调用: `///round-planning`（并明确 Level: L1）
3. 查看: `spec/build/round_estimation.md`
4. 预计耗时: 2-3分钟

---

## 7. 使用说明

**输入要求**: bdd_test_scenarios_file需包含至少3个TS

**输出格式** (`spec/build/round_estimation.md`包含):
- **每SubPlan估算**: TS数量、Round数、预估时长范围
- **总体估算**: 总Round数、总时长、Red/Green/Refactor比例(40%/40%/20%)

---

## 8. 价值

- **SPEC组织**: 项目时长预估，资源规划
- **PM/BA**: 了解交付周期
- **Dev**: Round分配指导，避免Round过大或过小

---

## 9. 质量检查

- [ ] Round数量合理（不超过20 Rounds/SubPlan）
- [ ] 时长估算包含范围（最小-最大）
- [ ] Red/Green/Refactor比例已定义

---

## 10. 限制条件

- **不支持**: 动态调整（需手动修改估算）
- **依赖**: 需要bdd_test_scenarios_file已生成

---

## 相关 SKILLs

- **前置**: 无（TS文件已存在）
- **并行**: dependency-graph-generator
- **后续**: 无（Dashboard 在 Master Plan 生成时自动创建）

---
