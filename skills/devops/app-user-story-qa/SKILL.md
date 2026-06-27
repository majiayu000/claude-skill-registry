---
name: app-user-story-qa
description: "End-to-end app feature inventory and user-story testing workflow. Use when the user asks to audit every feature, create user stories or expected behavior from code, maintain a single canonical spreadsheet/tracker, test each user behavior, document errors, fix logistical or UX issues, and retest after fixes."
---

# App User Story QA

## Purpose

Use this skill to turn a broad "test every feature in this app" request into a controlled loop with one source of truth. Anchor every feature to code, track expected behavior in a canonical spreadsheet, run tests against each user story, classify failures, fix only in-scope logistical or UX defects, and retest.

## Route

Use `plan_first` for most runs. Switch to `clarify_first` only when the app boundary, writable checkout, production risk, or acceptance criteria are unclear enough that a wrong assumption would waste substantial work.

Before editing:

1. Run a repo state snapshot: current path, branch, latest remote, dirty files, open PRs when relevant.
2. If the checkout is dirty or user work is present, first decide which state the user asked to test. Preserve current user work in the isolated test worktree when the request targets the working tree; use a clean base only when the user asked for the base branch.
3. Read applicable repo instructions such as `AGENTS.md`, `README`, architecture docs, and feature entrypoints.
4. Search for existing QA trackers before creating a new one.
5. Define the app boundary by user-facing surfaces, not internal helper functions.

## Operating Contract

Direct actions:
- Inventory local code and docs, create or update the single canonical tracker, run local tests, document failures, and fix narrow in-scope logistical or UX defects.
- Add focused coverage when a production or UX fix changes user-observable behavior.

Escalate before:
- Testing production systems, using paid external services, changing credentials or deployment state, deleting user data, or broadening the app boundary beyond the user's request.
- Editing shared test infrastructure, weakening assertions, or changing product requirements instead of the implementation.

Evidence-backed pushback:
- Challenge requests to skip the tracker, mark untested rows as passed, or fix symptoms without reproducing the failure. Cite the tracker row, command output, code anchor, or missing environment precondition.

Feedback loop:
- Promote repeated setup failures, brittle manual paths, or recurring test gaps into tracker notes, scripts, docs, or follow-up issues instead of leaving them only in chat.

## Gotchas

- Do not create scattered notes or duplicate trackers. One canonical tracker is the audit log.
- Do not invent expected behavior from product hopes. Expected behavior comes from current code, docs, and visible user surfaces.
- Do not mark a feature passed from stale output. Fresh evidence from the current session is required.
- Do not "fix" environment blockers unless the user asked for environment repair.

## Canonical Tracker

Create or update exactly one tracker. Prefer a real spreadsheet when the runtime supports it; otherwise use a CSV and treat it as the canonical spreadsheet. Do not scatter status across side reports.

Use these columns:

```csv
Feature ID,Surface,Feature / capability,User story,Expected behavior based on code,Code anchors,Initial test approach,Initial test command or route,Status,Test result,Errors,Fix status,Retest result,Notes
```

Rules:

- Assign stable IDs such as `F001`, `F002`.
- Require at least one code anchor per row. A row without an anchor is not complete.
- Write expected behavior from current code and docs, not from aspirational specs.
- Keep the tracker parseable: validate CSV/spreadsheet row widths after edits.
- Update the tracker during the loop, not only at the end.

## Status Values

Use a small, consistent status set:

- `Not Tested`
- `Passed`
- `Failed - Product`
- `Failed - UX`
- `Failed - Logistical`
- `Failed - Test Infra`
- `Blocked - Env`
- `Fixed`
- `Passed after fix`

Use `Failed - Logistical` for repo-owned setup, script, port, packaging, or local workflow defects that block a valid user path.
Use `Blocked - Env` for local machine issues such as missing credentials, occupied services outside the repo, stale PATH binaries, or unavailable optional runtimes. Do not "fix" the user's environment unless they explicitly ask.

## Defect Taxonomy

Classify every failure before fixing:

- `Product`: implemented behavior violates the user story or loses data.
- `UX`: behavior works but the user path is confusing, brittle, or poorly surfaced.
- `Logistical`: scripts, ports, setup, packaging, or local workflow make valid behavior hard to exercise.
- `Test Infra`: the test itself is flaky, racy, or asserts the wrong contract.
- `Env`: external setup blocks execution and is not a repo defect.

Fix only defects that are in scope for the task. Record out-of-scope defects in the tracker with clear rationale.

## Workflow

### 1. Inventory

Map all user-visible surfaces first:

- CLI commands and flags
- Web or desktop UI routes
- API endpoints
- background jobs or hooks that affect users
- plugin, package, install, or release surfaces
- import/export, backup, migration, and governance flows

For each feature, record the user story as:

```text
As a <user>, I want <capability>, so <outcome>.
```

Keep stories practical. Do not create rows for private helpers unless the user can observe the behavior through a surface.

### 2. Test

For every tracker row, choose the strongest feasible evidence:

- direct smoke test for the user path
- focused unit or integration test for the exact contract
- broad regression suite when a feature is already covered there
- manual or browser test when automation is missing

Record the command, route, or manual steps in the tracker. Fresh output from the current session is required before marking a row passed.

### 3. Fix

Before editing, state the exact defect and files being changed. Keep fixes narrow:

- For UX defects, fix production code and add or update focused coverage.
- For product defects, record the evidence and escalate unless the user's request explicitly authorizes product behavior fixes.
- For logistical defects, improve scripts, defaults, setup checks, or error messages.
- For test-infra defects, preserve the behavior contract and fix the fixture or race.
- Do not weaken assertions to make the suite pass.

Stop and re-evaluate after three failed attempts on the same defect.

### 4. Retest

After each fix:

1. Rerun the focused failing test or smoke.
2. Rerun the relevant broader gate for the touched surface.
3. Update `Fix status` and `Retest result`.
4. Keep the original error text or summary in `Errors` so the tracker remains an audit log.

Before completion, run the repo's required formatting, build, typecheck, lint, and test commands when practical.

## Completion Gate

Finish only when:

- every feature row has a user story, expected behavior, code anchors, and a status;
- every `Failed` row is fixed, explicitly out of scope, or blocked by environment with evidence;
- every fix has a retest result;
- the tracker validates structurally;
- the final answer names the tracker path, changed files, defects found, fixes made, and verification commands.

If the repo has existing dirty work that is not yours, mention the isolated worktree or scope boundary in the final answer.
