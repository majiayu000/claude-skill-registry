---
name: scope-guard
description: |

Triggers: prioritization, anti-overengineering, yagni, scope, guard
  Prevents overengineering through worthiness scoring, opportunity cost comparison,
  and branch threshold monitoring.

  Triggers: scope creep, overengineering, worthiness score, branch size, YAGNI,
  feature evaluation, scope validation, anti-overengineering, opportunity cost

  Use when: evaluating features during brainstorming, planning new functionality,
  branches approach size limits (1000/1500/2000 lines, 15/25/30 commits)

  DO NOT use when: feature is already approved and in progress.
  DO NOT use when: simple bug fixes with clear scope.

  Use this skill BEFORE implementing any new feature. This is NON-NEGOTIABLE
  for scope control.
category: workflow-methodology
tags: [anti-overengineering, scope, YAGNI, prioritization, backlog]
dependencies: []
tools: []
usage_patterns:
  - feature-evaluation
  - scope-validation
  - threshold-monitoring
  - backlog-management
complexity: intermediate
estimated_tokens: 2500
modules:
  - modules/decision-framework.md
  - modules/github-integration.md
  - modules/anti-overengineering.md
  - modules/branch-management.md
  - modules/baseline-scenarios.md
version: 1.3.5
---
## Table of Contents

- [Philosophy](#philosophy)
- [When to Use](#when-to-use)
- [When NOT to Use](#when-not-to-use)
- [Quick Start](#quick-start)
- [1. Score the Feature](#1-score-the-feature)
- [2. Check Against Backlog](#2-check-against-backlog)
- [3. Verify Branch Budget](#3-verify-branch-budget)
- [4. Monitor Thresholds](#4-monitor-thresholds)
- [Core Workflow](#core-workflow)
- [Step 1: Calculate Worthiness (`scope-guard:worthiness-scored`)](#step-1:-calculate-worthiness-(scope-guard:worthiness-scored))
- [Step 2: Compare Against Backlog (`scope-guard:backlog-compared`)](#step-2:-compare-against-backlog-(scope-guard:backlog-compared))
- [Step 3: Check Branch Budget (`scope-guard:budget-checked`)](#step-3:-check-branch-budget-(scope-guard:budget-checked))
- [Step 4: Document Decision (`scope-guard:decision-documented`)](#step-4:-document-decision-(scope-guard:decision-documented))
- [Anti-Overengineering Rules](#anti-overengineering-rules)
- [Backlog Management](#backlog-management)
- [Directory Structure](#directory-structure)
- [Queue Rules](#queue-rules)
- [Adding to Queue](#adding-to-queue)
- [Integration Points](#integration-points)
- [With superpowers:brainstorming](#with-superpowers:brainstorming)
- [With superpowers:writing-plans](#with-superpowers:writing-plans)
- [During superpowers:execute-plan](#during-superpowers:execute-plan)
- [Required TodoWrite Items](#required-todowrite-items)
- [Related Skills](#related-skills)
- [Module Reference](#module-reference)


# Scope Guard

Prevents overengineering by both Claude and human during the brainstorm→plan→execute workflow. Forces explicit evaluation of every proposed feature against business value, opportunity cost, and branch constraints.

## Philosophy

**Core Belief:** Not all features deserve implementation. Most ideas should be deferred to backlog until proven necessary.

**Three Pillars:**
1. **Worthiness Scoring** - Quantify value vs cost before building
2. **Opportunity Cost** - Compare against existing backlog
3. **Branch Discipline** - Respect size thresholds

## When to Use

- During brainstorming sessions before documenting designs
- During planning sessions before finalizing implementation plans
- When evaluating "should we add this?" decisions
- Automatically via hooks when branches approach thresholds
- When proposing new features, abstractions, or patterns

## When NOT to Use

- Bug fixes with clear, bounded scope
- Documentation-only changes
- Trivial single-file edits (< 50 lines)
- Emergency production fixes

## Quick Start

### 1. Score the Feature

Use the Worthiness formula:
```
(Business Value + Time Criticality + Risk Reduction) / (Complexity + Token Cost + Scope Drift)
```
**Verification:** Run the command with `--help` flag to verify availability.

See [decision-framework.md](modules/decision-framework.md) for details.

**Thresholds:**
- **> 2.0** → Implement now
- **1.0 - 2.0** → Discuss first
- **< 1.0** → Defer to backlog

### 2. Check Against Backlog

Compare against `docs/backlog/queue.md`:
- Does it beat top queued items?
- Is there room in branch budget?

### 3. Verify Branch Budget

**Default: 3 major features per branch**

If at capacity, must drop existing feature, split to new branch, or justify override.

### 4. Monitor Thresholds

Watch for Yellow/Red zones:
- **Lines:** 1000/1500/2000
- **Commits:** 15/25/30
- **Days:** 3/7/7+

See [branch-management.md](modules/branch-management.md) for monitoring.

## Core Workflow

### Step 1: Calculate Worthiness (`scope-guard:worthiness-scored`)

Score each factor (1, 2, 3, 5, 8, 13):
- **Value Factors:** Business Value, Time Criticality, Risk Reduction
- **Cost Factors:** Complexity, Token Cost, Scope Drift

Details: [decision-framework.md](modules/decision-framework.md)

### Step 2: Compare Against Backlog (`scope-guard:backlog-compared`)

1. Check `docs/backlog/queue.md` for existing items
2. Compare Worthiness Scores
3. New item must beat top queued item OR fit within branch budget

### Step 3: Check Branch Budget (`scope-guard:budget-checked`)

Count current features in branch. If at budget (default: 3), new feature requires:
- Dropping an existing feature, OR
- Splitting to new branch, OR
- Explicit override with justification

### Step 4: Document Decision (`scope-guard:decision-documented`)

Record outcome:
- **Implementing:** Note Worthiness Score and budget slot
- **Deferring (MANDATORY STEPS):**
  1. **Create GitHub issue immediately** - See [github-integration.md](modules/github-integration.md)
  2. Mark `scope-guard:github-issue-created` complete
  3. Optionally add to `docs/backlog/queue.md` with issue link
- **Rejecting:** Document why (low value, out of scope)

**IMPORTANT:** Deferral is NOT complete until a GitHub issue exists. This prevents context loss when branches are merged or abandoned.

## Anti-Overengineering Rules

**Key Principles:**
- Ask clarifying questions BEFORE proposing solutions
- No abstraction until 3rd use case
- Defer "nice to have" features
- Stay within branch budget

See [anti-overengineering.md](modules/anti-overengineering.md) for full rules and red flags.

## Backlog Management

### Directory Structure

```
**Verification:** Run the command with `--help` flag to verify availability.
docs/backlog/
├── queue.md              # Active ranked queue
└── archive/
    ├── ideas.md          # Deferred feature ideas
    ├── optimizations.md  # Deferred performance work
    ├── refactors.md      # Deferred cleanup
    └── abstractions.md   # Deferred patterns
```
**Verification:** Run the command with `--help` flag to verify availability.

### Queue Rules

- Max 10 items in active queue
- Items older than 30 days without pickup → move to archive
- Re-score monthly or when project context changes

### Adding to Queue

When deferring, add to `docs/backlog/queue.md`:

```markdown
| Rank | Item | Worthiness | Added | Branch/Epic | Category |
|------|------|------------|-------|-------------|----------|
| 1 | [New item description] | 1.8 | 2025-12-08 | current-branch | idea |
```
**Verification:** Run the command with `--help` flag to verify availability.

Re-rank by Worthiness Score after adding.

## Integration Points

### With superpowers:brainstorming

At end of brainstorming, before documenting design:
1. List all proposed features/components
2. Score each with Worthiness formula
3. Defer items scoring < 1.0 to backlog
4. Check branch budget for remaining items

**Self-invoke prompt:** "Before documenting this design, let me evaluate the proposed features with scope-guard."

### With superpowers:writing-plans

Before finalizing implementation plan:
1. Verify all planned items have Worthiness > 1.0
2. Compare against backlog queue
3. Confirm within branch budget
4. Document any deferrals

**Self-invoke prompt:** "Before finalizing this plan, let me verify scope with scope-guard."

### During superpowers:execute-plan

Periodically during execution:
1. Run threshold check: lines, files, commits, days
2. Warn if Yellow zone reached
3. Require justification if Red zone reached

**Self-invoke prompt:** "This branch has grown significantly. Let me check scope-guard thresholds."

## Required TodoWrite Items

When evaluating a feature, create these todos:

1. `scope-guard:worthiness-scored`
2. `scope-guard:backlog-compared`
3. `scope-guard:budget-checked`
4. `scope-guard:github-issue-created` (MANDATORY if deferring - blocks step 5)
5. `scope-guard:decision-documented`

**Note:** Step 4 (`github-issue-created`) is REQUIRED when deferring items. You cannot mark `decision-documented` complete without first completing `github-issue-created` for deferrals.

## Related Skills

- `superpowers:brainstorming` - Ideation workflow this guards
- `superpowers:writing-plans` - Planning workflow this validates
- `imbue:review-core` - Review methodology pattern

## Module Reference

- **[decision-framework.md](modules/decision-framework.md)** - Worthiness formula, scoring, thresholds
- **[github-integration.md](modules/github-integration.md)** - MANDATORY issue creation for deferrals
- **[anti-overengineering.md](modules/anti-overengineering.md)** - Rules, patterns, red flags
- **[branch-management.md](modules/branch-management.md)** - Thresholds, monitoring, zones
- **[baseline-scenarios.md](modules/baseline-scenarios.md)** - Testing scenarios and validation
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
