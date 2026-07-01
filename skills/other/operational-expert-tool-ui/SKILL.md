---
name: operational-expert-tool-ui
description: Operational expert tools — used by domain specialists for hours every day — require a different design approach than consumer or occasional-use software. Information density, workflow linearity, and at-a-glance status take priority over whitespace and discoverability. Use when designing dispatch tools, warehouse management, logistics, scheduling, or any B2B tool whose primary users are trained specialists.
metadata:
  priority: 7
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "app/**"
    - "pages/**"
  promptSignals:
    phrases:
      - "dispatch"
      - "warehouse"
      - "logistics"
      - "operations"
      - "operator"
      - "workflow tool"
      - "professional tool"
      - "expert user"
      - "power user"
      - "B2B tool"
      - "scheduling"
      - "planning tool"
retrieval:
  aliases:
    - operational UI
    - expert tool
    - dispatch UI
    - warehouse management
    - logistics UI
    - professional tool
    - B2B tool
    - scheduling UI
    - planning tool
    - power user interface
  intents:
    - design a tool for expert users
    - design a dispatch or logistics interface
    - design a workflow-driven tool
    - make a dense data UI for professionals
    - design an operational planning tool
  examples:
    - this is used by warehouse staff all day
    - design a dispatch tool for logistics operators
    - design a planning UI for professional schedulers
    - how should a tool for expert users be different from a consumer app
    - the users know the domain deeply but are not developers
---

# Operational Expert Tool UI

An operational expert tool is software used by trained domain specialists — warehouse operators, dispatchers, planners, analysts — as their primary work surface, often for the entire working day. These users are not beginners discovering a product; they are professionals executing a defined job with the tool as their instrument.

This is a fundamentally different design context from consumer software or occasional-use SaaS. The design priorities are reversed: density and speed of action take precedence over discoverability and visual spaciousness.

---

## Primary Design Principles

### 1. Information over whitespace

An expert user does not need breathing room to orient themselves — they know the tool. Every pixel of empty space is a missed opportunity to show data they need to act on.

- Use compact row heights (28–36px) for data tables
- Show secondary attributes (status, type, date) inline, not on hover or in a detail panel
- Prefer text labels over icons alone — experts read fast, icon-only UIs slow them down at the margins

### 2. Workflow linearity

Expert tools are used to complete a defined task sequence, not to browse. Design the layout to reflect the workflow order: left to right, or top to bottom, matching the mental model of the task.

```
[Step 1: Select items]  →  [Step 2: Configure]  →  [Step 3: Execute]
```

The UI should make the next step obvious at every point, without hiding it behind menus or requiring navigation away from the current context.

### 3. Persistent state

Filters, column widths, view modes, and open/closed panels are part of the operator's work context. They should survive page reloads and be consistent between sessions unless the user explicitly resets them.

Do not reset the UI on every visit — the expert has spent time configuring it to their workflow.

---

## Hierarchical Accordion Tables

Many operational domains have naturally hierarchical data: an order contains lines; a route contains stops; a project contains tasks. The right pattern is an in-place accordion, not a drill-down to a separate page.

```
▶ Order #1042   ACME Corp    3 lines    Pending
▼ Order #1089   Globex       2 lines    Ready
    ├─ Line 1   Widget A    Qty: 12    ✓ In stock
    └─ Line 2   Widget B    Qty:  4    ✗ No stock
▶ Order #1091   Initech      5 lines    Pending
```

**Why accordion over page navigation:**
- Context is preserved — the operator can see multiple orders simultaneously
- Status across siblings is visible without navigating back
- Keyboard navigation (expand/collapse with arrow keys) keeps hands on the keyboard

**Per-row inclusion toggles:** In planning and staging workflows, each row may need to be explicitly included or excluded from a batch operation. Use a checkbox or toggle per row that is always visible — not hidden on hover.

---

## At-a-Glance Status Indicators

Operators make decisions based on status. Status should be visible without interaction.

| Good | Avoid |
|---|---|
| Coloured dot or pill always visible in the row | Status only visible on hover or in a tooltip |
| 2–3 status states with distinct colours | More than 5 status colours (hard to memorise) |
| Status label beside colour for accessibility | Colour alone as the only indicator |
| Consistent colour semantics across the whole tool | Same colour meaning different things in different tables |

Status colour conventions should align with `status-colors-and-errors` — green for ready/complete, amber for warning/pending, red for error/blocked, grey for inactive.

---

## Workflow-State Filters vs. Search Filters

Expert tools often have two distinct types of filters that should be treated differently in the UI:

**Workflow-state filters** narrow the dataset to the operator's current work scope. They persist, they are broad, and they represent a decision ("I am working on today's orders that are not yet assigned"). Place these in a permanent filter bar or sidebar, always visible.

**Search filters** find a specific item within the current scope. They are transient. Place these in a search input that can be cleared quickly.

Do not merge these into a single filter UI — the operator switches mental mode between "what scope am I working in?" and "where is that specific item?"

```
[Workflow scope: Today ▾]  [Status: Unassigned ▾]  [Stock: Available ▾]
                                                     ↑ Persistent workflow-state filters

    Search within scope: [___________]
                                                     ↑ Transient search
```

---

## Keyboard Navigation

Expert users learn keyboard shortcuts. They should not be required, but they dramatically increase throughput for trained users.

- Arrow keys navigate rows in a table
- Space or Enter expands an accordion row
- Escape closes an open panel or dialog
- Common actions have discoverable shortcuts (shown in tooltips: `Delete [Del]`, `Include [Space]`)

Do not rely on right-click context menus as the only path to actions — they are not discoverable and break keyboard-only workflows.

---

## Action Feedback at Scale

When an operation affects many items (batch assign, mass status update), the feedback must be proportional:

- For fewer than ~10 items: inline confirmation is sufficient
- For 10–100 items: a toast notification with count ("42 orders updated")
- For 100+ items: a progress indicator during the operation, then a summary on completion

Never silently complete a bulk operation with no feedback — the expert needs to confirm their action took effect.

---

## Review Checklist

- [ ] Is the information density appropriate for trained daily users (compact rows, inline status)?
- [ ] Does the layout reflect the workflow sequence (left-to-right or top-to-bottom task flow)?
- [ ] Are filters, view modes, and open panels persisted across sessions?
- [ ] Is hierarchical data shown as in-place accordions, not separate pages?
- [ ] Are per-row inclusion controls always visible, not hidden on hover?
- [ ] Are status indicators always visible without interaction?
- [ ] Are workflow-state filters separated from transient search filters?
- [ ] Are common actions accessible via keyboard?
- [ ] Does bulk operation feedback scale with the number of affected items?
