---
name: univer-cli
description: "Use when solving spreadsheet workbook problems with the `univer` or `unv` CLI, especially Excel-compatible `.xlsx` handoff, `.univer`/`.unv` packages, workbook inspection, range search, formulas, formatting, rich spreadsheet edits, live preview, versioning, shell-native `pipe out`/`pipe in` roundtrips, or bounded `run` scripts."
---

# univer-cli

`univer-cli` is a shell-native spreadsheet workbook CLI for agents. Use it when the workbook itself is the source of truth: Excel-compatible handoff, real sheet structure, formulas, formatting, rich spreadsheet edits, local preview, versioning, or verified rectangular data roundtrips.

Install it with `npm i -g univer-cli`.

Prefer `univer` over ad hoc CSV/text handling when the task depends on workbook-visible state. The executable is `univer`; `unv` may be available as a short alias.

## When To Use

Use this skill when the task involves any of these:

- local `.xlsx`, `.csv`, `.univer`, or `.unv` workbook files
- inspecting workbook, sheet, range, formula, or lint state
- locating rows or cells before editing
- changing formulas, formatting, layout, sheet structure, or derived workbook data
- streaming a bounded rectangle through shell tools such as `awk`, `sort`, `uniq`, `wc`, or `jq`
- opening a readonly local preview with `univer view`
- checking local workbook status and creating local changesets with `status` and `commit`
- cloning, pulling, or syncing workbook versioning state with a configured remote
- exporting a handoff file and proving it is usable

Do not use this skill as an API reference. For exact command syntax, run `univer help` or `univer help <command...>`. For `run` APIs, use `univer help run` and `univer help run <topic>`.

## Operating Model

Default to this loop:

1. Pick one explicit workbook path, for example `./budget.univer`.
2. Create or import the workbook first if no `.univer` or `.unv` target exists.
3. Inspect workbook-visible state before deciding where to write.
4. Choose the smallest command surface that fits the task.
5. Mutate through public CLI commands, not by editing package internals.
6. Verify the changed workbook-visible state with `inspect` or `pipe out`.
7. Export only after verification when the user needs a handoff file.
8. Commit only after verified changes when the workflow needs a local changeset.

The workbook path is the local identity. Do not treat `unitId`, `sessionId`, or manifest ids as the CLI target.

## Hard Prohibitions

`.univer` and `.unv` files are `univer-cli` operation targets, not agent-editable data stores.

- Do not read `.univer` or `.unv` internals directly to infer workbook contents.
- Do not write, patch, unzip, rezip, rename internal files, or otherwise manipulate `.univer` or `.unv` package contents.
- Do not inspect `manifest.json`, snapshots, mutation logs, or package fragments as a substitute for workbook-visible reads.
- Do not guess sheet names, cell values, formulas, ranges, or workbook state from package files.
- Use `univer inspect`, `univer pipe out`, `univer run`, `univer export`, or other public CLI surfaces to read workbook data.

Direct package access can corrupt workbooks or teach the agent false state. If the CLI cannot read what you need, diagnose the CLI/runtime path instead of bypassing it.

## Command Choice

| Need | Prefer |
| --- | --- |
| Discover available command syntax | `univer help`, `univer help <command...>` |
| Start a workbook package | `univer new` or `univer import` |
| Hand back Excel-compatible output | `univer export` |
| Understand workbook shape before editing | `univer inspect workbook`, then `univer inspect range` |
| Locate content-defined targets | `univer search` when available; fall back to bounded `inspect range` |
| Stream rectangular data through shell tools | `univer pipe out` |
| Write a known rectangular matrix back | `univer pipe in` |
| Apply bounded workbook-local logic | `univer run --file` |
| Preview readonly workbook state | `univer view --no-open --json` or `univer view` |
| Check local versioning state | `univer status` |
| Create a local changeset from local mutations | `univer commit --message <message>` |
| Initialize a local package from an existing remote unit | `univer clone --unit-id <unitID>` |
| Pull remote-only changes | `univer pull` |
| Sync local and remote versioning state | `univer sync` |
| Diagnose runtime problems | `univer doctor`, `univer daemon status` |

Start small. If `inspect`, `pipe`, or another narrow surface expresses the job, use it directly. Reach for `run` when the task needs workbook-native logic rather than bulk data movement.

## Execution Results

Pay attention to both the process exit code and stderr:

- `$?` tells you whether the command succeeded. Treat non-zero exit as a failed operation even if partial stdout exists.
- stderr usually contains the stable diagnostic code, usage, and retry examples. Read it before changing approach.
- stdout may be data, JSON, Markdown, or a short success summary depending on the command. Do not treat any stdout text as proof of workbook state until you verify with a workbook-visible read.
- In shell pipelines, keep data stdout clean. Redirect stderr separately when you need diagnostics without corrupting downstream data.

Useful pattern:

```bash
univer inspect range "$WB" --range 'Sheet1!A1:D20' > ./range.md 2> ./range.err
status=$?
if [ "$status" -ne 0 ]; then
  sed -n '1,80p' ./range.err
  exit "$status"
fi
sed -n '1,40p' ./range.md
```

## Workflow Recipes

These recipes show verified command shapes. Replace paths, sheet names, and ranges with inspected workbook facts.

### Import And Inspect

```bash
WB=./orders.univer
univer import ./orders.csv "$WB" --json
univer inspect workbook "$WB"
univer inspect range "$WB" --range 'Sheet1!A1:D4'
```

Use `new` instead of `import` when the task starts from a blank workbook:

```bash
WB=./workbook.univer
univer new "$WB" --name "Workbook"
univer inspect workbook "$WB"
```

### Locate Before Editing

Prefer a content search when it returns real matches in your installed CLI:

```bash
univer search "$WB" West
```

If search is unavailable or reports a pending implementation, inspect a bounded range and derive the edit boundary from visible headers and sample rows:

```bash
univer inspect range "$WB" --range 'Sheet1!A1:D20'
```

Do not guess row numbers from memory or file metadata.

### Pipe Out Through Shell Tools

Use `pipe out` when the shell can reduce or reshape rectangular data before the agent reads it.

```bash
univer pipe out "$WB" --range 'Sheet1!A1:D4' --format tsv > ./orders.tsv
awk -F '\t' 'BEGIN{OFS="\t"} NR==1 || $2=="West" {print $1,$3}' ./orders.tsv > ./west.tsv
sed -n '1,5p' ./west.tsv
```

Prefer TSV when `awk` is the next consumer. Use `--type rawValue` when formatted display text is not safe enough for comparisons.

### Pipe In Generated Table Data

Write only a known matrix into an explicit, sheet-qualified range. Make `pipe in` the terminal stage of a pipeline unless you intentionally want its success summary downstream.

```bash
univer pipe in "$WB" --range 'Sheet1!F1:G3' --input-format tsv --data-file ./west.tsv
univer inspect range "$WB" --range 'Sheet1!F1:G3'
univer pipe out "$WB" --range 'Sheet1!F1:G3' --format tsv
```

Verify headers, first rows, and key columns. Row count alone is weak evidence because shifted columns can still preserve the row count.

### Run A Bounded Workbook Script

Use `run --file` for non-trivial logic so quoting does not become the task. Check `univer help run` before writing scripts, and check topic help such as `univer help run ranges` when you need API details.

```bash
cat > ./review.js <<'JS'
() => {
  const workbook = univerAPI.getActiveWorkbook();
  const sheet = workbook.getSheetByName("Sheet1");
  if (!sheet) return { success: false, error: "Sheet1 not found" };

  sheet.getRange("I1:J3").setValues([
    ["metric", "value"],
    ["west_orders", 2],
    ["reviewed", "yes"],
  ]);

  return { success: true, changedRanges: ["Sheet1!I1:J3"] };
}
JS

univer run "$WB" --file ./review.js
univer inspect range "$WB" --range 'Sheet1!I1:J3'
```

Only use documented APIs. If the API you need is not in `univer help run` or a run manual topic, stop and inspect the current docs or implementation instead of inventing method names.

### Preview Locally

Use preview when visual confirmation helps. `--no-open --json` is useful for agents and remote environments; the server process remains active until stopped.

```bash
univer view "$WB" --no-open --json
```

Use `univer help view` for port and browser-opening options.

### Commit Verified Changes

Check status before committing. Commit only after workbook-visible verification.

```bash
univer status "$WB"
univer commit "$WB" --message "Update review ranges"
univer status "$WB"
```

`commit` creates a local changeset from current local mutations. It does not push to a remote.

### Clone, Pull, And Sync

Use `clone` when a remote workbook unit already exists and you need a new local package path. The
target `.univer` path must be nonexistent or empty.

```bash
WB=./budget.univer
univer clone "$WB" --unit-id unit-remote --json
univer status "$WB"
univer inspect workbook "$WB"
```

Use `pull` when you only need missing remote changesets for a package already bound to a remote
unit. Use `sync` to sync local and remote versioning state.

```bash
univer status "$WB"
univer pull "$WB"
univer status "$WB"

univer commit "$WB" --message "Update review ranges"
univer sync "$WB"
univer status "$WB"
```

`sync` creates the remote workbook first when the package is still local-only. It pulls remote
changes and pushes local changesets, but it does not push uncommitted local mutations.
Remote endpoints come from `collaboration.defaultRemote` and `collaboration.remotes.<name>.url`.

### Export Handoff

Export after inspection proves the workbook state. Then prove the handoff file exists and, when useful, can be read back.

```bash
univer inspect workbook "$WB"
univer export "$WB" ./handoff.csv --json
test -s ./handoff.csv
univer import ./handoff.csv ./handoff.univer --json
univer inspect workbook ./handoff.univer
```

Use `.xlsx` for Excel handoff when the task requires workbook interoperability rather than plain CSV data.

## Run Scripts Without Guessing APIs

`run` executes bounded JavaScript inside the Univer workbook runtime. It is powerful, but it is the easiest place for agents to hallucinate APIs.

Hard rules:

- Read `univer help run` before using unfamiliar script APIs.
- Read `univer help run <topic>` for API families such as ranges, formulas, sheets, or formatting.
- Wrap code in `() => { ... }` or `async () => { ... }`.
- Return a plain object with explicit success/error fields.
- Use explicit sheet lookup, usually `getSheetByName(...)`.
- Keep target sheets and A1 ranges readable.
- Prefer A1 notation for fixed workbook-facing locations.
- Remember numeric coordinate overloads are 0-based.
- If writing formulas and reading computed results in the same run, wait for formula calculation using the documented formula wait API.
- Prefer `--file` for scripts that are more than a short one-liner.

Do not use private package files, manifest ids, or undocumented runtime objects as shortcuts.

## Shell-Native Rules

Use shell tools to reduce context before bringing data back to the agent. `pipe out` should produce clean data, while diagnostics and help belong outside the pipeline.

Good shell-native habits:

- keep ranges explicit and sheet-qualified
- quote the full A1 range string, especially for non-English or shell-sensitive sheet names
- prefer TSV for `awk`
- use JSON when `jq` or structured matrix handling is the next consumer
- stage intermediate files when you need a stable preview or assertion
- make `pipe in` the usual final pipeline stage
- verify with `inspect range` or `pipe out` after every writeback

Avoid `pnpm dev -- ...` in clean pipeline examples. The pnpm/tsx wrapper can print logs to stdout and corrupt streamed data. Use the installed `univer`/`unv` executable or another entrypoint you have proven emits clean stdout.

## Gotchas

- Never directly read or manipulate `.univer` or `.unv` internals. They are workbook packages owned by `univer-cli`, and direct access can corrupt the workbook or mislead you.
- `manifest.json` is metadata only. It does not prove sheet names, formulas, changed cells, or handoff correctness.
- Package contents are not a meaningful way to infer spreadsheet data. Use public CLI reads instead.
- Local file identity is the workbook path, such as `./budget.univer`, not `unitId`, `sessionId`, or manifest ids.
- Command success is not enough after import, mutation, export, or handoff. Verify workbook-visible state.
- A non-zero `$?` means the operation failed. Read stderr for the diagnostic, usage, and retry guidance.
- Top-level help group headings are visual sections only. Do not run `univer help read`, `univer help stream`, or group-prefixed leaf topics such as `univer help read inspect range`; use canonical command help such as `univer help inspect range` and `univer help pipe out`.
- Quote the full range: `--range '工作表1!A1:J20'`, not just the sheet name fragment.
- Shell row counts can pass while headers, columns, or keys shift. Check headers, samples, and key columns together.
- `pipe in` writes parsed matrix data and reports a summary; it does not echo input.
- `view` is readonly preview. Do not treat it as mutation verification unless the task is visual review.
- `commit` is local only; use `sync` to push local changesets.
- `sync` does not push uncommitted local mutations. Commit verified workbook changes first.
- If `sync` reports an invalid remote binding, stop and diagnose the package or remote setup.
- `pull` requires a package already bound to a remote unit. Use `sync` for first remote creation or `clone --unit-id` for an existing remote unit.
- `clone` replaced older remote binding wording. Do not use or invent a `bind` command.
- If runtime-backed commands fail to start, inspect `univer daemon status` before retrying blindly.
- If workbook-visible reads disagree with package metadata, trust workbook-visible reads first.
