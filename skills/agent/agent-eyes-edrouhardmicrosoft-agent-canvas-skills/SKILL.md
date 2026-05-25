---
name: agent-eyes
description: Visual context analyzer for AI agents. Provides screenshots, accessibility scans, DOM snapshots, and element descriptions for web pages. Use when you need to see what a web page looks like, analyze accessibility issues, inspect DOM structure, or get detailed element information. Triggers on requests like "take a screenshot", "check accessibility", "what does this page look like", "analyze the UI", "inspect this element", or any visual/UI analysis task.
---

# Agent Eyes

Visual context analyzer for web pages. Provides AI agents with the ability to "see" web applications through screenshots, accessibility scans, DOM snapshots, and element descriptions.

## Prerequisites

- Python 3.10+
- `uv` package manager (recommended)
- Playwright browsers installed: `playwright install chromium`

## Compact Mode (Token-Efficient Output)

**All commands support `--compact` / `-c` flag** for token-efficient output:

| Mode | Screenshot | DOM | A11y | Total Tokens |
|------|------------|-----|------|--------------|
| Standard | Base64 inline | depth=5, 20 children | Full violations | ~500K+ |
| **Compact** | File path only | depth=3, 10 children | Summary only | **~3-5K** |

Use compact mode when context window size is a concern (which is most of the time).

```bash
# Compact context - reduces ~500K tokens to ~3-5K tokens
uv run $SKILL_DIR/agent_eyes.py context http://localhost:3000 --compact

# Compact screenshot - always saves to file, never returns base64
uv run $SKILL_DIR/agent_eyes.py screenshot http://localhost:3000 --compact

# Compact a11y - returns summary + top N issues only
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000 --compact

# Compact DOM - stricter limits on depth and children
uv run $SKILL_DIR/agent_eyes.py dom http://localhost:3000 --compact
```

## Commands

All commands use `uv run` for automatic dependency management:

```bash
SKILL_DIR=".claude/skills/agent-eyes/scripts"
```

### Screenshot

Capture full page or element screenshots:

```bash
# Full page screenshot (saves to .canvas/screenshots/)
uv run $SKILL_DIR/agent_eyes.py screenshot http://localhost:3000

# Element screenshot
uv run $SKILL_DIR/agent_eyes.py screenshot http://localhost:3000 --selector ".hero"

# Save to specific path
uv run $SKILL_DIR/agent_eyes.py screenshot http://localhost:3000 --output ./tmp/page.png

# Get as base64 (for inline context) - NOT recommended, use --compact instead
uv run $SKILL_DIR/agent_eyes.py screenshot http://localhost:3000 --base64

# RECOMMENDED: Compact mode - always saves to file, never returns base64
uv run $SKILL_DIR/agent_eyes.py screenshot http://localhost:3000 --compact
```

### Accessibility Scan

Run axe-core accessibility analysis:

```bash
# Full page scan (WCAG 2.1 AA)
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000

# Scoped to element
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000 --selector "main"

# WCAG AAA level
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000 --level AAA

# RECOMMENDED: Compact mode - summary + top issues only (~1-2K tokens vs 100K+)
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000 --compact
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000 --compact --max-issues 5
```

### DOM Snapshot

Get simplified DOM tree:

```bash
# Full page DOM
uv run $SKILL_DIR/agent_eyes.py dom http://localhost:3000

# Subtree only
uv run $SKILL_DIR/agent_eyes.py dom http://localhost:3000 --selector ".content"

# Control depth and children
uv run $SKILL_DIR/agent_eyes.py dom http://localhost:3000 --depth 3 --max-children 10

# RECOMMENDED: Compact mode - depth=3, max-children=10, text=50 chars
uv run $SKILL_DIR/agent_eyes.py dom http://localhost:3000 --compact
```

### Describe Element

Get detailed element information (styles, bounding box, attributes):

```bash
uv run $SKILL_DIR/agent_eyes.py describe http://localhost:3000 --selector ".hero-button"
```

### Full Context

Get comprehensive context bundle (screenshot + a11y + DOM + description):

```bash
# Full context for page
uv run $SKILL_DIR/agent_eyes.py context http://localhost:3000

# Focused on element
uv run $SKILL_DIR/agent_eyes.py context http://localhost:3000 --selector ".hero"

# Without screenshot (smaller output)
uv run $SKILL_DIR/agent_eyes.py context http://localhost:3000 --no-screenshot

# RECOMMENDED: Compact mode - file paths only, limited DOM/a11y (~3-5K tokens)
uv run $SKILL_DIR/agent_eyes.py context http://localhost:3000 --compact

# Compact with custom limits
uv run $SKILL_DIR/agent_eyes.py context http://localhost:3000 --compact \
  --dom-depth 2 --max-children 5 --max-issues 5
```

## Output Format

All commands return JSON to stdout:

```json
{
  "ok": true,
  "...": "command-specific fields"
}
```

On error:

```json
{
  "ok": false,
  "error": "Error description"
}
```

### Compact Mode Output Examples

**Compact context output** (~3-5K tokens instead of ~500K):

```json
{
  "ok": true,
  "url": "http://localhost:3000",
  "title": "My App",
  "timestamp": "2026-01-22T10-30-00-000Z",
  "compact": true,
  "screenshot_path": ".canvas/screenshots/2026-01-22T10-30-00-000Z.png",
  "screenshot_size": 443281,
  "dom": {
    "tag": "body",
    "children": [...]
  },
  "a11y_summary": {
    "total_violations": 5,
    "by_severity": {"critical": 1, "serious": 2, "moderate": 2, "minor": 0},
    "top_issues": [
      {"id": "color-contrast", "impact": "serious", "affected_count": 3}
    ]
  }
}
```

**Compact a11y output** (~1-2K tokens instead of ~100K):

```json
{
  "ok": true,
  "total_violations": 15,
  "by_severity": {"critical": 2, "serious": 5, "moderate": 6, "minor": 2},
  "by_category": {"color": 3, "aria": 5, "keyboard": 2},
  "top_issues": [
    {
      "id": "color-contrast",
      "impact": "serious",
      "description": "Elements must have sufficient color contrast...",
      "affected_count": 3,
      "help_url": "https://dequeuniversity.com/rules/axe/..."
    }
  ],
  "passes": 42,
  "incomplete": 3
}
```

## Typical Agent Workflow

1. **Start dev server** (if not running):
   ```bash
   npm run dev &
   ```

2. **Take initial screenshot** to see current state:
   ```bash
   uv run $SKILL_DIR/agent_eyes.py screenshot http://localhost:3000
   ```

3. **Run accessibility scan** to find issues:
   ```bash
   uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000
   ```

4. **Inspect specific element** for details:
   ```bash
   uv run $SKILL_DIR/agent_eyes.py describe http://localhost:3000 --selector ".problematic-button"
   ```

5. **Get full context** for comprehensive analysis:
   ```bash
   uv run $SKILL_DIR/agent_eyes.py context http://localhost:3000 --selector ".hero"
   ```

## Example: Analyze and Fix A11y Issues

```bash
# 1. Get accessibility violations
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000

# Output shows violations like:
# {
#   "ok": true,
#   "violations": [
#     {
#       "id": "color-contrast",
#       "impact": "serious",
#       "description": "Elements must have sufficient color contrast",
#       "nodes": [{"html": "<button class='cta'>..."}]
#     }
#   ]
# }

# 2. Describe the element to understand current styles
uv run $SKILL_DIR/agent_eyes.py describe http://localhost:3000 --selector ".cta"

# 3. Make code changes to fix the contrast issue

# 4. Re-run a11y to verify fix
uv run $SKILL_DIR/agent_eyes.py a11y http://localhost:3000
```

## Notes

- Screenshots are saved to `.canvas/screenshots/` by default with ISO timestamps
- The tool runs headless Chromium via Playwright
- All commands wait for `networkidle` before capturing
- DOM snapshots are simplified to reduce output size
- A11y scans use axe-core, the industry standard accessibility testing engine

## Token Budget Guide

| Operation | Standard Mode | Compact Mode |
|-----------|---------------|--------------|
| Screenshot | ~100-470K tokens (base64) | ~50 tokens (path only) |
| DOM Snapshot | ~50-150K tokens | ~2-3K tokens |
| A11y Scan | ~50-100K tokens | ~500-1K tokens |
| Full Context | ~500K+ tokens | **~3-5K tokens** |

**Recommendation**: Always use `--compact` flag unless you specifically need base64 data for inline image processing. The compact mode reduces token usage by **99%** while preserving all essential information.

### When to Use Each Mode

| Mode | Use Case |
|------|----------|
| Standard | Debugging, when you need full HTML snippets, when feeding to vision model |
| **Compact** | Most agent workflows, design reviews, accessibility audits, CI/CD pipelines |
