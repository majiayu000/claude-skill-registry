---
name: flexcel-vcl
description: Use when writing Delphi / FreePascal / C++Builder code that reads, writes, manipulates, or exports Excel (.xlsx / .xls) files, generates PDF or HTML from Excel, or produces data-driven reports with FlexCel Studio for VCL and FireMonkey (TMS FlexCel). Triggers include Excel/xlsx from Delphi, TXlsFile, TFlexCelReport, TFlexCelPdfExport, TFlexCelHtmlExport, FireMonkey Excel export, Lazarus Excel, and Excel reporting from Pascal.
---

# FlexCel Studio for VCL / FireMonkey

This skill helps write Delphi (VCL, FMX, Lazarus/LCL, Linux/SKIA) and C++Builder code that uses **FlexCel** — the TMS Software library for working with Excel `.xlsx` / `.xls` files, exporting to PDF/HTML/images, and generating data-driven reports from templates.

## When to use this skill

Activate whenever the user wants to, from Pascal/Delphi/C++Builder code:

- **Read** an Excel file (`.xlsx` or `.xls`) — cell values, formulas, formatting.
- **Create or modify** an Excel file programmatically.
- **Generate reports** by merging data into Excel templates.
- **Export** an Excel file to **PDF**, **HTML**, **SVG**, or images.
- **Autofit** rows/columns, render sheets, or measure cells.
- Target **VCL, FireMonkey (desktop & mobile), Lazarus, or Delphi Linux**.

FlexCel does **not** require Excel or any Office installation on the target machine. It has no OLE/COM dependency.

## Two ways to create Excel files — pick one

Before writing code, decide which API fits the task:

| If the user wants to… | Use | Why |
|-----------------------|-----|-----|
| Read existing files, or build files cell-by-cell in code | **`TXlsFile` API** (`FlexCel.XlsAdapter`) | Full programmatic control; no designer required. |
| Produce the same report repeatedly from changing data, with a styled layout | **`TFlexCelReport` + Excel template** (`FlexCel.Report`) | Non-programmers can edit the template in Excel; code just provides data. |

When the user says "generate a report with company logo / nice formatting / many rows from a database", prefer **Reports**. When they say "read this file and extract values" or "create an Excel file with these calculations", prefer the **API**.

You can combine both: run a report to produce an in-memory `TXlsFile`, then manipulate it with the API, then export to PDF.

## Quick-start recipes

All examples assume VCL. For FireMonkey replace `FlexCel.VCLSupport` with `FlexCel.FMXSupport`; for Lazarus use `FlexCel.LCLSupport`; for Delphi Linux use `FlexCel.SKIASupport`. The platform support unit goes in the **main program (`.dpr`) uses clause only**, not every unit.

### Recipe 1 — Create an Excel file

```pascal
uses
  System.IOUtils,
  FlexCel.Core, FlexCel.XlsAdapter;

procedure CreateExcelFile;
var
  xls: TXlsFile;
begin
  // Start an empty workbook with 1 sheet and Excel-2019 default formatting.
  xls := TXlsFile.Create(1, TExcelFileFormat.v2019, true);
  try
    xls.SetCellValue(1, 1, 'Hello from FlexCel!');          // A1 text
    xls.SetCellValue(2, 1, 7);                              // A2 number
    xls.SetCellValue(3, 1, 11.3);                           // A3 number
    xls.SetCellValue(4, 1, TFormula.Create('=Sum(A2:A3)')); // A4 formula

    xls.Save(TPath.Combine(TPath.GetDocumentsPath, 'test.xlsx'));
  finally
    xls.Free;
  end;
end;
```

Key points:
- **All row/column/sheet indices are 1-based.** `(1, 1)` is cell `A1`. (XF format indices are the single exception — they're 0-based.)
- File format is inferred from the extension (`.xlsx` → OOXML, `.xls` → BIFF8).
- `TXlsFile` is a plain class, **not** a component — you create it in code and must `Free` it.

### Recipe 2 — Read an Excel file

```pascal
uses
  System.IOUtils,
  FlexCel.Core, FlexCel.XlsAdapter;

procedure ReadExcelFile(const aMemo: TMemo);
var
  xls: TXlsFile;
  row, colIndex, XF: integer;
  cell: TCellValue;
  addr: TCellAddress;
  s: string;
begin
  xls := TXlsFile.Create(TPath.Combine(TPath.GetDocumentsPath, 'test.xlsx'));
  try
    xls.ActiveSheetByName := 'Sheet1';   // or loop xls.ActiveSheet from 1 to xls.SheetCount
    for row := 1 to xls.RowCount do
    begin
      // Use ColCountInRow, NOT ColCount — much faster. See performance guide.
      for colIndex := 1 to xls.ColCountInRow(row) do
      begin
        XF := -1;
        cell := xls.GetCellValueIndexed(row, colIndex, XF);
        addr := TCellAddress.Create(row, xls.ColFromIndex(row, colIndex));

        s := 'Cell ' + addr.CellRef + ' ';
        if      cell.IsEmpty   then s := s + 'is empty.'
        else if cell.IsString  then s := s + 'string: '  + cell.ToString
        else if cell.IsNumber  then s := s + 'number: '  + FloatToStr(cell.AsNumber)
        else if cell.IsBoolean then s := s + 'bool: '    + BoolToStr(cell.AsBoolean)
        else if cell.IsError   then s := s + 'error: '   + cell.ToString
        else if cell.IsFormula then s := s + 'formula: ' + cell.AsFormula.Text;

        aMemo.Lines.Add(s);
      end;
    end;
  finally
    xls.Free;
  end;
end;
```

Key points:
- Iterate with **`ColCountInRow(row)`** combined with **`GetCellValueIndexed` + `ColFromIndex`** — this skips empty cells and is dramatically faster than a dense `1..ColCount` loop.
- `TCellValue` is a discriminated-union record. Test with `IsEmpty / IsString / IsNumber / IsBoolean / IsError / IsFormula`, then extract with `ToString / AsNumber / AsBoolean / AsFormula`.
- Excel dates are stored as numbers; detect them via the cell's format, not the value type.

### Recipe 3 — Export Excel to PDF

```pascal
uses
  FlexCel.Core, FlexCel.XlsAdapter, FlexCel.Render;

procedure XlsxToPdf(const Source, Dest: string);
var
  xls: TXlsFile;
  pdf: TFlexCelPdfExport;
begin
  xls := TXlsFile.Create(Source);
  try
    pdf := TFlexCelPdfExport.Create(xls);
    try
      pdf.Export(Dest);                   // one PDF covering all visible sheets
    finally
      pdf.Free;
    end;
  finally
    xls.Free;
  end;
end;
```

PDF export needs **`FlexCel.Render`** plus the platform-support unit in the main `.dpr` (the renderer uses the graphics engine for font measurement). For PDF/A, digital signatures, font embedding tuning, or multi-sheet bookmarks see `references/pdf-html-export.md`.

### Recipe 4 — Run a report from a template

Assume an Excel template `invoice-template.xlsx` already exists, with tags like `<#Customers.Name>` inside a named range `__Customers__` spanning the repeating row(s).

```pascal
uses
  FlexCel.Core, FlexCel.XlsAdapter, FlexCel.Report;

procedure RunReport(Customers: TDataSet);
var
  report: TFlexCelReport;
begin
  report := TFlexCelReport.Create(true);         // true = case-insensitive tags
  try
    report.AddTable('Customers', Customers, TDisposeMode.DoNotDispose);
    report.SetValue('ReportDate', Now);
    report.SetValue('CompanyName', 'Acme Corp');
    report.Run('invoice-template.xlsx', 'invoice-output.xlsx');
  finally
    report.Free;
  end;
end;
```

To write the **output straight to PDF**, run the report into a `TXlsFile` and pipe it through `TFlexCelPdfExport`:

```pascal
out := TXlsFile.Create;
try
  report.Run('template.xlsx', out);
  pdf := TFlexCelPdfExport.Create(out);
  try pdf.Export('report.pdf'); finally pdf.Free end;
finally
  out.Free;
end;
```

For the full tag language and template-design conventions see `references/reports-cheatsheet.md`.

## Unit reference (what to put in `uses`)

Always include **`FlexCel.Core`** in every unit that touches FlexCel types. Then add, per task:

| Task | Additional units |
|------|------------------|
| Platform graphics (main `.dpr` only) | `FlexCel.VCLSupport` / `FlexCel.FMXSupport` / `FlexCel.LCLSupport` / `FlexCel.SKIASupport` |
| Read / write xls/xlsx | `FlexCel.XlsAdapter` |
| PDF / HTML / image export, autofitting | `FlexCel.Render` |
| Low-level PDF access (sign, PDF/A options, standalone PDF) | `FlexCel.Pdf` |
| Template-based reports | `FlexCel.Report` |

## Critical gotchas (read this every time)

1. **1-based indexing** for rows, columns, sheets. `SetCellValue(1, 1, ...)` writes to `A1`. (XF format indices are 0-based.)
2. **Always `Free`** `TXlsFile`, `TFlexCelReport`, `TFlexCelPdfExport`, etc. They're plain classes, not components. Use `try..finally`.
3. **Don't iterate with `ColCount`** — it scans the whole sheet. Use `ColCountInRow(row)` + `GetCellValueIndexed` + `ColFromIndex`.
4. **Platform support unit belongs in the `.dpr` only**, not in every unit — it has no published types.
5. **Dates are numbers.** `GetCellValue` returns the serial date; check the cell's number format to know it's a date.
6. **Measurement units in Excel are unusual** — column widths are in 1/256 of a character, row heights in 1/20 of a point, etc. See the "Understanding Excel measurement units" tip in the docs before fiddling with widths/heights.
7. **Use APIMate.** When the user asks "how do I make a cell blue / add an autofilter / create a pivot table", the canonical answer is: do it in Excel, open the file in APIMate (ships with FlexCel), and copy the generated Delphi/C++ code. APIMate is the recommended way to discover API calls for anything Excel-specific. Mention this to the user.

## When to consult the references

Load a reference file only when the task actually needs it — keeps your context lean.

- **`references/api-cheatsheet.md`** — deeper `TXlsFile` usage: formatting, fonts, colors, merging, row/column sizing, comments, images, charts, data validation, protection, sheet management, streams.
- **`references/reports-cheatsheet.md`** — full tag reference, named-range conventions for bands, master-detail, config sheets, user functions, events.
- **`references/pdf-html-export.md`** — `TFlexCelPdfExport` and `TFlexCelHtmlExport` options: PDF/A, font embedding, digital signing, HTML5, image embedding.
- **`references/pitfalls.md`** — longer list of gotchas drawn from the official Tips section: locale, fonts on Docker/Linux, barcodes, tokens in formulas, strict xlsx, conditional formats, etc.

## When you need authoritative detail

The cheatsheets cover the common path. For anything deeper, fetch from the public documentation source:

- Markdown source (raw): `https://raw.githubusercontent.com/tmssoftware/TMS-FlexCel.VCL-doc-src/main/<path>.md`
  - Guides: `guides/api-developer-guide.md`, `guides/reports-developer-guide.md`, `guides/reports-tag-reference.md`, `guides/pdf-exporting-guide.md`, `guides/html-exporting-guide.md`, `guides/performance-guide.md`
  - Tips: `tips/<topic>.md` (one file per tip)
  - API reference: `api/FlexCel.XlsAdapter/TXlsFile/<MemberName>.md` and similar
- Rendered docs: `https://doc.tmssoftware.com/flexcel/vcl/index.html`
- Official sample repository (Delphi + C++Builder + FireMonkey): `https://github.com/tmssoftware/TMS-FlexCel.VCL-demos`

Use `WebFetch` on the raw markdown URL when you need to confirm a signature or pull an official example. Prefer the raw markdown over the rendered HTML.

## Style expectations for generated code

- Use `try..finally..Free` around every FlexCel object. Don't rely on interface reference counting — these are not interfaces.
- Use 1-based literals explicitly (`SetCellValue(1, 1, ...)`) — do not pretend indices are 0-based.
- Prefer the generic overloads (`TFormula.Create('=...')`, `TCellValue`) over implicit conversions when the intent is ambiguous.
- When exporting to PDF/HTML/images, include the platform-support unit in the example's `.dpr` block or mention it in a comment — otherwise rendering will fail at runtime with a missing-graphics-engine error.
- Don't invent method names. If unsure, check the API markdown under `api/<unit>/<class>/<member>.md` in the doc source, or tell the user to verify with APIMate.
