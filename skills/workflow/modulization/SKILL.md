---
name: modulization
description: >
  Cadence-driven work moderation and recomposition system that discovers unfinished,
  fragmented, and drifting work across the codebase and collaboration surfaces, then
  recomposes it into coherent, schedulable units of work aligned with the roadmap and
  spec-driven development.
version: 1.0.0
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
  - Task
  - TodoWrite
license: MIT
---

# Modulization Skill

**Cadence-Driven Work Moderation & Recomposition**

> *Treat unfinished work as structured information, not noise to be ignored.*

Modulization is a sophisticated agent that runs on a regular cadence (daily, weekly, or per-release) to discover scattered, incomplete, and drifting work across your project, then recomposes it into coherent **modules** — units of work that can be scheduled, spec'd, and delivered together.

---

## When to Use This Skill

Invoke `modulization` when you need to:

- **Audit project health** — Understand the true state of unfinished work
- **Prepare for a milestone** — Identify what needs attention before release
- **Triage accumulated debt** — TODOs, stale PRs, forgotten issues
- **Align work to roadmap** — Ensure unfinished work has a home
- **Run periodic maintenance** — Weekly/biweekly cleanup cadence
- **Onboard to a project** — Understand what's been left behind
- **Close out a development phase** — Ensure nothing falls through cracks

**Trigger phrases:**
- "Run modulization"
- "Audit unfinished work"
- "What work is floating?"
- "Prepare for milestone X"
- "Run weekly work moderation"
- "Discover stale work"
- "Recompose backlog"

---

## Core Concepts

### What is a Module?

A **Module** is a coherent, self-contained unit of unfinished or future work that:

- **Shares intent** — All items address the same goal or problem
- **Shares technical surface area** — Affects the same files, systems, or domains
- **Can be reasoned about together** — Schedulable as a single work package

Unlike flat task lists, modules group related breadcrumbs into actionable units.

### What is "Squeeze-In"?

Squeeze-in is **intentional insertion** of modular work into existing delivery arcs:

- Identify natural seams between milestones
- Propose intermediate versions (v1.1.1-alpha, internal milestones)
- Attach modules to hard dependencies or opportunistic alignments
- Explicitly defer work that would fragment focus

This avoids surprise scope creep while ensuring nothing is forgotten.

### Work Classification

Every discovered module is classified into one of four paths:

| Classification | Meaning | Action |
|---------------|---------|--------|
| **Integrate Now** | Aligned with active milestone, low cost, high leverage | Add to current work |
| **Schedule Explicitly** | Important but disruptive | Assign to future milestone |
| **Ice (Intentional Pause)** | Valid idea, wrong time | Document and defer |
| **Archive/Close** | Obsolete or superseded | Close with context preserved |

**Nothing remains floating.**

---

## Core Workflow

### Phase 1: Signal Collection

Modulization gathers signals from multiple sources:

#### Codebase Signals
```
Scan for:
- TODO / FIXME / NOTE / HACK / XXX comments
- Dead or partially used code paths
- Experimental flags or feature toggles
- Unreferenced modules or tests
- Inline comments that no longer match reality
- Incomplete implementations (stub functions, panic!("not implemented"))
```

#### GitHub/VCS Signals
```
Collect from:
- Stale PRs (open > 14 days, draft, closed without merge)
- Issues without recent activity (> 30 days)
- Linked but unresolved conversations
- PR review comments requesting follow-up work
- Abandoned branches (no commits > 30 days)
- Draft issues in projects
```

#### Process Signals
```
Reference:
- ROADMAP.md milestones and due dates
- Spec-kitty worktrees (.worktrees/)
- Spec-driven artifacts (spec.md, plan.md, tasks.md)
- CODEOWNERS and area ownership
- Constitution principles
```

#### Historical Context
```
Trace:
- Origin of work (issue → PR → discussion → commit)
- Why it stalled (dependency, scope creep, priority shift)
- Similar work elsewhere in the project
- Previous decisions and discussions
```

### Phase 2: Signal Analysis

For each discovered signal:

1. **Extract intent** — What was the original goal?
2. **Assess currency** — Is this still relevant?
3. **Trace lineage** — Where did this originate?
4. **Measure scope** — How big is this work?
5. **Identify dependencies** — What does this block/depend on?
6. **Evaluate risk** — What happens if ignored?

### Phase 3: Module Composition

Group related signals into modules:

1. **Cluster by intent** — Group items addressing same goal
2. **Cluster by surface area** — Group items touching same files/systems
3. **Identify natural boundaries** — Find clean seams between modules
4. **Validate coherence** — Ensure each module makes sense as a unit
5. **Name the module** — Give it a clear, descriptive identifier

### Phase 4: Classification & Scheduling

For each module, apply decision heuristics:

```
IF aligned_with_active_milestone AND low_marginal_cost THEN
  → Integrate Now

IF important AND disruptive THEN
  → Schedule Explicitly (assign milestone)

IF valid_but_wrong_time OR blocked_by_external THEN
  → Ice (document rationale)

IF obsolete OR superseded THEN
  → Archive (preserve context)
```

### Phase 5: Output Generation

Produce actionable outputs:

1. **Module Report** — Markdown summary of all discovered modules
2. **Roadmap Updates** — Suggested milestone adjustments
3. **Spec Seeds** — Inputs for spec-driven development
4. **GitHub Updates** — Comments on stale PRs/issues
5. **Cleanup Actions** — Safe deletions and archival suggestions

---

## Integration with Spec-Driven Development

Modulization does not write final specs — it prepares **spec-ready inputs**.

For each module, it can emit:

### Spec Seed
```yaml
module_id: MOD-2024-001
title: "Complete i18n infrastructure"
problem: |
  Internationalization work was started but left incomplete.
  Multiple TODOs and a draft PR exist.
context: |
  - PR #147 (draft): Basic locale detection
  - 12 TODOs in src/i18n/
  - Issue #89: RTL support request
constraints:
  - Must maintain backwards compatibility
  - Performance budget: <10ms overhead
suggested_artifacts:
  - PRD: User-facing i18n capabilities
  - ADR: Locale detection strategy
  - Design: Translation file format
```

This feeds directly into `/spec-kitty.specify` for full spec generation.

---

## Output Format

### Module Report Structure

```markdown
# Modulization Report
Generated: 2026-01-08
Cadence: Weekly
Scope: Full repository

## Summary
- Signals Collected: 47
- Modules Formed: 8
- Integrate Now: 2
- Schedule Explicitly: 4
- Ice: 1
- Archive: 1

## Modules

### MOD-001: Incomplete Safety Validation Patterns
**Classification:** Integrate Now
**Milestone:** v1.1.0-beta
**Confidence:** 0.87

**Description:**
Safety validation patterns have TODOs for edge cases and a stale PR
with additional patterns that was never merged.

**Signals:**
- [TODO] src/safety/patterns.rs:142 - Handle nested quotes
- [TODO] src/safety/validator.rs:89 - Add timeout patterns
- [PR #156] Draft: Additional safety patterns (stale 23 days)
- [Issue #134] Safety bypass with unicode (open)

**Scope:**
- Files: 4
- Lines: ~200
- Complexity: Medium
- Risk if ignored: High (security)

**Recommendation:**
Integrate into current sprint. Aligns with v1.1.0-beta safety focus.
Create spec seed for structured implementation.

**Spec Seed:** [Link to generated seed]

---
```

---

## GitHub Action Integration

Modulization is designed to run as a scheduled GitHub Action:

```yaml
# .github/workflows/modulization.yml
name: Modulization Cadence

on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday 9 AM UTC
  workflow_dispatch:      # Manual trigger
    inputs:
      scope:
        description: 'Scan scope'
        type: choice
        options:
          - full
          - codebase-only
          - github-only
        default: full

jobs:
  modulization:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Modulization
        uses: anthropic/claude-code-action@v1
        with:
          skill: modulization
          scope: ${{ inputs.scope || 'full' }}
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: modulization-report
          path: .modulization/reports/
```

---

## Configuration

Modulization behavior can be configured via `.modulization/config.yaml`:

```yaml
# .modulization/config.yaml
version: 1

cadence:
  schedule: weekly          # daily, weekly, biweekly, monthly
  day: monday
  timezone: UTC

signals:
  codebase:
    enabled: true
    patterns:
      - "TODO"
      - "FIXME"
      - "HACK"
      - "XXX"
      - "NOTE"
    exclude_paths:
      - "vendor/"
      - "node_modules/"
      - ".git/"

  github:
    enabled: true
    stale_pr_days: 14
    stale_issue_days: 30
    include_draft_prs: true
    include_closed_unmerged: true

  process:
    enabled: true
    roadmap_path: "ROADMAP.md"
    worktrees_path: ".worktrees/"

classification:
  # Custom rules for classification
  auto_integrate:
    - label: "good first issue"
      max_scope: small
    - label: "quick-fix"

  auto_ice:
    - label: "wontfix"
    - label: "deferred"

  auto_archive:
    - label: "duplicate"
    - label: "invalid"

output:
  report_path: ".modulization/reports/"
  spec_seeds_path: ".modulization/spec-seeds/"
  create_github_issues: false  # Auto-create issues for modules
  comment_on_stale: true       # Add comments explaining classification

integration:
  spec_kitty: true             # Generate spec-kitty compatible seeds
  roadmap_sync: true           # Suggest ROADMAP.md updates
```

---

## Best Practices

### DO:
- Run modulization before major milestones
- Review the module report with stakeholders
- Use classification to drive sprint planning
- Let spec-seeds inform architectural discussions
- Close/archive with context preserved
- Document why something was iced

### DON'T:
- Auto-merge modules without review
- Ignore high-risk flagged items
- Create busywork from minor TODOs
- Lose historical context when archiving
- Skip the classification step
- Run too frequently (noise > signal)

---

## Integration Points

### With Roadmap
- Reads ROADMAP.md for milestone context
- Suggests milestone assignments for modules
- Identifies work that fits natural seams

### With Spec-Kitty
- Produces spec-seeds compatible with `/spec-kitty.specify`
- Groups work into spec-able units
- Provides context for clarification questions

### With Beta Testing
- Identifies stale test cases
- Flags incomplete test coverage TODOs
- Groups testing debt into modules

### With Continuity System
- Preserves context across sessions
- Links to handoff documents
- Maintains module history

---

## Example Session

```
User: Run weekly modulization

Agent: Starting modulization scan...

📊 Collecting Signals
├── Codebase: 23 TODOs, 4 FIXMEs, 2 incomplete implementations
├── GitHub: 5 stale PRs, 8 dormant issues, 2 draft PRs
├── Process: 4 worktrees with pending work
└── Historical: Traced 15 items to original discussions

🧩 Composing Modules
├── MOD-001: Safety validation gaps (7 signals)
├── MOD-002: i18n infrastructure (5 signals)
├── MOD-003: CLI help improvements (4 signals)
├── MOD-004: Backend retry logic (3 signals)
├── MOD-005: Documentation sync (6 signals)
└── MOD-006: Deprecated API cleanup (4 signals)

📋 Classification
├── Integrate Now: MOD-001 (aligns with v1.1.0-beta security focus)
├── Schedule: MOD-002 → v1.2.0, MOD-003 → v1.1.0, MOD-004 → v1.1.0
├── Ice: MOD-006 (breaking change, defer to v2.0.0)
└── Archive: None this cycle

📝 Outputs Generated
├── Report: .modulization/reports/2026-01-08-weekly.md
├── Spec Seeds: 4 seeds for scheduled modules
├── GitHub: Comments added to 5 stale PRs
└── Roadmap: 2 suggested milestone additions

Would you like me to:
1. Review any specific module in detail?
2. Generate full specs for scheduled modules?
3. Create GitHub issues for tracking?
```

---

## References

- [Module Schema](./references/module-schema.md) — JSON schema for modules
- [Decision Heuristics](./references/decision-heuristics.md) — Classification logic
- [Signal Collectors](./references/signal-collectors.md) — Collection strategies
- [Integration Guide](./references/spec-kitty-integration.md) — Spec-kitty workflow

---

## Related Skills

- `continuity_ledger` — State preservation across sessions
- `create_handoff` — Work transfer documentation
- `quality-engineer-manager` — Release validation orchestration
- `beta-test-cycles` — Systematic testing improvement

---

## Changelog

### v1.0.0 (2026-01-08)
- Initial release
- Core signal collection from codebase, GitHub, process
- Module composition and classification
- Spec-kitty integration
- GitHub Action cadence support
