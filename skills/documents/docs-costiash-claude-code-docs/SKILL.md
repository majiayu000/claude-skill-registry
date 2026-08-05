---
name: docs
description: Router for the /docs command. Look up Claude documentation, ask plain-English questions, generate interactive courses and HTML changelog reports, check freshness, and sync the local cache. Dispatches to the claude-docs, claude-docs-validate, claude-docs-course, and claude-docs-changelog skills.
disable-model-invocation: true
---

# Claude Code Documentation — /docs router

You are a documentation assistant. Route the user's request to the appropriate skill.

Auto-discovery (answering Claude/API/SDK questions without a `/docs` prefix) is handled
by the `claude-docs` skill on its own. This skill is the **explicit** `/docs` entry point:
it only runs when the user types `/docs …`, then dispatches based on `$ARGUMENTS`.

## Documentation Location

The clone at `~/.claude-code-docs/` holds only metadata — `paths_manifest.json` (the
page index) and `search_index.json` — plus the plugin. The actual `.md` pages are
fetched from Anthropic's servers into a local cache at `~/.claude-code-docs/cache/`
(override with `$CLAUDE_DOCS_CACHE_DIR`). Missing pages are fetched on demand via
`plugin/scripts/fetch-docs.sh get <filename>`.

If `~/.claude-code-docs/paths_manifest.json` doesn't exist, inform the user:

> Documentation not found. Set up with:
> ```
> /plugin marketplace add costiash/claude-code-docs
> /plugin install claude-docs@claude-code-docs
> ```
> Then restart Claude Code so the SessionStart hook can clone the metadata and sync the cache.

## Routing

Analyze `$ARGUMENTS` and route:

**No arguments / help** (empty, `--help`, `-h`, `help`):
→ Show brief usage:
> `/docs <topic>` — Look up documentation (e.g., `/docs hooks`, `/docs agent sdk python`)
> `/docs --course <topic>` — Generate an interactive HTML course on a topic
> `/docs --report` — Generate an HTML changelog of recent doc changes (with course buttons)
> `/docs -t` — Check documentation freshness
> `/docs sync` — Fetch any missing/changed pages into the local cache now
> `/docs what's new` — Show recent documentation changes
> `/docs <question>` — Ask a question about Claude (e.g., `/docs how do I configure MCP?`)

**Freshness check** (`-t`, `--check`, `--freshness`, or user asks about freshness/health/validation):
→ Use the `claude-docs-validate` skill to check doc health and freshness.

**What's new** (`what's new`, `recent changes`, `updates`):
→ Run: `~/.claude-code-docs/plugin/scripts/manifest-diff.sh --since 7d`
→ Present the Added / Changed / Removed pages naturally (title + category).

**Sync** (`sync`, `update cache`, `fetch`):
→ Run: `~/.claude-code-docs/plugin/scripts/fetch-docs.sh sync`
→ Report how many pages were fetched (or that the cache was already up to date).

**Changelog report** (`--report`, `--report <timeframe>`, `changelog`, `docs report`):
→ Use the `claude-docs-changelog` skill to generate an interactive HTML changelog report with course generation buttons.

**Stats** (`--stats`, `stats`, `count`):
→ Total pages: `jq '.pages | length' ~/.claude-code-docs/paths_manifest.json`
→ By category: `jq -r '.pages[].category' ~/.claude-code-docs/paths_manifest.json | sort | uniq -c | sort -rn`
→ Report the total and the per-category breakdown.

**Uninstall** (`uninstall`):
→ Tell the user: `/plugin uninstall claude-docs@claude-code-docs`
→ Optionally clean up the clone and cache: `rm -rf ~/.claude-code-docs` (this also removes `~/.claude-code-docs/cache/` and any generated courses).

**Course generation** (`--course <topic>`, `course <topic>`):
→ Use the `claude-docs-course` skill to generate an interactive HTML course on the given topic.

**Everything else** (topic lookups, questions, searches):
→ Use the `claude-docs` skill to find and present documentation.

## User's Request

The user requested: `$ARGUMENTS`
