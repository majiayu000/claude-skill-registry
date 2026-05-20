---
name: research-frontmatter
description: >-
  Validate and enforce standard YAML frontmatter on research documents with
  JD-aware path resolution. Use when creating, editing, or validating research
  files, when user mentions "research metadata", "research frontmatter",
  "research staleness", "validate research", "RD-rules", or "research docs
  validation".
argument-hint: "validate [path] | schema | staleness | index | resolve-path"
allowed-tools: Read, Glob, Grep, Bash
---

# Research Frontmatter

Enforce standard YAML frontmatter on research documents so GitHub renders metadata as a table and readers can judge staleness.

## Quick Start

```bash
# Validate all research documents
uv run ${CLAUDE_SKILL_DIR}/scripts/validate_research_docs.py --format text

# Check staleness only
uv run ${CLAUDE_SKILL_DIR}/scripts/validate_research_docs.py --staleness-only

# Resolve research path (JD-aware)
uv run ${CLAUDE_SKILL_DIR}/scripts/resolve_research_path.py --format json

# Override research directory
uv run ${CLAUDE_SKILL_DIR}/scripts/validate_research_docs.py --research-dir docs/30-research
```

## Required Frontmatter

Every research file MUST have these 5 fields:

```yaml
---
title: "Human-readable title"
version: "1.0.0"
status: Published           # Published | Draft | Living Document
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

Optional fields (slug, tags, aliases, promoted_at, last_refreshed, sources) MAY follow.

## JD-Aware Path Resolution

The skill auto-detects Johnny.Decimal structure:

1. Look for `.jd-config.json` at project root
2. Find area containing "research" (default: prefix `30`)
3. Construct path: `{root}/{prefix}-{name}/` (e.g. `docs/30-research/`)
4. Fall back to `docs/research/` if no JD config

This applies to both validation and the deep-research promote workflow.

## Validation Rules

| Rule | Severity | Check |
|------|----------|-------|
| RD001 | ERROR | Missing YAML frontmatter |
| RD002-006 | ERROR | Missing required field (title, version, status, created, last_updated) |
| RD007 | ERROR | Invalid status value |
| RD008-009 | WARNING | Invalid date format |
| RD010 | WARNING | Invalid version format |
| RD011 | WARNING | Missing Executive Summary section |
| RD012 | WARNING | Missing References section |
| RD013 | ERROR | Research doc not in README.md index |
| RD014 | WARNING | README index metadata mismatch |
| RD015 | WARNING | Index references missing file |
| RD016 | WARNING | Stale last_updated vs git history |

## Version Increment

- **Patch** (1.0.0 -> 1.0.1): Typo fixes, formatting, minor clarifications
- **Minor** (1.0.0 -> 1.1.0): New sections, updated examples
- **Major** (1.0.0 -> 2.0.0): Complete rewrite, fundamental scope change

## README Index Format

The research README.md MUST use these columns:

```markdown
| Topic | Version | Status | Created | Last Updated |
```

## Integration

- **deep-research**: Promote uses JD-aware path resolution for Tier 2 output
- **doc-freshness**: Research docs with `last_updated` qualify for deep scanning
- **jd-docs**: Area `30-research` is the default research home in JD structure

## Template

New research files should follow the `TEMPLATE.md` in the research directory.

See [WORKFLOW.md](WORKFLOW.md) for detailed procedures.
See [EXAMPLES.md](EXAMPLES.md) for usage examples.
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
