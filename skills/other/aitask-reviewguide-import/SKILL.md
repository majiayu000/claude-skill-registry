---
name: aitask-reviewguide-import
description: Import external content (file, URL, or repository directory) as a reviewguide with proper metadata.
---

## Source of Truth

This is an OpenCode wrapper. The authoritative skill definition is:

**`.claude/skills/aitask-reviewguide-import/SKILL.md`**

Read that file and follow its complete workflow. For tool mapping and
OpenCode adaptations, read **`.opencode/skills/opencode_tool_mapping.md`**.

## Arguments

Accepts an optional source: `/aitask-reviewguide-import https://...` or `/aitask-reviewguide-import path/to/file.md`. Without argument, prompts for source.
