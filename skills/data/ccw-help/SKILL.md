---
name: ccw-help
description: CCW command help system. Search, browse, recommend commands. Triggers "ccw-help", "ccw-issue".
allowed-tools: Read, Grep, Glob, AskUserQuestion
version: 7.0.0
---

# CCW-Help Skill

CCW 命令帮助系统，提供命令搜索、推荐、文档查看功能。

## Trigger Conditions

- 关键词: "ccw-help", "ccw-issue", "帮助", "命令", "怎么用"
- 场景: 询问命令用法、搜索命令、请求下一步建议

## Operation Modes

### Mode 1: Command Search

**Triggers**: "搜索命令", "find command", "search"

**Process**:
1. Query `command.json` commands array
2. Filter by name, description, category
3. Present top 3-5 relevant commands

### Mode 2: Smart Recommendations

**Triggers**: "下一步", "what's next", "推荐"

**Process**:
1. Query command's `flow.next_steps` in `command.json`
2. Explain WHY each recommendation fits

### Mode 3: Documentation

**Triggers**: "怎么用", "how to use", "详情"

**Process**:
1. Locate command in `command.json`
2. Read source file via `source` path
3. Provide context-specific examples

### Mode 4: Beginner Onboarding

**Triggers**: "新手", "getting started", "常用命令"

**Process**:
1. Query `essential_commands` array
2. Guide appropriate workflow entry point

### Mode 5: Issue Reporting

**Triggers**: "ccw-issue", "报告 bug"

**Process**:
1. Use AskUserQuestion to gather context
2. Generate structured issue template

## Data Source

Single source of truth: **[command.json](command.json)**

| Field | Purpose |
|-------|---------|
| `commands[]` | Flat command list with metadata |
| `commands[].flow` | Relationships (next_steps, prerequisites) |
| `commands[].essential` | Essential flag for onboarding |
| `agents[]` | Agent directory |
| `essential_commands[]` | Core commands list |

### Source Path Format

`source` 字段是相对路径（从 `skills/ccw-help/` 目录）：

```json
{
  "name": "lite-plan",
  "source": "../../../commands/workflow/lite-plan.md"
}
```

## Slash Commands

```bash
/ccw-help                    # 通用帮助入口
/ccw-help search <keyword>   # 搜索命令
/ccw-help next <command>     # 获取下一步建议
/ccw-issue                   # 问题报告
```

## Maintenance

### Update Index

```bash
cd D:/Claude_dms3/.claude/skills/ccw-help
python scripts/analyze_commands.py
```

脚本功能：扫描 commands/ 和 agents/ 目录，生成统一的 command.json

## Statistics

- **Commands**: 88+
- **Agents**: 16
- **Essential**: 10 核心命令

## Core Principle

**智能整合，非模板复制**

- 理解用户具体情况
- 整合多个来源信息
- 定制示例和说明
