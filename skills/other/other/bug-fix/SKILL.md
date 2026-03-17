---
name: bug-fix
description: Streamlines bug fixing by creating a GitHub issue first, then a feature branch for implementing and thoroughly testing the solution before merging.
version: 1.0.0
author: danielscholl
source: Claude Code Marketplace
keywords: claude-code,ai,assistant
---

# bug-fix

Streamlines bug fixing by creating a GitHub issue first, then a feature branch for implementing and thoroughly testing the solution before merging.

## 来源信息

- **原始平台**: Claude Code
- **市场来源**: Claude Code Marketplace
- **原始名称**: bug-fix
- **版本**: 1.0.0
- **作者**: danielscholl
- **关键词**: 无

## 功能描述

Understand the bug: $ARG

Before Starting:
- GITHUB: create a issue with the a short descriptive title.
- GIT: checkout a branch and switch to it.

Fix the Bug

On Completion:
- GIT: commit with a descriptive message.
- GIT: push the branch to the remote repository.
- GITHUB: create a PR and link the issue.

## 使用方法

1. **自动触发**: Codex 会根据任务描述自动选择并使用此技能
2. **手动指定**: 在提示中提及技能名称或相关关键词
3. **斜杠命令**: 使用 `/skills` 命令查看并选择可用技能

## 兼容性

- ✅ Codex CLI
- ✅ Codex IDE 扩展
- ✅ 基于 Agent Skills 开放标准

---
*此技能由 Claude Code 插件自动转换，已适配 Codex 官方技能系统*
