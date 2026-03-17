---
name: test-pyramid-advisor
description: 分析unit/integration/e2e测试分配比例，建议60/30/10比例平衡。当AICTXT/测试策略确定后使用，优化测试执行效率和覆盖质量。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## test-pyramid-advisor: 测试金字塔建议

### 描述
分析unit/integration/e2e测试的当前分配比例，对标CRAFT标准建议调整，确保测试金字塔比例合理。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2**: 创建 AICTXT（如 `aictxt.md`）和 `test_suites.md` 时
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection分析测试粒度时
- **WORKFLOW_STEP_5 Task S5-5**: CONSTRAINT验收前的结构检查

### 输入
- AICTXT artifact host file（如 `aictxt.md`，包含测试策略与质量门禁口径）
- test_suites.md（测试套件组织）
- scenarios/bdd_test_scenarios.md（所有测试场景）
- 当前级别（L1/L2/L3）

### 输出
- 测试金字塔分析报告（markdown）
- 当前分配比例（如"unit:55%, integration:30%, e2e:15%"）
- 对标标准比例：L1(60/30/10), L2(70/20/10), L3(70/20/10)
- 失衡诊断和调整建议
- 关键路径建议（哪些SC应作为unit/integration/e2e）

### 执行策略
1. 从test_suites.md提取各层级测试计数
   - Unit tests: 基础单元测试数量
   - Integration tests: 模块间集成测试数量
   - E2E tests: 端到端业务流测试数量
2. 计算当前分配比例
3. 对标CRAFT标准（L1/L2/L3各不同）
4. 分析失衡原因
5. 根据SC优先级建议重新分配
6. 生成调整方案

### 价值
- **SPEC组织**: 确保测试金字塔比例合理，优化测试成本
- **PM**: 理解测试投入分配，评估测试时间
- **Dev**: 清晰的各层级测试策略，提升TDD效率

### 验收标准（CRAFT标准）
| 级别 | Unit | Integration | E2E |
|------|------|-------------|-----|
| L1 | 60% | 30% | 10% |
| L2 | 70% | 20% | 10% |
| L3 | 70% | 20% | 10% |
