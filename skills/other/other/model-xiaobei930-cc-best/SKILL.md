---
name: model
description: "Model selection strategy and routing. Use when choosing between models for different task types, subagent configurations, or optimizing token cost vs quality tradeoffs."
allowed-tools: Read, Grep, Glob
---

# 模型选择技能

本技能提供任务类型到模型的推荐映射，帮助 Claude 在不同场景下选择合适的模型。

## 子文件

- [routing-matrix.md](routing-matrix.md) - 任务类型→模型推荐矩阵

## 核心原则

1. **探索用 Haiku** — 快速、低成本，适合大量 Glob/Grep/Read 操作
2. **实现用 Sonnet** — 平衡质量和速度，适合编码和测试
3. **决策用 Opus** — 深度思考，适合架构设计和安全审查

## 与 /cc-best:model 命令的关系

- `/cc-best:model` 命令用于**全局切换**所有 Agent 的模型策略（quality/balanced/economy）
- 本技能提供**细粒度参考**，帮助 Claude 在具体任务中判断模型选择
- 命令是"批量切换"，技能是"逐任务建议"

## 使用场景

### 自动参考

当 Claude 遇到以下场景时，会自动参考本技能：

- 启动子代理（Task tool）时选择 model 参数
- 评估当前任务复杂度时
- 用户询问模型选择建议时

### 决策流程

```
任务到达 ──→ 评估复杂度 ──→ 查询 routing-matrix ──→ 选择模型
                │
                ├─ 简单（搜索/读取）→ haiku
                ├─ 中等（编码/测试）→ sonnet
                └─ 复杂（架构/安全）→ opus
```

## 最佳实践

1. **成本敏感场景** — 子代理探索任务优先 haiku，节省 token
2. **质量敏感场景** — 安全审查、架构决策必须用 opus
3. **混合场景** — 同一工作流中可对不同阶段使用不同模型
4. **用户偏好** — 尊重 `/cc-best:model` 设定的全局策略

---

> **记住**：模型选择的目标是用最低成本达到足够的质量。不是所有任务都需要最强模型，也不是所有任务都能用最快模型。
