---
name: shipflow-audit-design
description: Professional UI/UX design review — single page (with argument) or full project audit (no argument)
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -100 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Tailwind/CSS config: !`cat tailwind.config.* 2>/dev/null | head -80 || echo "no tailwind config"`
- Global styles: !`cat src/styles/global.css 2>/dev/null || cat src/assets/styles/*.css 2>/dev/null | head -100 || echo "no global styles found"`
- All pages: !`find src/pages src/app -name "*.astro" -o -name "*.tsx" -o -name "*.vue" 2>/dev/null | grep -v node_modules | sort`
- Component files: !`find src/components -name "*.astro" -o -name "*.tsx" -o -name "*.vue" 2>/dev/null | grep -v node_modules | sort`
- Legacy patterns: !`grep -rn --include="*.{js,ts,jsx,tsx,astro,vue}" -E '\balert\(|\bconfirm\(|\bprompt\(|\bdocument\.write\(' src/ 2>/dev/null | head -20 || echo "none found"`
- Deprecated HTML: !`grep -rn --include="*.{astro,vue,tsx,jsx,html}" -iE '<marquee|<blink|<center|<font ' src/ 2>/dev/null | head -20 || echo "none found"`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit ALL projects in the workspace.
- **`$ARGUMENTS` is a file path** → PAGE MODE: review that single page.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full design audit of the entire project.

---

## GLOBAL MODE

Audit ALL UI projects in the workspace for design, UX, and accessibility issues.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the Design column.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for design & UX?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md
   - All applicable projects pre-listed as options

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 6 phases: Design System Inventory → Outdated Patterns Scan → Page-by-Page Scan → Cross-Page Consistency → Fix → Report)
   - The **Tracking** section from this skill
   - Rule: **read-only analysis** — no code fixes, only update AUDIT_LOG.md and TASKS.md

4. After all agents return, compile a **cross-project design report**:

   ```
   GLOBAL DESIGN AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Systemic design issues in 2+ projects]
   ALL ISSUES BY SEVERITY
     🔴 [project] file:line — description
     🟠 [project] file:line — description
     🟡 [project] file:line — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, Design column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: Design` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## PAGE MODE

### Step 1: Gather the page

1. Read the target file (`$ARGUMENTS`).
2. Read its layout/wrapper component if it imports one.
3. Read any component files it imports (follow the imports).
4. Read the relevant CSS/Tailwind classes used.

### Step 2: Audit against this checklist

Score each category **A/B/C/D** (A = excellent, D = critical issues). Be strict — professional standard.

#### 1. Visual Hierarchy & Layout
- [ ] Clear primary action / CTA above the fold
- [ ] Logical reading flow (F-pattern or Z-pattern)
- [ ] Proper whitespace rhythm — consistent spacing scale (not arbitrary px values)
- [ ] Content sections have clear visual separation
- [ ] No orphaned headings, dangling text, or layout widows

#### 2. Typography
- [ ] Heading hierarchy is semantic (h1 > h2 > h3, no skipped levels)
- [ ] Body text is 16px+ with line-height >= 1.5
- [ ] Max line width ~65-75 characters (measure/prose constraint)
- [ ] Font pairing is intentional (max 2-3 families)
- [ ] No font-size under 14px except legal/fine print

#### 3. Color & Contrast
- [ ] WCAG AA contrast ratios (4.5:1 text, 3:1 large text/UI)
- [ ] Color is not the only way to convey information
- [ ] Consistent color token usage (no hardcoded hex outside design system)
- [ ] Interactive elements have visible focus/hover/active states
- [ ] Dark mode support if the project uses it

#### 4. Responsiveness
- [ ] Mobile-first or gracefully responsive (no horizontal scroll)
- [ ] Touch targets >= 44x44px on mobile
- [ ] Images/media have proper aspect ratio handling
- [ ] Navigation works on small screens
- [ ] No content hidden or broken between 320px-1440px

#### 5. Component Consistency
- [ ] Buttons follow a single pattern (size, radius, padding)
- [ ] Cards/containers have consistent elevation/border treatment
- [ ] Icons are same set and consistent size
- [ ] Spacing uses design system tokens, not arbitrary values
- [ ] States are covered: empty, loading, error, populated

#### 6. Accessibility
- [ ] All images have meaningful alt text (or alt="" for decorative)
- [ ] Form inputs have visible labels (not just placeholders)
- [ ] Keyboard navigation works (tab order, focus visible)
- [ ] ARIA roles where needed (modals, menus, tabs)
- [ ] Skip navigation link present if applicable
- [ ] Animations respect `prefers-reduced-motion`
- [ ] **Click target propagation**: Containers with a single action child (icon button, hamburger menu, link) should make the whole container clickable — add `onClick`/`role="button"`/`tabIndex={0}`/`onKeyDown` to parent, `cursor-pointer` + hover state for feedback, `e.stopPropagation()` on secondary actions. Skip if: multiple competing actions, destructive action (precise click = safety), drag surface, or form controls (use `<label>` instead)

#### 7. No Outdated Patterns
- [ ] No `alert()`, `confirm()`, or `prompt()` browser dialogs — use toast/modal components
- [ ] No `document.write()` — never acceptable
- [ ] No deprecated HTML (`<marquee>`, `<blink>`, `<center>`, `<font>`)
- [ ] No inline `onclick="..."` handlers — use framework event handling
- [ ] No jQuery when using a modern framework
- [ ] No `innerHTML` for user-facing content (XSS risk)

### Step 3: Fix what you can

For each issue rated B or worse:
1. Explain the problem with the specific line/component.
2. Fix it directly in the code.
3. If a fix requires a design decision (e.g., color choice), propose 2 options and ask the user.

### Step 4: Report

```
DESIGN REVIEW: [page name]
─────────────────────────────────────
Visual Hierarchy   [A/B/C/D] — one-line summary
Typography         [A/B/C/D] — one-line summary
Color & Contrast   [A/B/C/D] — one-line summary
Responsiveness     [A/B/C/D] — one-line summary
Consistency        [A/B/C/D] — one-line summary
Accessibility      [A/B/C/D] — one-line summary
Modern Patterns    [A/B/C/D] — one-line summary
─────────────────────────────────────
OVERALL            [A/B/C/D]

Fixed: X issues | Remaining: Y issues
```

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `src/` dir, no `tailwind.config.*`) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for design?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run design audit across every UI project" (Recommended)
  - One option per UI project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### Phase 1: Design System Inventory

Read the Tailwind config, global styles, and 5-10 representative components. Document:

1. **Color palette**: List all colors actually used (Tailwind classes + custom). Flag inconsistencies (e.g., `text-gray-600` AND `text-gray-500` for similar purposes).
2. **Typography scale**: List all font sizes, weights, and line heights in use. Flag violations of the scale.
3. **Spacing system**: Check if spacing is consistent (Tailwind scale) or has arbitrary values.
4. **Component patterns**: Identify repeated patterns (cards, buttons, sections). Flag inconsistencies between instances.
5. **Breakpoint usage**: Check if responsive breakpoints are consistent.

### Phase 2: Outdated Patterns Scan

Search the entire codebase for legacy/outdated patterns:

**JavaScript browser dialogs**:
- [ ] `alert(` — replace with toast/notification component
- [ ] `confirm(` — replace with modal dialog component
- [ ] `prompt(` — replace with form input/modal
- [ ] `document.write(` — never acceptable

**Outdated UI patterns**:
- [ ] `<marquee>`, `<blink>`, `<center>`, `<font>` tags
- [ ] `<table>` used for layout (tables only for tabular data)
- [ ] Inline `onclick="..."` handlers
- [ ] `<iframe>` for layout purposes (embeds like YouTube/maps are fine)

**Deprecated CSS patterns**:
- [ ] `!important` overuse (more than 2-3 instances is a red flag)
- [ ] Vendor prefixes without autoprefixer
- [ ] Fixed pixel font sizes below `14px` for body text
- [ ] `float` used for primary layout (use flexbox/grid)

**Legacy JS patterns**:
- [ ] jQuery when using a modern framework
- [ ] `innerHTML` for user-facing content
- [ ] `setTimeout`/`setInterval` for UI state

**Undersized click targets & action propagation**:

Look for containers where a small child element (icon button, hamburger, link, toggle) is the sole interactive element but the parent is not clickable. Flag when: container has descriptive content + exactly one primary action + container is NOT already interactive. Fix: propagate action to parent with `onClick`, `role="button"`, `tabIndex={0}`, `cursor-pointer` + hover state. Do NOT propagate when: multiple competing actions, destructive action, drag surface, or form controls.

### Phase 3: Page-by-Page Scan

For each page, check:
- [ ] Visual hierarchy
- [ ] Design system consistency
- [ ] Responsive behavior
- [ ] Accessibility (contrast, alt text, focus states, ARIA)
- [ ] Click targets
- [ ] States: loading, empty, error
- [ ] No layout shifts

### Phase 4: Cross-Page Consistency

- [ ] Header/footer identical across pages
- [ ] Navigation active states work correctly
- [ ] Consistent card/list treatment across content types
- [ ] Consistent spacing between sections
- [ ] Favicon, apple-touch-icon, and theme-color present

### Phase 5: Fix

Fix all issues directly in code. Prioritize:
1. **Accessibility violations** (legal risk + user impact)
2. **Design system inconsistencies** (fix in components, not per-page)
3. **Responsive breakages** (mobile-first)
4. **Missing states** (loading/error/empty)

### Phase 6: Report

```
DESIGN AUDIT: [project name]
═══════════════════════════════════════

DESIGN SYSTEM HEALTH
  Colors:     X tokens used, Y inconsistencies
  Typography: X sizes used, Y violations
  Spacing:    [consistent / mixed / chaotic]
  Components: X patterns, Y inconsistencies

OUTDATED PATTERNS
  Browser dialogs:  X found
  Legacy HTML:      X found
  Deprecated CSS:   X found
  Legacy JS:        X found
  Click targets:    X containers with undersized single-action children

PAGE SCORES
  /                  [A/B/C/D]
  /about             [A/B/C/D]
  ...

CROSS-PAGE CONSISTENCY    [A/B/C/D]
ACCESSIBILITY             [A/B/C/D]
RESPONSIVENESS            [A/B/C/D]
═══════════════════════════════════════
OVERALL                   [A/B/C/D]

Fixed: X issues across Y files
Needs decision: Z items (listed below)
```

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append a row filling only the Design column, `—` for others.
2. **Project-local `./AUDIT_LOG.md`**: same without the Project column.

Create either file if missing.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace an `### Audit: Design` subsection with critical (🔴), high (🟠), and medium (🟡) issues as task rows.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace an `### Audit: Design` subsection with the same tasks. Update the Dashboard "Top Priority" if critical issues found.

---

## Important (all modes)

- Be ruthlessly honest. A-level means genuinely production-ready, not "it works".
- When the project has a design system or Tailwind config, enforce its tokens — don't introduce new arbitrary values.
- Respect the project's existing aesthetic. Improve, don't redesign.
- If the project content is in French, review in that language context (French text is ~15% longer than English).
- **All `<textarea>` elements MUST use `field-sizing: content`** — flag and fix any textarea missing this property.
- In project mode, identify **systemic** problems and fix at the source (component/config level), not per-page.
