---
name: project-manager
description: 马斯克时间盒项目管理系统，追踪项目状态、管理优先级、生成快照。触发词：项目管理、项目快照、仪表板、时间盒、今日计划。
version: 2.0
---

# Project Manager - 时间盒项目管理

> 基于 Obsidian + 时间盒（Time Blocking）的项目管理系统
>
> 核心理念：时间盒驱动 + AI 辅助 + 可视化追踪

---

## 触发词

| 优先级 | 触发词 | 动作 |
|--------|--------|------|
| **高** | 项目管理、打开仪表板、项目快照 | 自动调用 |
| **高** | proj-open、proj-snapshot、proj-log、proj-stat | 自动调用 |
| **中** | 我的项目有哪些、今天做什么、项目进度 | 询问确认 |
| **中** | 创建项目、分析优先级 | 询问确认 |

---

## 快速启动

```bash
# 查看项目快照（最常用）
node ~/skills/project-manager/scripts/snapshot.mjs

# 打开项目仪表板
node ~/skills/project-manager/scripts/dashboard.mjs

# 创建今日时间盒日志
node ~/skills/project-manager/scripts/timebox.mjs

# 项目统计
node ~/skills/project-manager/scripts/stats.mjs
```

---

## 核心概念

### 时间盒 (Time Blocking)

将工作日划分为多个专注时间段，每个时间段专注单一任务：

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  09:00-11:00 │  11:00-12:00 │  14:00-16:00 │  16:00-18:00 │
│  深度工作    │  会议/沟通   │  深度工作    │  收尾/总结   │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### 项目快照 (Project Snapshot)

AI 可读的项目状态摘要，包含：
- 项目列表及状态
- 优先级排序
- 待办事项
- 阻塞问题

### 仪表板 (Dashboard)

Obsidian 可视化界面，整合：
- 项目进度概览
- 时间盒日历
- 任务看板
- 统计图表

---

## 命令说明

| 命令 | 脚本 | 用途 |
|------|------|------|
| `snapshot` | `snapshot.mjs` | 生成 AI 可读项目快照 |
| `dashboard` | `dashboard.mjs` | Obsidian 打开仪表板 |
| `timebox` | `timebox.mjs` | 创建/打开时间盒日志 |
| `stats` | `stats.mjs` | 显示项目统计 |

---

## 使用示例

### 查看项目状态

```
用户：我的项目有哪些？
→ 调用：project-manager snapshot
→ 输出：project-snapshot.md 内容
→ AI：基于快照分析优先级
```

### 开始今日工作

```
用户：今天开始工作
→ 调用：project-manager timebox
→ 动作：打开今日时间盒日志
→ AI：协助规划今日时间盒
```

### 项目分析

```
用户：分析一下我的项目优先级
→ 调用：project-manager snapshot
→ AI：基于快照给出优先级建议
→ 输出：更新后的项目计划
```

---

## 与 AI 协作流程

### 会话开始

```
用户触发"项目管理"
    ↓
AI 读取 project-snapshot.md
    ↓
AI 分析当前项目状态
    ↓
AI 给出优先级建议和今日计划
```

### 会话结束

```
AI 记录本次会话决策到快照
    ↓
更新待办事项状态
    ↓
git commit 保存变更
```

---

## 文件结构

```
~/skills/project-manager/
├── SKILL.md              # 本文档
├── scripts/
│   ├── snapshot.mjs      # 查看快照
│   ├── dashboard.mjs     # 打开仪表板
│   ├── timebox.mjs       # 时间盒日志
│   └── stats.mjs         # 项目统计
└── docs/
    └── USAGE.md          # 详细使用指南
```

---

## 相关路径

| 路径 | 说明 |
|------|------|
| `~/Obsidian/Projects/` | 项目管理主目录 |
| `~/Obsidian/Projects/project-snapshot.md` | AI 可读项目快照 |
| `~/Obsidian/Projects/Dashboards/` | 项目仪表板 |
| `~/Obsidian/Projects/Logs/` | 时间盒日志 |

---

## 完成标准

触发此 skill 时，任务完成必须满足：
- [ ] 项目快照已读取/更新
- [ ] 优先级已分析并记录
- [ ] 待办事项状态已同步
- [ ] 会话决策已保存到快照

---

## Token 效率优化

```bash
# 只读取快照文件（避免扫描整个目录）
head -100 ~/Obsidian/Projects/project-snapshot.md

# 使用 jq 处理 JSON 数据
node ~/skills/project-manager/scripts/snapshot.mjs --json | jq '.projects[] | {name, status}'
```

---

## 依赖

- [x] Obsidian（已安装）
- [ ] Obsidian 插件：Dataview, Templater（需用户安装）
- [x] fish/zsh shell 别名（已配置）

---

## 注意事项

1. **首次使用**：需要在 Obsidian 中安装 Dataview 插件
2. **项目快照**：每次项目状态变化时手动更新
3. **时间盒**：建议设置 25 分钟番茄钟
4. **AI 协作**：会话前运行 `proj-snapshot` 分享状态

---

## 相关技能

- [[deep-work-tracker]] - 深度工作追踪
- [[productivity-dashboard]] - 生产力仪表板
- [[task-executor]] - 任务执行器

---

*版本：v2.0 | 最后更新：2026-03-15*
