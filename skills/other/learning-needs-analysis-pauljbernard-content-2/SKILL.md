---
name: learning-needs-analysis
description: Conduct comprehensive learning needs analysis including stakeholder interviews, performance gap identification, job/task analysis, and competency mapping. Use when starting any learning project to identify what training is actually needed. Activates on "needs analysis", "training needs", "performance gaps", or "what should we teach".
---

# Learning Needs Analysis

Systematically identify learning needs, performance gaps, and training requirements before designing curriculum.

## When to Use

- Starting any new learning project
- Performance improvement initiatives
- Identifying skill gaps
- Determining training vs. non-training solutions
- Stakeholder requirement gathering

## Required Inputs

- **Context**: Organization, role, or learner population
- **Business Goals**: What outcomes are desired
- **Current State**: Baseline performance or knowledge
- **Stakeholders**: Who to interview/survey

## Workflow

### 1. Define Analysis Scope

```markdown
# Learning Needs Analysis: [PROJECT]

**Context**: [Organization/department/role]
**Requested By**: [Stakeholder]
**Date**: [Date]
**Analyst**: Learning Needs Analysis System

## Analysis Scope

**Population**: [Who needs training - size, demographics, roles]
**Business Context**: [Why this analysis is needed now]
**Success Metrics**: [How we'll know needs are addressed]
**Timeline**: [When training must be delivered]
**Budget**: [Approximate budget constraints]
```

### 2. Conduct Stakeholder Analysis

**Key Stakeholders**:
- **Learners**: Those who will receive training
- **Managers**: Supervisors of learners
- **Subject Matter Experts (SMEs)**: Content experts
- **Leadership**: Decision makers and budget holders
- **Customers**: End recipients of learner performance

**Interview Questions by Stakeholder**:

**For Learners**:
- What tasks do you struggle with?
- What knowledge/skills would help you perform better?
- What training have you received? What was helpful/not?
- What barriers prevent you from performing well?
- What resources or support do you need?

**For Managers**:
- What performance gaps do you observe?
- What does excellent performance look like?
- What consequences result from poor performance?
- What non-training factors affect performance?
- What results would you like training to achieve?

### 3. Identify Performance Gaps

**Performance Gap Analysis**:

| Task/Skill | Desired Performance | Current Performance | Gap Size | Priority |
|------------|---------------------|---------------------|----------|----------|
| [Task 1] | [Standard] | [Actual] | [Difference] | High/Med/Low |
| [Task 2] | [Standard] | [Actual] | [Difference] | High/Med/Low |

**Gap Classification**:
- **Knowledge Gap**: Don't know what to do
- **Skill Gap**: Know what but can't execute
- **Motivation Gap**: Can do but won't do
- **Environment Gap**: Want to but blocked by system/tools

### 4. Determine Root Causes

For each performance gap, analyze root causes:

**Is it a Training Need?**
✅ Learners lack knowledge or skills
✅ Performers don't know standards/expectations
✅ New process/system requires learning

**Or a Non-Training Need?**
❌ Poor tools or technology
❌ Lack of resources or time
❌ Inadequate incentives/consequences
❌ Unclear job expectations
❌ Poor hiring/selection

**Recommendation**: Training solves knowledge/skill gaps only. Recommend non-training solutions for other gaps.

### 5. Conduct Job/Task Analysis

For skills-based training:

```markdown
## Job Analysis: [ROLE]

**Critical Tasks** (what must be done):
1. [Task 1]: [Frequency] [Importance] [Difficulty]
2. [Task 2]: [Frequency] [Importance] [Difficulty]

**For Each Critical Task**:
- **Steps**: [Procedure breakdown]
- **Knowledge Required**: [What they need to know]
- **Skills Required**: [What they need to do]
- **Tools/Resources**: [What they need]
- **Standards**: [How to measure success]
- **Consequences**: [What happens if done wrong]
```

### 6. Map Competencies

**Competency Framework**:

| Competency | Definition | Proficiency Levels | Current | Target |
|------------|------------|-------------------|---------|--------|
| [Skill 1] | [Description] | Novice/Competent/Expert | [Level] | [Level] |
| [Skill 2] | [Description] | Novice/Competent/Expert | [Level] | [Level] |

### 7. Prioritize Learning Needs

**Prioritization Matrix**:

```
Impact on Performance (High/Low) × Frequency of Use (High/Low)

High Impact + High Frequency = PRIORITY 1 (Must Train)
High Impact + Low Frequency = PRIORITY 2 (Should Train)
Low Impact + High Frequency = PRIORITY 3 (Nice to Train)
Low Impact + Low Frequency = PRIORITY 4 (Don't Train)
```

### 8. Generate Needs Analysis Report

```markdown
# Learning Needs Analysis Report

## Executive Summary

[2-3 paragraphs summarizing key findings and recommendations]

## Findings

### Performance Gaps Identified

1. **Gap**: [Description]
   - **Current State**: [Baseline]
   - **Desired State**: [Target]
   - **Impact**: [Business consequence]
   - **Root Cause**: [Knowledge/Skill/Motivation/Environment]
   - **Recommendation**: [Training or non-training solution]

### Training Needs (Priority 1)

- **Need 1**: [Description] - [Target audience] - [Urgency]
- **Need 2**: [Description] - [Target audience] - [Urgency]

### Non-Training Needs

- **Issue**: [Description] - **Solution**: [Recommended approach]

## Recommendations

### Training Solutions Recommended

1. **Training Program**: [Name/Topic]
   - **Target Audience**: [Who]
   - **Learning Objectives**: [What they'll learn]
   - **Delivery Method**: [How delivered]
   - **Duration**: [Time required]
   - **Expected Impact**: [Performance improvement]

### Non-Training Solutions Recommended

1. **Solution**: [Description]
   - **Type**: [Process/Tool/Policy change]
   - **Owner**: [Who implements]
   - **Timeline**: [When]

## Implementation Plan

**Phase 1**: [Action items with timeline]
**Phase 2**: [Action items with timeline]

## Success Metrics

- **Metric 1**: [How we'll measure success]
- **Metric 2**: [How we'll measure success]

## Next Steps

1. [Action item with owner]
2. [Action item with owner]
```

### 9. CLI Interface

```bash
# Full needs analysis
/learning.needs-analysis --context "sales team" --population "50 reps" --goal "increase conversion rate"

# Quick gap analysis
/learning.needs-analysis --gap-analysis --role "customer service" --current "70% satisfaction" --target "90% satisfaction"

# Competency mapping
/learning.needs-analysis --competency-map --role "software developer" --level "mid-level"

# Help
/learning.needs-analysis --help
```

## Output Format

**Human-Readable**: Full markdown report with tables, analysis, recommendations
**JSON**: Structured data for integration with other systems

## Composition with Other Skills

**Input to**:
- `/curriculum.research` - Informs what to research
- `/curriculum.design` - Drives learning objectives
- `/learning.pathway-designer` - Personalizes based on gaps

## Exit Codes

- **0**: Analysis complete, needs identified
- **1**: Insufficient data to complete analysis
- **2**: Invalid context or scope
- **3**: No performance gaps identified
