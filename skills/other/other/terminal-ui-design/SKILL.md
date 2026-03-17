---
name: terminal-ui-design
description: Use when creating CLI tools, terminal user interfaces (TUI), or any command-line applications. Load for terminal UI design, ASCII art, color schemes, box drawing characters, and polished terminal output. Also use for refactoring boring CLIs into distinctive experiences.
keywords: terminal, cli, tui, ascii, ansi, console, command-line, rich, textual, bubbletea
---

# Terminal UI Design

Create distinctive, production-grade terminal interfaces with intentional aesthetics. Don't just print text—craft an experience.

## Quick Start

Before coding, choose a **bold aesthetic direction**:

| Style | Vibe | Colors | Borders |
|-------|------|--------|---------|
| Cyberpunk | Neon, futuristic | Hot pink #ff00ff, cyan #00ffff, purple #1a0a2e | Block █▀▄ |
| Amber Terminal | Vintage CRT | #ffb000 on black | Double ╔═╗ |
| Minimalist Zen | Clean, focused | Nord palette, cool blues | Rounded ╭─╮ |
| Retro Mainframe | Corporate, formal | Green on black | ASCII-only +-+ |
| Synthwave | 80s nostalgia | Purple, pink gradients | Heavy ┏━┓ |
| Monochrome Brutalist | Stark, bold | Single color + intensity | Heavy ┏━┓ |

**Pick ONE direction and execute it with precision.**

## Design Thinking Checklist

| Question | Decision Point |
|----------|----------------|
| **Purpose** | What problem? Who uses it? What workflow? |
| **Tone** | Pick extreme: cyberpunk, zen, retro, maximalist, playful |
| **Constraints** | Python Rich, Go bubbletea, Rust ratatui, ANSI codes? |
| **Differentiation** | What makes this UNFORGETTABLE? |

## Box Drawing & Borders

Choose borders that match your aesthetic:

```
Single:     ┌─────┐ │   └─────┘  Clean, modern
Double:     ╔═════╗ ║   ╚═════╝  Bold, formal, retro
Rounded:    ╭─────╮ │   ╰─────╯  Soft, friendly
Heavy:      ┏─────┓ ┃   ┗─────┛  Strong, industrial
Dashed:     ┄┄┄┄┄┄ ┆              Light, airy
ASCII:      +-----+ |   +-----+  Retro, universal
Block:      █▀▀▀▀█ ▄   ▀▀▀▀▀    Chunky, brutalist
```

**Pro tip**: Use decorative corners: ◆ ◈ ✦ ⬡ ◢◣◤◥

## Color Strategies

| Strategy | When to Use | Technique |
|----------|-------------|-----------|
| ANSI 16 | Universal compatibility | Classic palette, craft unique combos |
| 256-color | Rich but portable | Gradients, subtle variations |
| True color | Modern terminals | Full spectrum, smooth transitions |
| Monochrome | Elegant constraint | Single color, vary intensity |

**Create atmosphere**:
- Background color blocks for sections
- Gradient fills: ░▒▓█
- Semantic color (avoid cliché red=bad, green=good)
- Reverse video for emphasis
- Dim for secondary, bold for primary

## Typography

The terminal is ALL typography:

| Technique | Effect | Example |
|-----------|--------|---------|
| ASCII art headers | Dramatic intro | `figlet` style banners |
| Text weight | Hierarchy | Bold, dim, normal |
| Decoration | Emphasis | Underline, italic, strikethrough |
| Letter spacing | Headers | H E A D E R |
| Case | Voice | ALL CAPS headers, lowercase body |
| Unicode symbols | Richness | → • ◆ ★ ⚡ λ ∴ ≡ ⌘ ✓ ✗ |
| Custom bullets | Personality | ▸ ◉ ✓ ⬢ › instead of `-` |

```
Block:    ███████╗██╗██╗     ███████╗
Slant:    /___  / / // /     / ____/
Small:    ╔═╗┌─┐┌─┐
Minimal:  [ HEADER ]
```

## Layout & Spatial Composition

Break free from single-column output:

| Element | Usage |
|---------|-------|
| Panels & Windows | Distinct regions with borders |
| Columns | Side-by-side information |
| Tables | Aligned data, Unicode table chars |
| Whitespace | Generous padding, breathing room |
| Density | Match purpose—dense dashboards, sparse wizards |
| Hierarchy | Visual distinction: primary, secondary, chrome |
| Asymmetry | Off-center titles, weighted layouts |

## Motion & Animation

| Element | Examples |
|---------|----------|
| Spinners | ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏, ⣾⣽⣻⢿⡿⣟⣯⣷ |
| Progress bars | ▓░, █▒, [=====>    ], ◐◓◑◒ |
| Typing effects | Character-by-character reveal |
| Transitions | Wipe effects, fade with color intensity |
| Live updates | Streaming data, real-time charts |

## Data Display

| Type | Technique |
|------|-----------|
| Sparklines | ▁▂▃▄▅▆▇█ inline mini-charts |
| Bar charts | Horizontal bars with block chars |
| Tables | Smart sizing, alternating rows, aligned nums |
| Trees | ├── └── │ hierarchies |
| Status | ● green, ○ empty, ◐ partial, ✓ complete |
| Gauges | [████████░░] with percentage |

## Decorative Elements

```
Dividers:   ───── ═════ •••••• ░░░░░░ ≋≋≋≋≋≋
Sections:   ▶ SECTION, [ SECTION ], ─── SECTION ───, ◆ SECTION
Textures:   · ∙ ░ patterns for backgrounds
Icons:       (if Nerd Fonts available)
```

## Anti-Patterns to Avoid

| ❌ Avoid | ✅ Instead |
|---------|-----------|
| Plain unformatted text | Styled output with intent |
| Default colors | Cohesive palette |
| Generic [INFO] prefixes | Styled prefixes with icons |
| Simple ---- dividers | Unicode dividers ───── ═════ |
| Walls of text | Structured panels and sections |
| Generic progress | Creative spinners and bars |
| Boring help | Formatted, aligned help text |
| Inconsistent spacing | Precise alignment |

## Library Quick Reference

| Language | Libraries |
|----------|-----------|
| Python | Rich, Textual, curses, prompt_toolkit |
| Go | Bubbletea, Lipgloss |
| Rust | Ratatui |
| Node.js | Ink, Blessed, cliui |
| Pure | ANSI escape codes |

### ANSI Escape Codes

```
\x1b[1m       Bold
\x1b[3m       Italic
\x1b[4m       Underline
\x1b[31m      Red foreground
\x1b[38;2;R;G;Bm  True color (RGB)
\x1b[2J       Clear screen
\x1b[H        Cursor home
```

## Implementation Pattern

1. **Choose aesthetic** first (cyberpunk, zen, retro, etc.)
2. **Define palette** (2-3 colors + background)
3. **Select border style** (single, double, rounded, block)
4. **Create reusable components** (panel, table, status)
5. **Apply consistently** across all output

## Resources

| File | When to Load |
|------|--------------|
| references/box-drawing.md | Need border character reference |
| references/ansi-codes.md | Need escape code reference |
| references/color-palettes.md | Need pre-defined palettes |

## Exit Criteria (Code Verified)

- Output has intentional aesthetic (not generic)
- Cohesive color palette used throughout
- Borders and typography match chosen style
- No plain text without formatting
- Anti-patterns avoided
