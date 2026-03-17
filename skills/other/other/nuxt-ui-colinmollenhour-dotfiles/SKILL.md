---
name: nuxt-ui
description: Use when implementing or debugging UI features with Nuxt UI components, designing forms, tables, modals, or any user interface work - fetches current documentation to ensure accurate component APIs
---

# Nuxt UI Skill

**Source of Truth:** `https://ui.nuxt.com/llms.txt` for all Nuxt UI component APIs.

Nuxt UI v4 is actively developed with frequent changes. Training data may be outdated. Always verify component APIs before implementing.

## Mandatory Workflow

### Step 1: Fetch Targeted Documentation

Before implementing ANY Nuxt UI component, execute a WebFetch request:

```
WebFetch to https://ui.nuxt.com/llms.txt with prompt:
"Extract ONLY the documentation for [UComponent] from Nuxt UI.
Include: Props, Slots, Events, code examples.
Exclude everything else. Return a concise summary."
```

**CRITICAL**: Never fetch the full documentation. Use targeted extraction to avoid context bloat.

### Step 2: Read Relevant Guide

Read the appropriate guide for your task:

| Task | Guide |
|------|-------|
| Form validation, inputs, selects | `FORMS.md` |
| Data tables with filtering | `TABLES.md` |
| Modals, slideovers, popovers | `OVERLAYS.md` |
| Buttons, dropdowns, badges, layout | `COMPONENTS.md` |
| Best practices, accessibility, common mistakes | `PATTERNS.md` |

### Step 3: Implement with Type Safety

All implementations must use:
- Zod schemas for form validation
- Proper TypeScript types
- `FormSubmitEvent<Schema>` for form handlers

## Red Flags - Stop and Fetch Docs First

| Warning Sign | Why It's Dangerous |
|-------------|-------------------|
| "I know how UModal works" | API may have changed |
| "This is a simple component" | Simple tasks have highest error rates |
| Using `@close` instead of `v-model:open` | Event names change between versions |
