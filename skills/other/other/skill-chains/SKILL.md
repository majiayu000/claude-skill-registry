---
id: skill-chains
title: Skill Chains Skill
category: advanced
difficulty: intermediate
triggers:
  - skill chain
  - audit depth
  - quick scan
  - deep audit
  - full engagement
  - chain workflow
related_skills:
  - advanced/context-detection/SKILL.md
  - methodology/SKILL.md
  - commands/SKILL.md
tags:
  - skill-chains
  - workflow
  - depth-levels
  - advanced
last_updated: 2026-02-26
description: >-
  Ordered sequences of individual audit skills to execute for different
  audit depth levels ensuring comprehensive, systematic coverage. Use when
  selecting between quick scan, standard audit, deep audit, or full
  engagement workflows to match coverage to time and scope constraints.
---

# Skill Chains Skill

## Purpose
Skill chains define ordered sequences of individual audit skills to execute for different audit depth levels. They ensure comprehensive, systematic coverage appropriate to the engagement scope.

## Available Chains

| Chain | Duration | Depth | Use Case |
|-------|----------|-------|----------|
| [Quick Scan](quick-scan-chain.md) | 1-2 hours | Surface | Initial assessment, triage |
| [Deep Dive](deep-dive-chain.md) | 1-2 days | Focused | Specific contract/module analysis |
| [Full Audit](full-audit-chain.md) | 1-2 weeks | Comprehensive | Complete protocol audit |

## Chain Selection Guide
```
Time < 2 hours?  → Quick Scan
Focused on specific area? → Deep Dive
Full engagement? → Full Audit
```

## Design Principles
1. **Progressive Depth**: Each chain level includes all previous levels plus more
2. **Exit Early**: If critical issue found, can escalate from Quick Scan to Deep Dive
3. **Composable**: Deep Dive can be run on specific modules identified by Quick Scan
4. **Reproducible**: Same chain on same code produces same coverage

## Prerequisites

Skill chains require all individual skills referenced in the chain to be available. The [Commands](../../commands/SKILL.md) skill MUST be loaded for chain invocation.

## Validation

To verify chain completeness, validate skill availability:

```python
# Validate all skills in a chain are loadable
def validate_chain(chain_config):
    for step in chain_config['steps']:
        skill_path = f"skills/{step['skill']}/SKILL.md"
        assert os.path.exists(skill_path), f"Missing skill: {skill_path}"
        print(f"Verified: {step['skill']} (order: {step['order']})")
```

```yaml
# Example chain configuration
chain: quick-scan
duration: 1-2 hours
steps:
  - skill: solidity-scanner
    order: 1
    required: true
  - skill: checklists
    order: 2
    required: true
  - skill: severity
    order: 3
    optional: true
```

```bash
# Test chain execution order
python -m pytest tests/skill_chains/ -v --chain quick-scan
```

## Behavior Guidelines

- Chain selection MUST match engagement scope and time constraints
- Quick Scan steps are **required** as a minimum for any engagement
- Deep Dive modules may optionally be added based on Quick Scan findings
- Full Audit chains ALWAYS include all Quick Scan and Deep Dive steps

## References

- [Skill Chains References](references/README.md) - Chain composition diagrams and coverage matrices
