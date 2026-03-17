---
name: contributor-analyzer
description: >
  Analyzes engineering contributors for annual reviews, progress tracking,
  and production ownership. Reads every commit diff (not sampling), calculates
  accuracy rates, assesses engineering maturity through qualitative judgment,
  and generates promotion-ready performance reviews. Works with any git
  repository using local git for commit analysis and gh CLI for GitHub
  PR/review metadata.
license: MIT
compatibility: "Requires git (local repository access) and gh (GitHub CLI) for full analysis. Optional: jq for JSON parsing, bc for arithmetic."
metadata:
  author: anivar
  version: 1.0.0
  tags:
    - contributor-analysis
    - annual-review
    - code-quality
    - production-ownership
    - promotion
    - engineering-maturity
---

# Contributor Analyzer

Unified skill for engineering contributor analysis. Combines annual review generation, historical progress tracking, production ownership mapping, and qualitative judgment — all driven by reading actual commit diffs.

## Skill Format

Each reference file covers one analysis concern:

- **Quick Reference**: Summary tables and key thresholds
- **Process Steps**: Bash commands and orchestration
- **Templates**: Output formats for reports and profiles
- **Deep Dive**: Full context with examples from real-world 1,091-commit analysis

**Impact ratings**: CRITICAL (blocks accuracy), HIGH (major insight), MEDIUM (enriches analysis)

## When to Apply

Reference these guidelines when:
- Running annual or quarterly performance reviews
- Assessing promotion readiness with evidence
- Tracking contributor progress over time (incremental updates)
- Mapping production code ownership and risk
- Comparing multiple engineers for team decisions
- Identifying single points of failure in codebase ownership

## Priority-Ordered References

| Priority | Reference | Impact | Description |
|----------|-----------|--------|-------------|
| 1 | `agent-context-management.md` | CRITICAL | Batch sizing, file-based output, context budget |
| 2 | `annual-review-process.md` | CRITICAL | 7-phase analysis: identity, metrics, diffs, bugs, quality, report, comparison |
| 3 | `accuracy-analysis.md` | HIGH | Bug introduction detection, accuracy rate calculation, benchmarks |
| 4 | `code-quality-catalog.md` | HIGH | Anti-pattern catalog (9 patterns) and strength catalog (8 patterns) |
| 5 | `qualitative-judgment.md` | HIGH | Engineering wisdom, situational decisions, growth trajectory |
| 6 | `report-templates.md` | HIGH | Report sections, rating scale, promotion framework, comparison format |
| 7 | `production-ownership.md` | MEDIUM | Production branch ownership, domain map, SPOF detection |
| 8 | `historical-progress.md` | MEDIUM | Incremental profiles, plateau detection, period-over-period tracking |

## Quick Reference

### Critical: Context Management

**Before launching ANY analysis, count commits:**
```bash
git log --author="EMAIL" --after="YEAR-01-01" --before="YEAR+1-01-01" --oneline | wc -l
```

**Batch sizing (hard limits from real failures):**

| Commits | Action |
|---------|--------|
| 1-40 | Read in main session |
| 41-70 | Single sub-task, writes findings to file |
| 71-90 | Split into 2 sub-tasks |
| 91+ | WILL FAIL — split into 3+ or monthly sub-tasks |

**Sub-tasks write to files, return 3-line summaries.** Never return raw analysis inline.

### Critical: Annual Review Process

7 phases, sequential:
1. **Identity Discovery** — find all git email variants
2. **Metrics** — commits, PRs, reviews, lines (git + gh CLI)
3. **Read ALL Diffs** — quarterly parallel sub-tasks, file-based output
4. **Bug Introduction** — self-reverts, crash-fixes, same-day fixes, hook bypass
5. **Code Quality** — anti-patterns and strengths from diff reading
6. **Report Generation** — structured markdown with rating + promotion assessment
7. **Comparison** — multi-engineer ranking with evidence

### High: Accuracy Rate

```
Effective Accuracy = 100% - (fix-related commits / total commits)
```

| Rate | Assessment |
|------|-----------|
| >90% | Excellent |
| 85-90% | Good |
| 80-85% | Concerning |
| <80% | Poor — significant rework |

### High: Tool Separation

- **Local `git`**: ALL commit-level analysis (log, show, diff, blame, shortlog)
- **`gh` CLI**: ONLY for PR counts, review counts, user verification
- **Never use `gh` to read diffs** — local git is faster with no rate limits

## References

Full documentation with process steps and templates in `references/`:

### Analysis Process

| File | Impact | Description |
|------|--------|-------------|
| `annual-review-process.md` | CRITICAL | Complete 7-phase review process with bash commands |
| `agent-context-management.md` | CRITICAL | Batch sizing, file-based output, multi-engineer orchestration |
| `accuracy-analysis.md` | HIGH | Bug detection commands, accuracy formula, benchmarks |
| `code-quality-catalog.md` | HIGH | 9 anti-patterns + 8 strengths with severity/significance |

### Judgment & Assessment

| File | Impact | Description |
|------|--------|-------------|
| `qualitative-judgment.md` | HIGH | Engineering wisdom indicators, growth trajectory, promotion signals |
| `report-templates.md` | HIGH | Required report sections, rating scale, comparison format |

### Ownership & Progress

| File | Impact | Description |
|------|--------|-------------|
| `production-ownership.md` | MEDIUM | Production file identification, domain map, SPOF detection |
| `historical-progress.md` | MEDIUM | Incremental profiles, plateau detection, cumulative profiles |

## Searching References

```bash
# Find by keyword
grep -rl "accuracy" references/
grep -rl "promotion" references/
grep -rl "ownership" references/
grep -rl "anti-pattern" references/
```

## Problem to Reference Mapping

| Problem | Start With |
|---------|------------|
| Annual review for 1 engineer | `annual-review-process.md` then `report-templates.md` |
| Comparing 2+ engineers for promotion | `annual-review-process.md` then `qualitative-judgment.md` |
| Engineer has 200+ commits | `agent-context-management.md` (read FIRST) |
| Session keeps running out of context | `agent-context-management.md` |
| Is this engineer ready for promotion? | `qualitative-judgment.md` then `accuracy-analysis.md` |
| Who owns the payment system? | `production-ownership.md` |
| Track progress since last review | `historical-progress.md` |
| Quality assessment from code | `code-quality-catalog.md` then `accuracy-analysis.md` |
| Single points of failure in team | `production-ownership.md` |
| Plateau detection | `historical-progress.md` |

## Full Compiled Document

For the complete guide with all references expanded: `AGENTS.md`

## Usage Examples

```
# Annual review (single engineer)
Analyze @alice for 2025 annual review in repo org/repo.
Git email: alice@company.com. Write to ./alice-2025-review.md

# Multi-engineer comparison with promotion decision
Analyze @alice, @bob, @charlie for 2025 reviews.
I need to decide which 2 get promoted.

# Production ownership mapping
Analyze production code ownership in this repo.

# Incremental progress update
Update @alice's progress profile with latest contributions.

# Critical path risk detection
Find single points of failure in production code ownership.

# Plateau detection
Has @bob plateaued? Check last 3 quarters.
```
