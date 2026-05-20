---
name: vibe-requirements-validator
description: Validates PRD, user stories, or feature requirements against SMART criteria. Use when reviewing requirements to catch vagueness before it causes expensive rework.
user-invocable: true
---

# vibe-requirements-validator

Vague requirements cause expensive rework. Catch them early.

## When to Use This Skill

- Reviewing a PRD or feature spec before implementation
- Writing acceptance criteria for user stories
- When you notice requirements like "make it fast" or "improve UX"
- Before estimating effort for a feature

## When NOT to Use This Skill

- Internal technical tasks with clear scope
- Bug fixes (the bug IS the requirement)
- When requirements are already validated and approved

## SMART Criteria

Score each requirement 1-5 on:

- **S**pecific — Is it clear what exactly needs to be built? (Not "improve performance" but "reduce P95 latency to <200ms")
- **M**easurable — Can you objectively verify it's done? (Not "users like it" but "NPS score >40")
- **A**chievable — Can it be built with available resources and constraints?
- **R**elevant — Does it align with project goals and user needs?
- **T**ime-bound — Is there a clear scope boundary? (Not "eventually" but "in v1.0")

## Steps

1. **List all requirements** from the document
2. **Score each** on SMART (1-5 per dimension)
3. **Flag issues**:
   - Score < 3 on any dimension → needs revision
   - Measurability < 3 → most common failure, flag prominently
   - Near-duplicates → consolidate
   - Positioning statements masquerading as requirements → remove

4. **Report**:

## Output Format

### Requirements Validation: [Document Name]

**Total Requirements**: X
**Passing (avg >= 3.5)**: Y (Z%)
**Flagged**: W

| ID | Requirement | S | M | A | R | T | Avg | Issue |
|----|------------|---|---|---|---|---|-----|-------|
| FR-1 | "..." | 4 | 2 | 5 | 4 | 3 | 3.6 | Low measurability |

### Top Issues
1. **Measurability crisis** — X requirements have M < 3
2. **Near-duplicates** — [list pairs]
3. **Not requirements** — [positioning statements]

### Recommended Revisions
| ID | Current | Suggested |
|----|---------|-----------|
| FR-3 | "Improve load time" | "Reduce initial page load to <2s on 3G" |
