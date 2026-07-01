---
name: coordinated-data-views
description: When data has both a tabular/list representation and a visual representation, show both simultaneously and keep them synchronized. Clicking a row highlights the corresponding element in the visual view, and vice versa. Applies to maps, diagrams, timelines, and charts that accompany a data table. Use when designing any UI where data appears in two different representations at once.
metadata:
  priority: 6
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "app/**"
  promptSignals:
    phrases:
      - "map view"
      - "chart view"
      - "visualization"
      - "linked views"
      - "coordinated"
      - "highlight"
      - "synchronize"
      - "side by side"
      - "table and chart"
      - "diagram and list"
retrieval:
  aliases:
    - coordinated views
    - linked views
    - chart and table
    - map and list
    - linked visualization
    - synchronized views
    - two representations
    - dual view
    - visual and tabular
  intents:
    - synchronize a chart with a data table
    - link a map to a list
    - highlight items across two views
    - design a dual-view layout
    - coordinate a chart with a table
    - keep two views in sync
  examples:
    - clicking a row should highlight it in the map view
    - the map and the list should stay in sync
    - show a diagram and a table for the same data
    - how should a visual view and a table interact
    - the user should be able to select from either the chart or the list
---

# Coordinated Data Views

Some data has more than one natural representation. A set of locations has both a map and a list. A dependency network has both a diagram and a node table. A dataset has both a chart and a raw table. When both representations are genuinely useful for different tasks, show them simultaneously and keep them synchronized — this is called a coordinated view.

The core rule: **any selection or highlight made in one view is immediately reflected in the other.**

---

## When to Use Coordinated Views

Use coordinated views when:

1. The two representations serve different tasks — the table is for finding/scanning; the visual view is for understanding arrangement or relationships
2. Users will frequently move between the two — not just glance at one occasionally
3. The dataset is large enough that the visual view alone doesn't identify individual items, and the table alone doesn't communicate how they relate

Do not add a coordinated view purely for visual richness. If users only ever look at the table and ignore the visual view, it adds complexity without benefit.

---

## The Synchronized Selection Model

Selection state is owned by a single shared store, not by either view. Both views read from and write to the same state.

```
Table row clicked → shared highlight state updated → both views re-render

Visual element clicked → shared highlight state updated → both views re-render
```

**What synchronization covers:**

| Interaction | Effect in table | Effect in visual view |
|---|---|---|
| Click row | Row highlights | Corresponding element highlighted |
| Click visual element | Corresponding row highlighted, scrolled into view | Element highlighted |
| Hover row | Subtle row highlight | Subtle element highlight |
| Hover visual element | Subtle row highlight | Subtle element highlight |
| Clear selection | Row returns to default | Element returns to default |

**Scroll-into-view:** When a visual element is clicked, the table must scroll to bring the corresponding row into view. A row that is highlighted but off-screen is useless.

---

## Consistent Colour Coding

Colour meaning must be identical in both views. If a category is orange in the table badge, it is orange in the visual view. Never use different colour assignments for the same data in different representations.

Define colours centrally:

```ts
const CATEGORY_COLORS = {
  groupA: 'hsl(24, 80%, 55%)',
  groupB: 'hsl(210, 70%, 55%)',
  groupC: 'hsl(145, 60%, 45%)',
} as const;
```

Both the table cell renderer and the visual element renderer import from the same source.

A shared legend appears once in the layout — not duplicated in each view.

---

## Layout

The split between views depends on which is primary:

**Table-primary (exploration, data management):** Table takes 60–70% of the width; visual view is a companion panel on the right or bottom.

**Visual-primary (understanding arrangement and relationships):** Visual view takes 60–70%; table is a supporting panel.

**Equal weight:** A 50/50 split with a draggable divider. Persist the user's preferred split.

```
┌─────────────────────┬────────────────┐
│                     │                │
│   Table (primary)   │  Visual view   │
│                     │                │
└─────────────────────┴────────────────┘
```

On mobile, show one view at a time with a tab or toggle to switch. Do not attempt to show both on a small screen.

---

## Visual View Controls

Controls that affect only the visual representation belong in the visual view panel, not in the table area.

Common visual-specific controls:
- **Zoom / pan** — navigation (usually handled by the rendering library)
- **Layer opacity** — reveal overlapping regions on a dense map or diagram
- **Layer toggle** — show/hide categories or types
- **Reset view** — fit all elements into view; extent reset for maps

These controls do not affect the table. Do not put them in the table toolbar.

Controls that affect the shared data (filters, time range, category selection) belong outside both views, above or beside the layout, since they affect what appears in both.

---

## Highlighting vs. Selection

These are distinct states:

**Highlight (hover):** Transient, shown while the pointer is over an element. Does not persist. Both views show a subtle version (e.g. 50% opacity overlay, or a faint row background). No interaction required to clear it — moving the pointer clears it.

**Selection (click):** Persistent until explicitly cleared. Both views show a strong, unambiguous visual (e.g. bright border, saturated colour, selected row background). Cleared by clicking elsewhere or pressing Escape.

Do not conflate these. A hover highlight that persists after the pointer leaves is confusing.

---

## Performance Considerations

Coordinated views can trigger expensive re-renders if not carefully managed.

- Debounce hover highlights — do not update on every pointer-move event, only when the target element changes
- Use stable identity for items (a consistent ID) so React (or equivalent) can reconcile without re-creating elements
- For large datasets (1000+ items), virtualize the table regardless of the visual view
- For canvas- or WebGL-rendered views, avoid re-creating elements on each highlight — update style properties on the existing ones instead

---

## Review Checklist

- [ ] Is selection state shared between views via a single store — not duplicated?
- [ ] Does clicking a row highlight the corresponding visual element, and vice versa?
- [ ] Does clicking a visual element scroll the table to the corresponding row?
- [ ] Are colour assignments identical in both views, defined from a single source?
- [ ] Is the shared legend shown once, not duplicated per view?
- [ ] Are visual-specific controls (zoom, transparency, layer toggle) in the visual panel, not the table?
- [ ] Are hover highlight and click selection visually distinct states?
- [ ] On mobile, is there a clear way to switch between views?
- [ ] Are hover events debounced to avoid unnecessary re-renders?
