---
name: ui-density
description: UI density — how much information and how many features appear at once — should match the primary platform and user type. Desktop supports dense, feature-rich interfaces; mobile requires focused, reduced layouts. Enterprise power users tolerate higher density than occasional users. Use when designing data tables, dashboards, toolbars, or adapting a desktop product for mobile.
metadata:
  priority: 7
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
  promptSignals:
    phrases:
      - "density"
      - "compact"
      - "spacious"
      - "too crowded"
      - "too much"
      - "feature count"
      - "information density"
      - "data table"
      - "dashboard"
retrieval:
  aliases:
    - ui density
    - compact layout
    - spacious layout
    - information density
    - feature count
    - dashboard density
  intents:
    - decide how dense the UI should be
    - make a dashboard less overwhelming
    - design a compact data table
    - reduce feature count on mobile
    - match density to user type
  examples:
    - this dashboard feels overwhelming
    - how dense should this table be
    - reduce this for mobile
    - this is an enterprise tool, can it be denser
---

# UI Density

Density describes how much information and how many interactive elements appear in a given area. The right density is not a universal standard — it depends on platform, user type, and session context.

## Platform Defaults

| Platform | Default density | Reason |
|---|---|---|
| Desktop | Medium to high | Large screen, precise input, often primary work surface |
| Tablet | Medium | Touch input, larger than phone but less than desktop |
| Mobile | Low | Small screen, touch targets need space, interrupted sessions |

Never port a dense desktop layout directly to mobile. Remove, collapse, or deprioritise features rather than shrinking them.

## User Type and Density

| User type | Appropriate density | Examples |
|---|---|---|
| Power user / enterprise | High density acceptable | Trading platforms, ERP, analytics, developer tools |
| Occasional / general user | Medium — clear visual breathing room | SaaS dashboards, project management |
| Consumer / first-time user | Low — guided, uncluttered | Onboarding flows, consumer apps, e-commerce |

A trading platform operator sits in the product for 8 hours a day and has learned every pixel — high density serves them. A user visiting a settings page once a month needs clear space and obvious labels.

## Density Tokens

Define spacing scale with density in mind. A compact variant reduces padding without changing structure:

```css
/* Default density */
--density-row-height:    44px;
--density-cell-padding:  var(--space-3) var(--space-4);
--density-gap:           var(--space-4);

/* Compact (enterprise / data-heavy) */
[data-density="compact"] {
  --density-row-height:    32px;
  --density-cell-padding:  var(--space-2) var(--space-3);
  --density-gap:           var(--space-2);
}

/* Spacious (consumer / onboarding) */
[data-density="spacious"] {
  --density-row-height:    56px;
  --density-cell-padding:  var(--space-4) var(--space-6);
  --density-gap:           var(--space-6);
}
```

## Feature Count by Platform

Not every feature belongs on every platform. For each feature ask: does a mobile user need this right now?

| Priority | Mobile | Tablet | Desktop |
|---|---|---|---|
| Core task | Always | Always | Always |
| Secondary actions | Collapsed (menu/sheet) | Visible | Visible |
| Filters and sorting | Accessible but not persistent | Collapsible | Persistent sidebar or toolbar |
| Bulk actions | Hidden or minimal | Reduced | Full |
| Advanced settings | Link to separate screen | Link or panel | Inline or panel |
| Data visualisation | Simplified (key metric only) | Reduced chart | Full chart |

## Density and Feature Reduction on Mobile

Sections and features can be removed, collapsed, or repositioned on smaller viewports — not just resized.

- **Remove:** Decorative sidebars, secondary data columns, promotional banners
- **Collapse:** Filters, advanced options, secondary navigation into accordions or bottom sheets
- **Reposition:** Toolbars move from top to bottom (thumb reach), sidebars move to drawers
- **Simplify:** A multi-column data table becomes a card list; a full chart becomes a single key metric

Progressive disclosure is the principle: show the minimum needed to complete the primary task, reveal more on demand.

## Review Checklist

- [ ] Is the density appropriate for the primary platform (desktop = can be denser, mobile = must be sparse)?
- [ ] Is the density appropriate for the user type (power user = higher density, consumer = more space)?
- [ ] Are spacing tokens used to define density — not one-off padding values?
- [ ] On mobile: are secondary features collapsed, repositioned, or removed rather than shrunk?
- [ ] Are touch targets ≥ 44×44px even in compact density variants?
- [ ] Is a density toggle offered for enterprise tools where users have strong personal preferences?
