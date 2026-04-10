---
name: kb-lint
description: Health-check the knowledge bank for orphan documents, stale content, broken WikiLinks, index drift, and missing frontmatter. Generates a severity-graded report. Use this skill whenever the user mentions lint, health check, KB maintenance, stale docs, broken links, orphan pages, missing references, knowledge bank quality, or hasn't run a check in a while. Also trigger when the user asks "what's not cross-referenced?", "are there any dead links?", or expresses concern about KB quality.
user-invocable: true
---

# Knowledge Bank Lint

Health-check the knowledge bank to detect quality issues that accumulate over time. Without periodic linting, orphan documents pile up, cross-references break, and stale content persists unchallenged.

**Knowledge Bank Location**: Read from `~/.claude/plugins/config/second-brain/config.json`.

---

## Invocation

- **Slash command**: `/second-brain:kb-lint`
- **Skill tool**: `Skill({ skill: "second-brain:kb-lint" })`
- **Natural language**: "Run a health check on the knowledge bank", "Find orphan docs in KB"

---

## Workflow

### Step 1: SCAN

Run lint checks in order. Each check produces findings with a severity level.

#### Check 1: Broken WikiLinks (severity: error)

Find WikiLinks that don't resolve to any file in the KB:

```bash
./scripts/lint_broken_links.sh "$KB_PATH"
```

Reuses WikiLink extraction from `knowledge-bank-lookup/scripts/wikilink-utils.sh` and resolution logic.

#### Check 2: Missing Frontmatter (severity: error)

Find documents missing required frontmatter fields (`title`, `type`, `created`):

```bash
./scripts/lint_frontmatter.sh "$KB_PATH"
```

Reuses frontmatter reading from `skills/common/obsidian_helpers.sh`.

#### Check 3: Orphan Documents (severity: warning)

Find documents with zero incoming WikiLinks (not referenced by any other document):

```bash
./scripts/lint_orphans.sh "$KB_PATH"
```

Builds a reverse-link index across the entire KB. Excludes structural files (`_meta/`, `_index/`, `_sessions/`).

#### Check 4: Index Drift (severity: warning)

Find documents that exist on disk but are missing from `_meta/index.md`:

```bash
./scripts/lint_index_drift.sh "$KB_PATH"
```

Compares filesystem against the generated index. Also detects entries in the index that no longer have backing files.

#### Check 5: Stale Documents (severity: info)

Find documents not modified in 90+ days:

```bash
./scripts/lint_stale.sh "$KB_PATH"
```

Uses file modification timestamps. Excludes `_sessions/` and `daily-log/` (inherently historical).

### Step 2: REPORT

Generate a lint report at `_meta/lint-report-YYYY-MM-DD.md`:

```markdown
---
title: KB Lint Report YYYY-MM-DD
type: lint-report
generated: YYYY-MM-DDTHH:MM:SSZ
---

# KB Lint Report

| Severity | Count |
|----------|-------|
| Error    | N     |
| Warning  | N     |
| Info     | N     |

## Errors

### Broken WikiLinks
- [[Target]] referenced from [[Source]] — target not found

### Missing Frontmatter
- /path/to/doc.md — missing: title, type

## Warnings

### Orphan Documents
- [[Doc Name]] — zero incoming references

### Index Drift
- /path/to/doc.md — exists on disk but missing from index

## Info

### Stale Documents
- [[Doc Name]] — last modified YYYY-MM-DD (N days ago)
```

### Step 3: LOG

Append operation to `_meta/log.md`:

```bash
source skills/common/obsidian_helpers.sh
append_kb_log "$KB_PATH" "lint" "kb-lint" "N errors, N warnings, N info findings"
```

---

### Step 4: FIX (optional)

After presenting the report, use **AskUserQuestion tool** to offer resolution:

- **Fix broken WikiLinks** — For each broken link, classify as:
  - **Stub candidate** — the target *should* exist but hasn't been documented yet. Create a stub file with `status: stub` (see below).
  - **Near-match** — an existing doc with a similar name could resolve it. Add an alias to the existing doc.
  - **Bad reference** — the WikiLink itself is wrong (typo, template placeholder). Fix or remove it from the source file.
  - **Template placeholder** — generic WikiLinks like `[[Related Concept 1]]`. Remove from source files.
- **Fix index drift** — Run `generate_index.sh` to rebuild `_meta/index.md`
- **Fix missing frontmatter** — Add required YAML fields to flagged documents
- **Skip** — Just the report, no fixes needed

See [fix-guide.md](references/fix-guide.md) for stub creation templates, classification heuristics, alias resolution, and template placeholder removal details.

---

## Interpreting Results

| Severity | Meaning | Action |
|----------|---------|--------|
| **Error** | Data integrity issue | Fix immediately — broken links mislead lookups |
| **Warning** | Quality degradation | Fix soon — orphans and drift reduce discoverability |
| **Info** | Potential staleness | Review periodically — may need updating or archiving |

---

## Resources

- [KB Schema](_meta/schema.md) — Conventions that lint checks enforce
- [Fix Guide](references/fix-guide.md) — Stub creation, alias resolution, template cleanup

---

## Completion Criteria

| Mode | Complete when |
|------|---------------|
| **Report only** | All 5 checks run, lint report generated, log appended, findings summarized |
| **Report + Fix** | All of above, plus chosen fixes applied, index regenerated |
