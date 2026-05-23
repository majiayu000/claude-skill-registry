---
name: univer-cli
description: "Use when solving spreadsheet workbook problems with the `univer` or `unv` CLI as a terminal-native spreadsheet engine: Excel-compatible `.xlsx` handoff, `.univer` or `.unv` packages, workbook inspection, range search, formulas, formatting, charts, shapes, floating images, rich spreadsheet edits, live preview and viewer review comments, versioning, shell-native `pipe out`/`pipe in` roundtrips, or bounded `run` scripts."
---

# univer-cli

`univer` is a spreadsheet engine in the terminal. Use it when an agent needs real workbook semantics: sheets, ranges, formulas, formatting, layout, previews, imports, exports, or versioned workbook state.

Install the CLI with `npm i -g univer-cli`. Update the CLI with `univer update`. The executable is `univer`; `unv` may be available as a short alias.

## Core Mental Model

Treat workbook-visible state as the source of truth. A successful command summary, package metadata, or an internal manifest does not prove that sheet names, cell values, formulas, formatting, or exported handoff files are correct.

The workbook path is the local identity. Pick one explicit path such as `./budget.univer` and use that path as the CLI target. Do not target workbooks by `unitId`, `sessionId`, manifest ids, or runtime ids.

`.univer` and `.unv` files are CLI operation targets, not agent-editable data stores. Read and write workbook data through public CLI surfaces such as `inspect`, `search`, `pipe`, `run`, `export`, `status`, and `commit`.

Use `univer help` and `univer help <command...>` for exact syntax. For `run` scripts, use `univer help run` and `univer help run <topic>` before relying on unfamiliar APIs.

## Use When

Use this skill when the task involves spreadsheet or workbook work, especially:

- creating, importing, exporting, or handing off `.xlsx`, `.csv`, `.univer`, or `.unv` files
- inspecting workbook shape, sheets, ranges, formulas, formatting, or visible cell state
- locating content-defined rows, columns, headers, or cells before editing
- making bounded edits to cells, formulas, formatting, charts, shapes, floating images, layout, or sheet structure
- streaming rectangular workbook data through shell tools before reading it into context
- writing generated matrix data back into a sheet-qualified range
- previewing workbook state locally with `univer view`
- reading submitted local viewer review comments with `univer view comments`
- creating, restoring, resetting, pulling, or syncing local workbook changesets
- proving that a workbook-visible mutation or export is correct enough to hand back

## Default Operating Loop

1. Pick one explicit workbook path, for example `./budget.univer`.
2. Create or import a workbook first if no `.univer` or `.unv` target exists.
3. Inspect workbook-visible state before deciding where to write.
4. Locate targets from visible headers, values, formulas, or inspected ranges.
5. Choose the smallest public CLI surface that fits the task.
6. Mutate through the CLI, not by editing package internals.
7. Verify changed workbook-visible state with `inspect`, `pipe out`, or another public read.
8. Export only after verification when the user needs a handoff file.
9. After changes have been verified, if the user may need to inspect, audit, or review the final workbook, run `univer view "$WB" --no-open --json` to get a local preview link and include that link in your response.
10. Commit or sync only after verified changes when versioning is part of the workflow.

## Hard Rules

- Do not read `.univer` or `.unv` internals to infer workbook contents.
- Do not write, patch, unzip, rezip, rename internal files, or manipulate workbook package contents.
- Do not inspect `manifest.json`, snapshots, mutation logs, or package fragments as a substitute for workbook-visible reads.
- Do not guess sheet names, row numbers, formulas, ranges, or changed cells from memory or file metadata.
- Do not treat stdout summaries as proof of workbook state. Verify with a workbook-visible read.
- Do not invent commands or `run` APIs. Check `univer help` and documented run topics.

Direct package access can corrupt workbooks or teach the agent false state. If the CLI cannot read what you need, diagnose the CLI/runtime path instead of bypassing it.

## Command Selection

| Need | Prefer |
| --- | --- |
| Discover exact command syntax | `univer help`, `univer help <command...>` |
| Start a workbook package | `univer new` or `univer import` |
| Hand back Excel-compatible output | `univer export` |
| Understand workbook shape before editing | `univer inspect workbook`, then `univer inspect range` |
| Locate content-defined cells | `univer search`, scoped with `--sheet` and/or `--range` when possible |
| Stream rectangular data through shell tools | `univer pipe out` |
| Write a known rectangular matrix back | `univer pipe in` |
| Apply bounded workbook-local logic | `univer run --file` |
| Create or maintain workbook charts | `univer run --file` with `univer help run charts` |
| Create or maintain workbook shapes and connectors | `univer run --file` with `univer help run shapes` |
| Create or maintain workbook floating images | `univer run --file` with `univer help run images` |
| Preview readonly workbook state | `univer view --no-open --json` or `univer view` |
| Read local viewer review feedback | `univer view comments "$WB" --json` |
| Check local versioning state | `univer status` |
| Create a local changeset from local mutations | `univer commit --message <message>` |
| Discard uncommitted local mutations | `univer restore` |
| Reset local unsynced commits | `univer reset --soft HEAD~N` or `univer reset --hard HEAD~N` |
| Initialize a local package from an existing remote unit | `univer clone --unit-id <unitID>` |
| Pull remote-only changes for a bound package | `univer pull` |
| Sync local and remote versioning state | `univer sync` |
| Diagnose runtime problems | `univer doctor`, `univer daemon status` |
| Prepare a bug report or Univer team support artifact after user authorization | `univer doctor collect` |

Use canonical command help such as `univer help inspect range` and `univer help pipe out`. Top-level help group headings are visual sections only; do not run group-prefixed topics such as `univer help read inspect range`.

## Execution Results

Treat non-zero exit as failure even when stdout is partially present. Read stderr before changing approach; it usually contains the stable diagnostic code, usage, and retry examples.

Keep data stdout clean in shell pipelines. If diagnostics are needed, capture stderr separately so downstream tools receive only workbook data.

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

These are verified command shapes. Replace paths, sheet names, and ranges with inspected workbook facts.

### Create Or Import, Then Inspect

```bash
WB=./orders.univer
univer import ./orders.csv "$WB" --json
univer inspect workbook "$WB"
univer inspect range "$WB" --range 'Sheet1!A1:D4'
```

Use `new` when the task starts from a blank workbook:

```bash
WB=./workbook.univer
univer new "$WB" --name "Workbook"
univer inspect workbook "$WB"
```

### Locate Before Editing

Use `search` before editing when the target is defined by visible workbook content:

```bash
univer search "$WB" West
```

Plain text output is one A1 reference per matched cell, which keeps shell pipelines clean. With no
matches, stdout is empty and the command still succeeds. Use `--json` when you need match metadata,
the matched cell data preview, truncation flags, counts, or the searched scope:

```bash
univer search "$WB" West --sheet Orders --range 'A1:Z200' --json
```

By default, search checks `displayValue`, so formatted values such as dates are searchable by the
same strings a user sees in the sheet. Use `--type rawValue` for underlying numeric/string values
such as spreadsheet date serials, and `--type formula` for formulas:

```bash
univer search "$WB" 2024-01-01
univer search "$WB" 45292 --type rawValue
univer search "$WB" SUM --type formula --json
```

Useful narrowing options:

- `--sheet <name>` may be repeated.
- `--range <A1>` may be repeated; unqualified ranges require a `--sheet`.
- `--case-sensitive` and `--whole-cell` tighten matching.
- `--max-results` limits returned matches; truncation is reported on stderr for text output and in JSON fields for `--json`.
- `--max-cell-value-length` bounds previewed cell data in JSON.

If `search` fails, read stderr for the diagnostic message before changing approach. If the target is
not content-defined, inspect a bounded range and derive the edit boundary from visible headers and
sample rows:

```bash
univer inspect range "$WB" --range 'Sheet1!A1:D20'
```

### Pipe Out Through Shell Tools

Use `pipe out` when the shell can reduce or reshape rectangular data before the agent reads it. Prefer TSV for `awk`, JSON for `jq`, and `--type rawValue` when formatted display text is not safe enough for comparisons.

```bash
univer pipe out "$WB" --range 'Sheet1!A1:D4' --format tsv > ./orders.tsv
awk -F '\t' 'BEGIN{OFS="\t"} NR==1 || $2=="West" {print $1,$3}' ./orders.tsv > ./west.tsv
sed -n '1,5p' ./west.tsv
```

### Pipe In Generated Table Data

Write only a known matrix into an explicit, sheet-qualified range. Make `pipe in` the terminal stage of a pipeline unless you intentionally want its success summary downstream.

```bash
univer pipe in "$WB" --range 'Sheet1!F1:G3' --input-format tsv --data-file ./west.tsv
univer inspect range "$WB" --range 'Sheet1!F1:G3'
univer pipe out "$WB" --range 'Sheet1!F1:G3' --format tsv
```

Verify headers, sample rows, and key columns. Row count alone is weak evidence because shifted columns can still preserve row count.

### Run A Bounded Workbook Script

Use `run --file` for workbook-native logic that does not fit `inspect`, `search`, `pipe`, or `export`. Check `univer help run` and the relevant `univer help run <topic>` manual before using unfamiliar APIs.

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

`run` scripts should:

- wrap code in `() => { ... }` or `async () => { ... }`
- return a plain object with explicit success or error fields
- use explicit workbook, sheet, and A1 range boundaries
- prefer A1 notation for fixed workbook-facing locations
- remember numeric coordinate overloads are 0-based
- use documented facade builders for conditional formatting instead of editing internal rule model shapes
- use official enum references for conditional formatting color scales, data bars, and icon sets: `ConditionFormatIconSetTypeEnum` supplies `setIconSet().iconConfigs[].iconType`, and `ConditionFormatValueTypeEnum` supplies value config `type` values
- use documented chart builders and worksheet chart APIs from `univer help run charts` instead of editing chart resource internals
- use documented shape builders and worksheet shape APIs from `univer help run shapes` instead of editing drawing or shape resource internals
- use documented floating image builders and worksheet image APIs from `univer help run images` instead of editing drawing or resource internals
- wait for formula calculation with the documented formula wait API before reading same-run computed results
- prefer `--file` for scripts beyond a short one-liner

### Create Or Maintain Charts

Use `univer run` for workbook-local charts and `univer view` for visual inspection. Command-line verification should read facade state such as `sheet.getCharts()`, `chart.getChartId()`, `chart.getRange()`, `chart.getSeriesData()`, and `chart.getCategoryData()`.

```bash
univer help run charts
univer run "$WB" --file ./create-chart.js
univer view "$WB" --no-open --json
```

In scripts, seed or choose a source range, configure `sheet.newChart()`, call `build()`, then insert it with `sheet.insertChart(chartInfo)`. Use `chart.updateRange()` or `sheet.removeChart(chart)` for maintenance.

Special chart types have stricter source shapes:

- Most charts use a category-plus-series table, for example `month, sales, cost`.
- Relation charts require a node/type matrix: first column is node, second column is type/category, remaining columns are the numeric relation matrix. For `N` nodes, use `N` data rows and `N + 2` columns.
- Sankey charts require a `source, target, value` edge list. The third column must be numeric; avoid reverse edges that create circular Sankey data.
- Bubble charts need numeric `x`, `y`, and `size` columns.
- Heatmap charts use the first column as y-axis labels, remaining headers as x-axis labels, and remaining cells as numeric heat values.

### Create Or Maintain Shapes

Use `univer run` for workbook-local shapes and connectors and `univer view` for visual inspection. Command-line verification should read facade state such as `sheet.getShapes()`, `shape.isLineShape()`, `shape.getShapeId()`, `shape.getShapeType()`, `shape.getPosition()`, `shape.getSize()`, `shape.getStartConnectInfo()`, and `shape.getEndConnectInfo()`.

```bash
univer help run shapes
univer run "$WB" --file ./create-shapes.js
univer view "$WB" --no-open --json
```

In scripts, configure `sheet.newShape()`, call `build()`, then insert it with `sheet.insertShape(shapeInfo)`. Use `sheet.newConnector()` for connector lines, `sheet.connectShapes()` to attach connector endpoints to facade shape objects from the same worksheet, `sheet.newShape(existingShape)` with `sheet.updateShape(updatedShapeInfo)` for updates, and `sheet.removeShape(shape)` for deletion.

Use `univerAPI.Enum.ShapeTypeEnum` with `setShapeType()`. Common starts are `Rect`, `RoundRect`, `Ellipse`, `Diamond`, flowchart values such as `FlowchartProcess`, and connector values such as `StraightConnector1`, `BentConnector3`, or `CurvedConnector3`. Use shape facade enums for fill, stroke, dash, cap, join, and arrows: `ShapeFillEnum`, `ShapeGradientTypeEnum`, `ShapeLineTypeEnum`, `ShapeLineDashEnum`, `ShapeLineCapEnum`, `ShapeLineJoinEnum`, `ShapeArrowTypeEnum`, and `ShapeArrowSizeEnum`.

The shapes topic covers workbook-local floating shapes and connectors only. `univer run` does not export shape images, perform browser screenshots, or provide an interactive shape editor.

### Create Or Maintain Floating Images

Use `univer run` for workbook-local floating images and `univer view` for visual inspection. Command-line verification should read facade state such as `sheet.getImages()`, `sheet.getImageById(id)`, `image.getId()`, `image.toBuilder().getSource()`, `image.toBuilder().getSourceType()`, and update or delete return values.

```bash
univer help run images
univer run "$WB" --file ./create-image.js
univer view "$WB" --no-open --json
```

In scripts, configure `sheet.newOverGridImage()`, call `buildAsync()`, then insert it with `sheet.insertImages([image])`. Use `image.toBuilder()` with `sheet.updateImages([newImage])`, direct `FOverGridImage` methods such as `setSizeAsync()` or `setPositionAsync()`, or `sheet.deleteImages([image])` for maintenance.

Use `univerAPI.Enum.ImageSourceType.URL` for HTTP(S) image URLs and full data URLs, `ImageSourceType.BASE64` for raw base64 payloads, and `ImageSourceType.UUID` only for existing Univer-managed image or file UUIDs. For predictable report placement, start with `univerAPI.Enum.SheetDrawingAnchorType.Position`.

The images topic covers floating images only. It does not cover cell images, floating DOM, screenshot export, local image upload helpers, or a top-level `univer image` command.

### Preview Locally

Use preview when visual confirmation helps. `--no-open --json` is useful for agents and remote environments; the server process remains active until stopped.

```bash
univer view "$WB" --no-open --json
```

When a human submits review feedback in the local viewer, read it without reopening the browser:

```bash
univer view comments "$WB" --json
univer view comments --session "<session-id>" --all --json
```

By default, `view comments` returns actionable submitted comments that are not resolved. Use `--all` when you need pending, submitted, and resolved comments for audit context. These are local viewer review comments, not workbook-native cell notes or collaboration thread comments; the command is read-only and does not start a host, open a browser, create a session, or mutate the workbook.

Use `univer help view` for port and browser-opening options.

### Version Verified Changes

Check status before committing. Commit only after workbook-visible verification.

```bash
univer status "$WB"
univer commit "$WB" --message "Update review ranges"
univer status "$WB"
```

`commit` creates a local changeset from current local mutations. It does not push to a remote.

Use `restore` when current uncommitted workbook mutations should be discarded while preserving local commits and synced history.

```bash
univer status "$WB"
univer restore "$WB"
univer status "$WB"
```

Use `reset --soft HEAD~N` to remove the last N local unsynced commits and restore their mutations as uncommitted local mutations. Use `reset --hard HEAD~N` to remove the last N local unsynced commits and discard current uncommitted local mutations.

```bash
univer status "$WB"
univer reset "$WB" --soft HEAD~1
univer status "$WB"

univer reset "$WB" --hard HEAD~1
univer status "$WB"
```

`reset` only accepts `HEAD~N` targets and only operates on local unsynced commits. It does not rewrite synced changesets or remote history.

### Clone, Pull, And Sync

Use `clone` when a remote workbook unit already exists and you need a new local package path. The target `.univer` path must be nonexistent or empty.

```bash
WB=./budget.univer
univer clone "$WB" --unit-id unit-remote --json
univer status "$WB"
univer inspect workbook "$WB"
```

Use `pull` when you only need missing remote changesets for a package already bound to a remote unit. Use `sync` to sync local and remote versioning state.

```bash
univer status "$WB"
univer pull "$WB"
univer status "$WB"

univer commit "$WB" --message "Update review ranges"
univer sync "$WB"
univer status "$WB"
```

`sync` creates the remote workbook first when the package is still local-only. It pulls remote changes and pushes local changesets, but it does not push uncommitted local mutations. Remote endpoints come from `collaboration.defaultRemote` and `collaboration.remotes.<name>.url`.

### Export Handoff

Export after inspection proves the workbook state. Then prove the handoff file exists and, when useful, can be read back.

```bash
univer inspect workbook "$WB"
univer export "$WB" ./handoff.xlsx --json
test -s ./handoff.xlsx
univer import ./handoff.xlsx ./handoff.univer --json
univer inspect workbook ./handoff.univer
```

Use `.xlsx` for Excel handoff when workbook interoperability matters. Use CSV only when plain rectangular data is enough for the handoff.

## Shell-Native Rules

Use shell tools to reduce large ranges before bringing data back to the agent. `pipe out` should produce clean data; diagnostics and help belong outside the data stream.

- Keep ranges explicit and sheet-qualified.
- Quote the full A1 range string, especially for non-English or shell-sensitive sheet names.
- Prefer TSV for `awk` and JSON for `jq`.
- Stage intermediate files when you need a stable preview or assertion.
- Make `pipe in` the usual final pipeline stage.
- Verify with `inspect range` or `pipe out` after every writeback.

Avoid `pnpm dev -- ...` in clean pipeline examples. The pnpm/tsx wrapper can print logs to stdout and corrupt streamed data. Use the installed `univer`/`unv` executable or another entrypoint you have proven emits clean stdout.

## Gotchas

- `manifest.json` is metadata only. It does not prove sheet names, formulas, changed cells, or handoff correctness.
- Package contents are not a meaningful way to infer spreadsheet data. Use public CLI reads instead.
- Local file identity is the workbook path, such as `./budget.univer`, not `unitId`, `sessionId`, or manifest ids.
- Command success is not enough after import, mutation, export, or handoff. Verify workbook-visible state.
- A non-zero exit means the operation failed. Read stderr for the diagnostic, usage, and retry guidance.
- `search` may be unavailable or limited in some installed versions. Fall back to bounded `inspect range`.
- Quote the full range: `--range 'Sheet1!A1:J20'`, not just the sheet name fragment.
- Shell row counts can pass while headers, columns, or keys shift. Check headers, samples, and key columns together.
- `pipe in` writes parsed matrix data and reports a summary; it does not echo input.
- `view` is readonly preview. Do not treat it as mutation verification unless the task is visual review.
- Charts are maintained through `univer run` and the Pro Charts facade. Do not edit chart resource internals or expect `run` to export chart images.
- Shapes are maintained through `univer run` and the Pro Shapes facade. Do not inspect private drawing resource storage or expect `run` to export shape images.
- Floating images are maintained through `univer run` and the Sheets Drawing facade. Do not invent a top-level `univer image` command or inspect private drawing resource storage.
- `commit` is local only; use `sync` to push local changesets.
- `restore` discards only uncommitted local mutations; it does not remove local commits.
- `reset` is local-only and limited to `HEAD~N` over unsynced local commits. Do not use it as a remote revert or force-push workflow.
- `sync` does not push uncommitted local mutations. Commit verified workbook changes first.
- If `sync` reports an invalid remote binding, stop and diagnose the package or remote setup.
- `pull` requires a package already bound to a remote unit. Use `sync` for first remote creation or `clone --unit-id` for an existing remote unit.
- `clone` replaced older remote binding wording. Do not use or invent a `bind` command.
- If runtime-backed commands fail to start, inspect `univer daemon status` before retrying blindly.
- If workbook-visible reads disagree with package metadata, trust workbook-visible reads first.

## Support

Only enter support flow when the user asks to report a suspected CLI bug. Public issues: https://github.com/dream-num/skills/issues. Community support and builder discussions: https://discord.gg/nThHPupraR. Private artifacts: email developer@univer.ai; get authorization before guiding `univer doctor collect`.

Skill document revision: 2026-05-22.
