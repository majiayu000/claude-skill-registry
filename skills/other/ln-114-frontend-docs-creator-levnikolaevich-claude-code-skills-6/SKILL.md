---
name: ln-114-frontend-docs-creator
description: Creates design_guidelines.md for frontend projects. L3 Worker invoked CONDITIONALLY when hasFrontend detected.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Frontend Documentation Creator

L3 Worker that creates design_guidelines.md. CONDITIONAL - only invoked when project has frontend.

## Purpose & Scope
- Creates design_guidelines.md (if hasFrontend)
- Receives Context Store from ln-110-project-docs-coordinator
- WCAG 2.1 Level AA accessibility compliance
- Design system documentation
- Never gathers context itself; uses coordinator input

## Invocation (who/when)
- **ln-110-project-docs-coordinator:** CONDITIONALLY invoked when:
  - `hasFrontend=true` (react, vue, angular, svelte detected)
- Never called directly by users

## Inputs
From coordinator:
- `contextStore`: Context Store with frontend-specific data
  - DESIGN_SYSTEM (Material-UI, Ant Design, custom)
  - COLOR_PALETTE (primary, secondary, accent)
  - TYPOGRAPHY (font families, sizes, weights)
  - COMPONENT_LIBRARY (detected components)
- `targetDir`: Project root directory
- `flags`: { hasFrontend }

## Documents Created (1, conditional)

| File | Condition | Questions | Auto-Discovery |
|------|-----------|-----------|----------------|
| docs/project/design_guidelines.md | hasFrontend | Q43-Q45 | Low |

## Workflow

### Phase 1: Check Conditions
1. Parse flags from coordinator
2. If `!hasFrontend`: return early with empty result

### Phase 2: Create Document
1. Check if file exists (idempotent)
2. If exists: skip with log
3. If not exists:
   - Copy template
   - Replace placeholders with Context Store values
   - Populate design system section
   - Mark `[TBD: X]` for missing data

### Phase 3: Self-Validate
1. Check SCOPE tag
2. Validate sections:
   - Design System (component library)
   - Typography (font families, sizes)
   - Colors (hex codes, semantic colors)
3. Check WCAG 2.1 references
4. Check Maintenance section

### Phase 4: Return Status
```json
{
  "created": ["docs/project/design_guidelines.md"],
  "skipped": [],
  "tbd_count": 1,
  "validation": "OK"
}
```

## Critical Notes

### Core Rules
- **Conditional:** Skip entirely if no frontend detected
- **WCAG compliance:** Document must reference accessibility standards
- **Design tokens:** Extract from CSS variables, tailwind config, or theme files
- **Idempotent:** Never overwrite existing files

### NO_CODE_EXAMPLES Rule (MANDATORY)
Design guidelines document **visual standards**, NOT code:
- **FORBIDDEN:** CSS code blocks, component implementations
- **ALLOWED:** Tables (colors, typography), design tokens, Figma links
- **INSTEAD OF CODE:** "See [Component Library](link)" or "See src/components/Button.tsx"

### Stack Adaptation Rule (MANDATORY)
- Link to correct component library docs (MUI for React, Vuetify for Vue)
- Reference framework-specific patterns (React hooks, Vue composition API)
- Never mix stack references (no React examples in Vue project)

### Format Priority (MANDATORY)
Tables (colors, typography, spacing) > Lists (component inventory) > Text

## Definition of Done
- Condition checked (hasFrontend)
- Document created if applicable
- Design system, typography, colors documented
- WCAG references included
- **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- Status returned to coordinator

## Reference Files
- Templates: `references/templates/design_guidelines_template.md`
- Questions: `references/questions_frontend.md` (Q43-Q45)

---
**Version:** 1.1.0
**Last Updated:** 2025-01-12
