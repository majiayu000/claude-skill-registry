---
name: agent-sheet
description: Deprecated legacy alias for `univer-cli`; use only for older prompts or installs that still call `agent-sheet`. Prefer `univer-cli` for current shell-native workbook work.
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

Deprecated: `agent-sheet` is the old name for `univer-cli`. Prefer `univer-cli` and the `univer` / `unv` command surface for new work.

Keep using this skill only when an older prompt, install, or environment explicitly refers to `agent-sheet`.

`agent-sheet` is the shell-native workbook CLI for agent work. Use it when the task needs real workbook structure, formulas, workbook-local logic, or a safe stdin/stdout roundtrip instead of ad hoc CSV handling.

Treat the workbook as the source of truth. Read from workbook-visible state, mutate through the public surface, and prove success from workbook-visible results.

## Start here

Use the smallest surface that cleanly matches the task:

- `inspect`: first read, reconnaissance, workbook-visible structure, formulas, ranges, lint signals
- `search`: first-class localization before edits
- `fill`: first-class propagation when a correct seed already exists
- `run`: default programmable workbook surface for bounded workbook-local logic
- `pipe out` / `pipe in`: bulk rectangular data plane for shell roundtrips

Start small. If `inspect`, `search`, `fill`, or `pipe` cleanly expresses the job, use that surface directly. Use `run` when the work is programmable workbook logic rather than bulk data movement.

## Default operating model

- if you do not have an `entry-id` yet, get one first with `file list`, `file create`, or `file import`, then stay on that workbook
- resolve one workbook and keep its `--entry-id` for the whole task
- start with `inspect` so worksheet names, headers, formulas, and write boundaries are real rather than guessed
- use `search` before mutation when the target is content-defined
- use `fill` for spreadsheet-native propagation from a known seed
- use `pipe out` / `pipe in` when the shell is the right place for a rectangular transform
- use `run` for bounded workbook-local logic, structural edits, formatting, or formula orchestration
- verify from workbook-visible reads after every mutation or handoff step

## Hard defaults

- prefer `--entry-id` to keep the target explicit
- start with `inspect`
- treat `run` as the default programmable workbook surface
- treat `pipe out` / `pipe in` as the bulk rectangular data plane
- verify from workbook-visible results, not metadata alone
- verify shell roundtrips with structure plus sample rows, not row count alone
- use workbook-visible inspection for handoff and completion checks

## Highest-signal gotchas

- imported local entries can be healthy even when later `file info` shows `unitId: null`; keep operating on `entryId`
- `file info` is metadata only; it does not prove worksheet count, worksheet names, or formula state
- non-English worksheet names work, but quote the full A1 range string in the shell
- shell pipelines can preserve the expected row count while still shifting headers or keys; verify the first rows and key columns after writeback
- if workbook-visible verification disagrees with metadata, trust the workbook-visible surface first

## Read next

Read only what matches the task:

- [playbooks/01-getting-started.md](playbooks/01-getting-started.md): first contact, target resolution, basic flow
- [playbooks/02-common-workflows.md](playbooks/02-common-workflows.md): workflow recipes by task intent
- [playbooks/03-handoff-and-verification.md](playbooks/03-handoff-and-verification.md): handoff, completion checks, workbook-visible verification
- [references/command-selection-matrix.md](references/command-selection-matrix.md): shortest path from task intent to command choice
- [references/run-api.md](references/run-api.md): `run` entry point and reference map for bounded programmable workbook logic
- [references/shell-patterns.md](references/shell-patterns.md): small shell-native patterns for `pipe` workflows
- [references/gotchas.md](references/gotchas.md): real-world failure modes and edge cases
- [examples/handoff-verify.md](examples/handoff-verify.md): export/import/handoff proof
- [examples/roundtrip-pipe-review-rectangle.md](examples/roundtrip-pipe-review-rectangle.md): staged shell roundtrip with explicit preview verification
