---
name: libreoffice-writer
description: Use when creating, editing, formatting, exporting, or extracting LibreOffice Writer (.odt) documents via UNO, including session-based edits, structured text targets, tables, images, lists, patch workflows, and snapshots.
---

# LibreOffice Writer

Use the bundled `writer` modules for UNO-backed Writer document work.
All paths must be **absolute**. Bundled modules live under `scripts/` in this
skill directory, so set `PYTHONPATH=<skill_base_dir>/scripts`.
If setup or runtime issues appear, check `references/troubleshooting.md`.

## API Surface

```python
# Non-session utilities
create_document(path)
export_document(path, output_path, export_format)   # formats: "pdf", "docx"
snapshot_page(doc_path, output_path, page=1, dpi=150)

# Session (primary editing API)
WriterSession(path) -> context manager

WriterSession methods:
  read_text(target: WriterTarget | None = None) -> str
  insert_text(text, target: WriterTarget | None = None)
  replace_text(target: WriterTarget, new_text)
  delete_text(target: WriterTarget)
  format_text(target: WriterTarget, formatting: TextFormatting)
  insert_table(rows, cols, data=None, name=None, target: WriterTarget | None = None)
  update_table(target: WriterTarget, data)
  delete_table(target: WriterTarget)
  insert_image(image_path, width=None, height=None, name=None, target: WriterTarget | None = None)
  update_image(target: WriterTarget, image_path=None, width=None, height=None)
  delete_image(target: WriterTarget)
  insert_list(items: list[ListItem], ordered: bool, target: WriterTarget | None = None)
  replace_list(target: WriterTarget, items: list[ListItem], ordered: bool | None = None)
  delete_list(target: WriterTarget)
  set_metadata(field, value)          # field: "title", "subject", "description", "author"
  get_metadata() -> dict[str, str]
  patch(patch_text, mode="atomic") -> PatchApplyResult
  export(output_path, export_format)
  reset()
  close(save=True)

# Standalone patch utility
patch(path, patch_text, mode="atomic") -> PatchApplyResult
```

## Structured Targets: `WriterTarget`

```python
from writer import WriterTarget

WriterTarget(
    kind="text" | "insertion" | "table" | "image" | "list",
    text=None,
    after=None,
    before=None,
    occurrence=None,
    name=None,
    index=None,
)
```

### Target kinds

| Kind | Supported fields | Use |
|---|---|---|
| `text` | `text`, `after`, `before`, `occurrence` | Read, replace, delete, or format matched text |
| `insertion` | `text`, `after`, `before`, `occurrence` | Insert at a resolved boundary or after a matched span |
| `table` | `name` or `index` | Update/delete a table |
| `image` | `name` or `index` | Update/delete an image |
| `list` | `text`, `after`, `before`, `occurrence` | Replace/delete one logical list block |

### Resolution rules

- Omit `target` to read the full document or append inserted content at the end.
- Use `after` and `before` to constrain a search window.
- Use `occurrence` when repeated text is expected; otherwise matching must be unique.
- Prefer full sentences or distinctive paragraph-sized phrases for `text`, `after`, and `before` anchors; single-word anchors are often too brittle for realistic prose edits.
- For table/image targets, prefer `name`; use `index` only when order is stable.
- For insertion after inline text, Writer inserts at the boundary after the matched span; paragraph breaks must come from the inserted text or the session helper.

## Formatting Payload

```python
from writer import TextFormatting

TextFormatting(
    bold=None,
    italic=None,
    underline=None,
    font_name=None,
    font_size=None,
    color=None,          # named color or integer
    align=None,          # "left" | "center" | "right" | "justify"
    line_spacing=None,
    spacing_before=None,
    spacing_after=None,
)
```

Notes:

- Character and paragraph formatting can be combined in one call.
- Paragraph properties such as `align` apply to the full paragraph containing the match, not just the exact matched span.
- At least one formatting field must be set.

## List Items

```python
from writer import ListItem

ListItem(text="Confirm scope", level=0)
```

- `level` is zero-based nesting.
- Nesting cannot skip levels.
- `ordered=True` uses a numbering style; `ordered=False` uses bullets.

## Patch DSL

Use `patch()` or `session.patch()` to apply ordered operations.

```ini
[operation]
type = format_text
target.kind = text
target.text = Quarterly revenue grew 18%.
target.after = Financial Summary
target.before = Action Items
format.bold = true
format.align = center

[operation]
type = insert_list
target.kind = insertion
target.after = Action Items
list.ordered = false
items <<JSON
[
  {"text": "Confirm scope", "level": 0},
  {"text": "Review output", "level": 0},
  {"text": "Update packaging", "level": 1}
]
JSON
```

### Supported operation types

- `insert_text`
- `replace_text`
- `delete_text`
- `format_text`
- `insert_table`
- `update_table`
- `delete_table`
- `insert_image`
- `update_image`
- `delete_image`
- `insert_list`
- `replace_list`
- `delete_list`

### Patch value rules

- Use `target.*` fields for target definition.
- Use `format.*` fields for formatting payloads.
- Use `list.ordered` plus JSON `items` for list operations.
- `items` and `data` must be valid JSON.
- Heredoc blocks are supported with `<<TAG ... TAG` for multiline text or JSON.

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

## Example: Edit a Report in Session

```python
from pathlib import Path

from writer import ListItem, TextFormatting, WriterSession, WriterTarget
from writer.core import create_document

output = str(Path("test-output/report.odt").resolve())
create_document(output)

with WriterSession(output) as session:
    session.insert_text(
        "Executive Summary\n\n"
        "Financial Summary\n\n"
        "Quarterly revenue grew 18%.\n\n"
        "Action Items"
    )
    session.format_text(
        WriterTarget(
            kind="text",
            text="Quarterly revenue grew 18%.",
            after="Financial Summary",
            before="Action Items",
        ),
        TextFormatting(bold=True, align="center"),
    )
    session.insert_list(
        [
            ListItem(text="Confirm scope", level=0),
            ListItem(text="Review output", level=0),
            ListItem(text="Update packaging", level=1),
        ],
        ordered=False,
        target=WriterTarget(kind="insertion", after="Action Items"),
    )
```

## Example: Patch an Existing Document

```python
from writer import patch

result = patch(
    "/abs/path/report.odt",
    """
    [operation]
    type = replace_text
    target.kind = text
    target.text = Draft
    new_text = Final

    [operation]
    type = update_table
    target.kind = table
    target.name = Summary
    data = [["Metric", "Value"], ["Revenue", "$2M"]]

    [operation]
    type = replace_list
    target.kind = list
    target.text = Confirm scope
    items = [{"text": "Approve release", "level": 0}, {"text": "Notify team", "level": 1}]
    list.ordered = true
    """,
    mode="best_effort",
)

print(result.overall_status)
```

## Snapshots

```python
from pathlib import Path
from writer import snapshot_page

result = snapshot_page(doc_path, "/tmp/page1.png", page=1, dpi=150)
print(result.file_path, result.width, result.height)
Path(result.file_path).unlink(missing_ok=True)   # cleanup used snapshots
```

Use snapshots to verify layout after formatting, list edits, image placement, or table changes.

## Common Mistakes

- Passing a relative path; UNO-facing Writer APIs expect absolute file paths.
- Omitting `occurrence` for repeated text and then getting an ambiguity error.
- Using anchors that are too short or too common; prefer full-sentence or paragraph-level anchor text plus `after` / `before` bounds when possible.
- Expecting `align` to apply only to a phrase; Writer applies paragraph alignment to the containing paragraph.
- Supplying malformed JSON in `items` or `data` patch fields.
- Calling `session.export()` or other methods after `session.close()`.
