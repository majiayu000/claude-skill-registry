---
name: scan-scss-styling
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/scss-styling-guide.md with BEM methodology, SCSS architecture, mixins, variables, theming, and responsive patterns.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan project stylesheets and populate `docs/project-reference/scss-styling-guide.md` with BEM methodology usage, SCSS architecture, mixins/variables inventory, theming patterns, responsive breakpoints, and design token conventions.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover styling patterns via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update reference doc from report
5. **Verify** — Validate file paths and variable names exist

**Key Rules:**

- Generic — works with any CSS methodology (SCSS, Less, CSS Modules, Tailwind, styled-components)
- Detect styling approach first, then scan for approach-specific patterns
- Every example must come from actual stylesheets with file:line references
- Focus on project conventions, not generic CSS tutorials

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan SCSS Styling

## Phase 0: Read & Assess

1. Read `docs/project-reference/scss-styling-guide.md`
2. Detect mode: init (placeholder) or sync (populated)
3. If sync: extract existing sections and note what's already well-documented

## Phase 1: Plan Scan Strategy

Detect styling approach:

- `*.scss` files → SCSS/Sass (check for BEM patterns, mixins, variables)
- `*.less` files → Less
- `*.module.css` / `*.module.scss` → CSS Modules
- `tailwind.config.*` → Tailwind CSS
- `styled-components` / `emotion` in package.json → CSS-in-JS
- Multiple approaches → document each

Identify styling infrastructure:

- Global styles entry point (`styles.scss`, `global.css`)
- Theme files (CSS custom properties, SCSS theme maps)
- Design token files (JSON tokens, CSS variables)
- Shared mixins/variables directories

Use `docs/project-config.json` styling section if available.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **2 Explore agents** in parallel:

### Agent 1: SCSS Architecture & Variables

- Glob for `**/*.scss` (or detected extension) to map stylesheet tree
- Find the main/global stylesheet entry points and their @import/@use chains
- Grep for SCSS variables (`$variable-name`) — inventory the most-used ones
- Find mixin definitions (`@mixin`) and their usage frequency
- Discover function definitions (`@function`)
- Find design token files (CSS custom properties `--token-name`, JSON token files)
- Look for breakpoint definitions and responsive mixins

### Agent 2: BEM Patterns & Theming

- Grep for BEM class patterns in templates/HTML (`block__element--modifier`)
- Find BEM naming conventions (separator style, nesting depth)
- Discover theming patterns (light/dark, CSS custom properties, theme switching)
- Find component-scoped vs global style patterns
- Look for z-index management (variables, scale)
- Find animation/transition conventions
- Identify color palette definitions and usage patterns

Write all findings to: `plans/reports/scan-scss-styling-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report. Build these sections:

### Target Sections

| Section                 | Content                                                                          |
| ----------------------- | -------------------------------------------------------------------------------- |
| **BEM Methodology**     | BEM naming convention used, nesting rules, examples from actual components       |
| **SCSS Architecture**   | File organization, import chain, global vs component styles                      |
| **Mixins & Variables**  | Inventory table: mixin/variable name, purpose, file location, usage count        |
| **Theming**             | Theme approach (CSS vars, SCSS maps, etc.), how to add/modify themes             |
| **Responsive Patterns** | Breakpoint definitions, responsive mixins, mobile-first vs desktop-first         |
| **Design Tokens**       | Token naming convention, categories (color, spacing, typography), file locations |
| **Color Palette**       | Color variables/tokens with their hex values and semantic names                  |
| **Z-Index Scale**       | Z-index variable definitions and layering conventions                            |

### Content Rules

- Show actual SCSS/CSS snippets (5-15 lines) from the project with `file:line` references
- Include variable/mixin inventory tables with usage counts
- Use color swatches or hex values for color palette documentation
- Show BEM examples from real components (not fabricated)

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: 5 stylesheet file paths exist (Glob check)
3. Verify: variable names in examples match actual SCSS definitions
4. Report: sections updated, variables counted, theming approach documented

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
