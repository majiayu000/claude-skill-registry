---
name: refresh-research
description: Use when user invokes /refresh-research to re-fetch refreshable research sources, detect meaningful changes, and update synthesis files. Supports specific files, categories, staleness thresholds, backfill of source_type, and audit-only dry runs.
dependencies: python>=3.10
---

# Research Refresh Protocol

## Overview

Re-fetch live research sources (repos, docs), detect meaningful changes since initial capture, and update synthesis files. Raw sources are versioned (never overwritten), syntheses are surgically updated, and INDEX.md is rebuilt.

**Core principles:**
1. **Only refreshable sources are fetched.** `repo` and `docs` source types. Blogs, papers, videos, and internal docs are static — skip them.
2. **Raw sources are versioned, never overwritten.** New fetch → new file with today's date.
3. **Syntheses are updated, not replaced.** Preserve analysis and structure; update facts.

## When to Use

User types `/refresh-research` followed by:

| Invocation | Behavior |
|------------|----------|
| *(empty)* | Interactive — show stale entries, let user pick which to refresh |
| `research/agent-memory/cognee-architecture.md` | Refresh a specific synthesis file |
| `agent-memory` | All refreshable entries in that category |
| `--all` | All refreshable entries across all categories |
| `--stale 14` | Entries not checked in 14+ days (default threshold: 30) |
| `--backfill` | One-time: add `source_type` to entries missing it |
| `--audit` | Dry-run: staleness report, no modifications |

Flags can be combined: `/refresh-research agent-memory --stale 7`

## Frontmatter Fields

Three optional fields extend the existing synthesis frontmatter:

```yaml
---
tags: [github, memory, open-source]
date: 2026-02-12              # original research date (unchanged meaning)
source: https://docs.cognee.ai/
source_type: docs              # NEW — repo | docs | blog | paper | internal | video
last_checked: 2026-03-16      # NEW — when last verified against source
refresh_status: changed        # NEW — changed | unchanged | dead-link | archived
---
```

- `source_type` gates refresh eligibility — only `repo` and `docs` are refreshable
- `last_checked` is the staleness clock (separate from `date` which means "first captured")
- `refresh_status` is informational only (doesn't gate behavior)

## Source Type Classification Logic

When `source_type` is missing, auto-detect from the `source` URL:

```
github.com/{owner}/{repo}                  → repo
contains "docs." or "/docs" or "/api"      → docs
contains ".io" or ".dev" or ".ai"          → docs (if not a blog path)
contains "blog" or "medium" or "substack"  → blog
contains "arxiv" or ".pdf"                 → paper
starts with "internal" or empty            → internal
contains "youtube" or "youtu.be"           → video
else                                       → blog (safe default, not refreshable)
```

Borderline cases: flag for user confirmation during `--backfill`.

## Workflow (MANDATORY — 8 Steps)

**You MUST follow this order. No skipping steps.**

---

### Step 0: Build Candidate List

Based on invocation mode:

1. **Specific file:** Read that file's frontmatter. If missing `source_type`, auto-detect from URL.
2. **Category:** Scan all `research/{category}/*.md` files.
3. **`--all`:** Scan all `research/**/*.md` files (excluding INDEX.md, README.md, etc.).
4. **`--stale N`:** Scan all, then filter to entries where `last_checked` is missing or older than N days (default 30).
5. **Empty (interactive):** Scan all, display staleness table, ask user which to refresh.
6. **`--backfill`:** Jump to Backfill Mode (see below).
7. **`--audit`:** Jump to Audit Mode (see below).

**Filter to refreshable types:** Only proceed with entries where `source_type` is `repo` or `docs` (auto-detect if missing).

**Display staleness table:**

```
Refreshable entries:
| # | File | Source Type | Last Checked | Days Stale | Status |
|---|------|-------------|-------------|------------|--------|
| 1 | research/agent-memory/cognee-architecture.md | docs | (never) | 33+ | — |
| 2 | research/tools/ntfy.md | docs | 2026-03-11 | 5 | unchanged |
...

N entries eligible for refresh. Proceed with all / pick numbers / cancel?
```

**Confirm with user before proceeding.** Never auto-refresh without confirmation.

---

### Step 1: Fetch Current Content

For each confirmed entry:

**For `repo` source type:**
1. Extract `{owner}/{repo}` from the source URL
2. Fast-path check: `gh api repos/{owner}/{repo} --jq '.pushed_at'`
   - Compare `pushed_at` with `last_checked`
   - If no pushes since last check → mark `unchanged`, update `last_checked`, skip
3. If changed: fetch key content
   - `gh api repos/{owner}/{repo}/git/trees/HEAD?recursive=1 --jq '[.tree[] | select(.type=="blob") | .path]'`
   - Identify README, docs/, key .md files (same logic as `/research` Step 1)
   - Fetch each via `gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | tr -d '\n' | base64 -d`
   - Also fetch: `gh api repos/{owner}/{repo}/releases?per_page=5` for recent releases

**For `docs` source type:**
1. Try Context7 first:
   - `resolve-library-id` with the library/tool name
   - If resolved: `query-docs` for key topics
2. If Context7 has no coverage: fall back to WebFetch on the source URL
3. If 404 or unreachable: mark `refresh_status: dead-link`, update `last_checked`, report to user, skip

**Error handling:**
- 404 / dead link → mark `dead-link`, preserve synthesis, report
- Repo archived → mark `archived`, note in Update Log
- GitHub rate limit → `gh api rate_limit`, report quota, offer to continue or stop

---

### Step 2: Change Detection

For each fetched entry:

1. **Load existing raw source** from `resources/` (find the most recent file matching the topic)
2. **Structural diff** — compare:
   - Section headers (H1-H4)
   - Version numbers (semver patterns)
   - Key content blocks (feature lists, API endpoints, architecture sections)
   - For repos: star count, last commit date, release versions
3. **Classify the change:**
   - **No changes** → mark `unchanged`, update `last_checked` only, skip Steps 3-6
   - **Minor update** → version bump, small section additions, typo fixes
   - **Major update** → new features, architecture changes, breaking changes, significant new content

4. **Report diff summary to user:**

```
## cognee-architecture.md
Source: https://docs.cognee.ai/
Change level: MINOR
- Version bump: 0.5.0 → 0.6.2
- New section: "Streaming Pipeline"
- Updated: "Storage Architecture" (minor wording changes)

Proceed with update? [y/n/skip]
```

**Wait for user confirmation before modifying any files.**

---

### Step 3: Save New Raw Source (Versioned)

Write fetched content to `resources/` with today's date:

- Format: `resources/[topic]-[type]-YYYY-MM-DD.md`
- Examples:
  - `resources/cognee-docs-2026-03-16.md`
  - `resources/ntfy-readme-2026-03-16.md`

**Rules:**
- Old raw files are NEVER deleted or overwritten
- Use the same `[topic]` slug as the original raw source file
- Include a header comment: `<!-- Refresh fetch: YYYY-MM-DD, previous: resources/[old-filename] -->`

**Verify file exists before continuing:** `ls resources/[filename]`

---

### Step 4: Update Synthesis

Based on change classification:

**Minor changes:**
- Surgical section updates — find the specific section, update in place
- Version number bumps in overview/header
- Add new subsections where content was added upstream
- Do NOT rewrite existing analysis paragraphs

**Major changes:**
- Re-synthesize using existing structure as scaffolding
- Preserve: analysis, opinions, cross-references, Bridge to Technical Work
- Update: facts, feature lists, architecture descriptions, version info
- Add new sections for genuinely new content

**Always add an Update Log entry** (before the References section):

```markdown
### Update Log

- **2026-03-16:** Refreshed from source. Version 0.5.0 → 0.6.2. Added Streaming Pipeline section. Updated storage architecture details. ([raw source](resources/cognee-docs-2026-03-16.md))
```

If an `### Update Log` section already exists, append to it.

**Update frontmatter:**
```yaml
last_checked: 2026-03-16  # update to today
refresh_status: changed   # set to changed
```

Leave `date` unchanged — it records when the topic was first researched, not when it was last refreshed.

Keep `source` and `tags` unchanged unless the refresh reveals new relevant tags.

---

### Step 5: Update References Section

Add the new raw source file to the `## References` → `### Raw Sources` list:

```markdown
- `resources/cognee-docs-2026-03-16.md` — Refresh fetch: updated docs content, 2026-03-16
```

Do NOT remove existing raw source entries — they form the version history.

---

### Step 6: Cross-Reference Check (Lightweight)

**Only for major changes:**

1. Search `research/INDEX.md` and `research/**/*.md` for references to the updated entry
2. Check if any related syntheses cite outdated facts that this refresh corrected
3. **Do NOT auto-modify related files** — just flag for user review:

```
Cross-reference alert:
- research/agent-memory/tool-comparison.md references Cognee v0.5.0
  → Cognee is now v0.6.2, comparison may need updating
```

**Skip this step entirely for minor changes.**

---

### Step 7: Rebuild INDEX.md

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/rebuild-research-index.py"
```

Run from the project root. Expected output: `Rebuilt INDEX.md: N entries`

If the script fails, manually update the row in `research/INDEX.md` for the refreshed entry.

**Do NOT skip this step. It is the final required action.**

---

## Backfill Mode (`--backfill`)

One-time migration: add `source_type` to entries missing it.

1. Scan all `research/**/*.md` files
2. For each file missing `source_type` in frontmatter:
   a. Read the `source` field
   b. Auto-classify using the Source Type Classification Logic above
   c. Display classification for user review:
   ```
   Backfill classifications:
   | File | Source URL | Detected Type | Confidence |
   |------|-----------|---------------|------------|
   | cognee-architecture.md | https://docs.cognee.ai/ | docs | high |
   | rowboat.md | https://github.com/rowboatlabs/rowboat | repo | high |
   | agent-memory-landscape-analysis.md | (none) | internal | high |
   | ai-routing-quick-reference.md | (none) | internal | high |
   ...
   ```
   d. Flag borderline cases (confidence: `low`) for user confirmation
   e. After user confirms, write `source_type` into each file's frontmatter
3. Rebuild INDEX.md: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/rebuild-research-index.py"`

**Backfill does NOT refresh content** — it only adds the `source_type` field.

---

## Audit Mode (`--audit`)

Dry-run staleness report. No files are modified.

1. Scan all `research/**/*.md` files
2. Classify each by `source_type` (auto-detect if missing)
3. Calculate staleness from `last_checked` (or `date` if `last_checked` is missing)
4. Output report:

```
# Research Freshness Audit — 2026-03-16

## Summary
- Total synthesis files: 136
- Refreshable (repo/docs): 59
- Non-refreshable (blog/paper/internal/video): 77
- Missing source_type field: 42 (run --backfill to fix)

## Staleness Breakdown
- Never checked: 59
- Checked < 7 days ago: 0
- Checked 7-30 days ago: 0
- Checked 30+ days ago: 0

## Refreshable Entries by Staleness
| File | Source Type | Source | Last Checked | Days Stale |
|------|------------|--------|-------------|------------|
| cognee-architecture.md | docs | docs.cognee.ai | (never) | 33+ |
| ntfy.md | docs | ntfy.sh | (never) | 5 |
...

## Dead Links
(none detected — run refresh to verify)
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| 404 / dead link | Mark `dead-link`, preserve synthesis, report to user |
| Repo archived | Mark `archived`, note in Update Log, preserve synthesis |
| GitHub rate limit | `gh api rate_limit`, report quota, offer to continue or stop |
| No changes detected | Mark `unchanged`, update `last_checked`, report "up to date" |
| Context7 no coverage | Fall back to WebFetch |
| Missing `source_type` | Auto-detect from URL, warn about `--backfill` |
| WebFetch fails | Report error, skip entry, continue with next |
| Frontmatter parse error | Report file, skip entry, continue with next |
| No `source` URL in frontmatter | Skip entry (can't refresh without a source), report |

---

## Quick Reference

### Single File Refresh
1. Read frontmatter → check `source_type` (auto-detect if missing)
2. Confirm with user
3. Fetch current content (gh api for repos, Context7/WebFetch for docs)
4. Compare with existing raw source in `resources/`
5. Classify: unchanged / minor / major
6. Report diff summary → wait for confirmation
7. Save new raw source to `resources/[topic]-[type]-YYYY-MM-DD.md`
8. Verify raw file exists
9. Update synthesis (surgical for minor, re-scaffold for major)
10. Add Update Log entry
11. Update frontmatter (date, last_checked, refresh_status)
12. Update References section
13. Cross-reference check (major changes only)
14. Rebuild INDEX.md

### Category/All Refresh
1. Scan files → filter to refreshable → display staleness table
2. Confirm scope with user
3. Process each entry through the single-file workflow above
4. Final summary: N refreshed, N unchanged, N errors

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Overwrote existing raw source file | Always create a NEW file with today's date |
| Refreshed a blog post or paper | Only `repo` and `docs` are refreshable |
| Skipped user confirmation | Always show diff summary and wait for confirmation |
| Replaced synthesis instead of updating | Preserve analysis; update facts only |
| Deleted old raw source | Never delete — raw sources are the version history |
| Skipped Step 7 (INDEX rebuild) | Always rebuild INDEX.md after any synthesis update |
| Auto-modified cross-referenced files | Only FLAG related files — never auto-modify |
| Used WebFetch for GitHub repos | Use `gh api` for repos — WebFetch is for docs fallback |
| Refreshed without checking `pushed_at` | Fast-path skip if no pushes since `last_checked` |
| Skipped `--backfill` warning | If files are missing `source_type`, suggest `--backfill` |
| Changed `source` URL during refresh | Never change the source URL — it's the canonical reference |
| Forgot Update Log entry | Every refresh that changes content MUST have an Update Log entry |

---

## Red Flags — STOP and Fix

- About to overwrite an existing raw source file
- About to refresh a blog, paper, or internal source
- Modifying synthesis without user confirming the diff summary
- No raw source saved before updating synthesis
- Skipped INDEX.md rebuild
- Auto-editing a file that wasn't the target of the refresh
- No Update Log entry after a content change
- `refresh_status` set to `changed` but no actual content updates made
