---
name: google-slides-tables
description: Create proper tables in Google Slides presentations using the Slides API. Use when building tabular data, metrics, comparisons, or any slide that needs rows and columns.
requires:
  - google-oauth
---

# Google Slides Tables Skill

Create proper tables in Google Slides presentations using the Slides API.

## When to Use

Use this skill when:

- Creating tabular data in Google Slides presentations
- Displaying user metrics, costs, or statistics
- Building comparison tables or data grids
- Any time you need formatted rows and columns

## Key Principle: Use Real Tables, Not Text

**WRONG**: Creating "tables" with text characters like dashes and pipes:

```
USER     COST    STATUS
─────────────────────────
tom      $100    Active
dan      $50     Active
```

This renders as bullet points and looks terrible in Google Slides!

**CORRECT**: Use the `ai_first_slides_create_table` MCP tool to create actual Google Slides table objects.

## Available Tool

### `ai_first_slides_create_table`

Creates a native Google Slides table with proper formatting.

**Parameters:**

- `slideId` (required): The slide object ID where the table will be placed
- `data` (required): 2D array of strings - rows of cells
- `presentationUrl` (optional): Presentation URL or ID
- `headerRow` (optional, default: true): Style first row as header (bold, colored)
- `position` (optional): `{x: number, y: number}` in points
- `size` (optional): `{width: number, height: number}` in points

**Example:**

```json
{
  "slideId": "SLIDES_API12345_0",
  "presentationUrl": "19f8Px6u-gf7DXnI1k8xhnm9lAYAqCNKvcfvoX5Dbrtk",
  "data": [
    ["User", "Cursor $", "API Tokens", "Lines", "Status"],
    ["tom", "$1,283", "44M", "7,438", "🟢 Power"],
    ["daniel", "-", "-", "10,755", "🟢 Power"],
    ["yuval", "$184", "-", "425", "🟡 Regular"],
    ["assaf", "$164", "0.8M", "-", "🟡 Regular"]
  ],
  "headerRow": true
}
```

## Workflow: Adding Tables to Presentations

### Step 1: Get the Presentation Structure

```
ai_first_slides_get_presentation
  presentationUrl: "YOUR_PRESENTATION_ID"
```

This returns all slides with their IDs.

### Step 2: Choose Target Slide

Either:

- Use an existing slide's ID
- Create a new blank slide with `ai_first_slides_duplicate_template`

### Step 3: Create the Table

```
ai_first_slides_create_table
  slideId: "SLIDES_API12345_0"
  presentationUrl: "YOUR_PRESENTATION_ID"
  data: [["Header1", "Header2"], ["Val1", "Val2"]]
  headerRow: true
```

### Step 4: Verify (Optional)

Use the browser MCP to take a screenshot and verify the table looks correct.

## Table Formatting

### Header Row (Default: enabled)

- Bold text
- Blue background (#336699)
- White text color

### Data Rows

- Normal weight
- Default background
- Auto-sized cells

### Positioning

Default position is `{x: 50, y: 120}` (in points from top-left).
Adjust if you have a title at the top of the slide.

### Sizing

Default width is 620pt (fits most slides).
Height auto-calculates based on number of rows (30pt per row).

## Best Practices

1. **Keep tables concise** - Max 10-12 rows per slide for readability
2. **Use clear headers** - First row should describe each column
3. **Align data types** - Numbers right-aligned, text left-aligned (default)
4. **Split large tables** - Create multiple slides for many rows
5. **Add a title** - Use a text box or slide title above the table

## Common Data Patterns

### User Metrics Table

```json
[
  ["User", "Cost", "Tokens", "Status"],
  ["user1@example.com", "$100", "10M", "Active"],
  ["user2@example.com", "$50", "5M", "Exploring"]
]
```

### Model Usage Table

```json
[
  ["Model", "Cost", "Requests", "% of Total"],
  ["claude-4.5-opus", "$1,465", "8,910", "76.5%"],
  ["gpt-5.2", "$157", "1,594", "8.2%"]
]
```

### Status Summary Table

```json
[
  ["Status", "Count", "Percentage"],
  ["🟢 Power User", "6", "21%"],
  ["🟡 Regular", "5", "17%"],
  ["🟠 Exploring", "10", "34%"],
  ["⚪ Not Started", "8", "28%"]
]
```

## Troubleshooting

### "Table looks cramped"

- Increase `size.height` in the options
- Reduce number of rows per table

### "Table overlaps title"

- Increase `position.y` to move table down

### "Columns too narrow"

- Increase `size.width`
- Reduce number of columns
- Shorten cell text

### "Can't find slide ID"

- Run `ai_first_slides_get_presentation` first
- Slide IDs look like `SLIDES_API12345_0` or `g3b635182008_0_0`
