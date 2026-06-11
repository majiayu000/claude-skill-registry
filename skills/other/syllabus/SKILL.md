---
name: syllabus
description: Build or restructure a course syllabus from a topic list or reading list — course description + prerequisites, week-by-week schedule (topic → readings → deliverables), measurable learning objectives, an assessment scheme + rubric, standard policies (late work, AI use, academic integrity, accessibility), and a per-week work-list to hand to `/create-lecture`. Use when user says "build a syllabus", "structure my course", "turn this reading list into a schedule", "draft a course outline", "make a syllabus for Econ 7xx", or "map weeks to lectures". Economics-aware (PhD metrics/micro/macro sequences, undergrad); generic enough for any field.
argument-hint: "[course title or topic/reading list] [--weeks N] [--level phd|grad|undergrad] [--sessions-per-week N] [--no-policies]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
effort: medium
---

# Build a Course Syllabus

Turn a bare topic list or reading list into a teachable syllabus: a course description, a sequenced weekly schedule, measurable objectives, an assessment scheme with a rubric, the boilerplate policies every syllabus needs, and a week→lecture work-list you can feed straight into `/create-lecture`. The instructor owns the academic judgment; this skill structures it.

## When to use

- You have a pile of topics or papers and need them ordered into a term.
- You are converting last year's syllabus to a new length, level, or modality.
- You want the schedule's weeks pre-mapped to lecture decks before you start building slides.

Not for building the slides themselves (`/create-lecture`), reviewing a deck's pedagogy (`/pedagogy-review`), or assembling the reading list from scratch (`/lit-review`).

## Phase 0: Intake (elicit before drafting)

A syllabus is shaped almost entirely by three parameters. Resolve them first — from flags, then by asking. Do **not** start sequencing until all three are pinned.

1. **Level + audience** — `--level` (`phd` / `grad` / `undergrad`). For economics, name the sequence (first-year metrics, micro theory, macro, field course, undergrad intermediate). Level sets reading depth, proof-vs-application balance, and assessment type.
2. **Length + cadence** — `--weeks` (default 14) and `--sessions-per-week` (default 2). A reading seminar and a problem-set course at the same length need very different schedules.
3. **Material** — the topic list or reading list (`$ARGUMENTS`, a file path, or a `.bib`). If the user points at a `.bib` or a folder of PDFs, `Glob`/`Read` to inventory it; if topics are bare, ask for 1-2 anchor texts per topic.

Echo a short **Intake Report** (level, weeks, cadence, N topics / N readings, any gaps) and get confirmation before Phase 1.

## Phase 1: Sequence topics into weeks

1. **Order by dependency, not by the reading list's order.** Build a prerequisite chain — foundational tools before the topics that use them (e.g., asymptotics → GMM → applications; consumer theory → GE → welfare). Front-load what later weeks assume.
2. **Allocate readings to weeks.** Distribute material so each week's load is realistic for the level (a PhD field week carries 2-4 papers; an undergrad week, 1 chapter + 1 application). Flag any week that is overloaded or thin.
3. **Place deliverables on the calendar.** Problem sets after the tools they exercise; the midterm at a natural conceptual break; referee report / replication / paper proposal milestones spaced so they don't collide. Mark reading-break and no-class weeks.
4. **Emit the schedule table** (topic → readings → deliverable per week) and get sign-off before writing objectives — re-sequencing is cheap now, expensive later.

## Phase 2: Objectives + assessment

1. **Write measurable learning objectives.** One course-level set plus per-unit objectives, each using an observable verb (derive, estimate, replicate, critique, prove) — not "understand" or "be familiar with". Tie each objective to the week(s) that deliver it.
2. **Design the assessment scheme.** Pick instruments that fit the level (problem sets + final for a methods course; referee report + replication + paper for a field/PhD course; exams + project for undergrad). State weights summing to 100%, and check every objective is assessed by something.
3. **Write one rubric** for the highest-stakes deliverable (the paper, project, or referee report) — criteria × levels, with point bands. Keep it short and concrete.

## Phase 3: Emit the syllabus + the lecture work-list

1. **Assemble the syllabus document** in the Output format below (skip policies if `--no-policies`).
2. **Generate the per-week `/create-lecture` work-list** — one row per teaching week mapping it to a deck name, its objective(s), and its anchor reading, so the instructor can hand each row to `/create-lecture` in order. This is the bridge from syllabus to slides.

## Output format

Write to `syllabus.md` (or a user-specified path):

```markdown
# [Course title] — [Term, Year]
[Level · meeting cadence · units]

## Course description
[2-4 sentences: what the course is, what students leave able to do.]

## Prerequisites
[Courses / skills assumed. Be specific — "first-year metrics or equivalent".]

## Learning objectives
By the end of this course, students will be able to:
- [observable verb] … (Weeks N-M)

## Weekly schedule
| Week | Topic | Readings | Deliverable |
|------|-------|----------|-------------|
| 1 | … | … | — |

## Assessment
| Component | Weight | Maps to objectives |
|-----------|-------:|--------------------|
| … | …% | … |

### Rubric — [highest-stakes deliverable]
| Criterion | Excellent | Adequate | Weak |
|-----------|-----------|----------|------|

## Policies
Late work · AI / LLM use · academic integrity · accessibility / accommodations · attendance.

## Week → lecture work-list (hand to `/create-lecture`)
| Week | Deck name | Objective(s) | Anchor reading |
|------|-----------|--------------|----------------|
```

End the chat message (not the file) with a **gap summary**: weeks with no reading, objectives not assessed, deliverable collisions, or topics dropped for lack of time — the instructor decides how to resolve each.

## Flags

- `--weeks` — term length in teaching weeks (default 14).
- `--level` — `phd` / `grad` / `undergrad`; sets reading depth and assessment type.
- `--sessions-per-week` — meetings per week (default 2); affects per-week load.
- `--no-policies` — omit the boilerplate Policies section (use when an institutional template supplies it).

## Exit behavior

- Phase 0 halts until level, length, and material are all resolved — a forked or unattended run never guesses these. If the material is empty, ask for a topic/reading list and stop.
- Each phase gates on user sign-off (schedule before objectives, objectives before policies); re-ordering is offered cheaply at Phase 1.
- The deliverable is the syllabus file plus the work-list; the chat message always carries the gap summary, even when empty (`No gaps — every week has a reading and every objective is assessed.`).
- This skill is text-only; it never compiles, renders, or builds slides.

## Cross-references

- `/create-lecture` ([`.claude/skills/create-lecture/SKILL.md`](../create-lecture/SKILL.md)) — the natural next step; feed it the work-list rows one week at a time.
- `/lit-review` ([`.claude/skills/lit-review/SKILL.md`](../lit-review/SKILL.md)) — build or extend the reading list *before* sequencing.
- `/interview-me` ([`.claude/skills/interview-me/SKILL.md`](../interview-me/SKILL.md)) — if the course goals are still fuzzy, formalize them first.
- `/pedagogy-review` ([`.claude/skills/pedagogy-review/SKILL.md`](../pedagogy-review/SKILL.md)) — review narrative/pacing once decks exist; the syllabus arc is the input it checks against.
- Authoring conventions: [`templates/skill-template.md`](../../../templates/skill-template.md).

## What this skill does NOT do

- Does not write slide content or scaffold `.tex`/`.qmd` decks — that is `/create-lecture`.
- Does not search for or vet readings — pair with `/lit-review`.
- Does not grade, generate problem sets, or build answer keys.
- Does not assert institutional policy as binding — the Policies section is editable boilerplate the instructor must reconcile with their department's rules.
- Does not invent citations; every reading in the schedule comes from the material the user supplied.
