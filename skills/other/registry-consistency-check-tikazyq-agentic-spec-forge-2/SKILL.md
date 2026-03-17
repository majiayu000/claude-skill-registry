---
name: registry-consistency-check
description: 审计spec_artifacts_registry.md的Stage 3条目一致性，确保AICTXT/GOAL/SC等都已注册。当IMPLEMENTATION artifact创建完成后使用。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## registry-consistency-check: Registry一致性检查

### 描述
审计spec_artifacts_registry.md中Stage 3的所有IMPLEMENTATION_PLANNING artifact是否已正确注册，避免注册遗漏导致追溯链断裂。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2/S5-3**: 各artifact创建完成后检查是否已注册
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection中定期审计Registry
- **WORKFLOW_STEP_5 Task S5-5**: CONSTRAINT验收前的最终检查

### 输入
- spec_artifacts_registry.md（全局artifact注册表）
- implementation/ 目录（所有artifact文件）
- 当前级别（L1/L2/L3）

### 输出
- Registry审计报告（markdown）
- 已注册artifact清单（按类型分组）
- 缺失注册清单（哪些artifact未注册）
- 过时注册清单（Registry中存在但文件已删除）
- 修复建议

### 执行策略
1. 扫描implementation/目录，提取所有artifact文件
   - L1: project_structure.md, ai_context.txt, goal_breakdown.md, bdd_test_scenarios.md
   - L2: 上述+test_suites.md
   - L3: 上述+module_contracts.md
2. 从spec_artifacts_registry.md提取Stage 3的所有registered artifact
3. 对比两份清单：
   - 哪些文件未注册
   - 哪些Registry条目已过时
4. 验证Registry中Stage 3条目的完整性（ID/SN/Front Matter等）
5. 生成审计报告

### 价值
- **SPEC组织**: 维持Registry全局视图，确保追溯链完整
- **PM/BA**: 了解所有artifact的注册状态和产生时间
- **Gov**: 审计artifact生产过程，符合质量管理要求

### 验收标准
- 所有implementation artifact都在Registry中注册
- Registry条目信息完整（ID/SN/stage/level等）
- 无过时条目（已删除的artifact）
- 注册顺序合理（反映实际生产顺序）
