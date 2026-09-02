---
name: show-way
description: 'Use when the user asks for a flattened view of roadmaps and next actions. Returns a dependency-ordered task list with status glyphs and a next-actions frontier as chat output, without taking execution authority. Not for multi-session route planning — use wayfinder.'
---

# Show way

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks for a flattened view of roadmaps and next actions. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Chat output only: a flattened human-readable roadmap and next-action list. |
| Done | Roadmaps and next actions are shown without taking execution authority. |

## Inputs

- **Roadmap source** (required): one or more of the following, supplied by the user or discoverable in the current session context:
  - A planning document, spec, or strategy file path.
  - A tracker reference (GitHub issue, project board, or local ticket set).
  - A conversation thread containing a plan or decomposition.
- **Scope constraint** (optional): a named subsystem, phase, or time horizon to limit the flattened view. If absent, flatten everything discoverable.

## Procedure

1. **Collect roadmap material.** Read every source the user names or that the session already holds. If the user names nothing and the session holds no plan, stop and ask one question naming what to flatten; do not flatten nothing. Done when: every named source is read or the user is asked for a source.
2. **Extract structure.** From each source, extract milestones or phases, tasks or tickets, dependencies or ordering constraints, and status markers (done, in-progress, blocked, open). Preserve the source's own grouping where it exists. Done when: milestones, tasks, dependencies, and status markers are extracted from every source.
3. **Flatten.** Linearize the extracted structure into a single ordered list:
   - Group by milestone or phase heading.
   - Within each group, order by dependency: items with no unmet blockers first, then items blocked by those, and so on.
   - Mark each item with its status using a single glyph: `[x]` done, `[~]` in progress, `[!]` blocked (name the blocker), `[ ]` open.
   - For each open or blocked item, append a **next action**: the smallest concrete step that advances it.
   Done when: the full list is linearized with groups, dependency ordering, status glyphs, and next actions.
4. **Identify the frontier.** After the full list, add a `## Next actions` section listing only the open items whose blockers are all resolved, each with its next action. These are the items a human or agent could act on right now. Done when: the frontier section lists only immediately actionable items.
5. **Stop.** Do not create tickets, assign work, modify files, or propose execution plans. The flattened view is the deliverable. Done when: no execution action is taken; the flattened view is the sole output.

## Failure and recovery
- **No roadmap source found.** Report that no plan or roadmap material was identified. Ask one question naming what to read. Do not invent structure.
- **Source is ambiguous or partial.** Flatten what is legible. Flag gaps with `[?]` and a one-line note naming what is missing. Do not fill gaps with guesses.
- **Source contains execution state the skill cannot verify.** Present the state as reported by the source without confirming or disputing it. Label it `source-reported`.
- **Scope is too large for one output.** Flatten the portion the user scoped. If no scope was given and the result exceeds a reasonable single message, split by milestone and deliver the first chunk, naming the remainder.

## Output
A single chat message: a flat dependency-ordered task list grouped by milestone with status glyphs and next actions per item, followed by a `## Next actions` frontier section listing only immediately actionable items. No execution commitment, tracker mutation, or follow-up scheduling.
