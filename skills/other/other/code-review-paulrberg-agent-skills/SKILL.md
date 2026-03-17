---
argument-hint: '[--fix]'
disable-model-invocation: false
name: code-review
user-invocable: true
description: This skill should be used when the user asks to "review code", "review PR", "code review", "audit code", "check for bugs", "security review", "review my changes", "find issues in this code", "review the diff", or asks for pull request review or code audit.
---

# Code Review

## Objective

Find high-impact defects in changed code with evidence. Prioritize security, correctness, and regressions over style nits.

## Arguments

- `--fix`: After reporting findings, apply all suggested fixes automatically in severity order (`CRITICAL -> HIGH -> MEDIUM -> LOW`), then rerun targeted checks and report exactly what changed.
- Default: Report findings and wait for confirmation before editing.

## Scope Resolution

1. Verify repository context: `git rev-parse --git-dir`. If this fails, stop and tell the user to run from a git repository.
2. If user provides file paths/patterns or a commit/range, scope is exactly those targets.
3. Otherwise, scope is **only** session-modified files. Do not include other uncommitted changes.
4. If there are no session-modified files, fall back to all uncommitted tracked + untracked files:
   - tracked: `git diff --name-only --diff-filter=ACMR`
   - untracked: `git ls-files --others --exclude-standard`
   - combine both lists and de-duplicate.
5. Exclude generated/low-signal files unless requested: lockfiles, minified bundles, build outputs, vendored code.
6. If scope still resolves to zero files, report and stop.

## Workflow

1. Resolve scope and read diffs plus minimal surrounding context.
2. Classify files by domain/risk.
3. Load `references/profiles/core.md` plus only the domain profiles that match the current diff.
4. Generate findings with: location, impact, evidence, confidence, and concrete fix.
5. Assign severity with the model below.
6. Default behavior: report and wait.
7. With `--fix`: apply all suggested fixes in severity order, then run targeted verification.
8. Report using `references/output-schema.md`.

## Profile Dispatch

- `references/profiles/security.md`: auth, external input, secrets, crypto, public network surfaces, unsafe parsing.
- `references/profiles/configuration.md`: env/config, timeouts, retries, pools, limits, resource tuning, rollout controls.
- `references/profiles/typescript-react.md`: TypeScript/JavaScript/React/Node files.
- `references/profiles/python.md`: Python services, scripts, async workloads.
- `references/profiles/shell.md`: shell scripts, CI command blocks, deployment scripts.
- `references/profiles/smart-contracts.md`: Solidity/Solana/on-chain protocol code.
- `references/profiles/data-formats.md`: CSV/JSON/YAML/binary ingestion/export/parsing.
- `references/profiles/naming.md`: naming/intent clarity (after correctness and security pass).

Load only profiles relevant to touched files. Prefer no more than three domain profiles per pass unless the user requests a deep audit.

## Severity Model

- **CRITICAL**: exploitable security flaw, data loss path, or outage risk on critical paths.
- **HIGH**: logic defect or performance failure that can break core behavior.
- **MEDIUM**: maintainability/reliability issue likely to cause near-term defects.
- **LOW**: localized clarity/style/documentation improvements.

## Evidence Rules

- Never fabricate line numbers.
- Tie each finding to concrete code evidence.
- Explain blast radius and failure mode succinctly.
- Prefer targeted fixes over broad rewrites.

## Verification

Run the narrowest checks that validate touched behavior:

- formatter/lint on touched files,
- targeted tests for impacted modules,
- typecheck when relevant.

If checks cannot run, state exactly what was skipped and why.

## Stop Conditions

Stop and ask for direction when:

- fixes require API/contract redesign,
- behavior intent is too ambiguous to classify severity,
- required validation tooling is unavailable and risk is high.
