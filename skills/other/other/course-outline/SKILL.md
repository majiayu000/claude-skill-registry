---
name: course-outline
description: Create a full course structure from a topic and transformation goal. Output includes course name, tagline, target student, prerequisites, module-by-module breakdown (3-7 modules), lessons per module (3-5 each), learning objectives per lesson, and estimated completion time. Use when user wants to "outline a course", "structure a course", "plan a curriculum", or "build a course".
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Course Outline Builder

**Purpose:** Create a complete course structure that takes students from Point A (where they are) to Point B (the transformation). Every module and lesson is purposeful — no filler.

## Required Input

- **Topic** — What the course teaches
- **Transformation** — Where students start → where they end up
- **Target student** (or pull from ICP.md)
- **Depth level** — Beginner, intermediate, advanced, or all levels?

## Course Design Principles

1. **Transformation-first** — Start with the end result, work backwards
2. **Progressive complexity** — Each module builds on the last
3. **Action-oriented** — Every lesson ends with something the student DOES
4. **No filler** — If a lesson doesn't directly serve the transformation, cut it
5. **Quick wins early** — Module 1 should produce a visible result

## Output Format

```markdown
# Course Outline: [Course Name]

**Tagline:** [One sentence capturing the transformation]
**Target student:** [Who this is for — specific description]
**Prerequisites:** [What they need before starting — or "None"]
**Estimated completion time:** [X hours total]
**Modules:** [X] | **Lessons:** [X total]

---

## Course Overview

**The transformation:**
- **Start:** [Where the student is now — their current frustration]
- **End:** [Where they'll be after completing the course — specific outcome]

**What makes this course different:**
[2-3 sentences on the unique angle or methodology]

---

## Module 1: [Name] — [Quick Win Theme]
*Estimated time: [X] hours*

**Module goal:** [What the student can DO after this module]

| # | Lesson | Learning Objective | Time |
|---|--------|--------------------|------|
| 1.1 | [Lesson title] | Student will be able to [specific skill] | [X min] |
| 1.2 | [Lesson title] | Student will be able to [specific skill] | [X min] |
| 1.3 | [Lesson title] | Student will be able to [specific skill] | [X min] |

**Module deliverable:** [What they create or complete by end of this module]

---

## Module 2: [Name] — [Foundation Theme]
*Estimated time: [X] hours*

**Module goal:** [Outcome]

| # | Lesson | Learning Objective | Time |
|---|--------|--------------------|------|
| 2.1 | [Lesson] | [Objective] | [Time] |
| 2.2 | [Lesson] | [Objective] | [Time] |
| 2.3 | [Lesson] | [Objective] | [Time] |
| 2.4 | [Lesson] | [Objective] | [Time] |

**Module deliverable:** [Output]

---

[Continue for all modules — 3-7 total]

---

## Module [X]: [Name] — [Capstone/Advanced Theme]
*Estimated time: [X] hours*

**Module goal:** [Final transformation outcome]

[Lessons...]

**Module deliverable:** [Final project or output]

---

## Course Summary

| Module | Theme | Lessons | Time | Key Deliverable |
|--------|-------|---------|------|----------------|
| 1 | [Quick Win] | [X] | [X]h | [What they make] |
| 2 | [Foundation] | [X] | [X]h | [What they make] |
| 3 | [Core Skill] | [X] | [X]h | [What they make] |
[Continue...]

**Total:** [X] modules | [X] lessons | [X] hours

---

## Recommended Add-Ons

- **Community/support group** — [Yes/No and why]
- **Live Q&A sessions** — [Recommended frequency]
- **Templates/resources** — [What to include]
- **Certificate of completion** — [Yes/No]
```

## Quality Checklist

- [ ] Course name is compelling (not generic)
- [ ] Transformation is clear (Point A → Point B)
- [ ] 3-7 modules with logical progression
- [ ] 3-5 lessons per module
- [ ] Every lesson has a specific, measurable learning objective
- [ ] Module 1 delivers a quick win
- [ ] Each module has a tangible deliverable
- [ ] Time estimates are realistic
- [ ] No filler lessons (every lesson serves the transformation)
- [ ] Based on user's expertise (not fabricated content)
