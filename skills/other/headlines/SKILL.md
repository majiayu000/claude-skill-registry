---
name: headlines
description: "Generate headlines, titles, and subject lines: charge, volume, tighten."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  triggers:
    - "headline"
    - "headlines"
    - "article title"
    - "title options"
    - "subject line"
    - "better title"
  category: content-creation
  pairs_with:
    - voice-writer
    - content-engine
    - topic-brainstormer
---

# Headlines

## Overview

Generates headlines, article titles, social posts, and email subject lines from a brief or draft. Four phases: find the charge, generate volume across named moves, tighten survivors, output per format. Core rule: **volume over polish** — word-level features predict winners weakly, so breadth beats optimization.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| generating candidates: the ten named headline moves with examples | `references/headline-moves.md` | Move definitions and concrete examples for Phase 2. |

## Instructions

### Phase 1: FIND THE CHARGE

**Goal**: Identify the single most compelling tension or stake in the material.

1. Read the brief, draft, or topic statement in full.
2. List every tension candidate: a surprise, a reversal, a cost, a conflict, a number that changes the picture, a stake the reader holds.
3. Pick ONE — the charge. Write it as a single sentence naming who is affected and what is at stake.
4. Test it: would a reader who saw only this sentence want the rest? A topic label ("Kubernetes networking") fails; a live tension ("DNS resolved yesterday, fails today, nothing changed") passes.

**Gate**: Charge is one sentence, names a specific tension or stake, and is true to the source material. Proceed only when it passes — every candidate in Phase 2 builds on it, so a weak charge produces 20 weak headlines.

---

### Phase 2: GENERATE VOLUME

**Goal**: Produce 15–25 candidate headlines spread across the named moves.

Load `references/headline-moves.md` for the move catalog: **curiosity gap, specificity, stakes, contrast, question, how-to, number, voice-of-reader, news peg, negative space**.

1. Generate 15–25 candidates. Write fast; judge later. Polishing during generation narrows the search exactly where breadth pays.
2. Cover at least 6 of the 10 moves. Tag each candidate with its move.
3. Keep every candidate anchored to the Phase 1 charge. A clever line off-charge is a miss.
4. Pull concrete material from the brief into candidates: numbers, names, error messages, dates. Specifics carry more pull than adjectives.

**Gate**: 15–25 candidates exist, each tagged with a move, at least 6 moves represented. Fewer than 15 means the charge is under-mined — return to the brief for more concrete material.

---

### Phase 3: TIGHTEN

**Goal**: Select and sharpen 3–5 survivors using a stated criterion.

1. Score every candidate 1–5 on each of: specificity, tension, accuracy to the brief. Sum the three.
2. Keep the top 3–5 by score. Require move diversity among survivors — two candidates from the same move compete for the same reader reflex, so keep the stronger one.
3. Tighten each survivor:
   - Cut filler words; front-load the charge into the first 3–4 words (truncation and scanning both favor the front).
   - Replace any vague noun with the concrete one from the brief.
   - Verify every claim in the headline against the brief. The headline promises only what the content delivers — an overpromising headline buys one click and spends the reader's trust. This honesty rule applies in every mode, standalone included.
4. Drop any survivor that needs a hedge to stay accurate. Promote the next candidate by score instead.

**Gate**: 3–5 survivors, each accurate to the brief, each from a distinct move where possible.

---

### Phase 4: OUTPUT PER FORMAT

**Goal**: Adapt survivors to the formats the task needs. The user receives selected options plus one recommendation — triage stays inside this skill.

| Format | Constraint | Adjustment |
|--------|-----------|------------|
| Article title | ~60–70 chars; sentence case per site convention | Full charge; specificity over wordplay |
| Social post | Platform length; standalone (no body to lean on) | Add the stake or number the title implies; end with pull, not summary |
| Email subject line | ~30–50 chars; first words decide the open | Front-load the charge; cut articles and qualifiers first |

Per-platform length and format specs stay with content-engine (`skills/content/content-engine/references/platform-specs.md`); when both apply, the platform spec wins on length.

Present output as:

```markdown
## Headline Options

**Charge**: [one-sentence charge]

### Article titles
1. "[title]" — [move]
2. ...

### Social posts
1. "[post]"

### Subject lines
1. "[subject]"

**Recommendation**: [pick one, one sentence why]
```

**Gate**: Each requested format has 2+ options. Recommendation given with reasoning.

---

## Integration

- **voice-writer HOOK-GATE (Phase 5)**: conceptual feed only — voice-writer's pipeline is unchanged. When voice-writer's hook scores below 8, the HOOK-GATE agent may run Phases 1–3 here against the article body to surface the concrete detail the opening should lead with; survivors also serve as title candidates.
- **content-engine**: supplies titles and subject lines for pipeline output; content-engine owns per-platform format specs.
- **Standalone**: usable directly on any brief, draft, or topic. The Phase 3 honesty rule still gates output.

---

## Error Handling

### Error: "Brief has no tension — it is a topic label or flat release notes"
Cause: Input has no stake, surprise, or change worth charging.
Solution: Ask for the one fact that surprised the author, the cost of the problem, or what changed. If none exists, say so and produce plain utilitarian titles — a fabricated tension fails the Phase 3 accuracy check anyway.

### Error: "All candidates sound the same"
Cause: Generation stayed inside one or two moves.
Solution: Walk the move catalog in order and force one candidate per unused move. Mechanical coverage breaks the rut.

### Error: "Accurate headlines feel flat"
Cause: The charge is weak, not the wording. Word-level polish cannot rescue a stake-free premise.
Solution: Return to Phase 1. Find a sharper tension in the material, or report honestly that the brief needs a stronger finding before headlines can work.
