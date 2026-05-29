---
name: aitask-pick
description: Select the next AI task for implementation from the `aitasks/` directory.
---

## Plan Mode Prerequisites

**BEFORE executing the workflow**, read **`.opencode/skills/opencode_planmode_prereqs.md`**
and follow its guidance for plan mode phases.

## Source of Truth

This is an OpenCode wrapper. The authoritative skill definition is:

**`.claude/skills/aitask-pick/SKILL.md`**

Read that file and follow its complete workflow. For tool mapping and
OpenCode adaptations, read **`.opencode/skills/opencode_tool_mapping.md`**.

## Arguments

Accepts an optional task ID: `/aitask-pick 16` (parent) or `/aitask-pick 16_2` (child). Without argument, follows interactive selection.
