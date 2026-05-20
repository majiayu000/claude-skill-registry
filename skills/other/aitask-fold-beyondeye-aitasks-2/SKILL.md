---
name: aitask-fold
description: Identify and merge related tasks into a single task, then optionally execute it.
---

## Plan Mode Prerequisites

**BEFORE executing the workflow**, read **`.opencode/skills/opencode_planmode_prereqs.md`**
and follow its guidance for plan mode phases.

## Source of Truth

This is an OpenCode wrapper. The authoritative skill definition is:

**`.claude/skills/aitask-fold/SKILL.md`**

Read that file and follow its complete workflow. For tool mapping and
OpenCode adaptations, read **`.opencode/skills/opencode_tool_mapping.md`**.

## Arguments

Accepts optional task IDs: `/aitask-fold 106,108,112` or `/aitask-fold 106 108`. Without arguments, follows interactive discovery.
