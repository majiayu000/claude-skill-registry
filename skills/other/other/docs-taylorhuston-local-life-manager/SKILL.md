---
name: docs
description: "Documentation health check and maintenance across all ideas. Use for periodic maintenance, finding gaps, and keeping docs accurate."
model: claude-haiku-4-5-20251001
allowed-tools: Read, Edit, Glob, Grep
---

# /docs

Documentation health check, validation, and maintenance.

## Usage

```bash
/docs --health                   # Overall health report
/docs --validate                 # Check broken links, missing files
/docs --stale                    # Find documents >30 days old
/docs --sync                     # Sync CLAUDE.md with project state
/docs --project coordinatr       # Focus on specific project
```

## Flags

| Flag | Purpose |
|------|---------|
| `--health` | Comprehensive health report with scores |
| `--validate` | Check links, references, required files |
| `--stale` | Find outdated documentation |
| `--sync` | Update CLAUDE.md with current status |
| `--project` | Focus on specific project |

## Health Report

```
## Documentation Health Report

### Overall Score: 72/100

### By Project
| Project | Brief | Critique | Specs | Issues | Score |
|---------|-------|----------|-------|--------|-------|
| Coordinatr | ✓ | ✓ | 2 | 3 | 85 |
| YourBench | ✓ | ✗ | 1 | 0 | 60 |

### Recommendations
1. Run /critique on [project]
2. Create project-brief.md for [project]
```

## Validation Report

```
## Validation Report

### Broken Links
- ideas/coordinatr/README.md:15 -> ../specs/SPEC-001.md (not found)

### Missing Required Files
- ideas/irl-social/project-brief.md

### Orphaned Files
- ideas/shared/docs/old-research.md (not referenced)

### Structure Issues
- ideas/lorecraft/ missing issues/ directory
```

## Health Scoring

| Component | Weight |
|-----------|--------|
| README.md | 20% |
| project-brief.md | 25% |
| critique.md | 15% |
| specs/ | 20% |
| issues/ | 10% |
| Freshness | 10% |

## Execution Flow

### --health
1. Scan all `ideas/*/` directories
2. Check for required files
3. Count specs, issues, research docs
4. Calculate health score per project

### --validate
1. Parse markdown files for links
2. Verify link targets exist
3. Check for required structure
4. Identify orphaned files

### --stale
1. Get file modification dates via git
2. Flag files older than threshold
3. Categorize by severity

### --sync
1. Read current CLAUDE.md
2. Scan all ideas/*/README.md for status
3. Compare and identify differences
4. Propose updates

## When to Use

- Weekly documentation review
- Before presenting ideas
- After adding/removing ideas
- Finding forgotten projects
