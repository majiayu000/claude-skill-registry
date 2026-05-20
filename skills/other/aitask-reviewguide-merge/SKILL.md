---
name: aitask-reviewguide-merge
description: Compare two similar review guide files and merge, split, or keep separate.
---

## Prerequisites

**If you are Codex CLI:** Read **`.agents/skills/codex_interactive_prereqs.md`** BEFORE proceeding.

## Source of Truth

This is a unified skill wrapper for Codex CLI and Gemini CLI. The authoritative skill definition is:

**`.claude/skills/aitask-reviewguide-merge/SKILL.md`**

Read that file and follow its complete workflow.

**If you are Codex CLI:** For tool mapping and adaptations, read **`.agents/skills/codex_tool_mapping.md`**.

**If you are Gemini CLI:** For tool mapping and adaptations, read **`.agents/skills/geminicli_tool_mapping.md`**.

## Arguments

Accepts 0-2 fuzzy patterns: `security error`. Without arguments, runs batch discovery.
