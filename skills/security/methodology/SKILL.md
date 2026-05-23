---
id: methodology
title: Methodology Skill
category: methodology
difficulty: beginner
triggers:
  - audit methodology
  - workflow guide
  - how to audit
  - formal verification
  - invariant testing
  - prompt engineering
  - quality scoring
related_skills:
  - report-writer/SKILL.md
  - scoring/SKILL.md
  - severity/SKILL.md
tags:
  - methodology
  - workflow
  - testing
  - verification
  - quality
last_updated: 2026-02-26
description: >-
  Comprehensive audit methodology guides covering the full security auditor
  workflow -- from preparation and AI-assisted analysis through formal
  verification, economic modeling, report writing, and skill quality scoring.
  Use when learning audit workflows, selecting testing strategies, or
  authoring new skills with TDD methodology.
---

# Methodology Skill

## Purpose
Comprehensive audit methodology guides covering the full security auditor workflow — from preparation and AI-assisted analysis through formal verification, economic modeling, and report writing.

## Core Methodologies

### Audit Workflow
- [LLM Audit Workflow](llm-audit-workflow.md) - Structured AI playbook with phases, modes, and context transfer
- [AI-Assisted Auditing](ai-assisted-auditing.md) - Prompt engineering, automation scripts, and tool comparison
- [Prompt Evolution](prompt-evolution.md) - Beam search optimization system for audit prompts

### Testing & Verification
- [Invariant Testing](invariant-testing.md) - Foundry stateful fuzzing with handler patterns and ghost variables
- [Symbolic Execution](symbolic-execution.md) - Halmos, HEVM, and Certora formal verification
- [PoC Writing Guide](poc-writing-guide.md) - Proof of concept templates for all major vulnerability types

### Attack Analysis
- [Economic Attack Modeling](economic-attack-modeling.md) - Flash loan profitability, game theory, tokenomics analysis
- [Composability Attacks](composability-attacks.md) - Cross-protocol attack patterns (oracle, liquidity, donation)
- [Exploit Case Studies](exploit-case-studies.md) - Forensic analysis of $100M+ historical hacks
- [Learning Path & Attack Vectors](learning-path-attack-vectors.md) - Structured learning path with top 10 attack patterns

### Security Patterns
- [Secure Pattern Reference](secure-pattern-reference.md) - Quick-reference for correct implementations (CEI, oracles, vaults)
- [Gas Optimization Security](gas-optimization-security.md) - When gas optimization introduces vulnerabilities
- [Fix Verification Patterns](fix-verification-patterns.md) - Ensuring fixes don't introduce new bugs

### Protocol-Specific
- [Fork Audit](fork-audit.md) - Diff-based methodology for auditing protocol forks
- [Upgrade & Migration Patterns](upgrade-migration-patterns.md) - Proxy, initialization, and storage layout security

### Reporting
- [Audit Report Templates](audit-report-templates.md) - Finding format, severity matrix, PoC templates, executive summary

### Skill Quality & Authoring
- [Quality Scoring](quality-scoring.md) - 10-point Anthropic best practices scoring framework for evaluating skill quality
- [Skill TDD Methodology](skill-tdd.md) - Test-Driven Documentation: pressure test → baseline → write → verify → close loopholes
- [Skill Authoring Guide](skill-authoring-guide.md) - Three creation paths, progressive disclosure, quality guarantee loop, version tracking

## Usage
```
1. Start with LLM Audit Workflow for structured phase-by-phase approach
2. Apply protocol-specific methodology (fork-audit, economic-modeling, etc.)
3. Use testing tools (invariant testing, symbolic execution) for verification
4. Write PoCs following poc-writing-guide
5. Generate report using audit-report-templates
```

## Related Skills
- [Checklists](../checklists/index.md) - Protocol-specific audit checklists
- [Patterns](../patterns/) - Vulnerability pattern library
- [Exploit Forensics](../exploit-forensics/) - Historical exploit deep dives
- [Severity](../severity/) - Finding severity classification

## Prerequisites

Methodology skills require familiarity with at least one blockchain platform. Formal verification methods (Halmos, Certora) require their respective tool installations.

## Validation

To verify methodology completeness, validate all referenced files exist:

```bash
# Verify all methodology files are present
for f in llm-audit-workflow.md invariant-testing.md symbolic-execution.md poc-writing-guide.md; do
  test -f "$f" && echo "OK: $f" || echo "MISSING: $f"
done
```

```python
# Test methodology coverage
def validate_methodology_files():
    required = ['llm-audit-workflow.md', 'invariant-testing.md', 'poc-writing-guide.md']
    for f in required:
        assert os.path.exists(f), f"Missing methodology file: {f}"
    print("All methodology files verified")
```

```yaml
# Methodology selection guide
audit_type: full
required_methods:
  - llm-audit-workflow  # ALWAYS required
  - invariant-testing    # Required for DeFi
optional_methods:
  - symbolic-execution   # For formal verification
  - economic-modeling    # For tokenomics review
```

## Behavior Guidelines

- LLM Audit Workflow MUST be the starting point for all AI-assisted audits
- Invariant testing is **required** for DeFi protocol audits
- Symbolic execution may optionally be applied when formal guarantees are needed
- PoC writing is ALWAYS expected for HIGH and CRITICAL severity findings

## References

- [Methodology References](references/README.md) - Workflow comparison charts and tool integration guides
