---
name: exa
description: 使用 Exa.ai API 进行高质量的互联网搜索。需要 EXA_API_KEY 环境变量。
---

# Exa.ai 搜索技能

一个简单的 Exa API 封装。

## 执行环境

| 路径类型 | 路径 | 基准目录 |
|---------|------|---------|
| **技能目录** | `~/.pi/agent/skills/exa/` | 固定位置 |
| **使用方式** | API 调用，`pi` 自动激活 | 无需手动执行 |

## 安装

```bash
cd ~/.pi/agent/skills/exa
pnpm install exa-js
```

## 配置

在你的环境变量中设置 `EXA_API_KEY`。

## 用法

`pi` 会自动调用此技能进行搜索，无需手动执行命令。

## 路径说明

- **无需本地脚本执行**：此技能通过 API 调用使用
- **依赖位置**：`~/.pi/agent/skills/exa/` 包含依赖包和配置
- **环境变量**：`EXA_API_KEY` 需在系统环境变量中设置
