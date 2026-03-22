---
name: assess-slts
description: Evaluate SLT quality across 5 dimensions with rewrite suggestions.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Assess Student Learning Targets


## Description
Evaluates the quality of a list of Student Learning Targets (SLTs) against established education research and Andamio protocol conventions. Provides per-SLT assessment and actionable suggestions for improvement.

## Instructions

### Path Resolution

Resolve file paths based on your execution context:

- **Plugin context** (`${CLAUDE_PLUGIN_ROOT}` is set): Read knowledge from `${CLAUDE_PLUGIN_DATA}/knowledge/` (user data), falling back to `${CLAUDE_PLUGIN_ROOT}/knowledge/` (seed data). Read research from `${CLAUDE_PLUGIN_ROOT}/knowledge/research/`.
- **Clone/symlink context** (default): Read knowledge from `knowledge/` relative to the project root (research is at `knowledge/research/`).

### Pre-Execution Knowledge Check

Before assessing SLTs, read the knowledge base for patterns that should influence your assessment. **If any knowledge file does not exist, skip it and proceed without prior patterns — note "No prior data available" in output.**

1. **Read `knowledge/slt-patterns/quality-issues.yaml`**
   - Flag SLTs matching known problematic patterns
   - Include "seen in [n] courses" when citing issues

2. **Read `knowledge/slt-patterns/successful-rewrites.yaml`**
   - When suggesting fixes, prefer proven rewrites
   - Include "this rewrite worked in [course]" when applicable

3. **Surface knowledge in assessment** (if relevant patterns exist):
   ```markdown
   **Known Issue:** This pattern (task-focused verb) was flagged in 3 previous courses.
   **Proven Rewrite:** "I can complete the setup" → "I can configure my environment to run X" (from andamio-for-contributors)
   ```

---

The user will provide a markdown file containing a list of SLTs. Read the file, then assess each SLT against the criteria below. Always read `knowledge/research/slt-research-report.md` for full research context before running the assessment.

### Assessment Criteria

Evaluate each SLT on the following dimensions, rating each as **Strong**, **Acceptable**, or **Needs Work**:

#### 1. Student-Facing Language & Approachability
- Is it written from the learner's perspective?
- Does it use "I can..." or "Learner can..." format?
- Is the language accessible and free of unnecessary jargon?
- Would a motivated beginner read this SLT and feel invited into the topic rather than intimidated by it?
- Tool names, library names, and framework names are fine — they orient the learner. But implementation details (specific functions, flags, protocol specifics) belong in the lesson, not the SLT.
- **Strong**: Clear "I can..." statement that any learner could read and immediately understand what they'll be able to do. Names the relevant tools/concepts without burying the reader in technical detail.
- **Acceptable**: Learner-facing but leans on jargon or implementation specifics that narrow the audience unnecessarily.
- **Needs Work**: Written as a teacher objective, uses third person, or reads like a spec rather than a learning invitation.

#### 2. Focus on Learning, Not Tasks
- Does it describe what the learner will *learn* or *be able to do*, rather than what activity they will perform?
- **Strong**: Clearly states a capability or understanding the learner will gain.
- **Acceptable**: Implies learning but is phrased partly as an activity.
- **Needs Work**: Describes a task or activity rather than a learning outcome (e.g., "I can complete the worksheet" or "I can read chapter 5").

#### 3. Specificity and Measurability
- Is the SLT narrow enough that mastery can be assessed?
- Could a teacher (or peer) determine whether this target has been met based on evidence?
- **Strong**: Clear, observable, and assessable. You could design an assignment around it.
- **Acceptable**: Mostly assessable but somewhat broad or ambiguous.
- **Needs Work**: Too vague to assess (e.g., "I can understand blockchain") or too broad to fit a single module.

#### 4. Cognitive Level (Bloom's Taxonomy)
- Identify the Bloom's level implied by the verb: Remember, Understand, Apply, Analyze, Evaluate, or Create.
- Is the cognitive level appropriate for the apparent subject matter and context?
- Flag SLTs that cluster entirely at low levels (Remember/Understand) when higher-order thinking would be expected.
- Flag SLTs that use vague verbs like "understand" or "know" — these are difficult to measure. Suggest more precise alternatives.

#### 5. Standalone Clarity
- Can the SLT be understood without needing to read surrounding course material?
- Does it make sense as an independent unit of learning?
- **Strong**: Self-contained and clear.
- **Acceptable**: Understandable but references implicit context.
- **Needs Work**: Requires significant external context to interpret.

### Output Format

Respond with a markdown document structured as follows:

```markdown
# SLT Quality Assessment

## Summary

- **Total SLTs reviewed**: [number]
- **Overall quality**: [brief 1-2 sentence summary]
- **Distribution**: [count] Strong / [count] Acceptable / [count] Needs Work

## Per-SLT Assessment

### SLT 1: "[full text of SLT]"

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Student-Facing Language | [rating] | [brief note] |
| Focus on Learning | [rating] | [brief note] |
| Specificity & Measurability | [rating] | [brief note] |
| Cognitive Level | [Bloom's level] | [brief note] |
| Standalone Clarity | [rating] | [brief note] |

**Overall**: [Strong / Acceptable / Needs Work]

**Suggestion**: [If not Strong, provide a concrete rewrite or improvement. If Strong, say "No changes needed."]

---

[Repeat for each SLT]

## Set-Level Observations

[After all individual assessments, note any patterns across the full set:]
- Bloom's level distribution — are targets clustered at one level?
- Gaps — are there obvious areas of learning not covered?
- Redundancy — do any SLTs overlap significantly?
- Prerequisite logic — does the ordering suggest a reasonable learning progression?
```

### Guidelines

- Be direct and specific. Vague feedback like "could be better" is not useful.
- When suggesting a rewrite, provide the full rewritten SLT text.
- Preserve the learner's domain and intent — don't change what they're learning, improve how it's expressed.
- If an SLT is Strong on all dimensions, say so briefly and move on. Spend more space on SLTs that need work.
- The overall rating for an SLT is determined by its weakest dimension: one "Needs Work" rating makes the overall "Needs Work."

#### Tone & Technicality
- SLTs should be **approachable gateways**, not technical specifications. They should make a learner curious about what's ahead, not anxious about what they don't yet know.
- Name tools and frameworks (e.g., "Cobra", "Fiber", "Go") — these give learners real-world orientation. But leave implementation details (specific functions, flags, API patterns, protocol internals) to the lesson content.
- A good test: if someone who has never touched the subject reads the SLT, they should understand the *shape* of what they'll learn, even if they can't do it yet.
- When rewriting an overly technical SLT, aim for language that is **specific enough to assess** but **plain enough to invite**. Err on the side of approachability — the lesson itself is where depth lives.
