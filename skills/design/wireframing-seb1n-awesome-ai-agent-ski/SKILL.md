---
name: wireframing
description: Create text-based wireframes at low, mid, and high fidelity with component inventories, interaction annotations, and responsive breakpoint specifications. Use when the user requests wireframing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Wireframing

This skill enables the agent to produce wireframes at three fidelity levels — low-fi (block layouts and content hierarchy), mid-fi (defined components with placeholder content), and high-fi (pixel-accurate specs with real content, spacing values, and interaction notes). Since the agent works in text, wireframes are rendered as ASCII/box-drawing layouts or structured component specifications with precise dimensions. Each wireframe includes a component inventory, interaction annotations, and responsive breakpoint behavior.

## Workflow

1. **Clarify the Screen and Its Purpose**: Identify which screen or view to wireframe, its role in the user flow, and the primary user action on that screen. Determine the target platform (desktop web, tablet, mobile) and any framework constraints (e.g., Bootstrap grid, Material Design components). This scoping prevents wireframes from growing beyond their intended focus.

2. **Define the Component Inventory**: List every UI component the screen requires: navigation bars, headings, cards, forms, buttons, tables, modals, tooltips, empty states, and loading states. For each component, note its content requirements (label text, data fields, image dimensions) and its interactive behavior (clickable, expandable, draggable, editable). This inventory becomes the wireframe's bill of materials.

3. **Create the Low-Fidelity Layout**: Produce a block-level layout showing content zones and their spatial relationships. Use ASCII box drawing to represent regions. Focus on information hierarchy: what the user sees first, second, third. Do not specify exact pixel values or real content at this stage — use labels like `[Hero Image]`, `[Product Grid 3×2]`, `[CTA Button]`.

4. **Elevate to Mid-Fidelity**: Replace placeholder labels with representative content. Add specific component types (dropdown vs. radio, text input vs. textarea), define column counts and approximate proportions, and note key spacing relationships (e.g., "16px gap between cards"). Include navigation states (active tab, breadcrumb trail) and basic content hierarchy (heading levels, body text, captions).

5. **Produce High-Fidelity Specifications**: Add exact dimensions, spacing values (in px or rem), typography specs (font, size, weight, line-height), color token references, border-radius values, and shadow levels. Annotate every interactive element with its behavior: hover state, focus state, click action, validation rules, error messages. Include responsive breakpoint notes describing what changes at each breakpoint.

6. **Document Responsive Behavior**: For each wireframe, specify layout changes at mobile (< 640px), tablet (640-1023px), and desktop (≥ 1024px). Describe which components stack, collapse, hide, or reflow. Note touch target sizes for mobile (minimum 44x44px) and any gesture interactions (swipe to dismiss, pull to refresh).

## Usage

Provide the agent with the screen name, its purpose, the target platform, and the desired fidelity level. Include any existing design system tokens or component library references. The agent will produce a wireframe with a component inventory and interaction annotations.

## Examples

### Example 1: ASCII Wireframe for an Analytics Dashboard

**User Request**: "Create a low-to-mid fidelity wireframe for a web analytics dashboard. Desktop layout. It should show a sidebar nav, KPI summary cards, a line chart, and a data table."

**Agent Response**:

```
┌──────────────────────────────────────────────────────────────────────┐
│  ┌─────────┐   Dashboard                     🔔  👤 Jane Smith ▾   │
│  │  LOGO   │                                                        │
├──┴─────────┴─┬───────────────────────────────────────────────────────┤
│              │                                                       │
│  Dashboard • │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
│  Analytics   │  │ Total Users │ │  Revenue    │ │ Bounce Rate │    │
│  Reports     │  │   12,482    │ │  $48,250    │ │   34.2%     │    │
│  Settings    │  │  ▲ +8.3%   │ │  ▲ +12.5%  │ │  ▼ -2.1%   │    │
│              │  └─────────────┘ └─────────────┘ └─────────────┘    │
│              │                                                       │
│              │  ┌───────────────────────────────────────────────┐    │
│              │  │                                               │    │
│              │  │          Sessions Over Time (Line Chart)      │    │
│              │  │       ___/\      /\                           │    │
│              │  │     _/    \____/  \___                        │    │
│              │  │   _/                  \__                     │    │
│              │  │  Jan  Feb  Mar  Apr  May  Jun                 │    │
│              │  │                                               │    │
│              │  └───────────────────────────────────────────────┘    │
│              │                                                       │
│              │  ┌───────────────────────────────────────────────┐    │
│              │  │  Page            Views    Bounce   Avg Time   │    │
│              │  │  ─────────────── ──────── ──────── ────────── │    │
│              │  │  /home           8,421    32.1%    2m 14s     │    │
│              │  │  /pricing        3,892    28.7%    3m 42s     │    │
│              │  │  /docs           2,104    41.3%    5m 08s     │    │
│              │  │  /blog           1,876    45.6%    1m 52s     │    │
│              │  │                                               │    │
│              │  │  ◀ 1 2 3 ... 12 ▶                  Showing   │    │
│              │  │                                    1-10 of 47 │    │
│              │  └───────────────────────────────────────────────┘    │
│              │                                                       │
└──────────────┴───────────────────────────────────────────────────────┘
```

**Component inventory**:
| Component | Content | Interaction |
|-----------|---------|-------------|
| Sidebar nav | 4 items: Dashboard, Analytics, Reports, Settings | Click to navigate; active item has bold + left accent border |
| KPI cards (×3) | Metric name, value, % change with trend arrow | Click to drill down to detail view |
| Line chart | Time series, 6-month range, single dataset | Hover for tooltip with exact values; date range selector above |
| Data table | 4 columns, sortable, paginated (10 rows/page) | Click column header to sort; click row to view page detail |
| Top bar | Logo, page title, notification bell, user avatar + dropdown | Bell shows count badge; avatar opens profile/logout menu |

**Responsive behavior**: At tablet (< 1024px), the sidebar collapses to an icon-only rail (48px wide). At mobile (< 640px), the sidebar becomes a bottom tab bar with 4 icons; KPI cards stack vertically in a single column; the data table switches to a card-list layout with one card per row.

### Example 2: Mobile App Screen Specification with Annotations

**User Request**: "Create a high-fidelity wireframe spec for a mobile app 'Create Task' screen. Include form fields, validation, and interaction notes."

**Agent Response**:

**Screen: Create Task (Mobile, 375px width)**

```
┌─────────────────────────────────┐
│  ← Back        Create Task      │  ← Top bar: 56px height
│─────────────────────────────────│
│                                 │
│  Task Name *                    │  ← Label: 14px/500, gray-600
│  ┌─────────────────────────────┐│
│  │ Enter task name...          ││  ← Input: 44px height, 16px text
│  └─────────────────────────────┘│
│  ⚠ Task name is required        │  ← Error: 12px/400, red-500
│                                 │
│  Description                    │
│  ┌─────────────────────────────┐│
│  │                             ││
│  │ Add details...              ││  ← Textarea: 120px min-height
│  │                             ││
│  └─────────────────────────────┘│
│                                 │
│  Priority                       │
│  ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ Low  │ │ Med  │ │ High │   │  ← Segmented control: 36px h
│  └──────┘ └──────┘ └──────┘   │
│                                 │
│  Due Date                       │
│  ┌─────────────────────────────┐│
│  │ 📅  Select date...          ││  ← Tappable, opens date picker
│  └─────────────────────────────┘│
│                                 │
│  Assignee                       │
│  ┌─────────────────────────────┐│
│  │ 👤  Select team member...   ││  ← Opens searchable member list
│  └─────────────────────────────┘│
│                                 │
│  ┌─────────────────────────────┐│
│  │        Create Task          ││  ← Primary button: 48px height
│  └─────────────────────────────┘│    bg: blue-600, text: white
│                                 │
└─────────────────────────────────┘
```

**Detailed specifications**:
- **Screen padding**: 16px horizontal, 24px top (below nav), 32px bottom (safe area)
- **Field spacing**: 20px between field groups (label + input + error)
- **Input fields**: height 44px, border 1px gray-300, border-radius 8px, padding 12px horizontal. Focus state: border blue-500, ring 2px blue-100.
- **Error state**: Red-500 border on input, error message appears below with 4px top margin, `aria-describedby` linking input to error text.
- **Priority segmented control**: Equal-width segments filling the available width minus padding. Selected segment: bg blue-600, text white, border-radius 6px. Unselected: bg gray-100, text gray-700.
- **Create Task button**: Full width, 48px height, border-radius 10px. Disabled state (no task name): bg gray-300, not tappable. Loading state: spinner replaces text.
- **Keyboard behavior**: Tapping "Task Name" opens keyboard with return key labeled "Next" which moves focus to Description. Tapping "Description" opens keyboard with return key labeled "Done."

**Validation rules**:
- Task Name: required, max 100 characters. Show error on blur if empty.
- Description: optional, max 1000 characters. Show character count at 800+.
- Priority: defaults to "Med" if not selected.
- Due Date: optional. Cannot be in the past. If selected and then cleared, no error.

## Best Practices

- **Start at the lowest fidelity that answers the current question**: If the question is "what content goes on this page?", a low-fi block layout is sufficient. Do not produce pixel specs when the layout itself is still undecided.
- **Include empty and error states in every wireframe**: A screen that only shows the happy state is incomplete. Wireframe what the user sees when there is no data, when a request fails, and when validation errors appear.
- **Annotate interactions, not just layout**: Static wireframes omit critical design decisions. Note what happens on tap, swipe, hover, and focus for every interactive element directly on the wireframe.
- **Use real representative content, not lorem ipsum**: Real content exposes layout problems that placeholder text hides — long names that overflow, short descriptions that leave awkward whitespace, numbers with varying digit counts.
- **Specify responsive behavior alongside the wireframe**: A wireframe without breakpoint notes will be interpreted differently by every developer. State explicitly what stacks, collapses, hides, or reflows at each breakpoint.
- **Maintain a component inventory per screen**: List every component with its content requirements and interaction behavior. This inventory serves as a checklist for both design review and development implementation.

## Edge Cases

- **Screen requires infinite scroll or pagination**: Wireframe the initial loaded state, the loading-more indicator (skeleton rows or spinner), and the end-of-list state ("No more results"). Note the scroll trigger point (e.g., "Load more when 200px from bottom").
- **Content is user-generated and length is unpredictable**: Show the wireframe with both a minimal-content version (one-word title, no description) and a maximal-content version (100-character title, full paragraph description). Define truncation rules: max lines, ellipsis behavior, "Show more" toggle.
- **Screen must support multiple user roles**: If an admin sees edit/delete buttons that a viewer does not, wireframe both variants and label them clearly. Note which elements are conditionally visible and what controls their visibility.
- **Offline or slow connection state**: Wireframe a skeleton/placeholder version of the screen that appears while data loads. Include an explicit error state for failed network requests with a retry action.
- **Accessibility requirements affect layout**: If the wireframe includes color-only status indicators (red/yellow/green dots), add a text label or icon alternative. Note minimum tap target sizes (44x44px) for all interactive elements in the mobile wireframe.
