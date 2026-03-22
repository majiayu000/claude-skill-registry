---
name: opencrow-forensics-toolbox
description: Use the OpenCROW forensics stack for memory dumps, metadata extraction, and carved-file workflows. Use when Codex needs `volatility3`, `exiftool`, `foremost`, or when a full install tracks manual Autopsy setup.
---

# OpenCROW Forensics Toolbox

Use this skill for challenge artifacts that look like disk, memory, firmware, or metadata problems. It covers RAM analysis with `volatility3`, metadata extraction with `exiftool`, and file carving with `foremost`.

## Quick Start

Start the MCP server from the installed CLI:

```bash
opencrow-forensics-mcp
```

Verify the mapped stack:

```bash
python ~/.codex/skills/opencrow-forensics-toolbox/scripts/verify_toolkit.py
```

## Workflow

1. Start with `exiftool` when the artifact is an image, document, archive, or file bundle that may hide metadata clues.
2. Use `foremost` when the challenge is about recovering deleted or embedded files from a blob or disk image.
3. Use `volatility3` when the artifact is a memory dump or live-memory-style capture.
4. If a full profile was installed, use the manual Autopsy step from the installer summary for GUI-heavy disk forensics.
5. Read [references/tooling.md](references/tooling.md) for quick selection notes.
6. Prefer the MCP server operations first: `toolbox_info`, `toolbox_verify`, `toolbox_capabilities`, `forensics_metadata`, `forensics_carve`, and `forensics_memory_inspect`.

## Resources

- `opencrow-forensics-mcp`: stdio MCP server for typed metadata, carving, and memory workflows.
- `scripts/verify_toolkit.py`: confirm that the mapped forensics tools are installed.
- `references/tooling.md`: quick guidance for choosing between memory, metadata, and carving tools.
