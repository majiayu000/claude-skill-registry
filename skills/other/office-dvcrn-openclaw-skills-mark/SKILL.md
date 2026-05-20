---
name: Office
description: "Master Excel, Word, PowerPoint, and Google Workspace with formulas, formatting, and automation."
---

## What "Office" Means Here

Productivity software: Microsoft 365, Google Workspace, and office administration.

| Signal | Context | Load |
|--------|---------|------|
| Formulas, pivot tables, VLOOKUP, macros | Spreadsheets | `tools/spreadsheets.md` |
| Formatting, headers, mail merge, TOC | Documents | `tools/documents.md` |
| Slides, animations, presenter view | Presentations | `tools/presentations.md` |
| Supplies, vendors, facilities, space | Office admin | `admin/facilities.md` |

---

## Spreadsheets (Excel / Google Sheets)

**Formulas people actually need:**
- `VLOOKUP` / `XLOOKUP` — lookup value in table, return another column
- `SUMIF` / `COUNTIF` — sum/count with conditions
- `INDEX/MATCH` — more flexible than VLOOKUP
- `IF` with `AND`/`OR` — conditional logic

**Common problems:**
- VLOOKUP returns #N/A → check for spaces, data types, exact match setting
- Formula works in one cell, breaks when copied → missing `$` for absolute references
- Dates sorting wrong → format as actual dates, not text

**Pivot tables:** Right-click data → Create Pivot Table → drag fields to rows/columns/values.

---

## Documents (Word / Google Docs)

**Formatting essentials:**
- Use Styles (Heading 1, 2, 3) for structure — enables automatic TOC
- Page numbers starting on page 3: Insert break → Different First Page → start numbering
- Different headers per section: Section breaks, unlink from previous

**Mail Merge:**
1. Prepare data source (Excel with columns: Name, Address, etc.)
2. Word → Mailings → Start Mail Merge → Letters
3. Insert Merge Fields where dynamic content goes
4. Preview Results → Finish & Merge

---

## Presentations (PowerPoint / Google Slides)

**Professional basics:**
- Slide Master for consistent styling (View → Slide Master)
- 6x6 rule: max 6 bullets, 6 words per bullet
- One idea per slide

**Animations:**
- Entrance animations for bullet reveal (Appear > Fade > Fly In)
- Timing: On Click vs After Previous
- Keep it subtle — animation should aid, not distract

**Presenter View:** F5 to present, use Presenter View to see notes while audience sees slides.

---

## Office Administration

For those managing physical office operations:

**Supplies & Inventory:**
- Track with simple spreadsheet: Item, Quantity, Reorder Point, Supplier
- Set calendar reminders for regular orders
- Bulk ordering usually 15-30% cheaper

**Vendor Management:**
- Cleaning, maintenance, IT support contracts
- Document SLAs and contact info in shared location
- Review contracts annually for renegotiation

**Space Planning:**
- Hot-desking: Use booking system (even a shared calendar works)
- Meeting room: Clear naming, visible displays, 15-min buffers

---

## Quick Reference

| Task | Excel/Sheets | Word/Docs | PowerPoint/Slides |
|------|-------------|-----------|-------------------|
| Find value | VLOOKUP/XLOOKUP | Find & Replace | Find & Replace |
| Conditional format | Home → Conditional | N/A | N/A |
| Auto-update content | Formulas | Fields | Links |
| Export to PDF | File → Save As | File → Save As | File → Save As |
