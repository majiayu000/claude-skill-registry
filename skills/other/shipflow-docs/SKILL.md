---
name: shipflow-docs
description: Generate or update documentation from code — README, API docs, component docs, or single file documentation
disable-model-invocation: true
argument-hint: [file-path | "readme" | "api" | "components"]
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -80 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Package.json: !`cat package.json 2>/dev/null | head -40 || echo "no package.json"`
- Existing README: !`head -20 README.md 2>/dev/null || echo "no README.md"`
- Project structure: !`find . -maxdepth 3 -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.astro" -o -name "*.vue" -o -name "*.py" \) 2>/dev/null | grep -v node_modules | grep -v .git | grep -v dist | sort | head -40`

## Mode detection

- **`$ARGUMENTS` is a file path** → FILE MODE: document that specific file.
- **`$ARGUMENTS` is "readme"** → README MODE: generate or update README.md.
- **`$ARGUMENTS` is "api"** → API MODE: document all API endpoints.
- **`$ARGUMENTS` is "components"** → COMPONENTS MODE: document all UI components.
- **`$ARGUMENTS` is empty** → AUTO MODE: detect gaps and suggest what to document.

---

## FILE MODE

Document a specific file with inline documentation.

### Flow

1. Read the target file and all its imports (1 level deep).
2. Analyze: exports, functions, types, classes, side effects.
3. Add documentation:
   - **TypeScript/JavaScript**: JSDoc/TSDoc comments for exports
   - **Python**: docstrings (Google style)
   - **Astro/Vue**: component description comment at top
4. Don't document obvious code. Focus on:
   - Why, not what
   - Non-obvious parameters and return values
   - Edge cases and gotchas
   - Usage examples for public APIs

---

## README MODE

Generate or update `README.md` for the project.

### Flow

1. Analyze the project: package.json, CLAUDE.md, directory structure, framework, features.
2. Generate sections:

```markdown
# [Project Name]

[One-line description]

## Features
- [Auto-detected from code and package.json]

## Quick Start
[Install + run commands from package.json scripts]

## Project Structure
[Key directories and their purpose]

## Tech Stack
[Framework, UI, backend, auth — auto-detected]

## Environment Variables
[From .env.example or CLAUDE.md]

## Scripts
[All package.json scripts with descriptions]

## Contributing
[Standard section]
```

3. If README.md exists, use **AskUserQuestion**:
   - Question: "README.md already exists. How should I update it?"
   - Options:
     - **Merge** — "Add missing sections, keep existing content" (Recommended)
     - **Replace** — "Overwrite with fresh generation"
     - **Skip** — "Don't modify README.md"

---

## API MODE

Document all API routes/endpoints.

### Flow

1. Find all API route files:
   - Next.js: `app/api/**/route.ts`, `pages/api/**/*.ts`
   - Astro: `src/pages/api/**/*.ts`
   - Convex: `convex/*.ts` (queries, mutations, actions)
   - Python: FastAPI routes, Flask routes
2. For each endpoint, document:
   - **Method**: GET, POST, PUT, DELETE
   - **Path**: full URL path
   - **Auth**: required? what type?
   - **Request body**: schema/type
   - **Response**: schema/type + status codes
   - **Example**: curl or fetch example
3. Output to `docs/API.md` or inline in the route files (ask user preference).

---

## COMPONENTS MODE

Document all UI components.

### Flow

1. Find all component files in the project.
2. For each component, document:
   - **Name**: component name
   - **Description**: what it does (from code analysis)
   - **Props/Slots**: all accepted props with types and defaults
   - **Usage example**: how to use the component
   - **Dependencies**: what it imports/requires
3. Output to `docs/COMPONENTS.md` or as a component index.

---

## AUTO MODE

Detect documentation gaps and suggest what to document.

### Flow

1. Check for:
   - Missing README.md
   - Undocumented exports (no JSDoc/docstring)
   - API routes without documentation
   - Components without prop documentation
   - Missing .env.example
   - Missing CHANGELOG.md
2. Use **AskUserQuestion**:
   - Question: "I found these documentation gaps. What should I document?"
   - `multiSelect: true`
   - Options based on detected gaps

---

## Important

- **Read actual code** — never invent functionality that doesn't exist.
- **Match existing doc style** — if the project uses a specific documentation format, follow it.
- **French for French projects** — GoCharbon, claiire, plaisirsurprise (FR content).
- Every code example must be **syntactically correct** and **runnable**.
- Don't over-document. Simple, self-explanatory code doesn't need comments.
- For component docs, include the actual prop types from the source code.
- Keep README concise — link to detailed docs instead of putting everything in one file.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
