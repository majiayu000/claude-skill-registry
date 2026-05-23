---
name: schedule-manager
description: 通过 osascript 和 reminders-cli 管理 Apple Calendar 和 Reminders，遵循 GTD 方法论。触发场景：用户说「安排会议」「创建提醒」「查看日程」「规划下周」「添加待办」「今天要做什么」「周回顾」「记一下」「别忘了」时触发。
---

# Schedule Manager

通过 osascript (Calendar) 和 reminders-cli (Reminders) 管理日程，遵循 GTD 方法论。

## 核心原则（GTD 风格）

| 工具 | 用途 | 示例 |
|------|------|------|
| Calendar | 固定时间承诺 | 会议、约会、截止日期 |
| Reminders | 待办事项（无固定时间） | 购物清单、任务、想法 |

**决策流程：**

```text
有具体时间？ → Calendar 事件
无具体时间？ → Reminders 待办
需要提醒？ → 两者都可设置提醒
```

## 模式选择

| 用户意图 | 模式 | 操作 |
|----------|------|------|
| 「安排会议」「创建事件」 | Calendar | 创建带时间的事件 |
| 「添加待办」「创建提醒」「记一下」 | Reminders | 创建任务 |
| 「查看日程」「今天有什么」 | 查询 | 查询 Calendar + Reminders |
| 「规划下周」「周回顾」 | 规划 | 综合工作流 |

## Calendar 操作

### 查看日历列表

```bash
osascript -e 'tell application "Calendar" to get name of calendars'
```

### 查看今日/本周事件

```bash
osascript <<'EOF'
set today to current date
set time of today to 0
set tomorrow to today + (1 * days)

tell application "Calendar"
    repeat with cal in calendars
        set evts to (every event of cal whose start date ≥ today and start date < tomorrow)
        if (count of evts) > 0 then
            repeat with e in evts
                log (summary of e) & " | " & (start date of e)
            end repeat
        end if
    end repeat
end tell
EOF
```

详见 [osascript-calendar.md](references/osascript-calendar.md)。

### 创建事件

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        set startDate to (current date) + (1 * days)
        set hours of startDate to 14
        set minutes of startDate to 0
        set endDate to startDate + (1 * hours)
        make new event with properties {summary:"会议标题", start date:startDate, end date:endDate}
    end tell
end tell'
```

**可用属性：** `summary`, `start date`, `end date`, `description`, `location`, `allday event`

详见 [osascript-calendar.md](references/osascript-calendar.md)。

### 删除事件

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        delete (every event whose summary is "要删除的事件名")
    end tell
end tell'
```

## Reminders 操作

> **注意**：osascript 访问 Reminders 非常慢（已知问题），推荐使用 `reminders-cli`。
>
> 详见 [reminders-cli-guide.md](references/reminders-cli-guide.md)。

### 查看提醒列表

```bash
reminders show-lists
```

### 查看待办事项

```bash
# 查看所有未完成提醒
reminders show-all

# 查看指定列表
reminders show "工作"

# 按截止日期筛选
reminders show-all --due-date today
```

### 创建提醒

```bash
# 基础创建
reminders add "收件箱" "任务名称"

# 带截止日期
reminders add "工作" "完成报告" --due-date "tomorrow 5pm"

# 带优先级 (low/medium/high)
reminders add "工作" "紧急任务" --priority high
```

### 完成提醒

```bash
# 按索引完成（索引通过 show 命令查看）
reminders complete "收件箱" 0
```

### 其他操作

```bash
# 取消完成
reminders uncomplete "收件箱" 0

# 编辑提醒
reminders edit "收件箱" 0 "新的任务名称"

# 删除提醒
reminders delete "收件箱" 0
```

### osascript 备选（仅用于复杂操作）

osascript 适合需要批量操作或复杂查询的场景，但速度很慢。详见 [osascript-reminders.md](references/osascript-reminders.md)。

## 常见工作流

### 场景 1: 快速收集（GTD Capture）

用户说「记一下」「待会做」「别忘了」→ 创建 Reminder 到收件箱

```bash
reminders add "提醒" "<任务名>"
```

### 场景 2: 安排会议

用户说「安排明天下午 2 点的会议」→ 创建 Calendar 事件（使用 osascript）

### 场景 3: 每日规划

1. 查看今日 Calendar 事件（osascript）
2. 查看 Reminders 待办（`reminders show-all`）
3. 为重要任务安排 Time Block（Calendar 事件）

### 场景 4: 周回顾（GTD Weekly Review）

1. 查看本周完成的提醒
2. 查看下周 Calendar 事件（osascript）
3. 整理 Reminders 列表（`reminders show-all`）

详见 [gtd-methodology.md](references/gtd-methodology.md)。

## 依赖与权限

### 依赖

- **reminders-cli**（必需）：`brew install keith/formulae/reminders-cli`

### 权限配置（macOS）

首次运行需要授权，进入系统设置 → 隐私与安全性：

1. **日历** - 勾选 Terminal / iTerm / 你使用的终端应用
2. **提醒事项** - 同上

⚠️ 修改权限后需重启终端应用

检查权限：

```bash
# Calendar 权限
osascript -e 'tell application "Calendar" to get name of first calendar' 2>&1

# Reminders 权限（使用 reminders-cli）
reminders show-lists
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `AppleEvent timed out` | 权限未授予 | 在系统设置中授权 |
| `Can't get list` | 列表不存在 | 先用 `reminders show-lists` 查看可用列表 |
| `Invalid date` | 日期格式错误 | 使用 `current date` 作为基准 |
| `reminders: command not found` | 未安装 | `brew install keith/formulae/reminders-cli` |
| osascript Reminders 卡顿 | 已知性能问题 | 改用 `reminders-cli` |
