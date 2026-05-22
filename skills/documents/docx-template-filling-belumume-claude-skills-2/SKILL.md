---
name: docx-template-filling
description: Fill DOCX template forms programmatically while preserving 100% of original structure - logos, footers, styles, metadata. Zero-artifact insertion for forms, applications, and standardized documents. Output indistinguishable from manual filling.
version: 1.0.0
dependencies:
  - python>=3.8
  - python-docx>=0.8.11
---

# DOCX Template Filling - Forensic Preservation

Fill template forms programmatically with **zero detectable artifacts**. The filled document must be indistinguishable from manual typing in the original template.

## When to Use This Skill

Invoke when:
- Filling standardized forms and templates
- Completing application forms
- Responding to questionnaires and surveys
- Processing template-based documents
- Any scenario where the recipient must not detect programmatic manipulation

**Critical requirement**: Template integrity must be 100% preserved (logos, footers, headers, styles, metadata, element structure).

## Core Philosophy: Preservation Over Recreation

**WRONG approach**: Extract content from template, generate new document
- Loses metadata
- Changes element IDs
- Alters styles subtly
- Creates detectable artifacts

**RIGHT approach**: Load template, insert content at anchor points using XML API
- Preserves all original elements
- Maintains metadata
- Zero structural changes
- Indistinguishable from manual entry

## Critical Anti-Patterns

### ❌ NEVER: Use pandoc with --reference-doc

```bash
# This SEEMS correct but ONLY copies styles, NOT structure
pandoc content.md -o output.docx --reference-doc=template.docx
```

**What happens**:
- Template's tables disappear
- Logos, headers, footers lost
- Only style definitions copied
- **Looks completely different**

**Why it fails**: `--reference-doc` means "copy the style definitions," NOT "preserve the document structure"

### ❌ NEVER: Append content at the end

```python
# This destroys template structure
template = Document('template.docx')

# Remove content after markers
# ... (deletion logic)

# Append all new content at end
for para in new_content:
    template.add_paragraph(para.text)  # WRONG!
```

**What happens**:
- Template questions appear unanswered
- All answers grouped at end
- Structure broken
- **Obviously programmatic**

### ❌ NEVER: Recreate tables

```python
# DON'T copy table structure and rebuild
new_table = template.add_table(rows=3, cols=2)
# Even if copying all properties, it's not the original!
```

**What happens**:
- Loses original element IDs
- Style inheritance breaks
- Metadata changes
- **Detectable as modified**

## Essential Workflow

### Step 1: Inspect Template Structure FIRST

**Always** inspect before modifying. Never assume structure.

Use the provided inspection script:

```bash
python scripts/inspect_template.py template.docx
```

This prints:
- All tables with identities
- Potential anchor points (paragraphs ending with ":", "Answer:", etc.)
- Headers and footers
- Document element counts

**Why critical**: Prevents modifying wrong tables, missing anchors, breaking structure.

### Step 2: Selective Table Filling

Modify cells in place. Never recreate tables.

```python
from docx import Document

template = Document('template.docx')

# Fill specific cells in existing table
info_table = template.tables[0]
info_table.rows[0].cells[1].text = "Jane Smith"
info_table.rows[1].cells[1].text = "S12345"

# Table structure, styles, borders all preserved
```

**Principle**: Modify existing cells. Never remove and recreate.

### Step 3: Anchor-Based Content Insertion

Insert content at specific positions using XML API.

```python
# Find anchor paragraphs
anchor_positions = []
for i, para in enumerate(template.paragraphs):
    if para.text.strip() == "Answer:":
        anchor_positions.append(i)

# Insert content after anchor using XML API
def insert_after(doc, anchor_idx, content_paras):
    anchor_elem = doc.paragraphs[anchor_idx]._element
    parent = anchor_elem.getparent()

    for offset, para in enumerate(content_paras):
        parent.insert(
            parent.index(anchor_elem) + 1 + offset,
            para._element
        )

# Load content to insert
content_doc = Document('my_content.docx')
section_paragraphs = content_doc.paragraphs[5:64]

# Insert at anchor
insert_after(template, anchor_positions[0], section_paragraphs)

# Save
template.save('completed.docx')
```

**Why XML API**:
- `doc.add_paragraph()` appends at end → wrong position
- `para.insert_paragraph_before()` has stale reference issues
- XML API: direct element manipulation → correct position, zero artifacts

### Step 4: Multi-Anchor Insertion (Reverse Order)

When inserting at multiple positions, insert from bottom to top to preserve earlier indices.

```python
# Template has anchors at paragraphs 18, 27, 37

# Insert in REVERSE order
insert_after(template, 37, section3_content)  # Last anchor first
insert_after(template, 27, section2_content)  # Middle still at 27
insert_after(template, 18, section1_content)  # First still at 18
```

**Why reverse**: Inserting content shifts later paragraph indices but not earlier ones.

## Advanced Patterns

For detailed implementations, see `references/patterns.md`:

- **Content range extraction** - Extract multi-section content between markers
- **Table identity detection** - Identify tables when no IDs exist
- **Robust anchor matching** - exact/partial/smart modes
- **Table repositioning** - Move tables without recreating
- **Verification** - Ensure zero artifacts after filling

## Common Scenarios

### Scenario 1: Form with Info Table + Q&A

```python
template = Document('form_template.docx')

# Fill info table
info_table = template.tables[0]
info_table.rows[0].cells[1].text = "Applicant Name"

# Find "Answer:" anchors
anchors = [i for i, p in enumerate(template.paragraphs)
           if p.text.strip() == "Answer:"]

# Insert responses
responses = Document('my_responses.docx')
response_content = responses.paragraphs[5:30]

insert_after(template, anchors[0], response_content)

template.save('form_completed.docx')
```

### Scenario 2: Report with Table Repositioning

```python
template = Document('report_template.docx')

# Fill team table
team_table = template.tables[0]
team_table.rows[0].cells[1].text = "Team 5"

# Insert section content at anchors
# ... (insertion code)

# Move summary table to correct position
summary_heading_idx = next(i for i, p in enumerate(template.paragraphs)
                           if "Summary Table:" in p.text)

# Move table from end to after summary heading
# See references/patterns.md for move_table_to_position()

template.save('report_completed.docx')
```

## Bundled Resources

### Scripts

- **`scripts/inspect_template.py`** - Inspect template structure before modification
  - Usage: `python scripts/inspect_template.py <template.docx>`
  - Prevents destructive mistakes by showing all tables, anchors, headers/footers

### References

- **`references/patterns.md`** - Detailed technical patterns
  - Content range extraction
  - Table identity detection strategies
  - XML-level insertion patterns
  - Multi-anchor workflows
  - Verification procedures
  - Complete code examples

Load patterns.md when implementing specific operations beyond basic workflow.

## Verification Checklist

Template filling is successful if:
- [ ] Filled document indistinguishable from manual entry
- [ ] All template tables preserved (count unchanged unless expected)
- [ ] Headers/footers unchanged
- [ ] Logo(s) intact
- [ ] Scoring/grading tables empty (if they should be)
- [ ] Styles identical to original
- [ ] Content inserted at correct anchor points (not at end)
- [ ] Template owner cannot detect programmatic manipulation

## Key Lessons

**This skill documents patterns where:**
- Templates have info tables (to fill) and evaluation/scoring tables (preserve empty)
- Multiple anchor points like "Answer:", "Response:", or "Solution:" for content insertion
- Tables may need repositioning to correct sections
- Document structure must remain intact (headers, footers, logos, branding)
- Zero artifacts requirement (recipient cannot detect automation)

**Use cases**: Forms, questionnaires, standardized documents, applications, reports.

**Core principle**: **Preservation over recreation.** Never rebuild - always modify in place.
