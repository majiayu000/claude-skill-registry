---
name: Design Spec Auditor
description: Verify code implementation aligns with design specifications. Use after implementing features, during code reviews, or when refactoring to ensure architectural compliance. Compares design docs with actual code.
---

# Design Spec Auditor

Verify that code implementations match their design specifications and identify inconsistencies.

## Quick Start

**Most common usage:**
```bash
# User says: "Check if parser matches the design doc"
# This skill will:
# 1. Read design doc (design_docs/planned/ or implemented/)
# 2. Read corresponding code
# 3. Compare and identify discrepancies
# 4. Generate compliance report
```

## When to Use This Skill

Invoke when user says:
- "Check if implementation matches design"
- "Audit the parser against its spec"
- "Verify code compliance"
- "Review design alignment"

Also use:
- After implementing new features
- During code reviews
- After refactoring

## Workflow

### Step 1: Identify Design Documents

```bash
# Find relevant design docs
ls design_docs/planned/     # Planned features
ls design_docs/implemented/ # Completed features

# For a specific feature:
find design_docs -name "*parser*" -o -name "*type*"
```

### Step 2: Map Design to Code

For each design component, identify:

| Design Element | Code Location |
|----------------|---------------|
| Module boundaries | `internal/` package structure |
| Interface contracts | Type definitions, function signatures |
| Data flow | Function call chains |
| Error handling | Error types and propagation |

### Step 3: Systematic Comparison

**Check each design requirement:**

1. **Architectural decisions**
   - Are module boundaries respected?
   - Are dependencies one-way as specified?

2. **Interface contracts**
   - Do function signatures match spec?
   - Are return types correct?

3. **Behavioral requirements**
   - Does error handling match spec?
   - Are edge cases covered?

4. **Performance requirements**
   - Are complexity bounds met?
   - Are resource limits respected?

### Step 4: Categorize Discrepancies

| Severity | Definition | Action |
|----------|------------|--------|
| **Critical** | Breaks core architectural principles | Fix code immediately |
| **Major** | Significant behavioral deviation | Fix code or update design |
| **Minor** | Small inconsistency | Document and track |
| **Naming** | Terminology mismatch | Update docs for clarity |
| **Missing** | Specified but not implemented | Add to backlog |
| **Extra** | Implemented but not specified | Update design doc |

### Step 5: Generate Report

**Report format:**

```markdown
# Design Compliance Audit: [Feature Name]

## Summary
- **Compliance**: 85%
- **Critical Issues**: 0
- **Major Issues**: 2
- **Minor Issues**: 5

## Critical Issues
(none)

## Major Issues

### Issue 1: Missing error propagation
- **Design doc**: design_docs/implemented/v0_3_0/effects.md, Section 3.2
- **Code location**: internal/effects/handler.go:145-160
- **Discrepancy**: Design specifies errors should propagate to caller; code silently ignores
- **Recommendation**: Fix code to match design

## Minor Issues
...

## Recommendations
1. Update internal/effects/handler.go to propagate errors
2. Add missing test cases for edge conditions
3. Update design doc section 4.1 to reflect actual behavior
```

## Comparison Checklist

Use this checklist for each audit:

- [ ] Module structure matches design
- [ ] Public APIs match signatures in spec
- [ ] Error types and handling match spec
- [ ] Data structures match definitions
- [ ] Invariants are enforced
- [ ] Performance requirements met
- [ ] Tests cover specified scenarios
- [ ] Edge cases handled as specified

## Common Discrepancy Patterns

### Intentional Deviations
Sometimes code legitimately differs from design:
- Performance optimizations
- Discovered constraints during implementation
- Pragmatic simplifications

**Action**: Update design doc to reflect reality

### Unintentional Oversights
- Forgot to implement a feature
- Misunderstood requirement
- Copy-paste errors

**Action**: Fix code to match design

### Design Drift
Design docs lag behind rapid development:
- Features added without updating docs
- Refactoring changed structure

**Action**: Update design docs

## Example Session

**User**: "Check if the type system matches its design"

**Response**:
```
Auditing type system against design_docs/implemented/v0_3_0/type-system.md...

Reading design doc... Found 15 specified behaviors
Reading code in internal/types/... Found 12 implemented

## Compliance Report: Type System

### Summary
- Compliance: 80%
- Critical: 0
- Major: 1
- Minor: 2

### Major Issues

1. **Row polymorphism extension**
   - Design: Section 4.2 specifies record extension syntax `{...r, x: T}`
   - Code: internal/types/unify.go only supports field access, not extension
   - Action: Implement extension or mark as "planned" in docs

### Minor Issues

1. **Naming**: Design uses "type variable", code uses "tyvar"
2. **Extra**: Code has `TypeCache` not mentioned in design

### Recommendations
1. Implement row extension or update roadmap
2. Add TypeCache to design doc (performance optimization)
```

## Tips

- **Newer docs supersede older ones** - check dates
- **Some deviations are intentional** - document them
- **Focus on behavior, not exact wording**
- **Consider evolution** - designs change over time
