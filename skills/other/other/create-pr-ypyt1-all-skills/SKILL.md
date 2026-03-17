---
name: create-pr
description: |
  Streamlines pull request creation by handling the entire workflow: creating a 
  new branch, committing changes, formatting modified files with Biome, and 
  submitting the PR.
version: 1.0.0
author: toyamarinyon
source: Claude Code Marketplace
keywords: claude-code,ai,assistant

---

# create-pr

Streamlines pull request creation by handling the entire workflow: creating a new branch, committing changes, formatting modified files with Biome, and submitting the PR.

## 来源信息

- **原始平台**: Claude Code
- **市场来源**: Claude Code Marketplace
- **原始名称**: create-pr
- **版本**: 1.0.0
- **作者**: toyamarinyon
- **关键词**: 无

## 功能描述

# Create Pull Request Command

This command automates the process of creating a pull request with several key features:

## Key Behaviors
- Creates a new branch from current changes
- Formats files using Biome
- Automatically splits changes into logical commits
- Generates descriptive commit messages
- Pushes branch to remote repository
- Creates a pull request with summary and test plan

## Commit Splitting Guidelines
- Split commits by feature, component, or concern
- Keep related file changes together
- Separate refactoring from new features
- Ensure each commit is independently understandable
- Separate unrelated changes into distinct commits

The command aims to streamline the code contribution process by providing intelligent commit and pull request creation.

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