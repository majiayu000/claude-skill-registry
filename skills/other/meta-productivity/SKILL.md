---
name: meta-productivity
description: 统一生产力框架，整合时间盒、Checkpoint、专注追踪、任务执行、学习晋升。触发词：生产力系统、开始工作、今日计划、项目追踪。
version: 1.0
modules: [timebox, checkpoint, focus-tracker, task-executor, learning-hub]
---

# Meta-Productivity Framework - 统一生产力框架

> **整合 5 个最佳实践 Skill 的统一框架**
>
> 核心理念：Checkpoint 保护 + 时间盒驱动 + 强制闭环 + 知识晋升

---

## 触发词

| 优先级 | 触发词 | 动作 |
|--------|--------|------|
| **高** | 生产力系统、开始工作、今日计划 | 启动框架 |
| **高** | 创建 Checkpoint、回滚、恢复 | Checkpoint 管理 |
| **高** | 专注时间、开始深度工作 | 追踪专注 |
| **中** | 项目快照、时间盒、习惯打卡 | 调用模块 |
| **中** | 记录学习、错误日志、晋升知识 | 学习管理 |

---

## 核心模块

### 模块矩阵

| 模块 | 来源 | 核心功能 | 默认状态 |
|------|------|---------|---------|
| **Checkpoint** | task-executor | 创建/回滚检查点 | ✅ 启用 |
| **Timebox** | project-manager | 时间盒规划 | ✅ 启用 |
| **Focus** | deep-work-tracker | 专注时间追踪 | ✅ 启用 |
| **Task** | task-executor | 任务执行验证 | ⚠️ 按需 |
| **Learning** | self-improving-agent | 知识记录晋升 | ⚠️ 按需 |

---

## 快速启动

```bash
# 1. 初始化框架（首次使用）
node ~/skills/meta-productivity/scripts/init.mjs

# 2. 开始今日工作
node ~/skills/meta-productivity/scripts/start-day.mjs

# 3. 创建 Checkpoint
node ~/skills/meta-productivity/scripts/checkpoint.mjs create "before-change"

# 4. 开始专注时间
node ~/skills/meta-productivity/scripts/focus.mjs start "任务描述"

# 5. 查看状态
node ~/skills/meta-productivity/scripts/dashboard.mjs
```

---

## 核心机制

### 1. 五不原则（元规则）

| 原则 | 执行方式 |
|------|---------|
| **不做完不结束** | 每个任务必须有 `完成标准` 字段 |
| **不验证不完成** | 必须有 `验证者` 或 `验证命令` |
| **不记录不结束** | 所有操作写入 `progress.json` |
| **不恢复不开始** | 新会话自动检查 `.meta/active-session.json` |
| **不提交不结束** | 文件变更自动提示 `git commit` |

---

### 2. Checkpoint 系统（安全网）

```bash
# 创建 Checkpoint
node scripts/checkpoint.mjs create "before-config-change"

# 列出 Checkpoint
node scripts/checkpoint.mjs list

# 回滚
node scripts/checkpoint.mjs rollback "before-config-change"

# 验证 Checkpoint
node scripts/checkpoint.mjs verify
```

**Checkpoint JSON 结构**:
```json
{
  "id": "ckpt-20260315-001",
  "name": "before-config-change",
  "created": "2026-03-15T09:00:00+08:00",
  "type": "file-snapshot|git-commit|manual",
  "files": [".config/hypr/hyprland.conf"],
  "git_commit": "abc123",
  "description": "修改键位绑定前"
}
```

---

### 3. 时间盒 + 专注混合模式

```
┌─────────────────────────────────────────────────────────┐
│  时间盒：09:00-11:00 深度工作                           │
│  任务：实现用户认证模块                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [09:00] Checkpoint: session-start              │   │
│  │ [09:45] Checkpoint: focus-block-1-complete     │   │
│  │ [10:00] Checkpoint: break-start (休息 10 分钟)    │   │
│  │ [10:10] Checkpoint: break-end                  │   │
│  │ [11:00] Checkpoint: session-end + 自动生成总结  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

### 4. 学习晋升管道

```
┌──────────────┐    审查     ┌──────────────┐    晋升     ┌──────────────┐
│  原始记录    │ ──────────→ │  分类整理    │ ──────────→ │  知识库      │
│  ERRORS.md   │  每周回顾   │  标签 + 摘要  │  符合模式   │  CLAUDE.md   │
│  LEARNINGS.md│            │              │            │  AGENTS.md   │
└──────────────┘            └──────────────┘            └──────────────┘
```

**晋升条件**:
- 被引用 ≥ 3 次
- 适用于 ≥ 2 个不同场景
- 经过验证有效

---

## 数据持久化

### 统一进度 Schema

```json
{
  "$schema": "meta-productivity-v1",
  "session_id": "mp-20260315-001",
  "started": "2026-03-15T09:00:00+08:00",
  "modules": {
    "timebox": {
      "active": true,
      "current_box": {"start": "09:00", "end": "11:00", "task": "用户认证"},
      "boxes_today": [
        {"start": "09:00", "end": "11:00", "task": "用户认证", "status": "in_progress"},
        {"start": "14:00", "end": "16:00", "task": "Code Review", "status": "pending"}
      ]
    },
    "focus": {
      "total_minutes": 45,
      "blocks": [{"start": "09:00", "duration": 45, "quality": 4}]
    },
    "checkpoint": {
      "created_today": 2,
      "last_ckpt": "before-api-change"
    },
    "learning": {
      "entries_today": 1,
      "pending_promotions": ["LRN-20260315-001"]
    }
  },
  "checkpoints": [
    {"type": "session-start", "time": "09:00"},
    {"type": "focus-block-1-complete", "time": "09:45"}
  ],
  "completed": false
}
```

### 文件结构

```
~/.meta-productivity/
├── sessions/
│   └── 2026-03/
│       └── mp-20260315-001.json    # 会话进度
├── checkpoints/
│   └── <session-id>/
│       ├── ckpt-001.json           # Checkpoint 元数据
│       └── snapshots/              # 文件快照
├── focus/
│   └── 2026-03-15.json             # 专注记录
├── learnings/
│   ├── ERRORS.md                   # 错误日志
│   ├── LEARNINGS.md                # 学习记录
│   └── FEATURES.md                 # 功能请求
└── config/
    └── settings.json               # 用户配置
```

---

## 模块详细说明

### Module 1: Checkpoint

```bash
# 创建文件快照 Checkpoint
node scripts/checkpoint.mjs create <name> --files <file1,file2>

# 创建 Git Checkpoint（推荐）
node scripts/checkpoint.mjs create <name> --git

# 列出所有 Checkpoint
node scripts/checkpoint.mjs list [--session <id>]

# 回滚到 Checkpoint
node scripts/checkpoint.mjs rollback <name>

# 验证当前状态 vs Checkpoint
node scripts/checkpoint.mjs diff <name>
```

**自动回滚触发条件**:
| 条件 | 动作 |
|------|------|
| 测试失败 | 回滚 + 生成测试报告 |
| 配置验证失败 | 回滚 + 显示错误日志 |
| 服务启动失败 | 回滚 + 尝试 3 次 |
| 用户中断（Ctrl+C） | 回滚 + 保存中间状态 |

---

### Module 2: Timebox

```bash
# 创建今日时间盒
node scripts/timebox.mjs create

# 添加时间盒
node scripts/timebox.mjs add "09:00-11:00" "深度工作" "任务描述"

# 开始当前时间盒
node scripts/timebox.mjs start

# 结束当前时间盒
node scripts/timebox.mjs end [--quality 1-5]

# 查看今日时间盒
node scripts/timebox.mjs today
```

---

### Module 3: Focus Tracker

```bash
# 开始专注区块
node scripts/focus.mjs start "任务描述" [--duration 25|45|90]

# 结束专注区块
node scripts/focus.mjs end [--quality 1-5]

# 添加休息记录
node scripts/focus.mjs break [--duration 5|10|15]

# 查看今日专注
node scripts/focus.mjs today

# 生成本周报告
node scripts/focus.mjs report --week
```

---

### Module 4: Task Executor

```bash
# 创建任务
node scripts/task.mjs create "任务描述" --checkpoint "before-change"

# 执行命令序列
node scripts/task.mjs run "cmd1" "cmd2" --mode auto|semi|manual

# 验证任务
node scripts/task.mjs validate <task-id>

# 完成任务
node scripts/task.mjs complete <task-id> [--success|--failure]

# 回滚任务
node scripts/task.mjs rollback <task-id>
```

---

### Module 5: Learning Hub

```bash
# 记录错误
node scripts/learning.mjs error "错误描述" --category config|code|tool

# 记录学习
node scripts/learning.mjs learn "学习内容" --category best-practice|correction|tip

# 记录功能请求
node scripts/learning.mjs feature "功能描述"

# 列出待晋升内容
node scripts/learning.mjs pending

# 晋升到知识库
node scripts/learning.mjs promote <id> --to CLAUDE.md|AGENTS.md
```

---

## 完成标准

触发此 skill 时，任务完成必须满足：
- [ ] 会话进度已保存到 `.meta-productivity/sessions/`
- [ ] Checkpoint 已创建（如有修改）
- [ ] 时间盒状态已更新
- [ ] 专注时间已记录
- [ ] git commit 已创建（如有文件变更）
- [ ] 学习记录已晋升（如符合条件）

---

## Token 效率优化

```bash
# 只读取今日进度
head -50 ~/.meta-productivity/sessions/mp-$(date +%Y%m%d)-*.json

# 提取关键状态
jq '{session_id, timebox: .modules.timebox, focus_minutes: .modules.focus.total_minutes}' \
  ~/.meta-productivity/sessions/mp-$(date +%Y%m%d)-*.json
```

---

## 会话恢复协议

```bash
# 1. 检查活跃会话
if [ -f ~/.meta-productivity/sessions/active.json ]; then
  # 2. 读取进度
  progress=$(cat ~/.meta-productivity/sessions/active.json)

  # 3. 询问用户
  echo "发现未完成的会话：$(echo $progress | jq -r '.session_id')"
  echo "继续还是结束此会话？"
fi
```

---

## 相关技能

- [[task-executor]] - 任务执行器（Checkpoint 来源）
- [[project-manager]] - 项目管理（时间盒来源）
- [[deep-work-tracker]] - 深度工作追踪（专注模块来源）
- [[self-improving-agent]] - 自我改进（学习晋升来源）
- [[long-running-agent]] - 长任务管理（五不原则来源）

---

*版本：v1.0 | 创建日期：2026-03-15*
