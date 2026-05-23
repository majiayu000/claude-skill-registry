---
name: automating-numbers
description: Automates Apple Numbers via JXA with AppleScript dictionary discovery. Use when asked to "automate Numbers spreadsheets", "create spreadsheets programmatically", "JXA Numbers scripting", or "bulk data operations in Numbers". Focuses on sheets, tables, ranges, batch I/O, clipboard shim, and high-performance data workflows.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Numbers (JXA-first, AppleScript discovery)

## Relationship to the macOS automation skill
- Standalone for Numbers, aligned with `automating-mac-apps` patterns.
- Use `automating-mac-apps` for permissions, shell, and UI scripting guidance.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core Framing
- Numbers AppleScript dictionary is AppleScript-first; discover there.
- JXA provides logic and data processing.
- Objects are specifiers; read via methods, write via assignments.
- Handle errors from Numbers operations using try/catch blocks and Application error checking.

## Workflow (default)
1) [ ] Discover terms in Script Editor (Numbers dictionary).
2) [ ] Prototype minimal AppleScript commands.
3) [ ] Port to JXA and add defensive checks.
4) [ ] Prefer batch reads and clipboard shim for writes.
5) [ ] Use UI scripting only for dictionary gaps.

## Validation Checklist
- [ ] Empty document handling works without errors
- [ ] Data integrity verified after batch operations
- [ ] Numbers UI remains responsive after automation runs
- [ ] Errors logged with specific Numbers object paths
- [ ] Sheet/table indices validated before access
- [ ] Clipboard shim restores original clipboard contents

## Examples

**Basic table read (JXA - Legacy):**
```javascript
const numbers = Application('Numbers');
const doc = numbers.documents[0];
const sheet = doc.sheets[0];
const table = sheet.tables[0];
const data = table.rows.whose({_not: [{cells: []}]})().map(row => row.cells().map(c => c.value()));
```

**Basic table read (PyXA - Recommended):**
```python
import PyXA

numbers = PyXA.Numbers()

# Get first document, sheet, and table
doc = numbers.documents()[0]
sheet = doc.sheets()[0]
table = sheet.tables()[0]

# Read all rows with data
rows = table.rows()
data = []

for row in rows:
    cells = row.cells()
    if cells:  # Skip empty rows
        row_data = [cell.value() for cell in cells]
        data.append(row_data)

print("Table data:", data)
```

**PyObjC with Scripting Bridge:**
```python
from ScriptingBridge import SBApplication

numbers = SBApplication.applicationWithBundleIdentifier_("com.apple.Numbers")

# Access document and table
doc = numbers.documents()[0]
sheet = doc.sheets()[0]
table = sheet.tables()[0]

# Read table data
rows = table.rows()
data = []

for row in rows:
    cells = row.cells()
    if cells:
        row_data = [cell.value() for cell in cells]
        data.append(row_data)

print("Table data:", data)
```

**Batch write with clipboard shim (JXA - Legacy):**
```javascript
const numbers = Application('Numbers');
// Prepare data array
const data = [['Name', 'Age'], ['Alice', 25], ['Bob', 30]];
// Use clipboard for bulk insertion
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.setTheClipboardTo(data.map(row => row.join('\t')).join('\n'));
numbers.activate();
delay(0.5);
// UI scripting to paste
SystemEvents = Application('System Events');
SystemEvents.keystroke('v', {using: 'command down'});
```

**Batch write (PyXA - Modern):**
```python
import PyXA

numbers = PyXA.Numbers()

# Prepare data
data = [
    ['Name', 'Age'],
    ['Alice', 25],
    ['Bob', 30]
]

# Get table to write to
doc = numbers.documents()[0]
sheet = doc.sheets()[0]
table = sheet.tables()[0]

# Clear existing data and write new data
table.clear()  # Clear table first

for i, row_data in enumerate(data):
    # Add row if needed
    if i >= len(table.rows()):
        table.rows().push({})

    # Set cell values
    row = table.rows()[i]
    for j, value in enumerate(row_data):
        if j >= len(row.cells()):
            row.cells().push({})
        cell = row.cells()[j]
        cell.value = value
```

**PyObjC Batch Write:**
```python
from ScriptingBridge import SBApplication

numbers = SBApplication.applicationWithBundleIdentifier_("com.apple.Numbers")

# Prepare data
data = [
    ['Name', 'Age'],
    ['Alice', 25],
    ['Bob', 30]
]

# Get table
doc = numbers.documents()[0]
sheet = doc.sheets()[0]
table = sheet.tables()[0]

# Clear and write data
table.clear()

for i, row_data in enumerate(data):
    # Ensure row exists
    while len(table.rows()) <= i:
        table.rows().push({})

    row = table.rows()[i]

    for j, value in enumerate(row_data):
        # Ensure cell exists
        while len(row.cells()) <= j:
            row.cells().push({})

        cell = row.cells()[j]
        cell.value = value
```

## When Not to Use
- General macOS automation without Numbers involvement
- AppleScript alone suffices (no JXA logic needed)
- Complex UI interactions beyond data operations (use `automating-mac-apps`)
- Cross-platform compatibility required (use CSV/pandas)
- Real-time collaborative editing scenarios

## What to load
- JXA Numbers basics: `automating-numbers/references/numbers-basics.md`
- Recipes (tables, ranges, formatting): `automating-numbers/references/numbers-recipes.md`
- Advanced patterns (clipboard, performance, ObjC): `automating-numbers/references/numbers-advanced.md`
- Dictionary translation table: `automating-numbers/references/numbers-dictionary.md`
- Formulas and locale notes: `automating-numbers/references/numbers-formulas.md`
- Sorting patterns: `automating-numbers/references/numbers-sorting.md`
- UI scripting patterns: `automating-numbers/references/numbers-ui-scripting.md`
- **PyXA API Reference** (complete class/method docs): `automating-numbers/references/numbers-pyxa-api-reference.md`