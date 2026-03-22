---
name: lp-launch-qa
description: Pre-launch quality assurance gate for startup loop (S9B). Validates conversion flows, SEO technical readiness, performance budget, and legal compliance before a site goes live.
---

# Launch QA Gate

Pre-launch quality assurance gate (S9B). Audits 6 domains in parallel and produces a go/no-go decision backed by evidence before any site goes live or experiment launches.

## Invocation

```
/lp-launch-qa --business <BIZ> [--domain conversion|seo|performance|legal|brand-copy|measurement|security|all]
```

**Arguments:**
- `--business`: Business unit code (`BRIK`, `PLAT`, `PIPE`, `BOS`)

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

- `--domain`: Optional scope filter. Default: `all`

**Fast path examples:**
```
/lp-launch-qa --business BRIK
/lp-launch-qa --business PIPE --domain conversion
/lp-launch-qa --business BRIK --domain seo
```

**When to use:** After `/lp-do-build` completes (DO); before `/lp-launch` (S10) or any experiment driving external traffic; as a periodic health check on live production sites.

**When NOT to use:** During development; for non-customer-facing internal tools; as a replacement for `/lp-do-plan` validation contracts.

## Operating Mode

**AUDIT + GATE (read-only)**

**Allowed:** Read deployed site; run automated checks (Lighthouse, crawler, smoke tests); read config files (analytics IDs, sitemap, robots.txt, legal doc paths); inspect network requests; read source code.

**Not allowed:** Code changes, config changes, deployments, destructive commands, committing fixes.

**Commits allowed:** QA report artifact (`docs/business-os/site-upgrades/<BIZ>/launch-qa-report-YYYY-MM-DD.md`); startup loop checkpoint update (`docs/business-os/startup-baselines/<BIZ>/loop-state.json`).

## Inputs

- `--business` (required) and `--domain` (optional, default `all`)
- Site baseline: `docs/business-os/site-upgrades/<BIZ>/latest.user.md`
- Platform capability baseline: `docs/business-os/platform-capability/latest.user.md`
- Startup loop state: `docs/business-os/startup-baselines/<BIZ>/loop-state.json`

**If baseline/loop-state is missing:** STOP — "Baseline missing. Run `/lp-do-fact-find` with `Startup-Deliverable-Alias: website-upgrade-backlog` to create site baseline before launch QA."

## Workflow

### 1) Intake and discovery

**1a) Validate arguments** — confirm `--business` valid; confirm `--domain` is one of: `conversion`, `seo`, `performance`, `legal`, `brand-copy`, `measurement`, `all`.

**1b) Locate site baseline and loop state** — read `latest.user.md` for deployment URL, analytics config, conversion flows, legal doc paths; read loop state to confirm DO (`/lp-do-build`) complete. If DO (`/lp-do-build`) incomplete: STOP — "Build incomplete. Complete `/lp-do-build` (DO) tasks before running launch QA."

**1c) Identify deployment target** — staging URL for pre-launch; production URL for health check. Default to staging unless user specifies production.

**1d) Read platform capability baseline** — confirm analytics platform, SEO infrastructure, performance baseline expectations.

### 2) Execute domain checks

**If `--domain all`** (default): dispatch all 8 domain modules simultaneously via Task tool in a SINGLE message. Load `modules/report-template.md` for output format.

Protocol: `_shared/subagent-dispatch-contract.md` (Model A — domain subagents run read-only audit checks; orchestrator aggregates results).

Dispatch brief per domain subagent:
- Load `modules/domain-<name>.md` for check definitions
- Perform all checks; collect evidence
- Return: `{ domain: "<name>", status: "pass|fail|warn", checks: [{ id, status, evidence }] }`
- `touched_files`: [] (audit-only — no file writes)

Await all 7 completions. If a domain subagent returns `status: fail` (unrecoverable error — not a failing check): quarantine per dispatch contract §5; flag domain as incomplete in report.

**If `--domain <X>`** (single domain): load only `modules/domain-<X>.md`; run checks without dispatching subagents.

Domain modules:
- `modules/domain-conversion.md` — C1–C5
- `modules/domain-seo.md` — S1–S6
- `modules/domain-performance.md` — P1–P5
- `modules/domain-legal.md` — L1–L6
- `modules/domain-brand-copy.md` — BC-04, BC-05, BC-07
- `modules/domain-measurement.md` — M1–M7
- `modules/domain-security.md` — SEC-01–SEC-08
- `modules/domain-data-hardening.md` — DH-01–DH-07 (dispatches `/lp-do-data-audit`)

### 3) Cross-domain synthesis

**MANDATORY — do not skip.**

Scan all domain verdict objects for:
- Cross-domain failure patterns (e.g., analytics not firing may indicate both a Conversion failure AND a Measurement failure)
- Conflicting signals between domains
- Shared root causes across multiple domain failures

Document synthesis findings in the report under "Cross-Domain Analysis" before emitting go/no-go.

### 4) Aggregate go/no-go decision

Validate that all 8 domain verdicts are received before emitting. Then:
- **GO**: all blocker checks pass; warnings documented for follow-up
- **NO-GO**: one or more blocker checks fail

**Blocker vs. warning severity:**
- **Blocker:** Any failure in Conversion or Legal; Performance P1–P3 failures; Measurement M1, M2, or M7 failures; Security domain `status: fail` (any of SEC-01–SEC-05, SEC-07, SEC-08 [high/critical CVE], or SEC-06 [unauthenticated access to private route]); Data Hardening domain `status: fail` (any CRITICAL or HIGH finding from `/lp-do-data-audit`)
- **Warning:** SEO failures; Performance P4–P5; all Brand Copy failures (GATE-BD-06b Warn); Measurement M3, M5, M6; all DV-series delayed checks; Security `status: warn` (SEC-06 missing rate-limiting when auth is correct; SEC-08 moderate/low CVEs only); Data Hardening MEDIUM/LOW findings only
- **Existing-site gap advisory (non-blocking):** M1/M2 failure where S1B was not run → recommend `measurement-quality-audit-prompt.md`

### 5) Write QA report

Use `modules/report-template.md` as output structure. Write to:
`docs/business-os/site-upgrades/<BIZ>/launch-qa-report-YYYY-MM-DD.md`

Update `docs/business-os/startup-baselines/<BIZ>/loop-state.json` (S9B checkpoint: `complete` if GO, `blocked` if NO-GO). Commit both artifacts.

## Quality Checks

A launch QA run is complete only if:
- [ ] All invocation arguments validated
- [ ] Site baseline and loop state located (or missing baseline reported as blocker)
- [ ] Deployment URL identified and accessible
- [ ] All selected domain checks executed (no checks skipped without documented reason; data hardening domain runs `/lp-do-data-audit` and awaits its PASS/FAIL verdict)
- [ ] Each check result includes pass/fail + evidence
- [ ] Cross-domain synthesis completed before go/no-go
- [ ] Blocker vs. warning severity correctly assigned
- [ ] Go/no-go decision matches blocker count
- [ ] QA report artifact written with all required sections
- [ ] Loop state updated (if applicable)
- [ ] QA report committed to repo
