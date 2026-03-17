---
name: docx-advanced-patterns
description: Advanced python-docx patterns for nested tables, complex cells, and content extraction beyond .text property. Techniques for forms, checklists, and complex layouts.
---

# DOCX Advanced Patterns Skill

Specialized patterns for python-docx that handle complex document structures not covered by basic `.text` extraction.

## When to Use This Skill

Invoke this skill when working with DOCX files that have:
- Nested tables within table cells
- Forms with checkbox options
- Complex multi-row cell layouts
- Checklists with embedded options
- Cell content that doesn't appear with `.text` property

**Use alongside** the official `docx` skill for comprehensive document handling.

## Core Pattern: Nested Table Extraction

### Problem

python-docx's `cell.text` property only extracts direct paragraph text - it **does not** traverse nested tables within cells.

**Symptom:**
```python
cell.text  # Returns: '' or '\n'
# But cell visually contains content!
```

### Detection

Check if a cell contains nested tables:

```python
if cell.tables:
    print(f"Found {len(cell.tables)} nested table(s)")
    # Cell has nested content - need special extraction
```

### Solution (Simple)

```python
def extract_cell_content_with_nested_tables(cell):
    """
    Extract all text from a cell, including text from nested tables.

    Args:
        cell: python-docx _Cell object

    Returns:
        str: Combined text from cell paragraphs and nested tables
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
                # For checkbox lists: Column 0 = label, Column 1 = checkbox
                # Extract text from first column only
                if nested_row.cells:
                    first_col_text = nested_row.cells[0].text.strip()
                    # Filter out checkbox characters
                    if first_col_text and first_col_text not in ['⁮', '☐', '☑', '☒']:
                        text_parts.append(first_col_text)

    return '\n'.join(text_parts) if text_parts else ''
```

### Solution (Recursive for Deep Nesting)

For documents with multiple levels of table nesting:

```python
def extract_cell_content_recursively(cell):
    """
    Recursively extract text from cell including deeply nested tables.

    Handles arbitrary nesting depth.
    """
    text_parts = []

    def _extract_recursive(cell_obj):
        # Get direct paragraphs
        for para in cell_obj.paragraphs:
            para_text = para.text.strip()
            if para_text and para_text not in ['⁮', '☐', '☑', '☒']:
                text_parts.append(para_text)

        # Recursively get nested tables
        for nested_table in cell_obj.tables:
            for nested_row in nested_table.rows:
                for nested_cell in nested_row.cells:
                    _extract_recursive(nested_cell)

    _extract_recursive(cell)
    return '\n'.join(text_parts) if text_parts else ''
```

## Usage Examples

### Example 1: Extracting Form Checkbox Options

**Document Structure:**
```
Table Cell contains:
  Nested Table:
    Row 1: "High potential" | ☐
    Row 2: "Moderate potential" | ☐
    Row 3: "Low potential" | ☐
```

**Extraction:**
```python
from docx import Document

doc = Document('form.docx')
table = doc.tables[0]
cell = table.rows[1].cells[0]

# Wrong way - returns empty
basic_text = cell.text
print(basic_text)  # Output: '' or '\n'

# Right way - extracts nested content
full_text = extract_cell_content_with_nested_tables(cell)
print(full_text)
# Output:
# High potential
# Moderate potential
# Low potential
```

### Example 2: Processing All Cells in a Table

```python
def process_table_with_nested_content(table):
    """Process all cells, handling nested tables"""
    for row in table.rows:
        for cell in row.cells:
            # Extract with nested table support
            content = extract_cell_content_with_nested_tables(cell)

            if content:
                # Process content (translate, analyze, etc.)
                processed = do_something_with(content)
                print(f"Cell content: {processed}")
```

### Example 3: Detecting Nested Tables

```python
def analyze_document_structure(doc):
    """Find all cells with nested tables"""
    nested_cells = []

    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                if cell.tables:
                    nested_cells.append({
                        'table': t_idx,
                        'row': r_idx,
                        'col': c_idx,
                        'nested_count': len(cell.tables)
                    })

    return nested_cells

# Usage
doc = Document('complex_form.docx')
nested = analyze_document_structure(doc)

for item in nested:
    print(f"Table {item['table']}, Row {item['row']}, Col {item['col']}: "
          f"{item['nested_count']} nested table(s)")
```

## Common Use Cases

### 1. Government Forms

Forms often use nested tables for checkbox grids:

```python
def extract_form_responses(doc):
    """Extract all form checkbox options"""
    responses = {}

    for table in doc.tables:
        for row in table.rows:
            # First cell = question
            question = row.cells[0].text.strip()

            # Second cell = checkbox options (nested table)
            if row.cells[1].tables:
                options = extract_cell_content_with_nested_tables(row.cells[1])
                responses[question] = options.split('\n')

    return responses
```

### 2. Evaluation Forms

Extract rating scales and options:

```python
def extract_evaluation_items(doc):
    """Extract evaluation criteria and options"""
    evaluations = []

    for table in doc.tables:
        for row_idx, row in enumerate(table.rows[1:], 1):
            # Get criterion
            criterion = row.cells[0].text.strip()

            # Get rating options (often nested)
            rating_cell = row.cells[1]
            rating_options = extract_cell_content_with_nested_tables(rating_cell)

            evaluations.append({
                'criterion': criterion,
                'options': rating_options.split('\n')
            })

    return evaluations
```

### 3. Complex Data Tables

Extract structured data from cells with nested layouts:

```python
def extract_complex_cell_data(cell):
    """Extract data from cells with complex nested structures"""
    data = {
        'main_content': '',
        'nested_items': []
    }

    # Direct paragraphs
    for para in cell.paragraphs:
        if para.text.strip():
            data['main_content'] = para.text.strip()
            break

    # Nested table data
    if cell.tables:
        for nested_table in cell.tables:
            for nested_row in nested_table.rows:
                row_data = [c.text.strip() for c in nested_row.cells]
                data['nested_items'].append(row_data)

    return data
```

## Integration with Official docx Skill

This skill **complements** the official docx skill:

**Official docx skill provides:**
- Document creation (docx-js)
- Basic text extraction (pandoc)
- Tracked changes workflows
- Comment handling
- XML access for complex cases

**This skill provides:**
- Nested table extraction
- Complex cell content handling
- Form and checklist processing
- Advanced content extraction patterns

**Use together:**
```python
# For basic operations: use official skill
from docx import Document

# For nested table handling: use this skill
from docx_advanced import extract_cell_content_with_nested_tables

# Combine both
doc = Document('complex_form.docx')  # Official
for table in doc.tables:            # Official
    for row in table.rows:          # Official
        for cell in row.cells:      # Official
            # Advanced extraction:
            content = extract_cell_content_with_nested_tables(cell)
```

## Performance Considerations

**For Large Documents:**

Cache nested table checks:

```python
def build_nested_table_cache(doc):
    """Pre-compute which cells have nested tables"""
    cache = {}

    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                if cell.tables:
                    cache[(t_idx, r_idx, c_idx)] = len(cell.tables)

    return cache

# Usage
cache = build_nested_table_cache(doc)

for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            if (t_idx, r_idx, c_idx) in cache:
                # This cell has nested tables
                content = extract_cell_content_with_nested_tables(cell)
            else:
                # Regular extraction
                content = cell.text
```

## Troubleshooting

### Issue: Extraction returns empty despite visible content

**Diagnosis:**
```python
cell = table.rows[1].cells[0]
print(f"cell.text: '{cell.text}'")
print(f"cell.tables: {len(cell.tables)}")

if not cell.text.strip() and cell.tables:
    print("Content is in nested tables!")
```

**Fix:** Use `extract_cell_content_with_nested_tables(cell)`

### Issue: Checkbox characters (⁮, ☐) appear in output

**Fix:** Filter them out:
```python
text = cell.text.strip()
# Remove checkbox unicode characters
clean_text = text.replace('⁮', '').replace('☐', '').replace('☑', '').replace('☒', '')
```

### Issue: Multi-line content not preserved

**Fix:** Join with newlines:
```python
'\n'.join(text_parts)  # Preserves line structure
```

## Best Practices

1. **Always check for nested tables first:**
   ```python
   if cell.tables:
       content = extract_cell_content_with_nested_tables(cell)
   else:
       content = cell.text
   ```

2. **Handle checkbox characters:**
   ```python
   CHECKBOX_CHARS = ['⁮', '☐', '☑', '☒']
   if text not in CHECKBOX_CHARS:
       # Process text
   ```

3. **Preserve structure:**
   ```python
   # Use newlines to maintain line breaks
   '\n'.join(lines)
   ```

4. **Test with sample documents:**
   ```python
   def test_extraction():
       doc = Document('sample_form.docx')
       cell = doc.tables[0].rows[1].cells[0]

       extracted = extract_cell_content_with_nested_tables(cell)
       assert 'High potential' in extracted
       assert 'Moderate potential' in extracted
   ```

## Reference Implementation

See `REFERENCE.md` for:
- Complete working examples
- Integration patterns
- Advanced recursive extraction
- Performance optimization techniques

## Contributing to Anthropic Skills

This pattern is not currently in the official `docx` skill. If you find it useful, consider contributing:

1. Fork https://github.com/anthropics/skills
2. Add to `document-skills/docx/SKILL.md`
3. Submit pull request with:
   - Pattern description
   - Code examples
   - Use cases

## Success Criteria

Pattern is working if:
- [ ] Cells with nested tables return full content
- [ ] Checkbox options are extracted correctly
- [ ] Form fields are readable
- [ ] No content is lost during extraction
- [ ] Structure is preserved (line breaks maintained)
