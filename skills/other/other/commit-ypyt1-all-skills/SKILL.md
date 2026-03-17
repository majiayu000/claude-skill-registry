---
name: commit
description: Creates git commits using conventional commit format with appropriate emojis, following project standards and creating descriptive messages that explain the purpose of changes.
version: 1.0.0
author: evmts
source: Claude Code Marketplace
keywords: claude-code,ai,assistant
---

# commit

Creates git commits using conventional commit format with appropriate emojis, following project standards and creating descriptive messages that explain the purpose of changes.

## 来源信息

- **原始平台**: Claude Code
- **市场来源**: Claude Code Marketplace
- **原始名称**: commit
- **版本**: 1.0.0
- **作者**: evmts
- **关键词**: 无

## 功能描述

# Commit Command

This slash command is a Git commit helper that:

1. Runs pre-commit checks by default (linting, building, generating docs)
2. Automatically stages files if none are staged
3. Analyzes code changes to suggest potential commit splits
4. Creates commits using conventional commit format with descriptive emojis

## Key Features
- Supports options like `--no-verify` to skip pre-commit checks
- Encourages "atomic commits" with focused, logical changes
- Provides a comprehensive list of commit types and corresponding emojis
- Offers guidelines for splitting complex commits

## Example Commit Messages
- "✨ feat: add user authentication system"
- "🐛 fix: resolve memory leak in rendering process"
- "📝 docs: update API documentation with new endpoints"

The command aims to improve code quality, commit clarity, and developer workflow by providing structured commit guidance.

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
