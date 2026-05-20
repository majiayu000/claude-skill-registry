---
name: aitask-explain
description: "Explain files in the project: functionality, usage examples, and code evolution history traced through aitasks."
---

## Source of Truth

This is an OpenCode wrapper. The authoritative skill definition is:

**`.claude/skills/aitask-explain/SKILL.md`**

Read that file and follow its complete workflow. For tool mapping and
OpenCode adaptations, read **`.opencode/skills/opencode_tool_mapping.md`**.

## Arguments

Accepts optional file/directory paths: `/aitask-explain src/app.py` or `/aitask-explain src/lib/`. Supports line ranges: `path:start-end`.
