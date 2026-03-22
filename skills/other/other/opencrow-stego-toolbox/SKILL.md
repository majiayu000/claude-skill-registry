---
name: opencrow-stego-toolbox
description: Use the OpenCROW steganography stack for hidden-data triage and extraction. Use when Codex needs `steghide`, `zsteg`, or when a full install tracks manual StegSolve or OpenStego setup.
---

# OpenCROW Stego Toolbox

Use this skill for image or audio artifacts that may hide data in metadata, bit planes, or container structures. It covers `steghide` for embedded payload extraction and `zsteg` for PNG/BMP stego triage.

## Quick Start

Start the MCP server from the installed CLI:

```bash
opencrow-stego-mcp
```

Verify the mapped stack:

```bash
python ~/.codex/skills/opencrow-stego-toolbox/scripts/verify_toolkit.py
```

## Workflow

1. Start with `zsteg` when the target is a PNG or BMP and you suspect LSB or plane-based data hiding.
2. Start with `steghide` when the file type matches its embedding model and a passphrase may be involved.
3. Combine this toolbox with `opencrow-forensics-toolbox` when metadata or carved files may be involved too.
4. If a full profile was installed, use the manual StegSolve or OpenStego steps from the installer summary for GUI-assisted analysis.
5. Prefer the MCP server operations first: `toolbox_info`, `toolbox_verify`, `toolbox_capabilities`, `stego_inspect`, and `stego_extract`.

## Resources

- `opencrow-stego-mcp`: stdio MCP server for typed stego inspection and extraction workflows.
- `scripts/verify_toolkit.py`: confirm that the mapped stego tools are installed.
- `references/tooling.md`: quick guidance for choosing stego tools.
