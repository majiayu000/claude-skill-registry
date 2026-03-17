---
name: project-conventions
description: Guides discovery and application of project-specific conventions including code patterns, naming, structure, and team practices. Use when exploring a codebase or implementing features to match existing patterns.
dependencies: []
---

# Project Conventions

This skill guides you in discovering and applying project-specific conventions. Every codebase has its own patterns and practices - your job is to find them and follow them.

---

## Convention Discovery Process

### Step 1: Project Configuration

Check these files for explicit conventions:

**Code Style:**
- `.eslintrc*`, `eslint.config.*` - JavaScript/TypeScript linting rules
- `.prettierrc*`, `prettier.config.*` - Formatting rules
- `pyproject.toml`, `setup.cfg`, `.flake8` - Python config
- `.editorconfig` - Editor settings
- `ruff.toml`, `.ruff.toml` - Ruff linter config

**Project Structure:**
- `tsconfig.json` - TypeScript paths and settings
- `package.json` - Scripts, dependencies
- `pyproject.toml` - Python project config

**Documentation:**
- `CONTRIBUTING.md` - Contribution guidelines
- `CLAUDE.md` - AI coding guidelines
- `README.md` - Project overview
- `docs/` - Extended documentation

### Step 2: Existing Code Patterns

Study the codebase to find implicit conventions:

**File Organization:**
- List the contents of `src/components/` to see how components are organized
- Search for files matching `*.test.*`, `*_test.*`, or `test_*` to find test file patterns
- List the contents of `src/utils/`, `src/lib/`, or `src/helpers/` to see utility organization

**Naming Patterns:**
- Search for exported function declarations in `src/` to find function naming patterns
- Search for Python function definitions (`def `) in `src/` to find naming conventions
- Search for exported class declarations to find class naming patterns

**Import Patterns:**
- Search for import statements in `src/` to find import style (absolute vs relative)
- Search for relative imports in Python files (`from .`) to find local import conventions

### Step 3: Similar Features

Find features similar to what you're building:

1. **Search for similar functionality:**
   - Search file contents for terms related to your feature (e.g., "profile")
   - Search for files matching feature-related name patterns

2. **Study the implementation:**
   - How is it structured?
   - What patterns does it use?
   - How does it handle errors?
   - How is it tested?

3. **Note the patterns:**
   - Component structure
   - State management approach
   - API call patterns
   - Validation approach

---

## Common Convention Areas

### Naming Conventions

**Discover by example:**
- Search for function declarations like `(export )?(async )?function ` in TypeScript files
- Search for variable declarations like `(const|let|var) ` in TypeScript files
- Search for component declarations like `(export )?function [A-Z]` in TSX files

**Common patterns:**
- `camelCase` for functions/variables
- `PascalCase` for components/classes
- `UPPER_SNAKE` for constants
- `kebab-case` for file names (some projects)
- `snake_case` for file names (Python)

### File Structure

**Discover the pattern:**
- List the contents of a component directory (e.g., `src/components/Button/`)
- List the contents of a feature module directory (e.g., `src/features/auth/`)

**Common patterns:**

Flat structure:
```
components/
  Button.tsx
  Button.test.tsx
  Button.styles.ts
```

Folder per component:
```
components/
  Button/
    index.ts
    Button.tsx
    Button.test.tsx
    Button.module.css
```

Feature-based:
```
features/
  auth/
    components/
    hooks/
    api.ts
    types.ts
```

### Error Handling

**Discover the pattern:**
- Search for try-catch patterns in TypeScript files
- Search for custom error types (`extends Error`) in the source
- Search for error handling in API modules

**Apply what you find:**
- Use the same error types
- Follow the same handling pattern
- Match logging approach

### Testing Patterns

**Discover the pattern:**
- Read the first 50 lines of test files to understand the test structure
- Read test setup and utility files (`src/test/setup.ts`, `src/test/utils.ts`)

**Match the patterns:**
- Test file location (co-located vs separate)
- Naming convention (`*.test.ts` vs `*.spec.ts`)
- Setup and teardown approach
- Mocking strategy
- Assertion style

### API Patterns

**Discover the pattern:**
- Search for API call patterns (`fetch`, `axios`, `api.`) in the source
- Read API response handling in API modules

**Match the patterns:**
- How are endpoints defined?
- How is authentication handled?
- What's the error format?
- How are responses typed?

---

## Convention Application Checklist

When implementing a feature, verify you're following conventions for:

### Code Style
- [ ] Variable naming matches existing code
- [ ] Function naming matches existing code
- [ ] File naming follows project pattern
- [ ] Import style matches (absolute vs relative)

### Structure
- [ ] File location follows project structure
- [ ] Component organization matches
- [ ] Export style matches (default vs named)

### Patterns
- [ ] Error handling follows project patterns
- [ ] Async patterns match existing code
- [ ] State management follows project approach
- [ ] API calls follow established patterns

### Testing
- [ ] Test file location is correct
- [ ] Test naming follows convention
- [ ] Test structure matches existing tests
- [ ] Mocking approach is consistent

### Documentation
- [ ] Comments follow existing style
- [ ] JSDoc/docstrings match project
- [ ] README updates if needed

---

## When Conventions Conflict

Sometimes you'll find inconsistent patterns:

1. **Prefer newer code** - Recent files often reflect current team preferences
2. **Prefer maintained code** - Active parts of the codebase reflect current practices
3. **Prefer documented conventions** - Explicit rules in configs override implicit patterns
4. **Ask if unclear** - When in doubt, ask the user which pattern to follow

---

## Red Flags

Watch for these signs that you might be breaking conventions:

- Your code looks very different from surrounding code
- You're using a library/pattern not used elsewhere
- Your file structure doesn't match siblings
- Your naming feels inconsistent with the codebase
- Linting errors (the project has explicit rules you're breaking)

When you notice these, stop and investigate the existing conventions more carefully.

## Integration Notes

Reference skill for discovering project conventions. Requires file reading and searching capabilities.
