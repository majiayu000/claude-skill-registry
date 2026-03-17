---
name: generate-api-docs
description: Generate API documentation for endpoints
version: 1.0.0
author:  Anand Tyagi
source: Claude Code Marketplace
keywords: documentation
---

# generate-api-docs

Generate API documentation for endpoints

## 来源信息

- **原始平台**: Claude Code
- **市场来源**: Claude Code Marketplace
- **原始名称**: generate-api-docs
- **版本**: 1.0.0
- **作者**:  Anand Tyagi
- **关键词**: documentation

## 功能描述

## Context

- API routes: !`find . -path "*/routes/*" -name "*.js" -o -path "*/api/*" -name "*.js" | head -20`
- Current API files: @$ARGUMENTS

## Your task

Generate comprehensive API documentation including:

1. **Endpoint Overview**: Method, URL, purpose
2. **Parameters**: Query params, path params, request body
3. **Request Examples**: Sample requests with curl
4. **Response Examples**: Success and error responses
5. **Status Codes**: All possible HTTP status codes
6. **Authentication**: Required auth if applicable

Format as clear, readable documentation that can be used by other developers.

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
