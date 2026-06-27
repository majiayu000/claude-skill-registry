---
name: doc-review
description: Persona-based review of a requirements doc, plan, spec, or PRD by content shape — classify the document, dispatch conditional reviewer lenses in parallel, merge confidence-anchored findings, and route each as safe-auto / gated-auto / manual / FYI. Read-only on the reviewed document. Use when the user says "review this plan", "review this spec", "review this PRD", "review these requirements", "critique this design doc", or "/doc-review". Reviews prose documents, not code — docs↔code drift is `sync-docs`; code review is `review`.
metadata:
  short-description: Multi-persona content-shape review of plans/specs/PRDs — read-only, findings routed by tier
---

# Doc-review — multi-persona content-shape review of plans and specs

`doc-review` evaluates a requirements doc, plan, spec, or PRD through specialist reviewer lenses. It classifies the document by content shape, selects the lenses the document actually warrants, dispatches them in parallel as read-only subagents, merges their confidence-anchored findings, and routes each survivor into one of four handling tiers. The structural invariant: **it never edits the document under review.** The only surface it may write is a single review-record file, and only when persistence is requested.

`Op:` of every run is `extend` — it adds an evaluation artifact (findings, optionally one record file), never a change to the reviewed doc. There is no `correct` path here: the skill is read-only on its subject, so it cannot restore an invariant *in* it — restoring the document is a separate writer's job.

Adapted from EveryInc/compound-engineering-plugin (MIT).

## Auto-invoke

<auto_invoke>
<trigger_phrases>
- "review this plan"
- "review this spec"
- "review this PRD"
- "review these requirements"
- "critique this design doc"
</trigger_phrases>
Fire automatically on a trigger phrase against a prose document, or on `/doc-review`. Auto-firing is permission to **evaluate**, not permission to fabricate — every finding still has to clear the evidence-quote and confidence-anchor floor below. A clean "nothing above the floor" is a valid, correct result.
<manual_override>`/doc-review [path]` reviews the named document, or lists candidates to choose from when no path is given. `--record` persists a review-record file and stages only it. `mode:headless` makes the run non-interactive (return structured findings, no questions, no record unless `--record`).</manual_override>
</auto_invoke>

## When to Apply / NOT

Apply when the user wants a **prose planning document** evaluated: a requirements doc, a plan, a spec, a PRD, a design doc, a brainstorm. The deliverable is findings — and, on request, one review-record file.

NOT:
- **Code review** → `review` (or `review-fix-grill-loop` for review→fix). `doc-review` reads prose, never a diff.
- **Docs↔code drift** (public docs/examples/versions stale against a code change) → `sync-docs`. That corrects docs to match code; `doc-review` evaluates the document's own quality, makes no edits.
- **Behavior-preserving code compression** → `simplify`.
- **Capturing a solved problem as a learning** → `autolearn`.

If the target is source code, stop and route to `review`. This skill does not open a diff.

## Support files — read on demand

Don't bulk-load these at start. Read each persona file only when that persona is selected, and paste its full content into that subagent's prompt. Each file is a self-contained lens: what it hunts, what it refuses to flag, its confidence anchors.

- `references/personas/coherence.md` — internal-consistency lens. Always-on. Owns the mechanically-fixable consistency findings (the safe-auto candidates).
- `references/personas/feasibility.md` — buildability lens. Always-on. Tightens to fundamental-rework gaps on requirements docs.
- `references/personas/product.md` — premise/strategy lens. Conditional. Also absorbs design/UX-shape concerns (cognitive load, adoption, workflow fit).
- `references/personas/security.md` — plan-level threat-surface lens. Conditional.
- `references/personas/scope-guardian.md` — right-sizing / earns-its-keep lens. Conditional.
- `references/personas/adversarial.md` — falsification / assumption-surfacing lens. Conditional.

## Workflow

### Phase 1 — Locate and classify by shape

Resolve the document. Prefer an explicit path. With none given, list the `.md` candidates from the likely homes and ask the user which one — never silently auto-pick, since reviewing the wrong document wastes the whole run:

```
fd -e md . docs/plans docs/ideation docs/brainstorms docs/specs 2>/dev/null
```

One match → confirm and proceed. Several → present them and let the user choose. Empty or missing → say so in one line and exit. Launch no agents.

Classify by **content shape, not path**. Path is a tie-breaker only — a plan-shaped doc under `docs/brainstorms/` is still a `plan`.

- **requirements** (what-to-build): `R#`/`A#`/`F#`/`AE#` IDs, `Actors`/`Key Flows`/`Acceptance Examples`/`Outstanding Questions` headings, problem/scope/success framing, no implementation units.
- **plan** (how-to-build): `U#` IDs, `Implementation Units`/`Key Technical Decisions`/`Risks & Dependencies` headings, per-unit `Goal`/`Files`/`Approach`/`Test scenarios`, repo-relative paths.
- **spec / prd**: a contract document — normative `MUST`/`SHALL`, interface/API definitions, invariants. Review as the closest of the two shapes above (interface-heavy → `plan`-grade feasibility; behavior/scope-heavy → `requirements`-grade).

Extract the `origin:` frontmatter value once (or the literal `none`). Pass classification + origin to every persona; personas adapt on them and do not re-classify.

When shape is genuinely ambiguous, default to `requirements` — the conservative classification that activates fewer plan-grade feasibility checks.

### Phase 2 — Select personas by signal

Always dispatch: **coherence** + **feasibility**.

Add conditional lenses only when the document carries the signal — spawning a lens the doc doesn't warrant manufactures noise:

| Persona | Activate when the document… |
|---|---|
| **product** | stakes a challengeable claim about what/why to build, ranks priorities, predicts user outcomes, OR carries strategic/positioning weight. Also activate on UI/UX/flow/cognitive-load signals (product owns the design-shape lens — adoption, workflow fit). |
| **security** | touches auth/authz, exposed endpoints, PII/payments/credentials/encryption, or third-party trust boundaries. |
| **scope-guardian** | has priority tiers (P0/P1/P2), >8 requirements or units, stretch/"future work" sections, or scope-boundary language misaligned with goals. |
| **adversarial** | is a requirements doc with 2+ challengeable claims, touches a high-stakes domain (auth/payments/migrations/compliance/crypto), proposes a new abstraction/framework, is a plan with `origin: none`, or extends scope beyond its origin. NOT on a routine plan derived from a validated origin that stays in scope. |

Announce the team and the one-line justification per conditional persona before dispatch.

### Phase 3 — Dispatch in parallel (read-only)

Launch every selected persona in **one parallel tool-call message**. Sequential dispatch breaks the parallel-launch contract. Each subagent is read-only — no Write, no Edit, no files; it returns findings text only.

Seed each subagent with: the full persona file content, the classification, the `origin:` value, the full document text, and this findings schema:

```
findings:
  - persona: <persona-name>
    section: <heading or line anchor in the reviewed doc>
    evidence: "<verbatim quote from the document>"
    issue: <one-line statement of the problem>
    suggested_fix: <one-line fix, or "" when judgment-only>
    confidence: 100 | 75 | 50
```

Pass the **full document** — never split into sections. An empty findings list is a valid return.

### Phase 4 — Confidence-anchored verdicts

Confidence is anchored, not a vibe slider. Personas emit only three values:

- **100** — provable from the document text alone (can quote two passages that contradict, or a named surface with no mitigation).
- **75** — likely to bite; full confirmation needs context outside the document. The normal working ceiling for premise/strategy/adversarial lenses.
- **50** — advisory; a real observation with no forcing consequence. Routes to FYI.

Anything a persona would score below 50 is **suppressed at the source**, not downgraded to FYI. Every finding at any anchor must carry a verbatim evidence quote — no quote, no finding.

### Phase 5 — Merge

1. **Validate** — drop any finding missing an evidence quote or a {100,75,50} anchor.
2. **Dedup** — fingerprint on `normalize(section) + normalize(issue)`; collapse duplicates across personas into one.
3. **Cross-persona agreement** — when two personas independently raise the same fingerprint, promote the merged finding one anchor step (50→75, 75→100). Corroboration earns confidence.
4. **Gate** — suppress everything below 50 after promotion.

### Phase 6 — Route by tier

Label every survivor. The tiers are **recommendations recorded in the report**, not edits applied to the document — this skill is read-only on the reviewed doc (see Constitutional Rules).

| Tier | Definition |
|---|---|
| **safe-auto** | Mechanical consistency fix at confidence 100, authoritative from the doc text (coherence-owned: header/body count mismatch, stale cross-ref, terminology drift, summary/detail contradiction). Safe for a writer to apply verbatim. |
| **gated-auto** | Confidence ≥75 with a concrete one-line `suggested_fix`. Apply on confirmation. |
| **manual** | Confidence ≥75 but the fix is a judgment call or tradeoff (premise, strategy, architecture decision). Needs a human decision. |
| **FYI** | Confidence 50 advisory. Surfaced as an observation, forces no decision. |

Present grouped by tier, highest first. In `mode:headless`, return the structured tiered list and stop — no questions, no record unless `--record`.

### Phase 7 — Review-record (only on request)

Default: report findings inline; write nothing. The reviewed document and the rest of the tree stay untouched.

On `--record` (or when the user asks to persist), write **one** file — `docs/reviews/<doc-slug>-review.md` — containing the tiered findings, the classification, and the persona roster. Then:

```
bat -P -p -n docs/reviews/<doc-slug>-review.md   # read back; confirm it landed
git add docs/reviews/<doc-slug>-review.md         # stage ONLY the record
```

Never `git add -A` / `git add .`. Never stage the reviewed document. Commit with `Op: extend` by the repo's normal flow.

## Constitutional Rules (Non-Negotiable)

Baseline wins on any conflict.

1. **Read-only on the reviewed document.** Never edit, write, or commit the document under review. Tiers are recorded recommendations, not in-place edits. Applying fixes is a separate handoff to a writer or the user.
2. **Only the orchestrator writes, and only the review-record.** Personas return findings text and write nothing — no Write, no Edit, no files.
3. **Evidence or it isn't a finding.** Every finding quotes the document verbatim. No quote → drop it in merge validation.
4. **Confidence is anchored.** Only 100/75/50. Below 50 is suppressed at the source, never relabeled FYI to keep it alive.
5. **Trigger is permission to evaluate, not fabricate.** If nothing clears the evidence + anchor floor, say so in one line and exit. Never invent findings to look thorough.
6. **Stage only the record.** When a record is written, `git add <that one path>` — never `-A`, never `.`, never the reviewed doc.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Document resolved | A single prose doc read; empty/missing → clean exit, no agents | Yes |
| Shape classified | `requirements`/`plan`/`spec`/`prd` decided by content shape; path used only as tie-breaker | Yes |
| Personas selected | coherence + feasibility always-on, plus justified conditionals; design-shape signals routed to product | Yes |
| Parallel dispatch | All selected personas launched in one batch, read-only, schema-bound | Yes |
| Evidence present | Every finding carries a verbatim document quote; unquotable findings dropped | Yes |
| Confidence anchored | Each finding ∈ {100,75,50}; sub-50 suppressed, not relabeled | Yes |
| Merge applied | Validate → dedup by fingerprint → cross-persona promotion → sub-50 gate | Yes |
| Tier routed | Every survivor labeled safe-auto / gated-auto / manual / FYI | Yes |
| Read-only honored | Zero writes/edits to the reviewed document | Yes |
| Record discipline | If a record is written: only that path written, read back, staged alone; never `git add -A` | Yes when `--record` |

## Anti-patterns

- **Editing the reviewed doc.** Even a safe-auto fix is a recommendation here, not an edit. Applying it breaks the read-only invariant.
- **`git add -A` after writing the record.** Stage the one record path; nothing else.
- **Classifying by path.** A brainstorm-shaped doc under `docs/plans/` is requirements. Shape decides.
- **Spawning every persona.** Conditional lenses fire on signal. A lens the doc doesn't warrant manufactures noise.
- **Findings without a quote.** Unquotable means unverifiable means suppressed.
- **Downgrading a sub-50 to FYI to keep it.** Below the floor is suppressed, not parked.
- **Fabricating findings to look thorough.** A clean review is a valid result; say so in one line.
- **Reviewing code.** A diff is `review`'s job; doc↔code drift is `sync-docs`.

## Disambiguation / See also

- **vs `review`** — `review` reads a code diff and critiques source. `doc-review` reads a prose planning document and never opens a diff.
- **vs `sync-docs`** — `sync-docs` corrects public docs/examples/versions to match a code change (docs↔code drift) and edits docs. `doc-review` evaluates a planning document's own quality and edits nothing.
- **vs `review-fix-grill-loop`** — that loops review→resolve→fix over a code change-set with auto-revert. `doc-review` is read-only, single-pass over one prose document, and applies no fixes.
- **vs `autolearn`** — `autolearn` writes a net-new learning doc from a solved problem. `doc-review` critiques an existing planning doc.
