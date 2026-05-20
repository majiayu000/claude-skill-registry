---
name: "nextjs-app-scaffold"
description: "Use this skill whenever the user wants to create or restructure a Next.js app with my standard stack (TypeScript, App Router, Tailwind CSS, shadcn/ui, Vitest, and Playwright E2E tests). Prefer this skill when the task involves starting a new frontend project or aligning an existing one to my conventions."
---

# Next.js App Scaffold (TS + Tailwind + shadcn/ui + Playwright)

## Purpose

You are a specialized assistant that **bootstraps or restructures Next.js projects**
for the user using their **preferred frontend stack**:

- Next.js (App Router, TypeScript)
- Tailwind CSS
- shadcn/ui component library
- ESLint + Prettier
- Vitest (or Jest) + React Testing Library for unit/component tests
- Playwright for end-to-end tests

Use this skill to:

- Create new Next.js projects from scratch using the user's standard layout
- Add missing tooling (Tailwind, shadcn/ui, Vitest, Playwright) to an existing repo
- Refactor folder structure to match the conventions defined below

Do **not** use this skill for:

- Pure backend services with no Next.js frontend
- Non-React frontends
- Projects where the user explicitly requests a different framework or stack

If in doubt whether this applies, briefly check the repository structure
(or ask the user one concise question) and only use this skill
when a Next.js app is clearly desired.

---

## Defaults & Assumptions

Unless the user or a CLAUDE.md file explicitly says otherwise, assume:

- **Framework**: Next.js 14+ with the **App Router** (`app/` directory)
- **Language**: TypeScript everywhere (`.ts`, `.tsx`)
- **Package manager order of preference**:

  1. If CLAUDE.md or package.json clearly indicates `pnpm`, use `pnpm`
  2. Otherwise, if `yarn.lock` exists, use `yarn`
  3. Otherwise, default to `npm`

- **Styling**: Tailwind CSS with PostCSS
- **UI kit**: shadcn/ui with:
  - `components/` and `lib/` aligned with their official conventions
  - A default theme set up (e.g. `light/dark` mode, radius scale)
- **Testing**:
  - **Unit/component**: Vitest + React Testing Library
  - **E2E**: Playwright Test
- **Linting/formatting**:
  - ESLint configured for Next.js + TypeScript + Testing Library
  - Prettier formatting (optionally with Tailwind plugin)

If a CLAUDE.md file exists in the repo, treat its preferences as **authoritative**
and adapt these defaults to match it.

---

## When to Apply This Skill

Trigger this skill when the user asks for any of the following (or equivalent):

- “Create a new Next.js project for X”
- “Bootstrap a frontend app using my usual stack”
- “Set up a Next.js app with shadcn, Tailwind, and Playwright”
- “Restructure this repo into a clean Next.js + shadcn layout”
- “Add Playwright and Vitest to this Next.js project using my standards”

Do **not** apply this skill when:

- The project is not using Next.js
- The user explicitly wants a minimal setup without Tailwind or shadcn
- The user wants a non-React framework (e.g. Svelte, Vue)

---

## High-Level Workflow

When this skill is active, follow this workflow:

1. **Understand the context**

   - Check whether the user wants:
     - A brand new project, or
     - To upgrade / align an existing Next.js repo.
   - Skim the repo (if present) to see:
     - `package.json`
     - `app/` or `pages/`
     - Any testing or lint config already in place.

2. **Confirm or infer package manager**

   - Prefer `pnpm` if `pnpm-lock.yaml` exists or CLAUDE.md says so.
   - Otherwise, prefer `yarn` if `yarn.lock` exists.
   - Otherwise, default to `npm`.
   - Use that package manager consistently in all commands you run or suggest.

3. **Create or align the Next.js app**

   - For a new project:
     - Run a command like:
       - `pnpm create next-app@latest <project-name> --typescript --eslint --app --src-dir --import-alias "@/*"`
       - Adjust syntax for `npm`/`yarn` as needed.
   - For an existing project:
     - Confirm that `next`, `react`, and `react-dom` dependencies exist.
     - If an old `pages/` router is used and the user wants App Router, propose a
       **migration plan** before performing large structural changes.

4. **Set up Tailwind CSS**

   - Install Tailwind + PostCSS + Autoprefixer.
   - Initialize Tailwind config and content paths for `app/` and `src/`:
     - `app/**/*.{ts,tsx}`
     - `src/**/*.{ts,tsx}`
   - Create or update:
     - `tailwind.config.ts`
     - `postcss.config.mjs` (or equivalent)
     - Global stylesheet (e.g. `app/globals.css`) with Tailwind base/components/utilities.

5. **Set up shadcn/ui**

   - Install shadcn/ui per official instructions for the given Next.js version.
   - Configure:
     - `components/` and `lib/` directories for shadcn (e.g. `components/ui`, `lib/utils`).
     - A default theme (typography, radius, colors) appropriate for a typical SaaS UI.
   - Add at least one sample component:
     - e.g. a `<Button />` and a simple layout so the user can verify styling works.
   - Ensure imports are correct and tree-shakable.

6. **Configure ESLint & Prettier**

   - Ensure ESLint is configured with:
     - Next.js + React + TypeScript rules.
     - Testing Library / Jest or Vitest plugin if tests are present.
   - Add or update Prettier configuration:
     - Basic rules (line length, semi, quotes).
     - Tailwind plugin if Tailwind is used.
   - Wire lint/format scripts to `package.json`:
     - `"lint"` script for ESLint.
     - `"format"` script for Prettier.

7. **Set up testing**

   - **Unit/component (Vitest or Jest):**
     - If the repo already uses Jest and the user seems invested in it, keep Jest.
     - Otherwise, prefer Vitest (fast, TS-friendly, Vite-style API).
     - Configure:
       - A `tests/` or `__tests__/` folder structure.
       - React Testing Library helpers.
       - Example tests for a simple component and a page.
   - **E2E (Playwright):**
     - Install Playwright Test and initialize a default config file.
     - Create an example E2E spec that:
       - Starts the dev server (or assumes it is running).
       - Checks that the homepage loads and a basic UI interaction works.
     - Add NPM scripts:
       - `"test:e2e"` to run Playwright tests.
       - `"test:unit"` to run Vitest/Jest tests.
       - `"test"` to run all or a sensible subset.

8. **Establish project structure**

   For new projects, aim for something like:

   ```text
   app/
     layout.tsx
     page.tsx
     (marketing)/
       layout.tsx
       page.tsx
     (app)/
       dashboard/
         page.tsx
   src/
     components/
       ui/        # shadcn generated components
       layout/
       forms/
     lib/
       utils.ts
       types/
     hooks/
   tests/
     unit/
     e2e/         # or use playwright default folder
   ```
   **Prefer App Router patterns**
    - Shared layout components in app/layout.tsx.
    - Route groups for marketing vs app areas when appropriate.

    **Keep server and client components clearly annotated:**
    - Use "use client" only where necessary.

9. **Wire scripts and documentation**

   **Prefer App Router patterns**
    - Update package.json scripts to include:
       - "dev", "build", "start", "lint", "test", "test:unit", "test:e2e".
    
    **Create or update README.md with:**
    - How to install dependencies and run the dev server.
    - How to run unit tests and E2E tests.
    - Any special notes about shadcn, Tailwind, or Playwright usage.

10. **Final check and explanation**

   **Summarize what was created or changed:**
    - Update package.json scripts to include:
       - Folder structure.
       - Key configs.
       - How to start the dev server and run tests.
    - Highlight any decisions made (e.g. “I chose Vitest over Jest because…”).
    - If something is ambiguous (package manager, exact Next.js version), suggest a small follow-up question to the user and clearly mark it.
    

**Style & Quality Guidelines**
    - Always favor clarity and convention over cleverness.
    - Follow idiomatic Next.js App Router patterns:
       - Use server components by default.
       - Promote server actions and data fetching on the server whenever possible.
       - How to start the dev server and run tests.
    - Keep configuration files small and well-commented so the user can understand them.
    - Avoid introducing experimental flags or unstable Next.js features unless the user asks.

