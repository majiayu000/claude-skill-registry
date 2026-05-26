---
name: arch-options-compare
description: 比较多个架构方案（单体/微服务等），从SOLID原则、成本、复杂度等维度评分，生成对比表和推荐方案。当需要向客户解释架构选择或ADR决策时使用。
stage: DESIGN
level_supported: [L1, L2, L3]
---

## arch-options-compare: 架构方案对比

### 描述
比较 2-3 个架构方案（如单体/微服务/Serverless），从 SOLID 原则、成本、复杂度、团队技能等维度评分，生成对比表。

### 适用场景
- **WORKFLOW_STEP_4 Task S4-2 Round 1**：用户提供多个技术选型方案时
- **WORKFLOW_STEP_4 Task S4-7**：需要向客户解释为什么选择某个架构
- **L3 特定**：ADR 记录架构决策时需要对比分析

### 输入
- 2-3 个架构方案名称（如"单体 vs 微服务"）
- 当前项目上下文（SPEC_PRJ_DESC + requirements/）

### 输出
- 对比表（markdown）
- 推荐方案 + 理由
- SOLID 原则支持度评分（每个原则 1-5 分）

### 执行策略
1. 提取项目规模、团队技能、NFR 要求（从 requirements/ 的 NFR artifact）
2. 对每个方案，评估：
   - 单一职责支持度（S）
   - 开闭原则支持度（O）
   - 里氏替换支持度（L）
   - 接口隔离支持度（I）
   - 依赖倒置支持度（D）
   - 成本（开发/运维）
   - 复杂度（学习曲线/维护难度）
   - 团队技能匹配度
3. 生成对比表（5-7 个维度）
4. 给出推荐方案 + 3-5 句理由（业务语言）

### 价值
- **SPEC 组织**：为 ARCH/ADR 提供决策依据
- **PM/用户**：理解技术选择的业务价值
- **Dev**：明确架构决策的权衡
