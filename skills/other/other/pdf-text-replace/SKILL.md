---
name: pdf-text-replace
description: Replace text in fillable PDF forms by updating form field values. This skill should be used when users need to update names, addresses, dates, or other text in PDF form fields.
---

# PDF Text Replace Skill

Replace text in fillable PDF forms by updating form field values.

## Description

This skill allows you to search and replace text in PDF files that have fillable form fields. It scans all form fields in the PDF, finds fields containing the search text, and replaces it with the replacement text.

## Use Cases

- Update names in filled tax forms
- Replace addresses in PDF documents
- Update dates or reference numbers
- Batch update form field values

## Requirements

- PDF must have fillable form fields (not flattened)
- Python 3.7+
- pypdf library

## Usage

### Basic Usage

```bash
python /app/uploads/skills/public/pdf-text-replace/scripts/replace_text_in_pdf.py \
    /app/uploads/input.pdf \
    "OLD TEXT" \
    "NEW TEXT" \
    /app/uploads/output.pdf
```

### Example: Replace Name in Tax Form

```bash
python /app/uploads/skills/public/pdf-text-replace/scripts/replace_text_in_pdf.py \
    /app/uploads/f5472.pdf \
    "MANISH KUMAR" \
    "MANNU KUMAR" \
    /app/uploads/f5472_updated.pdf
```

## Script Details

**Script:** `scripts/replace_text_in_pdf.py`

**Arguments:**
1. `input_pdf` - Path to input PDF file
2. `search_text` - Text to search for in form fields
3. `replace_text` - Text to replace with
4. `output_pdf` - Path to save the updated PDF

**Output:**
- Creates a new PDF with updated field values
- Preserves all form fields (not flattened)
- Reports number of fields modified

## Limitations

- Only works with fillable PDF forms (not scanned/image PDFs)
- Replaces text in form field values, not static text
- Case-sensitive search by default
- Cannot modify flattened PDFs

## Dependencies

The script requires the `pypdf` library, which is included in the container requirements.

## Error Handling

The script will report errors if:
- Input PDF doesn't exist
- PDF doesn't have fillable form fields
- Search text is not found
- Output path is not writable
