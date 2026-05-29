---
name: standards-coverage-validator
description: Validate that curriculum fully covers required standards, check depth and rigor of coverage, verify assessment alignment, and generate coverage reports for administrators. Use for comprehensive validation. Activates on "validate coverage", "standards compliance", or "coverage report".
---

# Standards: Coverage Validator

Comprehensively validate standards coverage, depth, and assessment alignment for accountability and compliance.

## When to Use

- End-of-year curriculum validation
- Textbook/program adoption decisions
- Accreditation reviews
- District curriculum audits
- Administrator reporting
- Board presentations

## Validation Dimensions

### 1. Coverage Completeness

**Check**:
- All required standards addressed
- No standards omitted
- Optional vs. required distinction

**Thresholds**:
- ✓ 100% required standards
- ⚠ 95-99% (note missing)
- ✗ <95% (insufficient)

### 2. Depth of Coverage

**Levels**:
- **Insufficient**: Mentioned only, no instruction
- **Basic**: Introduced, minimal practice
- **Proficient**: Taught, practiced, formative assessment
- **Comprehensive**: Mastery expected, multiple assessments

**Validation**: Each standard meets minimum depth requirement

### 3. Cognitive Rigor

**DOK/Bloom's Alignment**:
- Instruction matches standard's cognitive level
- Practice at appropriate complexity
- Assessments test required thinking

**Example**:
- Standard requires "analyze" (DOK 3)
- Instruction must go beyond recall
- Assessment must include analysis tasks

### 4. Assessment Alignment

**Verify**:
- Each standard has assessment items
- Assessment difficulty matches standard
- Sufficient items per standard
- Varied item types

**Quality Checks**:
- Clear alignment (not inferential)
- Valid measurement
- Reliable scoring

### 5. Instructional Time

**Adequacy Check**:
- Sufficient time allocated
- Matches standard complexity
- Proportional to test weight

### 6. Prerequisite Coherence

**Sequence Validation**:
- Prerequisites taught before dependent standards
- Logical progression
- Spiraling/review appropriate

## Validation Report Components

### Executive Summary

**Key Metrics**:
- Overall coverage: X% of standards
- Depth score: Average depth level
- Assessment alignment: X% fully aligned
- Critical gaps: [list if any]
- **Recommendation**: Approved / Conditional / Not Approved

### Detailed Standards Matrix

| Standard | Covered | Depth | DOK Match | Assessed | Time (min) | Status |
|----------|---------|-------|-----------|----------|------------|--------|
| 7.NS.A.1 | ✓ | Proficient | ✓ | ✓ | 120 | ✓ Pass |
| 7.NS.A.2 | ✓ | Basic | ✗ (DOK 2 needed, only DOK 1) | Partial | 45 | ⚠ Needs Improvement |

### Coverage by Domain/Strand

**Visualization**:
- Pie chart or bar graph
- % coverage per strand
- Balance assessment

### Timeline Analysis

**Pacing Validation**:
- Standards coverage over school year
- Front-loaded vs. back-loaded
- Adequate review time before tests

### Assessment Blueprint Comparison

**Test Alignment**:
- Curriculum emphasis vs. test emphasis
- Over-coverage or under-coverage by domain
- Item count adequacy

## Validation Criteria

### Passing Thresholds

**Minimum Requirements**:
- 100% of standards addressed
- Average depth: Proficient (3/4)
- 95% assessment alignment
- No critical gaps
- Prerequisite sequence valid

### Conditional Approval

**Remediation Needed**:
- 95-99% standards covered (minor gaps)
- Some depth issues (average 2.5-3)
- 85-94% assessment alignment
- **Condition**: Address gaps by [date]

### Not Approved

**Significant Issues**:
- <95% standards covered
- Insufficient depth (<2.5 average)
- <85% assessment alignment
- Critical prerequisites missing

## Administrative Reporting

### Board Presentation Format

**Slides Include**:
1. Executive Summary (1 slide)
2. Coverage Overview (visual)
3. Depth and Rigor Analysis
4. Assessment Alignment Summary
5. Comparison to District/State Benchmarks
6. Recommendations

### Accreditation Documentation

**Required Evidence**:
- Standards crosswalk
- Scope and sequence
- Assessment blueprints
- Sample assessments with alignment tags
- Validation summary

## CLI Interface

```bash
# Full validation
/standards.coverage-validator --curriculum "full-year-math-7/" --standards "CCSS-Math-7" --comprehensive-report

# Quick validation
/standards.coverage-validator --content "ela-units/" --standards "State-ELA-5" --quick-check

# Comparison validation
/standards.coverage-validator --program-a "textbook-a/" --program-b "textbook-b/" --standards "NGSS-MS-LS" --compare

# Board report generation
/standards.coverage-validator --curriculum "district-science/" --standards "NGSS-HS" --report-type "board-presentation" --output board-report.pptx

# Accreditation package
/standards.coverage-validator --all-curricula "k-12-curricula/" --standards "all-applicable" --accreditation-package --output accreditation/
```

## Output

- Comprehensive validation report
- Standards coverage matrix
- Pass/Conditional/Fail determination
- Detailed recommendations
- Board presentation (slides/PDF)
- Accreditation documentation package
- Comparison reports (if comparing programs)

## Composition

**Input from**: All curriculum and standards skills
**Final validation** after: `/standards.gap-analysis`, `/standards.us-state-mapper`, `/curriculum.analyze-outcomes`
**Output to**: Administrative reports, compliance documentation

## Exit Codes

- **0**: Validation passed
- **1**: Validation failed (critical issues)
- **2**: Conditional approval (minor issues)
- **3**: Insufficient data for validation
