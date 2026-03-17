---
name: learning-diagnostic-assessment
description: Design pre-assessments, placement tests, and diagnostic instruments to identify learner starting points, knowledge gaps, and optimal entry points for personalized pathways. Use when determining where learners should start. Activates on "placement test", "diagnostic assessment", "pre-test", or "skill assessment".
---

# Learning Diagnostic Assessment

Create assessments that diagnose learner readiness, identify gaps, and recommend personalized starting points.

## When to Use
- Course placement
- Prerequisite validation
- Personalized pathway routing
- Prior learning assessment
- Skill gap identification

## Assessment Types

### 1. Placement Tests
- Determine appropriate course level
- Route to beginner/intermediate/advanced
- Validate prerequisites

### 2. Knowledge Gap Analysis
- Identify specific missing concepts
- Map to remediation content
- Prioritize interventions

### 3. Prior Learning Assessment
- Credit for prior experience
- Portfolio-based assessment
- Challenge exams

### 4. Readiness Checks
- Prerequisites met?
- Motivational readiness?
- Technology access?

## Design Principles

**Efficient Coverage**:
- Sample across objectives
- Quick administration (10-20 min)
- Computer-adaptive if possible

**Actionable Results**:
- Clear starting point recommendation
- Specific gap identification
- Next-step guidance

**Low-Stakes**:
- No grades, just guidance
- Multiple attempts allowed
- Formative purpose

## CLI Interface
```bash
/learning.diagnostic-assessment --objectives "course-objectives.json" --format "adaptive"
/learning.diagnostic-assessment --placement --levels "beginner,intermediate,advanced"
/learning.diagnostic-assessment --gap-analysis --domain "mathematics" --level "algebra"
```

## Output
- Diagnostic test items
- Scoring rubric/algorithm
- Routing logic
- Learner feedback templates
- Remediation recommendations

## Composition
**Input from**: `/curriculum.design`, `/learning.pathway-designer`
**Output to**: Learner placement, personalization system

## Exit Codes
- **0**: Diagnostic created
- **1**: Insufficient objective coverage
- **2**: Invalid routing logic
