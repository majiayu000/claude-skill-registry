---
name: claude-docs-validate
description: >
  Check the health and freshness of locally-stored Claude documentation.
  Use this skill when the user asks about documentation health, broken links,
  stale docs, freshness checks, or wants to validate that their local install
  is up-to-date and all URLs are reachable. Triggers on: "are my docs current",
  "check doc health", "validate documentation", "broken links", "stale docs".
---

# Claude Documentation Validation Skill

Check whether the local documentation clone at `~/.claude-code-docs/` is healthy and up-to-date.

## When to Use This Skill

Activate when the user asks about:
- Documentation freshness or staleness
- Broken links or unreachable docs
- Health checks on their local install
- Whether docs need updating

## Validation Workflow

### Step 1: Check if the metadata is installed

Verify `~/.claude-code-docs/paths_manifest.json` exists. If not:
> Documentation not found. Run this in Claude Code to install:
> ```
> /plugin marketplace add costiash/claude-code-docs
> /plugin install claude-docs@claude-code-docs
> ```

### Step 2: Check freshness

Two signals — when the manifest was last generated (server-side), and when the clone last pulled:
```bash
jq -r '.generated_at' ~/.claude-code-docs/paths_manifest.json          # manifest build time
cd ~/.claude-code-docs && git log -1 --format="%ci %s"                  # clone last updated
```
If the manifest is older than ~24h, the SessionStart hook normally refreshes it on the next
session; a manual refresh is `cd ~/.claude-code-docs && git fetch origin main && git reset --hard origin/main`.

### Step 3: Check the cache status

```bash
~/.claude-code-docs/plugin/scripts/fetch-docs.sh status
```
Reports manifest pages / cached / pending / stale. If pending > 0, suggest `/docs sync`.

### Step 4: Run URL validation (if user asks for it)

Quick spot-check (recommended first), or full scan (1-2 min):
```bash
bash ~/.claude-code-docs/plugin/skills/claude-docs-validate/scripts/validate-paths.sh --quick
bash ~/.claude-code-docs/plugin/skills/claude-docs-validate/scripts/validate-paths.sh
```
These read URLs directly from the manifest. Report the summary (reachable / broken / timed out).
For persistent broken URLs, the upstream page may have moved — report at
https://github.com/costiash/claude-code-docs/issues.

### Step 5: Doc statistics (if user asks for stats/count)

```bash
jq '.pages | length' ~/.claude-code-docs/paths_manifest.json                       # total
jq -r '.pages[].category' ~/.claude-code-docs/paths_manifest.json | sort | uniq -c | sort -rn  # by category
```

## Troubleshooting

| Issue | Solution |
|---|---|
| "Documentation not found" | Plugin not installed or docs not cloned. Re-run `/plugin install claude-docs@claude-code-docs` |
| Many broken URLs | Likely a sitemap change. Run `git pull` first, then re-validate |
| Timeout errors | Network issue or Anthropic site is slow. Try again later |
| "Permission denied" | Check that `~/.claude-code-docs/` is readable |

## Reference Files

- `examples/validate-docs.md` — Example validation workflow
