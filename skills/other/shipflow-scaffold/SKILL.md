---
name: shipflow-scaffold
description: Generate new files matching existing project patterns — pages, components, layouts, API routes, hooks, utils
disable-model-invocation: true
argument-hint: <type> <name> (e.g., "page about", "component UserCard")
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -80 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Package.json: !`cat package.json 2>/dev/null | head -40 || echo "no package.json"`
- Project structure: !`find . -maxdepth 3 -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.astro" -o -name "*.vue" -o -name "*.py" -o -name "*.sh" \) 2>/dev/null | grep -v node_modules | grep -v .git | grep -v dist | sort | head -40`

## Mode detection

Parse `$ARGUMENTS` for type and name:
- `page about` → type: page, name: about
- `component UserCard` → type: component, name: UserCard
- `api users` → type: api, name: users
- Empty → use AskUserQuestion

---

## Supported types

| Type | Description | Typical location |
|------|-------------|-----------------|
| `page` | Route/page file | `src/pages/`, `app/`, `pages/` |
| `component` | UI component | `src/components/`, `components/` |
| `layout` | Layout wrapper | `src/layouts/`, `app/layout` |
| `api` | API route/endpoint | `src/pages/api/`, `app/api/`, `convex/` |
| `content` | Content/blog post | `src/content/`, `content/` |
| `hook` | Custom hook | `src/hooks/`, `hooks/` |
| `util` | Utility function | `src/utils/`, `src/lib/`, `utils/` |

## Flow

### Step 1: Parse arguments

If `$ARGUMENTS` is empty, use **AskUserQuestion**:
- Q1: "What type of file should I scaffold?"
  - Options: page, component, layout, api, content, hook, util
- Q2: "What name?" (free text — user types via "Other")

### Step 2: Find existing examples

Find 2-3 existing files of the same type in the project:

```bash
# For pages:
find src/pages -maxdepth 2 -type f | head -3
# For components:
find src/components -maxdepth 2 -type f | head -3
# etc.
```

Read each example file completely.

### Step 3: Analyze patterns

From the examples, extract:
- **File extension**: `.astro`, `.tsx`, `.vue`, `.py`, etc.
- **Naming convention**: PascalCase, kebab-case, camelCase
- **Import style**: relative vs alias (`@/`), named vs default
- **Component structure**: function vs arrow, export style
- **Styling approach**: Tailwind classes, CSS modules, scoped styles
- **TypeScript patterns**: interface vs type, Props naming, generics
- **Frontmatter**: Astro frontmatter patterns, metadata
- **Framework patterns**: `getStaticPaths`, `loader`, `useQuery`, etc.

### Step 4: Generate new file

Create the new file matching EXACTLY the patterns found:
- Same file extension
- Same naming convention
- Same import style and structure
- Same export pattern
- Same styling approach
- Placeholder content that matches the pattern

### Step 5: Report

```
SCAFFOLDED: [type] — [name]
─────────────────────────────
File:     [created file path]
Based on: [example files used]
Patterns: [key patterns matched]
─────────────────────────────
```

---

## Important

- **Never invent patterns.** Always derive from existing files in the project.
- **Consistency > creativity.** The generated file should look like it was written by the same developer.
- If no examples of the requested type exist, tell the user and ask how to proceed.
- For Astro projects: detect whether to use `.astro`, `.tsx`, or `.vue` based on existing patterns.
- For content files: use the project's content schema (Content Collections, MDX frontmatter).
- Name the file following the project's existing naming convention (don't impose a different one).
- Place the file in the correct directory based on where existing files of that type live.
