---
name: setup-chalk
description: Initialize .chalk folder — analyze a repo and capture its architecture, coding style, tech stack, design assets, and project identity into chalk.json and structured docs
author: chalk
version: "2.0.0"
metadata-version: "3"
allowed-tools: Read, Write, Glob, Grep, Bash
argument-hint: "[optional: path to repo root, defaults to current project]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: setup, chalk, bootstrap
capabilities: chalk.setup, chalk.docs.bootstrap
activation-intents: set up chalk, initialize chalk, bootstrap chalk
activation-events: user-prompt, session-start
activation-artifacts: .chalk/**, README.md, AGENTS.md
risk-level: medium
---

Initialize a `.chalk/` folder for any repository. Produces a machine-readable `chalk.json` (the single source of truth for skills) and human-readable PROFILE docs covering product, engineering, design, and AI orientation.

## What This Skill Produces

```
.chalk/
  chalk.json                          # Machine-readable project identity (skills read this first)
  docs/
    product/
      PROFILE.md                      # What the product is, who it's for, core JTBD
    engineering/
      PROFILE.md                      # Architecture + tech stack + data flow (single source)
      coding-style.md                 # Naming, file structure, component patterns, conventions
    ai/
      PROFILE.md                      # Agent-facing orientation, gotchas, quick reference
    design/
      PROFILE.md                      # Design system: colors, typography, spacing, tokens
      assets/                         # Copied logos, icons, favicons, brand marks
```

## Workflow

### Phase 1 — Discover

1. **Locate the repo root** — Use `$ARGUMENTS` if provided, otherwise use the current working directory.
2. **Check for existing `.chalk/`** — If it already exists, warn the user and ask whether to merge or overwrite. If merging, skip files that already exist and only fill gaps.
3. **Scan the repo** — Read these files to understand the project:
   - `README.md` (or `readme.md`)
   - `package.json` / `Cargo.toml` / `pyproject.toml` / `go.mod` / `Gemfile` / `pom.xml` (dependency manifest)
   - `tsconfig.json` / `tsconfig.*.json`
   - Build configs: `vite.config.*`, `next.config.*`, `webpack.config.*`, `electron.vite.config.*`, `turbo.json`, `angular.json`
   - Styling: `tailwind.config.*`, `postcss.config.*`, any `*.css` files in `src/`
   - `.eslintrc*`, `.prettierrc*`, `biome.json` (linter/formatter config)
   - `Dockerfile`, `docker-compose.yml`
   - `.github/workflows/*.yml` (CI/CD)
   - Existing `AGENTS.md`, `.cursorrules`, or `CLAUDE.md`

### Phase 2 — Analyze

4. **Detect framework and project type** — Identify from dependencies:

   | Dependency | Framework | Type | Default Port |
   |-----------|-----------|------|-------------|
   | `next` | Next.js | web | 3000 |
   | `vite` + `@vitejs/plugin-react` | Vite + React | web | 5173 |
   | `react-scripts` | CRA | web | 3000 |
   | `nuxt` | Nuxt | web | 3000 |
   | `@angular/core` | Angular | web | 4200 |
   | `svelte` / `@sveltejs/kit` | SvelteKit | web | 5173 |
   | `electron` / `electron-vite` | Electron | desktop | varies |
   | `vue` | Vue | web | 5173 |
   | `express` / `fastify` / `koa` | Node API | api | 3000 |
   | `django` / `flask` / `fastapi` | Python web | web/api | 8000 |

5. **Detect routes** — Scan based on detected framework:
   - **File-based routing** (Next.js, Nuxt, SvelteKit): glob `app/**/page.{tsx,jsx,ts,js}` or `pages/**/*.{tsx,jsx,vue}`
   - **React Router**: grep for `<Route`, `createBrowserRouter`, or `path:` in `src/`
   - **Vue Router**: grep for `path:` in router config files
   - **Angular**: grep for `{ path:` in routing modules
   - **Query-param routing** (Electron): grep for `searchParams.get` or `?page=`
   - **Express/API**: grep for `app.get(`, `router.get(`, `@app.route`
   - **Fallback**: scan for page components in `src/pages/`, `src/views/`, `src/app/`, `src/routes/`

6. **Map source layout** — Identify key directories:
   - Source root (`src/`, `app/`, `lib/`)
   - Entry points (main files, renderers, workers)
   - Components, pages/views, styles, and tests directories

7. **Map the architecture** — Identify:
   - Process model (monolith, Electron multi-process, SPA, SSR, etc.)
   - Directory structure patterns (feature folders, atomic design, domain-driven)
   - Entry points and boot sequence
   - Data flow (state management, IPC, API calls, database)
   - Key abstractions (hooks, services, stores, controllers)

8. **Extract coding style** — Analyze 3-5 representative files from different layers:
   - Naming conventions, export patterns, component patterns
   - State management, error handling, comment style
   - Import ordering, TypeScript strictness

9. **Catalog the tech stack** — For every dependency: name, version, layer, purpose, category.

10. **Extract design tokens** — CSS custom properties, Tailwind theme extensions, recurring color/typography/spacing values.

11. **Find brand assets** — Glob for icons, logos, favicons under resources/, public/, assets/.

### Phase 3 — Generate

12. **Create `.chalk/chalk.json`** — The machine-readable project identity. This is the most important file — skills read it first.

```json
{
  "version": "1.0",
  "project": {
    "name": "<from package.json or directory name>",
    "description": "<from package.json description or README>",
    "language": "<typescript|javascript|python|go|rust|java>",
    "framework": "<next|vite|electron|django|express|etc>",
    "type": "<web|desktop|api|library|cli|monorepo>"
  },
  "dev": {
    "command": "<npm run dev|yarn dev|make dev|etc>",
    "port": 3000,
    "url": "http://localhost:3000"
  },
  "test": {
    "command": "<npm test|pytest|go test ./...>",
    "framework": "<jest|vitest|pytest|node:test>"
  },
  "build": {
    "command": "<npm run build>",
    "output": "dist/"
  },
  "routes": [
    { "path": "/", "name": "Home", "src": "src/pages/index.tsx" }
  ],
  "sourceLayout": {
    "root": "src/",
    "entrypoints": { "main": "src/main.tsx" },
    "components": "src/components/",
    "pages": "src/pages/",
    "styles": "src/styles/",
    "tests": "tests/"
  },
  "createdAt": "<ISO timestamp>",
  "updatedAt": "<ISO timestamp>"
}
```

**Schema reference**: `docs/chalk.schema.json` in the chalk-skills repo defines all valid fields.

**Important**: Fill every field you can detect. Omit fields you can't determine — don't guess. Skills handle missing fields gracefully.

13. **Create `.chalk/docs/product/PROFILE.md`**

Summarize:
- Product name, one-liner, primary users, core value prop
- Problem: what pain this solves
- Target Users: table (Persona, Job, How This Helps)
- Core Jobs To Be Done: numbered list, each starts with a verb
- Current Status: feature table (Feature, Status, Notes)

14. **Create `.chalk/docs/engineering/PROFILE.md`** — Single comprehensive engineering doc covering architecture + tech stack + data flow:

Include:
- Architecture diagram (ASCII or Mermaid)
- Execution contexts table (entry point, lifecycle, access)
- Boot sequence (numbered steps)
- Directory structure (annotated tree with purpose per directory)
- Data flow (state management, API/IPC boundaries, storage)
- Tech stack table (Package, Version, Category, Purpose) grouped by runtime vs dev/build
- Key patterns (design patterns, error handling, testing approach)

15. **Create `.chalk/docs/engineering/coding-style.md`**

Include:
- File & folder naming conventions with examples
- Component/module structure with real code example from the codebase
- Naming conventions (variables, functions, types, files)
- Import ordering with real example
- Export patterns (default vs named)
- TypeScript patterns (strict mode, type vs interface)
- Styling patterns (Tailwind, CSS approach)
- Error handling patterns

16. **Create `.chalk/docs/ai/PROFILE.md`** — Agent-facing quick reference:

Include:
- Project Identity: 1 paragraph
- Where Things Live: table (What, Where, Notes)
- Conventions to Follow: top 5-10 rules
- Gotchas: numbered list of agent-surprising things
- How to Add a Feature: step-by-step guide

17. **Create `.chalk/docs/design/PROFILE.md`**

Include:
- Brand identity (name, visual tone)
- Color palette: Primary, Neutral, Semantic tables (Name, Hex, Tailwind, Usage)
- Typography (font families, size/weight scales)
- Spacing & layout (common values, breakpoints)
- Borders & shadows
- Icons (library, usage patterns)
- Component patterns (buttons, cards, common UI)

18. **Copy brand assets** to `.chalk/docs/design/assets/` (files < 500KB, prefer SVG).

### Phase 4 — Verify

19. **Validate `chalk.json`** — Check that required fields are present and values make sense. Print warnings for missing optional fields.
20. **List created files** — Print a tree of everything created under `.chalk/`.
21. **Summarize** — Tell the user what was captured, what has gaps, and suggest running `/setup-docs` to enrich stubs with deeper analysis.

## Doc Format Rules

- No YAML frontmatter in docs (plain markdown)
- First `# Heading` is the document title
- `Last updated: YYYY-MM-DD (<brief note>)` immediately after the title
- Use `## Heading` for sections
- GFM features: tables, code blocks, checkboxes, Mermaid diagrams
- Use real code examples from the repo, not generic placeholders
- Be specific and concrete — hex codes not "brand green", actual file paths not "components folder"

## Migration from v1

If the project has the old docs structure (numbered files like `0_PRODUCT_PROFILE.md`, `1_architecture.md`, `3_techstack.md`):

1. Merge `0_ENGINEERING_PROFILE.md` + `1_architecture.md` + `3_techstack.md` → `engineering/PROFILE.md`
2. Rename `0_PRODUCT_PROFILE.md` → `product/PROFILE.md`
3. Rename `0_AI_PROFILE.md` → `ai/PROFILE.md`
4. Rename `0_design-system.md` → `design/PROFILE.md`
5. Rename `2_coding-style.md` → `engineering/coding-style.md`
6. Keep any extra docs as additional files in their vertical
7. Expand `chalk.json` with new fields (project, dev, test, build, routes, sourceLayout)
8. Delete old numbered files after confirming the merge

Ask the user before performing migration.

## Style Transfer Focus

The goal is **fidelity**. An AI agent reading these docs should be able to:

1. Write new code that looks like it belongs in the codebase (coding style)
2. Place files in the right directories following the right patterns (architecture)
3. Use the correct libraries and APIs (tech stack)
4. Match the visual design exactly — right colors, right spacing, right typography (design system)
5. Use the brand assets correctly (design assets)

Prioritize **concrete examples over abstract rules**.
