---
name: dependency-graph-generator
description: 生成GOAL/SubPlan依赖DAG和关键路径分析，并执行SubPlan划分。当需要分析技术依赖、业务依赖、识别关键路径、发现并行执行机会、执行SubPlan分配时使用。基于GOAL的dependencies字段和业务逻辑分析生成Mermaid依赖图和SubPlan划分方案。
stage: EXECSPEC_COMPILE
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Dependency Graph Generator

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
> **版本**: 1.0.0 | **创建日期**: 2025-02-03

---

## 1. 描述

生成GOAL/SubPlan依赖关系的有向无环图（DAG），执行SubPlan划分，识别关键路径和并行执行机会。

**核心职责**：分析技术依赖、业务依赖、生成Mermaid图、识别关键路径、建议并行执行、执行SubPlan划分与编号

---

## 2. 适用场景

- **WORKFLOW Step 3 Task 3-4**: Phase规划时分析依赖关系和SubPlan划分
- **场景A**: 多个GOAL之间有依赖，需要确定执行顺序
- **场景B**: L3项目需要并行执行优化
- **场景C**: 需要将GOAL分配到SubPlan（Step 3核心任务）

**对应**: Build_Exec_Spec_Plans Step 3 (SubPlan划分与编号) + Step 4 (Phase规划，依赖排序)

---

## 3. 输入

- `spec/spec_artifacts_registry.md` - 从Registry查询GOAL清单
- GOAL front matter dependencies字段

---

## 4. 输出

- `spec/build/dependency_graph.md` - Mermaid依赖图
- 关键路径分析
- 并行执行建议
- SubPlan划分方案（GOAL→SubPlan映射表）
- SubPlan编号（Phase_X.SubPlan_Y格式）

---

## 5. 执行步骤

1. Read all GOAL files, extract id and dependencies from front matter
2. Build dependency graph (adjacency list)
3. Detect cycles (if found, report error and suggest fix)
4. Generate Mermaid diagram (graph TD format)
5. Calculate critical path using topological sort
6. Identify parallel groups (GOALs with no dependencies between them)
7. Generate SubPlan partitioning based on dependency clustering:
   - Group GOALs with tight dependencies into same SubPlan
   - Keep SubPlan size reasonable (L1: 3-5 GOALs/SubPlan, L2: 4-6, L3: 5-8)
   - Ensure SubPlan boundaries align with natural breakpoints
8. Assign SubPlan numbers (Phase_1.SubPlan_1, Phase_1.SubPlan_2...)
9. Output GOAL→SubPlan mapping table
10. Write all outputs to dependency_graph.md

---

## 6. 快速开始

1. 开发者确保所有GOAL的front matter包含dependencies字段
2. 调用: `///dependency-graph-generator`
3. 查看: `spec/build/dependency_graph.md`
4. 预计耗时: 3-5分钟

---

## 7. 使用说明

**输入要求**: GOAL front matter必须包含dependencies字段（可为空数组）

**输出格式** (`spec/build/dependency_graph.md`包含):
- **Mermaid Diagram**: graph TD格式的依赖图
- **Critical Path**: 最长路径和估算时长
- **Parallel Groups**: 可并行执行的GOAL分组（L2+）
- **SubPlan划分方案**: SubPlan与GOALs映射表（含分组理由）
- **GOAL→SubPlan映射表**: 每个GOAL的分配结果和依赖关系

---

## 8. 价值

- **SPEC组织**: 可视化依赖，避免循环依赖
- **PM/BA**: 理解业务执行顺序
- **Dev**: 识别并行机会，优化执行效率

---

## 9. 质量检查

- [ ] 依赖图已生成（Mermaid格式）
- [ ] 无循环依赖
- [ ] 关键路径已识别
- [ ] 并行组已建议（L2+）
- [ ] SubPlan划分方案已输出
- [ ] GOAL→SubPlan映射表已生成

---

## 10. 限制条件

- **不支持**: 动态依赖（运行时决定）
- **最大规模**: 100个GOAL
- **依赖**: 需要GOAL文件包含dependencies字段

---

## 相关 SKILLs

- **前置**: 无（GOAL文件已存在）
- **并行**: constraints-generator
- **后续**: round-planning

---
