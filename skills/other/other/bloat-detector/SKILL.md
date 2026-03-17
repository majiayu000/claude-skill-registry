---
name: bloat-detector
description: 'Detect codebase bloat through progressive analysis: dead code, duplication,
  complexity, documentation bloat. Use when context usage high, quarterly maintenance,
  pre-release cleanup, before refactoring. Do not use when active feature development,
  time-sensitive bugs, codebase < 1000 lines.'
category: conservation
tags:
- bloat
- cleanup
- static-analysis
- technical-debt
- optimization
tools:
- Bash
- Grep
- Glob
- Read
modules:
- quick-scan
- git-history-analysis
- code-bloat-patterns
- ai-generated-bloat
- documentation-bloat
- static-analysis-integration
- remediation-types
progressive_loading: true
estimated_tokens: 400
---
## Table of Contents

- [Bloat Categories](#bloat-categories)
- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [Confidence Levels](#confidence-levels)
- [Prioritization](#prioritization)
- [Module Architecture](#module-architecture)
- [Safety](#safety)

# Bloat Detector

Systematically detect and eliminate codebase bloat through progressive analysis tiers.

## Bloat Categories

| Category | Examples |
|----------|----------|
| **Code** | Dead code, God classes, Lava flow, duplication |
| **AI-Generated** | Tab-completion bloat, vibe coding, hallucinated deps |
| **Documentation** | Redundancy, verbosity, stale content, slop |
| **Dependencies** | Unused imports, dependency bloat, phantom packages |
| **Git History** | Stale files, low-churn code, massive single commits |

## Quick Start

### Tier 1: Quick Scan (2-5 min, no tools)
```bash
/bloat-scan
```
Detects: Large files, stale code, old TODOs, commented blocks, basic duplication

### Tier 2: Targeted Analysis (10-20 min, optional tools)
```bash
/bloat-scan --level 2 --focus code   # or docs, deps
```
Adds: Static analysis (Vulture/Knip), git churn hotspots, doc similarity

### Tier 3: Deep Audit (30-60 min, full tooling)
```bash
/bloat-scan --level 3 --report audit.md
```
Adds: Cross-file redundancy, dependency graphs, readability metrics

## When To Use

| Do | Don't |
|----|-------|
| Context usage > 30% | Active feature development |
| Quarterly maintenance | Time-sensitive bugs |
| Pre-release cleanup | Codebase < 1000 lines |
| Before major refactoring | Tools unavailable (Tier 2/3) |

## When NOT To Use

- Active feature development
- Time-sensitive bugs
- Codebase < 1000 lines

## Confidence Levels

| Level | Confidence | Action |
|-------|------------|--------|
| HIGH | 90-100% | Safe to remove |
| MEDIUM | 70-89% | Review first |
| LOW | 50-69% | Investigate |

## Prioritization

```
Priority = (Token_Savings × 0.4) + (Maintenance × 0.3) + (Confidence × 0.2) + (Ease × 0.1)
```

## Module Architecture

**Tier 1** (always available):
- See `modules/quick-scan.md` - Heuristics, no tools
- See `modules/git-history-analysis.md` - Staleness, churn, vibe coding signatures

**Tier 2** (optional tools):
- See `modules/code-bloat-patterns.md` - Anti-patterns (God class, Lava flow)
- See `modules/ai-generated-bloat.md` - AI-specific patterns (Tab bloat, hallucinations)
- See `modules/documentation-bloat.md` - Redundancy, readability, slop detection
- See `modules/static-analysis-integration.md` - Vulture, Knip

**Shared**:
- See `modules/remediation-types.md` - DELETE, REFACTOR, CONSOLIDATE, ARCHIVE

## Auto-Exclusions

Always excludes: `.venv`, `__pycache__`, `.git`, `node_modules`, `dist`, `build`, `vendor`

Also respects: `.gitignore`, `.bloat-ignore`

## Safety

- **Never auto-delete** - all changes require approval
- **Dry-run support** - `--dry-run` for previews
- **Backup branches** - created before bulk changes

## Related

- `bloat-auditor` agent - Executes scans
- `unbloat-remediator` agent - Safe remediation
- `context-optimization` skill - MECW principles
