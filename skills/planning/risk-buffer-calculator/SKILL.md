---
name: risk-buffer-calculator
description: 计算每Phase风险缓冲百分比，基于复杂度、依赖和未知因素进行启发式分析。当需要风险评估、缓冲时间规划、资源预留时使用。主要用于L3项目的严格风险管理。
stage: EXECSPEC_COMPILE
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Risk Buffer Calculator

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
> **版本**: 1.0.0 | **创建日期**: 2025-02-03

---

## 1. 描述

计算每Phase的风险缓冲百分比，为项目时长预估提供风险储备。

**核心职责**：计算风险缓冲百分比、基于复杂度和依赖因子、推荐缓冲分配策略

---

## 2. 适用场景

- **WORKFLOW Step 3 Task 3-8**: Phase规划时计算风险缓冲
- **场景A**: L3项目需要严格风险管理
- **场景B**: 高依赖项目需要缓冲时间

**对应**: Build_Exec_Spec_Plans Step 4 (Phase规划，风险缓冲)

---

## 3. 输入

- `spec/build/dependency_graph.md` - 依赖分析
- `spec/spec_artifacts_registry.md` - 从Registry查询VS数量
- `spec/build/scaffold_analysis_report.md` - 外部服务依赖

---

## 4. 输出

- `spec/build/risk_buffer_allocation.md` - 风险缓冲分配

---

## 5. 执行步骤

1. Read dependency_graph.md, count external API dependencies
2. Read spec_artifacts_registry.md, query VS count from DESIGN section
3. Calculate complexity_factor:
   - VS_Count > 10 → +5%, >20 → +10%
4. Calculate dependency_factor:
   - External_APIs > 3 → +5%, >5 → +10%
5. Calculate buffer% = Base(10%) + complexity_factor + dependency_factor
6. Adjust by SPEC level:
   - L1: 固定10%
   - L2: 10-15% (简单计算)
   - L3: 15-25% (综合分析)
7. Write risk_buffer_allocation.md

---

## 6. 快速开始

1. 开发者确保dependency_graph.md已生成
2. 调用: `///risk-buffer-calculator`（并明确 Level: L3）
3. 查看: `spec/build/risk_buffer_allocation.md`
4. 预计耗时: 2-3分钟

---

## 7. 使用说明

**输入要求**: dependency_graph.md需包含外部依赖标注

**输出格式** (`spec/build/risk_buffer_allocation.md`包含):
- **每Phase计算**: 基础缓冲(10%) + 复杂度因子 + 依赖因子 = 总缓冲百分比
- **建议预留时间**: 基于Phase预估时长计算具体小时数
- **L1固定**: L1级别统一10%，不进行复杂计算

---

## 8. 价值

- **SPEC组织**: 科学化风险预估
- **PM/BA**: 真实项目周期预估
- **Dev**: 缓冲时间指导

---

## 9. 质量检查

- [ ] 缓冲百分比在合理范围（10-25%）
- [ ] 每个Phase有单独计算
- [ ] 建议预留时间已提供

---

## 10. 限制条件

- **启发式**: 基于简单规则，不是精确模型
- **L1固定**: L1级别固定10%，不进行复杂计算

---

## 相关 SKILLs

- **前置**: dependency-graph-generator
- **并行**: integration-window-planner
- **后续**: 无

---
