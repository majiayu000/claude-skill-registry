---
id: audit-context-building
title: Audit Context Building Skill
category: methodology
difficulty: beginner
triggers:
  - audit context
  - protocol overview
  - architecture mapping
  - pre-audit
  - start audit
  - understand protocol
related_skills:
  - methodology/SKILL.md
  - solidity-scanner/SKILL.md
tags:
  - context
  - architecture
  - pre-audit
  - methodology
last_updated: 2026-02-26
description: >-
  Systematically build comprehensive understanding of a protocol before
  code-level analysis. Use when starting a new audit engagement, mapping
  trust boundaries and external dependencies, or when needing to identify
  all privileged roles and protocol invariants before manual review.
---

# Audit Context Building Skill

Systematically build comprehensive understanding of a protocol before diving into code-level analysis. Rushing into code without context leads to missed vulnerabilities, wasted time, and incomplete coverage.

---

## Why Context Building Matters

| Without Context | With Context |
|-----------------|-------------|
| Miss cross-contract interactions | Map all trust boundaries before reading code |
| Spend time on low-risk functions | Prioritize functions handling value |
| Overlook admin-only backdoors | Know every privileged role and its power |
| Miss assumptions about external protocols | Document all external dependencies upfront |
| Can't identify broken invariants | Invariants identified before code review |

### Time Allocation

For a typical DeFi protocol audit:

| Phase | Time % | Activity |
|-------|--------|----------|
| Context building | 15-20% | Architecture mapping, docs review, invariants |
| Function-level analysis | 40-50% | Line-by-line code review with context |
| Cross-cutting concerns | 20-25% | Reentrancy, access control, value flows |
| Reporting | 10-15% | Writing findings, severity classification |

---

## Capabilities

### Architecture Mapping
- Contract inventory with purpose and SLOC
- Inheritance hierarchy (is-a relationships)
- Contract interaction graph (calls-to relationships)
- Proxy/upgrade pattern identification
- Library usage and dependency versions

### Function-Level Analysis
- Access control classification (unrestricted / role-gated / owner-only)
- State change documentation (reads vs writes)
- External call mapping (call targets, data flow, return handling)
- CEI pattern compliance per function
- Edge case identification

### Protocol Understanding
- Protocol invariant identification and documentation
- Trust boundary mapping (what trusts what)
- Token and value flow tracing
- Fee mechanism analysis
- Integration point documentation

### Risk Surface Identification
- Centralization risk assessment (admin power)
- Oracle dependency risk
- External protocol dependency risk
- Upgrade mechanism risk
- Economic design risk areas

---

## When to Use

| Trigger | Action |
|---------|--------|
| Starting a new audit | Full pre-audit context workflow |
| Reviewing unfamiliar protocol type | Architecture analysis first |
| Auditing upgradeable contracts | Storage layout + proxy analysis |
| Multi-contract system | Contract interaction mapping |
| Post-deployment review | Focus on live state + deployed config |

---

## Workflows
- [Pre-Audit Context](workflows/pre-audit-context.md) — Complete before code review
- [Architecture Analysis](workflows/architecture-analysis.md) — Contract relationships and structure
- [Deep Code Review](workflows/deep-code-review.md) — Function-by-function analysis

## Resources
- [Completeness Checklist](resources/completeness-checklist.md) — Ensure nothing is missed
- [Function Analysis Example](resources/function-analysis-example.md) — Template with real example
- [Output Template](resources/output-template.md) — Standardized context report format
