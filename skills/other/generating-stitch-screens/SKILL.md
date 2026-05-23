---
name: generating-stitch-screens
description: >
  Generates Stitch screens from authored prompt files using MCP tools. Reads prompt
  sections, sends each to Stitch for generation, and fetches resulting images and code.
  Use when user mentions "generate in stitch", "create stitch screens", "run prompts in
  stitch", "send prompts to stitch", "generate screens from prompts", "fetch stitch
  images", or has prompt-v*.md files ready for generation. Requires Stitch MCP server.
---

# Generating Stitch Screens

Orchestrate screen generation in Google Stitch using MCP tools. Reads authored prompt files, sends each section to Stitch for generation, and fetches resulting images and code.

## Prerequisites

Requires Stitch MCP server (`@_davideast/stitch-mcp`). If MCP tools are not available, display:

```
Stitch MCP is not configured.
Run /stitch-setup for guided setup, or see the plugin README for manual configuration.
```

Never fail silently. Always inform the user if MCP is unavailable.

Typically invoked via `/stitch-generate` or after prompt authoring with MCP available.

## Quick Start

1. **Read prompt file** from `design-intent/google-stitch/{feature}/prompt-v{N}.md`
2. **Parse sections** by `---` separators, extracting `<!-- Layout: -->` and `<!-- Component: -->` markers
3. **Create or select project** via MCP (`create_project` / `list_projects`)
4. **Generate screens** — for each section: call `generate_screen_from_text` with prompt text
5. **Fetch images** — for each screen: call `fetch_screen_image` at full resolution, save to `{feature}/exports/` (see [WORKFLOW.md](WORKFLOW.md) for URL transformation)
6. **Fetch code** (optional) — call `fetch_screen_code`, save to `{feature}/code/`
7. **Extract design context** (optional) — call `extract_design_context`, save design DNA
8. **Report** — project URL, screen list, file paths

## Output Structure

```
design-intent/google-stitch/{feature}/
├── prompt-v{N}.md              <- Source prompts
├── exports/                    <- Generated images
│   ├── {layout-name}.png
│   ├── {component-1}.png
│   └── {component-2}.png
├── code/                       <- Generated code (optional)
│   ├── {layout-name}/
│   └── {component-1}/
└── design-dna.md               <- Extracted design context (optional)
```

## Section Parsing

Prompt files use `---` separators with HTML comment labels:

```markdown
<!-- Layout: Analytics Dashboard -->
[layout prompt text]

---

<!-- Component: KPI Metrics -->
[component prompt text]

---

<!-- Component: Revenue Chart -->
[component prompt text]
```

Parse each section independently. Use the label text as the screen name in Stitch.

## Error Handling

- **Partial failure**: If some screens fail to generate, continue with remaining sections and report failures
- **Generation timeout**: Wait, then retry once. If still pending, report and suggest checking Stitch directly
- **Empty result from fetch**: Generation may still be in progress — wait briefly and retry

## Workflow Details

See [WORKFLOW.md](WORKFLOW.md) for detailed steps, error handling, and retry logic.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for end-to-end generation scenarios.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for MCP-specific issues.
