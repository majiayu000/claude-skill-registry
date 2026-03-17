---
name: ideas-readiness
description: Readiness gate for idea generation. Use before /ideas-go-faster, or whenever plans/context may be stale. Audit business-plan freshness, outcome clarity, code-to-plan traceability, and required tooling/data availability; fail closed on critical gaps; ask targeted questions to collect missing information and update source docs before allowing idea generation.
---

# Ideas Readiness

Run a fail-closed readiness audit before generating ideas. Do not run `/ideas-go-faster` until critical readiness gaps are closed.

## Invocation

```bash
/ideas-readiness
/ideas-readiness --scope=BRIK
/ideas-readiness --max-age-days=21
```

Notes:
- `--scope=<BIZ>` limits checks to one business; default is all active businesses.
- `--max-age-days` controls staleness threshold; default is `21`.

## Operating Mode

**READ + AUDIT + QUESTION + DOCUMENT UPDATE**

Allowed:
- Read plans, cards, sweeps, and people profiles.
- Audit working-tree changed code paths for business mapping.
- Ask targeted clarification questions to close gaps.
- Update source docs and produce readiness artifacts.

Not allowed:
- Run idea generation while hard blockers exist.
- Mark a business as ready when outcomes are undefined.

## Inputs

Required files:
- Business plans: `docs/business-os/strategy/<BIZ>/plan.user.md`
- People profiles: `docs/business-os/people/people.user.md`
- Maturity model: `docs/business-os/strategy/business-maturity-model.md`
- Current cards/ideas context: `docs/business-os/cards/`, `docs/business-os/ideas/`
- Last sweep context: `docs/business-os/sweeps/`

Optional but recommended:
- Path-to-business mapping registry: `docs/business-os/readiness/path-business-map.user.yaml`

## Readiness Gates

Evaluate each gate per business. Gate status is `pass`, `warning`, or `block`.

| Gate | What to detect | Block condition |
|---|---|---|
| `RG-01 Freshness` | Plan/profile currency | `Last-reviewed` older than max-age-days and no current update note |
| `RG-02 Outcome Clarity` | Current outcomes are explicit and measurable | No active outcome with full outcome contract fields |
| `RG-03 Business-vs-Code Balance` | Plan is not implementation-only | Current focus is mostly code/tasks with no business result statement |
| `RG-04 Code-to-Plan Traceability` | Changed code maps to business outcomes | Changed paths have no business/outcome mapping or explicit park/delete decision |
| `RG-05 Tooling/Data Prereqs` | Required measurement/decision tools are in place | Missing critical tool/data source that makes idea generation speculative |
| `RG-06 Decision Context` | Constraints and assumptions are explicit | Unknown current constraint, owner, or decision-to-unlock for the business |

### RG-02 Outcome Contract (mandatory)

A business is not ready unless at least one active current-period outcome includes:
- `Outcome`: result to achieve
- `Baseline`: current value/state
- `Target`: desired value/state
- `By`: deadline/date window
- `Owner`: accountable person
- `Leading Indicators`: weekly signal(s)
- `Decision Link`: which priority decision this outcome unlocks

If any field is missing, `RG-02 = block`.

## Workflow

### Stage 1: Scope and Source Discovery

1. Determine businesses in scope.
2. Load required source files.
3. Resolve `max-age-days` (default `21`).

### Stage 2: Gate Audit Per Business

For each business:
1. Run `RG-01` through `RG-06`.
2. Capture evidence pointers (file path + line references where possible).
3. Record gate verdict and reason.

### Stage 3: Code-to-Plan Traceability Audit

1. Read changed paths from `git status --short`.
2. For each changed path under `apps/`, `packages/`, `scripts/`, `docs/`:
   - Map to business using `path-business-map.user.yaml` if present.
   - Verify mapped business has an active outcome and explicit decision link.
3. Any unmapped path or unmapped decision impact is a `RG-04 block` until resolved.

If mapping registry is missing, create it and treat unknown mappings as blockers until confirmed.

### Stage 4: Blocker-First Question Cycle

If any `block` exists:
1. Do **not** run idea generation.
2. Ask targeted questions (max 3 at a time), prioritized by decision impact.
3. Wait for answers.
4. Update source docs directly.
5. Re-run gates.

Question style:
- Short, concrete, answerable in one response.
- Ask for measurable outcomes, owners, and dates.
- Ask for explicit mapping when code has no business-plan linkage.

### Stage 5: Produce Readiness Artifacts

Write:
- `docs/business-os/readiness/<YYYY-MM-DD>-ideas-readiness.user.md`
- `docs/business-os/readiness/<YYYY-MM-DD>-missing-context-register.user.md`

## Question Playbook

Use these prompts when gaps are detected.

### Missing outcomes (`RG-02`)

For each business with outcome gaps:
1. What is the single most important outcome for the next period?
2. What is the current baseline and target value?
3. By what date must this be achieved?
4. Who owns it?
5. What weekly leading indicator proves progress?
6. Which decision does this outcome unlock?

### Plan is code-only (`RG-03`)

1. Which business result does this implementation work produce?
2. How will we measure whether it worked?
3. What happens if this work is delayed 30 days?

### Orphan code paths (`RG-04`)

1. Which business does `<path>` serve?
2. Which current outcome does it support?
3. If none, choose one:
   - park it,
   - delete it,
   - define a new outcome and owner.

### Missing tooling/data (`RG-05`)

1. Which tool/data source is missing?
2. Who owns implementing it and by when?
3. What interim proxy metric will be used until it exists?

## Readiness Report Contract

`<YYYY-MM-DD>-ideas-readiness.user.md` must include:
1. Run status: `ready` or `blocked`
2. Scope and staleness threshold used
3. Gate table per business (`RG-01..RG-06`)
4. Hard blockers with evidence
5. Warnings with evidence
6. Questions asked and answers received
7. Exact docs updated
8. Go/No-go statement for `/ideas-go-faster`

`<YYYY-MM-DD>-missing-context-register.user.md` must include:
- Gap ID, business, gate, missing info, owner, due date, status

## Hard Stop Rule

If any business has one or more `block` gates, output exactly:

> "Readiness status: BLOCKED. Do not run `/ideas-go-faster` until listed blockers are resolved."

If all businesses pass (warnings allowed), output:

> "Readiness status: READY. `/ideas-go-faster` may run with listed warnings acknowledged."

## Red Flags (invalid readiness output)

A readiness run is invalid if any of these occur:
1. Marks READY while any block remains open.
2. Accepts implementation-only plans without outcome fields.
3. Ignores changed code paths that are unmapped to business outcomes.
4. Omits evidence pointers for blocker claims.
5. Runs idea generation despite a block verdict.

## Integration Contract with Ideas Generation

Before running `/ideas-go-faster`:
1. Run `/ideas-readiness`.
2. If status is `BLOCKED`, stop and close gaps first.
3. If status is `READY`, proceed to `/ideas-go-faster`.
4. Treat readiness reports older than 24 hours as stale for active planning days; re-run readiness.
