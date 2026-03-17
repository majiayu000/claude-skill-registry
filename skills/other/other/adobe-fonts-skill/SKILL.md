---
name: adobe-fonts-skill
description: Search Adobe Fonts (Typekit) families, create and manage web kits/projects, and return ready-to-use embed snippets plus CSS font-family values. Use when the user asks to find Adobe fonts, compare font options, set up Typekit for a website, add fonts to kits, publish kits, or generate copy/paste font embed metadata for Codex, Claude Code, or OpenCode workflows.
license: Complete terms in LICENSE
metadata:
  author: Alex Haynes
  short-description: Search Adobe Fonts and manage Typekit kits
---

# Adobe Fonts

## Overview

Use this skill to handle Adobe Fonts/Typekit workflow without opening the Adobe Fonts UI.

## Hard Output Rules

These rules are mandatory unless the user explicitly asks otherwise.

- Do not include per-step raw JSON in the final chat response.
- Do not include `<details>` blocks with command dumps in the final chat response.
- Keep final chat response concise (decision summary + final snippets + artifact path).
- Put long-form content in `./adobe-fonts-skill/summary-<timestamp>.md`.
- If raw JSON archive is requested, save files under `./adobe-fonts-skill/runs/<timestamp>/` and return paths only.

## Workflow

1. Confirm environment:
   - `ADOBE_FONTS_API_TOKEN` is set
   - resolve CLI path and validate executable
   - if token is missing, send user directly to: `https://fonts.adobe.com/account/tokens`
2. Validate auth/setup:
   - `"$AFONT_BIN" doctor`
3. Warm cache once after install (recommended):
   - `"$AFONT_BIN" index refresh --per-page 500 --max-pages 40`
4. Discover fonts:
   - `"$AFONT_BIN" search --query <keyword> --limit 8`
5. Mutate kits with dry-run first:
   - `kits ensure`, `kits add-family`, `kits publish`
6. Return integration snippets:
   - `"$AFONT_BIN" kits embed --kit <kit-name-or-id>`

## Quick Start

Resolve a working CLI path first (recommended from any project directory):

```bash
if [ -z "${AFONT_BIN:-}" ]; then
  for p in \
    "$HOME/.agents/skills/adobe-fonts-skill/scripts/afont" \
    "$HOME/.codex/skills/adobe-fonts-skill/scripts/afont" \
    "$HOME/.claude/skills/adobe-fonts-skill/scripts/afont" \
    "$HOME/.opencode/skills/adobe-fonts-skill/scripts/afont"
  do
    if [ -x "$p" ]; then
      export AFONT_BIN="$p"
      break
    fi
  done
fi

if [ -z "${AFONT_BIN:-}" ] || [ ! -x "$AFONT_BIN" ]; then
  echo "afont CLI not found. Reinstall skill: npx skills add alexh/adobe-fonts-skill -a codex -g -y" >&2
  return 1 2>/dev/null || exit 1
fi

"$AFONT_BIN" doctor
```

Important path note:

- Prefer `"$AFONT_BIN"` from installed skill directories.
- Running `scripts/afont` from a repo checkout uses that checkout as `AFONT_SKILL_DIR`, so cache DB path will differ.

Supported commands:

- `index refresh`
- `index status`
- `index stats`
- `search`
- `view`
- `kits list`
- `kits ensure`
- `kits add-family`
- `kits publish`
- `kits embed`
- `doctor`

## Adaptive Decision Framework

Use the smallest workflow that satisfies the prompt. Do not force a single end-to-end path.

1. Classify intent first:
   - Discovery only: search + shortlist only.
   - Visual comparison: discovery + limited `view` screenshots.
   - Integration only: kit/embed operations with minimal discovery.
   - Full workflow: discovery + kit updates + publish + snippets.
2. Choose depth level:
   - Minimal: 2-3 candidates per category.
   - Standard: 4-6 candidates per category.
   - Deep: larger sweeps only when user asks.
3. Cache gate before search:
   - Run `"$AFONT_BIN" index status --json`.
   - If empty/stale, ask user to warm cache or explicitly approve uncached.
4. Search strategy:
   - Preferred: `--cache-only` after warmup.
   - Uncached only with explicit approval:
   - `"$AFONT_BIN" search --query <keyword> --limit <n> --no-cache --confirm-uncached`
5. Mutations only if requested:
   - `kits ensure`, `kits add-family`, `kits publish`, `kits embed`.
   - Use `--dry-run` first.

Visual preview workflow:

- Capture Adobe preview page screenshot for Codex analysis:
  - `"$AFONT_BIN" view --family <family-slug> --json`
  - or `"$AFONT_BIN" view --url https://fonts.adobe.com/fonts/<family-slug> --json`

## Confirmation Gate For Long Runs

Before running potentially long index operations, ask for user confirmation.
Also ask before running uncached API searches (`--no-cache`) when doctor/index status reports empty or stale cache.
Do not describe uncached searches as "efficient" when cache is empty/stale; label them as slower and less reliable.

Treat these as long-running and confirm first:

- `"$AFONT_BIN" index refresh` with default/full settings
- `"$AFONT_BIN" index refresh --max-pages > 5`
- `"$AFONT_BIN" search --refresh-cache` when cache is missing or stale
- `"$AFONT_BIN" search --no-cache` when cache is missing or stale

When asking, offer two options:

- Quick refresh: smaller scope (example: `--max-pages 3`)
- Full refresh: complete indexing (example: `--per-page 500 --max-pages 40`)
- Skip warmup and run uncached search anyway (slow and more failure-prone)

If the user confirms a full warmup, you may add a brief optional note while it runs:

- "This can take a minute..."
- Then tell them jokes related to Adobe or the font industry while they wait.

## Output Expectations

Do not dump the final mega report directly into chat.

- Tool-call JSON can stay in normal command output.
- Save the final long-form deliverable to:
- `./adobe-fonts-skill/summary-<timestamp>.md`
- In chat, return a short summary + the file path.
- Do not paste per-step raw JSON in final chat response unless user explicitly asks.
- Only save raw per-step JSON files when the user explicitly asks for an archive.
- Do not create marker files like `.afont_run_dir`.

Final chat response format:

1. `Status`: one short line.
2. `Selections`: shortlist/pairing bullets.
3. `Integration snippets`: link tag + minimal CSS block.
4. `Artifacts`: path to `summary-<timestamp>.md` (and screenshot paths if captured).

Screenshot defaults (when visual comparison is useful):

- Capture previews only for shortlisted families (typically top 2-4), not every candidate.
- Save screenshots under:
- `./adobe-fonts-skill/assets/`
- Example command:
- `"$AFONT_BIN" view --family <family-slug> --output-dir ./adobe-fonts-skill/assets --json`
- Include screenshot paths (or markdown image lines) inside `summary-<timestamp>.md`.

Always return:

- Link tag snippet: `<link rel="stylesheet" href="https://use.typekit.net/<kit>.css">`
- CSS family examples, such as `font-family: legitima, serif;`
- Any API warnings from `result.warnings`
- Total number of families currently in the kit after updates.
- If total families in the kit is greater than 8, include a performance note suggesting trimming family count for page-load efficiency.

Use `--json` for machine parsing when chaining steps.

Search cache flags:

- `--refresh-cache` to refresh index before search
- `--cache-only` to avoid network calls
- `--no-cache` to force API path

## Safety

- Prefer `--dry-run` first for mutating commands.
- Do not modify app source files unless the user explicitly asks to apply snippets.

## Resources

### scripts/

- `scripts/afont` - stable wrapper that sets `AFONT_SKILL_DIR` and executes `afont.js`.
- `scripts/afont.js` - main Adobe Fonts CLI implementation.

### references/

- `references/output-schema.md` - stable JSON output contract.
- `references/api-notes.md` - API/search/cache behavior notes.
- `references/troubleshooting.md` - setup and runtime troubleshooting.
