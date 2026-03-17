---
name: tech-selection-explain
description: 将技术选型决策转换为业务语言解释，生成客户友好的技术说明。当ARCH中技术术语过多、需要向PM/客户解释时使用。
stage: DESIGN
level_supported: [L1, L2, L3]
---

## tech-selection-explain: 技术选型业务语言解释

### 描述
将技术选型决策（如"选择 PostgreSQL"）转换为业务语言解释（如"关系数据库确保订单数据一致性"），生成客户友好的技术说明。

### 适用场景
- **WORKFLOW_STEP_4 Task S4-2 Round 2**：生成 ARCH 后，需要补充业务语言解释
- **WORKFLOW_STEP_4 Task S4-7**：准备客户演示或评审会议
- **CONSTRAINT 验收前**：ARCH 中技术术语过多，PM/BA 难理解

### 输入
- ARCH artifact（包含技术栈）
- requirements/ 目录（业务上下文）

### 输出
- 技术选型业务语言解释（markdown）
- 每个技术选择 1-2 句业务价值说明

### 执行策略
1. 从 ARCH 提取技术栈（数据库/框架/中间件等）
2. 从 requirements/ 提取相关的 US/NFR
3. 为每个技术选择，生成业务语言解释：
   - 技术选择：<技术名称>
   - 业务价值：<1-2 句业务语言>
   - 支持的需求：<US-ID 或 NFR-ID>
4. 确保业务语言占比 ≥80%（符合 CRAFT 标准）

### 价值
- **SPEC 组织**：补充 ARCH 的业务语言，提升 CRAFT 符合度
- **PM/用户**：理解技术选择的业务意义
- **Dev**：明确技术选择与需求的映射
