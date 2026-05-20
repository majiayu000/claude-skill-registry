---
name: course-workflow
description: Orchestrate course development workflow, track progress, and capture learnings.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Course Workflow Orchestrator

## Description
Guides course development through a 11-phase workflow. Reads current status, suggests next steps, invokes appropriate skills, updates status, and captures learnings that improve the process over time.

## Instructions

### Path Resolution

Resolve file paths based on your execution context:

- **Plugin context** (`${CLAUDE_PLUGIN_ROOT}` is set): Read knowledge from `${CLAUDE_PLUGIN_DATA}/knowledge/` (user data), falling back to `${CLAUDE_PLUGIN_ROOT}/knowledge/` (seed data). Write knowledge to `${CLAUDE_PLUGIN_DATA}/knowledge/`.
- **Clone/symlink context** (default): Read and write knowledge at `knowledge/` relative to the project root.

### 1. List Courses and Select

First, scan `courses-in-progress/` for course directories. For each, read `00-course.md` to get title and status.

Present a course selection:

```markdown
## Courses In Progress

| # | Course | Status | Phase |
|---|--------|--------|-------|
| 1 | Andamio for Contributors | revised | 3/11 |
| 2 | Andamio for Course Creators | slts-drafted | 1/11 |
| 3 | Andamio for API Developers | slts-drafted | 1/11 |

Which course are you working on? (Or: "new" to start a new course)
```

If the user says "new", guide them through creating a new course directory with `01-slts.md`. The `00-course.md` (complete course outline) is built up through the workflow.

### 2. Determine Current State

Once a course is selected, read the course's `00-course.md` to get:
- Current `status` field (in frontmatter)
- Course metadata (title, audience, etc.)

Check which workflow artifacts exist:
- `00-course.md` (complete course outline — the final output)
- `01-slts.md` (working file for SLT drafting/revision)
- `02-slts-quality-review.md`
- `03-lesson-type-classification.md`
- `04-readiness-assessment.md`
- `05-delegation-map.md`
- `assets/screenshots/README.md` (screenshot checklist)
- `assets/code-examples/README.md` (code example checklist)
- `lessons/` directory contents

**Key insight:** `00-course.md` is the deliverable — it contains metadata, modules, SLTs, lesson types, and assignments. `01-slts.md` is the working file where SLTs are drafted and refined before being incorporated into the course outline.

### 3. Map Status to Next Action

| Current Status | Phase | Next Action | Skill to Invoke |
|----------------|-------|-------------|-----------------|
| `slts-drafted` | 1→2 | Assess SLT quality, apply fixes to `01-slts.md` | `/assess-slts` |
| `quality-reviewed` | 2→3 | Classify lesson types | `/classify-lesson-types` |
| `types-classified` | 3→4 | Assess agent readiness | `/self-assess-readiness` |
| `readiness-assessed` | 4→5 | Create delegation map | (manual) |
| `delegation-mapped` | 5→6 | Gather context assets | `/gather-screenshots`, `/gather-code-examples` |
| `context-gathered` | 6→7 | Build lessons | (lesson skills) |
| `building` | 7 | Continue building lessons | (lesson skills) |
| `lessons-complete` | 7→8 | Compile modules for import | `/compile` |
| `compiled` | 8→9 | Run full course retrospective | `/compound --rollup` |
| `compounded` | 9→10 | Move to courses/, update COURSES.md | (manual) |

**Note:** Phase 2 (quality review) now includes applying fixes. No separate "revise" phase — edits happen in place, patterns compound to knowledge base.

### 3b. Phase 6: Gather Context (Detail)

Phase 6 prepares assets needed before building lessons. The readiness assessment identifies what's missing; the gather skills create checklists for collection.

**Invoke based on lesson types:**

| Lesson Type | Skill | Output |
|-------------|-------|--------|
| Product Demo | `/gather-screenshots` | `assets/screenshots/README.md` |
| Developer Documentation | `/gather-code-examples` | `assets/code-examples/README.md` |
| How To Guide | (manual) | Supplementary docs in `assets/` |
| Exploration | (usually none) | Framing questions in lesson inputs |
| Organization Onboarding | (manual) | Org-specific context in `assets/` |

**Workflow:**
1. Run `/gather-screenshots` if course has Product Demo SLTs needing context
2. Run `/gather-code-examples` if course has Developer Documentation SLTs needing context
3. Human captures screenshots / writes code examples following checklists
4. Files saved to `assets/screenshots/` or `assets/code-examples/`
5. Check off items in README as completed
6. When all context gathered, update status to `context-gathered`

**Directory structure after Phase 6:**
```
courses-in-progress/[course-slug]/
  assets/
    screenshots/
      README.md           # Capture checklist
      1.2-wallet-connect-01.png
      ...
    code-examples/
      README.md           # Code checklist
      1.2-api-auth.ts
      ...
```

### 4. Present Status and Recommendation

Output a status card:

```markdown
## Course: [Course Title]

**Current Status:** [status] (Phase [n] of 11)
**Progress:** [visual indicator, e.g., ████░░░░░░ 4/11]

### Completed Artifacts
- [x] 01-slts.md
- [x] 02-slts-quality-review.md
- [ ] 03-lesson-type-classification.md
- ...

### Recommended Next Step
[Description of what to do next]

**Action:** [Specific action - invoke skill, manual step, etc.]
```

### 5. Execute or Guide

If the next step involves a skill:
- Confirm with user: "Ready to run /[skill-name]?"
- If yes, invoke the skill
- After skill completes, prompt to update status

If the next step is manual:
- Explain what needs to be done
- Offer to help with specific sub-tasks
- Prompt to update status when complete

### 6. Update Status

After each phase completes, update `00-course.md`:
- Change `status` field to new value
- Add `last_updated` timestamp
- Add brief note about what was done

### 7. Capture Learnings

After each phase transition, ask:
- "Any friction in this phase?"
- "Anything that should work differently next time?"

Append learnings to `workflow-learnings.md` in the project root (create if doesn't exist):

```markdown
## [Date] - [Course Name] - Phase [n] → [n+1]

**What happened:** [brief summary]

**Friction:** [what was hard or unclear]

**Improvement idea:** [how to make it better]

**Heuristic:** [if a generalizable pattern emerged]
```

### 7b. Compounding Knowledge

**Phase 9 (mandatory):** When lessons are complete, run `/compound --rollup` to extract all knowledge from the course before promotion. This is a required step in the workflow.

**Mid-workflow (optional):** You can also run compound after specific phases to capture knowledge incrementally:

| Phase Completed | Optional Command |
|-----------------|------------------|
| quality-reviewed (2→3) | `/compound quality-review` |
| types-classified (4→5) | `/compound classification` |
| readiness-assessed (5→6) | `/compound readiness` |

The `/compound` skill extracts structured knowledge from artifacts into the `knowledge/` directory, which improves future skill runs.

**Relationship between files:**
- `workflow-learnings.md` = human-readable narrative, captured conversationally
- `knowledge/*.yaml` = machine-readable patterns, consumed by skills

### 8. Show Accumulated Learnings

When starting a workflow session, check `workflow-learnings.md` for relevant insights:
- Learnings from the same phase
- Learnings from the same course type
- Recently added heuristics

Surface these as "tips from previous runs."

## Status Field Format

The `status` field in `00-course.md` should be in YAML frontmatter:

```yaml
---
course: Andamio for Contributors
status: quality-reviewed
last_updated: 2026-02-27
---
```

If no frontmatter exists, add it.

## Workflow Learnings File

The `workflow-learnings.md` file accumulates insights across all courses. Structure:

```markdown
# Workflow Learnings

Insights captured during course development that improve the process over time.

## Phase-Specific Learnings

### Phase 2: Assess SLT Quality
- [learning]

### Phase 4: Classify Lesson Types
- [learning]

...

## Cross-Cutting Heuristics

Patterns that apply across phases:
- [heuristic]

## Course-Specific Notes

### andamio-for-contributors
- [note]
```

## Guidelines

- **Don't skip phases.** The workflow is sequential for a reason. If artifacts are missing, flag it.
- **Update status promptly.** Status should reflect reality. Stale status causes confusion.
- **Learnings are optional but valuable.** Don't force them, but always ask.
- **Surface relevant history.** Previous learnings make each run smarter.
- **Manual steps are real steps.** Guide them as carefully as automated ones.
- **One course at a time.** Don't try to orchestrate multiple courses in parallel.
