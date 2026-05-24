---
name: mermaid-diagrams
description: Render Mermaid diagrams to SVG using beautiful-mermaid and bun. Use when the user asks to "render mermaid", "generate diagram", "create flowchart", "update diagrams", "render SVG from mermaid", "beautiful-mermaid", "regenerate diagrams", or needs to convert Mermaid diagram syntax into styled SVG files. Supports all Mermaid diagram types with 15 themes including tokyo-night.
---

# Mermaid Diagram Rendering with beautiful-mermaid

Render Mermaid `.mmd` files into styled SVG using [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) v1.0.2 and [bun](https://bun.sh).

## Skill Contents

| File | Purpose |
|------|---------|
| `render-mermaid.ts` | CLI tool: renders `.mmd` files to SVG |
| `gemini-diagram-prompt.md` | Prompt for Gemini image generation |

## Installation

Only **bun** is required. The `beautiful-mermaid` dependency is auto-installed by bun on first run.

```bash
# macOS
brew install oven-sh/bun/bun

# Or universal installer
curl -fsSL https://bun.sh/install | bash
```

## CLI Reference

```
render-mermaid — Render Mermaid .mmd files to themed SVG

Usage:
  bun run render-mermaid.ts [options] <input.mmd...>
  echo 'graph TD; A-->B' | bun run render-mermaid.ts -o out.svg

Options:
  -o, --output <file>   Output file (single input only)
  --outdir <dir>        Output directory for multiple files
  -t, --theme <name>    Theme (default: tokyo-night)
  --list-themes         List available themes
  --help                Show this help
```

**Output defaults:** Without `-o` or `-d`, writes `<name>.svg` next to each input file.

**Shorthand:** Set `MERMAID=plugins/autorun/skills/mermaid-diagrams/render-mermaid.ts` for shorter commands.

## Examples

```bash
MERMAID=plugins/autorun/skills/mermaid-diagrams/render-mermaid.ts

# Render single file (output next to input)
bun run $MERMAID diagram.mmd

# Render to specific output
bun run $MERMAID diagram.mmd -o pretty.svg

# Render all .mmd files to output directory
bun run $MERMAID docs/diagrams/*.mmd --outdir docs/diagrams

# Different theme
bun run $MERMAID -t dracula diagram.mmd

# Pipe from stdin
echo 'graph TD; A-->B-->C' | bun run $MERMAID -o quick.svg

# List themes
bun run $MERMAID --list-themes
```

## Project Diagrams

Mermaid source files (`.mmd`) and rendered output (`.svg`) in `docs/diagrams/`:

| Source | Description |
|--------|-------------|
| `docs/diagrams/autofile-policy.mmd` | AutoFile policy flowchart |
| `docs/diagrams/three-stage-autorun.mmd` | Three-stage autorun flowchart |
| `autorun-architecture.mmd` | Full architecture (too complex for beautiful-mermaid) |

Regenerate:

```bash
bun run $MERMAID docs/diagrams/*.mmd --outdir docs/diagrams
```

## Known Limitations

- Complex diagrams with deeply nested subgraphs may hit dagre layout bugs. Failed diagrams are reported but don't block other renders.
- `%%{init:...}%%` front matter is stripped automatically (beautiful-mermaid applies its own theming).

## Gemini Image Generation

`gemini-diagram-prompt.md` contains a prompt for Gemini to generate an outcome-focused project overview image. Copy the prompt into a Gemini conversation.
