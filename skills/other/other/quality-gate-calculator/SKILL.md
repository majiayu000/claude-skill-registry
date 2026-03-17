---
name: quality-gate-calculator
description: Calculates context-appropriate quality gate thresholds based on work type (Feature/Bug/Hotfix/Docs/Refactor). Ensures rigorous standards for features, pragmatic standards for hotfixes, and 100% test pass rate for all work.
---

# Quality Gate Calculator Skill

**Purpose**: Calculate appropriate quality gates based on work type and phase.

**When to Use**: At workflow start to set expectations, and at phase transitions to validate progress.

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# Basic usage
bash .claude/skills/quality-gate-calculator/execute.sh <work-type> <phase>

# Examples:
bash .claude/skills/quality-gate-calculator/execute.sh Feature 3
bash .claude/skills/quality-gate-calculator/execute.sh Hotfix 1
bash .claude/skills/quality-gate-calculator/execute.sh Bug 4
```

**Parameters**:
- `work-type`: Feature|Bug|Hotfix|Documentation|Refactoring (required)
- `phase`: 1|2|3|4|5 (required)

**Script outputs**:
- Required percentage for quality gate
- Target score (points needed to pass)
- Rationale for threshold
- Pass/fail examples
- Exports quality gate to /tmp/quality-gate.env

**Exit codes**:
- 0: Quality gate calculated successfully
- 1: Invalid work type or phase

## Quality Gate Philosophy

**Not all work is equal:**
- **Features**: Highest rigor (new functionality, high risk)
- **Bug Fixes**: Moderate rigor (fixing existing code)
- **Hotfixes**: Minimal rigor (production emergency)
- **Documentation**: High completion, moderate validation
- **Refactoring**: High quality, no behavior change

**Universal Rule**: ALL work types require 100% test pass rate in Phase 4.

## Quality Gate Matrix

### Phase 1: Requirements

| Work Type | Required % | Score Target | Rationale |
|-----------|------------|--------------|-----------|
| Feature | 95% | 24/25 points | Complete requirements critical for feature success |
| Bug Fix | 80% | 20/25 points | Focus on problem and fix, less ceremony |
| Hotfix | 70% | 18/25 points | Emergency - just enough to understand issue |
| Documentation | 85% | 21/25 points | Clear purpose and scope needed |
| Refactoring | 90% | 23/25 points | Understand current state and goals |

### Phase 2: Design

| Work Type | Required % | Score Target | Rationale |
|-----------|------------|--------------|-----------|
| Feature | 90% | 32/35 points | Thorough design prevents implementation issues |
| Bug Fix | 70% | 25/35 points | Focus on fix design, skip elaborate specs |
| Hotfix | 60% | 21/35 points | Quick design - enough to implement safely |
| Documentation | 80% | 28/35 points | Structure and organization plan |
| Refactoring | 85% | 30/35 points | Detailed refactoring plan with safety checks |

### Phase 3: Implementation

| Work Type | Required % | Score Target | Rationale |
|-----------|------------|--------------|-----------|
| Feature | 85% | 43/50 points | High code quality for new features |
| Bug Fix | 75% | 38/50 points | Focus on fix, tests, and no regressions |
| Hotfix | 70% | 35/50 points | Working fix with minimal tests |
| Documentation | 80% | 40/50 points | Complete documentation with examples |
| Refactoring | 90% | 45/50 points | Highest quality - no behavior changes allowed |

### Phase 4: Testing

| Work Type | Required % | Test Pass Rate | Rationale |
|-----------|------------|----------------|-----------|
| Feature | 100% | 100% | **ALL tests must pass** |
| Bug Fix | 100% | 100% | **ALL tests must pass** |
| Hotfix | 100% | 100% | **ALL tests must pass** |
| Documentation | 100% | 100% | **ALL tests must pass** |
| Refactoring | 100% | 100% | **ALL tests must pass** |

**CRITICAL**: Phase 4 is ZERO TOLERANCE for all work types. One failing test = cannot advance.

### Phase 5: Finalization

| Work Type | Required % | Score Target | Rationale |
|-----------|------------|--------------|-----------|
| Feature | 80% | 80/100 points | Complete documentation and cleanup |
| Bug Fix | 75% | 75/100 points | Document fix and lessons learned |
| Hotfix | 70% | 70/100 points | Basic documentation, commit, deploy |
| Documentation | 90% | 90/100 points | Comprehensive docs and cross-references |
| Refactoring | 85% | 85/100 points | Document changes and performance impact |

## Usage Examples

### From Orchestrator (Workflow Start)
```
Use the quality-gate-calculator skill to set quality gates for this feature work
```

### Manual Calculation
```bash
# Calculate quality gate for bug fix in design phase
bash .claude/skills/quality-gate-calculator.md Bug 2

# Calculate for hotfix in implementation
bash .claude/skills/quality-gate-calculator.md Hotfix 3
```

### From Validator
```bash
# Phase validator loads quality gate
source /tmp/quality-gate.env
echo "Required: $REQUIRED_PERCENTAGE%"
echo "Target: $TARGET_SCORE / $MAX_SCORE"
```

## Decision Flowchart

```
Start Workflow
     |
     v
Identify Work Type
     |
     +-- Is it production emergency? --> Hotfix (70-100%)
     |
     +-- Is it fixing existing bug? --> Bug Fix (75-100%)
     |
     +-- Is it new functionality? --> Feature (85-100%)
     |
     +-- Is it improving code? --> Refactoring (85-100%)
     |
     +-- Is it documentation? --> Documentation (80-100%)
     v
Calculate Quality Gates for Each Phase
     v
Store in Workflow Context
     v
Apply at Each Phase Validation
```

## Work Type Classification Guide

### Feature
**Characteristics**:
- Adds new functionality
- Creates new user-facing capabilities
- Introduces new APIs or components

**Examples**:
- "Add event registration system"
- "Implement user dashboard"
- "Create teacher profile pages"

### Bug Fix
**Characteristics**:
- Fixes existing functionality
- Addresses reported issues
- Resolves unexpected behavior

**Examples**:
- "Fix login button not working"
- "Resolve event date display issue"
- "Correct user role assignment"

### Hotfix
**Characteristics**:
- Production emergency
- Blocking critical functionality
- Requires immediate deployment

**Examples**:
- "Fix payment processing failure"
- "Resolve database connection timeout"
- "Patch security vulnerability"

### Documentation
**Characteristics**:
- Creates or updates documentation
- No code changes (or minimal)
- Improves developer/user understanding

**Examples**:
- "Document API endpoints"
- "Create onboarding guide"
- "Update architecture diagrams"

### Refactoring
**Characteristics**:
- Improves code quality
- No behavior changes
- Performance or maintainability focus

**Examples**:
- "Extract service layer"
- "Optimize database queries"
- "Simplify component structure"

## Integration with Validators

Each phase validator loads work type-specific quality gates:

```bash
#!/bin/bash
# In phase-1-validator.md

# Load quality gate for this work type
source /tmp/quality-gate.env

# Use in validation
if [ "$PERCENTAGE" -ge "$REQUIRED_PERCENTAGE" ]; then
    echo "✅ PASS - Meets quality gate"
else
    echo "❌ FAIL - Below quality gate"
    echo "   Required: $REQUIRED_PERCENTAGE%"
    echo "   Actual: $PERCENTAGE%"
fi
```

## Common Issues

### Issue: Work Type Misclassification
**Problem**: Feature classified as bug fix to lower quality gates
**Impact**: Lower quality work slips through
**Solution**: Orchestrator validates work type at workflow start

### Issue: Quality Gate Gaming
**Problem**: Developer tries to lower requirements
**Impact**: System integrity compromised
**Solution**: Quality gates are non-negotiable per work type

### Issue: Hotfix Abuse
**Problem**: Everything labeled "hotfix" to skip rigor
**Impact**: Production quality degrades
**Solution**: Hotfix requires prod issue ticket + approval

## Output Format

```json
{
  "qualityGate": {
    "workType": "Feature",
    "phase": 3,
    "phaseName": "Implementation",
    "required": {
      "percentage": 85,
      "score": 43,
      "maxScore": 50
    },
    "rationale": "Features require high code quality for new features",
    "criticalRules": [
      "Phase 4 requires 100% test pass rate regardless of work type"
    ],
    "exported": "/tmp/quality-gate.env"
  }
}
```

## Progressive Disclosure

**Initial Context**: Show work type and required percentage only
**On Request**: Show full matrix with rationale
**During Validation**: Show pass/fail threshold
**On Failure**: Show how far from target and what's needed

---

**Remember**: Quality gates ensure appropriate rigor for the work being done. Features get highest scrutiny, hotfixes get pragmatic validation, but ALL work requires 100% test pass rate. This balances quality with velocity.
