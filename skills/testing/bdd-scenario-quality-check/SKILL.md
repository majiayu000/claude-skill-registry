---
name: bdd-scenario-quality-check
description: 检查Given-When-Then格式规范性，发现场景缺口，提供丰富建议。当BDD场景编写完成后使用，确保场景质量符合CRAFT标准。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## bdd-scenario-quality-check: BDD场景质量检查

### 描述
检查Given-When-Then格式规范性，发现BDD场景缺口，提供丰富建议。确保所有SC都符合CRAFT标准的Given-When-Then格式。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2**: SC创建完成后
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection报告场景质量时
- **WORKFLOW_STEP_5 Task S5-5**: CONSTRAINT验收前的质量检查

### 输入
- scenarios/bdd_test_scenarios.md（所有SC）
- goal_breakdown.md（GOAL清单）
- 当前级别（L1/L2/L3）

### 输出
- BDD场景质量报告（markdown）
- 格式规范性得分（如"92%，23/25个场景格式正确"）
- 缺陷清单（格式错误、不完整、业务语言不清等）
- 场景缺口清单（哪些GOAL缺少对应SC）
- 丰富建议（如何改进场景描述）

### 执行策略
1. 扫描 bdd_test_scenarios.md 提取所有SC
2. 验证每个SC是否包含Given-When-Then三要素
3. 检查Given/When/Then是否遵循业务语言（不含代码）
4. 验证SC粒度（L1不超过3步，L2不超5步，L3更灵活）
5. 检查Given-When-Then链条逻辑是否通畅
6. 对照GOAL清单，发现缺失的SC
7. 生成质量报告和丰富建议

### 价值
- **SPEC组织**: 提早发现场景格式/内容问题，避免验收反复
- **QA**: 清晰的测试场景描述，易于转换为自动化
- **Dev**: 理解测试意图，TDD实施更精准

### 验收标准
- Given/When/Then 三要素完整
- 业务语言清晰（无代码）
- 场景粒度适当
- 逻辑链条通畅
- 每个GOAL都有对应SC
