---
name: format-markdown-table
description: Generate well-formatted markdown tables from data with proper alignment and spacing. Use for report statistics, comparison tables, or summary data presentation.
---

# Format Markdown Table

Create properly formatted markdown tables with alignment and consistent spacing.

## When to Use

- Report statistics tables
- Comparison tables
- Summary data presentation
- Metric dashboards in reports

## Instructions

### Step 1: Receive Table Data

Accept headers and rows as input.

**Expected Input**:

```json
{
  "headers": ["Column 1", "Column 2", "Column 3"],
  "rows": [
    ["Value 1", "Value 2", "Value 3"],
    ["Value 4", "Value 5", "Value 6"]
  ],
  "alignment": ["left", "center", "right"]
}
```

**Alignment** (optional):

- `left`: Left-aligned (default)
- `center`: Center-aligned
- `right`: Right-aligned

### Step 2: Calculate Column Widths

Determine maximum width for each column.

**Width Calculation**:

- Include header width
- Include all row values
- Add padding (1 space on each side)
- Minimum width: 3 characters

### Step 3: Format Header Row

Create header row with proper spacing.

**Format**:

```
| Header 1 | Header 2 | Header 3 |
```

### Step 4: Format Separator Row

Create separator with alignment indicators.

**Alignment Indicators**:

- Left: `:---` or `---`
- Center: `:---:`
- Right: `---:`

**Format**:

```
|----------|:--------:|---------:|
```

### Step 5: Format Data Rows

Create data rows with consistent spacing.

**Format**:

```
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
```

### Step 6: Return Complete Table

Return formatted markdown table.

**Expected Output**:

```markdown
| Column 1 | Column 2 | Column 3 |
| -------- | :------: | -------: |
| Value 1  | Value 2  |  Value 3 |
| Value 4  | Value 5  |  Value 6 |
```

## Error Handling

- **Empty Headers**: Return error requesting headers
- **Empty Rows**: Return warning, create table with headers only
- **Mismatched Columns**: Pad short rows with empty cells
- **Invalid Alignment**: Use 'left' as default, warn

## Examples

### Example 1: Simple Statistics Table

**Input**:

```json
{
  "headers": ["Metric", "Count", "Percentage"],
  "rows": [
    ["Critical Bugs", "3", "13%"],
    ["High Bugs", "8", "35%"],
    ["Medium Bugs", "12", "52%"]
  ],
  "alignment": ["left", "right", "right"]
}
```

**Output**:

```markdown
| Metric        | Count | Percentage |
| ------------- | ----: | ---------: |
| Critical Bugs |     3 |        13% |
| High Bugs     |     8 |        35% |
| Medium Bugs   |    12 |        52% |
```

### Example 2: Comparison Table

**Input**:

```json
{
  "headers": ["Feature", "Before", "After"],
  "rows": [
    ["Build Time", "45s", "12s"],
    ["Test Time", "2m 30s", "1m 15s"],
    ["Bundle Size", "2.3 MB", "1.8 MB"]
  ],
  "alignment": ["left", "center", "center"]
}
```

**Output**:

```markdown
| Feature     | Before | After  |
| ----------- | :----: | :----: |
| Build Time  |  45s   |  12s   |
| Test Time   | 2m 30s | 1m 15s |
| Bundle Size | 2.3 MB | 1.8 MB |
```

### Example 3: Priority Distribution

**Input**:

```json
{
  "headers": ["Priority", "Open", "Fixed", "Total"],
  "rows": [
    ["P0", "2", "5", "7"],
    ["P1", "5", "3", "8"],
    ["P2", "12", "8", "20"]
  ]
}
```

**Output**:

```markdown
| Priority | Open | Fixed | Total |
| -------- | ---- | ----- | ----- |
| P0       | 2    | 5     | 7     |
| P1       | 5    | 3     | 8     |
| P2       | 12   | 8     | 20    |
```

### Example 4: Empty Rows (Header Only)

**Input**:

```json
{
  "headers": ["Name", "Value", "Status"],
  "rows": []
}
```

**Output**:

```markdown
| Name | Value | Status |
| ---- | ----- | ------ |
```

## Validation

- [ ] Formats headers correctly
- [ ] Creates proper separators
- [ ] Aligns columns as specified
- [ ] Handles various data types (numbers, text)
- [ ] Pads columns for consistent width
- [ ] Handles empty rows gracefully

## Supporting Files

- `examples.md`: Table formatting examples (see Supporting Files section)
