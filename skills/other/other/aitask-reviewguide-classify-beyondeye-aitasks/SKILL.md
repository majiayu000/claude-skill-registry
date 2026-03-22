---
name: aitask-reviewguide-classify
description: Classify a review guide file by assigning metadata and finding similar existing guides.
---

## Prerequisites

**If you are Codex CLI:** Read **`.agents/skills/codex_interactive_prereqs.md`** BEFORE proceeding.

## Source of Truth

This is a unified skill wrapper for Codex CLI and Gemini CLI. The authoritative skill definition is:

**`.claude/skills/aitask-reviewguide-classify/SKILL.md`**

Read that file and follow its complete workflow.

**If you are Codex CLI:** For tool mapping and adaptations, read **`.agents/skills/codex_tool_mapping.md`**.

**If you are Gemini CLI:** For tool mapping and adaptations, read **`.agents/skills/geminicli_tool_mapping.md`**.

## Arguments

Accepts an optional fuzzy pattern: `security`. Without argument, runs batch mode.
