---
name: libreoffice-calc
description: Use when creating, editing, formatting, exporting, or extracting LibreOffice Calc (.ods) spreadsheets via UNO, including session-based cell and range edits, sheets, named ranges, validation, charts, patch workflows, and snapshots.
---

# LibreOffice Calc

Use the bundled `calc` modules for UNO-backed Calc spreadsheet work.
All paths must be **absolute**. Bundled modules live under `scripts/` in this
skill directory, so set `PYTHONPATH=<skill_base_dir>/scripts`.
If setup or runtime issues appear, check `references/troubleshooting.md`.

## API Surface

```python
# Non-session utilities
create_spreadsheet(path)
export_spreadsheet(path, output_path, export_format)   # formats: "pdf", "xlsx", "csv"
snapshot_area(doc_path, output_path, sheet="Sheet1", row=0, col=0, width=None, height=None, dpi=150)

# Session (primary editing API)
CalcSession(path) -> context manager

CalcSession methods:
  read_cell(target: CalcTarget) -> dict[str, object]
  write_cell(target: CalcTarget, value, value_type="auto")
  read_range(target: CalcTarget) -> list[list[dict[str, object]]]
  write_range(target: CalcTarget, data)
  format_range(target: CalcTarget, formatting: CellFormatting)
  list_sheets() -> list[dict[str, object]]
  add_sheet(name, index=None)
  rename_sheet(target: CalcTarget, new_name)
  delete_sheet(target: CalcTarget)
  define_named_range(name, target: CalcTarget)
  get_named_range(target: CalcTarget) -> dict[str, object]
  delete_named_range(target: CalcTarget)
  set_validation(target: CalcTarget, rule: ValidationRule)
  clear_validation(target: CalcTarget)
  create_chart(target: CalcTarget, spec: ChartSpec)
  update_chart(target: CalcTarget, spec: ChartSpec)
  delete_chart(target: CalcTarget)
  recalculate()
  patch(patch_text, mode="atomic") -> PatchApplyResult
  export(output_path, export_format)
  reset()
  close(save=True)

# Standalone patch utility
patch(path, patch_text, mode="atomic") -> PatchApplyResult
```

## Structured Targets: `CalcTarget`

```python
from calc import CalcTarget

CalcTarget(
    kind="cell" | "range" | "sheet" | "named_range" | "chart",
    sheet=None,
    sheet_index=None,
    row=None,
    col=None,
    end_row=None,
    end_col=None,
    name=None,
    index=None,
)
```

### Target kinds

| Kind | Supported fields | Use |
|---|---|---|
| `cell` | `sheet` or `sheet_index`, `row`, `col` | Read or write one cell |
| `range` | `sheet` or `sheet_index`, `row`, `col`, `end_row`, `end_col` | Read, write, format, validate, or chart a rectangular range |
| `sheet` | `sheet` or `sheet_index` | Rename or delete one sheet |
| `named_range` | `name` | Inspect or delete one named range |
| `chart` | `sheet` or `sheet_index`, plus `name` or `index` | Update or delete one chart |

### Resolution rules

- Coordinates are zero-based and must be non-negative.
- `sheet` and `sheet_index` are mutually exclusive.
- `name` and `index` are mutually exclusive.
- Range targets must keep `end_row >= row` and `end_col >= col`.
- Chart targets must identify one sheet plus one chart selector.
- Calc does not auto-convert a one-cell range into a cell target; keep those shapes explicit.

## Cell Read Results

`read_cell()` and `read_range()` return cell dictionaries with the same shape:

```python
{
    "value": 100.0,
    "formula": None,
    "error": None,
    "type": "number",
    "raw": 100.0,
}
```

Formula cells use `type="formula"`; when Calc reports a formula error, `error`
is populated and `value` becomes `None`.

## Formatting Payload: `CellFormatting`

```python
from calc import CellFormatting

CellFormatting(
    bold=None,
    italic=None,
    font_name=None,
    font_size=None,
    color=None,          # named color or integer
    number_format=None,  # "currency" | "percentage" | "date" | "time"
)
```

Notes:

- At least one formatting field must be set.
- `color` accepts a named color or `0xRRGGBB` integer.
- `format_range()` works for both a `cell` target and a rectangular `range` target.

## Validation Payload: `ValidationRule`

```python
from calc import ValidationRule

ValidationRule(
    type="whole",
    condition="between",
    value1=1,
    value2=10,
    show_error=True,
    error_message="Enter a value from 1 to 10.",
    show_input=True,
    input_title="Allowed values",
    input_message="Only integers from 1 to 10 are valid.",
    ignore_blank=True,
    error_style=0,
)
```

Supported `type` values:

- `any`
- `whole`
- `decimal`
- `date`
- `time`
- `text_length`
- `list`

Supported `condition` values:

- `between`
- `not_between`
- `equal`
- `not_equal`
- `greater_than`
- `less_than`
- `greater_or_equal`
- `less_or_equal`

## Chart Payload: `ChartSpec`

```python
from calc import CalcTarget, ChartSpec

ChartSpec(
    chart_type="line",
    data_range=CalcTarget(
        kind="range",
        sheet="Data",
        row=0,
        col=0,
        end_row=5,
        end_col=1,
    ),
    anchor_row=7,
    anchor_col=0,
    width=10000,
    height=7000,
    title="Revenue Trend",
)
```

Notes:

- `chart_type` must be one of `bar`, `line`, `pie`, or `scatter`.
- `width` and `height` use Calc chart rectangle units (the same units the packaged API already accepts).
- Create charts by targeting a sheet; update or delete charts by targeting a chart.

## Patch DSL

Use `patch()` or `session.patch()` to apply ordered spreadsheet operations.

```ini
[operation]
type = write_range
target.kind = range
target.sheet = Revenue Data
target.row = 0
target.col = 0
target.end_row = 2
target.end_col = 1
data <<JSON
[["Label", "Value"], ["Revenue", 100], ["Cost", 80]]
JSON

[operation]
type = format_range
target.kind = range
target.sheet = Revenue Data
target.row = 1
target.col = 1
target.end_row = 2
target.end_col = 1
format.number_format = currency
format.bold = true

[operation]
type = create_chart
target.kind = sheet
target.sheet = Revenue Data
chart.chart_type = line
chart.data_range.kind = range
chart.data_range.sheet = Revenue Data
chart.data_range.row = 0
chart.data_range.col = 0
chart.data_range.end_row = 2
chart.data_range.end_col = 1
chart.anchor_row = 5
chart.anchor_col = 0
chart.width = 9000
chart.height = 6000
chart.title = Revenue Trend
```

### Supported operation types

- `write_cell`
- `write_range`
- `format_range`
- `add_sheet`
- `rename_sheet`
- `delete_sheet`
- `define_named_range`
- `delete_named_range`
- `set_validation`
- `clear_validation`
- `create_chart`
- `update_chart`
- `delete_chart`
- `recalculate`

### Patch value rules

- Use `target.*` fields for the primary target.
- Use `format.*` fields for `CellFormatting`.
- Use `rule.*` fields for `ValidationRule`.
- Use `chart.*` fields for `ChartSpec`; chart source ranges use `chart.data_range.*`.
- `data` must be valid JSON.
- Heredoc blocks are supported with `<<TAG ... TAG` for multiline JSON or text.

### Modes

- `atomic` stops on first failure, resets the session, and persists nothing.
- `best_effort` keeps successful earlier operations and records failures.

`PatchApplyResult` fields:

- `mode`
- `overall_status` = `"ok" | "partial" | "failed"`
- `operations` = list of `PatchOperationResult`
- `document_persisted`

For standalone `patch(path, ...)`, `document_persisted` means the changes were
saved to disk. For `session.patch(...)`, it means the patch produced successful
mutations in the current open session state.

## Example: Build a Spreadsheet in Session

```python
from pathlib import Path

from calc import (
    CalcSession,
    CalcTarget,
    CellFormatting,
    ChartSpec,
    ValidationRule,
)
from calc.core import create_spreadsheet

output = str(Path("test-output/revenue-report.ods").resolve())
create_spreadsheet(output)

with CalcSession(output) as session:
    session.rename_sheet(CalcTarget(kind="sheet", sheet="Sheet1"), "Revenue Data")
    session.add_sheet("Summary")
    session.write_range(
        CalcTarget(kind="range", sheet="Revenue Data", row=0, col=0, end_row=2, end_col=1),
        [["Label", "Value"], ["Revenue", 100], ["Cost", 80]],
    )
    session.format_range(
        CalcTarget(kind="range", sheet="Revenue Data", row=1, col=1, end_row=2, end_col=1),
        CellFormatting(number_format="currency", bold=True),
    )
    session.define_named_range(
        "RevenueValues",
        CalcTarget(kind="range", sheet="Revenue Data", row=1, col=1, end_row=2, end_col=1),
    )
    session.set_validation(
        CalcTarget(kind="range", sheet="Revenue Data", row=1, col=1, end_row=2, end_col=1),
        ValidationRule(type="whole", condition="greater_than", value1=0),
    )
    session.create_chart(
        CalcTarget(kind="sheet", sheet="Revenue Data"),
        ChartSpec(
            chart_type="line",
            data_range=CalcTarget(
                kind="range",
                sheet="Revenue Data",
                row=0,
                col=0,
                end_row=2,
                end_col=1,
            ),
            anchor_row=5,
            anchor_col=0,
            width=9000,
            height=6000,
            title="Revenue Trend",
        ),
    )
    session.recalculate()
```

## Example: Patch an Existing Spreadsheet

```python
from calc import patch

result = patch(
    "/abs/path/revenue-report.ods",
    """
    [operation]
    type = write_cell
    target.kind = cell
    target.sheet = Summary
    target.row = 1
    target.col = 1
    value = Ready
    value_type = text

    [operation]
    type = format_range
    target.kind = cell
    target.sheet = Summary
    target.row = 1
    target.col = 1
    format.bold = true

    [operation]
    type = recalculate
    """,
    mode="best_effort",
)

print(result.overall_status)
```

## Snapshots

```python
from pathlib import Path
from calc import snapshot_area

result = snapshot_area(doc_path, "/tmp/revenue.png", sheet="Revenue Data", row=0, col=0, dpi=150)
print(result.file_path, result.width, result.height)
Path(result.file_path).unlink(missing_ok=True)   # cleanup used snapshots
```

Use snapshots to verify chart placement, formatting, and sheet layout before delivery.

## Common Mistakes

- Passing a relative path; UNO-facing Calc APIs expect absolute file paths.
- Mixing up `cell` and `range` targets; Calc keeps them distinct even for one-cell selections.
- Using one-based coordinates; rows and columns are zero-based.
- Assuming `create_chart()` picks a random later target name; when `title` is set, targeting the chart by that same name is the safest follow-up pattern.
- Forgetting `chart.data_range.*` fields when patching chart operations.
- Expecting exact requested PNG dimensions from `snapshot_area()`; Calc export can differ by a small amount.
- Calling session methods after `session.close()`.
