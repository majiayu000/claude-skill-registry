---
name: quality-verify
description: Verify the final deliverable meets all quality criteria before delivery. Use as the final validation step to ensure the output meets the user's quality standards across all 6 dimensions.
---

# Quality Verify Skill

## Purpose

Final validation that the formatted deliverable meets ALL quality standards before delivery. This is the last gate - if it passes here, it's ready to go.

## Quality Dimensions

The system checks against 6 quality dimensions. Evaluate each:

### 1. **Completeness**
- Does the deliverable have all required parts?
- Nothing missing or obviously incomplete?
- All requirements from the user met?

### 2. **Correctness**
- Is the code syntactically correct? (No errors)
- Are facts/information accurate?
- Does it do what was asked?
- No logical errors?

### 3. **Consistency**
- Formatting consistent throughout?
- Naming conventions consistent?
- Style consistent?
- Patterns applied consistently?

### 4. **Performance** (when applicable)
- Is it efficient? (Code shouldn't be obviously slow)
- Does it scale? (For large inputs/data)
- Any obvious performance issues?

### 5. **Security** (when applicable)
- No obvious vulnerabilities?
- Inputs validated/sanitized?
- No hardcoded secrets?
- Following security best practices?

### 6. **Maintainability**
- Is it readable?
- Is it documented?
- Would someone else understand it?
- Easy to modify later?

## Scoring System

Rate each dimension:

- **✓ Excellent** (90-100): Exceeds standards, professional quality
- **✓ Good** (75-89): Meets standards, ready to deliver
- **⚠ Acceptable** (60-74): Meets minimum standards, could be better
- **✗ Needs Work** (0-59): Below standards, needs revision

## Scoring Algorithm

```
Overall Score = Average of all applicable dimensions

0 Critical Issues = Base score
- 10 points per critical issue (e.g., code doesn't run, major security flaw)
- 5 points per major issue (e.g., missing section, formatting inconsistent)
- 2 points per minor issue (e.g., typo, minor inconsistency)

Final Score = Base score - deductions

80+ = Ready to Deliver ✓
60-79 = Minor fixes recommended
<60 = Major revision needed
```

## Process

1. Review the formatted deliverable
2. Load user's standards using StandardsRepository to understand what "good" means for this type
3. Evaluate against each quality dimension
4. Score each dimension
5. Calculate overall quality score
6. Identify any issues found
7. Provide detailed feedback

## Loading Standards

Use StandardsRepository to access quality criteria:

```javascript
const standards = standardsRepository.getStandards(context.projectType)
if (standards && standards.qualityCriteria) {
  // Check against their quality criteria definitions
  const criteria = standards.qualityCriteria
  // Verify deliverable meets: completeness, correctness, consistency, etc.
  verifyAgainstCriteria(deliverable, criteria)
} else {
  // Use general quality best practices
  verifyAgainstBestPractices(deliverable)
}
```

See `.claude/lib/standards-repository.md` for interface details.

## Output Format

```json
{
  "qualityScore": 92,
  "readyToDeliver": true,
  "dimensionScores": {
    "completeness": 95,
    "correctness": 90,
    "consistency": 88,
    "performance": 85,
    "security": 90,
    "maintainability": 95
  },
  "issuesFound": [
    "list of specific issues (if any)"
  ],
  "issuesSeverity": {
    "critical": [],
    "major": [],
    "minor": ["Missing one edge case test"]
  },
  "notes": "One minor issue found - everything else excellent quality",
  "summary": "Ready to deliver. Recommend adding edge case test.",
  "recommendations": [
    "Add test for empty array edge case"
  ]
}
```

## Success Criteria

### Score 85+
✓ Quality score above 85
✓ No critical issues
✓ Ready to deliver immediately

### Score 70-84
⚠ Good quality, minor issues
⚠ Should fix minor issues before delivery
⚠ Ask user: "Fix these, or deliver as-is?"

### Score <70
✗ Significant issues found
✗ Should not deliver in current state
✗ Recommend major revision

## Example Quality Checks

### Code Feature Quality Check

**Deliverable**: React dropdown component

**Checks**:
- ✓ Completeness: Has all required methods, props, event handlers
- ✓ Correctness: Code runs without errors, keyboard nav works
- ✓ Consistency: Naming consistent, formatting consistent
- ✓ Performance: No obvious inefficiencies, reasonable re-render count
- ✓ Security: Properly sanitizes user input, no XSS vulnerabilities
- ✓ Maintainability: Well-commented, clear variable names, easy to modify

**Score**: 94/100
**Issues**: None
**Recommendation**: Ready to deliver

### Documentation Quality Check

**Deliverable**: API endpoint documentation

**Checks**:
- ✓ Completeness: All endpoints documented, all parameters described
- ✓ Correctness: Information matches actual API behavior
- ✓ Consistency: Formatting consistent, examples follow same pattern
- ✓ Clarity: Easy to understand for new developers
- ⚠ Maintainability: Missing error response examples (minor)

**Score**: 82/100
**Issues**: ["Missing examples for error responses"]
**Recommendation**: Add error response examples, then deliver

## Decision Tree

```
Score 85+ → Ready to Deliver ✓
Score 70-84 → Ask about minor issues
Score <70 → Recommend major revision
```

## Notes for Implementation

- Be specific about issues found, not vague
- When recommending fixes, explain why they matter
- If user's standards are unclear, use general quality best practices
- Quality is subjective - but consistency is objective (did it follow their standards?)
- Better to be slightly harsh than let bad work through
