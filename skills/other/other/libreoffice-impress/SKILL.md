---
name: libreoffice-impress
description: Use when creating, editing, formatting, or extracting LibreOffice Impress (.odp) presentations via UNO, including session-based slide edits, structured targets, lists, tables, charts, media, notes, master pages, patch workflows, and snapshots.
---

# LibreOffice Impress

Use the bundled `impress` modules for UNO-backed Impress presentation work.
All paths must be **absolute**. Bundled modules live under `scripts/` in this
skill directory, so set `PYTHONPATH=<skill_base_dir>/scripts`.
If setup or runtime issues appear, check `references/troubleshooting.md`.

## API Surface

```python
# Non-session utilities
create_presentation(path)
get_slide_count(path)
export_presentation(path, output_path, export_format)   # formats: "pdf", "pptx"
snapshot_slide(doc_path, slide_index, output_path, width=1280, height=720)

# Session (primary editing API)
ImpressSession(path) -> context manager

ImpressSession methods:
  get_slide_count() -> int
  get_slide_inventory(target: ImpressTarget) -> dict[str, object]
  add_slide(index=None, layout="BLANK")
  delete_slide(target: ImpressTarget)
  move_slide(target: ImpressTarget, to_index)
  duplicate_slide(target: ImpressTarget)
  delete_item(target: ImpressTarget)
  read_text(target: ImpressTarget) -> str
  insert_text(text, target: ImpressTarget | None = None)
  replace_text(target: ImpressTarget, new_text)
  format_text(target: ImpressTarget, formatting: TextFormatting)
  insert_list(items: list[ListItem], ordered: bool, target: ImpressTarget | None = None)
  replace_list(target: ImpressTarget, items: list[ListItem], ordered: bool | None = None)
  insert_text_box(slide: ImpressTarget, text, placement: ShapePlacement, name=None)
  insert_shape(slide: ImpressTarget, shape_type, placement: ShapePlacement, fill_color=None, line_color=None, name=None)
  insert_image(slide: ImpressTarget, image_path, placement: ShapePlacement, name=None)
  replace_image(target: ImpressTarget, image_path=None, placement: ShapePlacement | None = None)
  insert_table(slide: ImpressTarget, rows, cols, placement: ShapePlacement, data=None, name=None)
  update_table(target: ImpressTarget, data)
  insert_chart(slide: ImpressTarget, chart_type, data, placement: ShapePlacement, title=None, name=None)
  update_chart(target: ImpressTarget, chart_type=None, data=None, placement: ShapePlacement | None = None, title=None)
  insert_media(slide: ImpressTarget, media_path, placement: ShapePlacement, name=None)
  replace_media(target: ImpressTarget, media_path=None, placement: ShapePlacement | None = None)
  set_notes(target: ImpressTarget, text)
  get_notes(target: ImpressTarget) -> str
  list_master_pages() -> list[str]
  apply_master_page(target: ImpressTarget, master_target: ImpressTarget)
  set_master_background(target: ImpressTarget, color)
  import_master_page(template_path) -> str
  patch(patch_text, mode="atomic") -> PatchApplyResult
  export(output_path, export_format)
  reset()
  close(save=True)

# Standalone patch utility
patch(path, patch_text, mode="atomic") -> PatchApplyResult
```

## Structured Targets: `ImpressTarget`

```python
from impress import ImpressTarget

ImpressTarget(
    kind=(
        "slide" | "shape" | "text" | "table" | "chart" |
        "media" | "notes" | "master_page" | "list" | "insertion" | "image"
    ),
    slide_index=None,
    shape_name=None,
    shape_index=None,
    shape_type=None,
    placeholder=None,
    text=None,
    after=None,
    before=None,
    occurrence=None,
    master_name=None,
)
```

### Target kinds

| Kind | Supported fields | Use |
|---|---|---|
| `slide` | `slide_index` | Slide inventory, deletion, move, duplicate, master-page application |
| `shape` | `slide_index` plus `shape_name` or `shape_index` | Read/delete one generic shape |
| `image` | `slide_index` plus `shape_name` or `shape_index` | Replace/delete one image |
| `table` | `slide_index` plus `shape_name` or `shape_index` | Update/delete one table |
| `chart` | `slide_index` plus `shape_name` or `shape_index` | Update/delete one chart |
| `media` | `slide_index` plus `shape_name` or `shape_index` | Replace/delete one media object |
| `text` | slide-scoped selectors plus `text`, `after`, `before`, `occurrence` | Read, replace, delete, or format text |
| `list` | slide-scoped text selectors | Replace/delete one structural list block |
| `insertion` | slide-scoped selectors plus anchors | Insert text or a list |
| `notes` | `slide_index` plus optional text bounds | Read or replace speaker notes |
| `master_page` | `master_name` | Resolve one master page |

### Resolution rules

- Slide indices are zero-based.
- `shape_name` and `shape_index` are mutually exclusive.
- `placeholder` targets support explicit values such as `title`, `body`, and `subtitle`.
- Use `after` and `before` to narrow text or list resolution inside one resolved text-bearing object.
- For object targets, prefer `shape_name`; use `shape_index` only when slide order is stable.
- `delete_item()` accepts any non-slide delete target: `text`, `notes`, `list`, `shape`, `image`, `table`, `chart`, or `media`.

## Formatting Payload: `TextFormatting`

```python
from impress import TextFormatting

TextFormatting(
    bold=None,
    italic=None,
    underline=None,
    font_name=None,
    font_size=None,
    color=None,          # named color or integer
    align=None,          # "left" | "center" | "right" | "justify" | "start" | "end"
)
```

Notes:

- At least one formatting field must be set.
- Color accepts a named color or `0xRRGGBB` integer.
- Paragraph alignment is applied through the same formatting payload as character styling.

## Geometry Payload: `ShapePlacement`

```python
from impress import ShapePlacement

ShapePlacement(x_cm=1.0, y_cm=2.0, width_cm=8.0, height_cm=4.0)
```

- Geometry values are in centimetres.
- Width and height must be positive.

## List Items

```python
from impress import ListItem

ListItem(text="Confirm scope", level=0)
```

- `level` is zero-based nesting.
- Nesting cannot skip levels.
- List editing is structural; do not add manual `- ` prefixes.
- Headless snapshot rendering may not visibly paint bullets even when list metadata is correct.

## Patch DSL

Use `patch()` or `session.patch()` to apply ordered operations.

```ini
[operation]
type = replace_text
target.kind = text
target.slide_index = 2
target.placeholder = body
target.text = Quarterly revenue rose 18%
new_text = Quarterly revenue rose 21%

[operation]
type = insert_list
target.kind = insertion
target.slide_index = 2
target.shape_name = Agenda Box
target.after = Action Items
list.ordered = false
items <<JSON
[
  {"text": "Confirm scope", "level": 0},
  {"text": "Review outputs", "level": 0},
  {"text": "Update notes", "level": 1}
]
JSON

[operation]
type = delete_item
target.kind = chart
target.slide_index = 4
target.shape_name = Disposable Chart
```

### Supported operation types

- `add_slide`
- `delete_slide`
- `move_slide`
- `duplicate_slide`
- `insert_text`
- `replace_text`
- `format_text`
- `insert_list`
- `replace_list`
- `insert_text_box`
- `insert_shape`
- `delete_item`
- `insert_image`
- `replace_image`
- `insert_table`
- `update_table`
- `insert_chart`
- `update_chart`
- `insert_media`
- `replace_media`
- `set_notes`
- `apply_master_page`
- `set_master_background`

### Patch value rules

- Use `target.*` fields for the primary target.
- Use `master.*` fields for `apply_master_page`.
- Use `format.*` fields for `TextFormatting`.
- Use `placement.*` fields for `ShapePlacement`.
- Use `list.ordered` plus JSON `items` for list operations.
- `items` and `data` must be valid JSON.
- Heredoc blocks are supported with `<<TAG ... TAG` for multiline text or JSON.

### Modes

- `atomic` stops on first failure, restores the original file bytes, and persists nothing.
- `best_effort` keeps successful earlier operations and records later failures.

`PatchApplyResult` fields:

- `mode`
- `overall_status` = `"ok" | "partial" | "failed"`
- `operations` = list of `PatchOperationResult`
- `document_persisted`

For standalone `patch(path, ...)`, `document_persisted` means the changes were
saved to disk. For `session.patch(...)`, it means the patch produced successful
mutations in the current open session state.

## Example: Edit a Deck in Session

```python
from pathlib import Path

from impress import (
    ImpressSession,
    ImpressTarget,
    ListItem,
    ShapePlacement,
    TextFormatting,
)
from impress.core import create_presentation

output = str(Path("test-output/demo.odp").resolve())
create_presentation(output)

with ImpressSession(output) as session:
    session.add_slide(layout="TITLE_AND_CONTENT")
    session.replace_text(
        ImpressTarget(kind="text", slide_index=1, placeholder="title"),
        "Executive Summary",
    )
    session.replace_text(
        ImpressTarget(kind="text", slide_index=1, placeholder="body"),
        "Quarterly revenue rose 18%.",
    )
    session.insert_text_box(
        ImpressTarget(kind="slide", slide_index=1),
        "Action Items",
        ShapePlacement(1.0, 5.0, 10.0, 4.0),
        name="Agenda Box",
    )
    session.insert_list(
        [
            ListItem(text="Confirm scope", level=0),
            ListItem(text="Review output", level=0),
            ListItem(text="Update packaging", level=1),
        ],
        ordered=False,
        target=ImpressTarget(
            kind="insertion",
            slide_index=1,
            shape_name="Agenda Box",
            after="Action Items",
        ),
    )
    session.format_text(
        ImpressTarget(
            kind="text",
            slide_index=1,
            placeholder="body",
            text="Quarterly revenue rose 18%.",
        ),
        TextFormatting(bold=True, align="center"),
    )
```

## Example: Patch an Existing Presentation

```python
from impress import patch

result = patch(
    "/abs/path/demo.odp",
    """
    [operation]
    type = replace_text
    target.kind = text
    target.slide_index = 1
    target.placeholder = body
    new_text = Quarterly revenue rose 21%.

    [operation]
    type = insert_media
    target.kind = slide
    target.slide_index = 1
    media_path = /abs/path/demo.wav
    placement.x_cm = 1.0
    placement.y_cm = 9.0
    placement.width_cm = 5.0
    placement.height_cm = 3.0
    name = Demo Media

    [operation]
    type = delete_item
    target.kind = media
    target.slide_index = 1
    target.shape_name = Demo Media
    """,
    mode="best_effort",
)

print(result.overall_status)
```

## Snapshots

```python
from pathlib import Path
from impress import snapshot_slide

result = snapshot_slide(doc_path, 0, "/tmp/slide1.png")
print(result.file_path, result.width, result.height)
Path(result.file_path).unlink(missing_ok=True)   # clean up used snapshots
```

Use snapshots to verify slide layout after text edits, master-page changes,
table/chart placement, or other visual operations.

## Common Mistakes

- Passing a relative path; UNO-facing Impress APIs expect absolute file paths.
- Using one-based slide indices.
- Using fragile single-word text anchors when a fuller phrase is available.
- Expecting exact shape names after LibreOffice-native slide duplication; UNO may rename duplicates such as `Name 1`.
- Supplying malformed JSON in `items` or `data` patch fields.
- Forgetting to clean up captured snapshots after inspection.
- Calling session methods after `session.close()`.
- The `"start"` and `"end"` paragraph alignment options require LibreOffice 26.2+.
