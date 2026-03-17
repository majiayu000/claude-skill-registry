---
name: constraints-generator
description: 生成ExecSpecMasterConstraints_L*.md权威约束文件，定义Phase/SubPlan/Round命名规范、目录结构、环境策略和质量门禁阈值。当需要创建 ExecSpec Master Plan 的约束文档、定义命名规范、定义质量门禁、定义HITL检查点时使用。
stage: EXECSPEC_COMPILE
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Constraints Generator

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
>
> **版本**: 1.0.0 | **创建日期**: 2025-02-03

---

## 1. 描述

Constraints Generator 生成权威约束文件，定义 ExecSpec 通路（编译 + 落实）的所有规范和阈值。

**核心职责**：
- 生成ExecSpecMasterConstraints_L*.md（L1/L2/L3）
- 定义Phase/SubPlan/Round命名规范
- 定义目录结构（_exec_specs/）
- 定义环境策略和质量门禁阈值
- 定义HITL检查点和升级策略

**Why**：
- ExecSpec 通路需要统一的规范和约束
- 避免命名混乱（Phase_1 vs phase-1）
- 明确质量标准（代码覆盖率阈值、测试通过率）
- 权威文档，所有SubPlan必须引用

---

## 2. 适用场景

- **WORKFLOW Step 3 Task 3-3**: 编译 ExecSpec Master Plan 时，生成约束文件
- **场景A**: 新项目启动，需要定义Build规范
- **场景B**: 多SubPlan执行，需要统一命名和目录结构
- **场景C**: 质量门禁配置，需要明确阈值

**对应 Build_Exec_Spec_Plans**: Step 5 (约束文件生成)

---

## 3. 输入

- SPEC级别（L1/L2/L3）
- `spec/build/scaffold_analysis_report.md`（项目类型、测试框架）
- `spec/build/environment_config_checklist.md`（环境策略）

---

## 4. 输出

- `_exec_specs/ExecSpecMasterConstraints_L1.md`（或L2/L3）

**文件包含6个核心章节**:
1. 命名规范（Phase/SubPlan/Round格式）
2. 目录结构（_exec_specs/布局）
3. 环境策略（dev/test/staging/prod分层）
4. 质量门禁（代码覆盖率/测试通过率阈值）
5. HITL检查点（L2/L3）
6. 升级策略（L2/L3）

---

## 5. 执行步骤

### Step 1: 确定SPEC级别

```
Read SPEC level input (L1/L2/L3)
Load level-specific templates:
  - L1: STREAMLINED (最小配置)
  - L2: BALANCED (标准配置)
  - L3: RIGOROUS (完整配置)
```

### Step 2: 生成命名规范章节

```
Define naming rules:
  - Phase: Phase_{{N}}
  - SubPlan: {{Phase}}.SubPlan_{{N}}
  - Round: Round_{{N}}_{{Stage}}
  - Integration: INTEGRATION_PHASE, INTEGRATION_FINAL

Generate examples for each rule
```

### Step 3: 生成目录结构章节

```
Define _exec_specs/ structure:
  - Master-level files (Plan/Constraints/Dashboard)
  - SubPlan files (ExecSpecSubPlan_*.md)

Generate directory tree in markdown format
```

### Step 4: 生成环境策略章节

```
Read environment_config_checklist.md
Extract environment list (dev/test/staging/prod)
For each environment:
  - Define purpose
  - Define data characteristics
  - Define access policy
```

### Step 5: 生成质量门禁章节

```
Based on SPEC level:
  L1: Code Coverage ≥70%, Test Pass ≥95%, Lint (optional)
  L2: Code Coverage ≥80%, Test Pass ≥98%, Lint (required), Security Scan (optional)
  L3: Code Coverage ≥90%, Test Pass ≥100%, Lint (required), Security Scan (required), Performance Benchmark (required)

Format as table with thresholds
```

### Step 6: 生成HITL检查点章节

```
Based on SPEC level:
  L1: High-risk SubPlan + Integration Phase
  L2: L1 + Dependency conflicts + External API integration
  L3: L2 + Security-sensitive changes + Performance degradation

Define escalation strategy (E1/E2/E3)
```

### Step 7: 写入约束文件

```
Write `_exec_specs/ExecSpecMasterConstraints_L{level}.md`
Include all 6 sections
Add metadata (creation date, SPEC level, reference links)
```

---

## 6. 快速开始

### 第1步：开发者确定SPEC级别

开发者需要确定项目使用L1/L2/L3哪个级别。

### 第2步：确保前置SKILL已执行

- scaffold-analysis（项目类型、测试框架）
- environment-config-generator（环境策略）

### 第3步：调用此SKILL

```
///constraints-generator

Level: L1
```

### 第4步：查看生成的约束文件

查看 `_exec_specs/ExecSpecMasterConstraints_L1.md`（或L2/L3）。

### 第5步：SubPlan引用约束文件

所有SubPlan必须在开头引用约束文件：
```markdown
**约束**: 生成后见 `_exec_specs/ExecSpecMasterConstraints_L1.md`（或 L2/L3）
```

**预计耗时**: 2-3分钟

---

## 7. 使用说明

### 输入要求

- **SPEC级别**：必须明确指定 L1/L2/L3
- **scaffold_analysis_report.md**：需包含项目类型和测试框架
- **environment_config_checklist.md**：需包含环境列表（可选，如缺失使用默认dev/test）

### 输出格式示例

**ExecSpecMasterConstraints_L1.md**包含以下章节：
- 命名规范：Phase/SubPlan/Round格式和示例
- 目录结构：_exec_specs/文件布局
- 环境策略：dev/test环境配置（L1仅2个环境）
- 质量门禁：代码覆盖率≥70%，测试通过率≥95%
- HITL检查点：高风险SubPlan和集成Phase的检查条件
- 升级策略：E1（阻塞）/E2（警告）处理规则

---

## 8. 价值

### SPEC组织
- 统一 ExecSpec 口径（Compile/Fulfill ExecSpec），减少混乱
- 明确质量标准，提供可验证的阈值

### PM/BA
- 了解质量门禁要求
- 识别HITL检查点，预估人工介入成本

### Dev
- 明确命名规范，避免命名冲突
- 明确质量标准，避免"测试够不够"的争论
- 权威文档，所有SubPlan统一引用

---

## 9. 质量检查

- [ ] 约束文件已生成（_exec_specs/ExecSpecMasterConstraints_L*.md）
- [ ] 包含6个必需章节（命名/目录/环境/质量/HITL/升级）
- [ ] 命名规范有示例
- [ ] 质量门禁有具体阈值（%数字）
- [ ] HITL检查点有触发条件
- [ ] 文件格式正确（markdown表格、代码块）

---

## 10. 限制条件

**不支持**：
- 动态调整质量门禁阈值（需手动修改约束文件）
- 自定义命名规范（必须遵循标准格式）

**依赖**：
- 需要SPEC级别明确指定
- 建议先执行scaffold-analysis和environment-config-generator

---

## 相关 SKILLs

- **前置**: scaffold-analysis, environment-config-generator
- **并行**: dependency-graph-generator, round-planning
- **后续**: 无（Dashboard 在 Master Plan 生成时自动创建）

---
