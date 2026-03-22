---
name: lp-coverage-scan
description: Coverage gap scanner for startup loop. Reads a business coverage manifest, scans the repo and known integrations for actual artifact/data-source state, classifies gaps as CRITICAL/MAJOR/MINOR, writes a gap report, and emits dispatch packets to queue-state.json for all CRITICAL and MAJOR gaps.
---

# Coverage Scan Orchestrator

`/lp-coverage-scan` is the scan and emission layer for startup loop coverage gap detection.

This skill does four things:
1. Read coverage manifest from `docs/business-os/strategy/<BIZ>/coverage-manifest.yaml`
2. Scan repo and known integration paths for each domain entry via `modules/scan-phase.md`
3. Classify gaps as CRITICAL/MAJOR/MINOR and produce a human-readable gap report
4. Emit dispatch packets for CRITICAL/MAJOR gaps to queue-state.json via `modules/emit-phase.md`

Keep this file thin. Do not embed scan rules, classification rubrics, or dispatch templates here.

## Invocation

```
/lp-coverage-scan --biz <BIZ> [--as-of-date <YYYY-MM-DD>] [--dry-run]
```

### Parameters

| Parameter | Required | Default | Notes |
|---|---|---|---|
| `--biz` | Required | — | Business identifier (e.g. `BRIK`, `PWRB`). Must match a directory under `docs/business-os/strategy/`. |
| `--as-of-date` | Optional | Today (YYYY-MM-DD) | Date used for artifact naming and staleness calculation. |
| `--dry-run` | Optional | — | When present: write gap report but skip all queue-state.json writes. Safe read-only mode for verifying scan behavior. |

## Global Invariants

### Operating mode

**SCAN + EMIT**

### Allowed actions

- Read strategy artifact files, frontmatter, and file mtimes (read-only scan)
- Read `docs/business-os/strategy/<BIZ>/coverage-manifest.yaml`
- Write gap report to `docs/business-os/strategy/<BIZ>/coverage-scan-<YYYY-MM-DD>.md`
- Write dispatch packets to `docs/business-os/startup-loop/ideas/trial/queue-state.json` (with writer lock only; see constraint below)
- Run `scripts/agents/with-writer-lock.sh` to acquire writer lock before any queue writes

### Prohibited actions

- Code changes, refactors, or production data modifications
- Destructive shell or git commands
- Writing to queue-state.json without first acquiring writer lock via `scripts/agents/with-writer-lock.sh`
- Running any scan or emitting any dispatch when no manifest exists (`preflight` fail-closed; see below)
- Skipping the dry-run flag when the operator passes it — must respect `--dry-run` and never write to queue-state.json in dry-run mode

## Inputs

| Input | Source | Notes |
|---|---|---|
| Coverage manifest | `docs/business-os/strategy/<BIZ>/coverage-manifest.yaml` | Required; preflight fails if missing |
| Strategy artifacts | `docs/business-os/strategy/<BIZ>/` | Scanned per `artifact_path_patterns` in manifest |
| Integration config | Various locations (see scan-phase.md) | Stripe, Firebase, GA4, Octorate |
| Queue state | `docs/business-os/startup-loop/ideas/trial/queue-state.json` | Written (appended) by emit-phase; never overwritten |

## Module Routing

Execute phases in sequence:

1. **Preflight** — validate manifest exists and is readable; fail-closed if not (see Preflight Gate below)
2. **`modules/scan-phase.md`** — read manifest; scan artifact directories; check data connections; produce gap classification table
3. **`modules/emit-phase.md`** — write gap report artifact; emit CRITICAL/MAJOR dispatches to queue-state.json (skipped entirely on `--dry-run`)

## Preflight Gate

If `docs/business-os/strategy/<BIZ>/coverage-manifest.yaml` does not exist, stop immediately with:

```
Error: No coverage manifest found for <BIZ>.
Expected path: docs/business-os/strategy/<BIZ>/coverage-manifest.yaml
Create a manifest from the template at docs/plans/coverage-manifest-scan-core/coverage-manifest.template.yaml before running lp-coverage-scan.
```

Additional preflight checks:

- If `--biz` argument is missing or no matching strategy directory exists: `Error: No strategy directory found for business <BIZ>. Run from repo root.`

## Output Paths

- **Gap report**: `docs/business-os/strategy/<BIZ>/coverage-scan-<YYYY-MM-DD>.md` — written every run (dry-run and live)
- **Queue dispatches**: `docs/business-os/startup-loop/ideas/trial/queue-state.json` — appended (live runs only; skipped on `--dry-run`)

## Dry-Run Mode

When `--dry-run` is active:

- Scan phase runs normally
- Gap report is written (always safe — no queue impact)
- emit-phase skips all queue-state.json writes and count updates
- Gap report header includes: `[DRY RUN — no dispatches emitted]`
