---
name: code-scaffolding
description: "Generate project boilerplate, component templates, and framework scaffolding that follows existing codebase conventions. Use when the user says 'scaffold', 'generate boilerplate', 'create a new component', 'set up a new service', 'bootstrap', 'new module', 'add a new route', 'create a new endpoint', 'template for', 'stub out', or 'create a new page'. Also triggers on 'scaffolding', 'boilerplate', 'code generation', 'new feature skeleton', 'project setup', 'starter template', or 'generate files for'."
version: 1.0.0
---

# Code Scaffolding

Scaffolding is not about saving keystrokes — it is about encoding team conventions into every new file. The most dangerous boilerplate is the one that does not match the codebase. This skill detects existing patterns before generating anything.

Every generated file must be indistinguishable from one written by a long-tenured team member. If the codebase uses `kebab-case` filenames, you use `kebab-case`. If tests live next to source files, your tests go there too. No exceptions.

## When to Activate

- Creating new components, services, routes, or modules
- Setting up new projects or sub-packages within a monorepo
- Adding CRUD endpoints or API routes
- Creating test files alongside new code
- Bootstrapping a new feature with multiple coordinated files
- Generating database models, migrations, or seed files
- Adding CLI commands, background workers, or middleware

## Core Workflow: Convention-First Scaffolding

### Step 1: Detect Conventions

Before writing a single line, analyze **3-5 existing examples** of the same file type in the codebase. Use Glob and Read to find them. Extract:

- **File naming**: `UserProfile.tsx` vs `user-profile.tsx` vs `userProfile.tsx`
- **Directory placement**: Where do files of this type live? Nested by feature or flat by type?
- **Import patterns**: Absolute paths (`@/components/...`) vs relative? Import grouping and ordering?
- **Export style**: Named exports vs default? Barrel/index re-exports?
- **Error handling**: Try/catch patterns, error boundaries, Result types?
- **Test co-location**: `__tests__/` subdirectory, `.test.ts` alongside, or separate `tests/` tree?
- **Boilerplate patterns**: Common setup code, decorators, annotations, wrapper components?

If fewer than 3 examples exist, widen the search. If the codebase is new or empty, ask the user which conventions to follow before generating.

### Step 2: Confirm with User

Present the discovered conventions in a brief summary:

```
Detected conventions for React components:
- Directory: src/components/{ComponentName}/
- Files: index.tsx (barrel), ComponentName.tsx, ComponentName.test.tsx, ComponentName.module.css
- Exports: Named exports, re-exported from index
- Styling: CSS Modules
- Tests: Co-located with component

Proceed with these conventions, or override?
```

**Never assume.** If conventions are ambiguous or inconsistent across the codebase, surface the inconsistency and let the user decide.

### Step 3: Generate

Create files that match the detected conventions exactly. Every generated file must include:

- Correct imports matching codebase style
- Proper TypeScript types/interfaces (if the project uses TS)
- Error handling consistent with codebase patterns
- `TODO` comments explaining what business logic to implement — never placeholder "hello world" code
- Consistent formatting (the project's Prettier/ESLint config will handle this, but match indentation and style)

### Step 4: Companion Files

After generating the primary file, check if companion files are needed:

- **Test stub**: Matching the project's test framework and patterns
- **Type exports**: If the project centralizes types (`types/`, `*.types.ts`)
- **Index/barrel updates**: If the directory uses barrel exports, update `index.ts`
- **Storybook file**: If the project uses Storybook, generate a `.stories.tsx`
- **Style file**: CSS Module, styled-components file, or Tailwind class extraction
- **Documentation**: If the project co-locates docs (e.g., `.mdx` alongside components)

Only generate companion files for patterns that **already exist** in the codebase. Never introduce a new companion file pattern.

## Scaffolding Categories

| Type | What to Detect | What to Generate |
|---|---|---|
| **Frontend component** (page, layout, widget, form) | Component structure, styling approach, prop patterns, state management | Component file, test, styles, stories, index re-export |
| **API endpoint / route handler** | Route organization, middleware chain, validation, response format | Route handler, validation schema, test, types |
| **Database model / migration** | ORM patterns, naming conventions, field types, relationships | Model definition, migration file, seed data stub, types |
| **Service / repository class** | Interface patterns, dependency injection, error handling | Service class, interface, test, types |
| **CLI command** | Command framework (Commander, yargs, oclif), option patterns | Command file, test, help text |
| **Background job / worker** | Queue framework, retry patterns, logging | Job handler, test, queue registration |
| **Test suite** | Testing framework, assertion style, mock patterns, fixtures | Test file with describe/it blocks matching project style |

See `references/scaffolding-decision-matrix.md` for the detailed mapping of user intent to scaffold output.

## Convention Detection Checklist

Run through this checklist before generating any scaffold:

### Naming and Structure
- [ ] File naming convention: PascalCase vs kebab-case vs camelCase
- [ ] Directory structure: flat vs nested, feature-based vs type-based
- [ ] Co-located tests vs separate test directory
- [ ] Barrel/index export files present?

### Code Patterns
- [ ] Export style: named exports vs default exports
- [ ] Component style: functional vs class-based, hooks vs HOCs
- [ ] State management: local state, Context, Zustand/Redux/MobX
- [ ] Error handling: try/catch, error boundaries, Result/Either types
- [ ] Validation: Zod, Yup, Joi, class-validator, or manual

### Import Conventions
- [ ] Path aliases configured? (`@/`, `~/`, `#/`)
- [ ] Import grouping: external, internal, relative — in what order?
- [ ] Type-only imports: `import type { ... }` used?

### Framework-Specific
- [ ] Routing pattern: file-based, config-based, decorator-based
- [ ] Middleware chain: how middleware is registered and ordered
- [ ] Dependency injection: constructor injection, module injection, none

See `references/template-conventions.md` for framework-specific detection guides.

## Gotchas

### Never Introduce New Patterns
Scaffold must not introduce conventions that do not already exist in the codebase. If the project uses CSS Modules, do not generate a styled-components file. Consistency over novelty, always.

### Respect Monorepo Boundaries
In monorepos, each package may follow different conventions. `packages/ui` may use PascalCase React components while `packages/api` uses kebab-case Express handlers. Detect conventions **within the target package**, not across the repo.

### Update Barrel/Index Files
Scaffolding a new component often requires updating an `index.ts` barrel file to include the new export. Search for barrel files in the target directory and its parent. Missing this step breaks the import chain.

### Flag New Dependencies
If the scaffold would introduce an import from a library not already in `package.json` (or equivalent), flag it to the user before generating. Never silently add new dependencies.

### Use TODO Comments, Not Placeholder Logic
Never generate fake business logic the user must delete. Instead:

```typescript
// TODO: Implement user validation logic
// Expected: validate email format, check uniqueness against database
// Returns: validated user object or throws ValidationError
```

### Check for Existing Code Generators
Before scaffolding manually, check if the project already has code generation tooling:
- `plopfile.js` or `plopfile.ts` (Plop)
- `.hygen/` directory (Hygen)
- `nx.json` with generators (Nx)
- `turbo/generators/` (Turborepo)
- Custom scripts in `package.json` (`generate`, `scaffold`, `new`)

If generators exist, inform the user and ask whether to use them or generate directly.

### Test File Conventions
When generating test stubs, match the project's exact testing patterns:
- `describe`/`it` vs `test` blocks
- Import style for test utilities (`@testing-library/react`, `enzyme`, `vitest`)
- Mock patterns (`jest.mock`, `vi.mock`, manual mocks in `__mocks__/`)
- Setup/teardown patterns (`beforeEach`, `afterEach`, fixtures)
