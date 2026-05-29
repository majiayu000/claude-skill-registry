---
name: goal-granularity-check
description: 确保GOAL粒度合理，不过粗或过细。当GOAL创建完成后使用，确保GOAL符合单一职责原则。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## goal-granularity-check: GOAL粒度检查

### 描述
检查goal_breakdown.md中所有GOAL的粒度（granularity），确保GOAL不过粗（能分解）也不过细（无意义）。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2**: GOAL创建初期，验证粒度合理性
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection中定期审视GOAL颗粒度
- **CONSTRAINT验收前**: 检查GOAL粒度是否符合CRAFT标准

### 输入
- goal_breakdown.md（所有GOAL）
- scenarios/bdd_test_scenarios.md（对应的SC）
- design/architecture.md（模块划分）
- 当前级别（L1/L2/L3）

### 输出
- GOAL粒度分析报告（markdown）
- 粗粒度问题清单（可进一步分解的GOAL）
- 细粒度问题清单（无实质意义的GOAL）
- 粒度评分（% 合理）
- 重构建议

### 执行策略
1. 读取goal_breakdown.md中所有GOAL
2. 对每个GOAL，检查以下指标：
   - **可分解性**: 是否可进一步分解成多个独立GOAL？
     - 可分解 → 过粗（标记为问题）
   - **有界性**: GOAL范围是否清晰？
     - 模糊 → 可能过粗
   - **SC数量**: 对应多少个SC？
     - 过多(>5) → 可能过粗
     - 过少(<1) → 可能过细或无用
   - **复杂度**: 估算实现难度
     - 很高 → 可能过粗
3. 对粗粒度GOAL提出分解建议
4. 对细粒度GOAL提出合并建议
5. 生成重构方案

### 价值
- **Dev**: 合理的GOAL粒度，便于TDD实施
- **QA**: 清晰的GOAL范围，便于SC编写
- **Architecture**: GOAL与模块对应关系清晰

### 验收标准（CRAFT标准）
| 级别 | 过粗标准 | 过细标准 | 最佳粒度 |
|------|--------|--------|--------|
| L1 | 可分解3个+ | SC<1个 | 2-3个SC |
| L2 | 可分解2个+ | SC<1个 | 3-5个SC |
| L3 | 可分解2个+ | SC<1个 | 3-5个SC |
