---
name: setup-docs
description: Analyze the codebase and populate all .chalk/docs PROFILE stubs and chalk.json with real project content. Run once after chalk init.
author: chalk
version: "2.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write, Bash
argument-hint: "[optional: specific vertical to populate, e.g. 'engineering only']"
read-only: false
destructive: false
idempotent: true
open-world: true
user-invocable: true
tags: setup, docs, bootstrap
capabilities: chalk.docs.populate, chalk.docs.bootstrap
activation-intents: populate chalk docs, fill chalk docs, bootstrap profile docs
activation-events: user-prompt
activation-artifacts: .chalk/docs/**, AGENTS.md, README.md
risk-level: low
---

One-shot bootstrap that deeply analyzes the codebase and populates all `.chalk/docs/` PROFILE stubs with real, project-specific content. Also enriches `chalk.json` with any fields that `setup-chalk` couldn't auto-detect.

## When to Use

- After running `/setup-chalk` or `npx create-chalk` to generate stub docs
- When PROFILE docs contain `<!-- STUB -->` markers or placeholder content
- When `chalk.json` has missing fields (routes, sourceLayout, etc.)
- To refresh docs after significant codebase changes

## Workflow

### Step 1: Read existing state

1. **Read `chalk.json`** — Check which fields are populated vs missing. Note any that need enrichment (especially `routes`, `sourceLayout`, `dev`).
2. **Read each PROFILE doc** — Skip any that are already populated (no `<!-- STUB -->` comment and more than 20 lines of real content). Note which verticals need work.
3. **Read the codebase** — `package.json`, `README.md`, `src/` directory structure, config files, and any existing docs.

### Step 2: Enrich `chalk.json`

Fill any missing fields by deep analysis:

- **`routes`** — If empty, scan the codebase:
  - File-based routing: glob for `app/**/page.{tsx,jsx}` or `pages/**/*.{tsx,vue}`
  - React Router: grep for `<Route path=` or `createBrowserRouter`
  - Vue/Angular: grep router configs
  - Express/API: grep for `app.get(`, `router.`
  - For each route found, identify the source file/directory
- **`sourceLayout`** — If empty, scan for standard directories (src/, app/, lib/, components/, pages/, tests/)
- **`dev`** — If missing port/url, check vite.config, next.config, or framework defaults
- **`test`** — If missing, check for jest.config, vitest.config, pytest.ini, or test scripts in package.json

Write the updated `chalk.json` with any new fields.

### Step 3: Populate Product Profile (`.chalk/docs/product/PROFILE.md`)

Deep analysis to populate:
- **Summary**: product name, one-liner, primary users, core JTBD, value prop
- **Problem**: what pain this solves (infer from README, package.json description)
- **Target Users**: table (Persona, Job, How This Helps)
- **Core Jobs To Be Done**: numbered list (infer from features, routes, UI patterns)
- **Current Status**: table of features (Feature, Status, Notes)
- **What It Is / What It Is Not**: clarify scope

### Step 4: Populate Engineering Profile (`.chalk/docs/engineering/PROFILE.md`)

Deep analysis to populate:
- **Architecture**: process model diagram, execution contexts table, boot sequence
- **Directory Structure**: annotated tree with purpose per directory
- **Data Flow**: state management, API/IPC boundaries, storage layer
- **Tech Stack**: full dependency tables (runtime + dev/build), grouped by category
- **Key Patterns**: design patterns, error handling, testing approach

This is a single comprehensive doc — do NOT create separate architecture or techstack files.

### Step 5: Populate Coding Style (`.chalk/docs/engineering/coding-style.md`)

Analyze 5+ representative files across different layers to document:
- File/folder naming conventions with real examples
- Component/module structure with a full code example from the codebase
- Naming conventions (variables, functions, types, files)
- Import ordering with a real example
- Export patterns
- TypeScript/language-specific patterns
- Styling approach
- Error handling patterns

### Step 6: Populate AI Profile (`.chalk/docs/ai/PROFILE.md`)

Create the agent orientation doc:
- **Project Identity**: 1 paragraph summary
- **Where Things Live**: table (What, Where, Notes) — map every major concern to its file/directory
- **Conventions to Follow**: top 5-10 rules for writing code in this project
- **Gotchas**: numbered list of things that will surprise an agent
- **How to Add a Feature**: step-by-step guide based on codebase patterns

### Step 7: Populate Design Profile (`.chalk/docs/design/PROFILE.md`)

Extract visual language:
- **Color Palette**: scan CSS files, Tailwind config, and components for hex codes and Tailwind classes. Organize into Primary, Neutral, and Semantic tables.
- **Typography**: font families, size scale, weight scale from CSS/config
- **Spacing**: recurring padding/margin values
- **Borders & Shadows**: border widths, radius, shadow definitions
- **Icons**: icon library and common icons used
- **Component Patterns**: common UI patterns (buttons, cards, panels)

### Step 8: Update AGENTS.md

If `AGENTS.md` exists, enrich with project-specific pointers to the populated docs and critical conventions. If it doesn't exist, create a minimal one pointing to `.chalk/docs/`.

### Step 9: Confirm

List what was populated, what was skipped, and any remaining gaps. Suggest next steps (e.g., "Design profile has placeholder content — run `/update-doc design/PROFILE.md` to refine").

## Rules

- **Write substantive content, not stubs** — Every section should have real information from the codebase analysis.
- **Remove `<!-- STUB -->` markers** — When populating a doc, remove the stub comment.
- **Preserve existing content** — If a doc already has real content in some sections, enhance rather than overwrite.
- **Use the vertical's tone** — Product docs are business-facing. Engineering docs are technical. AI docs are agent-facing reference.
- **Include the "Last updated" line** — Format: `Last updated: YYYY-MM-DD (populated from codebase analysis)`.
- **chalk.json is authoritative** — If chalk.json disagrees with a PROFILE doc, chalk.json wins. Update the doc to match.
- **Real examples over abstractions** — Always use actual code, file paths, and values from the codebase.

## Differences from related skills

- `/setup-chalk` creates the `.chalk/` scaffold with stubs — run it first
- `/setup-docs` populates those stubs with real content — run it second
- `/create-doc` creates a single new doc for a specific topic on demand
- `/update-doc` updates an existing doc with new information
- `/validate-chalk` checks if chalk.json and docs are complete and correct
