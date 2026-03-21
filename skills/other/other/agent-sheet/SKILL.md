---
name: agent-sheet
description: shell-native spreadsheet CLI for agent work. Use it for workbook inspection, sheet/range reads, precise writes, import/export handoff, review-table construction, formula analysis, and bounded workbook-native scripting with verification.
metadata:
  openclaw:
    os:
      - linux
      - macos
    requires:
      bins:
        - agent-sheet
      anyBins:
        - awk
        - sed
        - python3
        - python
    install:
      - kind: node
        package: agent-sheet@latest
        bins:
          - agent-sheet
    links:
      repository: https://github.com/dream-num/skills
      documentation: https://github.com/dream-num/skills
---

# agent-sheet

`agent-sheet` is a local spreadsheet CLI for agents. Prefer it when the task needs real workbook structure, formulas, sheet lifecycle, import/export handoff, or a safe shell roundtrip instead of plain CSV cleanup or ad-hoc `xlsx` library use.

## Use it for

- resolving a workbook and keeping the target explicit with `--entry-id`
- inspecting workbook structure, sheets, ranges, formulas, and search hits
- writing sparse cells, bounded ranges, anchored review tables, or formula fills
- importing a local workbook, continuing edits, and exporting a final file
- streaming workbook data through shell tools, then writing verified results back
- using bounded `script js` only when built-in commands do not express the workbook change cleanly

## Do not default to

- reopening the workbook with a local workbook library for reads or writes that `agent-sheet` already covers
- using shell transforms when a direct `write cells`, `write range`, `write table`, `write fill`, or `sheet ...` command is clearer
- trusting metadata-only surfaces such as `file info` as proof of workbook structure
- finishing after a write without a task-specific verification pass

## First path

1. Run [playbooks/00-preflight.md](playbooks/00-preflight.md).
2. Resolve the workbook and keep using `--entry-id`.
3. Choose the smallest matching command via [references/command-selection-matrix.md](references/command-selection-matrix.md).
4. Verify with [playbooks/15-verify.md](playbooks/15-verify.md) before finishing.

## Hard defaults

- prefer `entryId` over `unitId` for local workbooks and imports
- treat `write range` as a full bounded rectangle replacement
- treat `write table --sheet <name>` as an A1-anchored table write with header semantics
- verify shell roundtrips with structure plus sample rows, not row count alone
- use `sheet list` or `inspect workbook` for sheet existence and handoff verification

## Highest-signal gotchas

- imported local entries can be healthy even when later `file info` shows `unitId: null`; keep operating on `entryId`
- `file info` is metadata only; it does not prove sheet count, sheet names, or formula state
- do not run `init` inside an already initialized workspace tree; nested workspace refusal is expected
- non-English sheet names work, but quote the full A1 range string in the shell
- shell pipelines can preserve the expected row count while still shifting headers or keys; verify the first rows and key columns after writeback

Read [references/gotchas.md](references/gotchas.md) when the task looks routine but has import/handoff, shell roundtrip, or workspace ambiguity.

## Task routing

| Task | Read next |
|---|---|
| workspace root, CLI resolution, or workbook target is unclear | [playbooks/00-preflight.md](playbooks/00-preflight.md) |
| inspect workbook state, extract data, search, or review formulas | [playbooks/10-read-analyze.md](playbooks/10-read-analyze.md) |
| plan the smallest safe mutation path | [references/command-selection-matrix.md](references/command-selection-matrix.md) |
| make data-visible edits or structural workbook changes | [playbooks/20-write-safe.md](playbooks/20-write-safe.md) |
| verify a mutation, shell roundtrip, or handoff | [playbooks/15-verify.md](playbooks/15-verify.md) |
| create, import, open, or export a local workbook | [playbooks/30-file-lifecycle.md](playbooks/30-file-lifecycle.md) |
| stream workbook data through shell tools | [references/shell-patterns.md](references/shell-patterns.md) |
| formatting, layout, or other built-in command gaps | [playbooks/40-script-fallback.md](playbooks/40-script-fallback.md) |
| import/handoff, `entryId` targeting, `file info`, or shell verification edge cases | [references/gotchas.md](references/gotchas.md) |

## Output style

- prefer bounded previews, file paths, or stream output over oversized inline dumps
- use `--to-stdout` for shell pipelines
- use `--to-file --output <path>` for large reusable extracts
- when reporting success, include the verification surface you actually used

## Ready-made assets

Use these before improvising shell snippets:

| Asset | Use when |
|---|---|
| [examples/roundtrip-awk-write-table.md](examples/roundtrip-awk-write-table.md) | building a review sheet through shell roundtrip |
| [examples/handoff-verify.md](examples/handoff-verify.md) | exporting, importing, and proving handoff structure |
| [examples/template-import-anchor-check.md](examples/template-import-anchor-check.md) | importing a template workbook and checking anchor cells |
| [scripts/verify_csv_preview.py](scripts/verify_csv_preview.py) | comparing header, head sample rows, and a key column |
| [scripts/check_csv_cells.py](scripts/check_csv_cells.py) | asserting anchor values or non-empty cells from a CSV snippet |

## Read next

Read only the file needed for the task:

| File | Use when |
|---|---|
| [playbooks/00-preflight.md](playbooks/00-preflight.md) | workspace or workbook context is not yet resolved |
| [playbooks/10-read-analyze.md](playbooks/10-read-analyze.md) | inspecting workbook state, extracting data, searching, or reviewing formulas |
| [references/command-selection-matrix.md](references/command-selection-matrix.md) | picking the smallest correct command before writing |
| [playbooks/15-verify.md](playbooks/15-verify.md) | proving a mutation or handoff actually succeeded |
| [playbooks/20-write-safe.md](playbooks/20-write-safe.md) | choosing the smallest safe mutation path |
| [playbooks/30-file-lifecycle.md](playbooks/30-file-lifecycle.md) | creating, importing, opening, or exporting a local workbook |
| [playbooks/40-script-fallback.md](playbooks/40-script-fallback.md) | built-in commands cannot express the requested workbook change |
| [references/shell-patterns.md](references/shell-patterns.md) | the task is naturally a shell pipeline |
| [references/gotchas.md](references/gotchas.md) | the task involves common real-world failure modes |
| [references/js-api-minimal.md](references/js-api-minimal.md) | `script js` is necessary and must stay tightly bounded |
| [examples/roundtrip-awk-write-table.md](examples/roundtrip-awk-write-table.md) | you need a concrete shell roundtrip example |
| [examples/handoff-verify.md](examples/handoff-verify.md) | you need a concrete export/import handoff example |
| [examples/template-import-anchor-check.md](examples/template-import-anchor-check.md) | you need a concrete non-English template import example |
