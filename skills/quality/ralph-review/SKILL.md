---
name: ralph-review
description: Interactive review of auto-generated Ralph artifacts. Use when user asks to "ralph review stories", "ralph review tasks", "ralph review roadmap", or needs to validate planning artifacts against their intent.
---

# Ralph Review

Interactive review of planning artifacts with fresh eyes.

## Execution

Check the ARGUMENTS:

### `gap roadmap`

Launch a **subagent** with fresh context to analyze the roadmap for gaps.

Follow @context/workflows/ralph/planning/roadmap-gap-analysis.md completely.

### `gap stories <milestone>`

Launch a **subagent** with fresh context to analyze stories for gaps.

If no milestone provided, ask user: "Which milestone should I analyze? (e.g., milestone-1)"

Follow @context/workflows/ralph/planning/story-gap-analysis.md completely.

### `stories <milestone>`

Follow @context/workflows/ralph/review/stories-review.md completely.

### `roadmap`

Launch a **subagent** with fresh context to review the roadmap for quality and completeness.

**Presentation:** @context/workflows/ralph/review/chunked-presentation.md

Read and analyze:
- @docs/planning/VISION.md
- @docs/planning/ROADMAP.md

Walk through **milestone by milestone**:
1. "I'll review each milestone one at a time. Starting with the first..."
2. Present one milestone's review (quality, sequencing, scope)
3. Wait for [next / discuss / edit]
4. Continue until all milestones reviewed
5. Then: cross-milestone analysis (vision alignment, dependencies)

Review dimensions per milestone:
- **Milestone Quality**: Clear deliverables? Measurable success criteria?
- **Sequencing**: Does order make sense? Dependencies respected?
- **Vision Alignment**: Does this milestone contribute to the vision?
- **Scope**: Right-sized? Any scope creep traps?

### `tasks <story-id>`

Tell user: "Task review coming soon."

### No argument or `help`

Show:
```
/ralph-review stories <milestone>      Review stories for a milestone
/ralph-review roadmap                  Review roadmap milestones
/ralph-review gap roadmap              Cold analysis of roadmap gaps
/ralph-review gap stories <milestone>  Cold analysis of story gaps
/ralph-review tasks <story-id>         (coming) Review tasks for a story
```
