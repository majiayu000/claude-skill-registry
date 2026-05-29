---
name: help-system-architect
description: >
  Design and generate the in-app help system: havainnepolku (visual guidance path) components,
  help mode (apua-tila), contextual help content, and searchable help index.
  Use when (1) creating or updating help pages, (2) building the havainnepolku breadcrumb-path
  component, (3) implementing help mode overlay, (4) generating help search index,
  (5) adding contextual tips to pages, (6) brainstorming which guidance paths to create.
  Triggers: "help system", "apua", "havainnepolku", "guidance path", "help mode",
  "apua-tila", "contextual help", "help content", "help search", "user guidance",
  "breadcrumb path", "ohje", "opaste".
---

# Help System Architect

Design and generate the in-app help system for Raamattu Nyt.

## Authority

- Consumes `Docs/ai/core-user-model.json` as the **single source of truth** for tasks and paths
- NEVER redefines tasks or paths — only explains, guides, and contextualizes them
- The `core-ux-detective` skill owns task/path definitions; this skill owns help presentation

## Architecture

### Havainnepolku (Visual Guidance Path)

A horizontal strip at the top of the page showing the full user journey as linked blocks:

```
┌──────────┐   ┌────────────────┐   ┌───────────┐   ┌────────────────┐   ┌─────────────┐
│ MUISTIO  │ → │ VALITSE JAKEET │ → │ LUO REELS │ → │ EDITOI REELSIÄ │ → │ JULKAISE    │
│          │   │                │   │           │   │  ◄ olet tässä  │   │             │
│          │   │                │   │           │   │  Muokkaa tyyliä │   │             │
└──────────┘   └────────────────┘   └────────────┘   └────────────────┘   └─────────────┘
```

Each block:
- Is a clickable link to the page where that step happens
- Shows the step label (Finnish, from `core_tasks[].label`)
- When the user is on that step's page: highlighted + short contextual tip below

### Shared Package: `packages/help-guide/`

Havainnepolku and help mode as a shared monorepo package:

```
packages/help-guide/
  package.json          # @raamattu-nyt/help-guide
  tsconfig.json
  src/
    index.ts
    types.ts            # HelpPath, HelpStep, HelpContent, HelpSearchEntry
    GuidancePath.tsx    # Havainnepolku component
    HelpModeProvider.tsx # Context provider for help mode state
    useHelpMode.ts      # Hook: isHelpMode, toggleHelp, currentPath
    HelpTooltip.tsx     # Contextual tip bubble (non-blocking, dismissible)
    HelpSearchIndex.ts  # Search index builder from core-user-model
```

### Help Mode (Apua-tila)

Toggle-based overlay that reveals:
1. Havainnepolku bar at page top
2. Contextual tooltips on interactive elements
3. Non-blocking, dismissible — never prevents user from working
4. Persists in session storage (survives page navigation, clears on tab close)

### Help Search ("?")

Maps search queries to `core_tasks` and `user_paths`:
- Finnish keyword index built from task labels, path labels, and help content
- Never invents new terminology — only uses canonical labels from `core-user-model.json`

## Workflow

### 1. Read the User Model

```
Read Docs/ai/core-user-model.json
```

If file doesn't exist, inform the user to run `core-ux-detective` first.

### 2. Choose What to Generate

Determine scope from user request:
- **Full system**: All components + content + search index
- **Havainnepolku only**: Just the GuidancePath component + path data
- **Help content**: Help pages for specific tasks/paths
- **Search index**: Keyword-to-task/path mapping

### 3. Brainstorm Paths (Optional)

When the user needs help deciding which guidance paths to create:
- Invoke the `brainstorming` skill
- Provide it with the `user_paths` from `core-user-model.json`
- Focus questions on: which paths are most confusing, which need step-by-step guidance

### 4. Generate Components

See [references/component-specs.md](references/component-specs.md) for detailed component specifications.

### 5. Generate Help Content

For each task/path, generate help content in Finnish:

```json
{
  "task_id": "create_reel",
  "title": "Reelsin luominen",
  "what": "Luo kaunis kuvajae Raamatun jakeesta.",
  "when": "Kun haluat jakaa jakeen someen kuvana.",
  "steps": [
    "Valitse jae Raamatusta",
    "Paina 'Luo reels' -painiketta",
    "Valitse malli ja tyyli",
    "Esikatsele ja julkaise"
  ]
}
```

Rules:
- Finnish language, calm and supportive tone
- Non-technical — describe what the user sees, not implementation details
- Short sentences, max 15 words per step
- Reference canonical `core_tasks[].label` for consistency

### 6. Generate Search Index

Map Finnish keywords to task/path IDs:

```json
{
  "entries": [
    { "keywords": ["reels", "kuva", "jae", "julkaise"], "type": "path", "id": "create_and_share_reel" },
    { "keywords": ["haku", "etsi", "jae"], "type": "task", "id": "search_verses" }
  ]
}
```

Never add keywords that don't appear in the canonical model or help content.

### 7. Output Files

| File | Purpose |
|------|---------|
| `packages/help-guide/src/*.tsx` | Shared components |
| `apps/.../data/help-content.json` | Help content for all tasks/paths |
| `apps/.../data/help-search-index.json` | Search keyword index |
| `apps/.../components/help/HelpModeToggle.tsx` | App-level help button |
| `apps/.../components/help/HelpPage.tsx` | Full help page (optional) |

## Rules

- All user-facing text in Finnish
- Calm, supportive, non-technical tone
- Never redefine tasks or paths from `core-user-model.json`
- Havainnepolku steps must exactly match canonical path steps
- Help mode is non-blocking — user can always dismiss
- Search only uses canonical terminology
- Components go in `packages/help-guide/`, app wiring in `apps/raamattu-nyt/`
