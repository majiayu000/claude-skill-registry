---
name: "Architecture Audit"
description: "Comprehensive **project** consistency review across code, documentation, diagrams, and configuration"
---

# Architecture Audit

> Comprehensive **project** consistency review across code, documentation, diagrams, and configuration

## Overview

Systematic audit process to ensure all **project** artifacts stay synchronized. Catches version drift, terminology inconsistencies, outdated diagrams, broken references, and code-to-docs mismatches.

⚠️ **IMPORTANT**: This skill audits the **user's project code**, NOT the Alex cognitive architecture in `.github/`. Ignore `.github/` folder contents when performing audits - focus on the actual source code, documentation, and configuration in the project root and subdirectories.

## Triggers

- "audit", "comprehensive review", "fact-check"
- "consistency check", "project health"
- "pre-release audit", "documentation review"
- Before major releases or after significant refactoring

## Audit Checklist

### 1. Version Consistency

```powershell
# Find version references in common locations
# EXCLUDE: .github/** (Alex cognitive architecture - not project code)
$patterns = @(
    'package.json',           # "version": "x.y.z"
    'src/**/config*.json',    # Version in config files (not .github)
    '*.md',                   # Root documentation only
    'docs/**/*.md',           # Project docs (not .github)
    'src/**/constants.ts',    # Hardcoded versions
    'CHANGELOG.md'            # Version headers
)

# Grep for version patterns
Get-ChildItem -Recurse -Include $patterns |
    Select-String -Pattern 'v?\d+\.\d+\.\d+' |
    Group-Object -Property Line
```

**Check:** All version references match the canonical version (usually package.json)

### 2. Terminology Consistency

Build a deprecated terms list for your project:

| Deprecated Term | Current Term | Migration Pattern |
|-----------------|--------------|-------------------|
| `DK-*.md` | `skills/*/SKILL.md` | File format change |
| `domain-knowledge/` | `skills/` | Folder rename |
| (project-specific) | (project-specific) | (document here) |

```powershell
# Search for deprecated terms (exclude .github/)
$deprecated = @('OLD_TERM_1', 'OLD_TERM_2')
foreach ($term in $deprecated) {
    Get-ChildItem -Recurse -Include "*.md","*.ts","*.json" -Exclude ".github" |
        Where-Object { $_.FullName -notmatch '\\.github\\' } |
        Select-String -Pattern $term
}
```

### 3. Fact Inventory

Maintain a facts file or section with current counts:

```markdown
## Current Facts (Update on Audit)
- Skills: 46 folders
- Commands: 16 total
- Tools: 11 MCP tools
- Agents: 5 custom agents
- Instructions: 19 files
- Prompts: 7 files
```

**Check:** All documentation referencing these counts matches actual values

### 4. Diagram Validation

For each diagram (Mermaid/ASCII):

- [ ] Node labels match current terminology
- [ ] Counts in labels are accurate
- [ ] Flow directions reflect actual data flow
- [ ] Subgroup names are current
- [ ] No references to deprecated concepts

```powershell
# Find all diagrams in project (exclude .github/)
Get-ChildItem -Recurse -Include "*.md" |
    Where-Object { $_.FullName -notmatch '\\.github\\' } |
    Select-String -Pattern '```mermaid|```ascii|┌|╔' |
    Group-Object -Property Path
```

### 5. Cross-Reference Validation

- [ ] Internal links resolve (`[text](path)` → file exists)
- [ ] Anchor links work (`#section-name` → heading exists)
- [ ] Image references valid
- [ ] Import/require statements resolve

```powershell
# Find markdown links in project (exclude .github/)
Get-ChildItem -Recurse -Include "*.md" |
    Where-Object { $_.FullName -notmatch '\\.github\\' } |
    Select-String -Pattern '\[.*?\]\((?!http)[^)]+\)' |
    ForEach-Object {
        # Extract path and verify existence
    }
```

### 6. Code-to-Docs Sync

| Code Artifact | Documentation Location | Check |
|---------------|----------------------|-------|
| Exported functions | API docs | Signatures match |
| Config options | README/User Manual | All options documented |
| CLI commands | Help text / docs | Commands listed |
| Error messages | Troubleshooting | Errors explained |

### 7. Configuration Alignment

- [ ] TypeScript constants match documentation
- [ ] JSON schemas match actual structure
- [ ] Environment variables documented
- [ ] Feature flags documented

## Audit Report Template

```markdown
# Architecture Audit Report
**Date:** YYYY-MM-DD
**Version Audited:** x.y.z
**Auditor:** [name/AI]

## Summary
| Category | Status | Issues Found |
|----------|--------|--------------|
| Version Consistency | ✅/⚠️/❌ | N |
| Terminology | ✅/⚠️/❌ | N |
| Fact Accuracy | ✅/⚠️/❌ | N |
| Diagrams | ✅/⚠️/❌ | N |
| Cross-References | ✅/⚠️/❌ | N |
| Code-Docs Sync | ✅/⚠️/❌ | N |

## Issues Found
### [Category]
- **File:** path/to/file
- **Line:** N
- **Issue:** Description
- **Fix:** Suggested correction

## Actions Taken
- [ ] Issue 1 fixed
- [ ] Issue 2 fixed
```

## Automation Opportunities

### Pre-commit Hook
```bash
# .husky/pre-commit or similar
npm run audit:quick  # Fast checks only
```

### CI Pipeline
```yaml
# GitHub Actions
- name: Architecture Audit
  run: npm run audit:full
  if: github.event_name == 'pull_request'
```

### Scheduled Audit
```yaml
# Weekly full audit
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9am
```

## Anti-Patterns

❌ **Skipping audits before release** — Drift accumulates silently

❌ **Manual-only audits** — Automate what you can

❌ **Fixing without documenting** — Record the pattern for next time

❌ **Ignoring "cosmetic" issues** — They signal deeper drift

❌ **Auditing only changed files** — Drift affects unchanged files too

## Best Practices

✅ **Run full audit before major releases**

✅ **Add new deprecated terms as you migrate**

✅ **Update fact inventory after structural changes**

✅ **Document audit findings for patterns**

✅ **Automate repetitive checks**

✅ **Time-box manual review (don't boil the ocean)**

## Integration with Other Skills

- `release-preflight` → Trigger audit before release
- `architecture-health` → Synapse-specific validation
- `code-review` → Audit as part of PR review
- `refactoring-patterns` → Audit after major refactoring

## Synapses

- [release-preflight/SKILL.md] (High, Enables, Forward) - "Pre-release audit trigger"
- [architecture-health/SKILL.md] (High, Complements, Bidirectional) - "Health + consistency"
- [code-review/SKILL.md] (Medium, Extends, Forward) - "Broader than code"
- [refactoring-patterns/SKILL.md] (Medium, Triggers, Backward) - "Post-refactor audit"
- [self-actualization.instructions.md] (Medium, Complements, Bidirectional) - "Architecture introspection"
