---
name: deepagents-cli
description: 使用 Deep Agents CLI - 终端界面、持久化内存（AGENTS.md）、项目约定、技能目录和 CLI 命令。
language: js
---

# deepagents-cli (JavaScript/TypeScript)

## 概述

具有持久化内存的开源终端编码助手。功能包括：文件操作、shell 执行、网络搜索、HTTP 请求、任务规划、内存、HITL 和技能。

## 安装

```bash
npm install -g deepagents-cli

# 启动 CLI
deepagents
```

## CLI 命令

| 命令 | 描述 |
|---------|-------------|
| `deepagents` | 启动 CLI |
| `deepagents list` | 列出 agents |
| `deepagents skills` | 管理技能 |
| `deepagents help` | 显示帮助 |
| `deepagents reset --agent NAME` | 清除内存 |
| `deepagents threads list` | 列出会话 |
| `deepagents threads delete ID` | 删除会话 |

## 内存 (AGENTS.md)

### 全局内存
`~/.deepagents/<agent_name>/AGENTS.md`

存储：个性、编码偏好、沟通风格

### 项目内存
`.deepagents/AGENTS.md` (需要 `.git` 文件夹)

存储：项目架构、约定、团队指南

## 技能

```bash
# 创建技能
deepagents skills create test-skill

# 项目技能
cd /path/to/project
deepagents skills create test-skill --project
```

位置：
- 全局：`~/.deepagents/<agent_name>/skills/`
- 项目：`.deepagents/skills/`

## 决策表：内存 vs 技能

| 内容 | 位置 | 原因 |
|---------|----------|-----|
| 编码风格 | AGENTS.md (全局) | 始终相关 |
| 项目架构 | AGENTS.md (项目) | 项目上下文 |
| 测试工作流 | 技能 | 任务特定 |
| 大型文档 | 技能 | 按需加载 |

## 注意事项

### 1. 项目根目录需要 .git
```bash
# ❌ 无项目内存
cd /project  # 无 .git
deepagents

# ✅ 初始化 git
git init
deepagents
```

### 2. 技能位置
```bash
# ❌ 错误
/project/skills/SKILL.md

# ✅ 正确
/project/.deepagents/skills/skill-name/SKILL.md
```

### 3. 网络搜索需要 API Key
```bash
export TAVILY_API_KEY="your-key"
deepagents
```

## 完整文档

- [Deep Agents CLI](https://docs.langchain.com/oss/javascript/deepagents/cli)
- [Skills 指南](https://docs.langchain.com/oss/javascript/deepagents/skills)
