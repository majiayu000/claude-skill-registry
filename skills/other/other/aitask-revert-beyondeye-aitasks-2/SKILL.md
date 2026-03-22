---
name: aitask-revert
description: Revert changes associated with completed tasks — fully or partially.
---

## Plan Mode Prerequisites

**BEFORE executing the workflow**, read **`.opencode/skills/opencode_planmode_prereqs.md`**
and follow its guidance for plan mode phases.

## Source of Truth

This is an OpenCode wrapper. The authoritative skill definition is:

**`.claude/skills/aitask-revert/SKILL.md`**

Read that file and follow its complete workflow. For tool mapping and
OpenCode adaptations, read **`.opencode/skills/opencode_tool_mapping.md`**.

## Arguments

Optional task ID argument (e.g., `42` or `t42`). Without argument, presents interactive task discovery.
