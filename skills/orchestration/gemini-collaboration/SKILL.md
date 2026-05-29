---
name: gemini-collaboration
description: |
  Gemini expert consultation for architecture design, second opinions, and code review.
  Use when: user requests Gemini, need alternative perspective, or get independent review.
  Gemini 是与 Claude 同等级别的顶级 AI 专家，按需调用。
  **注意：前端/UI 任务应使用专门的 Frontend 代理！**
---

# Gemini 协作流程

## 角色定位

**Gemini** 是与 Claude 同等级别的顶级 AI 专家（**按需调用**）：
- 🧠 **高阶顾问**：架构设计、技术选型、复杂方案讨论
- ⚖️ **独立审核**：代码 Review、方案评审、质量把关
- 🔨 **代码执行**：原型开发、功能实现

> ⚠️ **前端/UI 任务**请使用专门的 `frontend` 工具！

## 触发场景

1. **用户明确要求**：用户指定使用 Gemini
2. **Claude 自主调用**：需要第二意见或独立视角时
3. **架构决策**：技术选型、方案评审

## 任务路由

```
前端/UI 任务 → Frontend（专用代理）
架构/第二意见 → Gemini
代码实现（设计完成后） → Coder
代码审查 → Codex
```

## 工具参考

| 参数 | 默认值 | 说明 |
|------|--------|------|
| sandbox | workspace-write | 沙箱策略（灵活控制） |
| yolo | true | 跳过审批 |
| model | gemini-3-pro-preview | 默认模型 |
| max_retries | 1 | 自动重试 |

**会话复用**：保存 `SESSION_ID` 保持上下文。

## UI/UX Pro Max 技能

Gemini 可集成 [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)：
- 57 种 UI 风格
- 95 种调色板
- 56 种字体搭配
- 98 条 UX 指南

安装：`uipro init --ai gemini`

## 独立决策

Gemini 的意见仅供参考。你（Claude）是最终决策者，需批判性思考，做出最优决策。

**详细指南**：
- [gemini-guide.md](gemini-guide.md) - 工具参数
- [frontend-guide.md](frontend-guide.md) - 前端/UI 开发
