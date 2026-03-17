---
name: beautiful-mermaid
description: Render Mermaid diagrams as ASCII/Unicode art for terminal display or as SVG files. Use when visualizing flowcharts, state machines, sequence diagrams, class diagrams, or ER diagrams. Supports 15 themes including tokyo-night, catppuccin, nord, dracula, and github.
user-invocable: false
---

# Beautiful Mermaid

Render Mermaid diagrams as ASCII/Unicode art (for terminal) or SVG (for files).

## Quick Start

```bash
# Render ASCII diagram to terminal
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs "graph LR; A-->B-->C"

# Output:
# ┌───┐     ┌───┐     ┌───┐
# │ A │────►│ B │────►│ C │
# └───┘     └───┘     └───┘
```

## Usage

```bash
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs [options] [input]
```

### Options

| Option | Description |
|--------|-------------|
| `-f, --format TYPE` | Output format: `ascii` (default) or `svg` |
| `-t, --theme NAME` | Theme for SVG output (default: zinc-dark) |
| `-o, --output FILE` | Write to file instead of stdout |
| `--ascii` | Use pure ASCII instead of Unicode box-drawing |
| `--themes` | List available themes |
| `-h, --help` | Show help |

### Input Sources

- **Inline**: `mermaid.mjs "graph TD; A-->B"`
- **File**: `mermaid.mjs diagram.mmd`
- **Stdin**: `echo "graph LR; A-->B" | mermaid.mjs -`

## Examples

### ASCII Output (Terminal)

```bash
# Flowchart with Unicode box-drawing (default)
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs "graph TD; Start-->Process-->End"

# Pure ASCII for maximum compatibility
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs --ascii "graph LR; A-->B"
```

### SVG Output (Files)

```bash
# Create SVG with tokyo-night theme
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs -f svg -t tokyo-night "graph TD; A-->B" -o diagram.svg

# Sequence diagram
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs -f svg -t catppuccin-mocha "sequenceDiagram
Alice->>Bob: Hello
Bob-->>Alice: Hi!" -o sequence.svg
```

## Supported Diagram Types

| Type | Syntax |
|------|--------|
| Flowchart | `graph TD/LR/BT/RL` or `flowchart TD/LR/BT/RL` |
| State | `stateDiagram-v2` |
| Sequence | `sequenceDiagram` |
| Class | `classDiagram` |
| ER | `erDiagram` |

## Available Themes (15)

**Dark themes:** zinc-dark, tokyo-night, tokyo-night-storm, catppuccin-mocha, nord, dracula, github-dark, solarized-dark, one-dark

**Light themes:** zinc-light, tokyo-night-light, catppuccin-latte, nord-light, github-light, solarized-light

List themes: `node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs --themes`

## When to Use

- **Architecture diagrams** — Visualize system components directly in conversation
- **Data flows** — Show how data moves through a system
- **State machines** — Document application states and transitions
- **Sequence diagrams** — Illustrate API interactions and message flows
- **Class diagrams** — Document object relationships
- **ER diagrams** — Database schema visualization
- **Documentation** — Export SVG for README files and docs
