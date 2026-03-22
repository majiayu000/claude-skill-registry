---
name: aitask-pickrem
description: Pick and implement a task in remote/non-interactive mode. All decisions from execution profile - no AskUserQuestion calls.
---

## Plan Mode Prerequisites

**BEFORE executing the workflow**, read **`.opencode/skills/opencode_planmode_prereqs.md`**
and follow its guidance for plan mode phases.

## Source of Truth

This is an OpenCode wrapper. The authoritative skill definition is:

**`.claude/skills/aitask-pickrem/SKILL.md`**

Read that file and follow its complete workflow. For tool mapping and
OpenCode adaptations, read **`.opencode/skills/opencode_tool_mapping.md`**.

## Arguments

Required task ID: `/aitask-pickrem 16` (parent) or `/aitask-pickrem 16_2` (child). Fully autonomous, no interactive prompts.
