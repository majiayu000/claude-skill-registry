---
name: ce-release-check
description: >
  Read release-plan state and select the next ADR-compliant actionable development
  step.
---

# CE Release Check

You are determining the next development step from the release plan.
This skill implements the "proceed according to plan" workflow defined in
`execution-plan.instructions.md`.

**Mandatory sequence:**
1. Read `docs/improvement/RELEASE_PLAN_v1.md`.
2. Identify the current released version and the target next milestone.
3. List outstanding gates and work items for that milestone.
4. Verify that the proposed next step is allowed by all relevant ADRs.
5. If an ADR constraint and a plan step conflict, the ADR wins.

---

## Files to read

```
docs/improvement/RELEASE_PLAN_v1.md   ← primary source: current version, milestones, gates
docs/improvement/adrs/                ← governance constraints (ADR takes precedence)
CHANGELOG.md                          ← completed items; do not duplicate
```

---

## Step 1 — Identify current state

```markdown
Current released version: v<X.Y.Z>   (from RELEASE_PLAN_v1.md top section)
Target next milestone:    v<X.Y.Z+1>
```

---

## Step 2 — Scan open gates for the target milestone

Look for sections like:
```
### v0.11.0 — <milestone name>
#### Gates
- [ ] ADR-NNN gap <description>
- [x] (already closed)
```

Gates marked `[ ]` are outstanding. List them with their ADR reference.

---

## Step 3 — Cross-reference ADRs

For each outstanding gate, identify the governing ADR(s) using `ce-adr-consult`.
If the proposed work from the plan conflicts with an ADR decision, **stop** and
flag the conflict rather than proceeding.

---

## Step 4 — Select the next actionable item

Priority order:
1. **Blocking gates** — items explicitly labeled as release blockers.
2. **Open ADR implementation gaps** — items in the ADR roadmap summary with open status.
3. **Non-gate improvements** — feature additions scheduled for the milestone.

---

## Step 5 — Verify against CHANGELOG

```bash
# Check what was delivered recently
head -100 CHANGELOG.md
```

Do not propose work that is already present in `CHANGELOG.md`.

---

## Output format

```
Release Check: <date>
======================
Current released version:  v<X.Y.Z>
Target next milestone:      v<X.Y.Z+1>

Outstanding gates:
  1. [ADR-NNN] <brief description>
  2. [ADR-NNN] <brief description>
  ...

Next actionable step:
  Work item: <title>
  ADR(s):    ADR-NNN (Decision section: <binding rule>)
  Plan ref:  RELEASE_PLAN_v1.md § <section>
  Rationale: <one sentence>

ADR conflicts detected: NONE | <list if any>
```

---

## Completing a work item (CHANGELOG update)

When an item is completed satisfactorily, add it to `CHANGELOG.md` under
the appropriate section header:

```markdown
## [Unreleased]

### Added
- Implemented `to_primitive` / `from_primitive` calibrator serialization (ADR-031).

### Fixed
- ...
```

---

## Quick reference: upcoming milestone summary (v0.11.x)

Based on `RELEASE_PLAN_v1.md` (verify current status in the file):

| ADR | Outstanding work | Target |
|---|---|---|
| ADR-004 | `ParallelFacade` → `ParallelExecutor` name alignment (docs) | v0.11.0 |
| ADR-005 | Strict payload validator + fixtures | v0.11.1 |
| ADR-006 | `PluginManager` shell, over-scoped surface cleanup | v0.11.0 |
| ADR-008 | Domain-model hardening | v0.11.1 |
| ADR-020 | Release checklist + legacy API audit workflow | v0.11.0 |
| ADR-026 | Strict invariant enforcement + immutability | v0.11.0 |
| ADR-028 | Enforcement tooling + examples | v0.11.1 |
| ADR-030 | Determinism / assertion checks in CI | v0.11.0 |
| ADR-031 | `to_primitive` / `from_primitive` + `save_state` / `load_state` | v0.11.x |
| ADR-033 | Metadata contract (v0.11.0); CLI/shims (v0.11.1) | v0.11.0–v0.11.1 |

---

## Evaluation Checklist

- [ ] `RELEASE_PLAN_v1.md` read before proposing any step.
- [ ] Current version and target milestone clearly identified.
- [ ] Outstanding gates listed with ADR references.
- [ ] No ADR constraint violated by the proposed next step.
- [ ] `CHANGELOG.md` checked to avoid duplicate work.
- [ ] Completed items added to `CHANGELOG.md` under `[Unreleased]`.
