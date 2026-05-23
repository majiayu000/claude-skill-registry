---
name: context-hub
description: "Use Context Hub (chub) for curated, versioned API/SDK docs and agent skills. Keep OpenAI tasks on official docs first."
---

# Context Hub Skill

Use `chub` as a fast retrieval layer for third-party API/SDK integration docs.

## When to Use This Skill

Triggered by:
- "查某个 SDK 的最新用法"
- "这个第三方 API 怎么接"
- "给我某库某版本的示例代码"
- "查文档并按语言返回"
- "搜索某个 provider 的文档条目"

## Prerequisites

1. Install Node.js and npm
2. Install `chub` manually:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 npm install -g --prefix "$HOME/.local" @aisuite/chub
export PATH="$HOME/.local/bin:$PATH"
```
3. Verify:
```bash
chub --cli-version
```

## Routing Policy

1. OpenAI tasks in Claude Code: prioritize official OpenAI docs first (`developers.openai.com` / `platform.openai.com`).
2. Non-OpenAI tasks: prioritize `chub`.
3. If `chub` has no matching entry, fallback to official vendor docs or source code.

## Core Workflow

1. Search the registry:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 chub search "<query>" --limit 10
```
2. Fetch the doc/skill entry with language/version:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 chub get <id> --lang py
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 chub get <id> --lang js --version <version>
```
3. Pull references when needed:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 chub get <id> --file references/<file>.md
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 chub get <id> --full
```
4. Use `--json` when downstream parsing is required.

## Optional Commands (Explicit User Request Only)

Do not run these by default. Run only when the user explicitly asks:

```bash
chub annotate <id> "<note>"
chub feedback <id> up
chub feedback <id> down --label outdated
```

## Guardrails

- Official vendor docs and SDK source code remain the source of truth for high-risk decisions.
- For OpenAI topics, use official OpenAI docs as primary evidence.
- Do not claim behavior that `chub` output does not show.
- Do not auto-send feedback or annotations without explicit consent.
