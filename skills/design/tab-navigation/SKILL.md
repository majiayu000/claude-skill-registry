---
name: tab-navigation
description: Tabs organise related content under a shared context — switching tabs swaps the view without leaving the page. Use when a screen has multiple distinct content areas that share a common header or action set, and when the user needs to switch between them frequently. Use when designing tabbed layouts, content panels, settings pages, detail views, or dashboards with multiple data views.
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
      - "tab"
      - "tabs"
      - "tab panel"
      - "tabbed"
      - "tab navigation"
      - "tab bar"
      - "tab strip"
      - "content switcher"
      - "pivot"
retrieval:
  aliases:
    - tab navigation
    - tab panel
    - tabbed interface
    - content switcher
    - tab bar
    - pivot control
  intents:
    - design a tabbed layout
    - add tabs to a detail view
    - organise content with tabs
    - switch between data views
    - build a settings page with tabs
  examples:
    - add tabs to this product detail page
    - design a settings screen with tab navigation
    - organise these data views with a tab strip
    - make it easy to switch between different reports
---

# Tab Navigation

Tabs organise related content under a shared context. The tab strip communicates the full set of available views; switching tabs swaps the content panel without a page navigation. They work best when all views share a heading, a primary action, or a common subject — tabs that have nothing to do with each other belong in separate pages.

---

## When to Use Tabs — and When Not To

| Use tabs when… | Use something else when… |
|---|---|
| 2–7 views share a common context (same record, same settings section) | There are more than 7–8 tabs — use a sidebar or section nav instead |
| Users switch between views frequently during a session | The content is sequential (use a stepper/wizard instead) |
| All tabs are equally valid entry points | One view is clearly primary — put the rest in a secondary nav or overflow |
| The views share a header or set of page-level actions | Each "tab" requires a different header and layout — use separate pages |

---

## Tab Types

Choose the visual style that fits the layout context.

### Underline / Indicator Tabs
A horizontal strip with a sliding underline or bottom border on the active tab. The lightest treatment — appropriate for page-level tabs where the tab strip sits inside the content area.

```
Overview  |  Activity  |  Settings
──────────
```

### Contained / Boxed Tabs
Each tab is a distinct box; the active tab appears connected to the panel below. Higher visual weight — appropriate for prominent tab groups near the top of a screen or within a card.

### Pill / Button Tabs
Rounded capsules that toggle between states. Lower emphasis — appropriate for secondary content switches within a section (not page-level). Often used for view toggles (e.g. "List / Grid / Map").

---

## Anatomy

```
┌─────────────────────────────────────────────────┐
│  Tab A  │  Tab B  │  Tab C  │                   │  ← Tab strip (role="tablist")
├─────────┴─────────────────────────────────────────┤
│                                                   │
│   Tab panel content                               │  ← Tab panel (role="tabpanel")
│                                                   │
└───────────────────────────────────────────────────┘
```

- **Tab strip:** Fixed height (typically 40–48px). Does not scroll with the page — consider making it sticky when the page is long.
- **Tab panel:** Fills the remaining available height. The panel, not the tab strip, scrolls when content overflows.
- **Active indicator:** A 2–3px bottom border in `--color-primary` for underline tabs; filled background for contained/pill tabs.

---

## States

| State | Visual treatment |
|---|---|
| Active | Primary colour indicator; label in `--color-text-primary` or primary |
| Inactive | Muted label (`--color-text-secondary`); no indicator |
| Hover | Subtle background shift (`--color-grey-50`); label slightly darkens |
| Focus | Visible focus ring (`outline: 2px solid --color-primary; outline-offset: 2px`) |
| Disabled | Reduced opacity (`0.4`); `cursor: not-allowed`; never the active tab |

Never disable the active tab. If content is unavailable, show it inside the panel with an explanation rather than disabling the tab.

---

## Tab Overflow

When the tab strip is wider than the viewport or container, do not wrap tabs onto multiple lines — it destroys the strip metaphor.

### Scrollable strip
The strip scrolls horizontally. Show a fade/gradient at the right edge to signal overflow. On touch devices this is the preferred solution.

```css
.tab-strip {
  display: flex;
  overflow-x: auto;
  scrollbar-width: none; /* hide scrollbar visually on desktop */
}
.tab-strip::after {
  content: '';
  position: absolute; right: 0;
  background: linear-gradient(to left, var(--color-surface), transparent);
  pointer-events: none;
}
```

### "More" overflow menu
Show as many tabs as fit, then collapse the rest into a `More ▾` dropdown. Update the "More" label when an overflowed tab is active: `Settings ▾` (showing the active hidden tab name).

For desktop dashboards with many views, prefer a sidebar nav over overflow tabs.

---

## Vertical Tabs

Use when there are 5+ tabs and the layout has a left sidebar. Vertical tabs allow longer labels without overflow issues and scale more gracefully.

- Fixed width sidebar (typically 200–240px) with tab labels stacked vertically
- Active tab: left border accent (`3px solid --color-primary`) + subtle background
- The main content area fills the remaining width

---

## Keyboard Navigation

Tabs follow the ARIA "roving tabindex" pattern for within-strip navigation.

| Key | Action |
|---|---|
| `Tab` | Move focus to the tab strip (then into the active panel) |
| `←` / `→` | Move between tabs (horizontal strip); activate immediately or on Enter depending on content cost |
| `↑` / `↓` | Move between tabs (vertical strip) |
| `Home` | Jump to first tab |
| `End` | Jump to last tab |
| `Enter` / `Space` | Activate focused tab (if not already auto-activating on arrow key) |

**Auto-activate vs. manual activate:** If switching tabs triggers a network request, use manual activation (arrow keys move focus, Enter activates) to avoid unnecessary fetches. If content is already loaded or cheap, auto-activation on arrow key is acceptable.

---

## ARIA

```html
<div role="tablist" aria-label="Product sections">
  <button
    role="tab"
    id="tab-overview"
    aria-selected="true"
    aria-controls="panel-overview"
    tabindex="0"
  >Overview</button>
  <button
    role="tab"
    id="tab-activity"
    aria-selected="false"
    aria-controls="panel-activity"
    tabindex="-1"
  >Activity</button>
</div>

<div
  role="tabpanel"
  id="panel-overview"
  aria-labelledby="tab-overview"
>…</div>

<div
  role="tabpanel"
  id="panel-activity"
  aria-labelledby="tab-activity"
  hidden
>…</div>
```

- `aria-selected="true"` on the active tab, `false` on all others
- `tabindex="0"` on the active tab, `-1` on all others (roving tabindex)
- `hidden` attribute (or `display: none`) on inactive panels — screen readers skip hidden panels
- `aria-label` on the `tablist` when the heading above doesn't sufficiently describe the group

---

## State Persistence

Remember the active tab across page loads and navigations:

- **URL fragment or query param:** `?tab=activity` — the most robust approach; supports deep linking and browser back/forward
- **localStorage:** Acceptable for preferences (e.g. a preferred dashboard view) that don't need to be shareable
- Do not use `sessionStorage` — tabs closing lose the state unexpectedly

When the URL contains a tab param, jump to that tab on load even if it's not the first tab.

---

## Nested Tabs

Avoid tabs within tabs. Nested tabbing creates confusion about scope — a user editing content in "Tab A › Sub-tab 2" has no clear mental model of what the outer tab means.

If you find yourself nesting tabs, reconsider the information architecture:
- Can the inner tabs become a secondary nav (pills, a sidebar within the panel)?
- Can the outer tabs become a top-level page nav instead?

One level of tabs maximum in the primary content area.

---

## Review Checklist

- [ ] Are there 2–7 tabs, each sharing a common subject or context?
- [ ] Is the tab strip not wrapping to multiple lines on any target viewport?
- [ ] Does tab overflow use scrollable strip or a "More" menu — not wrapping?
- [ ] Is the active tab clearly distinguished by colour and/or indicator?
- [ ] Do hover and focus states meet contrast requirements?
- [ ] Are disabled tabs avoided (showing unavailability inside the panel instead)?
- [ ] Does keyboard navigation follow roving tabindex (←/→ between tabs, Tab into panel)?
- [ ] Is `role="tablist"`, `role="tab"`, `role="tabpanel"`, and `aria-selected` set correctly?
- [ ] Are inactive panels hidden from the accessibility tree (`hidden` attribute)?
- [ ] Is the active tab persisted in the URL (for deep-linkable views) or localStorage?
- [ ] Are nested tabs avoided?
