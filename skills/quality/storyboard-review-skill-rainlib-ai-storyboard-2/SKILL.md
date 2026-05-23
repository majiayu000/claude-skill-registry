---
name: storyboard-review-skill
description: Use when reviewing storyboard outputs at any production stage (beat breakdown, beat board, sequence board, motion prompts), providing quality assurance feedback, or identifying revision requirements for Director agent
version: 1.0.0
allowed-tools: Read
user-invocable: false
---

# Storyboard Review Skill (故事板审查技能)

此技能为 Director 提供所有故事板制作阶段的系统化审查标准。

## 技能组件

### 1. **review-checklist.md**

各阶段质量标准：

- Beat Breakdown 审查检查清单
- Beat Board (9 格)审查检查清单
- Sequence Board (4 格)审查检查清单
- Motion Prompt 审查检查清单

## 用途

Director 使用此技能来：

- 系统性评估 Storyboard Artist 和 Animator 的输出
- 确保方法论合规性
- 识别需要修订的具体问题
- 提供可操作的反馈

## 何时使用此技能

Director 应在以下情况参考此技能：

- 审查任何 artifact 输出（所有 4 个阶段）
- 确定 PASS/FAIL 裁决
- 提供修订反馈
- 解释质量违规

## 审查理念

**公平，但严格**：

- PASS 意味着作品已准备好用于 AI 生成
- 有缺陷的提示词浪费生成预算和时间
- 现在要求修订总比生成糟糕的结果好

**具体明确**：

- 引用确切的行号、提示词或 beats
- 解释为什么某处有问题
- 准确告诉创作者需要修复什么

**教育性**：

- 帮助创作者理解方法论
- 认可做得好的地方
- 建立对质量标准的熟悉度

## 技能激活

此技能对 Director agent **始终激活**。所有审查必须遵循此处定义的检查清单。

---

**用法**: Director agent 自动引用此技能。无需手动调用。
