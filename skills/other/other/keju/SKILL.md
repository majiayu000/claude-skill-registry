---
name: keju
description: 系统一致性验证——检查 Skill frontmatter、Hook 语法、governance-core 与 team-bootstrap 角色一致性、受保护文件同步
user-invocable: true
disable-model-invocation: true
---

# Skill: 科举

> **适用 Agent**：太子（Lead）
> **加载时机**：皇上输入 `/keju` 时，或系统自检时

## 功能

全面验证三省六部系统的内部一致性，发现配置偏差与潜在问题。类似 lint + integration test。

## 检查项目

四类检查：Skill frontmatter 格式、Hook 脚本语法、角色名/agent_id 一致性、受保护文件列表同步。

> 📎 详细规则见 `keju-checklist.md`

## 输出格式

```
📋 科举成绩单

考试日期：2026-03-13

一、Skill Frontmatter（x/y 通过）
    ✅ morning-court — 通过
    ❌ xxx — ERROR: 缺少 description 字段

二、Hook 脚本（x/y 通过）
    ✅ H01-governance-shield.sh — 通过
    ⚠️ H03-audit-logger.sh — WARN: 缺少可执行权限

三、角色一致性（通过/未通过）
    ✅ 所有来源一致
    或
    ❌ roles-liubu.md 中缺少 agent_id: libu_hr

四、受保护文件同步（通过/未通过）
    ✅ 核心文件均在保护列表中
    或
    ⚠️ H06 未包含 CLAUDE.md

总评：x ERROR / y WARN / z INFO
      状元 🏆 / 进士 / 举人 / 落榜
```

**评级规则**：
- 0 ERROR + 0 WARN = 状元
- 0 ERROR + ≤3 WARN = 进士
- 0 ERROR + >3 WARN = 举人
- ≥1 ERROR = 落榜

## 约束

1. 检查过程为只读操作，不修改任何文件
2. 发现 ERROR 时建议修复方案但不自动修复
3. 成绩单必须呈报皇上，不得隐瞒不通过项
