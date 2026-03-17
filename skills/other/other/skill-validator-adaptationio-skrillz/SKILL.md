---
name: skill-validator
description: Ensure Claude Code skills meet quality standards through validation operations for structure, content, patterns, and production readiness. Task-based validation with pass/fail criteria, automated checks, and compliance reporting. Use when validating skills before deployment, ensuring standards compliance, certifying production readiness, or quality gating skill releases.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Skill Validator

## Overview

skill-validator ensures Claude Code skills meet established quality standards through systematic validation operations. Unlike review-multi (which scores 1-5), skill-validator provides pass/fail validation against minimum standards for production deployment.

**Purpose**: Quality gate for skill deployment - ensure minimum standards met

**The 4 Validation Operations**:
1. **Validate Structure** - YAML, files, naming must pass minimum standards
2. **Validate Content** - Essential sections and examples must be present
3. **Validate Pattern** - Architecture pattern correctly implemented
4. **Validate Production Readiness** - All critical criteria met for deployment

**Difference from review-multi**:
- **review-multi**: Scores 1-5, identifies improvements, comprehensive assessment
- **skill-validator**: Pass/fail, minimum standards, deployment gating

**Use Together**: review-multi for comprehensive assessment, skill-validator for go/no-go decisions

## When to Use

Use skill-validator when:

1. **Pre-Deployment Gating** - Validate skill ready for production before releasing
2. **Quality Standards Enforcement** - Ensure all skills meet minimum bar
3. **Continuous Integration** - Automated validation in build/deploy pipelines
4. **Certification** - Certify skills meet ecosystem standards
5. **Post-Update Validation** - Ensure changes didn't break compliance
6. **Ecosystem Consistency** - Maintain quality across all skills
7. **Binary Decision Needed** - Ship or don't ship (not "what's the score")

## Operations

### Operation 1: Validate Structure

**Purpose**: Ensure skill structure meets minimum standards for deployment

**Pass Criteria** (All must pass):
- ✅ YAML frontmatter valid with required fields (name, description)
- ✅ `name` in kebab-case format
- ✅ `description` includes 3+ trigger keywords minimum
- ✅ SKILL.md exists
- ✅ File naming follows conventions
- ✅ No critical structure violations

**Process**:
1. Run automated validation: `python3 review-multi/scripts/validate-structure.py <skill>`
2. Check score: Must be ≥4 to pass
3. Verify no critical issues
4. Document pass/fail

**Validation**: **PASS** if structure score ≥4, **FAIL** if <4

**Time**: 5-10 minutes (automated)

---

### Operation 2: Validate Content

**Purpose**: Ensure essential content sections and examples present

**Pass Criteria** (All must pass):
- ✅ Overview/Introduction section present
- ✅ When to Use section with 3+ scenarios minimum
- ✅ Main content present (workflow steps OR operations OR reference)
- ✅ At least 3 examples present (code/command)
- ✅ Some form of best practices or guidance

**Process**:
1. Check for Overview section (## Overview or ## Introduction)
2. Check for When to Use section with scenarios
3. Verify main content exists (steps, operations, or reference material)
4. Count examples (look for ``` code blocks, minimum 3)
5. Check for Best Practices, Common Mistakes, or guidance section

**Validation**: **PASS** if all 5 criteria met, **FAIL** if any missing

**Time**: 10-15 minutes (manual check)

---

### Operation 3: Validate Pattern

**Purpose**: Ensure architecture pattern correctly implemented

**Pass Criteria** (Pattern-specific):

**For Workflow Skills**:
- ✅ Sequential steps present
- ✅ Steps have consistent structure
- ✅ Prerequisites or Post-Workflow section exists

**For Task Skills**:
- ✅ Operations section present
- ✅ Operations have consistent structure
- ✅ Operations are independent (no forced sequence)

**For Reference Skills**:
- ✅ Topic-based organization
- ✅ Quick Reference present

**Process**:
1. Identify pattern type (workflow/task/reference)
2. Check pattern-specific criteria
3. Verify pattern consistency throughout
4. Document compliance

**Validation**: **PASS** if pattern correctly implemented, **FAIL** if pattern violated

**Time**: 10-20 minutes (manual check)

---

### Operation 4: Validate Production Readiness

**Purpose**: Comprehensive pass/fail check for deployment readiness

**Pass Criteria** (All must pass):
- ✅ Structure validation passes (Operation 1)
- ✅ Content validation passes (Operation 2)
- ✅ Pattern validation passes (Operation 3)
- ✅ No critical anti-patterns (from review-multi if available)
- ✅ SKILL.md completeness (not stub or incomplete)
- ✅ Examples are concrete (not all placeholders)

**Process**:
1. Run Operations 1-3
2. Check for critical anti-patterns:
   - Monolithic SKILL.md (>2,000 lines, no references)
   - All examples are placeholders
   - Major sections missing
3. Assess overall completeness
4. Make deployment decision

**Validation**: **PASS** if all criteria met (ready to deploy), **FAIL** if any critical issue

**Time**: 30-45 minutes (combines all operations)

**Output**: **DEPLOY** or **HOLD** decision

---

## Validation Report Format

```markdown
# Skill Validation Report: [Skill Name]

**Validation Date**: [Date]
**Validator**: [Name]

## Validation Results

Operation 1: Structure Validation
Status: ✅ PASS | ❌ FAIL
- YAML: [Pass/Fail]
- Files: [Pass/Fail]
- Naming: [Pass/Fail]
- Structure Score: [X]/5

Operation 2: Content Validation
Status: ✅ PASS | ❌ FAIL
- Overview: [Present/Missing]
- When to Use: [X scenarios - Pass if ≥3]
- Main Content: [Present/Missing]
- Examples: [X examples - Pass if ≥3]
- Guidance: [Present/Missing]

Operation 3: Pattern Validation
Status: ✅ PASS | ❌ FAIL
- Pattern: [Workflow/Task/Reference]
- Implementation: [Correct/Incorrect]
- Consistency: [Yes/No]

Operation 4: Production Readiness
Status: ✅ READY TO DEPLOY | ❌ HOLD

Critical Issues: [List if any]

## Deployment Decision

✅ DEPLOY - All validations passed, ready for production

OR

❌ HOLD - Critical issues must be fixed:
1. [Issue 1 with fix]
2. [Issue 2 with fix]
```

---

## Best Practices

### 1. Validate Before Deploy
**Practice**: Run skill-validator on all skills before production deployment

**Rationale**: Catches critical issues, prevents shipping broken skills

**Application**: Make validation part of deployment checklist

### 2. Use as Quality Gate
**Practice**: Skills must pass validation to be deployed

**Rationale**: Maintains ecosystem quality baseline

**Application**: No exceptions - PASS required for deployment

### 3. Automate Where Possible
**Practice**: Use review-multi automation for structure validation

**Rationale**: 95% automated, fast, consistent

**Application**: Run validate-structure.py as first check

### 4. Document Failures Clearly
**Practice**: When skill fails, specify exactly what to fix

**Rationale**: Actionable feedback enables quick fixes

**Application**: List specific issues with remediation steps

### 5. Re-Validate After Fixes
**Practice**: After fixing issues, run validation again to confirm

**Rationale**: Ensures fixes actually resolve issues

**Application**: Validate → Fix → Re-validate cycle

---

## Quick Reference

### The 4 Validations

| Operation | Focus | Pass Criteria | Time | Automation |
|-----------|-------|---------------|------|------------|
| **Structure** | YAML, files, naming | Score ≥4 | 5-10m | 95% (use review-multi) |
| **Content** | Sections, examples | 5 criteria all met | 10-15m | 40% |
| **Pattern** | Architecture compliance | Pattern correct | 10-20m | 50% |
| **Production Readiness** | Overall deployment decision | All validations pass | 30-45m | Combined |

### Minimum Standards

**Structure**:
- Valid YAML with name + description
- name in kebab-case
- 3+ trigger keywords
- SKILL.md exists
- Basic file structure

**Content**:
- Overview present
- 3+ When to Use scenarios
- Main content present
- 3+ examples
- Some guidance/best practices

**Pattern**:
- Correct pattern implementation
- Consistent structure
- Pattern-specific requirements met

**Production**:
- All validations pass
- No critical anti-patterns
- Completeness (not stub)
- Examples concrete

### Deployment Decision Tree

```
Run validation operations 1-4
     ↓
All PASS?
├─ Yes → ✅ DEPLOY (production ready)
└─ No → Which failed?
    ├─ Structure → Fix YAML/files (critical)
    ├─ Content → Add missing sections (critical)
    ├─ Pattern → Fix implementation (critical)
    └─ After fixes → Re-validate → Deploy if pass
```

### Integration with review-multi

**Use Both**:
1. **skill-validator**: Pass/fail, deployment gating
2. **review-multi**: 1-5 scoring, comprehensive assessment, improvements

**Workflow**:
```
Build skill → skill-validator (PASS?) → review-multi (score?) →
Deploy (if PASS) + Note improvements (from review-multi)
```

---

**skill-validator** provides quality gating for skill deployment, ensuring minimum standards met before production release.
