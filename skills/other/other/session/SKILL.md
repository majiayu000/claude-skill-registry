---
name: session
description: "Session lifecycle management. Parent skill for session-related skills: learning (pattern extraction) and compact (context compression)."
allowed-tools: Read, Grep, Glob
---

# 会话生命周期管理

本技能提供 Claude Code 会话的生命周期管理策略，整合持续学习和上下文压缩。

## 会话生命周期

```
会话开始 ──→ 工作阶段 ──→ 检查点 ──→ 会话结束
    │           │           │           │
    │           │           │           └─→ 提取模式 (/learning)
    │           │           └─→ 上下文压缩 (/cc-best:compact-context)
    │           └─→ 持续工作
    └─→ 加载上次上下文
```

## 策略选择

| 场景             | 推荐策略       | 子技能                     |
| ---------------- | -------------- | -------------------------- |
| 上下文接近限制   | 策略性压缩     | `/cc-best:compact-context` |
| 完成重要任务节点 | 主动压缩       | `/cc-best:compact-context` |
| 会话结束时       | 提取可复用模式 | `/learning`                |
| 解决了复杂问题   | 记录解决方案   | `/learning`                |
| 发现项目特定知识 | 记录到知识库   | `/learning`                |

## 子技能

### 1. learning（持续学习）

**适用场景**：

- 会话结束时提取模式
- 记录调试技巧
- 保存项目特定知识
- 积累可复用解决方案

**使用方式**：`/learning` 或参阅 `skills/learning/SKILL.md`

### 2. compact（上下文压缩）

**适用场景**：

- 上下文接近限制时
- 完成阶段性任务后
- 切换工作主题前
- 需要释放上下文空间

**使用方式**：`/cc-best:compact-context` 或参阅 `skills/compact/SKILL.md`

## 最佳实践

### 何时压缩

1. **主动压缩** - 完成一个功能模块后
2. **被动压缩** - 系统提示上下文接近限制
3. **切换压缩** - 准备切换到不同任务前

### 何时记录

1. **立即记录** - 解决问题后立即记录
2. **定期回顾** - 会话结束前检查值得记录的内容
3. **增量更新** - 发现新知识时更新已有记录

## 会话别名 | Session Aliases

为会话设置语义化标签，便于快速查找和恢复。

### 别名管理

在会话元数据中记录语义化标签：

```json
{
  "name": "feature-login-page",
  "sessionPath": "memory-bank/progress.md",
  "tags": ["feature", "frontend"],
  "created": "2026-02-24 14:30:00",
  "summary": "实现登录页面 - PM/Lead/Dev 已完成"
}
```

**存储位置**: `~/.claude/session-aliases.json`（全局，跨项目共享）

**标签分类系统**：

| 前缀         | 含义     | 示例                  |
| ------------ | -------- | --------------------- |
| `feature-*`  | 功能开发 | feature-login-page    |
| `bugfix-*`   | 缺陷修复 | bugfix-auth-timeout   |
| `refactor-*` | 重构改进 | refactor-api-layer    |
| `explore-*`  | 技术探索 | explore-new-framework |

### 跨会话恢复

当使用 `/cc-best:catchup` 恢复时：

1. 读取上次会话的 alias 信息
2. 加载对应的 progress.md 状态
3. 显示上次会话的关键决策摘要

### 别名操作

- **保存**: 会话结束时自动提示或通过 `/cc-best:checkpoint` 手动触发
- **查找**: 通过 `/cc-best:catchup --alias <name>` 快速恢复指定会话
- **清理**: 超过 30 天未使用的别名自动标记为过期

## 会话健康指标

| 指标         | 健康状态 | 行动         |
| ------------ | -------- | ------------ |
| 上下文使用   | < 70%    | 继续工作     |
| 上下文使用   | 70-90%   | 考虑压缩     |
| 上下文使用   | > 90%    | 立即压缩     |
| 有价值的发现 | 有       | 记录到知识库 |

---

> **记住**：良好的会话管理让每次对话都能高效利用上下文，同时积累可复用的知识。
