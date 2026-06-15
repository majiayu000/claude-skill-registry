---
name: layout-paradigms-and-consistency
description: A layout is not a neutral container — choosing the right layout paradigm (feed, board, table, canvas, master-detail, dashboard, gallery, timeline, map, single-focus) is a design decision that shapes how content is understood. Once chosen, the same paradigm and page skeleton must be reused consistently across the application so users build one mental model. This is consistency at the macro scale, above component and token consistency. Use when deciding the overall structure of a screen, designing page templates, or reviewing whether screens across a product feel like one coherent application.
metadata:
  priority: 8
  pathPatterns:
    - "app/**"
    - "pages/**"
    - "src/pages/**"
    - "src/app/**"
    - "**/layouts/**"
    - "**/templates/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.vue"
    - "**/*.svelte"
    - "design-system/**"
  promptSignals:
    phrases:
      - "layout"
      - "page layout"
      - "screen layout"
      - "layout paradigm"
      - "page template"
      - "app structure"
      - "dashboard layout"
      - "feed vs"
      - "master-detail"
      - "kanban"
      - "consistent layout"
      - "page structure"
  retrieval:
    aliases:
      - layout paradigm
      - layout archetype
      - page template
      - screen structure
      - layout consistency
      - cross-page consistency
      - app-wide layout
      - macro consistency
    intents:
      - choose the right layout for this content
      - decide the overall structure of a screen
      - design reusable page templates
      - keep layouts consistent across the app
      - review whether screens feel like one product
    examples:
      - should this be a feed, a table, or a board
      - what layout fits this kind of content
      - my detail pages are all structured differently
      - the app feels like several different products stitched together
      - design a consistent page template for these screens
---

# Layout Paradigms and Consistency

A layout is not a neutral container you pour content into. The layout paradigm you choose is part of the argument about how the content should be read, compared, and acted on. Two products showing the same data can communicate completely different things depending on whether that data is a feed, a table, or a board.

This skill operates at the **macro scale** of consistency. It sits above [[component-family-consistency]] (the *meso* scale — buttons and inputs sharing one DNA) and above token-level consistency like [[button-states]], [[status-colors-and-errors]], and [[modular-scale-typography]] (the *micro* scale). Consistency is not one rule — it is the same discipline applied at three altitudes.

## Consistency operates at three scales

| Scale | What stays consistent | Where it lives |
|---|---|---|
| **Macro** | Layout paradigm and page skeleton across screens | *this skill* |
| **Meso** | Component family — shared radius, height, colour logic | [[component-family-consistency]], [[brand-visual-language]] |
| **Micro** | States, tokens, type scale, semantic colours | [[button-states]], [[status-colors-and-errors]], [[modular-scale-typography]], [[algorithmic-color-palette]] |

A product can have perfect tokens and a coherent component family and still feel broken — because every screen is laid out differently and the user re-orients on every navigation. Macro consistency is what makes a product feel like *one* application.

---

## Layout is downstream — it serves something upstream

A layout paradigm is never the starting point. It is a *consequence* of decisions made earlier, and a *means* to ends defined elsewhere. Choosing a layout in isolation — "let's use a dashboard because dashboards look impressive" — is the most common way layouts go wrong.

**It flows down from information architecture.** The data model and structure ([[information-architecture]]) largely *determine* the candidate paradigms. Entities that move through states want a board; records compared on shared fields want a table; a hierarchy of containers and items wants master–detail. If the IA says "tasks belong to projects and have a status," the layout has already half-decided itself. Get the IA right first, then read the paradigm off it.

**It serves the brand and the story.** The same content can be laid out to feel calm or urgent, premium or utilitarian, editorial or operational. Layout is one of the loudest carriers of brand tone ([[brand-visual-language]]) and of the narrative you want the user to experience ([[motion-and-storytelling]]). A spacious single-focus layout tells a different story than a dense dashboard of the same data. Ask: *what should the user feel here, and what are we trying to say?* — then pick the paradigm that says it.

**It serves the user experience.** Ultimately the test is the user's task and context: what are they trying to do, how often, on what device, under what pressure ([[ui-density]], [[responsive-paradigms]]). The paradigm that best serves the task wins, even when a flashier one is available.

So the order is: **IA and brand intent first → derive the paradigm that supports them → then apply consistency.** Part 1 is how you derive it; Part 2 is how you keep it.

---

## Part 1 — Choose the paradigm that fits the content

Start from the nature of the content and the primary task, not from a default grid. Ask: *what relationship between items matters most here?* The answer points to a paradigm.

| Content nature / primary task | Layout paradigm | Why it fits | When NOT to use it |
|---|---|---|---|
| A stream of recent, homogeneous items, consumed top-down | **Feed** | Recency and flow are the message; infinite, low-commitment scanning | When items must be compared field-by-field, or order is not temporal |
| Items moving through stages of a workflow | **Board / Kanban** | Columns make state visible and transitions physical (drag) | When there are no discrete stages, or items have many attributes to compare |
| Many records compared across the same fields | **Table** | Aligned columns make values directly comparable; sort/filter is natural | When records are visual or heterogeneous, or on small screens |
| Browsing visual, heterogeneous items | **Gallery / Grid** | The artifact itself is the content; thumbnails carry meaning | When precise values matter more than the visual |
| A list plus the detail of the selected item | **Master–detail / Split** | Keeps context while drilling in; fast scanning + deep reading | On mobile where two panes don't fit (collapse to drill-down) |
| At-a-glance overview of many metrics | **Dashboard** | Spatial arrangement lets the eye triage what needs attention | When the user has one task, not monitoring — it becomes noise |
| Spatial relationships, free arrangement | **Canvas** | The user's spatial model *is* the data (diagrams, design, maps) | When content is inherently linear or ordered |
| Events ordered in time | **Timeline** | Time is the primary axis; gaps and density are meaningful | When time is just one of many equal attributes |
| Geographic data | **Map** | Location is the primary dimension | When location is incidental to the task |
| One object, one task, full attention | **Single-focus / Wizard** | Removes everything but the current decision | When the user needs surrounding context to decide → see [[user-flows-and-guided-paths]] |

The paradigm interacts with other layout skills: it must group coherently ([[gestalt-ui-organisation]]), establish one clear emphasis ([[visual-emphasis-and-hierarchy]]), reflect the data model and naming ([[information-architecture]]), and adapt — not merely shrink — across breakpoints ([[responsive-paradigms]]). Where a real-world metaphor reinforces the paradigm (a board feels like cards on a wall), lean on it ([[real-world-metaphors]]).

**A view can offer more than one paradigm.** A collection of records is legitimately a table *and* a gallery *and* a board, chosen by the user per task — see [[data-display-and-selection]]. The point is that each option is a *deliberate* fit, not an accident.

---

## Part 2 — Reuse the paradigm consistently across the application

Once a paradigm is chosen for a kind of content, every screen of that kind uses the same paradigm and the same page skeleton. This is what lets a user learn the product once.

### Page skeletons should be templates, not one-offs

Define a small set of page templates and reuse them:

- **List / index page** — same position for title, filters, view-mode toggle, primary action, and the collection itself, on *every* list page.
- **Detail page** — same skeleton for every detail screen: header (name + status + primary actions) → key attributes → related content → activity. When a user learns one detail page, they have learned them all.
- **Editor / form page** — consistent placement of the form body, validation summary, and the save/cancel actions → see [[form-design]].
- **Settings page** — consistent section structure and control alignment.

### What must stay in the same place across pages

- **Navigation** — global nav, breadcrumbs, and back affordances do not move between screens ([[ui-context-and-scope]]).
- **Primary action** — the main CTA sits in the same region on comparable pages, not top-right on one and bottom-left on the next.
- **Persistent chrome** — headers and toolbars behave consistently ([[sticky-and-fixed-elements]]).
- **Status and feedback** — toasts, banners, and inline errors appear in consistent locations ([[notifications-and-recovery]]).

This is **internal consistency** in Nielsen's terms (heuristic 4) — see [[nielsen-usability-heuristics]]. Familiar patterns within one application beat novel ones on every screen.

### When to deviate — and how

Consistency is the default, not a cage. Deviate when a screen's task genuinely differs (a focused checkout step legitimately drops the global nav). When you deviate:

- Do it for a clear reason tied to the task, not for visual variety.
- Deviate *completely and obviously* (a distinct mode), never subtly — a layout that is almost-but-not-quite the standard reads as a bug.
- Keep the deviation itself consistent: if focus mode hides nav, every focus-mode screen hides it the same way.

---

## Review Checklist

- [ ] Is the layout paradigm a deliberate fit for the content's nature and primary task — not a default grid?
- [ ] Could you state in one sentence *why* this paradigm beats the alternatives for this content?
- [ ] Do all screens of the same kind (all detail pages, all list pages) share one page skeleton?
- [ ] Does navigation stay in the same place across screens?
- [ ] Does the primary action sit in the same region on comparable pages?
- [ ] If a user learns one detail page, have they effectively learned them all?
- [ ] Where a screen deviates from the standard template, is there a clear task-driven reason — and is the deviation obvious rather than subtle?
- [ ] Does the product feel like one application rather than several stitched together?
