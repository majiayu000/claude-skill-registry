---
name: af-retrofit-design-grammar
description: Retrofit the Design Grammar into existing projects that lack it. Use when adding token setup, integrating grammar definitions, or migrating an existing UI to grammar-compliant patterns.

# AgentFlow documentation fields
title: Design Grammar Retrofit Expertise
created: 2026-03-09
updated: 2026-03-09
last_checked: 2026-03-09
tags: [skill, expertise, design-grammar, retrofit, tokens, brownfield]
parent: ../README.md
related:
  - ../../docs/guides/design-grammar-retrofit-guide.md
  - ../af-design-ui-components/SKILL.md
  - ../af-setup-project/SKILL.md
---

# Design Grammar Retrofit Expertise

## When to Use This Skill

Load this skill when you need to:
- Add the Design Grammar to a project that doesn't have it
- Set up project-specific design tokens from the grammar token schema
- Connect an existing component library to grammar definitions
- Configure the token build pipeline (Style Dictionary)
- Set up Tokens Studio for Figma ↔ repo token sync
- Map existing components to grammar types (atoms, molecules, organisms)

**Common triggers:**
- Module Installation phase (after Discovery selects Design Grammar)
- Brownfield project needs shared design vocabulary
- Project has ad-hoc tokens/components, needs grammar alignment
- Team wants Figma round-trip for an existing codebase

## Quick Reference

**The Design Grammar** (`.design-grammar/`) is the shared cross-project vocabulary. It defines WHAT components exist and HOW they compose. Projects consume it — they never modify it.

**A Project Design System** (`tokens/`, `src/components/`) is the project-specific implementation. It fills in the grammar's token schema with real values and implements components following grammar definitions.

```
.design-grammar/ (shared, read-only)     →  tokens/ (project, writable)
├── tokens-schema/                        →  ├── colors.json
├── primitives/                           →  ├── typography.json
├── organisms/marketing/hero.json         →  └── spacing.json
└── schemas/organism.schema.json          →  src/components/organisms/Hero.tsx
```

**Retrofit is 5 steps:**
1. Create project tokens from grammar token schema
2. Configure build pipeline (Style Dictionary)
3. Map existing components to grammar types
4. Align Storybook to extended atomic hierarchy
5. (Optional) Set up Tokens Studio for Figma sync

## Rules

### Token Rules

1. **MUST create tokens following grammar token schema** — Use `.design-grammar/tokens-schema/` as the shape, fill with project values
2. **MUST use W3C DTCG format** — `{ "$value": "...", "$type": "..." }` not plain JSON
3. **MUST separate light/dark tokens** — Use `$extensions.mode` or separate files
4. **MUST NOT invent token names** — Use names from the grammar schema only
5. **Token files go in project `tokens/`** — Never in `.design-grammar/`

### Build Pipeline Rules

6. **MUST install pipeline dependencies** — Copy `.design-grammar/pipeline/package.json` deps into project
7. **MUST configure Style Dictionary** — Use `.design-grammar/pipeline/sd.config.js` as reference, adapt paths
8. **MUST generate CSS + Tailwind output** — `build/css/variables.css`, `build/tailwind/theme.js`
9. **MUST add build scripts to project** — `npm run tokens:validate`, `npm run tokens:build`
10. **SHOULD add pre-commit validation** — Warn when `tokens/**` files change without running build

### Component Mapping Rules

11. **MUST audit existing components first** — List all components, classify by grammar level
12. **Map, don't rewrite** — Document which existing component maps to which grammar type
13. **Fill gaps, don't duplicate** — Only create new components for grammar types not yet covered
14. **MUST use grammar prop names** — When refactoring, align prop names to grammar definitions
15. **Prioritise organisms** — They deliver the most visible grammar alignment

### Storybook Rules

16. **MUST restructure titles** — Use extended hierarchy: `Atoms/Button`, `Organisms/Hero`
17. **MUST add `primitives/` folder** if project has unstyled behavioural components
18. **MUST create view components** for page-level UI — `src/components/views/`
19. **Stories import views** — Both stories and pages use the same view component

## Workflows

### Workflow: Full Retrofit

**When:** Project selected Design Grammar in Discovery, entering Module Installation.

**Prerequisites:**
- Project has existing components/tokens (even if informal)
- `.design-grammar/` available (via AgentFlow sync)
- Node.js 18+ for Style Dictionary

**Steps:**

1. **Audit existing tokens**
   - Find where design values live (CSS vars, Tailwind config, theme files)
   - List all colors, typography, spacing, radii, shadows
   - Note any light/dark theme support

2. **Create project `tokens/` directory**
   ```
   tokens/
   ├── colors.json      ← DTCG format, project-specific values
   ├── typography.json
   └── spacing.json
   ```
   - Reference: `.design-grammar/examples/tokens/` for format
   - Reference: `.design-grammar/tokens-schema/` for required shape

3. **Set up build pipeline**
   - Install: `npm install -D style-dictionary @tokens-studio/sd-transforms`
   - Copy and adapt: `.design-grammar/pipeline/sd.config.js`
   - Add scripts: `tokens:validate`, `tokens:build`
   - Run: `npm run tokens:build` → verify CSS + Tailwind output

4. **Audit existing components**
   - List all components in `src/components/`
   - Classify each against grammar hierarchy:
     - Primitives: unstyled behaviour wrappers
     - Atoms: single-purpose styled elements
     - Molecules: small compositions (2-3 atoms)
     - Organisms: page sections
     - Templates: page layouts
   - Check `.design-grammar/sources/tailwind-plus/catalogue.json` for variant references

5. **Restructure component folders**
   ```
   src/components/
   ├── primitives/    ← behavioural (Pressable, Slot) + layout (Stack, Grid)
   ├── atoms/         ← Button, Badge, Input
   ├── molecules/     ← FormField, NavItem
   ├── organisms/     ← Hero, Pricing, DataTable
   ├── templates/     ← LandingTemplate, DashboardTemplate
   └── views/         ← PricingView, DashboardView (shared by stories + pages)
   ```

6. **Align Storybook**
   - Update story titles to use atomic prefixes
   - Create view components for page-level stories
   - Add responsive + theme variants if missing

7. **(Optional) Set up Tokens Studio**
   - Follow `.design-grammar/tokens-studio/README.md`
   - Install Figma plugin, configure git sync to `tokens/`
   - Test round-trip: change token in Figma → PR → merge → CSS updated

### Workflow: Lightweight Retrofit

**When:** Project wants grammar alignment without full restructure.

1. Create `tokens/` with DTCG format (step 2 above)
2. Set up build pipeline (step 3 above)
3. Document component-to-grammar mapping in `docs/design/component-mapping.md` — don't restructure folders yet
4. Gradually align as components are touched (boy scout rule)

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Rewriting all components at once | Map first, refactor gradually |
| Inventing new token names | Use grammar schema names only |
| Putting tokens in `.design-grammar/` | Project tokens go in `tokens/` |
| Skipping DTCG format | Use `$value`/`$type` — Style Dictionary requires it |
| Not running token build | Add `tokens:build` to CI and pre-commit |
| Flat component folders | Restructure to `primitives/atoms/molecules/organisms/templates/` |
| Missing view components | Create `src/components/views/` for page-level rendering |

## Essential Reading

**Grammar documentation:**
- `.design-grammar/README.md` — Grammar overview, directory structure
- `.design-grammar/pipeline/SPEC.md` — Build pipeline specification

**Retrofit guide (step-by-step with examples):**
- [Design Grammar Retrofit Guide](../../docs/guides/design-grammar-retrofit-guide.md)

**Related skills:**
- `af-design-ui-components` — Component design patterns, Storybook workflow
- `af-setup-project` — Module installation (where retrofit happens)
- `af-sync-figma-designs` — Figma round-trip (optional visual layer)

**Platform mappings:**
- `.design-grammar/platform-mappings/web-react.json` — ShadCN/Tailwind mapping
- `.design-grammar/platform-mappings/flutter-material.json` — Flutter Material 3 mapping
