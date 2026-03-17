---
name: curriculum-grade-assist
description: Assist with grading by applying rubrics to student work, generating criterion-level feedback, and maintaining consistency across submissions. Use when grading assignments, applying rubrics, or providing feedback. Activates on "grade this", "apply rubric", "provide feedback", or "score student work".
---

# Grading Assistance & Rubric Application

Efficiently apply rubrics to student work with consistent, constructive, criterion-level feedback and scoring.

## When to Use

- Grade student submissions
- Apply rubrics consistently
- Generate feedback
- Score assessments
- Analyze student work quality

## Required Inputs

- **Student Work**: Submission to grade
- **Rubric**: Scoring criteria
- **Answer Key**: For objective items
- **Context**: Assignment expectations

## Workflow

### 1. Load Rubric and Student Work

Read:
- Rubric criteria and performance levels
- Student submission
- Assignment prompt/expectations
- Learning objectives assessed

### 2. Analyze Work Against Each Criterion

For each rubric criterion:

**Identify Evidence**:
- Find relevant content in submission
- Note what student did well
- Note what's missing or weak

**Determine Performance Level**:
- Compare to rubric descriptors
- Select appropriate level (Exemplary, Proficient, Developing, Beginning)
- Justify selection with specific evidence

**Generate Feedback**:
- Cite specific strengths
- Identify specific gaps
- Suggest concrete improvements

### 3. Generate Grading Report

```markdown
# Grading Report: [ASSIGNMENT]

**Student**: [ID or Anonymous]
**Submission Date**: [Date]
**Graded**: [Date]

## Overall Score

**Total Points**: [X] / [Y] ([Z]%)
**Performance Level**: [Exemplary | Proficient | Developing | Beginning]

## Criterion-Level Scores

### Criterion 1: [Name] (Score: [X]/[Y] - [Level])

**Performance Level**: [Exemplary/Proficient/Developing/Beginning]

**Strengths**:
- [Specific thing student did well with quote/reference]
- [Another strength with evidence]

**Areas for Growth**:
- [Specific gap with reference to submission]
- [What's missing or needs improvement]

**Feedback**:
"[Your analysis shows strong understanding of X, particularly when you explained Y. To strengthen this further, consider Z. For example, you could have..."

**Score Justification**:
This scores at [Level] because [specific reasons citing rubric descriptors].

### Criterion 2: [Name] (Score: [X]/[Y] - [Level])

[Same structure for each criterion]

## Overall Comments

**Summary of Performance**:
[2-3 sentences summarizing overall quality, patterns of strength, areas needing attention]

**Specific Recommendations**:
1. [Actionable step 1]
2. [Actionable step 2]
3. [Actionable step 3]

**Encouragement**:
[Positive, growth-oriented closing that motivates continued learning]

## Learning Objectives Assessment

| Objective | Mastery Level | Evidence |
|-----------|---------------|----------|
| LO-1.1 | ✅ Mastered | [Citation from work] |
| LO-1.2 | ⚠️  Developing | [Citation showing partial understanding] |
| LO-1.3 | ❌ Not Yet | [Missing or incorrect] |

## Next Steps for Student

- Review [concept] using [resource]
- Practice [skill] by [activity]
- Seek help with [specific difficulty]
- Prepare for next assignment: [preview]

---

**Grading Metadata**:
- **Grader**: Curriculum Grading Assistant
- **Rubric**: [Link to rubric used]
- **Time**: [Auto-calculated time on task from submission]
```

### 4. Batch Grading Features

For multiple submissions:

**Consistency Checks**:
- Compare scores across students
- Flag outliers for review
- Ensure rubric applied uniformly

**Common Error Identification**:
- Track recurring mistakes
- Identify patterns
- Generate group feedback opportunity

**Efficiency Tools**:
- Templates for common feedback
- Quick codes for frequent comments
- Progress tracking

### 5. Auto-Grading (Objective Items)

For MC, T/F, fill-in-blank with answer keys:

```markdown
**Auto-Graded Section**

| Item | Student Answer | Correct Answer | Points |
|------|----------------|----------------|--------|
| MC-1 | B | B | 1/1 ✅ |
| MC-2 | A | C | 0/1 ❌ |
| MC-3 | D | D | 1/1 ✅ |

**Section Score**: 2/3 (67%)

**Item Feedback**:
- Item MC-2: Incorrect. The correct answer is C because [explanation]. Review [concept].
```

### 6. Feedback Quality Standards

Ensure feedback is:
✅ **Specific**: Cites actual work, not generic
✅ **Actionable**: Clear steps to improve
✅ **Balanced**: Strengths and growth areas
✅ **Growth-Oriented**: Encourages learning
✅ **Aligned**: References rubric and objectives
✅ **Timely**: Generated quickly for fast return

### 7. CLI Interface

```bash
# Grade single submission
/curriculum.grade-assist --submission "student1-essay.pdf" --rubric "essay-rubric.md" --objective "LO-2.1"

# Batch grade
/curriculum.grade-assist --submissions "submissions/*.pdf" --rubric "rubric.md" --batch

# Auto-grade objective items
/curriculum.grade-assist --quiz "quiz-responses.csv" --answer-key "answers.json" --auto

# Consistency check
/curriculum.grade-assist --review-consistency --graded "graded/*.md"

# Help
/curriculum.grade-assist --help
```

## Educational Level Adaptations

**K-5**:
- Simple, encouraging feedback
- Focus on effort and progress
- Visual feedback (stickers, stamps)
- Parent-friendly language

**6-8**:
- Balance praise and critique
- Specific skill development focus
- Encourage self-assessment
- Age-appropriate tone

**9-12**:
- Detailed, analytical feedback
- College-prep quality expectations
- Emphasize critical thinking
- Professional tone

**Higher Ed**:
- Scholarly feedback
- Discipline-specific criteria
- Research and argument quality
- Professional development focus

## Composition with Other Skills

**Input from**:
- `/curriculum.assess-design` - Rubrics
- `/curriculum.develop-items` - Answer keys
- `/curriculum.design` - Learning objectives

**Output to**:
- `/curriculum.analyze-outcomes` - Grading data for analytics
- Students for learning
- Gradebook systems

## Exit Codes

- **0**: Grading completed successfully
- **1**: Cannot load rubric
- **2**: Cannot access student work
- **3**: Invalid grading configuration
- **4**: Rubric-work mismatch
