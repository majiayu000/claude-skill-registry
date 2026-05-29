---
name: registry-sync-validator
description: 审计Registry是否与设计artifacts保持一致，生成同步率报告和遗漏清单。当完成设计后、CONSTRAINT验收前使用，避免Registry不一致导致验收失败。
stage: DESIGN
level_supported: [L2, L3]
---

## registry-sync-validator: Registry同步一致性检查

### 描述
审计 Registry 是否与设计 artifacts 保持一致，确保每个 artifact 都已正确注册并关键字段同步。Registry 是追溯链的基础基础设施，不一致会导致：
- CONSTRAINT 验收失败（Registry 同步是第 1 组结构性必须项）
- 追溯链断裂，后续 IMPLEMENTATION 阶段追溯困难
- 多人协作中 artifact 遗漏或重复注册

### 适用场景
- **WORKFLOW_STEP_4 Task S4-2 Round 2**：生成所有 artifacts 后，第一次检查 Registry
- **WORKFLOW_STEP_4 Task S4-3**：Self-Reflection 中定期审核 Registry 一致性
- **WORKFLOW_STEP_4 Task S4-5 前**：准备进入 CONSTRAINT 验收前的最后检查
- **多人协作场景**：确保团队成员都正确注册了各自的 artifacts

### 输入
- `spec/design/` 目录（所有 VS/SD/DM/ARCH/ADR artifacts）
- Registry 文件（路径：`.registry.json` 或 `_sys/registry.md` 等）
- 当前级别（L2/L3）

### 输出
- Registry 同步检查报告（markdown）
- 同步率统计（如"95%，19/20 个 artifacts 已注册"）
- **遗漏清单**：在 design/ 中存在但未在 Registry 中注册的 artifacts
- **冗余清单**：在 Registry 中存在但在 design/ 中已删除的 artifacts
- **字段不一致清单**：已注册但关键字段与实际 artifact 不同步
- 修复建议（按优先级排序）

### 执行策略
1. **扫描 design/ 目录**，提取所有 artifacts：
   - VS-<SN>-NNN（Value Stream）
   - SD-<SN>-NNN（Sequence Diagram）
   - DM-<SN>-NNN（Data Model）
   - ARCH-<SN>-NNN（Architecture）
   - ADR-<SN>-NNN（Architecture Decision Record，L3 only）

2. **解析 Registry**，提取已注册的 artifacts 清单和关键字段：
   - name（artifact 名称）
   - id（unique ID）
   - level（L1/L2/L3）
   - stage（REQUIREMENTS/DESIGN/IMPLEMENTATION）
   - status（active/deprecated）

3. **对比分析**：
   - **遗漏注册**：在 design/ 中存在但不在 Registry 中
   - **冗余注册**：在 Registry 中但在 design/ 中已删除
   - **字段不一致**：关键字段（name/level/stage）与 design/ 中的 artifact 不一致

4. **生成报告**：
   - 同步率统计（% 数值）
   - 遗漏清单（按 artifact 类型分类）
   - 冗余清单
   - 字段不一致清单
   - 优先级修复建议（Critical: 遗漏 > High: 字段不一致 > Medium: 冗余）

5. **验收标准**：
   - L2：同步率 ≥95%（最多 1 个遗漏）
   - L3：同步率 ≥99%（无遗漏，允许冗余但应标注为 deprecated）

### 价值
- **SPEC 组织**：确保 Registry 准确性，是 CONSTRAINT 第 1 组验收的必要条件
- **质量报告**：Registry 是追溯链的基础，准确性直接影响 CRAFT/CONSTRAINT 验收报告
- **DevOps/工具链**：Registry 用于生成各类自动化报告（覆盖率、追溯链等），准确性至关重要
- **多人协作**：快速发现谁的 artifacts 没有注册或注册错误

### 验收标准（CONSTRAINT 第 1 组结构性）
| 级别 | Registry 同步率 | 遗漏容忍度 | 字段不一致容忍度 |
|------|----------------|----------|-----------------|
| L2 | ≥95% | 最多 1 个 | 0 个（必须修复） |
| L3 | ≥99% | 0 个 | 0 个（必须修复） |
