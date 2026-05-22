---
name: refactor-risk-assess
description: "[Code Quality] Evaluates risk level of proposed refactoring changes. Use to assess dependencies, blast radius, rollback difficulty, and determine if changes are safe to proceed."
---

# Refactor: Risk Assessment

Evaluate and mitigate risks before executing changes.

## Risk Dimensions

### 1. Blast Radius
| Level | Description | Example |
|-------|-------------|---------|
| LOW | Single file, private methods | Rename local variable |
| MEDIUM | Multiple files, internal APIs | Extract helper class |
| HIGH | Public APIs, many dependents | Change interface signature |

### 2. Reversibility
| Level | Description |
|-------|-------------|
| LOW RISK | Git revert fixes everything |
| MEDIUM | Requires coordinated rollback |
| HIGH | Data migration, external deps |

### 3. Test Coverage
| Coverage | Risk Impact |
|----------|-------------|
| > 80% | Safe to proceed |
| 50-80% | Add tests first |
| < 50% | HIGH RISK |

## Go/No-Go Criteria

**PROCEED if:** Test coverage adequate, Blast radius understood, Rollback plan exists
**BLOCK if:** Critical path no tests, Public API change without review