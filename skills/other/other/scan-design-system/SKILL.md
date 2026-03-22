---
name: scan-design-system
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/design-system/README.md with design system overview, app-to-doc mapping, design tokens, and component inventory.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan project for design system artifacts and populate `docs/project-reference/design-system/README.md` with an overview of the design system, app-to-documentation mapping, design token inventory, and component catalog.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover design system structure via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update reference doc from report
5. **Verify** — Validate component paths and token files exist

**Key Rules:**

- Generic — works with any design system approach (custom, Storybook, Figma tokens, etc.)
- Discover design system organization dynamically from file system
- Map relationships between apps and their design documentation
- Every reference must point to real files found in this project

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan Design System

## Phase 0: Read & Assess

1. Read `docs/project-reference/design-system/README.md`
2. Detect mode: init (placeholder) or sync (populated)
3. If sync: extract existing sections and note what's already well-documented
4. Also check for app-specific design docs in the same directory

## Phase 1: Plan Scan Strategy

Discover design system locations:

- `docs/project-reference/design-system/` directory and its contents
- Storybook config (`.storybook/`, `*.stories.ts`)
- Design token files (JSON, CSS, SCSS variables)
- Component library directories (shared components, UI kit)
- Figma token exports or style dictionary config

Use `docs/project-config.json` designSystem section if available for:

- `docsPath` — where design docs live
- `appMappings` — which apps have which design docs

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **2 Explore agents** in parallel:

### Agent 1: Design System Structure

- Glob for `docs/project-reference/design-system/**` to map all design docs
- Find design token files (CSS custom properties, SCSS variables, JSON tokens)
- Discover Storybook stories (`*.stories.ts`, `*.stories.tsx`, `*.stories.mdx`)
- Find component library entry points (index files, barrel exports)
- Look for style dictionary or token transformation configs
- Map app-to-design-doc relationships (which app uses which design doc)

### Agent 2: Component Inventory

- Grep for reusable UI components (shared component directories, exported components)
- Find component categories (layout, forms, feedback, navigation, data display)
- Discover component variants (size, color, state variations)
- Count components per category
- Find icon sets or asset libraries
- Look for accessibility patterns in components (ARIA roles, keyboard support)
- Find documentation for individual components (JSDoc, README, Storybook docs)

Write all findings to: `plans/reports/scan-design-system-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report. Build these sections:

### Target Sections

| Section                    | Content                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| **Design System Overview** | High-level description of the design system approach, tools, and organization               |
| **App Documentation Map**  | Table: App name, Design doc path, Token source, Component library                           |
| **Design Tokens**          | Token categories (color, typography, spacing, elevation), file locations, naming convention |
| **Component Inventory**    | Table: Component name, Category, Variants, Path, Has docs?                                  |
| **Icon & Asset Library**   | Icon set source, asset directory paths, usage patterns                                      |
| **Storybook**              | Storybook setup (if exists), story organization, how to add new stories                     |
| **Usage Guidelines**       | How to consume tokens and components in application code                                    |

### Content Rules

- Use tables for component inventory and token listings
- Include actual token values (colors, spacing scale) where practical
- Show component usage examples from real application code
- Map each app to its specific design documentation file

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: 3 design doc paths exist on filesystem
3. Verify: component paths in inventory match actual files
4. Report: sections updated, component count, token categories documented

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
