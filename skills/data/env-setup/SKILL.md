---
name: env-setup
description: AGI 环境一键同步工具。从 GitHub 仓库同步所有配置到本地：Skills 技能库、全局提示词、MCP 服务器配置、Output Styles。支持 Claude Code、Codex CLI、OpenClaw、Pi Coding Agent 等多平台。适用于多设备统一环境、换电脑恢复、团队共享配置等场景。
---

# AGI 环境一键同步工具

从 GitHub 仓库一键同步所有配置到本地 AI 开发环境，支持多平台。

## 支持的平台

| 平台 | Skills 目录 | 配置文件 |
|------|-------------|----------|
| Claude Code | `~/.claude/skills/` | `~/.claude.json`, `~/.claude/CLAUDE.md` |
| OpenClaw | `~/clawd/skills/` | `~/.openclaw/openclaw.json`, `~/clawd/AGENTS.md` |
| Codex CLI | `~/.codex/skills/` | `~/.codex/config.json`, `~/.codex/AGENTS.md` |
| Pi Coding Agent | `~/.pi/skills/` | `~/.pi/config.json` |

## 功能概述

### 同步内容

| 组件 | 来源 | 目标 |
|------|------|------|
| Skills | `skills/` | 各平台 skills 目录 |
| Output Styles | `config/output-styles/` | `~/.claude/output-styles/` |
| 全局提示词 | `config/CLAUDE.md` | 各平台全局提示词 |
| MCP Config | `config/mcp_config.json` | 各平台 MCP 配置 |
| Pass 密钥 | `~/.password-store/` | Git 同步 |

## 快速开始

### 一、克隆仓库

```bash
# 克隆到任意位置
git clone https://github.com/aAAaqwq/cc-skills.git ~/cc-skills
```

### 二、运行同步

```bash
# 同步到所有平台
python ~/cc-skills/env-setup/scripts/sync_env.py --target all

# 只同步到 Claude Code
python ~/cc-skills/env-setup/scripts/sync_env.py --target claude

# 只同步到 OpenClaw
python ~/cc-skills/env-setup/scripts/sync_env.py --target openclaw

# 只同步到 Codex
python ~/cc-skills/env-setup/scripts/sync_env.py --target codex
```

### 三、命令行选项

```bash
# 基本用法
python scripts/sync_env.py

# 指定目标平台
python scripts/sync_env.py --target claude|openclaw|codex|pi|all

# 强制覆盖
python scripts/sync_env.py --force

# 只同步特定组件
python scripts/sync_env.py --components skills mcp_config prompts

# 显示详细信息
python scripts/sync_env.py --verbose
```

**同步选项：**
- `skills` - 同步技能库
- `output_styles` - 同步对话风格
- `prompts` - 同步全局提示词
- `mcp_config` - 同步 MCP 配置

## 仓库结构

```
cc-skills/                    (GitHub 仓库)
├── README.md                 # 仓库说明
├── env-setup/                # 环境同步 skill
│   ├── SKILL.md
│   └── scripts/
│       └── sync_env.py       # 主同步脚本
├── config/                   # 配置模板
│   ├── output-styles/        # 对话风格
│   ├── CLAUDE.md             # Claude Code 全局提示词
│   ├── AGENTS.md             # OpenClaw/Codex 全局提示词
│   └── mcp_config.json       # MCP 服务器配置
├── pass-secrets/             # 密钥管理 skill
├── model-fallback/           # 模型降级 skill
├── openclaw-config/          # OpenClaw 配置 skill
└── ... (其他 skills)
```

## 配置文件格式

### mcp_config.json

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "${CONTEXT7_API_KEY}"]
    }
  },
  "allowedTools": [
    "mcp__github__*",
    "mcp__context7__*"
  ]
}
```

**注意：** 
- 使用 `${VAR_NAME}` 引用环境变量
- 敏感信息建议使用 Pass 管理：`pass api/github`

### AGENTS.md (OpenClaw/Codex 全局提示词)

```markdown
# AGENTS.md - Your Workspace

## First Run
...

## Memory
...

## Safety
...
```

### CLAUDE.md (Claude Code 全局提示词)

```markdown
# CLAUDE.md

## 身份
...

## 工作风格
...
```

## 平台特定配置

### Claude Code

```bash
# 配置位置
~/.claude.json              # MCP 配置
~/.claude/CLAUDE.md         # 全局提示词
~/.claude/output-styles/    # 对话风格
~/.claude/skills/           # Skills 目录
```

### OpenClaw

```bash
# 配置位置
~/.openclaw/openclaw.json                    # 主配置
~/.openclaw/agents/main/agent/models.json    # 模型配置
~/clawd/AGENTS.md                            # 全局提示词
~/clawd/SOUL.md                              # 身份配置
~/clawd/skills/                              # Skills 目录
```

### Codex CLI

```bash
# 配置位置
~/.codex/config.json        # 主配置
~/.codex/AGENTS.md          # 全局提示词
~/.codex/skills/            # Skills 目录
```

## MCP 配置同步

MCP 配置会同步到所有支持的平台：

| 平台 | MCP 配置文件 |
|------|-------------|
| Claude Code | `~/.claude.json` → `mcpServers` |
| OpenClaw | `~/.openclaw/openclaw.json` → `mcp` |
| Codex CLI | `~/.codex/config.json` → `mcpServers` |

### 同步行为

- **合并模式**（默认）：保留现有配置，添加/更新新配置
- **替换模式**：完全替换 MCP 配置

```bash
# 合并模式
python scripts/sync_env.py --components mcp_config

# 替换模式
python scripts/sync_env.py --components mcp_config --replace
```

## 使用场景

### 场景 1：新设备快速配置

```bash
# 1. 克隆仓库
git clone https://github.com/aAAaqwq/cc-skills.git ~/cc-skills

# 2. 同步到所有平台
python ~/cc-skills/env-setup/scripts/sync_env.py --target all --force

# 3. 导入 GPG 密钥（用于 Pass）
gpg --import gpg-private-key.asc

# 4. 克隆密钥库
git clone https://github.com/aAAaqwq/password-store.git ~/.password-store
```

### 场景 2：多平台开发

```bash
# 在 Claude Code 中开发
# 配置自动同步到 ~/.claude/

# 切换到 OpenClaw
python scripts/sync_env.py --target openclaw

# 切换到 Codex
python scripts/sync_env.py --target codex
```

### 场景 3：团队共享配置

```bash
# 团队成员克隆仓库
git clone https://github.com/team/shared-skills.git ~/shared-skills

# 同步配置
python ~/shared-skills/env-setup/scripts/sync_env.py --target all
```

### 场景 4：配置版本管理

```bash
# 更新配置后提交
git add .
git commit -m "Update MCP config"
git push

# 其他设备同步
git pull
python scripts/sync_env.py --target all
```

## 密钥管理集成

使用 `pass-secrets` skill 管理敏感信息：

```bash
# 存储 API 密钥
pass insert api/github
pass insert api/openai

# 在 MCP 配置中引用
{
  "env": {
    "GITHUB_TOKEN": "$(pass api/github)"
  }
}

# 或使用启动脚本
export GITHUB_TOKEN=$(pass api/github)
```

## 故障排查

### 同步失败

**问题：** "Permission denied"
- **解决：** 检查目标目录权限

**问题：** "Config file not found"
- **解决：** 确认平台已安装并运行过一次

**问题：** MCP 配置没有生效
- **解决：** 重启对应的 IDE/Agent

### 平台检测

```bash
# 检测已安装的平台
python scripts/sync_env.py --detect

# 输出示例：
# Claude Code: ✅ ~/.claude/
# OpenClaw: ✅ ~/.openclaw/
# Codex CLI: ❌ not found
# Pi Agent: ❌ not found
```

## 高级用法

### 自定义目标目录

```bash
python scripts/sync_env.py \
  --claude-dir "/custom/path/.claude" \
  --openclaw-dir "/custom/path/.openclaw"
```

### 排除特定 Skills

```bash
python scripts/sync_env.py --exclude backend-tester moltbook-integration
```

### 只同步特定 Skills

```bash
python scripts/sync_env.py --include pass-secrets model-fallback openclaw-config
```

### 自动化同步

创建 cron 任务：

```bash
# 每天同步一次
0 9 * * * cd ~/cc-skills && git pull && python env-setup/scripts/sync_env.py --target all
```

## 相关 Skills

- [pass-secrets](../pass-secrets/SKILL.md) - 密钥管理
- [openclaw-config](../openclaw-config/SKILL.md) - OpenClaw 配置
- [model-fallback](../model-fallback/SKILL.md) - 模型降级
- [mcp-installer](../mcp-installer/SKILL.md) - MCP 安装

---

*由小a维护 - AGI 通用技能库*
