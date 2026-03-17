---
name: client-components
description: Enforces project client component conventions for interactive React components with hooks, event handlers, Radix UI integration, and server action consumption. Extends react-coding-conventions with client-specific patterns.
---

# Client Components Skill

## Purpose

This skill provides client-specific React conventions that extend the base react-coding-conventions skill. It covers patterns unique to client components: hooks, interactivity, event handling, and server action consumption.

## When to Use This Skill

Use this skill in the following scenarios:

- Creating components with 'use client' directive
- Implementing useState, useEffect, or other hooks
- Adding event handlers (onClick, onChange, etc.)
- Consuming server actions via useServerAction
- Building interactive UI with Radix primitives
- Creating forms with TanStack Form

**Important**: This skill should activate automatically when client component work is detected.

## Prerequisite Skills

This skill REQUIRES loading these skills FIRST:

1. **react-coding-conventions** - Base React patterns
2. **ui-components** - UI component patterns

## How to Use This Skill

### 1. Load Prerequisites and Reference

Before creating or modifying client components:

```
1. Read .claude/skills/react-coding-conventions/references/React-Coding-Conventions.md
2. Read .claude/skills/ui-components/references/UI-Components-Conventions.md
3. Read .claude/skills/client-components/references/Client-Components-Conventions.md
```

### 2. Apply Client Component Patterns

**'use client' Directive**:

- Must be the first line of the file
- Required when using hooks, event handlers, or browser APIs

**Hook Organization**:

- Follow the 7-step internal organization order
- Use useCallback for memoized event handlers
- Use useMemo for expensive calculations

**Event Handling**:

- Prefix handlers with `handle`: handleClick, handleSubmit
- Include e.preventDefault() and e.stopPropagation() where needed
- Support keyboard accessibility

**Server Action Consumption**:

- Use `useServerAction` hook from `@/hooks/use-server-action`
- Use `executeAsync` with `toastMessages` for mutations
- Access results via `data.data` in callbacks

### 3. Automatic Convention Enforcement

After generating code:

1. **Scan for violations** against client component patterns
2. **Fix automatically** without asking permission
3. **Verify completeness** before presenting to user

### 4. Reporting

Provide a brief summary of conventions applied:

```
Client component conventions enforced:
  - Added 'use client' directive
  - Organized hooks in correct order
  - Used useCallback for event handlers
  - Added keyboard accessibility handlers
  - Used useServerAction for server action
```

## File Patterns

This skill handles:

- `src/components/ui/**/*.tsx`
- `src/components/feature/**/*.tsx` (with 'use client')
- `src/app/**/components/*-client.tsx`
- Any .tsx with hooks or event handlers
- NOT page.tsx, layout.tsx, loading.tsx

## Workflow Summary

```
1. Detect client component work (hooks, events, 'use client')
2. Load prerequisites: react-coding-conventions, ui-components
3. Load references/Client-Components-Conventions.md
4. Generate/modify code following ALL conventions
5. Scan for violations
6. Auto-fix violations
7. Report fixes applied
```
