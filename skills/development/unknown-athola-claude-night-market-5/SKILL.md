---
name: harden
description: 'Active codebase hardening with NIST/CWE-cited checks for Python and Rust. Composes existing reviews; proposes concrete remediations.'
globs: "**/*.{py,rs,toml,yaml,yml,sh}"
alwaysApply: false
category: security
tags:
- security
- hardening
- nist
- supply-chain
- python
- rust
- cwe
tools: []
provides:
  governance:
  - hardening-report
  - remediation-proposal
  security:
  - vuln-detection
  - hardening-posture
usage_patterns:
- security-hardening
- quarterly-posture-audit
- pre-release-security-gate
complexity: advanced
model_hint: deep
estimated_tokens: 1100
progressive_loading: true
dependencies:
- pensive:safety-critical-patterns
- pensive:rust-review
- pensive:bug-review
- pensive:tiered-audit
- pensive:blast-radius
- leyline:supply-chain-advisory
- leyline:authentication-patterns
- leyline:content-sanitization
- abstract:hook-authoring
- imbue:proof-of-work
modules:
- modules/nist-controls.md
- modules/python-checks.md
- modules/rust-checks.md
- modules/cross-cutting.md
- modules/frontier-checks.md
- modules/proposal-shape.md
---

# Harden Codebase Skill

Active security hardening — scan the existing repository for
vulnerabilities and forward-facing threats, then propose concrete
remediations the user can approve, defer, or file.

This skill is the engine behind `/harden`. It complements the
Claude Code built-in `/security-review` (which scans the pending
diff) by sweeping the whole repository against citation-backed
checks rather than line-level review of in-flight code.

## When To Use

- Quarterly security-posture audits.
- Before tagging a release that touches sensitive code paths.
- After a published advisory affects the language ecosystem.
- When onboarding a new repository and want a baseline.
- After integrating a new dependency or upstream service.

## When NOT To Use

- Pending-diff review on a single PR. Use `/security-review`.
- Architecture-level threat modeling. Use `attune:war-room`
  with a security-focused panel.
- Cryptographic protocol review. The skill flags suspect crypto
  but does not propose protocol fixes (specialist work).
- One-off bug hunting. Use `pensive:bug-review`.

## Required TodoWrite Items

1. `harden:discovery` — inventory languages, build files, hooks,
   CI workflows
2. `harden:scan-python` — run python-checks.md detectors when
   Python is present
3. `harden:scan-rust` — run rust-checks.md detectors when Rust
   is present
4. `harden:scan-cross-cutting` — run cross-cutting.md detectors
   (deps, secrets, SBOM, CI)
5. `harden:scan-frontier` — run frontier-checks.md (PQC, LLM
   supply chain, sandboxing)
6. `harden:nist-mapping` — map findings to NIST SSDF practices
7. `harden:proposals` — for each finding above the threshold,
   draft a concrete remediation per `modules/proposal-shape.md`
8. `harden:approval-gate` — present proposals to the user for
   apply / file / defer / reject
9. `harden:apply-and-validate` — apply approved proposals as
   discrete commits, re-run gates, capture evidence
10. `harden:report` — write `reviews/harden-<date>.md` and
    optionally post to Discussions

## Progressive Loading

Load modules based on what the discovery step finds.

| Detected | Load |
|----------|------|
| Python files (`*.py`, `pyproject.toml`) | `modules/python-checks.md` |
| Rust files (`*.rs`, `Cargo.toml`) | `modules/rust-checks.md` |
| Any | `modules/nist-controls.md` (citation backbone) |
| Any | `modules/cross-cutting.md` (deps, secrets, CI) |
| LLM SDK use (`anthropic`, `openai`), MCP server, post-quantum surface | `modules/frontier-checks.md` |
| Any with proposals enabled | `modules/proposal-shape.md` |

The module hub keeps the SKILL.md itself under the
`estimated_tokens: 1100` budget. Detail lives in the modules.

## Core Workflow

### Phase 1 — Discovery

Inventory the repo without modifying anything:

```bash
# Languages and build files
find . -type f \( -name '*.py' -o -name '*.rs' -o -name '*.sh' \) \
  | head -200 > /tmp/harden-langs.txt

# Build manifests
ls pyproject.toml Cargo.toml package.json go.mod 2>/dev/null

# CI workflows and pre-commit
ls .github/workflows/ .pre-commit-config.yaml 2>/dev/null

# Hooks and Dockerfiles
find . -path ./node_modules -prune -o -type f \
  \( -name 'hooks.json' -o -name 'Dockerfile*' \) -print
```

Dispatch `/discovery-prefilter` if the repo has > 5000 source files
to bound the scan.

### Phase 2 — Citation-backed scan

For each detected language, load the matching module and run its
detector list. Each detector outputs findings with the schema
defined in `modules/proposal-shape.md`. The citation column is
mandatory: a finding without a NIST/CWE reference is downgraded
to "advisory" and not eligible for active proposal.

### Phase 3 — NIST mapping

Group findings by SSDF practice (PW.4, PW.8, RV.1, etc.) and CWE
ID. The mapping table lives in `modules/nist-controls.md`. The
report's executive summary references SSDF practice coverage so
the audit is comparable across runs.

### Phase 4 — Proposal generation

For each finding above the configured severity threshold, draft a
concrete remediation per `modules/proposal-shape.md`:

- Specific files and lines touched
- Diff or config snippet (not "consider doing X")
- Blast-radius assessment via `pensive:blast-radius`
- Reversal plan: how to revert if the change breaks behavior
- Test that should pass after the change

### Phase 5 — Approval gate

Present proposals one at a time via `AskUserQuestion`. Default
options: **apply**, **file as issue**, **defer to backlog**,
**reject**. Auto-apply is opt-in via the `--auto-apply` flag and
respects a per-finding severity threshold.

### Phase 6 — Apply and validate

Apply each approved proposal as a discrete commit:

```bash
git add <touched files>
git commit -m "harden: <finding-id> <one-line summary>"
```

After each apply, re-run the project gates:

```bash
make test --quiet && make lint && make type-check
```

If a gate fails, revert the commit (`git revert HEAD --no-edit`)
and downgrade the finding to "needs human design."

### Phase 7 — Report

Write `reviews/harden-<date>.md` with:

- Executive summary (SSDF practice coverage, CWE distribution)
- Findings table grouped by severity
- Per-finding detail: detection signal, citation, proposal, status
- Disposition table (applied / filed / deferred / rejected)
- Re-run instructions

If running inside a PR context, post the executive summary as a
comment via `abstract:post_review_insights`.

## Severity Classification

| Severity | Definition | Default disposition |
|----------|------------|---------------------|
| **CRITICAL** | Active exploit path, RCE, credential leak | apply or file immediately |
| **HIGH** | Plausible exploit, missing defense-in-depth on attack surface | propose for apply |
| **MEDIUM** | Best-practice gap, hardening opportunity | propose for apply with `--auto-apply medium` |
| **LOW** | Style/documentation gap with security flavor | file as issue |
| **ADVISORY** | Pattern detected without exploit narrative | report only |

## Output Format

```markdown
# Hardening Report — <date>

## Executive Summary

- Codebase: <repo> @ <sha>
- Languages scanned: Python (X files), Rust (Y files)
- NIST SSDF practices covered: PW.4, PW.7, PW.8, RV.1, RV.2
- CWE Top 25 hits: <count> across <distinct CWEs>
- Disposition: <N> applied, <N> filed, <N> deferred, <N> rejected

## Findings

| ID | Severity | Citation | File:Line | Disposition |
|----|----------|----------|-----------|-------------|
| H1 | CRITICAL | CWE-502, NIST SSDF PW.7 | `src/x.py:45` | applied (commit abc123) |
| H2 | HIGH | CWE-89, NIST SSDF PW.4 | `src/y.py:120` | filed (#456) |

## Per-finding detail

### H1 — Unsafe deserialization

**Citation:** CWE-502 (Deserialization of Untrusted Data),
NIST SSDF PW.7 (Review and analyze human-readable code).

**Detection signal:**
- File: `src/x.py:45`
- Pattern: <module>.loads(user_supplied_input)
- Reachability: untrusted, comes from request body

**Proposal:** ...

**Blast radius:** ...

**Reversal plan:** ...
```

## Safety Rails

- **Never apply without approval.** Even with `--auto-apply`,
  CRITICAL findings always prompt.
- **One finding per commit.** Reversals are per-finding, not
  per-batch.
- **Re-run gates after each apply.** A gate failure reverts the
  commit and downgrades the finding.
- **Citation is mandatory.** Findings without a NIST/CWE/RustSec
  reference are advisory only and skip the apply phase.
- **Read-only on first run.** First invocation defaults to
  `--report-only` until the user has reviewed at least one
  report and explicitly opts into proposals.

## Integration

The skill composes (rather than re-implements):

- `pensive:rust-review` — full Rust audit when Rust is present
- `pensive:bug-review` — bug-hunting backbone
- `pensive:safety-critical-patterns` — NASA Power-of-10 adapted
- `pensive:tiered-audit` — three-tier discipline (`--tier 1/2/3`)
- `pensive:blast-radius` — change-impact assessment for proposals
- `leyline:supply-chain-advisory` — dependency posture
- `leyline:authentication-patterns` — auth/credential review
- `leyline:content-sanitization` — input handling
- `abstract:hook-authoring` — hook-event security
- `imbue:proof-of-work` — evidence discipline for findings

## Exit Criteria

- [ ] Discovery output lists every language and build manifest
      detected in the repo.
- [ ] Each finding carries a CWE or NIST SSDF citation; the
      report executive summary lists the SSDF practice coverage.
- [ ] Each finding above the severity threshold has a concrete
      proposal (file, diff or config snippet, blast radius,
      reversal plan, expected-passing test).
- [ ] No proposal was applied without explicit user approval
      (or without an `--auto-apply` flag covering its severity).
- [ ] Each applied proposal is its own commit, reversal-friendly.
- [ ] After every apply, the project gates were re-run; any
      gate failure reverted the commit and downgraded the
      finding.
- [ ] `reviews/harden-<date>.md` exists and lists every finding
      with a disposition (applied / filed / deferred / rejected /
      advisory).
