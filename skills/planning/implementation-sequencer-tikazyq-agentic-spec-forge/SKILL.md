---
name: implementation-sequencer
description: 验证代码构建顺序，分析依赖关键路径，建议Sprint划分和交付优先级。当STRUCT和GOAL确定后使用。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## implementation-sequencer: 实施顺序/依赖分析

### 描述
分析GOAL、组件、依赖关系，生成代码构建顺序和关键路径，建议Sprint划分和交付优先级。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-1**: STRUCT验证时，分析构建可行性
- **WORKFLOW_STEP_5 Task S5-2**: GOAL确定后，规划构建顺序
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection分析交付优先级
- **敏捷规划**: 转化为Sprint Backlog

### 输入
- spec/implementation/project_structure.md（模块拆分）
- goal_breakdown.md（所有GOAL）
- design/architecture.md（组件依赖）
- design/ 中的接口契约（模块间依赖）
- 当前级别和团队规模

### 输出
- 实施顺序报告（markdown）
- 代码构建依赖图（文本或可视化说明）
- 关键路径分析（哪些GOAL/模块是瓶颈）
- 构建顺序建议（基础→业务→集成）
- Sprint划分方案（按优先级/依赖分组）
- 风险识别（高依赖项、复杂模块等）

### 执行策略
1. 从project_structure.md提取模块依赖关系
2. 从goal_breakdown.md提取GOAL优先级和估算
3. 构建依赖图
   - 基础组件（无依赖）
   - 业务组件（依赖基础）
   - 集成组件（依赖多个）
4. 识别关键路径（影响整体交付的路径）
5. 计算完成时间（基于组件复杂度和并行度）
6. 生成构建顺序建议
7. 根据Sprint周期划分交付批次

### 价值
- **PM/Scrum Master**: 科学的Sprint规划，优化团队产能
- **Tech Lead**: 清晰的构建顺序，指导开发优先级
- **Dev**: 了解依赖关系，减少返工和阻塞

### 验收标准
- 构建顺序符合依赖关系（不出现循环依赖）
- 关键路径识别准确
- Sprint分组平衡（各Sprint工作量相近）
- 风险项提前识别
- 并行度充分（多个模块可同时开发）
