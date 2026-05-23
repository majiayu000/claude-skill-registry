---
name: plan-explore
description: Explore implementation plans, status, and relationships. Provides comprehensive plan ecosystem navigation with filtering, health analysis, and actionable recommendations.
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: design-doc-agent
---

# Plan Exploration

Provides comprehensive exploration and navigation of the plan ecosystem,
enabling agents to understand project status at a glance, discover plans,
identify health issues, and navigate relationships between plans and design docs.

## Overview

The plan-explore skill enables agents to:

1. **Understand project status** - See active, ready, blocked, and completed plans
2. **Discover plans** - Filter by module, status, design doc, or owner
3. **Identify health issues** - Detect stale, orphaned, or blocked plans
4. **Get recommendations** - Receive actionable next steps based on plan state
5. **Navigate relationships** - Explore plan-design doc bidirectional links

**Key Features:**

- Multiple output formats (summary, detailed, timeline, JSON)
- Rich filtering capabilities (module, status, design-doc, owner)
- Health analysis (staleness, orphans, blockers, schedule)
- Smart recommendations for next actions
- Fast metadata caching (5-minute TTL)

## Quick Start

**Show all active plans:**

```bash
/plan-explore --status=in-progress
```

**Show plans for specific module:**

```bash
/plan-explore effect-type-registry
```

**Find orphaned plans:**

```bash
/plan-explore --orphans
```

**Show stale plans:**

```bash
/plan-explore --stale --age-threshold=60
```

**Timeline view:**

```bash
/plan-explore --format=timeline
```

## Parameters

### Filters

- `module`: Filter by module name (e.g., `effect-type-registry`)
- `--status`: Filter by status (ready, in-progress, blocked, completed, abandoned)
  - Supports multiple: `--status=ready,in-progress`
- `--design-doc`: Filter by related design doc path
- `--owner`: Filter by plan owner username

### Display Options

- `--format`: Output format (summary, detailed, timeline, json) [default: summary]
- `--show-phases`: Show phase details [default: false]
- `--show-health`: Show health analysis [default: true]

### Analysis Options

- `--orphans`: Show only orphaned plans (no design docs)
- `--stale`: Show only stale plans
- `--blocked`: Show only blocked plans
- `--age-threshold`: Days since update for staleness [default: 30]

## Output Formats

### Summary Format (Default)

Concise overview with status summary, active plans, health insights, and
next actions. Typically <50 lines for clarity.

```text
Implementation Plans Overview
============================

Status Summary:
  Ready: 3 plans
  In Progress: 5 plans (avg 45% complete)
  Blocked: 2 plans
  Completed: 12 plans

Active Plans (In Progress):
  • Subagent Integration [45%] - 2 weeks old
    Modules: design-doc-system
    Design: architecture-proposal.md

Health Insights:
  ⚠️  2 plans stale (>30 days since update)
  ✅ All blocked plans have clear dependencies

Next Actions:
  1. Update stale plans: performance-tracking-plan.md
  2. Review blocked plans for unblocking
```

### Detailed Format

Shows full plan metadata including phases, dates, blockers, and complete
design doc relationships.

### Timeline Format

Chronological view grouped by date/month with schedule status:

```text
Implementation Timeline
======================

January 2026
------------
✅ Jan 5-10: Cache System v1 (completed)
🚧 Jan 15-25: Subagent Integration (45% - in progress)
⏸️  Jan 20-30: Performance Phase 2 (blocked)

Health:
  2 plans behind schedule
  3 plans on track
```

### JSON Format

Machine-readable output for programmatic processing.

## Health Analysis

The skill performs automatic health analysis:

**Staleness Detection:**

- Plans with `updated` > 30 days ago (configurable)
- Plans in-progress with no updates for 2 weeks
- Plans with target-completion in past

**Orphan Detection:**

- Plans with no design-docs references
- Plans referencing non-existent design docs

**Blocker Analysis:**

- Plans blocked by other blocked plans (cascading blocks)
- Plans blocked by completed plans (stale blockers)

**Schedule Analysis:**

- Plans beyond target-completion date
- Plans with unrealistic progress rates

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Implementation Details

See [instructions.md](instructions.md) for:

- Step-by-step exploration process
- Query algorithm details
- Health analysis implementation
- Caching strategy
- Performance optimization

**Load when:** Implementing the skill or debugging issues

### For Usage Examples

See [examples.md](examples.md) for:

- Common query patterns
- All filter combinations
- Output format examples
- Health analysis scenarios
- Integration with other skills

**Load when:** User needs examples or clarification

## Integration

Works well with:

- `/plan-list` - Quick list of plans (lighter weight)
- `/plan-validate` - Validate plan structure
- `/design-review` - Review design docs with plan context
- `/design-sync` - Sync design docs and check plan progress

## Success Criteria

A successful exploration:

- ✅ Returns relevant plans based on filters
- ✅ Health analysis is accurate and actionable
- ✅ Recommendations are clear and specific
- ✅ Output format is clean and readable
- ✅ Performance is acceptable (<500ms for detailed mode)
- ✅ No false positives in health checks
