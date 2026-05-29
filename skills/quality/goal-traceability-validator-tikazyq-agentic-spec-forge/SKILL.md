---
name: goal-traceability-validator
description: 验证GOAL的source_vs追溯链完整性，确保每个GOAL都能追溯到原始VS。当GOAL创建完成后使用。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## goal-traceability-validator: GOAL追溯性验证

### 描述
验证goal_breakdown.md中每个GOAL都有正确的source_vs字段，指向现存的VS。避免追溯链断裂导致需求遗漏。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2**: GOAL创建完成后立即检查
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection报告追溯链一致性
- **WORKFLOW_STEP_5 Task S5-5**: CONSTRAINT验收前的链接检查

### 输入
- design/（所有VS及其ID）
- implementation/goal_breakdown.md（所有GOAL）

### 输出
- 追溯链验证报告（markdown）
- 追溯链完整性百分比（如"100%, 所有GOAL都有source_vs"）
- 问题清单：
  - 缺失source_vs的GOAL
  - 指向不存在VS的GOAL
  - 指向不正确VS的GOAL
- 修复建议

### 执行策略
1. 从design/提取所有VS及其ID（格式：VS-<SN>-NNN）
2. 从goal_breakdown.md读取所有GOAL，检查source_vs字段
3. 验证source_vs格式正确（VS-<SN>-NNN）
4. 验证source_vs引用的VS确实存在
5. 生成验证报告和问题清单
6. 建议修复方案（指向正确的VS）

### 价值
- **SPEC组织**: 防止追溯链断裂，确保需求完整性
- **PM/BA**: 验证GOAL与需求映射的准确性
- **Dev**: 清晰的需求链接，避免理解偏差

### 验收标准
- 所有GOAL都有source_vs字段
- 所有source_vs引用有效的VS
- 追溯链逻辑合理（VS对应GOAL，GOAL对应SC）
