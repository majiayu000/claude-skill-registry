---
name: skill-author
description: The authoring gate for new skills. Routed to when the user invokes /new-skill "<gap>". Five gated phases — gap evidence, scope, authoring, self-review against the v2 house style, routing integration. A new skill is not written until an existing one is proven not to cover the gap, and not shipped until it carries gated phases, hard rules, and a routing entry. Every authored skill matches the v2 format (frontmatter name+description, # name, Pre-flight, Phase N · gate, Hard rules).
---

# skill-author

Author a new skill, the right way. Routed to when the user invokes `/new-skill "<gap>"`.

## Pre-flight

Read these, or STOP and surface the gap — never author on assumption:

- The `<gap>` argument. Absent → STOP and ask: "Describe the gap this skill would fill. What situation does no existing skill cover today?"
- `${CLAUDE_PLUGIN_ROOT}/skills/INDEX.md` — the surface scan of every existing skill. This is the gap-overlap check in Phase 1 and the integration target in Phase 5. Never bulk-read the skill bodies.
- `${CLAUDE_PLUGIN_ROOT}/skills/commit-gate/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/skills/tdd/SKILL.md` — the canonical v2 format the authored skill must mirror. Read them before Phase 3.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/CONTEXT.md` — project context, only if the gap is project-specific. A generic skill needs no project state.

## Phase 1 — Gap evidence · gate: BLOCK

A new skill is permanent surface area. It is not written until the gap is proven real and proven uncovered.

Restate the gap in one sentence. Then scan `INDEX.md` for overlap: if an existing skill's "Owns" column already covers this, STOP and name it — "The `<name>` skill already owns this; review it before requesting a new one."

If no skill covers it, demand evidence — one of:

- **A** — three specific cases where the gap blocked work: what was attempted, what happened with no skill, what it cost.
- **B** — one high-impact case with traceable evidence: a blocked PR, an introduced defect, a compliance finding, a repeated failure pattern.

Hypothetical cases do not count. Fewer than three (Option A) or no traceable evidence (Option B) → STOP and decline: "Insufficient evidence of a real, recurring gap. A skill adds permanent maintenance cost. Return with evidence and I'll author it."

Gate: the gap is restated, proven uncovered against `INDEX.md`, and backed by Option-A or Option-B evidence. Speculation does not pass.

## Phase 2 — Scope · gate: BLOCK

Settle scope with the user before any prose is written. Ask, and wait for an explicit answer:

- **Routed or dispatched?** A *skill* is routed to (gated phases, lives at `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md`). An *agent* is dispatched by a skill (a reviewer/author, lives at `${CLAUDE_PLUGIN_ROOT}/agents/<name>.md`). If the gap is really a reviewer, this is the wrong skill — redirect to agent authoring.
- **Command-invoked or internal?** Does a user type `/<name>` to reach it, or does another skill route to it mid-workflow? A command needs a routing-table entry; an internal skill needs a named parent that routes to it.
- **Single responsibility.** State the one thing the skill owns in a sentence. If it needs "and" to describe its job, it is two skills — split it or pick one.

Confirm back: "I will write a [command-invoked / internal] skill at `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md`, owning <one responsibility>. [A `/<name>` command will be added to the routing table. / The `<parent>` skill will route to it.]"

Gate: explicit user agreement on routed-vs-dispatched, command-vs-internal, and a one-sentence single responsibility. Assumed answers do not pass.

## Phase 3 — Authoring · gate: BLOCK

Write `SKILL.md` to the v2 house style — mirror `commit-gate` and `tdd` exactly. Start from `${CLAUDE_PLUGIN_ROOT}/skills/skill-author/references/skill-template.md`. Required shape:

- **Frontmatter** — `name:` and `description:` only. Description is terse: what routes to it, the phase count, the gate. No cut doc refs, no trigger disclaimer.
- **`# <name>`** H1, then a one-line intro naming what routes to it (`/<command>` or the parent skill).
- **`## Pre-flight`** — the docs to read or STOP on. Project state cites `${CLAUDE_PROJECT_DIR}/.codearbiter/<doc>`; other skills cite `${CLAUDE_PLUGIN_ROOT}/skills/<name>`; agents cite `${CLAUDE_PLUGIN_ROOT}/agents/<name>.md`. Never guess a command — read it or STOP.
- **`## Phase N — <title> · gate: BLOCK|STOP`** — sequential, each ending in a one-line `Gate:`. A phase with output that could be wrong has a gate; only a purely declarative phase may omit one.
- **`## Hard rules`** — `MUST NOT` lines, one per rule, no duplication.

Authoring rules:

- Imperative, terse, no hedging. No "should", no "if it looks wrong". A gate is a concrete, checkable condition.
- Surviving project docs only: `CONTEXT.md`, `tech-stack.md`, `coding-standards.md`, `specs/`, `plans/`, `security-controls.md`, `decisions/`, `overrides.log`. Do not reference cut docs or cut skills.
- Terminology lock: a skill is *routed to*; an agent is *dispatched*. Never "trigger", "fires", or "runs".
- An out-of-scope finding gets one line with an inline `[NEEDS-TRIAGE]` marker.

## Phase 4 — Self-review · gate: BLOCK

Re-read the authored skill against the v2 quality bar. Each line below is a checkable defect, not a vibe:

- **Single responsibility** — the skill owns one thing. If a phase belongs to a different job, it is the wrong skill; cut it.
- **Concrete gates** — every non-declarative phase ends in a `Gate:` line stating a checkable condition. "Looks good" / "seems right" is not a gate; rewrite it.
- **House-style prose** — terse, imperative, matches `commit-gate`/`tdd`. Strip hedging and filler.
- **No duplicated rules** — a rule stated in a phase is not restated in Hard rules, and Hard rules carry no duplicates. State each rule once.
- **Format conformance** — frontmatter is `name`+`description` only; H1 matches `name`; phases are numbered with `· gate:`; paths use `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PROJECT_DIR}` correctly; no cut docs/skills, no legacy `${FRAMEWORK_ROOT}`/`${PROJECT_ROOT}`/`.agents/` paths.
- **No trigger language** — "routed to" / "dispatched" only, and no `## Trigger` disclaimer block.

Compile the findings, fix each, and re-read once. Present the corrected skill and the findings list to the user.

Gate: zero open self-review defects, and the user has seen the corrected skill. An unaddressed defect blocks Phase 5.

## Phase 5 — Routing integration · gate: BLOCK

A skill no one routes to is dead code. Wire it in.

- Add a row to `${CLAUDE_PLUGIN_ROOT}/skills/INDEX.md`: skill name (linked), "Routed to by", and "Owns" (the one-sentence responsibility from Phase 2).
- Add the skill to the routing table — the invocation cue (the `/<command>` or condition), the primary route, any dispatched agents, the hard gate. For a command-invoked skill, also register the `/<command>` in the command reference.
- For an internal skill, update the named parent so it routes to the new skill explicitly.

Verify no broken references: every path the skill cites resolves, and the `INDEX.md` row matches the file.

Hand off to `commit-gate` — never `git commit` directly. The skill change ships only through the commit gate.

Gate: `INDEX.md` and the routing table updated, no broken references, and the change handed to `commit-gate`.

## Hard rules

- MUST NOT author a skill before the gap is proven uncovered against `INDEX.md` and backed by Option-A or Option-B evidence.
- MUST NOT begin authoring without explicit user agreement on scope (routed-vs-dispatched, command-vs-internal, single responsibility).
- MUST NOT emit a skill whose phases lack concrete `Gate:` lines, or whose Hard rules duplicate phase rules.
- MUST NOT use trigger language ("trigger", "fires", "runs") or a `## Trigger` disclaimer — a skill is routed to, an agent dispatched.
- MUST NOT reference a cut doc, cut skill, or a legacy `.agents/` / `${FRAMEWORK_ROOT}` / `${PROJECT_ROOT}` path in an authored skill.
- MUST NOT ship a skill without an `INDEX.md` row and a routing entry.
- MUST NOT commit the new skill directly — hand off to `commit-gate`.
