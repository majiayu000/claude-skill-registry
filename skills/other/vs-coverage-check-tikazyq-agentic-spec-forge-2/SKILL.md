---
name: vs-coverage-check
description: 检查每个US是否有对应的VS，生成覆盖率报告和修复建议。当设计文档创建后、CONSTRAINT验收前使用，避免US→VS覆盖率<100%导致验收失败。
stage: DESIGN
level_supported: [L1, L2, L3]
---

## vs-coverage-check: 设计覆盖率检查

### 描述
检查每个 US 是否有对应的 VS，生成覆盖率报告和修复建议。当设计文档创建后、CONSTRAINT 验收前使用，避免 US→VS 覆盖率 <100% 导致验收失败。

### 适用场景
- **WORKFLOW_STEP_4 Task S4-2 Round 2**：设计文档创建后
- **WORKFLOW_STEP_4 Task S4-5 前**：准备进入 CONSTRAINT 验收前
- **自检工具**：提前发现覆盖缺口，避免验收失败

### 输入
- requirements/ 目录（所有 US）
- design/ 目录（所有 VS）

### 输出
- VS 覆盖率报告（markdown）
- 覆盖率百分比（如"85%，12/14 个 US 有对应 VS"）
- 缺失的 US 清单（哪些 US 没有对应 VS）
- 修复建议（建议创建哪些 VS）

### 执行策略
1. 扫描 requirements/ 目录，提取所有 US-ID（格式：US-<SN>-NNN，参考 CRAFT_L{LEVEL}_REQUIREMENTS.md）
2. 扫描 design/ 目录，提取所有 VS 的 source_us 字段（Front Matter 必填字段，参考 CRAFT_L{LEVEL}_DESIGN.md）
3. 计算覆盖率（VS 覆盖的 US 数量 / 总 US 数量）
4. 识别缺失的 US（未被任何 VS 的 source_us 引用）
5. 生成修复建议（建议创建 VS-<SN>-NNN，派生自缺失的 US）

### 价值
- **SPEC 组织**：提前发现 US→VS 覆盖缺口，避免 CONSTRAINT 验收失败
- **PM/BA**：确保所有需求都有设计
- **Dev**：完整的设计视图，无遗漏
