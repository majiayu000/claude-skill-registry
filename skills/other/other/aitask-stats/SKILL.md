---
name: aitask-stats
description: Calculate and display statistics of AI task completions (daily, global, per-label).
---

## Source of Truth

This is a unified skill wrapper for Codex CLI and Gemini CLI. The authoritative skill definition is:

**`.claude/skills/aitask-stats/SKILL.md`**

Read that file and follow its complete workflow.

**If you are Codex CLI:** For tool mapping and adaptations, read **`.agents/skills/codex_tool_mapping.md`**.

**If you are Gemini CLI:** For tool mapping and adaptations, read **`.agents/skills/geminicli_tool_mapping.md`**.

## Arguments

Accepts optional flags: `--days N`, `--verbose`/`-v`, `--csv [FILE]`. Example: `--days 14 --verbose`.
