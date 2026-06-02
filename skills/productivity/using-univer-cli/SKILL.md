---
name: using-univer-cli
description: "Use when any task involves spreadsheets, workbook files, Excel-compatible files, .xlsx/.csv/.univer packages, sheets, cells, ranges, formulas, charts, formatting, workbook previews, or SaC workbook behavior."
---

# Using Univer CLI

This is the entry skill for workbook and spreadsheet tasks. If the task touches workbook files,
sheets, cells, ranges, formulas, formatting, charts, previews, or SaC workbook behavior, load this
skill before choosing tools or writing code.

<EXTREMELY-IMPORTANT>
If there is even a 1% chance the task is about a workbook, spreadsheet, Excel file, sheet, cell,
range, formula, chart, formatting, preview, or SaC workbook behavior, you MUST use this skill first.

IF THIS SKILL APPLIES, DO NOT CHOOSE A SPREADSHEET LIBRARY FIRST. USE THE UNIVER CLI PATH FIRST.
</EXTREMELY-IMPORTANT>

## The Rule

Decide the workflow before touching workbook content.

```dot
digraph using_univer_cli {
    "Workbook task received" [shape=doublecircle];
    "Ordinary workbook-visible work?" [shape=diamond];
    "Load univer-cli" [shape=box];
    "Use workbook-visible verification" [shape=box];
    "SaC source or complex behavior?" [shape=diamond];
    "Load writing-univer-plans" [shape=box];
    "Success criteria then plan" [shape=box];
    "Load executing-univer-plans" [shape=box];
    "Execute the plan" [shape=box];
    "Load test-driven-univer-development" [shape=box];
    "TDD each pack from the plan" [shape=box];
    "Implement only after the assertion gate exists" [shape=box];
    "Verify and repair" [shape=box];

    "Workbook task received" -> "Ordinary workbook-visible work?";
    "Ordinary workbook-visible work?" -> "Load univer-cli" [label="yes"];
    "Load univer-cli" -> "Use workbook-visible verification";
    "Ordinary workbook-visible work?" -> "SaC source or complex behavior?" [label="no"];
    "SaC source or complex behavior?" -> "Load writing-univer-plans" [label="yes"];
    "Load writing-univer-plans" -> "Success criteria then plan";
    "Success criteria then plan" -> "Load executing-univer-plans";
    "Load executing-univer-plans" -> "Execute the plan";
    "Execute the plan" -> "Load test-driven-univer-development";
    "Load test-driven-univer-development" -> "TDD each pack from the plan";
    "TDD each pack from the plan" -> "Implement only after the assertion gate exists";
    "Implement only after the assertion gate exists" -> "Verify and repair";
}
```

SaC source authoring MUST follow this order:

1. **Success criteria then plan**: load `writing-univer-plans`, write or update
   `<package.univer>/project/success-criteria/<topic>.md`, inspect enough workbook-visible evidence,
   and write or update `<package.univer>/project/plans/<topic>.md`.
2. **Execute the plan**: load `executing-univer-plans`, review the plan critically, and execute one
   Migration Pack at a time.
3. **TDD each pack from the plan**: load `test-driven-univer-development`, derive
   `assertions.ts` coverage from the plan, and watch the assertion fail for the intended
   workbook-visible reason.
4. **Implement only after the assertion gate exists**: edit Migration Packs only after the plan and
   plan-derived assertions exist.
5. **Verify and repair**: use `univer sac verify <package.univer> --json` and the verify report to drive
   repairs before claiming completion.

Do not write the plan before the success criteria checklist.
Do not write `assertions.ts` before the plan.
Do not edit Migration Packs before plan-derived assertions.
If you already did any step out of order, stop, write the missing success criteria and plan from
current evidence, then restart the TDD loop from that plan.

## Hard Gate

Do not treat workbook work as a generic file parsing job. Use the Univer skill stack and `univer`
CLI as the workbook engine.

- Do not import or install spreadsheet libraries such as `exceljs`, `xlsx`, pandas, or
  LibreOffice automation as a substitute for Univer CLI.
- Do not read or patch `.univer` package internals.
- Do not parse `.xlsx` files directly when the task can be handled through `univer import`,
  `univer inspect`, `univer pipe`, `univer run`, `univer export`, or SaC workflows.
- Shell tools are fine for text or JSON streams produced by `univer`, such as `pipe out` output or
  command JSON. They are not a replacement workbook engine.
- Only consider a non-Univer fallback after the relevant Univer skill has been loaded, the CLI path
  is proven insufficient, and the user agrees to the fallback.

## Red Flags

These thoughts mean STOP and route through Univer CLI:

| Thought | Reality |
| --- | --- |
| "This is just an Excel file; I'll use `exceljs`." | Workbook files are Univer CLI tasks first. |
| "I only need to inspect a few cells." | Use `univer inspect`, `search`, `pipe out`, or readonly `run`. |
| "I'll unzip or patch the workbook package directly." | Package internals are not the editing surface. |
| "I'll verify with package metadata or command success." | Verify workbook-visible state. |
| "SaC apply passed, so the behavior is done." | SaC completion needs test-driven Univer assertion evidence. |

## First Moves

1. Identify the workbook artifact and target outcome.
2. Route to the owning Univer skill before touching workbook content.
3. Use path-first `univer` commands or SaC source workflows; avoid workbook package internals.
4. Verify with workbook-visible evidence before claiming completion.

## Route Details

| Task shape | Load |
| --- | --- |
| Harness-provided workbook task with its own local contract, prepared package, or required handoff artifact | Follow the task-local harness contract first, then use `univer-cli` plus the appropriate workbook or SaC route below |
| Ordinary workbook-visible inspection, search, import, export, pipe, bounded edit, formula review, preview, comments, commit, pull, or sync | `univer-cli` |
| SaC source authoring, Facade Migration Pack work, `assertions.ts`, `univer sac`, or complex workbook behavior development | `writing-univer-plans`, `executing-univer-plans`, then `test-driven-univer-development` |
| Existing or legacy workbook with no SaC source, where the user wants behavior converted into SaC source | `univer-cli` for readonly baseline probes, then `writing-univer-plans`, `executing-univer-plans`, and `test-driven-univer-development` |

Ordinary workbook-visible work should not enter the SaC TDD workflow unless the user asks to author SaC source or durable workbook behavior.

For ordinary workbook-visible tasks, load `univer-cli` and stay with workbook-visible verification.

## SaC TDD Route

For SaC source authoring or complex workbook behavior:

1. Load `writing-univer-plans` before editing migration source.
2. Write or update package-local success criteria under `<package.univer>/project/success-criteria/`,
   then the plan under `<package.univer>/project/plans/`.
3. Load `executing-univer-plans` to review and execute the plan pack-by-pack.
4. Load `test-driven-univer-development` for assertion coverage, apply/verify, repair,
   and handoff gates.

In short: load `writing-univer-plans` to define success criteria and plan workbook behavior,
`executing-univer-plans` to execute the plan, and `test-driven-univer-development` to implement and
verify each pack.

Do not skip `writing-univer-plans` for complex SaC behavior. The plan is the place where range
roles, pack boundaries, and assertion gates become explicit.

## Legacy Workbook Bootstrap

When a user provides a legacy workbook without SaC source, use `univer-cli` for readonly baseline probes such as inspect, search, pipe out, or readonly run scripts. Capture useful facts into the SaC plan, migration source, or assertions before continuing.

Readonly baseline probes are not completion evidence. SaC TDD completion evidence comes from
`test-driven-univer-development`: changed packs need assertion coverage and a relevant
passed `univer sac verify <package.univer> --json` run.

## Completion Evidence

- Ordinary workbook work needs workbook-visible verification through `univer-cli`, such as
  `inspect`, `search`, `pipe out`, bounded `run`, preview, comments, or export/import checks.
- SaC TDD work needs `test-driven-univer-development` evidence: assertion coverage plus
  a relevant passed `univer sac verify <package.univer> --json` run.
- Do not treat command summaries, package metadata, `univer sac apply` success, or readonly probes as
  final SaC TDD proof.
- If the task type is unclear, ask whether the user wants an ordinary workbook edit or durable SaC
  source behavior.
