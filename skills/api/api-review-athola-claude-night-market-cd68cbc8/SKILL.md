---
name: api-review
description: |

Triggers: consistency, versioning, design, review, documentation
  Evaluate public API surfaces against internal guidelines and external exemplars.

  Triggers: API review, API design, consistency audit, API documentation,
  versioning, surface inventory, exemplar research

  Use when: reviewing API design, auditing consistency, governing documentation,
  researching API exemplars

  DO NOT use when: architecture review - use architecture-review.
  DO NOT use when: implementation bugs - use bug-review.

  Use this skill for API surface evaluation and design review.
category: code-review
tags: [api, design, consistency, documentation, versioning]
tools: [surface-analyzer, exemplar-finder, consistency-checker]
usage_patterns:
  - api-design-review
  - consistency-audit
  - documentation-governance
complexity: intermediate
estimated_tokens: 400
progressive_loading: true
dependencies: [pensive:shared, imbue:evidence-logging]
---
## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [Required TodoWrite Items](#required-todowrite-items)
- [Workflow](#workflow)
- [Step 1: Surface Inventory](#step-1:-surface-inventory)
- [Step 2: Exemplar Research](#step-2:-exemplar-research)
- [Step 3: Consistency Audit](#step-3:-consistency-audit)
- [Step 4: Documentation Governance](#step-4:-documentation-governance)
- [Step 5: Evidence Log](#step-5:-evidence-log)
- [Progressive Loading](#progressive-loading)
- [API Quality Checklist](#api-quality-checklist)
- [Naming](#naming)
- [Parameters](#parameters)
- [Return Values](#return-values)
- [Documentation](#documentation)
- [Output Format](#output-format)
- [API Review Report](#api-review-report)
- [Summary](#summary)
- [Surface Inventory](#surface-inventory)
- [Exemplar Comparison](#exemplar-comparison)
- [Consistency Issues](#consistency-issues)
- [Documentation Gaps](#documentation-gaps)
- [Recommendations](#recommendations)
- [Integration Notes](#integration-notes)
- [Exit Criteria](#exit-criteria)


# API Review Workflow

Evaluate API surfaces against guidelines and high-quality exemplars.

## Quick Start

```bash
/api-review
```
**Verification:** Run the command with `--help` flag to verify availability.

## When to Use

- Reviewing public API changes
- Designing new API surfaces
- Auditing API consistency
- Validating documentation completeness
- Before API releases

## Required TodoWrite Items

1. `api-review:surface-inventory`
2. `api-review:exemplar-research`
3. `api-review:consistency-audit`
4. `api-review:docs-governance`
5. `api-review:evidence-log`

## Workflow

### Step 1: Surface Inventory

**Module**: `@modules/surface-inventory.md`

Detect and catalog all public APIs by language. Record stability levels, feature flags, and versioning metadata.

Quick commands:
```bash
pwd && git status -sb
rg -n "^pub" src  # Rust
rg -n "^def [^_]" package  # Python
```
**Verification:** Run `git status` to confirm working tree state.

### Step 2: Exemplar Research

**Module**: `@modules/exemplar-research.md`

Find 2+ high-quality API references per language. Document patterns for namespacing, pagination, error handling, and documentation structure.

Common exemplars: pandas, requests, tokio, net/http, Stripe API

### Step 3: Consistency Audit

**Module**: `@modules/consistency-audit.md`

Compare project API against exemplar patterns. Check naming, parameters, return types, error semantics, and deprecation handling.

Identify duplication, leaky abstractions, missing feature gates, and documentation gaps.

### Step 4: Documentation Governance

validate documentation includes:
- Entry points and quickstarts
- Complete API reference
- Changelogs and migration notes
- Automated generation (rustdoc, Sphinx, typedoc, OpenAPI)

Verify versioning:
- SemVer compliance
- Stability promises
- Deprecation timelines

### Step 5: Evidence Log

**Dependency**: `imbue:evidence-logging`

Record all executed commands and findings. Summarize recommendation (Approve / Approve with actions / Block) with action items, owners, and dates.

## Progressive Loading

Load modules as needed:
- **Always load**: surface-inventory, consistency-audit
- **Load for new designs**: exemplar-research
- **Load for documentation audits**: Include docs-governance checklist

## API Quality Checklist

### Naming
- [ ] Consistent convention, clear descriptive names, follows language idioms

### Parameters
- [ ] Consistent ordering, optional parameters have defaults, complete type annotations

### Return Values
- [ ] Consistent patterns, error cases documented, pagination consistent

### Documentation
- [ ] All public APIs documented with examples, changelog maintained

## Output Format

```markdown
## API Review Report

### Summary
[Assessment of API surface]

### Surface Inventory
- Endpoints/Functions: N
- Public types: N
- Stability: [stable/beta/experimental counts]

### Exemplar Comparison
[Key patterns from exemplars and alignment analysis]

### Consistency Issues
[I1] [Issue title]
- Location: file:line
- Recommendation: [fix]

### Documentation Gaps
[Identified gaps and required additions]

### Recommendations
- Decision: Approve / Approve with actions / Block
- Action items with owners and dates
```
**Verification:** Run the command with `--help` flag to verify availability.

## Integration Notes

- Use `imbue:evidence-logging` for reproducible command capture
- Reference `imbue:diff-analysis/modules/risk-assessment-framework` for breaking change assessment
- Format output using `imbue:structured-output` for consistent findings

## Exit Criteria

- Surface inventory complete with stability metadata
- Exemplars researched with pattern citations
- Consistency issues documented with locations
- Documentation gaps identified
- Action plan with ownership and timeline
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
