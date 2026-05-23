---
name: curriculum-analyze-outcomes
description: Calculate objective mastery rates, analyze performance distributions, identify achievement gaps, and generate learning analytics dashboards. Use when analyzing assessment data, measuring outcomes, or generating reports. Activates on "analyze results", "learning analytics", "performance data", or "outcome measurement".
---

# Learning Analytics & Outcome Measurement

Analyze assessment data to measure learning objective mastery, identify trends, visualize performance, and generate actionable insights.

## When to Use

- Analyze assessment results
- Calculate mastery rates
- Identify performance patterns
- Generate analytics reports
- Measure learning outcomes

## Required Inputs

- **Assessment Data**: Student scores, responses
- **Learning Objectives**: What was assessed
- **Demographics** (optional): For gap analysis
- **Historical Data** (optional): For trends

## Workflow

### 1. Load and Validate Data

Import:
- Assessment scores by student
- Item-level responses
- Learning objective mappings
- Student demographic data (if analyzing equity)
- Timestamps for trend analysis

### 2. Calculate Objective Mastery Rates

For each learning objective:

```markdown
## Objective LO-1.1 Mastery Analysis

**Objective**: Students will identify the role of chlorophyll in photosynthesis

**Items Assessing This Objective**: MC-1, MC-5, SA-2

**Mastery Threshold**: 75% correct

**Results**:
- **Mastered** (≥75%): 23 students (76.7%)
- **Approaching** (50-74%): 5 students (16.7%)
- **Needs Support** (<50%): 2 students (6.7%)

**Average Score**: 82.3%
**Median Score**: 85%
**Mode**: 90%
**Standard Deviation**: 12.4

**Distribution**:
```
90-100%: ████████████████████ 18 students
80-89%:  ████████ 7 students
70-79%:  ███ 3 students
60-69%:  ██ 2 students
50-59%:  █ 1 student
< 50%:   █ 1 student
```

**Interpretation**:
Strong performance overall. 76.7% of students have mastered this objective, exceeding the target of 70%. Focus support on 2 students struggling significantly.

**Recommendations**:
- Continue current instructional approach (effective for majority)
- Provide small group intervention for 2 students below 50%
- Consider extension activities for 18 students scoring 90%+
```

### 3. Identify High/Low Performing Objectives

```markdown
## Objective Performance Summary

| Objective | Avg Score | Mastery Rate | Status | Action |
|-----------|-----------|--------------|--------|--------|
| LO-1.1 | 82% | 77% | ✅ Strong | Continue |
| LO-1.2 | 78% | 70% | ✅ Adequate | Monitor |
| LO-1.3 | 65% | 45% | ⚠️  Low | Reteach |
| LO-2.1 | 58% | 30% | ❌ Very Low | Redesign |

**Low Performing Objectives** (Mastery < 60%):
- **LO-1.3**: Only 45% mastery - Students struggle with applying concepts
- **LO-2.1**: Only 30% mastery - Major instructional gap

**Analysis**:
Pattern shows students understand content (LO-1.1, LO-1.2 strong) but cannot apply it (LO-1.3, LO-2.1 weak). Need more application practice and scaffolding.
```

### 4. Analyze Achievement Gaps

```markdown
## Equity Analysis

### Performance by Demographic Group

**By Gender**:
| Group | Avg Score | Mastery Rate | Gap |
|-------|-----------|--------------|-----|
| Female | 78% | 72% | +5% |
| Male | 73% | 67% | Baseline |

**Analysis**: Small gap favoring female students (5 percentage points). Not statistically significant but worth monitoring.

**By Race/Ethnicity**:
| Group | Avg Score | Mastery Rate | Gap |
|-------|-----------|--------------|-----|
| Asian | 82% | 78% | +8% |
| White | 75% | 70% | Baseline |
| Latino/a | 68% | 58% | -12% |
| Black | 65% | 55% | -15% |

**Analysis**: ⚠️  Significant gaps for Latino/a (-12%) and Black students (-15%). This requires immediate attention to ensure equitable outcomes.

**Potential Contributing Factors**:
- Language barriers in assessment items?
- Cultural bias in examples/scenarios?
- Prior knowledge gaps?
- Instructional approach not reaching all learners?

**Recommendations**:
1. Review assessment items for bias (use /curriculum.review-bias)
2. Check prerequisite mastery by group
3. Implement culturally responsive teaching strategies
4. Provide targeted support for affected groups
5. Monitor gap closure in future assessments

**By Socioeconomic Status** (Free/Reduced Lunch):
| Group | Avg Score | Mastery Rate | Gap |
|-------|-----------|--------------|-----|
| Not FRL | 77% | 73% | +7% |
| FRL | 70% | 66% | Baseline |

**Analysis**: Moderate gap (7 points). Consider resource access issues.
```

### 5. Item Analysis (Psychometrics)

```markdown
## Assessment Item Quality

| Item | Difficulty (p) | Discrimination (D) | Quality | Action |
|------|---------------|-------------------|---------|--------|
| MC-1 | 0.85 | 0.45 | ✅ Good | Keep |
| MC-2 | 0.52 | 0.60 | ✅ Excellent | Keep |
| MC-3 | 0.95 | 0.15 | ⚠️  Too Easy, Low Disc | Revise |
| MC-4 | 0.25 | 0.10 | ❌ Too Hard, Low Disc | Replace |

**Metrics**:
- **Difficulty (p-value)**: Proportion answering correctly
  - 0.85 = 85% correct = Easy
  - 0.50 = 50% correct = Moderate
  - 0.25 = 25% correct = Hard
- **Discrimination**: Correlation with total score
  - >0.40 = Excellent
  - 0.30-0.39 = Good
  - 0.20-0.29 = Fair
  - <0.20 = Poor (doesn't distinguish high/low performers)

**Item MC-4 Analysis**:
Very difficult (only 25% correct) AND poor discrimination (0.10). This suggests item is flawed—even high performers get it wrong. Review for:
- Ambiguous wording
- Trick question
- Content not taught
- Multiple defensible answers

**Recommendations**:
- Replace MC-4 with clearer item
- Make MC-3 slightly more challenging
- Keep MC-1 and MC-2 (functioning well)
```

### 6. Generate Analytics Dashboard

Create visual summary:

```markdown
# Learning Analytics Dashboard: [COURSE/UNIT]

**Period**: [Date Range]
**Students**: [N]
**Assessments**: [Count]

## At-a-Glance Metrics

📊 **Average Course Performance**: 74% (C+)
📈 **Objective Mastery Rate**: 68% (14/20 objectives)
⚠️  **At-Risk Students**: 5 (16.7%)
✅ **High Performers**: 12 (40%)

## Objective Mastery Heatmap

```
Unit 1:  ████████░░ 80% mastery
Unit 2:  ██████░░░░ 60% mastery  ⚠️
Unit 3:  ███████░░░ 70% mastery
```

## Performance Distribution

```
A (90-100%): ██████████ 10 students (33%)
B (80-89%):  ████████ 8 students (27%)
C (70-79%):  ████ 4 students (13%)
D (60-69%):  ███ 3 students (10%)
F (< 60%):   █████ 5 students (17%)  ⚠️
```

## Trend Analysis

[Line graph showing performance over time]
- Week 1: 65%
- Week 3: 72%
- Week 5: 74%
- Trend: +9 percentage points improvement 📈

## Top Recommendations

1. **Reteach Unit 2 objectives** (low mastery)
2. **Intervene with 5 at-risk students** (scoring below 60%)
3. **Address achievement gap for Latino/a and Black students** (-12% and -15%)
4. **Replace flawed assessment items** (MC-4)
5. **Provide enrichment for high performers** (12 students ready for extension)

---

**Analytics Metadata**:
- **Generated**: [Date]
- **Data Sources**: [Assessments included]
- **Next Analysis**: [Recommended timing]
```

### 7. CLI Interface

```bash
# Analyze single assessment
/curriculum.analyze-outcomes --assessment "unit1-exam-results.csv" --objectives "objectives.json"

# Course-level analysis
/curriculum.analyze-outcomes --course "BIO-101" --period "Fall 2024" --demographics

# Trend analysis
/curriculum.analyze-outcomes --assessments "results/*.csv" --trend --start "2024-09-01" --end "2024-11-30"

# Equity focus
/curriculum.analyze-outcomes --assessment "results.csv" --equity-analysis --demographics "students.csv"

# Help
/curriculum.analyze-outcomes --help
```

## Composition with Other Skills

**Input from**:
- `/curriculum.grade-assist` - Student scores
- `/curriculum.design` - Learning objectives
- `/curriculum.assess-design` - Assessment structure

**Output to**:
- `/curriculum.iterate-feedback` - Data for revision recommendations
- Educators for decision-making
- Administrators for reporting

## Exit Codes

- **0**: Analysis completed successfully
- **1**: Cannot load assessment data
- **2**: Data format invalid
- **3**: Insufficient data for analysis
- **4**: Missing objective mappings
