---
context: fork
description: Convert CSV files to Page notes with markdown tables (no truncation)
model: sonnet
---

# /csv-to-page

Convert CSV files into Page notes with properly formatted markdown tables.

**Key Feature**: No content truncation by default - full cell content is preserved regardless of length (PapaParse has no cell size limits; V8 engine supports strings up to 512MB).

**Features**:

- RFC 4180 compliant parsing via PapaParse
- **No truncation** - full cell content preserved (up to 512MB per cell)
- Auto-detects delimiter (comma, semicolon, tab)
- Handles quoted fields, multi-line content, embedded commas
- Escapes markdown special characters (pipes, backslashes)
- Auto-detects numeric columns for right-alignment
- **Split mode** - create individual notes for rows with long content

## Usage

```
/csv-to-page <csv-path>
/csv-to-page Inbox/data.csv
/csv-to-page Inbox/rfi.csv --split --split-folder "RFI-Responses"
/csv-to-page Inbox/data.csv --truncate 150  # Optional truncation
```

## Instructions

### Phase 1: CSV Analysis

1. **Verify the CSV file exists** at the specified path
2. **Run analysis** to understand structure:
   ```bash
   node scripts/csv-to-markdown.js "<csv-path>" --output-json
   ```
3. **Review the output** to identify:
   - Total rows and columns
   - Empty rows (common in Excel exports)
   - Maximum cell length (determines if split mode recommended)
   - Whether there are metadata/instruction rows before actual data

### Phase 2: Choose Conversion Mode

Based on the analysis, recommend a mode to the user:

**Use AskUserQuestion**:

```
Question: "How should the CSV be processed?"
Header: "CSV Mode"
Options:
  1. "Full table (Recommended for simple data)"
     Description: "Single markdown table with all content preserved"
  2. "Split mode (Recommended for long content)"
     Description: "Individual note per row - best for RFIs, surveys, responses"
  3. "Truncated summary"
     Description: "Compact table with truncated cells for overview"
```

**Recommendations**:

- **Full table**: For CSVs with cells under 500 characters
- **Split mode**: For RFI responses, surveys, or any CSV with cells over 1000 characters
- **Truncated**: Only when user specifically needs a compact summary view

### Phase 3: Run Conversion

**Full table mode (default, no truncation)**:

```bash
node scripts/csv-to-markdown.js "<csv-path>" --title "<title>"
```

**Split mode (recommended for long content)**:

```bash
node scripts/csv-to-markdown.js "<csv-path>" --split --split-folder "<folder>" --title "<title>" --id-column 2
```

**Truncated mode (optional)**:

```bash
node scripts/csv-to-markdown.js "<csv-path>" --truncate 150 --title "<title>"
```

### Script Options

| Option                  | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| `--title <title>`       | Custom title for the Page note                       |
| `--split`               | Create individual notes for each row                 |
| `--split-folder <path>` | Folder for split notes (e.g., "RFI-Responses")       |
| `--id-column <n>`       | Column index for note IDs (0-indexed, default: 0)    |
| `--truncate <n>`        | Truncate cells to N characters (disabled by default) |
| `--start-row <n>`       | Start from row N (0-indexed, for skipping metadata)  |
| `--end-row <n>`         | End at row N (for partial conversion)                |
| `--delimiter <char>`    | Force delimiter if auto-detect fails                 |
| `--dry-run`             | Preview without creating files                       |
| `--verbose`             | Show detailed processing info                        |

### Phase 4: Post-Processing

After conversion:

1. **Add entity links** - Link to existing Projects, People, Systems
2. **Add appropriate tags** - Based on content (activity/, project/, domain/)
3. **For split mode** - Review and enhance individual notes with relationships

### Phase 5: Summary Report

Provide user with:

**For full table mode**:

```markdown
## CSV Import Complete

**Created**: `Page - <title>.md`

**Statistics**:

- Rows: <count>
- Columns: <count>
- Max cell length: <chars>
- Truncation: None (full content preserved)

**Note**: Obsidian may have display issues with very wide tables.
Consider using Reading View for better rendering.
```

**For split mode**:

```markdown
## CSV Import Complete (Split Mode)

**Summary**: `Page - <title>.md`
**Individual Notes**: <count> notes in `<folder>/`

Each row has been converted to a separate note with:

- Full content preserved (no truncation)
- Proper markdown formatting
- Metadata linking back to source

**Next Steps**:

1. Review individual notes
2. Add project/person links
3. Add relevant tags
```

## Handling Common CSV Patterns

### RFI/Scoring Spreadsheets (Recommended: Split Mode)

Pattern: Questions with very long vendor responses (1000-10000+ chars).

```bash
node scripts/csv-to-markdown.js "<file>.csv" --split --split-folder "RFI-Responses" --id-column 2 --start-row 5
```

**Benefits**:

- Each question/response becomes a searchable note
- Full content preserved with proper formatting
- Can add scores, comments, tags to individual responses
- Supports Dataview queries for aggregation

### Data Exports (Recommended: Full Table)

Pattern: Clean data with short cells (<500 chars).

```bash
node scripts/csv-to-markdown.js "<file>.csv" --title "Data Export - Jan 2026"
```

### Multi-Section CSVs

Pattern: Multiple tables in one file separated by empty rows.

**Approach**: Use `--start-row` and `--end-row` to extract each section:

```bash
# Section 1
node scripts/csv-to-markdown.js data.csv --start-row 0 --end-row 20 --title "Section 1"

# Section 2
node scripts/csv-to-markdown.js data.csv --start-row 25 --end-row 50 --title "Section 2"
```

## Technical Notes

### No Content Limits

- **PapaParse**: No documented cell size limit
- **V8 Engine**: Strings up to 512MB supported
- **Practical**: Tested with 10,000+ character cells without issues

### Markdown Table Considerations

For very long content in tables:

- Newlines converted to `<br>` tags
- Pipe characters escaped as `\|`
- Backslashes escaped as `\\`
- May cause horizontal scrolling in Obsidian

**Recommendation**: Use `--split` mode for cells >1000 characters.

### Supported Delimiters

- Comma (`,`) - Default
- Semicolon (`;`) - Common in European exports
- Tab (`\t`) - TSV files

### Character Encoding

- UTF-8 (default)
- Handles Windows-1252 and Latin-1 from Excel exports
- Special characters preserved

## Example Workflows

### RFI Scoring Sheet

```
User: /csv-to-page Inbox/vendor-rfi-responses.csv
```
