---
name: automating-excel
description: Automates Microsoft Excel on macOS via JXA with AppleScript dictionary discovery. Use when asked to "automate Excel spreadsheets", "JXA Excel scripting", "Excel macOS automation", or "bulk Excel data operations". Focuses on workbooks, worksheets, ranges, 2D arrays, performance toggles, and VBA escape hatches.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Excel (JXA-first, AppleScript discovery)

## Relationship to the macOS automation skill
- Standalone for Excel, but aligned with `automating-mac-apps` patterns.
- Use `automating-mac-apps` for permissions, shell, and UI scripting guidance.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core Framing
- Excel AppleScript dictionary is AppleScript-first; use Script Editor for discovery.
- JXA is the production language for logic and data processing.
- Collections are specifiers; read via methods, set via assignments.
- Handle errors from Excel operations using try/catch blocks and Application error checking.

## Workflow (default)
1) [ ] Discover dictionary terms in Script Editor (Excel).
2) [ ] Prototype a minimal AppleScript command.
3) [ ] Port to JXA and add defensive checks.
4) [ ] Use bulk read/write (2D arrays) for performance.
5) [ ] Use VBA `run()` when dictionary coverage is missing.

## Validation Steps
- Test with empty documents to verify error handling
- Verify data integrity after batch operations
- Check Excel UI responsiveness after automation runs
- Log errors with specific Excel object paths for debugging

## Examples

**Basic workbook read:**
```javascript
const Excel = Application('Microsoft Excel');
const workbook = Excel.workbooks[0];
const worksheet = workbook.worksheets['Sheet1'];
const range = worksheet.ranges['A1:B10'];
const data = range.value();  // Returns 2D array
```

**Bulk write with performance toggle:**
```javascript
Excel.screenUpdating = false;
Excel.calculation = 'manual';
try {
  const range = worksheet.ranges['C1:D100'];
  range.value = my2DArray;
} finally {
  Excel.calculate();
  Excel.screenUpdating = true;
}
```

**VBA escape hatch:**
```javascript
Excel.run('MyMacro', {arg1: 'value', arg2: 123});  // Calls VBA subroutine
```

## When Not to Use
- For general macOS automation without Excel involvement
- When AppleScript alone suffices (no JXA logic needed)
- For Excel tasks requiring complex UI interactions (use `automating-mac-apps` for that)
- When cross-platform compatibility is required

## What to load
- JXA Excel basics: `automating-excel/references/excel-basics.md`
- Recipes (ranges, 2D arrays, formatting): `automating-excel/references/excel-recipes.md`
- Advanced patterns (performance toggles, VBA bridge): `automating-excel/references/excel-advanced.md`
- Pivot table guidance: `automating-excel/references/excel-pivots.md`
- Charting guidance: `automating-excel/references/excel-charts.md`
- Dictionary translation table: `automating-excel/references/excel-dictionary.md`
- PyXA (Python) alternative: `automating-excel/references/excel-pyxa.md`