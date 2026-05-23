---
name: data-display-and-selection
description: Complex data deserves multiple view modes — grid, list, table — chosen by the user based on their task. Row and item selection should use large hit areas (the whole row or card, not just a checkbox). Selected state is communicated through a subtle background colour shift. Mass actions appear when items are selected. Use when designing data tables, product listings, file browsers, or any multi-item collection.
metadata:
  priority: 7
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "data table"
      - "list view"
      - "grid view"
      - "mass action"
      - "bulk action"
      - "row selection"
      - "select all"
      - "item selection"
      - "view toggle"
      - "collection"
retrieval:
  aliases:
    - data table
    - list view
    - grid view
    - mass actions
    - bulk actions
    - row selection
    - view modes
    - collection UI
  intents:
    - design a data table
    - add grid and list view toggle
    - implement row selection
    - add bulk actions
    - design a product listing
    - make selection easier
  examples:
    - add grid and list view to this product listing
    - design row selection for this table
    - add bulk delete to this list
    - make it easier to select multiple items
---

# Data Display and Selection

Complex data collections — products, files, users, orders, tasks — have no single correct view. Different tasks call for different views. Browsing benefits from grid; comparing details benefits from list or table; bulk management benefits from a dense table with mass actions. Give users the choice.

---

## View Modes

Offer multiple views when the data has both visual and detailed dimensions.

| View | Best for | When to default |
|---|---|---|
| **Grid** | Visual items: products, images, files, cards | When items are visually distinct and browsing is the primary task |
| **List** | Moderate detail: tasks, emails, articles | When a key piece of text or metadata drives selection |
| **Table** | Dense data: orders, reports, user management | When multiple columns of data must be compared |

**View toggle placement:** top-right of the collection, adjacent to sort/filter controls. Use icon buttons with tooltips (`grid`, `list`, `table`). Persist the user's choice in localStorage.

```
[Filter ▾]  [Sort ▾]          [⊞ Grid]  [☰ List]  [⊟ Table]
```

On mobile, collapse to the view that works best for the content — grid for visual items, list for text. Do not offer a view toggle on small screens unless both views are genuinely usable.

---

## Selection: Prefer Large Hit Areas

Checkboxes are small targets. Requiring users to hit a 16×16px checkbox to select a row is unnecessary friction — especially on touch devices.

**Default: the entire row or card is the selection target.**

- Click anywhere on the row → selects the row (background shifts, checkbox checks)
- The checkbox is a visual indicator of selection state, not the only way to select
- Keyboard: Space selects the focused row; Shift+click extends selection; Ctrl/Cmd+click toggles individual items

```css
.row {
  cursor: pointer;
  background: var(--color-surface);
  transition: background 100ms ease-out;
}
.row:hover {
  background: var(--color-grey-50);
}
.row.selected {
  background: var(--color-primary-subtle); /* subtle brand tint */
}
```

For cards in a grid, the entire card is the selection area — not just a checkbox in the corner.

---

## Selected State Visual Language

Selected items communicate their state through a background colour shift — not just a checkbox tick.

**Background:** `--color-primary-subtle` — the brand primary colour heavily desaturated and lightened to ~5–8% opacity. Perceptible but not jarring.

**Left border accent (optional):** A 3px left border in `--color-primary` reinforces the selected state for list and table rows.

**Checkbox:** Checked and filled with `--color-primary`. The checkbox is a secondary signal, not the primary one.

```css
.row.selected {
  background: var(--color-primary-subtle);    /* e.g. hsl(224, 21%, 94%) */
  border-left: 3px solid var(--color-primary);
}
```

**Do not** use a high-contrast or saturated background for selection — it competes with content and makes dense tables hard to read.

---

## Mass Actions

When one or more items are selected, mass actions appear. They disappear when nothing is selected.

**Placement:** A contextual toolbar that appears at the top of the collection (replacing or supplementing the standard toolbar) when selection is active.

```
[✓ 3 selected]  [Delete]  [Archive]  [Export]  [Move to ▾]  [× Clear]
```

- Lead with the selection count: "3 selected" — confirms the scope before any action
- Show only actions applicable to the selection — if some actions require a single item, disable them for multi-select
- "Clear" deselects everything and dismisses the toolbar
- Destructive mass actions (Delete) always trigger a confirm dialog naming the count: "Delete 3 projects? This cannot be undone."

**Select all:** A checkbox in the table header selects all items on the current page. A secondary action "Select all 247" extends to the full dataset.

```
[☑ Select all on page]  →  [Select all 247 results]
```

---

## Sorting and Filtering

### Column sorting (table view)
- Click a column header to sort ascending; click again for descending; third click clears sort
- Active sort column shows a directional arrow (↑ ↓)
- Only sortable columns are clickable — non-sortable columns have no hover state on header

### Filters
- Persistent filters belong in a sidebar or filter bar above the collection
- Active filters should be visible as chips/tags that can be individually removed
- "Clear all filters" removes all active filters in one action
- Filter count badge on the filter button when filters are active: `Filter (3)`

### Empty states
- **No results from filter:** "No results for these filters. [Clear filters]" — do not show a generic empty state
- **Genuinely empty collection:** show a call to action for the first item: "No projects yet. [Create project]"

---

## Table-Specific Patterns

### Sticky header
Table column headers stick to the top when scrolling vertically — users must always be able to see what each column means.

### Sticky first column
For wide tables that scroll horizontally, the first column (row identifier — name, ID) sticks to the left.

### Row actions
Per-row actions (Edit, Delete, View) appear on hover in the rightmost column. Do not show them at rest — they add visual noise.

```
[Name]  [Status]  [Date]  [Amount]          ← at rest
[Name]  [Status]  [Date]  [Amount]  [Edit] [⋯]  ← on hover
```

### Column resize and reorder
For enterprise data tables: allow columns to be resized by dragging the header border, and reordered by dragging the header. Persist the layout.

---

## Review Checklist

- [ ] Is a view mode toggle offered when data has both visual and detail dimensions?
- [ ] Is the user's preferred view persisted across sessions?
- [ ] Is the entire row or card the selection hit area — not just the checkbox?
- [ ] Does selected state use a subtle background colour shift (`--color-primary-subtle`)?
- [ ] Does a mass action toolbar appear when items are selected, showing the selection count?
- [ ] Do destructive mass actions require a confirm dialog naming the item count?
- [ ] Does "Select all" work per page, with an option to extend to the full dataset?
- [ ] Are active filters visible as removable chips?
- [ ] Does the empty state differ between "no results" and "genuinely empty"?
- [ ] Are per-row actions shown on hover only, not at rest?
- [ ] Is the table header sticky when the table scrolls vertically?
