---
name: mapping-features
description: Generate behavioral/feature documentation for web apps using code-first analysis. Reads source code and _MAP.md files to produce _FEATURES.md, with optional visual verification via browser automation. Companion to mapping-codebases. Use when documenting app behavior, creating feature inventories, generating behavioral ground truth for agents, or before modifying UI code. Triggers on "map features", "document app behavior", "feature inventory", "what does this app do".
metadata:
  version: 0.3.0
---

# Mapping Features

Generate `_FEATURES.md` files documenting what a web app *does* — screens, flows, states, behavioral invariants. Companion to `mapping-codebases` which documents code *structure*.

**v0.3.0: Code-first architecture.** The code IS the ground truth; screenshots are supplementary verification.

## Prerequisites

1. **mapping-codebases** must have run first (`_MAP.md` files exist)
2. **Claude API key** available (via `api-credentials` skill or `ANTHROPIC_API_KEY` env var)
3. *Optional:* **webctl** for visual verification (not required for `--code-only`)

## Usage

```bash
# Code-only analysis (no browser needed):
python /mnt/skills/user/mapping-features/scripts/featuremap.py \
  --app-url https://example.com --codebase /path/to/repo --code-only

# Full pipeline (code analysis + selective visual verification):
python /mnt/skills/user/mapping-features/scripts/featuremap.py \
  --app-url https://example.com --codebase /path/to/repo

# Incremental update:
python /mnt/skills/user/mapping-features/scripts/featuremap.py \
  --app-url https://example.com --codebase . --incremental
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--app-url` | required | Base URL of the web app |
| `--codebase` | required | Path to repo root (must have `_MAP.md` files) |
| `--output` | `<codebase>/_FEATURES.md` | Output path |
| `--max-pages` | `100` | Cap on pages to discover |
| `--code-only` | `false` | Skip all vision — code analysis only |
| `--verify-only` | `false` | Only run vision on already-analyzed pages |
| `--batch-size` | auto | Pages per batch (auto-detected from environment) |
| `--incremental` | `false` | Only re-process changed pages |
| `--viewport` | `1280x720` | Screenshot viewport (WxH) |
| `--routes` | none | Comma-separated routes or path to routes file |
| `--screenshots-dir` | `<codebase>/screenshots` | Where to store PNGs |
| `--model` | `claude-sonnet-4-6` | Claude model for analysis/vision |
| `--dry-run` / `-n` | `false` | Discover only, print sitemap |

## Architecture: Code-First Pipeline

### Phase 1: DISCOVER
Discovers pages from **code structure**, not browser crawling:
- Scans for HTML files (static sites)
- Detects framework routing conventions (Next.js, SvelteKit, etc.)
- Parses `_MAP.md` for page references
- Supplements with `--routes` for manual seeding

No browser required for discovery.

### Phase 2: ANALYZE
Reads source code for each discovered page and uses Claude API (text, not vision) to generate behavioral descriptions:
- Finds relevant source files (HTML + referenced JS/CSS)
- Includes `_MAP.md` excerpts for code context
- Produces: what the user sees, interactions, invariants, code references

**Code-derived descriptions are usable standalone.** Vision is enrichment, not requirement.

### Phase 3: VERIFY (optional)
Selective visual verification for pages where it adds value:
- Skips error pages (404, 500), gated pages, redirects
- Captures screenshots + accessibility trees via webctl
- Sends to Claude vision API to verify/enrich code descriptions
- Falls back to code description if vision fails

Skipped entirely with `--code-only`. Run only this phase with `--verify-only`.

### Phase 4: ASSEMBLE
Compiles all descriptions into `_FEATURES.md`:
- Source badges indicate code-analyzed vs visually-verified
- Screenshot references only for verified pages
- Status summary with breakdown by source

## Environment-Adaptive Batching

The skill auto-detects the runtime environment and adjusts batch size:

| Environment | Batch Size | Notes |
|-------------|-----------|-------|
| Claude.ai container | 4 pages | Short bash timeouts |
| Claude Code on Web | 12 pages | Longer execution windows |
| Local CLI | Unbatched | Full control |

Override with `--batch-size N`.

Progress is checkpointed after each batch via `_FEATURES_MANIFEST.json`, so work survives if a conversation ends mid-pipeline.

## Incremental Mode

Each run stores page hashes and descriptions in `_FEATURES_MANIFEST.json`. With `--incremental`:
- Code analysis: skips pages with existing descriptions
- Visual verification: skips pages with unchanged screenshots
- Descriptions from previous runs are preserved and merged

## Auth / Gated Pages

Pages requiring authentication are detected during verification (redirect detection + text heuristics) and marked `GATED`. The skill generates step-by-step manual capture instructions in `GATED_PAGES.md`.

## Output Format

```markdown
# _FEATURES.md — App Name
Generated: 2026-03-22T12:00:00+0000
App URL: https://example.com

## Feature Inventory

### Status Summary
- **Documented:** 45 pages
  - Code-analyzed: 40
  - Visually verified: 5
- **Gated (auth required):** 2 pages

### Page Title (`/route`)
> *Derived from source code analysis*

**What the user sees:** Prose description from code analysis.

**Interactions:**
- Button "X" → does Y

**Invariants:**
- Rule 1

**Code:** `src/page.html` :1

---
```

## Relationship to CLAUDE.md

`_FEATURES.md` is the behavioral source of truth. Combined with `_MAP.md` (structural):

1. `mapping-codebases` → `_MAP.md` (structural)
2. `mapping-features` → `_FEATURES.md` (behavioral)
3. Merge both into CLAUDE.md architecture/concepts sections

## Limitations

- Code analysis requires Claude API calls (tokens)
- Visual verification requires webctl + a running app instance
- SPAs with client-side routing may need `--routes` flag
- Auth-gated pages require human intervention for visual verification
- Code analysis quality depends on source code readability
