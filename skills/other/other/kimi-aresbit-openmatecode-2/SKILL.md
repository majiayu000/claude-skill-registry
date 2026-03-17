---
name: docx
description: Generate and edit Word documents (.docx). Supports professional documents including covers, charts, track-changes editing, and more. Suitable for any .docx creation or modification task.
---

# Part 1: Goals

## ⚠️ When to Unzip vs Read

**To preserve ANY formatting from the source document, MUST unzip and parse XML.**

Read tool returns plain text only — fonts, colors, alignment, borders, styles are lost.

| Need | Method |
|------|--------|
| Text content only (summarize, analyze, translate) | Read tool is fine |
| Formatting info (copy styles, preserve layout, template filling) | Unzip and parse XML |
| Structure + comments/track changes | `pandoc input.docx -t markdown` |

## Core Principles

1. **Preserve formatting** — When editing existing documents, retain original formatting. Clone and modify, never recreate.

2. **Correct feature implementation** — Comments need multi-file sync. Track Changes need revision marks. Use the right structure.

**Never use python-docx/docx-js as fallback.** These libraries produce lower quality output than direct XML manipulation.

## Source Principle

**Template provided = Act as form-filler, not designer.**
- Format is the user's decision
- Task: replace placeholders, not redesign
- Like filling a PDF form—do not redesign

**No template = Act as designer.** Design freely based on scenario.

For .doc (legacy format), first convert with `libreoffice --headless --convert-to docx`.

---

# Part 2: Execution

## File Structure

```
docx/
├── SKILL.md                      ← This file (entry point + reference)
├── references/
│   └── EditingGuide.md           → Complete Python editing tutorial (comments, track changes, 5-file sync)
├── scripts/
│   ├── docx                      → Unified entry (the only script to call)
│   ├── fix_element_order.py      → Auto-fix XML element ordering
│   ├── validate_docx.py          → Business rule validation
│   ├── generate_backgrounds.py       → Morandi style backgrounds
│   ├── generate_inkwash_backgrounds.py → Ink-wash style backgrounds
│   └── generate_chart.py         → matplotlib (only for heatmaps/3D/radar; simple charts must use native)
├── assets/
│   └── templates/
│       ├── KimiDocx.csproj       → Project file template (for creating new docs)
│       ├── Program.cs            → Program entry template
│       ├── Example.cs            → Complete example (cover+TOC+charts+back cover)
│       ├── CJKExample.cs         → CJK content patterns (quote escaping, fonts)
│       └── xml/                  → XML templates for comments infrastructure
└── validator/                    → OpenXML validator (pre-compiled binary, AI does not modify)
```

**Creating new documents**: Use C# SDK with `./scripts/docx build` → See `Example.cs` for patterns, `CJKExample.cs` for CJK content
**Editing existing documents**: Use Python + lxml → See `references/EditingGuide.md` for complete tutorial

⚠️ **Do NOT mix these approaches.** C# SDK for creation, Python for editing. Never use python-docx/docx-js.

## Environment Setup

First time, execute in the SKILL directory:

```bash
cd /app/.kimi/skills/docx/
./scripts/docx init
```

**Fixed Path Conventions** (cannot be changed):

| Path | Purpose |
|------|---------|
| `/app/.kimi/skills/docx/` | SKILL directory, where commands are executed |
| `/tmp/docx-work/` | Working directory, edit `Program.cs` here |
| `/mnt/okcomputer/output/` | Output directory, final deliverables |
| `/mnt/okcomputer/upload/` | User upload location (input files) |

**Script Commands** (`./scripts/docx <cmd>`):

| Command | Purpose |
|---------|---------|
| `env` | Show environment status (no changes) |
| `init` | Setup dependencies + workspace |
| `build [out]` | Compile, run, validate (default: output/output.docx) |
| `validate FILE` | Validate existing docx |

The script automatically handles:
- Detects dotnet/python3 (required), pandoc/playwright/matplotlib (optional)
- Installed → use directly; Not installed → auto-install; Broken → repair
- Initializes working directory, copies template files

## Build Process

**Must use `./scripts/docx build`**, do not execute `dotnet build && dotnet run` separately (skips validation).

### Program.cs Output Path Convention (Critical)

**Program.cs must get output path from command line arguments**, otherwise build script cannot find the generated file:

```csharp
// Correct - get output path from command line arguments
string outputFile = args.Length > 0 ? args[0] : "/mnt/okcomputer/output/output.docx";

// Wrong - hardcoded path causes build failure
string outputFile = "my_document.docx";  // Script can't find file!
```

| Step | Action | Notes |
|------|--------|-------|
| 1. Compile | `dotnet build` | Provides fix suggestions on failure |
| 2. Generate | `dotnet run -- <output path>` | Path passed via command line args |
| 3. Auto-fix | `fix_element_order.py` | Fixes XML element ordering issues |
| 4. OpenXML validation | `validator/` | Mandatory |
| 5. Business rules | `validate_docx.py` | Mandatory |
| 6. Statistics | Character + word count | Optional (requires pandoc) |

**Validation is mandatory**: On failure, file is kept but warnings are shown. Check error messages to fix issues.

### Standalone Validation

```bash
cd /app/.kimi/skills/docx/
./scripts/docx validate /mnt/okcomputer/output/report.docx
```

### Content Verification (Mandatory)

**pandoc is the SOURCE OF TRUTH.** OpenXML validator checks structure; pandoc shows actual content.

Before delivery, verify with pandoc:
- `pandoc output.docx -t plain` — check text completeness
- For revisions/comments: add `--track-changes=all` to verify marker positions

**⚠️ Critical**: `comments.xml` exists ≠ comments visible. Count mismatch = `doc_tree` not saved. See `references/EditingGuide.md` §5.3.

---

# Part 3: Quality Standards

## Delivery Standard

**Generic styling and mediocre aesthetics = mediocre delivery.**

Deliver studio-quality Word documents with deep thought on content, functionality, and styling. Users often don't explicitly request advanced features (covers, TOC, backgrounds, back covers, footnotes, charts)—deeply understand needs and proactively extend.

## Language Consistency

**Document language = User conversation language** (including filename, body text, headings, headers, TOC hints, chart labels, and all other text).

## Headers and Footers - REQUIRED BY DEFAULT

Most documents **MUST** include headers and footers. The specific style (alignment, format, content) should match the document's overall design.

- **Header**: Typically document title, company name, or chapter name
- **Footer**: Typically page numbers (format flexible: "X / Y", "Page X", "— X —", etc.)
- **Cover/Back cover**: Use `TitlePage` setting to hide header/footer on first page

## Professional Elements (Critical)

Create documents that exceed user expectations, proactively add professional elements, don't wait for users to ask. **Delivery standard: Visual quality of a top designer in 2024.**

**Cover & Visual:**
- Formal documents (proposals, reports, financials, bids, contracts) / creative documents (invitations, greeting cards) must have **cover and back cover**
- Covers must have designer-quality background images
- Body pages can optionally include backgrounds to enhance visual appeal

**Structure:**
- Long documents (3+ sections) add TOC, must add refresh hint after TOC

**Data Presentation:**
- When comparing data or showing trends, use charts instead of plain text lists
- Tables use light gray headers or three-line style, avoid Word default blue

**Links & References:**
- URLs must be clickable hyperlinks
- Multiple figures/tables add numbering and cross-references ("see Figure 1", "as shown in Table 2")
- Academic/legal/data analysis citation scenarios implement correct in-text click-to-jump references with corresponding footnotes/endnotes

### TOC Refresh Hint

Word TOC is field code, page numbers may be inaccurate when generated. **Must add gray hint text after TOC**, informing users to manually refresh:

```
Table of Contents
─────────────────
Chapter 1 Overview .......................... 1
Chapter 2 Methods ........................... 3
...

(Hint: On first open, right-click the TOC and select "Update Field" to show correct page numbers)
```

**Hint text requirements**:
- Visually subtle — gray color, smaller font size, should not compete with actual TOC entries
- Language: **Matches user conversation language**

### Only When User Explicitly Requests

| Feature | Reason |
|---------|--------|
| Watermark | Changes visual state. **SDK limitation**: VML watermark classes don't serialize correctly; must write raw XML to header. |
| Document protection | Restricts editing |
| Mail merge fields | Requires data source |

### Chart Selection Strategy (Critical)

**Default to native Word charts**, editable, small file size, professional.

| Chart Type | Method | Notes |
|------------|--------|-------|
| Pie chart | **Native** | `Example.cs` → `AddPieChart()` |
| Bar chart | **Native** | `Example.cs` → `AddBarChart()` |
| Line chart | **Native** | Reference bar chart structure, use `c:lineChart` |
| Horizontal bar | **Native** | Reference bar chart structure, use `barDir="bar"` |
| Heatmap, 3D, radar | matplotlib | Word native doesn't support |
| Complex statistics (box plot, etc.) | matplotlib | Word native doesn't support |

Native charts are preferred (editable, smaller files), but matplotlib is acceptable for data analysis scenarios.

### Inserting Images/Charts

Any PNG (matplotlib charts, backgrounds, photos) must be inserted using `AddInlineImage()`:

```csharp
AddInlineImage(body, mainPart, "/path/to/image.png", "Description", docPrId++);
```

**Critical**:
- Chart labels/titles must match document language (e.g., Chinese labels for Chinese docs)
- Build output shows `X images` — if 0, images were not inserted

## Content Constraints

### Word/Page Count Requirements

| User Request | Execution Standard |
|--------------|-------------------|
| Specific word count (e.g., "3000 words") | Actual output within ±20% |
| Specific page count (e.g., "5 pages") | Exact match |
| Range (e.g., "2000-3000 words") | Within range |
| Minimum (e.g., "at least 5000 words") | No more than 2x the requirement |

**Forbidden**: Padding word count with excessive bullet point lists. Maintain information density.

### Outline Adherence

- **User provides outline**: Follow strictly, no additions, deletions, or reordering
- **No outline provided**: Use standard structure
  - Academic: Introduction → Literature → Methods → Results → Discussion → Conclusion
  - Business: Executive Summary → Analysis → Recommendations
  - Technical: Overview → Principles → Usage → Examples → FAQ

### Scene Completeness

Think one step ahead of the user, complete elements the scenario needs. **Examples below are not exhaustive — apply this principle to ALL document types:**

- **Exam paper** → Name/class/ID fill areas, point allocation per question (consider total), grading section
- **Contract** → Signature and seal areas for both parties, date, contract number, attachment list
- **Meeting minutes** → Attendees, absentees, action items with owners, next meeting time

## Design Philosophy

### Color Scheme

**Low saturation tones**, avoid Word default blue and matplotlib default high saturation.

**Flexibly choose** color schemes based on document scenario:

| Style | Palette | Suitable Scenarios |
|-------|---------|-------------------|
| Morandi | Soft muted tones | Artistic, editorial |
| Earth tones | Brown, olive, natural | Environmental, organic |
| Nordic | Cool gray, misty blue | Minimalist, tech |
| Japanese Wabi-sabi | Gray, raw wood, zen | Traditional, contemplative |
| French elegance | Off-white, dusty pink | Luxury, feminine |
| Industrial | Charcoal, rust, concrete | Manufacturing, engineering |
| Academic | Navy, burgundy, ivory | Research, education |
| Ocean mist | Misty blue, sand | Marine, wellness |
| Forest moss | Olive, moss green | Nature, sustainability |
| Desert dusk | Ochre, sandy gold | Warm, regional |

**Color scheme must be consistent within the same document.**

### Layout

White space (margins, paragraph spacing), clear hierarchy (H1 > H2 > body), proper padding (text shouldn't touch borders).

### Pagination Control

Word uses flow layout, not fixed pages. Control pagination with these properties:

| Property | XML | Effect |
|----------|-----|--------|
| Keep with next | `<w:keepNext/>` | Heading stays on same page as following paragraph |
| Keep lines together | `<w:keepLines/>` | Paragraph won't break across pages |
| Page break before | `<w:pageBreakBefore/>` | Force new page (for H1) |
| Widow/orphan control | `<w:widowControl/>` | Prevent single lines at top/bottom of page |

```csharp
// Example: H1 always starts on new page, stays with next paragraph
new ParagraphProperties(
    new ParagraphStyleId { Val = "Heading1" },
    new PageBreakBefore(),
    new KeepNext(),
    new KeepLines()
)
```

**Table pagination**:
```csharp
// Allow row to break across pages (avoid large blank areas)
new TableRowProperties(
    new CantSplit { Val = false }  // false = can split
)

// Repeat header row on each page
new TableRowProperties(
    new TableHeader()
)
```

---

# Part 4: Technical Reference

**Choose your path:**

| Task | Stack | Reference |
|------|-------|-----------|
| Create new document | C# + OpenXML SDK | 4.1-4.6 + `Example.cs` |
| Edit existing document | Python + lxml | 4.7 + `references/EditingGuide.md` |

---

## 4.1 SDK Fundamentals

### Schema Compliance (MEMORIZE THESE)

OpenXML has strict element ordering requirements. **Wrong order = Word cannot open the file.**

#### Required Styles

```csharp
// Normal style must exist - all Heading styles use basedOn="Normal"
styles.Append(new Style(
    new StyleName { Val = "Normal" },
    new StyleParagraphProperties(
        new SpacingBetweenLines { After = "200", Line = "276", LineRule = LineSpacingRuleValues.Auto }
    ),
    new StyleRunProperties(
        new RunFonts { Ascii = "Calibri", HighAnsi = "Calibri" },
        new FontSize { Val = "22" },
        new FontSizeComplexScript { Val = "22" }
    )
) { Type = StyleValues.Paragraph, StyleId = "Normal", Default = true });
```

#### Element Order Rules

Most ordering issues are auto-fixed by `fix_element_order.py`. Key rules to remember:

| Parent | Key Rule |
|--------|----------|
| **`sectPr`** | `headerRef` → `footerRef` must come before `pgSz` → `pgMar` |
| **`Table`** | Must have `tblGrid` between `tblPr` and `tr` (see below) |

#### Tables Must Have tblGrid

```csharp
// Correct - table must define grid
var table = new Table();
table.Append(new TableProperties(...));
table.Append(new TableGrid(           // Required!
    new GridColumn { Width = "4680" },
    new GridColumn { Width = "4680" }
));
table.Append(new TableRow(...));

// Wrong - missing tblGrid, Word cannot open
var table = new Table();
table.Append(new TableProperties(...));
table.Append(new TableRow(...));  // Adding rows directly
```

#### Table Column Width Consistency

Main cause of skewed tables: `gridCol` width in `tblGrid` doesn't match cell's `tcW` width.

```csharp
// Correct - gridCol and tcW match exactly
table.Append(new TableGrid(
    new GridColumn { Width = "3600" },  // First column
    new GridColumn { Width = "5400" }   // Second column
));

var row = new TableRow(
    new TableCell(
        new TableCellProperties(
            new TableCellWidth { Width = "3600", Type = TableWidthUnitValues.Dxa }  // Matches gridCol!
        ),
        new Paragraph(new Run(new Text("Content")))
    ),
    new TableCell(
        new TableCellProperties(
            new TableCellWidth { Width = "5400", Type = TableWidthUnitValues.Dxa }  // Matches gridCol!
        ),
        new Paragraph(new Run(new Text("Content")))
    )
);
```

| Rule | Reason |
|------|--------|
| gridCol count = table column count | Otherwise column width calculation fails |
| gridCol.Width = tcW.Width | Mismatch causes skewing (checked during validation) |
| All rows in same column use same tcW | Maintains column width consistency |

#### Value Limits

- `paraId` must be < `0x80000000` (for comment paragraph IDs)

### Creation vs Editing

| Task | Method | Why |
|------|--------|-----|
| Create new document | C# OpenXML SDK | Handles package structure, rels, Content_Types automatically |
| Edit existing document | Python + lxml | Transparent, no black box, full control |

**For creating new documents**: Use `Example.cs` patterns with SDK.

**For editing existing documents**: See `references/EditingGuide.md` for complete Python workflow.

---

### Example.cs

**Read the entire file to understand the overall structure**, not just individual functions. The file demonstrates how sections connect (cover → TOC → body → back cover).

The "Project Proposal", "[Company Name]", etc. in Example are **example content only**, and the color scheme is **for reference only**.

| What to Learn | What NOT to Learn |
|---------------|-------------------|
| Section division (cover → TOC → body → back cover) | Specific color values |
| Floating background insertion code | Business content from the example |
| Chart creation API calls | Copy/wording from the example |
| Style definition structure | Hardcoded data from the example |

⚠️ **Do NOT copy the Example's color scheme.** Redesign visual style based on YOUR document's scenario, like a top designer.

**Function Index** (read source for implementation details):

| Feature | Function | Line # |
|---------|----------|--------|
| **Document Structure** | | |
| Styles (Normal, Heading1-3) | `AddStyles()` | 85-203 |
| Cover page | `AddCoverSection()` | 369-453 |
| Table of contents | `AddTocSection()` | 458-526 |
| Body section | `AddContentSection()` | 531-729 |
| Back cover | `AddBackcoverSection()` | 734-794 |
| **Visual Elements** | | |
| Floating background | `CreateFloatingBackground()` | 228-279 |
| Proportional inline image | `AddInlineImage()` | 285-364 |
| **Tables** | | |
| Three-line table | `CreateDataTable()` | 853-888 |
| Header row (gray bg) | `CreateSimpleHeaderRow()` | 933-971 |
| Data row | `CreateSimpleDataRow()` | 976-1008 |
| **Charts** | | |
| Pie chart | `AddPieChart()` | 1013-1049 |
| Bar chart | `AddBarChart()` | 1133-1169 |
| **Page Elements** | | |
| Header with background | within `AddContentSection()` | 534-575 |
| Footer with page numbers | within `AddContentSection()` | 578-588 |
| Page number field | `CreatePageNumberField()` | 1345-1354 |
| Total pages field | `CreateTotalPagesField()` | 1356-1365 |
| **Advanced Features** | | |
| Footnote | `AddFootnote()` | 1370-1410 |
| Cross-reference | `CreateCrossReference()` | 1415-1425 |
| Numbering/lists | `CreateBasicNumbering()` | 1327-1340 |

### CJKExample.cs

**CJK documents must read `CJKExample.cs` only** — reading `Example.cs` instead will cause errors (missing font config, quote escaping). It handles:
- Quote escaping (`""` → `\u201c` `\u201d`)
- CJK font configuration (SimHei, Microsoft YaHei)
- Paragraph indentation for CJK text

Structure is identical to `Example.cs` — no need to read both.

## 4.2 Content Elements

### Field Codes

PAGE/NUMPAGES/DATE/TOC — structure: `FieldChar(Begin)` → `FieldCode(" PAGE ")` → `FieldChar(Separate)` → `Text` → `FieldChar(End)`. Results cached; WPS doesn't support `UpdateFieldsOnOpen`.

### Bookmarks and Cross-References

Bookmarks mark positions (`BookmarkStart`/`BookmarkEnd` with matching IDs); cross-references link via REF field (`" REF bookmarkName \\h "`).

**Pitfall**: Deleting bookmarked text deletes bookmark → "Error! Reference source not found".

## 4.3 Visual Design

### Background Image Design

Cover/back cover must have background. Background images should have center white space, use low saturation colors. Background images must NOT contain any text; text should be implemented in Word for user editability.

#### Design Flow

1. **Read example**: Read `scripts/generate_backgrounds.py` for HTML/CSS techniques (radial-gradient, transparency, positioning)
2. **Choose direction**: Select a style direction from the table below based on document scenario
3. **Create original**: Write new HTML/CSS from scratch—the example shows ONE style, yours should be different

⚠️ **Copying the example = all documents look the same = mediocre delivery.** Each document deserves a unique visual identity matching its content and purpose.

#### Style Reference

| Style | Key Elements | Scenarios |
|-------|--------------|-----------|
| MUJI | Thin borders + white space | Minimalist, Japanese, lifestyle |
| Bauhaus | Scattered geometric shapes | Art, design, creative |
| Swiss Style | Grid lines + accent bars | Professional, corporate |
| Soft Blocks | Soft color rectangles, overlapping transparent | Warm, education, healthcare |
| Rounded Geometry | Rounded rectangles, pill shapes | Tech, internet, youthful |
| Frosted Glass | Blur + transparency + subtle borders | Modern, premium, tech |
| Gradient Ribbons | Soft gradient ellipses + small dots | Feminine, beauty, soft |
| Dot Matrix | Regular dot pattern texture | Technical, data, engineering |
| Double Border | Nested borders + corner decorations | Traditional, formal, legal |
| Waves | Bottom SVG waves + gradient background | Ocean, environmental, flowing |
| Warm Natural | Earth tones + organic shapes | Environmental, agriculture, natural |

**Technical**: Playwright generates 794×1123px (`device_scale_factor=2`), insert as floating Anchor with `BehindDoc=true`. See `Example.cs:CreateFloatingBackground()`.

### Letterhead (Business Documents)

For formal business letters, consider adding a letterhead in the header area. Common patterns:
- **Full letterhead on first page** (logo + company name + contact info), simplified or hidden on subsequent pages
- Use `TitlePage` in `SectionProperties` to enable different first-page header
- Design flexibly based on the specific business context—no fixed rules

### Two-Column Layout

Use `sectPr` with `Columns`. Affects entire section until next `sectPr`.

## 4.4 Special Content

### Math Formulas (OMML)

**Core pattern**: `<m:e>` is the universal content container. Almost all elements wrap content in `<m:e>`.

**Text**: Always `<m:r><m:t>text</m:t></m:r>`, never bare text.

**Root**: `<m:oMath>` (inline) or `<m:oMathPara>` (display). Do NOT nest `<m:oMath>` inside another.

**Structure examples**:

| Element | Structure |
|---------|-----------|
| Fraction | `<m:f><m:num><m:e>…</m:e></m:num><m:den><m:e>…</m:e></m:den></m:f>` |
| Subscript | `<m:sSub><m:e>base</m:e><m:sub><m:e>…</m:e></m:sub></m:sSub>` |
| Superscript | `<m:sSup><m:e>base</m:e><m:sup><m:e>…</m:e></m:sup></m:sSup>` |
| Radical | `<m:rad><m:deg><m:e>n</m:e></m:deg><m:e>radicand</m:e></m:rad>` |
| Matrix | `<m:m><m:mr><m:e>cell</m:e><m:e>cell</m:e></m:mr></m:m>` |
| Nary (∑∫) | `<m:nary><m:sub><m:e>…</m:e></m:sub><m:sup><m:e>…</m:e></m:sup><m:e>body</m:e></m:nary>` |
| Delimiter | `<m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>…</m:e></m:d>` |
| Equation array | `<m:eqArr><m:e>eq1</m:e><m:e>eq2</m:e></m:eqArr>` |

**Trap**: Matrix uses `<m:e>` for cells, NOT `<m:mc>` (which is for column properties).

### Curly Quotes in C# Strings

C# treats `"` `"` as string delimiters → CS1003. **Simplest fix**: Use escaped straight quotes `\"` in string literals. If curly quotes are required, use XML entity encoding: `&#8220;` `&#8221;` (doubles) or `&#8216;` `&#8217;` (singles).

**Chinese quote handling** — see `CJKExample.cs` for complete patterns:

```csharp
// ❌ Wrong - Chinese quotes break compilation
new Text("请点击"确定"按钮")  // CS1003!

// ✓ Correct - use Unicode escapes
new Text("请点击\u201c确定\u201d按钮")
```

| Character | Unicode | Usage |
|-----------|---------|-------|
| " (left double) | `\u201c` | Opening quote |
| " (right double) | `\u201d` | Closing quote |
| ' (left single) | `\u2018` | Opening single |
| ' (right single) | `\u2019` | Closing single |

**⚠️ Do NOT use verbatim strings `@""`** — `\u` escapes don't work in verbatim strings:

```csharp
// ❌ WRONG - @"" verbatim string, \u NOT escaped, outputs literal "\u201c"
string text = @"她说\u201c你好\u201d";  // Outputs: 她说\u201c你好\u201d

// ✓ CORRECT - regular string, \u IS escaped
string text = "她说\u201c你好\u201d";   // Outputs: 她说"你好"

// ✓ For long text, use + concatenation
string para = "第一段内容，" +
              "她说\u201c这是引用\u201d，" +
              "继续写第二段。";
```

### Units

Twips = 1/20 pt (11906 = A4 width). Half-points for font size (24 = 12pt). EMU = 914400/inch.

## 4.5 Page Layout

### Image Size

`wp:extent` and `a:ext` Cx/Cy must match. For proportional scaling: read PNG header (bytes 16-23) for dimensions, calculate `cy = cx * height / width`.

### Pagination Control

Add `KeepNext` to title/chart paragraphs to prevent orphaned titles or chart-caption separation.

### Section Breaks

`sectPr` inside `pPr` = last paragraph of section. Avoid `PageBreak` + `Continuous` (blank page). Use `NextPage`.

### Table of Contents (TOC)

WPS doesn't support `UpdateFieldsOnOpen` → must pre-populate TOC entries using **field code structure**: `FieldChar(Begin)` → `FieldCode(" TOC ...")` → `FieldChar(Separate)` → placeholder entries (hyperlinked text + page numbers) → `FieldChar(End)`. The placeholder entries between Separate and End allow Word to display a TOC immediately; users refresh to get accurate page numbers. **Never use static text paragraphs to simulate a TOC**—must use field code structure, otherwise it cannot be refreshed. See `Example.cs:AddTocSection()`.

Parameters: `\o "1-3"` (heading levels), `\h` (hyperlinks), `\z` (hide page# in web), `\u` (outline level).

Headings must use built-in `Heading1`/`Heading2` styles (custom styles not recognized).

### Alignment and Typography

CJK body: justify + 2-char indent. English: left. Table numbers: right. Headings: no indent.

## 4.6 Page Elements

### Headers and Footers

```csharp
// 1. Create header part
var headerPart = mainPart.AddNewPart<HeaderPart>();
var headerId = mainPart.GetIdOfPart(headerPart);

headerPart.Header = new Header(
    new Paragraph(
        new ParagraphProperties(
            new ParagraphStyleId { Val = "Header" },
            new Justification { Val = JustificationValues.Center }
        ),
        new Run(new Text("Document Title"))
    )
);

// 2. Create footer part (with page numbers)
var footerPart = mainPart.AddNewPart<FooterPart>();
var footerId = mainPart.GetIdOfPart(footerPart);

var footerPara = new Paragraph(
    new ParagraphProperties(
        new Justification { Val = JustificationValues.Center }
    )
);
// PAGE field: Begin → FieldCode → Separate → Text → End
footerPara.Append(new Run(new FieldChar { FieldCharType = FieldCharValues.Begin }));
footerPara.Append(new Run(new FieldCode(" PAGE ")));
footerPara.Append(new Run(new FieldChar { FieldCharType = FieldCharValues.Separate }));
footerPara.Append(new Run(new Text("1")));  // Placeholder, updated on open
footerPara.Append(new Run(new FieldChar { FieldCharType = FieldCharValues.End }));
footerPara.Append(new Run(new Text(" / ") { Space = SpaceProcessingModeValues.Preserve }));
// NUMPAGES field (same structure)
footerPara.Append(new Run(new FieldChar { FieldCharType = FieldCharValues.Begin }));
footerPara.Append(new Run(new FieldCode(" NUMPAGES ")));
footerPara.Append(new Run(new FieldChar { FieldCharType = FieldCharValues.Separate }));
footerPara.Append(new Run(new Text("1")));
footerPara.Append(new Run(new FieldChar { FieldCharType = FieldCharValues.End }));
footerPart.Footer = new Footer(footerPara);

// 3. Reference in SectionProperties
new SectionProperties(
    new HeaderReference { Type = HeaderFooterValues.Default, Id = headerId },
    new FooterReference { Type = HeaderFooterValues.Default, Id = footerId },
    new PageSize { Width = 11906, Height = 16838 },
    new PageMargin { Top = 1440, Right = 1440, Bottom = 1440, Left = 1440, Header = 720, Footer = 720 }
)
```

**Header/Footer Types**:

| Type | HeaderFooterValues | Purpose |
|------|-------------------|---------|
| Default | `.Default` | Odd pages (or all pages) |
| Even | `.Even` | Even pages |
| First | `.First` | First page |

**Different first page** (for cover): add `TitlePage()` to sectPr.

**Different odd/even pages**: add `<w:evenAndOddHeaders/>` in settings.xml.

### Footnotes and Endnotes

**Separator trap**: FootnotesPart/EndnotesPart must include Id=-1 (Separator) and Id=0 (ContinuationSeparator) before any user notes. Missing these → Word fails to render.

```xml
<!-- Required in footnotes.xml / endnotes.xml before user notes -->
<w:footnote w:type="separator" w:id="-1">
  <w:p><w:r><w:separator/></w:r></w:p>
</w:footnote>
<w:footnote w:type="continuationSeparator" w:id="0">
  <w:p><w:r><w:continuationSeparator/></w:r></w:p>
</w:footnote>
<!-- User notes start from id="1" -->
```

### Lists

Requires `NumberingDefinitionsPart` with `AbstractNum` + `NumberingInstance`. Apply via `NumberingProperties` in paragraph.

Multi-level: create `AbstractNum` with multiple `Level`s. Formats: `Decimal`, `UpperLetter`, `LowerRoman`, `Bullet`, `ChineseCounting`.

### Hyperlinks

**Must use `<w:hyperlink>` element, not plain text.** Requires relationship first:

```csharp
var relId = mainPart.AddHyperlinkRelationship(new Uri("https://example.com"), true).Id;
paragraph.Append(new Hyperlink(new Run(
    new RunProperties(new Color { Val = "0563C1" }, new Underline { Val = UnderlineValues.Single }),
    new Text("Click here")
)) { Id = relId })
```

### Charts and Visualization

| Requirement | Preferred | Alternative |
|-------------|-----------|-------------|
| Data charts | Word native | matplotlib PNG |
| Flowcharts | DrawingML Shapes | Table layout |
| Illustrations | Image generation | Image search |

**Word Chart**: Use `NumberLiteral` (no Excel), `DataPoint` for colors. See Example.

**matplotlib**: `dpi=300`, `axes.unicode_minus=False`. Font/labels must match document language.

## 4.7 Editing Operations (Python API)

Use `docx_lib.editing` for comments and track changes:

```python
from scripts.docx_lib.editing import (
    DocxContext,
    add_comment, reply_comment, resolve_comment, delete_comment,
    insert_paragraph, insert_text, propose_deletion,
    reject_insertion, restore_deletion, enable_track_changes
)

with DocxContext("input.docx", "output.docx") as ctx:
    # add_comment(ctx, para_text, comment, highlight=None)
    # - para_text: text to locate paragraph
    # - comment: comment content
    # - highlight: text to highlight (omit to highlight entire paragraph)
    add_comment(ctx, "M-SVI index", "Please define", highlight="M-SVI")
    insert_text(ctx, "The method", after="method", new_text=" and materials")
```

**Complete guide**: `references/EditingGuide.md`

## 4.8 XML Quick Reference

### Text Formatting (rPr)

```xml
<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Times New Roman" w:eastAsia="SimSun"/>
    <w:sz w:val="24"/>  <!-- 12pt = 24 half-points -->
    <w:b/><w:i/><w:u w:val="single"/>
    <w:color w:val="FF0000"/>
  </w:rPr>
  <w:t>text</w:t>
</w:r>
```

**Font sizes**: 21=10.5pt, 24=12pt, 28=14pt, 32=16pt, 44=22pt

### Track Changes Structure

```xml
<!-- Insertion: <w:ins> wraps <w:r> -->
<w:ins w:id="1" w:author="..." w:date="...">
  <w:r><w:rPr>...</w:rPr><w:t>text</w:t></w:r>
</w:ins>

<!-- Deletion: <w:del> wraps <w:r> (same pattern as ins!) -->
<w:del w:id="2" w:author="..." w:date="...">
  <w:r><w:rPr>...</w:rPr><w:delText>text</w:delText></w:r>
</w:del>
```

**Key**: Both `<w:ins>` and `<w:del>` **wrap** `<w:r>`, not inside it. Use `<w:delText>` instead of `<w:t>` for deletions.

### Schema Constraints

| Rule | Requirement |
|------|-------------|
| RSID values | 8-digit uppercase hex: `00A1B2C3` |
| Whitespace | `xml:space="preserve"` for leading/trailing spaces |
| Revision structure | `<w:ins>`/`<w:del>` **wrap** `<w:r>`, must have `w:id` attribute |

---

**Complete examples**: See `references/EditingGuide.md` for full working code.
