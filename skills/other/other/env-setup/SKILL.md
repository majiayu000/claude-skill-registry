---
name: env-setup
description: Claude Code 环境一键同步工具。从 GitHub 仓库同步所有配置到本地：output-styles 风格、CLAUDE.md 全局提示词、MCP 服务器配置、Agent 配置、Plugin 配置。适用于多设备统一环境、换电脑恢复、团队共享配置等场景。当用户需要从 GitHub 仓库同步 Claude Code/OpenClaw 环境配置时使用此 skill。
---

# Claude Code & OpenClaw 环境一键同步工具

从 GitHub 仓库一键同步所有配置到本地 Claude Code 和 OpenClaw 环境。

## 功能概述

本 skill 提供**一键同步**功能，将配置从 GitHub 仓库同步到本地：

- **`sync_env.py`** - 同步所有配置到本地

### 同步内容

| 组件 | 来源 | 目标 | 说明 |
|------|------|------|------|
| Output Styles | `config/output-styles/` | `~/.claude/output-styles/` | Claude Code 对话风格 |
| CLAUDE.md | `config/CLAUDE.md` | `~/.claude/CLAUDE.md` | 全局提示词 |
| MCP Config | `config/mcp_config.json` | `~/.claude.json` | MCP 服务器（合并） |
| Agent Configs | `agents/` | `~/.openclaw/agents/` | OpenClaw Agent 配置 |
| MCP Servers | `mcp/` | 集成到 `~/.claude.json` | MCP 服务器独立配置 |
| Plugins | `plugins/` | `~/.openclaw/plugins/` | OpenClaw 插件配置 |

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
│       ├── CLAUDE.md         (全局提示词)
│       └── mcp_config.json   (MCP服务器配置)
├── agents/                   (Agent 配置目录)
│   ├── multimodal-agent/
│   │   ├── AGENT.md
│   │   └── system.md
│   ├── healthcare-monitor/
│   └── ...
├── mcp/                      (MCP 服务器配置)
│   ├── github/
│   │   ├── config.json
│   │   └── README.md
│   ├── lark-mcp/
│   └── ...
└── plugins/                  (插件配置)
    ├── feishu/
    │   └── config.json
    ├── telegram/
    └── ...
```

## 配置目录说明

### agents/ - Agent 配置

用于存放 OpenClaw Agent 的配置：

```
agents/
├── multimodal-agent/
│   ├── AGENT.md           (Agent 描述)
│   └── system.md          (System prompt)
├── healthcare-monitor/
│   ├── AGENT.md
│   └── system.md
└── ...
```

**同步目标：** `~/.openclaw/agents/`

### mcp/ - MCP 服务器配置

用于存放 MCP 服务器的独立配置：

```
mcp/
├── github/
│   ├── config.json         (MCP 服务器配置)
│   └── README.md          (使用说明)
├── lark-mcp/
│   └── ...
└── ...
```

**同步目标：** 集成到 `~/.claude.json` 的 mcpServers

### plugins/ - 插件配置

用于存放 OpenClaw 插件配置：

```
plugins/
├── feishu/
│   └── config.json
├── telegram/
│   └── config.json
└── ...
```

**同步目标：** `~/.openclaw/plugins/`

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

# 4. 复制 agents 配置（如果有）
cp -r ~/.openclaw/agents/* env-setup/agents/

# 5. 提取 MCP 配置（如果有独立配置）
mkdir -p env-setup/mcp
# (手动复制 MCP 服务器配置)

# 6. 提取插件配置（如果有）
mkdir -p env-setup/plugins
# (手动复制插件配置)

# 7. 推送到 GitHub
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

# 3. 重启 Claude Code / OpenClaw Gateway
```

### 三、命令行选项

```bash
# 基本用法（同步所有配置）
python scripts/sync_env.py

# 强制覆盖已存在的文件
python scripts/sync_env.py --force

# 只同步特定组件
python scripts/sync_env.py --components agents mcp plugins

# 指定配置目录
python scripts/sync_env.py --claude-dir "/path/to/.claude" --openclaw-dir "/path/to/.openclaw"
```

**同步选项：**
- `output_styles` - 同步对话风格配置
- `claude_md` - 同步全局 CLAUDE.md
- `mcp_config` - 同步 MCP 服务器配置
- `agents` - 同步 Agent 配置
- `mcp` - 同步独立 MCP 服务器配置
- `plugins` - 同步插件配置

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

**⚠️ 安全提醒：**
- **不要在仓库中提交真实的 API keys 或 tokens！**
- 敏感信息应使用环境变量或本地配置文件（在 .gitignore 中排除）
- 使用占位符标注需要填写的密钥位置，例如：`"GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"`

### Agent 配置

每个 Agent 目录包含：
- `AGENT.md` - Agent 描述和能力说明
- `system.md` - System prompt

### 插件配置

每个插件目录包含：
- `config.json` 或 `config.yaml` - 插件配置

## 使用场景

### 场景 1：多设备环境统一

在多台电脑上保持一致的配置：

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

团队成员共享统一的配置：

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
2. 更新相应目录 (config/, agents/, mcp/, plugins/)
   ↓
3. git add . && git commit -m "Update xxx"
   ↓
4. git push
   ↓
5. 其他设备: git pull && python scripts/sync_env.py
```

## 注意事项

### 配置同步策略

- **MCP 配置**：采用合并模式，不会覆盖现有的其他 MCP 服务器
- **Agent 配置**：直接复制到目标目录，会覆盖同名 Agent
- **插件配置**：直接复制到目标目录，会覆盖同名插件
- **不使用 `--force`**：跳过已存在的文件（除了 MCP 配置，始终合并）
- **使用 `--force`**：覆盖已存在的文件

### 重启应用

同步完成后需要**重启**才能生效：
- **Claude Code** - Output styles 会重新加载
- **OpenClaw Gateway** - Agents/MCP/Plugins 会重新加载

### 敏感信息管理

- **不要提交真实的 API keys 或 tokens**
- 使用环境变量或本地配置文件
- 在 .gitignore 中排除敏感文件

```
# .gitignore 示例
config/mcp_config.json.local
config/secrets/
*.key
*.token
.env
```

### 跨平台兼容

- 脚本自动处理 Windows/macOS/Linux 路径差异
- 配置文件使用 UTF-8 编码

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
# 只同步 agents 和 plugins，不改变其他配置
python scripts/sync_env.py --components agents plugins

# 只同步 MCP，不改变其他配置
python scripts/sync_env.py --components mcp
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

## 故障排查

### 同步失败

**问题：** "config/agents not found"
- **解决：** 确认仓库结构正确

**问题：** ".claude.json not found"
- **解决：** 确认 Claude Code/OpenClaw 已安装并运行过一次

**问题：** Agent 配置没有生效
- **解决：** 检查配置格式是否正确，重启 OpenClaw Gateway

### Git 相关

**问题：** 推送失败
- **解决：** 检查 GitHub 仓库权限、网络连接

### 密钥安全问题

**问题：** 意外提交了密钥
- **解决：** 使用 git filter-branch 或 git filter-repo 从历史中删除

```bash
# 从历史中删除包含密钥的文件
git filter-branch --force --tree-filter 'git rm -f filename' -- --all

# 强制推送
git push origin --force --all
```
