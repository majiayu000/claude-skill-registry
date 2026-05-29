---
name: interview-scorecard-builder
description: Эксперт по interview scorecards. Используй для структурированных интервью и оценки кандидатов.
---

# Interview Scorecard Builder

Expert in creating structured interview scorecards for consistent, fair candidate evaluation.

## Core Design Principles

### Competency-Based Structure
- Define 4-6 core competencies aligned with role requirements
- Include both technical and behavioral competencies
- Map competencies to specific job responsibilities
- Weight competencies based on role criticality

### STAR Method Integration
- Structure questions to elicit Situation, Task, Action, Result responses
- Provide behavioral indicators for each competency level
- Include follow-up probes to gather complete examples

### Scoring Consistency
- Use 1-5 point scales with clear descriptors
- Define specific observable behaviors for each score level
- Include "not assessed" options for untested areas
- Provide overall rating calculation methodology

## Scorecard Template Structure

```markdown
# Interview Scorecard: [Role Title]

**Candidate:** ________________
**Date:** ________________
**Interviewer:** ________________
**Interview Type:** [Phone Screen / Technical / Behavioral / Final]

---

## Competency 1: [Competency Name] (Weight: X%)

**Definition:** [Clear, concise description of what this competency means]

### Interview Questions:

**Primary Question:**
"Tell me about a time when [situation related to competency]..."

**Follow-up Probes:**
- "What was your specific role?"
- "What was the outcome?"
- "What would you do differently?"

### Scoring Rubric:

| Score | Level | Behavioral Indicators |
|-------|-------|----------------------|
| 5 | Exceptional | Demonstrates mastery; leads others; innovates |
| 4 | Strong | Consistently exceeds expectations; minimal guidance needed |
| 3 | Competent | Meets expectations; occasionally needs guidance |
| 2 | Developing | Below expectations; requires significant support |
| 1 | Inadequate | Does not meet minimum requirements |

**Score:** ___/5

**Evidence/Notes:**
_____________________________________________
_____________________________________________

---
```

## Technical Competency Assessment

```markdown
## Technical Competency: [Specific Technology/Skill]

### Assessment Method:
- [ ] Live coding exercise
- [ ] System design discussion
- [ ] Technical Q&A
- [ ] Portfolio/code review
- [ ] Take-home assignment review

### Evaluation Criteria:

| Criterion | Weight | Score (1-5) | Notes |
|-----------|--------|-------------|-------|
| Problem-solving approach | 25% | ___ | |
| Code quality & best practices | 25% | ___ | |
| Technical knowledge depth | 20% | ___ | |
| Communication of technical concepts | 15% | ___ | |
| Learning ability & curiosity | 15% | ___ | |

### Proficiency Levels:

**5 - Expert:**
- Can architect complex solutions independently
- Mentors others effectively
- Drives technical decisions at team/org level
- Deep understanding of trade-offs

**4 - Advanced:**
- Strong independent contributor
- Handles complex problems with minimal guidance
- Understands system-level implications
- Writes production-quality code

**3 - Intermediate:**
- Can work independently on routine tasks
- Needs guidance for complex problems
- Good foundational knowledge
- Produces acceptable quality work

**2 - Beginner:**
- Basic understanding of concepts
- Requires significant support
- Learning trajectory matters
- Some gaps in fundamentals

**1 - None:**
- No demonstrable knowledge
- Cannot perform basic tasks
- Significant training required

**Technical Score:** ___/5

**Specific Strengths:**
_____________________________________________

**Areas for Development:**
_____________________________________________
```

## Behavioral Competency Examples

### Problem Solving

```yaml
competency: Problem Solving
weight: 20%
definition: "Ability to analyze complex situations, identify root causes, and develop effective solutions"

questions:
  primary: "Tell me about a complex problem you solved that others had struggled with. How did you approach it?"

  follow_ups:
    - "What data or information did you gather?"
    - "What alternatives did you consider?"
    - "What was the outcome? How did you measure success?"
    - "What would you do differently?"

behavioral_indicators:
  exceptional_5:
    - "Systematically breaks down complex problems"
    - "Considers multiple perspectives and trade-offs"
    - "Proactively identifies potential issues"
    - "Solutions have lasting positive impact"

  strong_4:
    - "Logical, structured problem-solving approach"
    - "Considers consequences of solutions"
    - "Asks clarifying questions"
    - "Delivers effective solutions"

  competent_3:
    - "Can solve standard problems independently"
    - "May miss some edge cases"
    - "Adequate analytical skills"
    - "Needs some guidance for complex issues"

  developing_2:
    - "Struggles with ambiguous problems"
    - "Limited analytical framework"
    - "Often needs help identifying solutions"
    - "Solutions may be incomplete"

  inadequate_1:
    - "Cannot articulate problem-solving approach"
    - "Relies heavily on others"
    - "Poor judgment in solutions"
    - "No examples to share"
```

### Leadership

```yaml
competency: Leadership
weight: 25%
definition: "Ability to inspire, guide, and develop team members while driving results"

questions:
  primary: "Describe a situation where you had to lead a team through a challenging project or change."

  follow_ups:
    - "How did you get buy-in from the team?"
    - "How did you handle resistance or conflict?"
    - "How did you develop team members along the way?"
    - "What was the outcome for the team and the project?"

behavioral_indicators:
  exceptional_5:
    - "Inspires and motivates others consistently"
    - "Develops team members proactively"
    - "Navigates complex stakeholder dynamics"
    - "Builds high-performing teams"
    - "Leads through influence, not authority"

  strong_4:
    - "Clear vision and direction setting"
    - "Effective delegation and follow-through"
    - "Handles conflict constructively"
    - "Team members grow under their leadership"

  competent_3:
    - "Can lead small teams effectively"
    - "Basic delegation skills"
    - "Manages performance adequately"
    - "Some development of others"

  developing_2:
    - "Limited leadership experience"
    - "Struggles with delegation"
    - "Avoids difficult conversations"
    - "More individual contributor mindset"

  inadequate_1:
    - "No leadership examples"
    - "Cannot articulate leadership philosophy"
    - "Poor people skills"
    - "Not ready for leadership role"
```

## Role-Specific Scorecards

### Software Engineer

```yaml
role: Software Engineer
level: Senior

competencies:
  technical_expertise:
    weight: 30%
    areas:
      - "Programming proficiency"
      - "System design"
      - "Code quality and testing"
      - "Technical decision-making"

  problem_solving:
    weight: 25%
    areas:
      - "Analytical thinking"
      - "Debugging skills"
      - "Performance optimization"
      - "Root cause analysis"

  collaboration:
    weight: 20%
    areas:
      - "Code review effectiveness"
      - "Cross-team communication"
      - "Knowledge sharing"
      - "Mentoring"

  ownership:
    weight: 15%
    areas:
      - "End-to-end delivery"
      - "Quality focus"
      - "Initiative"
      - "Accountability"

  learning_agility:
    weight: 10%
    areas:
      - "Adaptability"
      - "Technology curiosity"
      - "Feedback receptiveness"
      - "Continuous improvement"

decision_thresholds:
  strong_hire: 4.0
  hire: 3.5
  borderline: 3.0
  no_hire: 2.5
```

### Product Manager

```yaml
role: Product Manager
level: Senior

competencies:
  product_strategy:
    weight: 25%
    areas:
      - "Vision and roadmap development"
      - "Market and competitive analysis"
      - "Prioritization frameworks"
      - "Business case development"

  execution:
    weight: 25%
    areas:
      - "Cross-functional leadership"
      - "Agile/Scrum proficiency"
      - "Delivery track record"
      - "Risk management"

  customer_focus:
    weight: 20%
    areas:
      - "User research methods"
      - "Data-driven decisions"
      - "Customer empathy"
      - "Problem validation"

  stakeholder_management:
    weight: 15%
    areas:
      - "Executive communication"
      - "Influence without authority"
      - "Conflict resolution"
      - "Alignment building"

  technical_acumen:
    weight: 15%
    areas:
      - "Technical concept understanding"
      - "Engineering collaboration"
      - "Trade-off evaluation"
      - "Technical debt awareness"
```

## Bias Mitigation Framework

```yaml
structured_process:
  - "Use identical questions across all candidates"
  - "Score immediately after each competency discussion"
  - "Document specific examples and evidence"
  - "Separate note-taking from scoring"
  - "Complete individual scorecards before debriefs"

inclusive_assessment:
  - "Focus only on job-relevant competencies"
  - "Avoid 'culture fit' as a criterion"
  - "Consider diverse backgrounds and communication styles"
  - "Evaluate potential, not just past opportunity"
  - "Use panel interviews when possible"

avoiding_common_biases:
  halo_effect:
    description: "Letting one strong area influence all ratings"
    mitigation: "Score each competency independently"

  confirmation_bias:
    description: "Looking for evidence to support initial impression"
    mitigation: "Document both strengths and concerns"

  similarity_bias:
    description: "Favoring candidates similar to yourself"
    mitigation: "Focus on job-related evidence only"

  recency_bias:
    description: "Weighting recent information too heavily"
    mitigation: "Take notes throughout interview"
```

## Scoring and Decision Framework

```yaml
weighted_score_calculation:
  formula: "Overall Score = Σ(Competency Score × Weight)"

  example:
    technical_expertise: "4 × 0.30 = 1.20"
    problem_solving: "4 × 0.25 = 1.00"
    collaboration: "3 × 0.20 = 0.60"
    ownership: "4 × 0.15 = 0.60"
    learning_agility: "5 × 0.10 = 0.50"
    total: "3.90"

decision_thresholds:
  strong_hire:
    score: "4.0+"
    criteria: "Exceptional across most competencies, no concerns"
    action: "Fast-track offer process"

  hire:
    score: "3.5-3.9"
    criteria: "Strong candidate, meets role requirements"
    action: "Proceed with offer"

  borderline:
    score: "3.0-3.4"
    criteria: "Mixed signals, additional evaluation needed"
    action: "Additional interview or references"

  no_hire:
    score: "2.5-2.9"
    criteria: "Does not meet requirements"
    action: "Decline, provide feedback"

  strong_no_hire:
    score: "<2.5"
    criteria: "Clear misalignment"
    action: "Decline"
```

## Final Assessment Section

```markdown
## Overall Assessment

**Total Weighted Score:** ___/5.0

**Recommendation:**
- [ ] Strong Hire (4.0+)
- [ ] Hire (3.5-3.9)
- [ ] Additional Interview Needed (3.0-3.4)
- [ ] No Hire (2.5-2.9)
- [ ] Strong No Hire (<2.5)

**Top 3 Strengths:**
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

**Development Areas/Concerns:**
1. _______________________________________________
2. _______________________________________________

**Additional Comments:**
_______________________________________________

**Recommended Next Steps:**
- [ ] Proceed to next interview round
- [ ] Schedule follow-up interview for [area]
- [ ] Check references with focus on [area]
- [ ] Extend offer
- [ ] Decline with feedback

**Interviewer Signature:** ________________
**Date:** ________________
```

## Лучшие практики

1. **Consistency** — одинаковые вопросы для всех кандидатов
2. **Evidence-based** — оценивайте по конкретным примерам
3. **Independent scoring** — оценивайте до группового обсуждения
4. **Document everything** — детальные заметки для каждой оценки
5. **Calibration** — регулярная калибровка между интервьюерами
6. **Legal compliance** — только job-related критерии
