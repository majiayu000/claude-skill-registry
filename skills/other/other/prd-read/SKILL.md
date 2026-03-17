---
name: prd-read
version: 1.0
description: |
  Fast PRD reference - Quick lookup for product requirements.
  Auto-activates on "PRD", "产品需求", "读取需求", "read PRD", "查看 PRD" keywords.
  AMP principle: Simple toolbox (47-line script mindset).
allowed-tools: [Read, Grep, Bash]
trigger_keywords:
  - PRD
  - 产品需求
  - 读取需求
  - read PRD
  - 查看 PRD
  - check PRD
  - PRD 内容
auto_activate: true
priority: high
---

# PRD Read - 快速读取产品需求文档

**Purpose**: 快速定位和读取 PRD.md 中的相关需求

**AMP Principle**: 简单工具化 - 不是教科书，是速查表

---

## Quick Commands

### 读取完整 PRD
```bash
cat /Users/young/project/career_ios_backend/PRD.md
```

### 读取特定章节
```bash
# 当前版本
grep -A 5 "## Version" /Users/young/project/career_ios_backend/PRD.md

# 当前功能
sed -n '/## Current Features/,/##/p' /Users/young/project/career_ios_backend/PRD.md

# 技术栈
sed -n '/## Tech Stack/,/##/p' /Users/young/project/career_ios_backend/PRD.md

# API 端点
sed -n '/## API Endpoints/,/##/p' /Users/young/project/career_ios_backend/PRD.md
```

### 搜索关键词
```bash
# 搜索特定功能
grep -i "session" /Users/young/project/career_ios_backend/PRD.md

# 搜索 API
grep -i "POST\|GET\|PUT\|DELETE" /Users/young/project/career_ios_backend/PRD.md
```

---

## PRD 结构速查

```
PRD.md 标准结构:
├── Version (当前版本号)
├── Overview (项目概述)
├── Current Features (已完成功能)
├── Planned Features (计划功能)
├── Tech Stack (技术栈)
├── API Endpoints (API 端点列表)
├── Database Schema (数据库结构)
└── Implementation Status (实施状态)
```

---

## 使用模式

### Pattern 1: 开始新功能前
```
User: "我要开发 Session name field"
Agent:
  1. grep -i "session" PRD.md
  2. 确认需求存在
  3. 读取相关 API endpoints
  4. 开始 TDD workflow
```

### Pattern 2: 检查功能状态
```
User: "Client search API 做完了吗?"
Agent:
  1. sed -n '/## Implementation Status/,/##/p' PRD.md
  2. 查找 "Client search"
  3. 确认状态
```

---

## IMPORTANT

- **不是教学文档** - 是快速参考
- **保持简单** - 只包含必要命令
- **工具化思维** - describe() + execute()

---

**Version**: 1.0 (Toolbox refactor)
**Size**: ~120 lines
**Philosophy**: Simple > Complex
