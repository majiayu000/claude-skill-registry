---
name: content-evaluation-framework
description: This skill should be used when evaluating the quality of book chapters, lessons, or educational content. It provides a systematic 6-category rubric with weighted scoring (Technical Accuracy 30%, Pedagogical Effectiveness 25%, Writing Quality 20%, Structure & Organization 15%, AI-First Teaching 10%, Constitution Compliance Pass/Fail) and multi-tier assessment (Excellent/Good/Needs Work/Insufficient). Use this during iterative drafting, after content completion, on-demand review requests, or before validation phases.
version: "2.1.0"
constitution_alignment: "v4.0.1"
---

# Content Evaluation Framework

This skill provides a comprehensive, systematic rubric for evaluating educational book chapters and lessons with quantifiable quality standards.

**Constitution Alignment**: v4.0.1 emphasizing:
- **Principle 1**: Specification Primacy ("Specs Are the New Syntax")
- **Section IIa**: Panaversity 4-Layer Teaching Method
- **Section IIb**: AI Three Roles Framework (bidirectional co-learning)
- **8 Foundational Principles**: Including Factual Accuracy, Coherent Structure, Progressive Complexity
- **Nine Pillars** (Section I): AI CLI, Markdown, MCP, AI-First IDEs, Cross-Platform, TDD, SDD, Composable Skills, Cloud-Native

## Purpose

Evaluate educational content across 6 weighted categories to ensure:
- Technical correctness and code quality
- Effective pedagogical design and learning outcomes
- Clear, accessible writing for target audience
- Proper structure and organization
- AI-augmented learning principles (learning WITH AI, not generating FROM AI)
- Constitution compliance and standards adherence

## When to Use This Skill

Invoke this evaluation framework at multiple checkpoints:

1. **During Iterative Drafting** - Mid-process quality checks to catch issues early
2. **After Lesson/Chapter Completion** - Comprehensive evaluation before moving to next content unit
3. **On-Demand Review Requests** - When user explicitly asks for quality assessment
4. **Before Validation Phase** - Part of the SDD Validate phase workflow for final sign-off

## Evaluation Methodology

### Scoring System

**Multi-Tier Assessment:**
- **Excellent (90-100%)** - Exceeds standards, exemplary quality
- **Good (75-89%)** - Meets all standards with minor improvements possible
- **Needs Work (50-74%)** - Meets some standards but requires significant revision
- **Insufficient (<50%)** - Does not meet minimum standards, requires major rework

### Weighted Categories

The evaluation uses 6 categories with the following weights:

| Category | Weight | Focus Area |
|----------|--------|------------|
| **Technical Accuracy** | 30% | Code correctness, type hints, explanations, examples work as stated |
| **Pedagogical Effectiveness** | 25% | Show-then-explain pattern, progressive complexity, quality exercises |
| **Writing Quality** | 20% | Readability (Flesch-Kincaid 8-10), voice, clarity, grade-level appropriateness |
| **Structure & Organization** | 15% | Learning objectives met, logical flow, appropriate length, transitions |
| **AI-First Teaching** | 10% | Co-learning partnership demonstrated, Three Roles Framework shown, Nine Pillars aligned, Specs-As-Syntax emphasized |
| **Constitution Compliance** | Pass/Fail | Must pass all non-negotiable constitutional requirements including Nine Pillars alignment (gate) |

**Total Weighted Score Calculation:**
```
Final Score = (Technical × 0.30) + (Pedagogical × 0.25) + (Writing × 0.20) +
              (Structure × 0.15) + (AI-First × 0.10)
```

**Constitution Compliance:** Must achieve "Pass" status. If "Fail," content cannot proceed regardless of weighted score.

## How to Conduct an Evaluation

### Step 1: Prepare Context

Before evaluation, gather:
- Content being evaluated (lesson.md, chapter.md, or section file)
- Relevant spec, plan, and tasks files from `specs/<feature>/`
- Constitution file (`.specify/memory/constitution.md`)
- Learning objectives and success criteria for the content unit
- Output style template used (`.claude/output-styles/lesson.md` or similar)

### Step 2: Load Detailed Rubric

Read the detailed tier criteria for each category:

```
Read: references/rubric-details.md
```

This file contains specific criteria defining Excellent/Good/Needs Work/Insufficient for each of the 6 categories.

### Step 3: Evaluate Constitution Compliance First

Constitution compliance is a **gate** - if content fails constitutional requirements, it cannot proceed.

Use the constitution checklist:

```
Read: references/constitution-checklist.md
```

Assess all non-negotiable principles and requirements. Mark as **Pass** or **Fail** with specific violations noted.

**If Constitution Compliance = Fail:** Stop evaluation and report violations immediately. Content must be revised before proceeding.

**If Constitution Compliance = Pass:** Continue to weighted category evaluation.

### Step 4: Score Each Weighted Category

For each of the 5 weighted categories (Technical Accuracy, Pedagogical Effectiveness, Writing Quality, Structure & Organization, AI-First Teaching):

1. **Review specific criteria** from `rubric-details.md` for that category
2. **Assess content** against criteria for each tier
3. **Assign tier** (Excellent/Good/Needs Work/Insufficient) with score range
4. **Record specific evidence** - Quote examples, note line numbers, cite specific passages
5. **Provide improvement recommendations** - Concrete, actionable feedback

### Step 5: Calculate Weighted Score

Apply the weighted formula:

```
Final Score = (Technical × 0.30) + (Pedagogical × 0.25) + (Writing × 0.20) +
              (Structure × 0.15) + (AI-First × 0.10)
```

Convert tier scores to numeric values:
- **Excellent:** 95%
- **Good:** 82%
- **Needs Work:** 62%
- **Insufficient:** 40%

*(Or use specific numeric score within tier range if warranted)*

### Step 6: Generate Evaluation Report

Use the structured evaluation template:

```
Read: references/evaluation-template.md
```

Complete all sections:
1. **Executive Summary** - Overall score, tier, pass/fail status
2. **Category Scores** - Table showing each category score, tier, and weight contribution
3. **Detailed Findings** - Evidence-based assessment for each category
4. **Strengths** - What the content does well (specific examples)
5. **Areas for Improvement** - Prioritized list of issues with recommendations
6. **Constitution Compliance Status** - Pass/Fail with specific principle checks
7. **Actionable Next Steps** - Concrete tasks to improve content

### Step 7: Communicate Results

Present evaluation report with:
- **Clear verdict** - Pass/Fail and overall quality tier
- **Evidence-based feedback** - Specific quotes and line numbers
- **Prioritized improvements** - Most critical issues first
- **Encouragement** - Acknowledge strengths and effort

## Evaluation Best Practices

### Be Objective and Evidence-Based
- Quote specific passages from content being evaluated
- Reference line numbers or section headers
- Compare against objective rubric criteria, not subjective preference
- Use concrete metrics where possible (word count, readability scores, etc.)

### Focus on Standards, Not Perfection
- Content rated "Good" (75-89%) is publication-ready with minor polish
- Content rated "Excellent" (90-100%) exceeds standards but is not required
- Focus improvements on moving "Needs Work" → "Good" before "Good" → "Excellent"

### Provide Actionable Feedback
- Don't just say "improve clarity" - specify which sentences are unclear and suggest rewrites
- Don't just say "add examples" - suggest specific example types that would help
- Prioritize recommendations: critical (blocking issues) → important → nice-to-have

### Respect the Learning Journey
- Recognize iterative improvement - drafts evolve through multiple passes
- Celebrate progress and strengths
- Frame criticism constructively as opportunities for growth
- Remember: the goal is helping create excellent educational content, not gatekeeping

## Quality Gates and Thresholds

### Minimum Acceptance Threshold
- **Constitution Compliance:** MUST be Pass (gate)
- **Overall Weighted Score:** MUST be ≥ 75% (Good or better)
- **No category below 50%:** Each individual category must achieve at least "Needs Work" tier

### Recommended for Publication
- **Constitution Compliance:** Pass
- **Overall Weighted Score:** ≥ 82% (Good tier)
- **Technical Accuracy:** ≥ 75% (Good tier) - Critical for credibility
- **Pedagogical Effectiveness:** ≥ 75% (Good tier) - Critical for learning outcomes

### Exemplary Content (Optional)
- **Overall Weighted Score:** ≥ 90% (Excellent tier)
- **At least 3 categories at Excellent tier**
- **No categories below Good tier**

## Common Evaluation Scenarios

### Scenario 1: Mid-Draft Check (Iterative)
**Context:** Writer requests feedback on partial draft
**Approach:**
- Focus on foundational issues (structure, learning objectives, concept scaffolding)
- Flag critical issues early (technical errors, constitution violations)
- Provide guidance for remaining sections
- Don't expect polish - prioritize content completeness and correctness

### Scenario 2: Completion Review
**Context:** Writer believes content is complete and ready for validation
**Approach:**
- Conduct full evaluation across all 6 categories
- Calculate final weighted score
- Check all quality gates and thresholds
- Provide comprehensive report with prioritized improvements
- Determine if content meets publication standards

### Scenario 3: Pre-Validation Quality Gate
**Context:** Content enters SDD Validate phase
**Approach:**
- Verify constitution compliance (gate)
- Confirm minimum acceptance threshold (≥75%)
- Validate all category scores meet minimums
- Generate pass/fail recommendation with evidence
- If fails gate: return to implementation with specific revision tasks

### Scenario 4: On-Demand Spot Check
**Context:** User asks "How's this looking?" for specific section
**Approach:**
- Evaluate relevant categories for that section (may not be all 6)
- Provide quick feedback on specific concerns
- Highlight any critical issues
- Suggest improvements without full formal report
- Use judgment on depth based on context

## Resources and References

This skill includes detailed reference materials:

- **`references/rubric-details.md`** - Comprehensive tier criteria for all 6 categories with specific indicators
- **`references/constitution-checklist.md`** - Pass/Fail checklist for constitutional compliance evaluation
- **`references/evaluation-template.md`** - Structured template for consistent evaluation reports

Load these references as needed during evaluation to ensure consistency and thoroughness.

---

## Example Evaluation Flow

**User Request:** "Please evaluate this lesson draft: `apps/learn-app/docs/chapter-3/lesson-2.md`"

**Evaluation Process:**

1. **Read content:** `apps/learn-app/docs/chapter-3/lesson-2.md`
2. **Load context:** spec, plan, constitution, learning objectives
3. **Check constitution compliance:** `references/constitution-checklist.md`
   - Result: **Pass** (all non-negotiables met)
4. **Load detailed rubric:** `references/rubric-details.md`
5. **Evaluate each category:**
   - Technical Accuracy: Good (80%) - Code works, minor type hint gaps
   - Pedagogical Effectiveness: Excellent (92%) - Strong scaffolding, great exercises
   - Writing Quality: Good (78%) - Clear writing, minor readability improvements
   - Structure & Organization: Good (85%) - Good flow, all LOs met
   - AI-First Teaching: Needs Work (65%) - AI exercises present but weak guidance
6. **Calculate weighted score:**
   - (80×0.30) + (92×0.25) + (78×0.20) + (85×0.15) + (65×0.10) = 81.55%
   - **Final Tier: Good (81.55%)**
7. **Load template:** `references/evaluation-template.md`
8. **Generate report** with findings, strengths, improvements, next steps
9. **Communicate verdict:** "Good (81.55%) - Ready for publication with minor improvements to AI-First Teaching section"

---

**Use this skill to maintain consistent, objective, evidence-based quality standards for all educational content.**
