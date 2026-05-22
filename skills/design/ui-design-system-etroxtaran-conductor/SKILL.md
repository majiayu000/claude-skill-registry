---
name: ui-design-system
description: Authoritative UI/UX Design System Guide based on EtroxTaran/Uiplatformguide
version: 1.1.0
tags: [ui, design-system, components]
owner: design
status: active
---

# UI Design System Skill

## Overview

Use the local reference design system as the source of truth for UI components and patterns.

## Usage

```
/ui-design-system
```

This skill is the **authoritative UI guidance** for the Conductor project. It is backed by a **local reference repository** that must be present and up to date:
`.claude/skills/ui-design-system/reference`

Primary sources:
- Repo (source of truth): `https://github.com/EtroxTaran/Uiplatformguide`
- Deployed guide (visual reference only): `https://booth-fit-99271772.figma.site/`

The local `reference/` folder contains a full clone of the design system repo and is **the canonical source** for tokens, component APIs, and patterns.

## 0. Policy (Non‑Negotiable)

- **All UI work must use this skill first.**
- **No UI change without checking the reference.**
- **If the reference is missing or outdated, stop and sync it.**
- **If a component/pattern doesn’t exist in the reference, request guidance before inventing.**

## 0.5 Quick Checklist (Use Every Time)

- [ ] Reference repo exists at `.claude/skills/ui-design-system/reference`
- [ ] Reference repo is up to date (`git fetch` + `merge --ff-only`)
- [ ] Component/pattern located in reference files
- [ ] Tokens taken from `reference/src/styles/globals.css`
- [ ] shadcn / Shadcraft component installed via CLI (if needed)
- [ ] Data tables follow `reference/src/components/shared/DataTable.tsx`

## 1. Core Principles

- **Source of Truth**: The local `reference/` code is the final authority for design tokens, components, and patterns.
- **No Guessing**: Do not invent UI. Always check the reference.
- **Primitives First**: Prefer primitives in `reference/src/components/ui/` before building composites.
- **Patterns Second**: For layouts and flows, use patterns in `reference/src/components/layout/` and `reference/src/components/design-system/`.
- **Visual Parity**: The deployed guide is for visual comparison only; implementation must follow the repo.

## 2. Reference Coverage Map (What to Use)

### 🎨 Design Tokens & Theming
**File**: `reference/src/styles/globals.css`
- CSS variables (light/dark mode), typography, spacing, elevation, animation tokens.
- Always use these variables for theming and custom styling.

### 🧩 UI Primitives (Radix + shadcn)
**Directory**: `reference/src/components/ui/*.tsx`
- Button, Input, Select, Dialog, Sheet, Tooltip, Tabs, Table, etc.
- Use the exact props/variants/classes from these files.

### 🧰 Shared UI Patterns
**Directory**: `reference/src/components/shared/`
- `LoadingState.tsx` (spinners, skeletons)
- `AccessibleTooltip.tsx` (responsive tooltips)
- `ResponsiveModal.tsx`, `DestructiveDialog.tsx`, `DataTable.tsx`

### 🧭 Layout & Navigation
**Directory**: `reference/src/components/layout/`
- `AppShell.tsx`, `GlobalTopNav.tsx`, `AppSwitcher.tsx`, `FinanceSideNav.tsx`

### 📚 Design System Guidance
**Directory**: `reference/src/components/design-system/`
- Foundation tokens, component templates, form patterns, overlays, dashboard patterns.

### 📄 Example Screens / Flows
**Directory**: `reference/src/components/`
- `DashboardLayout.tsx`, `SettingsPage.tsx`, `LoginPage.tsx`, `OverviewDashboard.tsx`

### 🔧 Utilities & Hooks
**Files**:
- `reference/src/components/ui/utils.ts` (class helpers)
- `reference/src/hooks/use-media-query.ts`, `use-view-preference.ts`

## 3. Shadcn + Shadcraft Usage (Required)

We use **shadcn/ui** and **Shadcraft** for components and blocks. Follow the official CLI workflow for installation and registry usage.

**Initialize shadcn:**
```bash
npx shadcn@latest init
```

**Install components or blocks:**
```bash
npx shadcn@latest add <component-name>
npx shadcn@latest add @shadcraft/<item-name>
```

For registry configuration, environment keys, and CLI usage details, follow:
`https://shadcraft.com/docs/installation-via-shadcn-cli`

## 4. Radix + shadcn Best Practices (Must Follow)

- Use Radix primitives through shadcn wrappers in `reference/src/components/ui/`.
- Keep accessibility attributes and ARIA props as implemented in the reference.
- Prefer composition over overrides; avoid custom wrappers unless a reference pattern exists.
- Keep motion/transition tokens aligned with `globals.css`.

## 5. TanStack Data Grid Guidance (Required)

When using data tables, follow the reference implementation:
- `reference/src/components/shared/DataTable.tsx`

Use the exact table structure, column definitions, and UI wrappers found there. Only extend behavior if the reference shows a pattern for it.

## 6. Reference Sync (Mandatory)

The local reference **must exist and be current** before implementing UI.

```bash
git -C .claude/skills/ui-design-system/reference fetch --all --prune
git -C .claude/skills/ui-design-system/reference checkout <default-branch>
git -C .claude/skills/ui-design-system/reference merge --ff-only FETCH_HEAD
```

If the repo is private, use SSH:
```bash
git -C .claude/skills/ui-design-system/reference remote set-url origin git@github.com:EtroxTaran/Uiplatformguide.git
```

## 7. Usage Instructions for Agent

When the user asks for UI work:
1. **Locate** the closest matching primitive or pattern in the reference.
2. **Read** the exact reference file(s).
3. **Implement** by mirroring props, structure, and tokens.
4. **Validate** any custom styling against `globals.css` tokens.
5. **Document** the source file(s) you used in your response.

If a requested UI element is not found in the reference:
- Stop and ask for guidance (or extend only after user approval).
```

## Outputs

- UI changes that match the reference design system tokens and component APIs.

## Related Skills

- `/frontend-dev-guidelines` - React/TypeScript UI standards
