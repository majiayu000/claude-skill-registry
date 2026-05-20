---
name: opencrow-osint-toolbox
description: Use the OpenCROW OSINT stack for username enumeration, archive lookup, and public search workflows. Use when Codex needs `sherlock`, `waybackpy`, `shodan`, or when a full install tracks manual theHarvester setup.
---

# OpenCROW OSINT Toolbox

Use this skill for challenges that depend on public-source reconnaissance rather than direct target exploitation. It covers username hunting with `sherlock`, historical site lookups with `waybackpy`, and Shodan-backed discovery with the `shodan` CLI and Python client.

## Quick Start

Start the MCP server from the installed CLI:

```bash
opencrow-osint-mcp
```

Verify the mapped stack:

```bash
python ~/.codex/skills/opencrow-osint-toolbox/scripts/verify_toolkit.py
```

## Workflow

1. Use `sherlock` for username reuse checks across public services.
2. Use `waybackpy` when the clue may exist in an archived site snapshot.
3. Use `shodan` when the problem involves public internet exposure, banners, or service fingerprints.
4. If a full profile was installed, treat theHarvester as a manual follow-up tool from the installer summary.
5. Prefer the MCP server operations first: `toolbox_info`, `toolbox_verify`, `toolbox_capabilities`, `osint_username_lookup`, `osint_archive_lookup`, and `osint_shodan_lookup`.

## Resources

- `opencrow-osint-mcp`: stdio MCP server for typed username, archive, and Shodan lookups.
- `scripts/verify_toolkit.py`: confirm that the mapped OSINT tools are installed.
- `references/tooling.md`: quick guidance for choosing OSINT tools.
