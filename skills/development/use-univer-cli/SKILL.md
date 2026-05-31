---
name: use-univer-cli
description: "Use when handling any workbook or spreadsheet task with Univer CLI, including ordinary workbook operations, SaC source authoring, Facade Migration Packs, assertions.ts, or complex workbook behavior."
---

# use-univer-cli

Use this as the entry skill for all workbook and spreadsheet tasks. It is intentionally short: decide which Univer skill owns the work, then load that skill.

## Route First

| Task shape | Load |
| --- | --- |
| Ordinary workbook-visible inspection, search, import, export, pipe, bounded edit, formula review, preview, comments, commit, pull, or sync | `univer-cli` |
| SaC source authoring, Facade Migration Pack work, `assertions.ts`, `univer sac`, or complex workbook behavior development | `univer-plan`, then `univer-tdd` |
| Existing or legacy workbook with no SaC source, where the user wants behavior converted into SaC source | `univer-cli` for readonly baseline probes, then `univer-plan` and `univer-tdd` |

Ordinary workbook-visible work should not enter the SaC TDD workflow unless the user asks to author SaC source or durable workbook behavior.

For ordinary workbook-visible tasks, load `univer-cli` and stay with workbook-visible verification.

## SaC TDD Route

For SaC source authoring or complex workbook behavior:

1. Load `univer-plan` before editing migration source.
2. Write or update the workspace plan under `plans/`.
3. Load `univer-tdd` for assertion coverage, apply/verify, repair, and handoff gates.

In short: load `univer-plan` to plan the workbook behavior, then load `univer-tdd` to implement and verify it.

Do not skip `univer-plan` for complex SaC behavior. The plan is the place where range roles, pack boundaries, and assertion gates become explicit.

## Legacy Workbook Bootstrap

When a user provides a legacy workbook without SaC source, use `univer-cli` for readonly baseline probes such as inspect, search, pipe out, or readonly run scripts. Capture useful facts into the SaC plan, migration source, or assertions before continuing.

Readonly baseline probes are not completion evidence. SaC TDD completion evidence comes from `univer-tdd`: changed packs need assertion coverage and a relevant passed `univer sac verify <workspace> --json` run.

## Hard Boundaries

- Do not read or patch `.univer` or `.unv` internals.
- Do not treat command summaries, package metadata, `univer sac apply` success, or readonly probes as final SaC TDD proof.
- If the task type is unclear, ask whether the user wants an ordinary workbook edit or durable SaC source behavior.
