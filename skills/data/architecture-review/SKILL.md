---
name: architecture-review
description: |

Triggers: adr, architecture, patterns, design, review
  Evaluate codebase architecture against ADRs, coupling rules, and team guardrails.

  Triggers: architecture review, ADR audit, coupling analysis, design review,
  principle checks, Law of Demeter, architecture assessment

  Use when: reviewing architecture decisions, auditing ADR compliance, analyzing
  coupling, validating design principles

  DO NOT use when: selecting architecture paradigms - use archetypes skills.
  DO NOT use when: API surface review - use api-review.

  Use this skill for architecture assessment and compliance.
category: architecture
tags: [architecture, design, adr, coupling, patterns, principles]
tools: [adr-auditor, coupling-analyzer, principle-checker]
usage_patterns:
  - architecture-assessment
  - adr-audit
  - refactor-review
  - design-validation
complexity: advanced
estimated_tokens: 300
progressive_loading: true
dependencies:
  - pensive:shared
  - imbue:evidence-logging
  - imbue:diff-analysis/modules/risk-assessment-framework
modules:
  - modules/adr-audit.md
  - modules/coupling-analysis.md
  - modules/principle-checks.md
version: 1.3.7
---
## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [Progressive Loading](#progressive-loading)
- [Required TodoWrite Items](#required-todowrite-items)
- [Workflow](#workflow)
- [Step 1: Establish Context (`arch-review:context-established`)](#step-1:-establish-context-(arch-review:context-established))
- [Step 2: ADR Audit (`arch-review:adr-audit`)](#step-2:-adr-audit-(arch-review:adr-audit))
- [Step 3: Interaction Mapping (`arch-review:interaction-mapping`)](#step-3:-interaction-mapping-(arch-review:interaction-mapping))
- [Step 4: Principle Checks (`arch-review:principle-checks`)](#step-4:-principle-checks-(arch-review:principle-checks))
- [Step 5: Risks and Actions (`arch-review:risks-actions`)](#step-5:-risks-and-actions-(arch-review:risks-actions))
- [Architecture Principles Checklist](#architecture-principles-checklist)
- [Coupling](#coupling)
- [Cohesion](#cohesion)
- [Layering](#layering)
- [Evolution](#evolution)


# Architecture Review Workflow

Architecture assessment against ADRs and design principles.

## Quick Start

```bash
/architecture-review
```

## When to Use

- Approving reimplementations.
- Large-scale refactoring reviews.
- System design changes.
- New module/service introduction.
- Dependency restructuring.

## Progressive Loading

Load modules based on review scope:

- **`modules/adr-audit.md`** (~400 tokens): ADR verification and documentation.
- **`modules/coupling-analysis.md`** (~450 tokens): Dependency analysis and boundary violations.
- **`modules/principle-checks.md`** (~500 tokens): Code quality, security, and performance.

Load all modules for full reviews. For focused reviews, load only relevant modules.

## Required TodoWrite Items

1. `arch-review:context-established`: Repository, branch, motivation.
2. `arch-review:adr-audit`: ADR verification and new ADR needs.
3. `arch-review:interaction-mapping`: Module coupling analysis.
4. `arch-review:principle-checks`: LoD, security, performance.
5. `arch-review:risks-actions`: Recommendation and follow-ups.

## Workflow

### Step 1: Establish Context (`arch-review:context-established`)

Confirm repository and branch:
```bash
pwd
git status -sb
```

Document:
- Feature/bug/epic motivating review.
- Affected subsystems.
- Architectural intent from README/docs.
- Design trade-off assumptions.

### Step 2: ADR Audit (`arch-review:adr-audit`)

**Load: `modules/adr-audit.md`**

- Locate ADRs in project.
- Verify required sections.
- Check status flow.
- Confirm immutability compliance.
- Flag need for new ADRs.

### Step 3: Interaction Mapping (`arch-review:interaction-mapping`)

**Load: `modules/coupling-analysis.md`**

- Diagram before/after module interactions.
- Verify composition boundaries.
- Check data ownership clarity.
- Validate dependency flow direction.
- Identify coupling violations.

### Step 4: Principle Checks (`arch-review:principle-checks`)

**Load: `modules/principle-checks.md`**

- Law of Demeter.
- Anti-slop patterns.
- Security (input validation, least privilege).
- Performance (N+1 queries, caching).

### Step 5: Risks and Actions (`arch-review:risks-actions`)

Summarize using `imbue:diff-analysis/modules/risk-assessment-framework`:
- Current vs proposed architecture.
- Business impact.
- Technical debt implications.

List follow-ups with owners and dates.

Provide recommendation:
- **Approve**: Architecture sound.
- **Approve with actions**: Minor issues to address.
- **Block**: Fundamental problems requiring redesign.

## Architecture Principles Checklist

### Coupling
- [ ] Dependencies follow defined boundaries.
- [ ] No circular dependencies.
- [ ] Extension points used properly.
- [ ] Abstractions don't leak.

### Cohesion
- [ ] Related functionality grouped.
- [ ] Single responsibility per module.
- [ ] Clear module purposes.

### Layering
- [ ] Layers have clear responsibilities.
- [ ] Dependencies flow downward.
- [ ] No layer bypassing.

### Evolution
- [ ] Changes are reversible.
- [ ] Migration paths are clear.
- [ ] ADRs document decisions.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
