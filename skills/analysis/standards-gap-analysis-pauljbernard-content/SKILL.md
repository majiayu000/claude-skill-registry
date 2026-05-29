---
name: standards-gap-analysis
description: Identify which standards are covered vs. missing, analyze depth of coverage for each standard, prioritize uncovered standards, and recommend content to fill gaps. Use when auditing curriculum coverage. Activates on "gap analysis", "standards gaps", or "coverage audit".
---

# Standards: Gap Analysis

Identify gaps in standards coverage and provide recommendations for filling them.

## When to Use

- Mid-year curriculum review
- Curriculum audit before testing
- New teacher assessment of materials
- Textbook evaluation
- Scope and sequence validation

## Gap Analysis Components

### 1. Coverage Identification

**Determine**:
- ✓ **Covered**: Standard addressed in curriculum
- ⚠ **Partially Covered**: Standard mentioned but insufficient depth
- ✗ **Not Covered**: Standard missing entirely

### 2. Depth Analysis

**Assess Rigor**:
- **Surface**: Mentioned only
- **Developing**: Some instruction/practice
- **Proficient**: Thorough instruction, multiple practice opportunities
- **Advanced**: Mastery expected, rigorous assessment

**DOK/Bloom's Level**:
- Does coverage match required cognitive level?
- Are assessments at appropriate complexity?

### 3. Time Allocation

**Coverage Duration**:
- Minutes/hours spent on standard
- Number of lessons addressing it
- Practice opportunities
- Assessment items

### 4. Balance Analysis

**Distribution**:
- Are all domains/strands proportionally covered?
- Do coverage percentages match test blueprints?
- Are foundational standards prioritized?

## Gap Types

### Critical Gaps

**High-Stakes Standards**:
- Heavily weighted on state tests
- Prerequisites for future learning
- Grade-level essential content

**Impact**: Immediate remediation needed

### Important Gaps

**Significant Standards**:
- Assessed but lower weight
- Supporting standards
- Enrichment opportunities

**Impact**: Should address before year end

### Minor Gaps

**Supplementary Standards**:
- Optional extensions
- Enrichment only
- Less critical for assessment

**Impact**: Address if time permits

## Prioritization Matrix

| Coverage | Test Weight | Priority |
|----------|-------------|----------|
| Missing | High | **Critical** - Address immediately |
| Partial | High | **High** - Deepen coverage |
| Missing | Medium | **Medium** - Add if possible |
| Partial | Medium | **Low** - Enhance if time |
| Missing | Low | **Optional** - Enrichment only |

## Recommendations

### Filling Gaps

**Strategies by Gap Size**:

**Large Gaps** (missing entire domain):
- Add new unit or extended lessons
- Reteach/introduce
- Consider summer school or intervention

**Medium Gaps** (missing some standards):
- Supplemental lessons
- Integrated practice
- Homework emphasis

**Small Gaps** (insufficient depth):
- Additional practice problems
- Deeper questioning
- More rigorous assessments

## Curriculum Pacing Adjustment

### Time Reallocation

**If Behind**:
1. Identify over-covered standards
2. Reduce time on low-priority standards
3. Combine related standards
4. Streamline activities

**Catch-Up Strategies**:
- Spiral review (integrate into ongoing lessons)
- Homework/extension focus
- Intervention groups
- Technology/independent practice

## CLI Interface

```bash
# Basic gap analysis
/standards.gap-analysis --curriculum "7th-grade-math/" --standards "Common-Core-Math-7"

# With prioritization
/standards.gap-analysis --content "ela-curriculum/" --standards "CCSS-ELA-8" --prioritize --test-blueprint "state-test-weights.json"

# Mid-year check
/standards.gap-analysis --taught-so-far "lessons/week-1-20/" --standards "TEKS-Science-7" --date "January" --remaining-weeks "18"

# Multi-teacher comparison
/standards.gap-analysis --compare-teachers --teacher-a "teacher1/lessons/" --teacher-b "teacher2/lessons/" --standards "State-Math-6"

# Generate action plan
/standards.gap-analysis --curriculum "social-studies/" --standards "C3-Framework-8" --action-plan --timeline "10-weeks"
```

## Output

- Standards coverage matrix
- Gap identification (critical/important/minor)
- Priority recommendations
- Suggested lessons/activities for gaps
- Revised pacing guide
- Action plan with timeline

## Composition

**Input from**: `/standards.us-state-mapper`, `/standards.subject-standards`, `/curriculum.design`
**Works with**: `/standards.coverage-validator`, `/curriculum.iterate-feedback`
**Output to**: Remediation plans, pacing adjustments

## Exit Codes

- **0**: Gap analysis complete
- **1**: Insufficient curriculum data
- **2**: Standards framework mismatch
- **3**: Critical gaps identified (>20% missing)
