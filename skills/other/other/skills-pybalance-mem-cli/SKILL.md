---
name: mem
description: "本地知识管理 CLI 工具。管理笔记、待办、日程，支持标签、搜索、日程视图、Markdown 导出和原生 SQL 查询。"
---

# mem - 个人知识管理 CLI

## 概述

`mem` 是一个本地命令行工具，用于管理个人知识、待办事项和日程安排。数据存储在本地 SQLite 数据库中。

## 数据库位置

- **默认路径**: `~/.mem/mem.db`
- **环境变量覆盖**: `MEM_DB=/path/to/db`

## 核心命令

### 添加条目

```bash
# 添加笔记
mem add --kind note --body "这是一条笔记"

# 添加待办
mem add --kind todo --body "完成报告" --due 2026-01-30

# 添加日程
mem add --kind event --body "团队会议" --event-time "2026-01-26T10:00:00Z"

# 添加带标签的条目
mem add --kind todo --body "紧急任务" --tag work --tag urgent

# JSON 输出
mem add --kind todo --body "测试" --json
```

**参数说明:**
- `-k, --kind`: 类型 (note/todo/event)，默认 note
- `-b, --body`: 内容（必填）
- `-p, --priority`: 优先级数字
- `-d, --due`: 截止日期 (YYYY-MM-DD)
- `-e, --event-time`: 事件时间 (RFC3339 格式)
- `-t, --tag`: 标签（可重复）

### 列表与搜索

```bash
# 列出所有条目
mem list

# 按类型筛选
mem list --kind todo

# 按状态筛选
mem list --status done
mem list --status trashed

# 按标签筛选
mem list --tag work

# 搜索内容
mem list --search "报告"

# JSON 输出
mem list --json
```

### 查看详情

```bash
mem show 1
mem show 1 --json
```

### 编辑条目

```bash
# 修改内容
mem edit 1 --body "更新后的内容"

# 修改类型
mem edit 1 --kind todo

# 设置截止日期
mem edit 1 --due 2026-02-01

# 清除截止日期
mem edit 1 --due ""
```

### 状态管理

```bash
# 标记完成
mem done 1

# 重新打开
mem reopen 1

# 移入回收站
mem trash 1

# 从回收站恢复
mem restore 1
```

### 标签管理

```bash
# 添加标签
mem tag add 1 work

# 移除标签
mem tag remove 1 work

# 列出所有标签
mem tag list
```

### 日程视图

```bash
# 查看未来 7 天
mem agenda

# 查看未来 14 天
mem agenda --days 14

# 指定日期范围
mem agenda --start 2026-01-25 --end 2026-02-01
```

### 导出 Markdown

```bash
# 输出到终端
mem export

# 导出到文件
mem export --output notes.md

# 按条件导出
mem export --kind todo --status active --output todos.md
```

## 高级功能

### 原生 SQL 查询

```bash
# 查询
mem sql "SELECT * FROM entries WHERE kind='todo'"

# 写入操作
mem sql --exec "UPDATE entries SET priority=1 WHERE id=1"

# 从文件执行
mem sql --file script.sql

# JSON 输出
mem sql "SELECT * FROM entries" --json
```

### 查看数据库结构

```bash
# 列出所有表
mem schema

# 查看表结构
mem schema entries
mem schema tags
mem schema entry_tags
```

## 数据库表结构

### entries 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| kind | TEXT | note/todo/event |
| body | TEXT | 内容 |
| status | TEXT | active/done/trashed |
| priority | INTEGER | 优先级 |
| due_date | TEXT | 截止日期 |
| event_time | TEXT | 事件时间 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### tags 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | 标签名（唯一） |

### entry_tags 表
| 字段 | 类型 | 说明 |
|------|------|------|
| entry_id | INTEGER | 条目 ID |
| tag_id | INTEGER | 标签 ID |

## 全局选项

- `--json`: 以 JSON 格式输出（适用于所有命令）
- `--help`: 显示帮助信息

## 常用工作流

### 每日待办管理
```bash
# 添加今日任务
mem add -k todo -b "完成代码审查" -d 2026-01-25 -t work

# 查看今日待办
mem list -k todo -s active

# 完成任务
mem done 1

# 查看已完成
mem list -s done
```

### 知识笔记
```bash
# 记录笔记
mem add -k note -b "Go 并发模式：使用 channel 进行通信" -t golang -t learning

# 按标签查找
mem list -t golang

# 搜索内容
mem list -q "并发"
```

### 日程管理
```bash
# 添加会议
mem add -k event -b "项目评审会" -e "2026-01-26T14:00:00+08:00" -t meeting

# 查看本周日程
mem agenda -d 7
```
