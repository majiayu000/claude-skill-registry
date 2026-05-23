---
name: sister-script
description: Document-first automation — the doc is the source of truth
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
related: [moollm, play-learn-lift, skill, sniffable-python, plain-text, yaml-jazz, constructionism, postel, debugging]
tags: [moollm, automation, documentation, methodology, development]
---

# Sister Script

> **Document-first development. Automate only what's proven.**

The document is the source of truth. Scripts are its children.

> [!TIP]
> **LIFT stage of [play-learn-lift](../play-learn-lift/).** Proven procedures become automation.

## The Pattern

```mermaid
graph TD
    D[📄 Document] -->|manual test| C[💻 Commands]
    C -->|document| P[📋 Procedure]
    P -->|automate| S[🤖 Sister Script]
    S -->|improve| D
```

1. Start with natural language (PLAY)
2. Add manual commands (PLAY/LEARN)  
3. Document working procedures (LEARN)
4. Generate automation (LIFT)

## Bidirectional Evolution

- Document → Script: Proven procedures become automated
- Script → Document: Automation insights improve docs

## Contents

| File | Purpose |
|------|---------|
| [SKILL.md](./SKILL.md) | Full methodology documentation |
| [PROCEDURE.md.tmpl](./PROCEDURE.md.tmpl) | Procedure template |
| [SISTER.yml.tmpl](./SISTER.yml.tmpl) | Sister relationship template |

## The Intertwingularity

Sister-script is the LIFT stage of [play-learn-lift](../play-learn-lift/) — automate proven patterns.

```mermaid
graph LR
    SS[👯 sister-script] -->|LIFT stage of| PLL[🎮📚🚀 play-learn-lift]
    SS -->|automates| DOC[📄 documents]
    SS -->|produces| CODE[🤖 scripts]
    
    RN[📓 research-notebook] -->|feeds| SS
    SL[📜 session-log] -->|source for| SS
```

---

## Sniffable Python: The Structure

Sister scripts should follow [sniffable-python/](../sniffable-python/) conventions:

```python
#!/usr/bin/env python3
"""tool-name: One-line description.

Docstring becomes --help AND is visible to LLM.
"""

import argparse

def main():
    """CLI structure — sniff this to understand the tool."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    # ... CLI tree here ...
    args = parser.parse_args()
    _dispatch(args)

# Implementation below the fold
```

**Why sniffable Python for sister scripts?**
- LLM can read `main()` and understand the CLI
- Human can run `--help` for the same info
- Single source of truth for documentation
- One sniff and you smell success

---

## Directory-Agnostic Invocation

**Critical pattern:** Sister scripts must work when invoked from ANY directory, not just their parent. They find their skill context using the script's own location, not the caller's working directory.

### Python

```python
from pathlib import Path

# Find THIS script's location (not caller's cwd)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent  # If script is in skill/scripts/

# Find sibling files relative to skill, not caller
CONFIG_FILE = SKILL_DIR / "config.yml"
PATTERNS_DIR = SKILL_DIR / "patterns"
```

**Why `__file__`?**
- `Path(__file__)` — path to THIS script file
- `.resolve()` — resolve symlinks to get real location
- `.parent` — containing directory

See [sniffable-python/](../sniffable-python/) for the full Python pattern with templates.

### Bash

```bash
#!/bin/bash
# tool-name: Works from any directory.

# Find THIS script's location (not the caller's cwd)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"  # If script is in skill/scripts/

# Now find sibling files relative to script location
CONFIG_FILE="$SKILL_DIR/config.yml"
PATTERNS_DIR="$SKILL_DIR/patterns"

load_patterns() {
    # Find patterns relative to skill, not caller
    for f in "$PATTERNS_DIR"/*.yml; do
        echo "Loading: $f"
    done
}
```

**Why `BASH_SOURCE[0]}?**
- `$0` can be "bash" if script is sourced
- `${BASH_SOURCE[0]}` always gives the script path
- Works whether script is executed directly or sourced

**Why the subshell `$(cd ... && pwd)`?**
- Resolves relative paths and symlinks
- Returns absolute path without changing caller's cwd

### Why This Matters

| Invocation | Wrong: `pwd` / `getcwd()` | Correct: script location |
|------------|---------------------------|--------------------------|
| `cd skills/foo && python scripts/bar.py` | `skills/foo/` | `skills/foo/scripts/` |
| `python skills/foo/scripts/bar.py` | `/home/user/` | `skills/foo/scripts/` |
| `cd / && bash /path/to/skills/foo/scripts/bar.sh` | `/` | `skills/foo/scripts/` |

**The script finds its own context regardless of where it's invoked from.**

---

## Dovetails With

### Sister Skills
| Skill | Relationship |
|-------|--------------|
| [sniffable-python/](../sniffable-python/) | **The structure** sister scripts should follow |
| [play-learn-lift/](../play-learn-lift/) | Sister-script IS the LIFT stage |
| [session-log/](../session-log/) | Source material for patterns |
| [research-notebook/](../research-notebook/) | Documented procedures |
| [plan-then-execute/](../plan-then-execute/) | Scripts can become plans |

### Protocol Symbols
| Symbol | Link |
|--------|------|
| `SISTER-SCRIPT` | [PROTOCOLS.yml](../../PROTOCOLS.yml#SISTER-SCRIPT) |
| `BUILD-COMMAND` | [PROTOCOLS.yml](../../PROTOCOLS.yml#BUILD-COMMAND) |
| `PLAY-LEARN-LIFT` | [PROTOCOLS.yml](../../PROTOCOLS.yml#PLAY-LEARN-LIFT) |

### Navigation
| Direction | Destination |
|-----------|-------------|
| ⬆️ Up | [skills/](../) |
| ⬆️⬆️ Root | [Project Root](../../) |
| 🎮 Sister | [play-learn-lift/](../play-learn-lift/) |
