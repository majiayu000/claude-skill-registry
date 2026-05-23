---
name: flexcel-net
description: Use when writing C# / VB.NET / F# code that reads, writes, manipulates, or exports Excel (.xlsx / .xls) files, generates PDF or HTML from Excel, or produces data-driven reports with FlexCel Studio for .NET (TMS Software). Triggers include Excel/xlsx from C#, XlsFile, FlexCelReport, FlexCelPdfExport, FlexCelHtmlExport, FlexCelImgExport, ExcelFile, PdfWriter, .NET Excel export, ASP.NET Excel generation, .NET MAUI Excel, Native AOT + Excel, and Excel reporting from .NET.
---

# FlexCel Studio for .NET

This skill helps write **C# / VB.NET / F#** code that uses **FlexCel** — the TMS Software library for working with Excel `.xlsx` / `.xls` files, exporting to PDF / HTML / SVG / images, and generating data-driven reports from templates. Works with .NET Framework 4.6+, .NET Core / .NET 5+, .NET Standard 2.0+, .NET MAUI, Xamarin, and .NET 9 Native AOT (with caveats — see below).

## When to use this skill

Activate whenever the user wants to, from .NET code:

- **Read** an Excel file (`.xlsx` or `.xls`) — cell values, formulas, formatting.
- **Create or modify** an Excel file programmatically.
- **Generate reports** by merging data into Excel templates.
- **Export** an Excel file to **PDF**, **HTML**, **SVG**, or images.
- **Autofit** rows/columns, render sheets, or measure cells.
- Target **.NET Framework, .NET Core / .NET 5+, .NET MAUI, Xamarin, Blazor server, ASP.NET Core**, or **Native AOT**.

FlexCel does **not** require Excel or any Office installation on the target machine. No OLE/COM, no interop. Fully managed — works on Windows, Linux, macOS, iOS, and Android.

## Two ways to create Excel files — pick one

Before writing code, decide which API fits the task:

| If the user wants to… | Use | Why |
|-----------------------|-----|-----|
| Read existing files, or build files cell-by-cell in code | **`XlsFile` API** (`FlexCel.XlsAdapter`) | Full programmatic control; no designer required; Native-AOT-safe. |
| Produce the same report repeatedly from changing data, with a styled layout | **`FlexCelReport` + Excel template** (`FlexCel.Report`) | Non-programmers can edit the template in Excel; code only provides data. |

When the user says "generate a report with company logo / nice formatting / many rows from a database", prefer **Reports**. When they say "read this file and extract values" or "create an Excel file with these calculations", prefer the **API**.

You can combine both: run a report to produce an in-memory `XlsFile`, then manipulate it with the API, then export to PDF.

## Package and namespace reference

**NuGet package:** `TMS.FlexCel` (includes almost all functionality). Install via `dotnet add package TMS.FlexCel` **after configuring the TMS NuGet source** — FlexCel is hosted at TMS's own NuGet feed, not on nuget.org. See `guides/installation-guide.md` in the doc source for feed setup.

Optional companion packages:
- `TMS.FlexCel.WinForms` — WinForms preview / grid components.
- `TMS.FlexCel.WebForms` — legacy WebForms viewer (rarely needed).

**Namespaces — add per task:**

| Task | `using` |
|------|---------|
| Any FlexCel code | `using FlexCel.Core;` |
| Read / write xls/xlsx | `using FlexCel.XlsAdapter;` |
| PDF / HTML / image export, autofitting | `using FlexCel.Render;` |
| Low-level PDF access (sign, PDF/A, standalone PDF) | `using FlexCel.Pdf;` |
| Template-based reports | `using FlexCel.Report;` |
| WinForms components | `using FlexCel.Winforms;` |
| ASP.NET helpers | `using FlexCel.AspNet;` |

**Note:** Unlike the VCL edition, `.NET` has **no platform-support unit/assembly** to register in the entry point — all platform integration ships with the core package. Just reference `TMS.FlexCel` and you're done.

## Critical gotchas (read this every time)

1. **1-based indexing** for rows, columns, and sheets. `xls.SetCellValue(1, 1, ...)` writes to `A1`. XF (format) indices are the single exception — they are **0-based**.
2. **No `T` prefix on class names.** VCL has `TXlsFile`, `TFlexCelReport`, `TFlexCelPdfExport`. .NET has **`XlsFile`**, **`FlexCelReport`**, **`FlexCelPdfExport`**. However value-type structs keep the `T` — `TFormula`, `TFlxFormat`, `TCellAddress`, `TRichString`, `TExcelFileFormat`, `TFlxFormulaErrorValue`.
3. **`GetCellValue` returns `object`.** There is no `TCellValue` discriminated union in .NET. Dispatch with `is` pattern matching:
   ```csharp
   if (cell == null)                       { /* empty */ }
   else if (cell is string s)              { /* plain text */ }
   else if (cell is TRichString rs)        { /* rich text */ }
   else if (cell is double d)              { /* number (dates too!) */ }
   else if (cell is bool b)                { /* boolean */ }
   else if (cell is TFlxFormulaErrorValue) { /* #DIV/0 etc. */ }
   else if (cell is TFormula f)            { /* formula */ }
   ```
4. **Never iterate with `ColCount`** — it scans the whole sheet. Use `ColCountInRow(row)` + `GetCellValueIndexed(row, colIdx, ref XF)` + `ColFromIndex(row, colIdx)` — this is sparse-aware and dramatically faster on real files.
5. **Dates are `double`.** Excel stores dates as numbers with a date format. Cell returns `double`. Check the cell's XF number-format to know it's a date (or use `TFlxNumberFormat.FormatValue` helpers).
6. **Memory.** `XlsFile`, `FlexCelReport`, and the export classes hold the full workbook in memory. They are fully managed — GC handles cleanup. However, the export classes (`FlexCelPdfExport`, `FlexCelHtmlExport`, `FlexCelImgExport`) and `FlexCelReport` **implement `IDisposable`**; wrap them in `using`. `XlsFile` does **not** require `using`, but don't hold big workbooks as long-lived statics.
7. **Use APIMate.** For anything Excel-specific ("how do I add a data validation / a conditional format / a chart / a pivot table?"), the canonical answer is: build it in Excel → open the file in **APIMate** (ships with FlexCel, also available for Linux and macOS) → copy the generated C# or VB.NET code. Tell the user this.
8. **Native AOT** (.NET 9+): `XlsFile` and the exporters are fully supported. `FlexCelReport` uses reflection on your POCO types — annotate them with `[DynamicallyAccessedMembers(...)]` or reports fail silently after trimming. See `references/pitfalls.md`.

## Quick-start recipes

All examples are C#. For VB.NET, translate syntactically — APIs are identical.

### Recipe 1 — Create an Excel file

```csharp
using System;
using System.IO;
using FlexCel.Core;
using FlexCel.XlsAdapter;

class Program
{
    static void Main()
    {
        // Empty workbook: 1 sheet, Excel-2019 default formatting.
        var xls = new XlsFile(1, TExcelFileFormat.v2019, true);

        xls.SetCellValue(1, 1, "Hello from FlexCel!");       // A1 text
        xls.SetCellValue(2, 1, 7);                           // A2 number (stored as double)
        xls.SetCellValue(3, 1, 11.3);                        // A3 number
        xls.SetCellValue(4, 1, new TFormula("=Sum(A2:A3)")); // A4 formula

        xls.Save(Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.Personal),
            "test.xlsx"));
    }
}
```

Key points:
- Indices are **1-based**: `(1, 1)` = `A1`.
- File format is inferred from the extension (`.xlsx` → OOXML, `.xls` → BIFF8). Override via `xls.Save(stream, TFileFormats.Xlsx)` when saving to streams.
- `SetCellValue(1, 1, "7")` writes a **string** `"7"`; `SetCellValue(1, 1, 7)` writes a **number** `7`. Type dispatch happens through method overloads.

### Recipe 2 — Read an Excel file

```csharp
using System;
using System.IO;
using FlexCel.Core;
using FlexCel.XlsAdapter;

void ReadExcel(string path)
{
    var xls = new XlsFile(path);
    xls.ActiveSheetByName = "Sheet1";   // or: xls.ActiveSheet = 1..xls.SheetCount

    for (int row = 1; row <= xls.RowCount; row++)
    {
        // Use ColCountInRow, NOT ColCount — much faster. See performance guide.
        for (int colIndex = 1; colIndex <= xls.ColCountInRow(row); colIndex++)
        {
            int XF = -1;
            object cell = xls.GetCellValueIndexed(row, colIndex, ref XF);
            var addr = new TCellAddress(row, xls.ColFromIndex(row, colIndex));

            string kind =
                cell == null                    ? "empty"
              : cell is TRichString             ? "rich string"
              : cell is string                  ? "string"
              : cell is double                  ? "number"
              : cell is bool                    ? "bool"
              : cell is TFlxFormulaErrorValue   ? "error"
              : cell is TFormula                ? "formula"
              :                                   "unknown";

            Console.WriteLine($"Cell {addr.CellRef} {kind}: {cell}");
        }
    }
}
```

Key points:
- **Iterate with `ColCountInRow` + `GetCellValueIndexed` + `ColFromIndex`**. The three together skip empty cells and give you the real column number of each non-empty cell.
- `GetCellValueIndexed` takes XF **by `ref`** and writes the cell's format index into it.
- `cell == null` means the cell is empty (never allocated). A cell containing an empty string is a different thing.

### Recipe 3 — Export Excel to PDF

```csharp
using FlexCel.Core;
using FlexCel.XlsAdapter;
using FlexCel.Render;

void XlsxToPdf(string src, string dst)
{
    var xls = new XlsFile(src);
    using var pdf = new FlexCelPdfExport(xls, true);  // true = allow overwrite
    pdf.Export(dst);                                  // all visible sheets, honoring Excel page setup
}
```

For PDF/A, font subsetting, digital signatures, multi-workbook PDFs, or tuning fonts on Linux/Docker see `references/pdf-html-export.md`.

### Recipe 4 — Run a report from a template

Assume an Excel template `invoice-template.xlsx` already exists, with tags like `<#Customers.Name>` inside a named range `__Customers__` spanning the repeating row(s).

```csharp
using System;
using System.Data;
using FlexCel.Core;
using FlexCel.XlsAdapter;
using FlexCel.Report;

void RunReport(DataTable customers)
{
    using var report = new FlexCelReport(true);   // true = allow overwrite

    // Supply data sources
    report.AddTable("Customers", customers);      // DataTable / DataSet / IEnumerable<T>

    // Scalar values
    report.SetValue("ReportDate", DateTime.Now);
    report.SetValue("CompanyName", "Acme Corp");

    report.Run("invoice-template.xlsx", "invoice-output.xlsx");
}
```

**AddTable overloads** (the most common):

```csharp
report.AddTable("Customers", customerList);          // IEnumerable<T> / List<T> / IQueryable<T>
report.AddTable("Customers", customerDataTable);     // DataTable
report.AddTable(customerDataSet);                    // DataSet — each contained DataTable by name
report.AddTable(myCustomerList);                     // single-arg: band name inferred from type name
```

**To output directly to PDF** — run the report into a fresh `XlsFile`, then pipe that through `FlexCelPdfExport`:

```csharp
var outXls = new XlsFile();
report.Run("template.xlsx", outXls);
using var pdf = new FlexCelPdfExport(outXls, true);
pdf.Export("report.pdf");
```

For the full tag language and template-design conventions see `references/reports-cheatsheet.md`.

## When to consult the references

Load a reference file only when the task actually needs it — keeps context lean for simple tasks.

- **`references/api-cheatsheet.md`** — deeper `XlsFile` / `ExcelFile` usage: formatting, fonts, colors, merging, row/column sizing, comments, images, charts, data validation, protection, named ranges, `InsertAndCopyRange` / `DeleteRange` / `MoveRange`, sheet management, streams, recalc, virtual mode.
- **`references/reports-cheatsheet.md`** — full tag reference, named-range conventions for bands, master-detail, config sheets, user functions, events.
- **`references/pdf-html-export.md`** — `FlexCelPdfExport`, `FlexCelHtmlExport`, `FlexCelImgExport` options: PDF/A, font embedding, digital signing, HTML5, image embedding, multi-workbook PDFs.
- **`references/pitfalls.md`** — extended gotchas, Native AOT specifics, Docker/Linux fonts, locale, barcodes, conditional formats, strict xlsx.

## When you need authoritative detail

The cheatsheets cover the common path. For anything deeper, fetch from the public documentation source:

- **Markdown source (raw):** `https://raw.githubusercontent.com/tmssoftware/TMS-FlexCel.NET-doc-src/main/<path>.md`
  - Guides: `guides/api-developer-guide.md`, `guides/reports-developer-guide.md`, `guides/reports-tag-reference.md`, `guides/pdf-exporting-guide.md`, `guides/html-exporting-guide.md`, `guides/performance-guide.md`, `guides/multiplatform-guide.md`
  - Tips: `tips/<topic>.md` (one file per tip — includes `native-aot.md`)
  - API reference: `api/FlexCel.XlsAdapter/XlsFile/<MemberName>.md`, `api/FlexCel.Report/FlexCelReport/<MemberName>.md`, etc.
- **Rendered docs:** `https://doc.tmssoftware.com/flexcel/net/index.html`
- **Official sample repository (C# + VB.NET, desktop + mobile):** `https://github.com/tmssoftware/TMS-FlexCel.NET-demos`

Use `WebFetch` on the raw markdown URL when you need to confirm a signature or pull an official example. Prefer the raw markdown over the rendered HTML.

## Style expectations for generated code

- Use `using` declarations / blocks for `FlexCelReport`, `FlexCelPdfExport`, `FlexCelHtmlExport`, `FlexCelImgExport`. They're `IDisposable`.
- `XlsFile` does **not** implement `IDisposable`; don't wrap it in `using`. Let it go out of scope and GC will collect it.
- Use 1-based literals explicitly (`SetCellValue(1, 1, ...)`) — never pretend indices are 0-based.
- Use `is` pattern matching (or switch expressions on type) for `GetCellValue` results — don't cast blindly.
- When providing PDF font folders, fall back gracefully: on Linux/macOS/Docker the fonts used by the workbook may not exist on the target. Use `FlexCelPdfExport.GetFontFolder` or `GetFontData` events.
- For **Native AOT**: always annotate POCOs passed to `FlexCelReport.AddTable` with `[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicProperties | DynamicallyAccessedMemberTypes.PublicMethods)]`. Without it, trimming will silently strip property accessors.
- Don't invent method names. If unsure, check the API markdown under `api/<namespace>/<class>/<member>.md` in the doc source, or tell the user to verify with APIMate.
