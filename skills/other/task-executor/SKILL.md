---
name: task-executor
description: 任务执行器，半自动任务执行系统，支持检查点、自动回滚、进度追踪。触发词：执行任务、任务管理。
version: v1.0
---

# Task Executor - 任务执行器 Skill

> 版本：v1.0
> 创建日期：2026-03-13
> 类型：人机协作系统

---

## 概述

Task Executor 是一个半自动任务执行系统，支持创建检查点、自动回滚、进度追踪等功能。

### 核心功能

| 功能 | 说明 |
|------|------|
| Checkpoint 管理 | 创建/恢复执行检查点 |
| 任务执行 | 执行命令序列，监控进度 |
| 配置验证 | 验证配置/代码是否正确 |
| 日志记录 | JSON 格式记录任务时间线 |
| 自动回滚 | 失败时自动恢复到检查点 |

---

## 使用方式

### 基本用法

```bash
# 创建任务
task-executor create "任务描述"

# 创建检查点
task-executor checkpoint create "检查点名称"

# 执行任务
task-executor run "命令 1" "命令 2" ...

# 回滚到检查点
task-executor rollback {task_id} {checkpoint_name}

# 查看任务状态
task-executor status {task_id}
```

### 执行模式

| 模式 | 说明 | 命令 |
|------|------|------|
| 全自动 | AI 执行，无需确认 | `--mode auto` |
| 半自动 | 关键节点等待确认 | `--mode semi` (默认) |
| 手动 | 逐条确认 | `--mode manual` |

---

## 脚本说明

### checkpoint.sh - 检查点管理

```bash
# 创建检查点
source checkpoint.sh
checkpoint_create "task_001" "before_config-change"

# 回滚到检查点
checkpoint_rollback "task_001" "before_config-change"

# 列出检查点
checkpoint_list "task_001"
```

### executor.mjs - 执行引擎

```javascript
// 执行任务
const executor = new Executor();
await executor.run(commands, { mode: 'semi' });

// 执行模式
// - auto: 全自动执行
// - semi: 关键节点确认
// - manual: 逐条确认
```

### validator.sh - 验证器

```bash
# 验证配置
source validator.sh
validate_config "hyprland"
validate_config "fish"
validate_config "fcitx5"
```

### logger.mjs - 日志记录

```javascript
// 记录事件
const logger = new Logger(taskId);
logger.info('任务开始');
logger.warn('配置验证失败');
logger.error('执行出错');
logger.complete('任务完成');
```

---

## 目录结构

```
~/skills/task-executor/
├── SKILL.md                 # 本文档
├── scripts/
│   ├── checkpoint.sh        # 检查点管理
│   ├── executor.mjs         # 执行引擎
│   ├── validator.sh         # 验证器
│   └── logger.mjs           # 日志记录
├── templates/
│   └── task-report.md       # 任务报告模板
└── tasks/                   # 任务数据
    └── {task_id}/
        ├── checkpoints/
        ├── logs/
        └── metadata.json
```

---

## 自动回滚触发条件

| 条件 | 动作 |
|------|------|
| 测试失败 | 回滚 + 生成测试报告 |
| 配置验证失败 | 回滚 + 显示错误日志 |
| 服务启动失败 | 回滚 + 尝试 3 次 |
| 用户中断（Ctrl+C） | 回滚 + 保存中间状态 |
| 超时（默认 30min） | 回滚 + 生成超时报告 |

---

## 集成示例

### 与 Auto-Router 集成

```bash
# 注册为 Skill
# 已在 ~/.claude/skills 中链接

# 触发词
- "执行任务"
- "自动完成"
- "帮我做"
```

### 与 Mission-Control 集成

```bash
# 同步任务状态到看板
task-executor sync --mission-control
```

---

## 配置

### 环境变量

```bash
# 执行超时（秒）
export TASK_EXECUTOR_TIMEOUT=1800

# 最大重试次数
export TASK_EXECUTOR_MAX_RETRIES=3

# 检查点目录
export TASK_EXECUTOR_CHECKPOINT_DIR="$HOME/.local/share/dotfiles/checkpoints"
```

### 配置文件

```yaml
# ~/.config/task-executor/config.yaml
mode: semi
timeout: 1800
max_retries: 3
checkpoint_dir: ~/.local/share/dotfiles/checkpoints
log_dir: ~/.local/share/dotfiles/logs/tasks
```

---

## 故障排查

### 问题 1: 检查点创建失败

```bash
# 检查目录权限
ls -la ~/.local/share/dotfiles/checkpoints/

# 创建目录
mkdir -p ~/.local/share/dotfiles/checkpoints
```

### 问题 2: 回滚失败

```bash
# 列出可用检查点
task-executor checkpoint list {task_id}

# 手动恢复
cp -r ~/.local/share/dotfiles/checkpoints/{task_id}/{checkpoint}/* ~/
```

### 问题 3: 日志不生成

```bash
# 检查日志目录
ls -la ~/.local/share/dotfiles/logs/tasks/

# 创建目录
mkdir -p ~/.local/share/dotfiles/logs/tasks
```

---

## 示例工作流

### 场景 1: 修改 Hyprland 配置

```bash
# 1. 创建任务
task-executor create "修改 Hyprland 快捷键"

# 2. 创建检查点
task-executor checkpoint create "before-keybinding-change"

# 3. 执行修改
task-executor run \
  "echo 'bind = SUPER, K, exec, kdeconnect-cli -d' >> ~/.config/hypr/keybindings.conf" \
  "hyprctl reload"

# 4. 验证
task-executor validate "hyprland"

# 5. 如果失败，回滚
task-executor rollback "before-keybinding-change"
```

### 场景 2: 批量安装软件

```bash
# 1. 创建任务
task-executor create "安装开发工具"

# 2. 创建检查点
task-executor checkpoint create "before-install"

# 3. 执行安装
task-executor run \
  "sudo pacman -S git neovim tmux" \
  "paru -S lazygit" \
  "npm install -g @anthropic-ai/claude-code"

# 4. 验证
task-executor validate "git" "nvim" "tmux" "claude"

# 5. 完成
task-executor complete
```

---

## API 参考

### task-executor create

```bash
task-executor create <description> [--id <task_id>]
```

### task-executor checkpoint

```bash
task-executor checkpoint create <name> [--task <task_id>]
task-executor checkpoint list <task_id>
task-executor checkpoint restore <task_id> <checkpoint_name>
```

### task-executor run

```bash
task-executor run <command1> [command2] ... [--mode auto|semi|manual]
```

### task-executor rollback

```bash
task-executor rollback <task_id> <checkpoint_name>
```

### task-executor status

```bash
task-executor status [task_id]
```

### task-executor complete

```bash
task-executor complete <task_id> [--success|--failure]
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-03-13 | 初始版本：Checkpoint 系统 + 执行引擎 |

---

*最后更新：2026-03-13*
