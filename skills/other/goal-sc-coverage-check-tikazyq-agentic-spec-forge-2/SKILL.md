---
name: goal-sc-coverage-check
description: 检查VS→GOAL→SC覆盖完整性，确保每个VS都有对应的GOAL和SC。当GOAL和SC创建完成后使用，避免覆盖缺口导致验收失败。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## goal-sc-coverage-check: GOAL-SC覆盖率检查

### 描述
检查VS→GOAL→SC覆盖完整性，确保每个VS都有对应的GOAL和SC，避免覆盖缺口导致CONSTRAINT验收失败。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2**: GOAL和SC创建完成后
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection报告覆盖率时
- **WORKFLOW_STEP_5 Task S5-5**: CONSTRAINT验收前的预检

### 输入
- design/（所有VS）
- implementation/goal_breakdown.md（所有GOAL）
- scenarios/bdd_test_scenarios.md（所有SC）

### 输出
- 覆盖率完整性报告（markdown）
- 覆盖率百分比（如"85%，12/14个VS有对应GOAL"）
- 缺失清单（哪些VS→GOAL→SC链路不完整）
- 修复建议（建议补全的GOAL/SC）

### 执行策略
1. 扫描 design/ 目录提取所有VS及其source_us
2. 扫描 goal_breakdown.md 提取所有GOAL及其source_vs
3. 扫描 bdd_test_scenarios.md 提取所有SC及其source_goal
4. 验证链路完整性：VS → GOAL → SC
5. 计算覆盖率（完整链路数 / 总VS数）
6. 生成缺失清单和修复建议

### 价值
- **SPEC组织**: 提前发现覆盖缺口，避免验收失败
- **PM/BA**: 确保所有VS都有测试覆盖
- **Dev**: 清晰的测试覆盖范围，避免遗漏

### 验收标准
- L1: ≥90% 覆盖率
- L2: ≥95% 覆盖率
- L3: 100% 覆盖率
