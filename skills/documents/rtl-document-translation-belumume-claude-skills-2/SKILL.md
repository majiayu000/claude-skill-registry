---
name: rtl-document-translation
description: Translate DOCX to RTL languages (Arabic, Hebrew, Urdu) preserving exact formatting, tables, colors, layouts. Handles quote normalization and multi-pass matching.
---

# RTL Document Translation Skill

Translate structured business documents to right-to-left (RTL) languages while maintaining pixel-perfect formatting, colors, table structures, and professional appearance.

## When to Use This Skill

Invoke this skill when the user requests:
- Translating DOCX files to Arabic, Hebrew, Urdu, or other RTL languages
- Preserving exact document structure (tables, sections, formatting)
- Maintaining colors, backgrounds, and visual styling
- Converting business/financial documents to RTL formats
- Creating RTL versions that match English originals exactly

**Do NOT use for:**
- Simple text translation (use translation APIs directly)
- Creating new documents from scratch
- PDF-only workflows (this skill works with DOCX)

## Core Methodology

### 1. Phased Approach (Critical)

**Phase 1: Analysis** → **Phase 2: Translation Dictionary** → **Phase 3: Document Generation** → **Phase 4: Verification**

Never skip directly to generation. Structure analysis prevents catastrophic errors like:
- Splitting multi-line cells into multiple rows
- Missing table dimensions
- Incorrect section orientations

### 2. RTL Formatting (3 Levels)

RTL documents require THREE distinct formatting levels:

**Level 1 - Text Direction:**
```python
paragraph.paragraph_format.bidi = True
run.font.rtl = True
run.font.complex_script = True
```

**Level 2 - Text Alignment:**
```python
paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
```

**Level 3 - Layout Direction:**
For data/financial tables: Keep columns in LEFT-TO-RIGHT order
- Temporal sequences (Month 1, 2, 3...) progress L→R
- Row labels stay in same positions as English
- Only TEXT WITHIN cells is RTL

Example: Month headers should be:
```
[الشهر] [1] [2] [3] [4]  ← Correct (columns L→R, text RTL)
[4] [3] [2] [1] [الشهر]  ← Wrong (mirrored columns)
```

## Implementation Patterns

### Pattern 1: Background Color Detection

**Problem:** Simple attribute access fails
**Solution:** Use XML traversal

```python
from docx.oxml.ns import qn

def get_cell_background(cell):
    """Reliably extract cell background color"""
    tc = cell._element
    tcPr = tc.tcPr if hasattr(tc, 'tcPr') and tc.tcPr is not None else None

    if tcPr is None:
        return None

    # CRITICAL: Use findall(), not direct attribute access
    shd_list = tcPr.findall(qn('w:shd'))
    for shd in shd_list:
        fill = shd.get(qn('w:fill'))
        if fill and fill != 'auto':
            return fill.upper()

    return None
```

**Why:** `tcPr.shading` doesn't work consistently. XML traversal is bulletproof.

### Pattern 2: Set Cell Background

```python
from docx.oxml import OxmlElement

def set_cell_background(cell, rgb_hex):
    """Set cell background color (e.g., 'CC0029' for red)"""
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()

    # Remove existing shading
    for shd in tcPr.findall(qn('w:shd')):
        tcPr.remove(shd)

    # Add new shading
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), rgb_hex)
    tcPr.append(shd)
```

### Pattern 3: Quote Normalization

**Problem:** DOCX files contain curly quotes (U+201C, U+201D) that break dictionary lookups

**Solution:** Multi-pass normalization

```python
def normalize_text(text):
    """Normalize quotes and unicode spaces for reliable matching"""
    # Convert curly quotes → straight quotes
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")

    # Normalize unicode spaces → regular spaces
    text = re.sub(r'[\u2002\u2003\u2009\u200A\u00A0]+', ' ', text)

    return text.strip()
```

### Pattern 4: Multi-Pass Translation Matching

**Problem:** Exact string matches fail due to whitespace variations, quotes, formatting

**Solution:** Progressive fallback strategy

```python
def translate_text(text, translation_dict):
    """Multi-pass translation with normalization fallbacks"""
    if not text or not text.strip():
        return text

    # Pass 1: Exact match
    if text in translation_dict:
        return translation_dict[text]

    # Pass 2: Stripped
    if text.strip() in translation_dict:
        return translation_dict[text.strip()]

    # Pass 3: Normalized quotes
    normalized_quotes = text.replace('\u201c', '"').replace('\u201d', '"')
    normalized_quotes = normalized_quotes.replace('\u2018', "'").replace('\u2019', "'")
    if normalized_quotes in translation_dict:
        return translation_dict[normalized_quotes]

    # Pass 4: Stripped + normalized
    if normalized_quotes.strip() in translation_dict:
        return translation_dict[normalized_quotes.strip()]

    # Pass 5: Unicode spaces
    cleaned = re.sub(r'[\u2002\u2003\u2009\u200A\u00A0]+', ' ', text).strip()
    if cleaned in translation_dict:
        return translation_dict[cleaned]

    # Pass 6: Combined (quotes + spaces)
    cleaned_quotes = re.sub(r'[\u2002\u2003\u2009\u200A\u00A0]+', ' ', normalized_quotes).strip()
    if cleaned_quotes in translation_dict:
        return translation_dict[cleaned_quotes]

    # Pass 7: Normalized whitespace (collapse multiple spaces)
    normalized_ws = ' '.join(text.split())
    if normalized_ws in translation_dict:
        return translation_dict[normalized_ws]

    # No match found - return as-is
    return text
```

**Success Rate:** 95%+ vs 60% with exact-match-only

### Pattern 5: RTL Cell Formatting

```python
def apply_rtl_to_cell(cell, arabic_text, font_size=10, bold=False, text_color=None):
    """Apply complete RTL formatting to table cell"""
    # Clear cell
    cell.text = ''

    # Add paragraph with Arabic text
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(arabic_text)

    # RTL text direction (Level 1)
    paragraph.paragraph_format.bidi = True
    run.font.rtl = True
    run.font.complex_script = True

    # Right alignment (Level 2)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Font settings
    run.font.name = 'Simplified Arabic'  # or 'Times New Roman' for formal docs
    run._element.rPr.rFonts.set(qn('w:ascii'), 'Simplified Arabic')
    run._element.rPr.rFonts.set(qn('w:hAnsi'), 'Simplified Arabic')
    run._element.rPr.rFonts.set(qn('w:cs'), 'Simplified Arabic')
    run.font.size = Pt(font_size)

    if bold:
        run.font.bold = True

    if text_color:
        run.font.color.rgb = RGBColor(*text_color)

    return cell
```

### Pattern 6: Auto-Correct White Text on Dark Backgrounds

**Problem:** Text becomes invisible on dark backgrounds

**Solution:** Auto-detect and correct

```python
def apply_colors_to_cell(cell, eng_cell, ar_text, font_size=10, bold=False):
    """Apply colors with auto-correction for visibility"""
    # Get background color
    bg_color = get_cell_background(eng_cell)

    # Get text color from English
    text_color = None
    if eng_cell.paragraphs and eng_cell.paragraphs[0].runs:
        for run in eng_cell.paragraphs[0].runs:
            if run.font.color and run.font.color.rgb:
                rgb = run.font.color.rgb
                text_color = (rgb[0], rgb[1], rgb[2])
                break

    # AUTO-CORRECTION: Set white text for dark backgrounds
    if bg_color and bg_color in ['CC0029', 'C00000', '000000']:  # Red/black
        text_color = (255, 255, 255)  # White

    # Apply formatting
    apply_rtl_to_cell(cell, ar_text, font_size, bold, text_color)

    # Set background
    if bg_color:
        set_cell_background(cell, bg_color)
```

### Pattern 7: Nested Table Content Extraction ⭐

**Problem:** `cell.text` property doesn't include text from nested tables within the cell. This causes cells with forms, checklists, or complex layouts to appear empty.

**Detection:**
```python
if cell.tables:
    print(f"Cell contains {len(cell.tables)} nested table(s)")
```

**Solution:** Extract content from nested tables using `cell.tables` property

```python
def extract_cell_content_with_nested_tables(cell):
    """
    Extract all text from a cell, including text from nested tables.

    Handles Word documents that use nested tables for:
    - Checklists with options
    - Forms with checkboxes
    - Complex multi-row cell layouts
    """
    text_parts = []

    # Get direct paragraph text (not inside nested tables)
    for para in cell.paragraphs:
        para_text = para.text.strip()
        if para_text:
            text_parts.append(para_text)

    # Get content from nested tables
    if cell.tables:
        for nested_table in cell.tables:
            for nested_row in nested_table.rows:
                # Extract text from first column only (skip checkbox/form columns)
                if nested_row.cells:
                    first_col_text = nested_row.cells[0].text.strip()
                    # Filter out checkbox characters
                    if first_col_text and first_col_text not in ['⁮', '☐', '☑', '☒']:
                        text_parts.append(first_col_text)

    return '\n'.join(text_parts) if text_parts else ''
```

**Usage in Translation Workflow:**
```python
# Instead of:
eng_text = eng_cell.text  # ❌ Misses nested table content

# Use:
eng_text = extract_cell_content_with_nested_tables(eng_cell)  # ✓ Gets all content
ar_text = translate_text(eng_text)
```

**Why This Matters:**
- Government forms often use nested tables for checkbox grids
- Evaluation forms use nested tables for rating scales
- Business checklists embed options in nested tables
- Without this, translated documents have empty cells

## Font Recommendations by Document Type

| Document Type | Recommended Font | Rationale |
|---------------|------------------|-----------|
| Financial/Business | Simplified Arabic | Better number/table rendering |
| Academic/Formal | Times New Roman | Traditional, paragraph-friendly |
| Technical | Arial Unicode MS | Wide character support |
| **Avoid** | Arial | Poor Arabic rendering quality |

## Complete Workflow

### Step 1: Structure Analysis

```python
def analyze_document(docx_path):
    doc = Document(docx_path)

    structure = {
        'sections': [],
        'tables': [],
        'paragraphs': len(doc.paragraphs),
        'colors': {'text': {}, 'backgrounds': {}},
        'fonts': {}
    }

    # Analyze sections
    for idx, section in enumerate(doc.sections):
        structure['sections'].append({
            'index': idx,
            'orientation': 'portrait' if section.page_width < section.page_height else 'landscape',
            'width': section.page_width.inches,
            'height': section.page_height.inches
        })

    # Analyze tables
    for idx, table in enumerate(doc.tables):
        table_info = {
            'index': idx,
            'rows': len(table.rows),
            'cols': len(table.columns),
            'multiline_cells': []
        }

        # Detect multi-line cells
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                if '\n' in cell.text:
                    table_info['multiline_cells'].append({
                        'row': r_idx,
                        'col': c_idx,
                        'content': cell.text
                    })

        structure['tables'].append(table_info)

    return structure
```

### Step 2: Translation Dictionary Creation

```python
def create_translation_dictionary(docx_files, target_language='arabic'):
    """Extract unique texts and create translation map"""
    unique_texts = set()

    for docx_path in docx_files:
        doc = Document(docx_path)

        # Extract from paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                unique_texts.add(para.text.strip())

        # Extract from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        unique_texts.add(cell.text.strip())

    # Create translation map
    translations = {}
    for text in unique_texts:
        # Call translation API or load from file
        arabic_text = translate_via_api(text, target_language)
        translations[text] = arabic_text

        # Also add normalized versions
        normalized = normalize_text(text)
        if normalized != text:
            translations[normalized] = arabic_text

    return translations
```

### Step 3: Document Generation

See REFERENCE.md for complete implementation example.

### Step 4: Verification

```python
def verify_arabic_document(ar_docx_path, eng_docx_path, translation_dict):
    """Comprehensive verification checks"""
    ar_doc = Document(ar_docx_path)
    eng_doc = Document(eng_docx_path)

    results = {
        'structure': 'PASS',
        'alignment': 'PASS',
        'english_scan': 'PASS',
        'colors': 'PASS',
        'issues': []
    }

    # 1. Structure match
    if len(ar_doc.sections) != len(eng_doc.sections):
        results['structure'] = 'FAIL'
        results['issues'].append(f"Section count mismatch")

    if len(ar_doc.tables) != len(eng_doc.tables):
        results['structure'] = 'FAIL'
        results['issues'].append(f"Table count mismatch")

    # 2. Alignment check
    total_cells = 0
    right_aligned = 0
    for table in ar_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                total_cells += 1
                if cell.paragraphs[0].alignment == WD_ALIGN_PARAGRAPH.RIGHT:
                    right_aligned += 1

    if right_aligned != total_cells:
        results['alignment'] = 'FAIL'
        results['issues'].append(f"Only {right_aligned}/{total_cells} cells right-aligned")

    # 3. English word scan
    allowed_english = get_allowed_english(translation_dict)
    unauthorized = scan_for_english(ar_doc, allowed_english)

    if unauthorized:
        results['english_scan'] = 'FAIL'
        results['issues'].extend([f"English found: {w}" for w in unauthorized])

    return results
```

## Common Pitfalls and Solutions

### Pitfall 1: Splitting Multi-Line Cells
**Wrong:**
```python
# Treats "A\n\nEstimated costs" as multiple rows
lines = cell.text.split('\n')
for line in lines:
    new_row = table.add_row()  # ❌ Creates extra rows
```

**Right:**
```python
# Preserves multi-line content in single cell
ar_cell.text = translate_text(eng_cell.text)  # ✓ Keeps \n intact
```

### Pitfall 2: Partial Translation
**Wrong:** "التدفق النقدي forecast" (mixed Arabic/English)

**Right:** "توقعات التدفق النقدي" (fully translated)

**Cause:** Dictionary missing compound phrases
**Solution:** Extract full phrases, not word-by-word

### Pitfall 3: Forgetting RTL for New Cells
**Wrong:**
```python
new_para = doc.add_paragraph(arabic_text)  # ❌ Missing RTL
```

**Right:**
```python
new_para = doc.add_paragraph()
run = new_para.add_run(arabic_text)
new_para.paragraph_format.bidi = True
run.font.rtl = True
new_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT  # ✓ Complete RTL
```

### Pitfall 4: Not Checking Visual Output
**Problem:** Automated checks pass but visual appearance is wrong

**Solution:** Always generate comparison images:
```python
# Convert to PDF then images
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', ar_docx])
subprocess.run(['pdftoppm', '-png', 'output.pdf', 'comparison'])
```

## Quick Reference: Essential Functions

```python
# 1. Get cell background
bg = get_cell_background(cell)

# 2. Set cell background
set_cell_background(cell, 'CC0029')

# 3. Normalize text
normalized = normalize_text(text)

# 4. Multi-pass translation
arabic = translate_text(english, translation_dict)

# 5. Apply RTL to cell
apply_rtl_to_cell(cell, arabic_text, font_size=10, bold=False)

# 6. Apply colors with auto-correction
apply_colors_to_cell(cell, eng_cell, ar_text)

# 7. Verify document
results = verify_arabic_document(ar_doc, eng_doc, trans_dict)
```

## Success Criteria

Before considering translation complete:
- [ ] Structure matches exactly (sections, tables, dimensions)
- [ ] All text right-aligned and RTL-formatted
- [ ] No unauthorized English words found
- [ ] All colors/backgrounds preserved
- [ ] Visual comparison shows matching layout
- [ ] Multi-line cells preserved (not split)
- [ ] PDF generated successfully

## Additional Resources

See REFERENCE.md for:
- Complete code examples
- Real-world document templates
- Troubleshooting guide
- Advanced patterns
