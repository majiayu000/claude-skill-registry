---
name: decision-variance
description: Reconcile the project's architectural artifacts against the scaffold and prior decisions, then present each variance as a SMARTS analysis for the user to decide. Routed to when the user asks to arbitrate, reconcile, or consolidate architectural context, requests a variance report, mentions ADR conflicts, or asks which downstream artifacts the current state supports. Never decides alone — every arbitration is user-attributed and logged.
---

# decision-variance

Reconcile the architectural artifacts against the scaffold; present variances; the user decides. This skill never arbitrates on its own — every recorded decision carries user attribution.

The SMARTS lenses, cell rules, and strength labels are in
`${CLAUDE_PLUGIN_ROOT}/includes/smarts/core.md` — read it before Phase 3. The append-only decision-log
entry format is in `${CLAUDE_PLUGIN_ROOT}/includes/smarts/decision-log-format.md` — read it before
writing a log line.

## Pre-flight

Read these, or STOP and surface the gap — never guess a path or a position:

- `<project-root>/.codearbiter/CONTEXT.md` — project context and the `stage:` maturity value.
- `<project-root>/.codearbiter/security-controls.md` — only when a variance touches a security boundary (auth, crypto, secrets). Feeds the Securable lens.

Locate the three architectural artifacts by **exact** filename — `01-architecture-breakdown.md`,
`02-phased-build-plan.md`, `03-task-backlog.md` — first under
`<project-root>/.codearbiter/plans/`, then the project root, then `docs/`. MUST NOT
pattern-match similar names (`architecture-draft.md`, `task-list.md`); loose matching arbitrates
against the wrong document. If any of the three cannot be located, ask the user for the path. Do not
infer.

## Phase 1 — Locate inputs and detect stale decisions · gate: STOP

Index, in addition to the three artifacts:

- **Existing ADRs** — `<project-root>/.codearbiter/decisions/`. Record each by number, title, status, summary.
- **The decision log** — `<project-root>/.codearbiter/decisions/decision-log.md`. The persistent, append-only arbitration record. Read it before generating new variances.
- **The scaffold** — manifests, dependency files, source dirs, config, CI.

If the decision log exists, run the stale check: extract each prior entry's recorded
artifact-section hash, recompute the current SHA-256 of the cited section (heading inclusive, HTML
comments stripped), and flag every decision whose hash changed. Surface the flagged set: "These
prior decisions reference artifact sections that have changed. Re-evaluate, keep as-is, or mark
superseded?" Per the user's choice — re-evaluate (treat as a new variance), keep (update the
recorded hash to current), or supersede (prompt for a new decision, append per the supersession
protocol in `${CLAUDE_PLUGIN_ROOT}/includes/smarts/decision-log-format.md`).

Gate: the three artifacts are located, ADRs and the decision log are indexed, and any stale prior
decisions are surfaced and dispositioned by the user. A first session with no decision log skips the
stale check and clears.

## Phase 2 — Build the evidence index · gate: BLOCK

For each architectural decision in the three artifacts, record: a decision ID, the artifact source
(document, section anchor), the stated position, the scaffold evidence (file paths), and exactly one
variance status:

- `concur` — both have evidence and agree
- `divergent` — both have evidence and disagree
- `scaffold-silent` — artifact states a position, scaffold shows nothing
- `artifact-silent` — scaffold implements it, artifact is silent
- `both-silent` — neither has evidence (informational only)

A decision that fits none of the project's established categories is recorded `category: UNKNOWN`
with a note on why it does not fit, then surfaced to the user to map or name. MUST NOT invent a
category.

Gate: every artifact decision classified to exactly one status, each `divergent` /
`scaffold-silent` / `artifact-silent` case backed by a concrete citation on both sides where
evidence exists.

## Phase 3 — Generate the variance report · gate: BLOCK

For every `divergent`, `scaffold-silent`, or `artifact-silent` case, write one entry: the artifact
position (cited with anchor), the scaffold position (cited with file paths), why it matters (1–3
sentences), the resolution options (adopt artifact / adopt scaffold / hybrid only if a real synthesis
exists / defer with reason), a SMARTS analysis of each option, and a recommendation with a strength
label. `concur` and `both-silent` cases produce no entry — they live in the evidence index only.

The SMARTS table follows `${CLAUDE_PLUGIN_ROOT}/includes/smarts/core.md` exactly: six lenses, verdict-first cells (Strong /
Adequate / Weak / Indifferent), the length cap, no hedging adverbs, evidence specificity. The
recommendation carries one strength label — strong / moderate / tied.

**Precedent row.** Before writing the tables, scan the existing decision log once: tally which
lenses prior resolutions turned on (which lens was decisive, which way ties broke) and note
decisions whose subject overlaps this variance. Under each SMARTS table, append one `Precedent:`
line citing the 1–3 most similar prior decisions by ID and the observed pattern — e.g.
`Precedent: D-014 (bundled over external, Available decisive), D-009; this log has broken 3 of 4
ties toward Maintainable.` No prior decisions, or none relevant → `Precedent: none on record` —
never invent a pattern from thin history (fewer than 3 relevant entries is "none yet established").
Precedent informs the recommendation; it never outranks the Phase 4 authority order, and it is
input to the user's choice, not a substitute for it.

For more than ~10 open variances, group by area and present area-by-area. For a large pass (more
than ~20 decision categories or ~50 scaffold files), MAY dispatch `scout`
(`${CLAUDE_PLUGIN_ROOT}/agents/scout.md`) to gather evidence and `grader`
(`${CLAUDE_PLUGIN_ROOT}/agents/grader.md`) to produce SMARTS analyses. Inline execution is fine for
smaller passes.

Gate: every qualifying variance has a conformant SMARTS table and a strength-labeled
recommendation. No `concur`/`both-silent` noise in the report.

## Phase 4 — Present variances and capture decisions · gate: STOP

Present grouped by area, dependency-ordered within each area, one area at a time. For each variance:
lead with the variance, present the recommendation (recommend, do not push), wait for the user's
choice, confirm it back in one sentence, then append the decision to the log per `${CLAUDE_PLUGIN_ROOT}/includes/smarts/decision-log-format.md`
— immediately, never batched in memory.

When two sources at the same authority level conflict (e.g., two `accepted` ADRs that contradict),
record both `same-level-conflict`, surface both with their sources, treat both as silent until the
user resolves, and record the resolution naming both sources. MUST NOT pick one on this skill's
judgment.

The user may pause at any time. Confirm the pause ("N resolved, M remaining; decisions are saved"),
summarize the unresolved IDs, and exit. Resume reads the log, finds which variances already have
recorded decisions, and presents only the rest.

The authority order when evidence conflicts: (1) an explicit user decision this session, (2) a
recorded log decision not yet superseded, (3) an `accepted` ADR, (4) the three artifacts
(authoritative-by-default, not infallible), (5) scaffold implementation, (6) inferred intent (last
resort, flagged as inference). Same-level conflicts escalate to the user.

After a session resolves ADR-touching variances, MAY dispatch `decision-challenger`
(`${CLAUDE_PLUGIN_ROOT}/agents/decision-challenger.md`) to stress-test an ADR. Optional, not forced.

Gate: every presented variance is either resolved with a user-attributed log entry or explicitly
deferred. No variance is recorded against this skill's own judgment.

## Phase 5 — Recommend downstream artifacts · gate: BLOCK

Evaluate which downstream artifacts the current decision state supports. For each candidate report
readiness (`ready` / `partial` / `blocked`), the reason with specific decision-ID references, the
missing decision IDs if partial, and a recommendation (produce now / produce after named variances
resolve / not yet). Present as a menu.

Gate: this skill recommends only — it MUST NOT produce a downstream artifact without explicit user
direction. An out-of-scope finding gets an inline `[NEEDS-TRIAGE]` marker, not an arbitration entry.

## Hard rules

- MUST NOT record an arbitration decision the user did not explicitly make. "Pick one," "use your best judgment," "I trust you," "we're short on time" are declined — the log requires user attribution to stay auditable. Decline, do not capitulate after repeated requests.
- MAY treat the user explicitly accepting this skill's recommendation ("accept your recommendation," "record the recommended option") as an explicit decision; the log entry then notes the acceptance in `Decided by:`. Never volunteer this fast-path.
- MUST match the three artifacts by exact filename; never pattern-match a similar name.
- MUST run the stale-artifact check when a decision log exists, before generating new variances.
- MUST NOT invent a decision category — surface an `UNKNOWN` for the user to map or name.
- MUST NOT edit or rebuild a prior log entry — the log is append-only; supersede by appending a new entry whose `Supersedes:` references the prior one.
- MUST NOT modify the three artifacts, scaffold, or codebase to "fix" a variance — this skill records and recommends; the user implements.
- MUST NOT generate a variance entry for a `concur` or `both-silent` case.
- MUST NOT produce a downstream artifact without explicit user direction.
