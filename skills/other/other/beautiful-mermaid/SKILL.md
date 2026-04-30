---
name: beautiful-mermaid
description: Render Mermaid diagrams as ASCII/Unicode art for terminal display or as SVG files. Use when visualizing flowcharts, state machines, sequence diagrams, class diagrams, or ER diagrams. Supports 17 themes (including vellum, tokyo-night, catppuccin, nord, dracula, github) plus custom colors via --colors JSON.
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
| `--colors JSON` | Custom colors as JSON: `{"bg":"#hex","fg":"#hex","accent":"#hex","line":"#hex","muted":"#hex"}`. Mutually exclusive with `--theme`. |
| `--transparent` | Transparent SVG background (for inlining into themed pages) |
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

## Available Themes (17)

**Dark themes:** zinc-dark, tokyo-night, tokyo-night-storm, catppuccin-mocha, nord, dracula, github-dark, solarized-dark, one-dark, blueprint-dark*

**Light themes:** zinc-light, tokyo-night-light, catppuccin-latte, nord-light, github-light, solarized-light, vellum*

\* = local theme extension (defined in CLI wrapper, not upstream package)

List themes: `node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs --themes`

## When to Use

- **Architecture diagrams** — Visualize system components directly in conversation
- **Data flows** — Show how data moves through a system
- **State machines** — Document application states and transitions
- **Sequence diagrams** — Illustrate API interactions and message flows
- **Class diagrams** — Document object relationships
- **ER diagrams** — Database schema visualization
- **Documentation** — Export SVG for README files and docs

## Cross-Skill Integration

Other skills invoke `beautiful-mermaid` to generate themed diagrams matching their visual identity. Standard pattern:

```bash
# Named theme
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs \
  -f svg -t vellum --transparent -o diagram.svg "graph TD; A-->B-->C"

# Custom colors (for project-specific palettes)
node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs \
  -f svg --colors '{"bg":"#1a1b26","fg":"#a9b1d6","accent":"#7aa2f7"}' \
  -o diagram.svg "graph TD; A-->B-->C"

# ASCII for markdown output (planning, design briefs)
printf 'graph TD\n  A --> B --> C' | \
  node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs -
```

**Theme mapping for consuming skills:**

| Skill | Theme | Notes |
|---|---|---|
| vellum-editorial | `vellum` | Cream/ink/copper; use `--transparent` for inline SVGs |
| Dark slide decks | `blueprint-dark` | Cyan-on-navy for technical presentations |
| minoan-frontend-design | `--colors` | Extract hex from project's DESIGN.md tokens |
| design-md | `github-light` | Neutral light theme for token documentation |
| shape | ASCII mode | Append decision flows to `.design-context.md` |
