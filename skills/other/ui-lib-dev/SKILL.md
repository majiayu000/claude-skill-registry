---
name: ui-lib-dev
description: (ePost) Use when building, auditing, or documenting UI library components through the Figma-to-code pipeline across web, iOS, or Android platforms
user-invocable: false

metadata:
  agent-affinity: [epost-muji, epost-fullstack-developer]
  keywords: [klara-theme, component, components, pipeline, audit, storybook]
  platforms: [all]
  connections:
    requires: [figma]
---

# klara-theme Skill

Domain knowledge for the klara-theme UI component library. Provides patterns for the complete Figma-to-code pipeline: planning, implementation, auditing, fixing, and documentation.

## Pipeline Overview

```
plan-feature → implement-component → audit-ui → fix-findings → document-component
```

Each stage has a dedicated aspect file with detailed steps, inputs, outputs, and success criteria.

## Aspect Files

| Aspect | Purpose | Key Outputs |
|--------|---------|-------------|
| `references/plan-feature.md` | Plan a new UI feature from Figma designs | 6 JSON plan artifacts |
| `references/implement-component.md` | Implement component from plan artifacts | Component code + Storybook stories |
| `references/audit-ui.md` | Audit implementation against plan and Figma | `audit-report.json` |
| `references/fix-findings.md` | Resolve audit findings | `PATCH.diff` or `fix-notes.json` |
| `references/document-component.md` | Document component with Figma data | `.figma.json` + `.mapping.json` |
| `references/audit-standards.md` | Enforceable klara-theme rules (all sections: KBLOAD, STRUCT, PROPS, TOKEN, BIZ, A11Y, TEST, SEC, PERF, LDRY, EMBED) | Pass/fail criteria per rule |
| `references/guidance.md` | Integration consulting workflow, design-code conflict resolution | Fix suggestions, consumer guidance checklist |

## Before Using This Skill — Load Live KB (Mandatory)

klara-theme has a structured knowledge base in `libs/klara-theme/docs/`. Always read the registry first — each entry has an `agentHint` that tells you when it applies.

**Step 1 — Read the registry:**
```
libs/klara-theme/docs/index.json
```

**Step 2 — Load by pipeline stage:**

| Pipeline Stage | Load these entries |
|---------------|--------------------|
| Any stage (baseline) | **CONV-0001** component structure, **FEAT-0001** component catalog |
| Plan feature | **ARCH-0001** architecture, **CONV-0003** props naming, **CONV-0006** tokens, **CONV-0007** BIZ isolation |
| Implement component | **CONV-0001**, **CONV-0003**, **CONV-0005** translations, **CONV-0006** tokens |
| Audit UI | **CONV-0001** through **CONV-0007** (all conventions), **FEAT-0001** catalog |
| Fix findings | Load the entry that corresponds to the violated convention (use finding `ruleId` prefix: STRUCT→CONV-0001, PROPS→CONV-0003, TOKEN→CONV-0006, BIZ→CONV-0007, A11Y→CONV-0004) |
| Document component | **FEAT-0001** catalog, **CONV-0001** structure |

If `index.json` is missing, fall back to: `Glob libs/klara-theme/docs/**/*.md` and read directly.

## Quick Reference

### Input/Output Directory

All per-feature artifacts live in:
```
libs/klara-theme/.ai-agents/ui/<feature>/
```

### Key Resources

- **Figma extraction**: `figma` skill
- **Token system**: `libs/klara-theme/_tokens/` (3-layer: primitives, themes, components)
- **Schemas**: `libs/klara-theme/figma-data/schema/`

### Build Commands

- Lint: `nx lint klara-theme`
- Test: `nx test klara-theme`
- Storybook: `npm run storybook-theme-build`

## Conventions

- **Reuse-first**: Always check existing components before creating new ones
- **Token-only**: No hardcoded values; use design tokens from the 3-layer system
- **Storybook coverage**: Default, Sizes, Variants, States stories for every component
- **forwardRef pattern**: All components use `forwardRef` with `displayName`
- **TypeScript strict mode**: Required for all component code

## Related Documents

- `libs/klara-theme/CLAUDE.md` — Component patterns, tokens, conventions
- `figma` skill — Figma MCP integration

## Platform-Specific Pipelines

The pipeline stages apply to all platforms. Platform differences:

| Stage | Web | iOS | Android |
|-------|-----|-----|---------|
| Source | `libs/klara-theme/` | `ios_theme_ui/` | `android_theme_ui/theme/` |
| Components | React + TypeScript | SwiftUI | Jetpack Compose |
| Tokens | CSS custom properties | Swift constants | Kotlin theme objects |
| Stories/Docs | Storybook | Xcode Previews | Compose Previews |
| Artifacts | `.ai-agents/ui/` | `.ai-agents/ui/` | `.ai-agents/ui/` |

Load platform-specific ui-lib skill (web-ui-lib, ios-ui-lib, android-ui-lib) via skill-discovery for component API reference.
