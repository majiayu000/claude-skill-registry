---
name: teach-from-paper
description: Turn a research paper into teaching materials — a lecture outline, the 3-5 results worth presenting (with intuition), a slide skeleton ready for `/create-lecture`, discussion questions, and a problem-set brief. Reads the paper end-to-end and pitches to a stated audience level. Use when user says "turn this paper into a lecture", "teach from this paper", "build slides from this PDF", "make teaching materials from X", "I'm presenting this paper to my class".
argument-hint: "[paper-path] [--level undergrad|phd|seminar] [--minutes N] [--no-exercises]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
effort: high
---

# Teach From Paper

Convert one research paper into a ready-to-build teaching package: a lecture outline, a shortlist of teachable results with the intuition spelled out, a slide skeleton, discussion questions, and an exercise brief. The deliverable is an outline and a brief — **not** a finished deck; the slide skeleton is shaped to hand straight to `/create-lecture`, and the exercise brief to `/scaffold-exercises`.

## When to use

- You have a paper (PDF, `.tex`, `.md`) and a slot to teach it — a lecture, a reading group, a job-market practice talk.
- You want the teachable core extracted and pitched to a level, not a generic summary.
- You're prepping the *plan* for a deck and want `/create-lecture` to do the drafting.

Not for: literature surveys across many papers (use `/lit-review`); refereeing the paper's correctness (use `/review-paper`); drafting the actual Beamer slides (use `/create-lecture`).

## Inputs

- `$0` — path to the paper.

| Format | How to read it |
| --- | --- |
| `.tex`, `.qmd`, `.md`, `.txt` | Read directly with the `Read` tool. |
| `.pdf` | `TMP=$(mktemp -t paper).txt && pdftotext "$0" "$TMP"` (poppler-utils), then Read/Grep `"$TMP"`. |

If extraction fails or the tool is missing, ask the user for a plain-text version and stop. The full paper goes in the context window (1M) — read it end-to-end before extracting; do not skim the abstract and guess.

## Phases

### Phase 0: Read the Paper + Set Audience Level (Pre-Flight Report)

Read the paper start to finish. Then resolve the audience level and time budget — from `--level` / `--minutes` if given, otherwise ask once. Echo a Pre-Flight Report before extracting:

```markdown
## Pre-Flight Report
**Paper:** [title, authors, year]
**One-line thesis:** [the paper's central claim in your words]
**Audience level:** undergrad | phd | seminar   (drives notation depth + which proofs survive)
**Time budget:** N minutes (~N/2 slides)
**Prerequisites assumed:** [concepts students must already have]
**Running example candidate:** [the paper's application that can thread the lecture]
```

Get a nod on level + thesis, then proceed. Level governs everything downstream: undergrad keeps intuition and drops proofs; phd keeps the identifying assumptions and one key derivation; seminar foregrounds the contribution-vs-literature framing.

### Phase 1: Extract the Teachable Core + Intuition

1. Identify the paper's **3-5 results worth presenting** — not every proposition, the ones a student should leave remembering. Prefer the headline result, the identifying assumption that makes it credible, and one surprise or limitation.
2. For each, capture: the **formal statement** (trimmed to the audience level), the **intuition** (why it's true in one breath, no algebra), and the **failure mode** (when it breaks).
3. Map the paper's notation to something teachable; flag any symbol clash a student would trip on.
4. Separate **method** (how they get the result) from **takeaway** (what we now believe) — students conflate these; the lecture must not.

### Phase 2: Build the Lecture Outline + Slide Skeleton

Produce a motivation → setup → key result → method → takeaways arc, then a slide skeleton matching the time budget (~2 min/slide). Each skeleton entry is a title + one-line content note + figure/diagram placeholder — enough for `/create-lecture` to draft from, no prose. Honor the project's pedagogy invariants in shape: motivation before formalism, a worked example near each definition, a transition slide at each act break.

### Phase 3: Discussion Questions + Exercise Brief

1. Write **4-6 discussion questions** graded by depth: comprehension → application → critique ("where would this identification fail?"). Pitch to the level.
2. Write an **exercise brief** — 2-4 problems sketched (prompt + what skill it drills + expected-answer shape), NOT full solutions. This is the hand-off to `/scaffold-exercises`, which fleshes out problems, data, and answer keys. Skip if `--no-exercises`.

## Output / Report format

Write to `quality_reports/teach_from_paper_[sanitized-title].md`:

```markdown
# Teaching Package: [Paper Title]
**Audience:** [level] · **Budget:** [N min] · **Date:** [YYYY-MM-DD]

## 1. Lecture Outline
Motivation → Setup → Key Result → Method → Takeaways  (one line each)

## 2. Results Worth Presenting
### R1 — [name]
- **Statement:** … · **Intuition:** … · **Breaks when:** …
[R2..R5]

## 3. Slide Skeleton  (→ /create-lecture)
| # | Title | Content note | Figure/diagram |

## 4. Discussion Questions
1. [comprehension] … 5. [critique] …

## 5. Exercise Brief  (→ /scaffold-exercises)
- **E1:** [prompt] — drills [skill] — answer shape: [form]
```

## Exit behavior

- Present the package in chat and confirm the file path written.
- Name the two hand-offs explicitly: "Slide skeleton ready — run `/create-lecture [Topic]`. Exercise brief ready — run `/scaffold-exercises`."
- If the audience level was never confirmed, do **not** ship — a deck pitched at the wrong level is wasted work. Halt and ask.

## Flags

- `--level` — `undergrad` | `phd` | `seminar`. Sets notation depth, which proofs survive, and question difficulty. Asked interactively if omitted.
- `--minutes` — target lecture length; the slide count is roughly `--minutes`/2.
- `--no-exercises` — skip Phase 3's exercise brief (keep discussion questions).

## Cross-references

- `/create-lecture` — consumes the Phase 2 slide skeleton to draft the actual Beamer deck. See [`.claude/skills/create-lecture/SKILL.md`](../create-lecture/SKILL.md).
- `/review-paper` — referee the paper's correctness *before* teaching it if you're unsure the result holds. See [`.claude/skills/review-paper/SKILL.md`](../review-paper/SKILL.md).
- `/lit-review` — for situating the paper among many, rather than teaching one deeply. See [`.claude/skills/lit-review/SKILL.md`](../lit-review/SKILL.md).
- The Phase 5 exercise brief is the input contract for `/scaffold-exercises` (a downstream skill that fleshes out problem sets); this skill stops at the brief.

## What this skill does NOT do

- Does **not** draft finished slides — that's `/create-lecture`. The slide skeleton is an outline, not Beamer.
- Does **not** write full problem-set solutions — the exercise brief is a sketch for `/scaffold-exercises`.
- Does **not** verify the paper is correct — pair with `/review-paper` if the result's validity is in doubt.
- Does **not** read multiple papers or survey a field — one paper in, one teaching package out.
