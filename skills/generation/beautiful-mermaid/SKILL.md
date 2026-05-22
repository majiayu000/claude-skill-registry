---
name: beautiful-mermaid
description: Render Mermaid diagrams as SVG and PNG using the Beautiful Mermaid library. Use when the user asks to render a Mermaid diagram.
---

# Beautiful Mermaid Diagram Rendering

Render Mermaid diagrams as SVG and PNG images using the Beautiful Mermaid library.

## Dependencies

This skill requires the `agent-browser` skill for PNG rendering. Load it before proceeding with PNG capture.

## Supported Diagram Types

- **Flowchart** - Process flows, decision trees, CI/CD pipelines
- **Sequence** - API calls, OAuth flows, database transactions
- **State** - State machines, connection lifecycles
- **Class** - UML class diagrams, design patterns
- **Entity-Relationship** - Database schemas, data models

## Available Themes

Default, Dracula, Solarized, Zinc Dark, Tokyo Night, Tokyo Night Storm, Tokyo Night Light, Catppuccin Latte, Nord, Nord Light, GitHub Dark, GitHub Light, One Dark.

If no theme is specified, use `default`.

## Common Syntax Patterns

### Flowchart Edge Labels

Use pipe syntax for edge labels:

```mermaid
A -->|label| B
A ---|label| B
```

Avoid space-dash syntax which can cause incomplete renders:

```mermaid
A -- label --> B   # May cause issues
```

### Node Labels with Special Characters

Wrap labels containing special characters in quotes:

```mermaid
A["Label with (parens)"]
B["Label with / slash"]
```

## Workflow

### Step 1: Generate or Validate Mermaid Code

If the user provides a description rather than code, generate valid Mermaid syntax. Consult `references/mermaid-syntax.md` for full syntax details.

### Step 2: Render SVG

Run the rendering script to produce an SVG file:

```bash
bun run scripts/render.ts --code "graph TD; A-->B" --output diagram --theme default
```

Or from a file:

```bash
bun run scripts/render.ts --input diagram.mmd --output diagram --theme tokyo-night
```

Alternative runtimes:
```bash
npx tsx scripts/render.ts --code "..." --output diagram
deno run --allow-read --allow-write --allow-net scripts/render.ts --code "..." --output diagram
```

This produces `<output>.svg` in the current working directory.

### Step 3: Create HTML Wrapper

Run the HTML wrapper script to prepare for screenshot:

```bash
bun run scripts/create-html.ts --svg diagram.svg --output diagram.html
```

This creates a minimal HTML file that displays the SVG with proper padding and background.

### Step 4: Capture High-Resolution PNG with agent-browser

Use the agent-browser CLI to capture a high-quality screenshot. Refer to the `agent-browser` skill for full CLI documentation.

```bash
# Set 4K viewport for high-resolution capture
agent-browser set viewport 3840 2160

# Open the HTML wrapper
agent-browser open "file://$(pwd)/diagram.html"

# Wait for render to complete
agent-browser wait 1000

# Capture full-page screenshot
agent-browser screenshot --full diagram.png

# Close browser
agent-browser close
```

For even higher resolution on complex diagrams, increase the viewport further or use the `--padding` option when creating the HTML wrapper to give the diagram more space.

### Step 5: Clean Up Intermediary Files

After rendering, remove all intermediary files. Only the final `.svg` and `.png` should remain.

Files to clean up:
- The HTML wrapper file (e.g., `diagram.html`)
- Any temporary `.mmd` files created to hold diagram code
- Any other files created during the rendering process

```bash
rm diagram.html
```

If a temporary `.mmd` file was created, remove it as well.

## Output

Both outputs are always produced:
- **SVG**: Vector format, infinitely scalable, small file size
- **PNG**: High-resolution raster, captured at 4K (3840×2160) viewport with minimum 1200px diagram width

Files are saved to the current working directory unless the user explicitly specifies a different path.

## Theme Selection Guide

| Theme | Background | Best For |
|-------|------------|----------|
| default | Light grey | General use |
| dracula | Dark purple | Dark mode preference |
| tokyo-night | Dark blue | Modern dark aesthetic |
| tokyo-night-storm | Darker blue | Higher contrast |
| nord | Dark arctic | Muted, calm visuals |
| nord-light | Light arctic | Light mode with soft tones |
| github-dark | GitHub dark | Matches GitHub UI |
| github-light | GitHub light | Matches GitHub UI |
| catppuccin-latte | Warm light | Soft pastel aesthetic |
| solarized | Tan/cream | Solarized colour scheme |
| one-dark | Atom dark | Atom editor aesthetic |
| zinc-dark | Neutral dark | Minimal, no colour bias |

## Troubleshooting

### Theme not applied

Check the render script output for the `bg` and `fg` values, or inspect the SVG's opening tag for `--bg` and `--fg` CSS custom properties.

### Diagram appears cut off or incomplete

- Check edge label syntax — use `-->|label|` pipe notation, not `-- label -->`
- Verify all node IDs are unique
- Check for unclosed brackets in node labels

### Render produces empty or malformed SVG

- Validate Mermaid syntax at https://mermaid.live before rendering
- Check for special characters that need escaping (wrap in quotes)
- Ensure flowchart direction is specified (`graph TD`, `graph LR`, etc.)
