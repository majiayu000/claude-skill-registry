---
name: design-consistency-check
description: 检查VS↔SD/DM一致性（value_path是否与序列图/数据模型匹配），生成不一致项清单和修复建议。当Self-Reflection报告一致性问题或准备CONSTRAINT验收前使用。
stage: DESIGN
level_supported: [L2, L3]
---

## design-consistency-check: 设计一致性检查

### 描述
检查 VS↔SD/DM 一致性（value_path 是否与序列图/数据模型匹配），生成不一致项清单和修复建议。

### 适用场景
- **WORKFLOW_STEP_4 Task S4-2 Round 2**：生成所有 artifacts 后
- **WORKFLOW_STEP_4 Task S4-3**：Self-Reflection 报告一致性问题时
- **WORKFLOW_STEP_4 Task S4-5 前**：准备 CONSTRAINT 验收前

### 输入
- design/ 目录（所有 VS/SD/DM）

### 输出
- 一致性检查报告（markdown）
- 一致性百分比（如"75%，9/12 个 VS 一致"）
- 不一致项清单（哪些 VS 的 value_path 与 SD/DM 不匹配）
- 修复建议

### 执行策略
1. 遍历所有 VS（检查正文中的 value_path 段落，参考 CRAFT_L{LEVEL}_DESIGN.md）
2. 对每个 VS：
   - 从正文中读取 value_path 字段（D1/D2/D3/D4）
   - 查找对应的 SD/DM（DESIGN 阶段禁止 `source_vs`；优先用 VS 的 `### 设计输入索引（Design Inputs Index）` 定位）
     - 优先：从 VS 的 Design Inputs Index 中读取 SD/DM 的 `id` 与相对路径（或等价引用）
     - 兜底：在 `design/` 中扫描 SD/DM 文件，按 `source_us = VS.source_us`（或 `related_us` 覆盖主 US）匹配；必要时再用 `sn` 与正文引用交叉确认
   - 验证：
     - D1-Frontend → SD 中有前端步骤？
     - D2-Data Flow → SD 中有数据传递 + DM 有对应结构？
     - D3-Backend → SD 中有后端步骤？
     - D4-Feedback → SD 中有反馈步骤？
3. 生成不一致项清单 + 修复建议

### 价值
- **SPEC 组织**：提前发现一致性问题，避免 CONSTRAINT 验收失败
- **PM/BA**：确保设计完整实现需求
- **Dev**：清晰的设计依赖
