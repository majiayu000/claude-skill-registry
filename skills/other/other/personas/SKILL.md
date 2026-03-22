---
name: personas
version: 2.2.6
description: Transform into 20 specialized AI personalities on demand. Switch mid-conversation and load only the active persona.
metadata: {"openclaw":{"requires":{"bins":["python3"],"note":"No API keys needed."}}}
triggers:
  - /persona <name>
  - /persona list
  - /persona exit
  - /personas
  - use persona
  - switch to
  - activate
  - exit persona
categories:
  - core
  - creative
  - learning
  - lifestyle
  - professional
  - curator
personas: 20
---

# Personas 🎭

Use one of 20 built-in personas for specialized help (coding, writing, fitness, medical education, legal orientation, and more).

## Usage

**Activate**
- "Use Dev"
- "Switch to Chef Marco"
- "Activate Dr. Med"

**List personas**
- "List all personas"
- "/persona list"
- "/personas"

**Exit persona mode**
- "Exit persona mode"
- "/persona exit"

## CLI Handler (`scripts/persona.py`)

This script manages the built-in personas and local active-persona state.

```bash
# List all personas
python3 scripts/persona.py --list

# Show one persona markdown file
python3 scripts/persona.py --show dev
python3 scripts/persona.py --show "chef-marco"

# Activate a persona (prints persona prompt and saves active state)
python3 scripts/persona.py --activate luna

# Show current active persona from state file
python3 scripts/persona.py --current

# Reset/deactivate persona mode
python3 scripts/persona.py --reset
```

- State file: `~/.openclaw/persona-state.json`
- Alias support exists for common names (e.g., `chef` → `chef-marco`, `dr` → `dr-med`).
- The CLI does **not** create new persona files.

## Built-in Personas (20)

### Core (5)
Cami, Chameleon Agent, Professor Stein, Dev, Flash

### Creative (2)
Luna, Wordsmith

### Curator (1)
Vibe

### Learning (3)
Herr Müller, Scholar, Lingua

### Lifestyle (3)
Chef Marco, Fit, Zen

### Professional (6)
CyberGuard, DataViz, Career Coach, Legal Guide, Startup Sam, Dr. Med

## Notes

- Only the active persona is loaded when used.
- Medical/legal personas are educational only, not professional advice.
- Personas are bundled in `data/*.md` and can be edited manually by maintainers.