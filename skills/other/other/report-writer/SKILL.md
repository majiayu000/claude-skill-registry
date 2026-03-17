---
id: report-writer
title: Report Writer Skill
category: methodology
difficulty: intermediate
triggers:
  - write report
  - generate finding
  - audit report
  - finding template
  - report format
related_skills:
  - severity/SKILL.md
  - methodology/SKILL.md
tags:
  - report
  - writing
  - findings
  - templates
last_updated: 2026-02-26
description: >-
  Generate professional audit reports with structured findings, severity
  classifications, proof-of-concept code, and actionable recommendations.
  Use when writing individual findings, composing full audit reports, or
  formatting results for Code4rena, Sherlock, or client engagements.
---

# Report Writer Skill

Generate professional audit reports with structured findings, severity classifications, proof-of-concept code, and actionable recommendations. Based on industry standards from Trail of Bits, OpenZeppelin, Cyfrin, Spearbit, and Code4rena.

---

## Report Components

| Component | Purpose | Length |
|-----------|---------|--------|
| Executive Summary | Non-technical overview for stakeholders | 1-2 paragraphs |
| Scope | Files/contracts reviewed, commit hash, exclusions | Table |
| Methodology | How the audit was conducted | 1 paragraph |
| Finding Summary | Table of all findings by severity | Table |
| Detailed Findings | Full write-up of each finding | Per finding |
| Centralization Risks | Admin/owner privilege analysis | Section |
| Gas Optimizations | Optional efficiency improvements | List |
| Appendix | Tools used, out-of-scope items | Section |

---

## Severity Classification

Based on the industry-standard Likelihood × Impact matrix:

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Medium | High | Critical |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Info | Low | Medium |

### Likelihood Assessment

| Level | Criteria |
|-------|----------|
| High | Exploitable by anyone, no special conditions, low cost |
| Medium | Requires specific conditions, timing, or moderate skill |
| Low | Requires unlikely conditions, high cost, or privileged access |

### Impact Assessment

| Level | Criteria |
|-------|----------|
| High | Direct loss of funds, protocol takeover, permanent DoS |
| Medium | Conditional fund loss, temporary DoS, incorrect state |
| Low | Inconvenience, minor gas waste, edge case behavior |

---

## Finding ID Convention

| Prefix | Severity | Example |
|--------|----------|----------|
| C | Critical | C-01, C-02 |
| H | High | H-01, H-02 |
| M | Medium | M-01, M-02 |
| L | Low | L-01, L-02 |
| I | Informational | I-01, I-02 |
| G | Gas Optimization | G-01, G-02 |

---

## Writing Quality Standards

### Good Finding Characteristics

1. **Specific title** — Describes the vulnerability, not just the location
   - BAD: "Issue in withdraw function"
   - GOOD: "Missing reentrancy guard in withdraw() allows ETH drain via malicious token callback"

2. **Clear description** — A reader unfamiliar with the code can understand the issue

3. **Precise location** — Contract name, function, line numbers

4. **Demonstrated impact** — Concrete scenario showing what an attacker achieves

5. **Working PoC** — For Critical/High, a test case that proves exploitability

6. **Actionable fix** — Specific code change, not "fix the issue"

---

## Resources
- [Finding Templates](resources/finding-templates.md)
- [Report Template](resources/report-template.md)

## Workflows
- [Report Workflow](workflows/report-workflow.md)
