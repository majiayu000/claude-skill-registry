---
name: env-setup
description: Claude Code 环境一键同步工具。从 GitHub 仓库同步所有配置到本地：output-styles 风格、CLAUDE.md 全局提示词、MCP 服务器配置。适用于多设备统一环境、换电脑恢复、团队共享配置等场景。当用户需要从 GitHub 仓库同步 Claude Code 环境配置时使用此 skill。
---

# Claude Code 环境一键同步工具

从 GitHub 仓库一键同步所有配置到本地 Claude Code 环境。

## 功能概述

本 skill 提供**一键同步**功能，将配置从 GitHub 仓库同步到本地：

- **`sync_env.py`** - 同步所有配置到本地

### 同步内容

| 组件 | 来源 | 目标 |
|------|------|------|
| Output Styles | `config/output-styles/` | `~/.claude/output-styles/` |
| CLAUDE.md | `config/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| MCP Config | `config/mcp_config.json` | `~/.claude.json` (合并) |

## GitHub 仓库结构

```
your-claude-env/              (GitHub 仓库)
├── env-setup.skill/          (或任意名称，放在 skills/ 下)
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── sync_env.py       (主同步脚本)
│   │   ├── backup_env.py     (备份脚本，可选)
│   │   └── restore_env.py    (恢复脚本，可选)
│   └── config/               (配置模板目录)
│       ├── output-styles/    (对话风格配置)
│       │   ├── laowang-engineer.md
│       │   ├── engineer-professional.md
│       │   └── ...
│       ├── CLAUDE.md         (全局提示词)
│       └── mcp_config.json   (MCP 服务器配置)
```

## 使用方法

### 一、初始化 GitHub 仓库

在主设备上创建仓库：

```bash
# 1. 创建项目目录
mkdir claude-env-sync
cd claude-env-sync

# 2. 复制 env-setup skill
cp -r ~/.claude/skills/env-setup ./

# 3. 复制当前配置到 config/
cp -r ~/.claude/output-styles/* env-setup/config/output-styles/
cp ~/.claude/CLAUDE.md env-setup/config/

# 4. 提取 MCP 配置
# (手动创建或使用脚本提取)
# mcp_config.json 格式见下方

# 5. 推送到 GitHub
git init
git add .
git commit -m "Initial Claude env config"
git remote add origin https://github.com/yourusername/claude-env-sync.git
git push -u origin main
```

### 二、在新设备上同步

```bash
# 1. 克隆仓库到 skills 目录
cd ~/.claude/skills
git clone https://github.com/yourusername/claude-env-sync.git

# 2. 运行同步脚本
python ~/.claude/skills/claude-env-sync/env-setup/scripts/sync_env.py

# 3. 重启 Claude Code
```

### 三、命令行选项

```bash
# 基本用法（同步所有配置）
python scripts/sync_env.py

# 强制覆盖已存在的文件
python scripts/sync_env.py --force

# 只同步特定组件
python scripts/sync_env.py --components output_styles mcp_config

# 指定 Claude 目录
python scripts/sync_env.py --claude-dir "/path/to/.claude"
```

**同步选项：**
- `output_styles` - 同步对话风格配置
- `claude_md` - 同步全局 CLAUDE.md
- `mcp_config` - 同步 MCP 服务器配置

## 配置文件格式

### mcp_config.json

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

**注意：** 敏感信息（API keys）建议使用环境变量或不在仓库中提交。

## 使用场景

### 场景 1：多设备环境统一

在多台电脑上保持一致的 Claude Code 配置：

```bash
# 主设备：更新配置后
git add .
git commit -m "Update config"
git push

# 其他设备：拉取并同步
git pull
python scripts/sync_env.py
```

### 场景 2：团队共享配置

团队成员共享统一的 output-styles 和 MCP 配置：

1. 创建团队 GitHub 仓库
2. 每个成员克隆到 `~/.claude/skills/`
3. 定期运行 `sync_env.py` 同步更新

### 场景 3：快速换电脑

```bash
# 新电脑上
git clone https://github.com/yourusername/claude-env-sync.git ~/.claude/skills/
python ~/.claude/skills/claude-env-sync/env-setup/scripts/sync_env.py --force
```

### 场景 4：版本管理配置

```bash
# 回滚到之前的配置
git log --oneline
git checkout <commit-hash>
python scripts/sync_env.py --force
```

## 工作流程

### 日常更新流程

```
1. 修改本地配置
   ↓
2. 更新 config/ 目录
   ↓
3. git add . && git commit -m "Update xxx"
   ↓
4. git push
   ↓
5. 其他设备: git pull && python scripts/sync_env.py
```

## 注意事项

### MCP 配置同步

- MCP 配置采用**合并模式**，不会覆盖现有的其他 MCP 服务器
- 同一个服务器的配置会被更新
- 敏感信息（API tokens）建议：
  - 使用环境变量
  - 或在 mcp_config.json 中使用占位符，本地手动填充

### 文件覆盖行为

- **不使用 `--force`**：跳过已存在的文件（除了 MCP 配置，始终合并）
- **使用 `--force`**：覆盖已存在的文件

### 重启 Claude Code

同步完成后需要**重启 Claude Code** 才能生效：
- Output styles 会重新加载
- MCP 服务器会重新连接
- CLAUDE.md 会更新

### 跨平台兼容

- 脚本自动处理 Windows/macOS/Linux 路径差异
- 配置文件使用 UTF-8 编码

## 故障排查

### 同步失败

**问题：** "config/output-styles not found"
- **解决：** 确认仓库结构正确，config/ 目录存在

**问题：** ".claude.json not found"
- **解决：** 确认 Claude Code 已安装并运行过一次

**问题：** MCP 配置没有生效
- **解决：** 检查 mcp_config.json 格式是否正确，重启 Claude Code

### Git 相关

**问题：** 推送失败
- **解决：** 检查 GitHub 仓库权限、网络连接

## 高级用法

### 分支管理

```bash
# 创建设备特定配置分支
git checkout -b my-custom-config

# 切换回主配置
git checkout main
```

### 部分同步

```bash
# 只同步风格，保留其他配置
python scripts/sync_env.py --components output_styles

# 只同步 MCP，不改变风格
python scripts/sync_env.py --components mcp_config
```

### 自动化同步（可选）

创建定期同步脚本：

```bash
# sync.sh
#!/bin/bash
cd ~/.claude/skills/claude-env-sync
git pull
python env-setup/scripts/sync_env.py
```

添加到 cron 或 Task Scheduler 定期执行。
