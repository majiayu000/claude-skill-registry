---
id: differential-review
title: Differential Review Skill
category: methodology
difficulty: intermediate
triggers:
  - diff review
  - upgrade review
  - compare versions
  - code changes
  - contract upgrade
  - version diff
related_skills:
  - fix-review/SKILL.md
  - methodology/SKILL.md
tags:
  - differential
  - upgrade
  - comparison
  - versioning
last_updated: 2026-02-26
description: >-
  Compare two versions of a codebase to identify security implications
  of changes. Use when reviewing protocol upgrades, verifying bug fixes,
  auditing dependency updates, or when only a subset of code has changed
  since the last audit.
---

# Differential Review Skill

Compare two versions of a codebase to identify security implications of changes. Essential for protocol upgrades, bug fix verification, and dependency updates.

---

## Why Differential Review?

A full audit of an already-audited codebase is wasteful if only 5% of the code changed. Differential review focuses effort on:

| Change Type | Risk Level | Examples |
|-------------|------------|----------|
| Logic changes | HIGH | Modified calculation, new branching, changed access control |
| State variable changes | HIGH | New storage, modified types, reordered variables |
| Dependency updates | MEDIUM-HIGH | OpenZeppelin upgrade, Solidity version change |
| Configuration changes | MEDIUM | Changed thresholds, updated addresses, new roles |
| Formatting only | NONE | Whitespace, comments, variable renames |
| New code | HIGH | Entirely new functions/contracts |
| Removed code | MEDIUM | Deleted security checks, removed functionality |

---

## Change Classification Matrix

| Change | Security Relevant? | Needs Review? |
|--------|-------------------|---------------|
| Function body modified | YES | ALWAYS |
| New function added | YES | FULL AUDIT |
| Function removed | MAYBE | Check if security-critical |
| Access control modified | YES | ALWAYS |
| Storage variable added | YES (upgrade compat) | ALWAYS |
| Storage variable removed | YES (dangerous) | ALWAYS |
| Storage variable reordered | YES (proxy breakage) | ALWAYS |
| Import changed | MAYBE | Check changelog |
| Compiler version changed | MAYBE | Check breaking changes |
| Comment changed | NO | Skip |
| Whitespace changed | NO | Skip |
| Event added/modified | LOW | Quick review |
| Error message changed | NO | Skip |
| Constant changed | MAYBE | Verify new value |

---

## Differential Review Strategy

### Step 1: Generate the Diff

```bash
# Between two git tags/commits
git diff v1.0..v2.0 -- '*.sol'
git diff v1.0..v2.0 --stat  # Summary of changed files

# Between two branches
git diff main..feature-branch -- 'contracts/'

# Exclude non-code changes
git diff v1..v2 -- '*.sol' ':!test/' ':!script/'
```

### Step 2: Categorize Changes

Sort the diff output into categories:

1. **Modified contracts** → Primary review target
2. **New contracts** → Full audit required
3. **Deleted contracts** → Check for orphaned references
4. **Modified tests** → Understand what changed and why
5. **Config changes** → Deployment parameter review

### Step 3: Impact Analysis

For each modified function:
- What did it do before?
- What does it do now?
- What invariants could break?
- Does the change affect other functions?
- Are existing tests still valid?

---

## Common Upgrade Pitfalls

| Pitfall | Example | Impact |
|---------|---------|--------|
| Storage slot collision | Adding variable before existing ones in upgradeable proxy | Critical — corrupted state |
| Initializer re-callable | `initialize()` without `initializer` guard after upgrade | Critical — protocol takeover |
| `selfdestruct` in new impl | Attacker calls `selfdestruct` on implementation | Critical — proxy bricked |
| Removed security check | Deleted `onlyOwner` modifier in upgrade | Critical — access control loss |
| Changed function selector | Renamed function breaks integrations | High — broken integrations |
| Immutable value changed | Constructor value differs in new deployment | Medium — unexpected behavior |

---

## Resources
- [Upgrade Safety](resources/upgrade-safety.md)

## Workflows
- [Differential Audit](workflows/differential-audit.md)
