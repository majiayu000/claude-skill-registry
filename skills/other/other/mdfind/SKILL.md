---
name: mdfind
context: fork
description: Search PDF, PPTX, and image content in Attachments using macOS Spotlight
model: haiku
---

# /mdfind - Attachment Content Search

Search inside PDFs, PowerPoints, images, and other files in `Attachments/` using macOS Spotlight (`mdfind`). This leverages the OS-level content index — no custom indexing needed.

## Usage

```
/mdfind <search query>           # Search all attachment content
/mdfind --type pdf <query>       # Search only PDFs
/mdfind --type pptx <query>      # Search only PowerPoints
/mdfind --type image <query>     # Search only images (OCR-indexed)
```

## Instructions

### 1. Run mdfind

Execute the appropriate search based on flags:

#### Default (all attachments)

```bash
mdfind -onlyin Attachments/ "<search_query>" 2>/dev/null
```

#### Filter by PDF

```bash
mdfind -onlyin Attachments/ "kMDItemContentType == 'com.adobe.pdf' && kMDItemTextContent == '*<query>*'" 2>/dev/null
```

If the above returns nothing, fall back to the simpler form:

```bash
mdfind -onlyin Attachments/ -name ".pdf" "<search_query>" 2>/dev/null
```

#### Filter by PPTX

```bash
mdfind -onlyin Attachments/ "kMDItemContentType == 'org.openxmlformats.presentationml.presentation'" "<search_query>" 2>/dev/null
```

#### Filter by Images

```bash
mdfind -onlyin Attachments/ "kMDItemContentType == 'public.image'" "<search_query>" 2>/dev/null
```

### 2. Present Results

Format results clearly:

```markdown
## Attachment Search: <query>

Found **N** matching files

| # | File | Type | Size |
|---|------|------|------|
| 1 | [filename](path) | PDF | 2.4 MB |
| 2 | ... | ... | ... |

### Quick Actions

- Read a PDF: `/pdf-to-page <path>`
- Read a PPTX: `/pptx-to-page <path>`
- Full vault search: `/q <query>`
```

### 3. Get File Details (Optional)

For each result, get file size and type:

```bash
ls -lh "<file_path>" 2>/dev/null
```

## Notes

- `mdfind` uses macOS Spotlight — files must be indexed (most are by default)
- Works best with text-based PDFs; scanned PDFs need OCR indexing
- For vault note content search, use `/q` instead
- Results are file paths relative to the vault root
