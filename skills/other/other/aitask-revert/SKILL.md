---
name: aitask-revert
description: Revert changes associated with completed tasks — fully or partially.
---

## Prerequisites

**If you are Codex CLI:** Read **`.agents/skills/codex_interactive_prereqs.md`** BEFORE proceeding.

**If you are Gemini CLI:** Read **`.agents/skills/geminicli_planmode_prereqs.md`** BEFORE proceeding.

## Source of Truth

This is a unified skill wrapper for Codex CLI and Gemini CLI. The authoritative skill definition is:

**`.claude/skills/aitask-revert/SKILL.md`**

Read that file and follow its complete workflow.

**If you are Codex CLI:** For tool mapping and adaptations, read **`.agents/skills/codex_tool_mapping.md`**.

**If you are Gemini CLI:** For tool mapping and adaptations, read **`.agents/skills/geminicli_tool_mapping.md`**.

## Arguments

Optional task ID argument (e.g., `42` or `t42`). Without argument, presents interactive task discovery.
