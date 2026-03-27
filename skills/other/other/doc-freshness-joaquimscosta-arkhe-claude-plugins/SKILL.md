---
name: doc-freshness
description: >
  Detect documentation drift, stale references, and cross-document inconsistencies in any project.
  Scans for code-doc drift (API/function changes not reflected in docs), cross-doc drift
  (conflicting information across documents), and stale references (broken links, deleted files,
  outdated versions). Use when checking "doc freshness", "stale docs", "documentation drift",
  "broken links", "outdated documentation", "doc accuracy", "docs out of date", "doc audit",
  "doc health", or "verify documentation".
argument-hint: scan | check <path> | links | drift <path> | cross-doc | claude-md | onboard | report
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Documentation Freshness

Detect documentation drift across any project. Reports findings without auto-fixing.

## Context Discovery

### Priority 1: Configuration

Read `.arkhe.yaml` from project root. Extract `doc-freshness:` section for custom patterns, exclusions, and doc-code mappings.
Extract `doc-health:` section for `output_dir` (used by `report` mode, default: `docs/health`).

### Priority 2: Project Identity

Read `CLAUDE.md` and `README.md` to understand project structure, tech stack, and conventions.

### Priority 3: Documentation Inventory

Run the scanner to discover all documentation files and perform mechanical checks:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scan_freshness.py <project-root>
```

Use `--links-only` for fast mode (links and file refs only, no git staleness).

## Arguments

Parse from `$ARGUMENTS`:

| Mode | Description |
|------|-------------|
| `scan` | Full freshness analysis (all three drift types) |
| `check <path>` | Focused analysis on one file or directory |
| `links` | Broken links and stale references only (script-driven, fast) |
| `drift <path>` | Code-doc drift for a specific doc or doc-code pair |
| `cross-doc` | Cross-document consistency check |
| `report` | Persist structured freshness report to `{output_dir}/` |
| `claude-md` | CLAUDE.md structural drift (plugin counts, components, versions) |
| `onboard` | Suggest/apply tracking frontmatter to docs that need it |
| _(none)_ | Full scan (same as `scan`) |

## Scanning Tiers

Documents are automatically classified into scanning tiers:

| Tier | Detection | Checks Performed |
|------|-----------|-----------------|
| **Basic** | All `.md` files | Broken links, git age classification, backtick-path verification |
| **Deep** | YAML frontmatter with `last_updated` or `version` | Basic + version drift, `last_updated` accuracy, cross-doc consistency |

Tier is auto-detected per file. No configuration needed. The scanner JSON output includes `"tier"` per doc and `"tier_counts"` in the summary.

## Mode Execution

### `scan` (default)

1. Run `scan_freshness.py` for mechanical checks (links, versions, git staleness)
2. Present script findings (broken links table, version mismatches, staleness scores)
3. For stale/very_stale docs: use Grep/Read to check code-doc alignment on key references
4. For docs covering the same topic: cross-check for consistency
5. Produce the freshness report

### `links`

1. Run `scan_freshness.py --links-only`
2. Present broken links table directly from JSON output
3. Group findings by severity: broken links first, then file_ref warnings

### `check <path>`

1. If path is a file, run link checker and version checker on that file only
2. If path is a directory, scan all `.md` files within it
3. Use Grep to check file path references and function names against the codebase
4. Report findings for the targeted scope

### `drift <path>`

1. Read the specified doc
2. Extract: function/method names, API endpoints, file paths, config keys, class names
3. Grep/Read the corresponding code to verify each reference still exists and is accurate
4. Report mismatches with evidence (doc line vs code location)

### `cross-doc`

1. Run `scan_freshness.py` to get doc inventory with headings
2. Identify docs with overlapping topics (shared heading keywords)
3. Read overlapping docs and compare factual claims
4. Flag contradictions (e.g., different version requirements, conflicting setup steps)

### `report`

Same as `scan` but write output to `{output_dir}/{YYYY-MM-DD}-freshness.md`.

### `claude-md`

1. Run `claude_md_checker.py` to compare CLAUDE.md claims against filesystem
2. Present findings by category: plugin counts, component inventories, versions, file paths
3. Highlight undocumented components (CRITICAL) and version mismatches (WARNING)

### `onboard`

1. Run `frontmatter_onboard.py` to find docs without tracking frontmatter
2. Uses whitelist of known-maintained docs (READMEs, custom docs)
3. Generates minimal `title` + `last_updated` frontmatter from git history
4. On user approval, apply with `--apply` flag

## Automation Integration

**SessionStart Hook**: Critical-doc fast scan on session start (5-second timeout)
```bash
/doc:health --critical-only
# Scans: README.md, CLAUDE.md only (root-level critical docs)
```

**PostToolUse Hook** (after `/commit`): Post-commit doc-impact checks
```bash
/doc:health drift
# Checks if modified code files have corresponding documentation
```

**User-Driven (`/loop`)**: Periodic freshness monitoring
```bash
/loop 1h /doc:health links        # Hourly broken-link checks
/loop 4h /doc:health scan         # Full scans every 4 hours
```

## Severity Levels

| Severity | Meaning |
|----------|---------|
| **CRITICAL** | Broken link to deleted file, doc references removed API/function |
| **WARNING** | Version mismatch, function signature changed, doc stale >30 days |
| **INFO** | Minor inconsistency, doc aging (7-30 days), cosmetic drift |

## Output Rules

- **Evidence-based**: every finding backed by file path and line number
- **Tabular**: summary table first, detailed findings below
- **Actionable**: each finding includes what needs updating
- **Detection only**: NEVER auto-fix documentation

## Lane Discipline

- Do NOT update or rewrite documentation — detection only
- Do NOT produce roadmap status, architecture analysis, or user stories
- Do NOT write source code

## References

- [WORKFLOW.md](WORKFLOW.md) — Detection algorithms and convention tables
- [EXAMPLES.md](EXAMPLES.md) — Usage examples for each mode
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes
