---
name: doc-view-roadmap
description: "{{ ƔƔƔ }} Visualise a project roadmap as an interactive HTML dashboard"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(open:*)", "Bash(mkdir:*)"]
argument-hint: [roadmap name or path (optional)]
---

Generate a self-contained HTML dashboard showing the current state of a project roadmap. Uses the visual-explainer skill's rendering patterns and a pink-to-sky colour palette derived from the user's terminal colour scheme.

## Step 1 — Locate the roadmap

Check in this order:

1. **`$ARGUMENTS` provided** — treat as roadmap name or path. Try `docs/roadmaps/$ARGUMENTS.md` then `docs/roadmaps/$ARGUMENTS`.
2. **`.claude/roadmaps.json`** — parse if present. One entry: use it. Multiple entries: list names and paths, ask the user to pick one.
3. **`docs/roadmaps/` directory** — list `.md` files. One file: use it. Multiple: ask.
4. **Fallback scan** — `Grep` for `classDef.*mile` to find roadmap files outside the standard location.

Stop and tell the user if nothing is found.

## Step 2 — Parse the roadmap

Read the file and extract:

**Milestone blocks** — for each `<a name="m{N}">` anchor:
- Milestone number and name
- Tasks per section: In Progress (`m{N}-doing`), To Do (`m{N}-todo`), Blocked (`m{N}-blocked`), Completed (`m{N}-done`)
- Per task: ID (e.g. `2TI.7`), description, any `depends on {IDs}` references

**Counts per milestone:**
```
total    = done + in_progress + todo + blocked
done_pct = done / total * 100
```

**Dependency edges** — extract `— **depends on {IDs}**` clauses into a map of `taskId → [blockedBy...]`.

**Status summary table** — read the top-level `| **Cat** | Status | Next Up | Blocked |` table if present.

## Step 3 — Load visual-explainer references

Resolve the installed path with Glob:
```
~/.claude/plugins/cache/visual-explainer-marketplace/visual-explainer/*/
```

Read these files before generating any HTML:
- `references/css-patterns.md` — depth tiers, Mermaid zoom controls, overflow protection, collapsible pattern
- `references/libraries.md` — font pairings, CDN imports, Mermaid theming guide
- `templates/mermaid-flowchart.html` — the full `diagram-shell` pattern with zoom/pan JS (~200 lines; copy wholesale)
- `references/responsive-nav.md` — sticky sidebar TOC + mobile horizontal nav

Do **not** skip any of these. The zoom/pan JS in particular must be reproduced exactly.

## Step 4 — Aesthetic and palette

### Colour palette

Derive from the user's terminal gradient: warm pink (`#B34480`) → steel blue (`#3E7F96`), mapped to Reasonable Colors.

Load the CDN stylesheet in `<head>`:
```html
<link rel="stylesheet" href="https://unpkg.com/reasonable-colors@0.4.0/reasonable-colors.css">
```

Define semantic aliases — components reference these only, never RC vars directly:

```css
:root {
  /* Milestone — sky family (≈ #3E7F96) */
  --color-milestone:      var(--color-sky-4);     /* #007590 */
  --color-milestone-bg:   var(--color-sky-1);     /* #e3f7ff */
  --color-milestone-text: var(--color-sky-6);     /* #001f28 */

  /* Primary accent — pink family (≈ #B34480) */
  --color-primary:        var(--color-pink-4);    /* #d2008f */
  --color-primary-bg:     var(--color-pink-1);    /* #fff7fb */
  --color-primary-text:   var(--color-pink-6);    /* #4b0030 */

  /* Task status */
  --color-done:           var(--color-teal-4);    /* #007c6e */
  --color-done-bg:        var(--color-teal-1);    /* #d7fff7 */
  --color-in-progress:    var(--color-sky-4);
  --color-in-progress-bg: var(--color-sky-1);
  --color-todo:           var(--color-gray-4);    /* #6f6f6f */
  --color-todo-bg:        var(--color-gray-1);    /* #f6f6f6 */
  --color-blocked:        var(--color-pink-4);
  --color-blocked-bg:     var(--color-pink-1);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-milestone:      var(--color-sky-2);   /* #aee9ff */
    --color-milestone-bg:   var(--color-sky-6);   /* #001f28 */
    --color-milestone-text: var(--color-sky-1);
    --color-primary:        var(--color-pink-2);  /* #ffdcec */
    --color-primary-bg:     var(--color-pink-6);
    --color-primary-text:   var(--color-pink-1);
    --color-done:           var(--color-teal-2);
    --color-done-bg:        var(--color-teal-6);
    --color-in-progress:    var(--color-sky-2);
    --color-in-progress-bg: var(--color-sky-6);
    --color-todo:           var(--color-gray-3);
    --color-todo-bg:        var(--color-gray-6);
    --color-blocked:        var(--color-pink-3);
    --color-blocked-bg:     var(--color-pink-5);
  }
}
```

Shade differences of ≥ 3 guarantee WCAG AA body text contrast on all pairs.

### Aesthetic direction

**Editorial + Blueprint hybrid:**
- Light: warm off-white (`var(--color-gray-1)`), sky-tinted milestone headers, generous whitespace, subtle CSS grid-line background pattern
- Dark: deep near-black, muted sky/pink accents, low-opacity borders
- Font: **IBM Plex Sans + IBM Plex Mono** — load via Google Fonts CDN
- No emoji in section headers — use styled monospace labels with coloured dot indicators
- Forbidden: Inter/Roboto body font, violet/indigo accents, gradient-text headings, glowing animated shadows

## Step 5 — Generate the HTML

### Output location

```bash
mkdir -p {project_root}/docs/diagrams
```

Write to `{project_root}/docs/diagrams/roadmap-{name}.html`.

### Page structure

Use the responsive section navigation from `references/responsive-nav.md`. Four sections:

1. **Overview** — overall progress KPI cards + per-milestone mini progress bars
2. **Milestones** — one collapsible card per milestone with full task breakdown
3. **Dependency Graph** — Mermaid diagram of the full task graph
4. **Next Up** — unblocked tasks grouped by milestone

### Section 1: Overview

Hero KPI card (`ve-card--hero`): **`{done}/{total} tasks — {pct}% complete`**. Large type, accent-tinted background.

Per-milestone mini-cards in a CSS Grid row:
- Milestone name and number
- `{done}/{total}` count
- Coloured progress bar — CSS `linear-gradient`, width set via inline `style`:

```html
<div class="progress-bar">
  <div class="progress-fill" style="width: {pct}%"></div>
</div>
```

Colour the fill by milestone health: high completion → `--color-done`, in-flight → `--color-in-progress`, unstarted → `--color-todo`, has blockers → `--color-blocked`.

### Section 2: Milestones

One `<details>/<summary>` per milestone. Open whichever milestone has In Progress tasks; collapse the rest.

Inside each card, four labelled groups:

```
● In Progress   ○ To Do   ✓ Done   ✗ Blocked
```

Task items: ID badge (monospace, small, accent-tinted) + description + dependency note.

**Overflow rule:** never `display: flex` on `<li>`. Use `position: relative` + `padding-left` for status indicators. All grid/flex children get `min-width: 0`.

### Section 3: Dependency Graph

Use the full `diagram-shell` pattern from `templates/mermaid-flowchart.html`. Never bare `<pre class="mermaid">`.

Map the roadmap's existing `:::open` / `:::blocked` / `:::mile` classDefs to the semantic palette:

```
classDef open    fill:var(--color-todo-bg),      stroke:var(--color-todo),      color:var(--color-todo);
classDef blocked fill:var(--color-blocked-bg),   stroke:var(--color-blocked),   color:var(--color-blocked);
classDef mile    fill:var(--color-milestone-bg), stroke:var(--color-milestone), color:var(--color-milestone-text);
classDef done    fill:var(--color-done-bg),      stroke:var(--color-done),      color:var(--color-done);
```

- Use `graph TD`. For 15+ nodes add `layout: 'elk'` (see libraries.md CDN import).
- Mermaid theme: `theme: 'base'` with `themeVariables` matching the page palette.
- `fontSize: 16` in `themeVariables`.
- Line breaks in labels: use `<br/>`, never `\n`.

### Section 4: Next Up

Flat prioritised list of tasks that are **In Progress** or **To Do with no unresolved dependencies**. Group by milestone. Each item: task ID badge + description + milestone label pill.

## Step 6 — Quality checks

Before writing the file:

- [ ] Every `.mermaid-wrap` has +/−/reset/expand buttons, Ctrl/Cmd+scroll zoom, drag-to-pan, click-to-expand
- [ ] Light and dark themes both look intentional
- [ ] No page-level `.node` CSS class (breaks Mermaid SVG positioning)
- [ ] All grid/flex children have `min-width: 0`; `overflow-wrap: break-word` on text containers
- [ ] Progress bar percentages match parsed task counts
- [ ] Reasonable Colors CDN `<link>` present in `<head>`
- [ ] IBM Plex Sans + IBM Plex Mono loaded via Google Fonts
- [ ] No Inter/Roboto, no violet/indigo accents, no gradient-text headings, no emoji headers, no animated glow shadows

## Step 7 — Open and confirm

```bash
open {project_root}/docs/diagrams/roadmap-{name}.html
```

Report:
- File path written
- Roadmap name, milestone count, total task count
- Any tasks currently In Progress (surfaced immediately, without needing to open the file)
