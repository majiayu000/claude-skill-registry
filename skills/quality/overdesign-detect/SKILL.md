---
name: overdesign-detect
description: 检测设计文档中的过度设计（实现细节、技术术语过多），生成过度设计清单和精简建议。当准备CONSTRAINT验收前使用，避免边界合规验收失败。
stage: DESIGN
level_supported: [L1, L2, L3]
---

## overdesign-detect: 过度设计检测

### 描述
检测设计文档中的过度设计（实现细节、技术术语过多），生成过度设计清单和精简建议。当准备 CONSTRAINT 验收前使用，避免边界合规验收失败。

### 适用场景
- **WORKFLOW_STEP_4 Task S4-2 Round 2**：生成 ARCH/ADR 后
- **L1/L2 特定**：担心设计包含过多实现细节
- **WORKFLOW_STEP_4 Task S4-5 前**：准备 CONSTRAINT 验收前

### 输入
- design/ 目录（所有 artifacts）
- 当前级别（L1/L2/L3）

### 输出
- 过度设计检测报告（markdown）
- 过度设计项清单（哪些 artifact 包含实现细节）
- 精简建议（建议删除或转移到 implementation/）

### 执行策略
1. 扫描 design/ 目录所有 artifacts
2. 检测禁止内容：
   - 代码片段（function/class 定义）
   - SQL 查询
   - 命令行命令
   - 具体算法实现（如"使用快速排序"）
3. 检测技术术语占比：
   - 统计技术术语（数据库表名、API endpoint、具体库名等）
   - 计算技术占比（应 ≤20% for L1/L2，≤40% for L3）
4. 生成过度设计清单 + 精简建议

### 价值
- **SPEC 组织**：提前发现边界违规，避免 CONSTRAINT 验收失败
- **PM/BA**：确保设��保持业务语言为主
- **Dev**：明确设计边界（设计不应包含实现细节）
