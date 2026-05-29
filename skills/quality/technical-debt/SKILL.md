---
name: technical-debt
description: This skill provides patterns for identifying, categorizing, and tracking technical debt. It includes scoring methodologies, YAML schemas for tracking files, and strategies for systematic debt resolution.
---

# Technical Debt Skill

Systematically identify, track, and resolve technical debt.

## When to Use

- Scanning codebase for technical debt
- Categorizing and prioritizing debt items
- Creating debt tracking files
- Planning debt resolution sprints
- Measuring debt trends over time

## Reference Documents

- [Debt Categories](./references/debt-categories.md) - Types of technical debt
- [Debt Scoring](./references/debt-scoring.md) - Impact/effort scoring matrix
- [Debt Frontmatter](./references/debt-frontmatter.md) - YAML schema for debt files
- [Debt Resolution](./references/debt-resolution.md) - Strategies for paying down debt

## Core Concepts

### What is Technical Debt?

Technical debt is the implied cost of future rework caused by choosing an easy solution now instead of a better approach that would take longer.

### Debt Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Code Debt** | Poor code quality | Duplication, complexity, no tests |
| **Architecture Debt** | Structural issues | Wrong patterns, tight coupling |
| **Test Debt** | Insufficient testing | Low coverage, flaky tests |
| **Documentation Debt** | Missing/outdated docs | No API docs, stale README |
| **Dependency Debt** | Outdated dependencies | Security vulnerabilities, EOL |
| **Infrastructure Debt** | Ops/DevOps issues | Manual processes, no monitoring |

## Debt Tracking Location

```
.claude/debt/
├── INDEX.md                    # Summary and metrics
├── code/
│   ├── DEBT-001-duplicate-validation.md
│   └── DEBT-002-complex-order-service.md
├── architecture/
│   └── DEBT-003-monolith-coupling.md
├── test/
│   └── DEBT-004-payment-coverage.md
├── documentation/
│   └── DEBT-005-api-docs-outdated.md
└── dependency/
    └── DEBT-006-rails-upgrade.md
```

## Debt File Format

```markdown
---
id: DEBT-001
title: Duplicate validation logic in controllers
category: code
severity: medium
impact: 3
effort: 2
priority: p2
status: open
created: 2024-01-15
tags: [duplication, validation, controllers]
affected_files:
  - app/controllers/orders_controller.rb
  - app/controllers/users_controller.rb
  - app/controllers/products_controller.rb
---

# Duplicate Validation Logic in Controllers

## Description
Validation logic for email, phone, and address is duplicated across multiple controllers instead of being centralized.

## Impact
- **Maintenance**: Changes must be made in multiple places
- **Bugs**: Inconsistent validation between controllers
- **Time**: Extra time reviewing each controller

## Current State
```ruby
# In OrdersController
def validate_email(email)
  email =~ /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i
end

# Same code in UsersController, ProductsController...
```

## Proposed Solution
Extract to a shared validator:
```ruby
# app/validators/contact_validator.rb
class ContactValidator
  def self.valid_email?(email)
    email =~ EMAIL_REGEX
  end
end
```

## Resolution Steps
1. [ ] Create ContactValidator class
2. [ ] Add tests for validator
3. [ ] Update OrdersController
4. [ ] Update UsersController
5. [ ] Update ProductsController
6. [ ] Remove duplicate code

## Related
- DEBT-007: Missing model validations
```

## Workflow: Scanning for Debt

### Step 1: Identify Debt Indicators

```bash
# Code complexity
find . -name "*.py" -exec wc -l {} \; | sort -rn | head -20

# Duplication
jscpd --reporters html --output .claude/debt/reports/

# TODO/FIXME comments
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.ts"

# Long methods
grep -rn "def \|function " --include="*.py" | head -50

# Test coverage gaps
pytest --cov=. --cov-report=term-missing | grep "MISS"
```

### Step 2: Categorize Findings

For each finding:
1. Determine category (code, architecture, test, etc.)
2. Assess severity (low, medium, high, critical)
3. Estimate impact (1-5)
4. Estimate effort (1-5)
5. Calculate priority

### Step 3: Create Debt Files

Create a file in `.claude/debt/[category]/` for each item.

### Step 4: Update Index

```markdown
# Technical Debt Index

**Last Updated:** 2024-01-15
**Total Items:** 12
**Open Items:** 10

## Summary by Category

| Category | Open | In Progress | Resolved |
|----------|------|-------------|----------|
| Code | 4 | 1 | 2 |
| Architecture | 2 | 0 | 0 |
| Test | 2 | 0 | 1 |
| Documentation | 1 | 0 | 0 |
| Dependency | 1 | 0 | 0 |

## Priority Distribution

| Priority | Count |
|----------|-------|
| P0 (Critical) | 1 |
| P1 (High) | 3 |
| P2 (Medium) | 4 |
| P3 (Low) | 2 |

## High Priority Items

1. **DEBT-006** [P0] Rails security update required
2. **DEBT-003** [P1] Monolith service coupling
3. **DEBT-001** [P1] Duplicate validation logic
```

## Priority Calculation

```
Priority Score = Impact × Effort Weight

Impact (1-5):
  5 = Critical (security, data loss risk)
  4 = High (major feature blocked)
  3 = Medium (development slowed)
  2 = Low (minor inconvenience)
  1 = Minimal (cosmetic)

Effort (1-5):
  1 = Hours (quick fix)
  2 = Days (small task)
  3 = Week (medium task)
  4 = Weeks (large task)
  5 = Months (major project)

Priority Mapping:
  Score 15-25: P0 (Critical)
  Score 9-14:  P1 (High)
  Score 4-8:   P2 (Medium)
  Score 1-3:   P3 (Low)
```

## Quick Reference

### Debt Indicators

| Indicator | Category | Severity |
|-----------|----------|----------|
| Duplicated code | Code | Medium |
| Complex methods (>50 lines) | Code | Medium |
| Missing tests | Test | High |
| Outdated dependencies | Dependency | Varies |
| No error handling | Code | High |
| Hardcoded values | Code | Low |
| Missing documentation | Documentation | Low |
| Circular dependencies | Architecture | High |

### Resolution Strategies

| Strategy | When to Use |
|----------|-------------|
| **Boy Scout Rule** | Small improvements during regular work |
| **Dedicated Sprint** | Critical or blocking debt |
| **20% Time** | Ongoing maintenance |
| **Refactoring Friday** | Regular small fixes |
| **Major Rewrite** | Fundamental architecture issues |
