---
name: ln-741-linter-configurator
description: Configures ESLint, Prettier, Ruff, and .NET analyzers
---

# ln-741-linter-configurator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-740-quality-setup

Configures code linting and formatting tools for TypeScript, .NET, and Python projects.

---

## Purpose & Scope

**Does:**
- Detects which linter stack to configure based on project type
- Checks for existing linter configurations
- Generates appropriate config files from templates
- Installs required dependencies
- Verifies linter runs without errors

**Does NOT:**
- Configure pre-commit hooks (ln-742 does this)
- Set up test infrastructure (ln-743 does this)
- Modify source code

---

## Supported Stacks

| Technology | Linter | Formatter | Config Files |
|------------|--------|-----------|--------------|
| TypeScript/React | ESLint 9+ (flat config) | Prettier | `eslint.config.mjs`, `.prettierrc` |
| .NET | Roslyn Analyzers | dotnet format | `.editorconfig`, `Directory.Build.props` |
| Python | Ruff | Ruff (built-in) | `ruff.toml` or `pyproject.toml` |

---

## Phase 1: Check Existing Configuration

Before generating configs, check what already exists.

**Files to Check:**

| Stack | Config Files | Glob Pattern |
|-------|--------------|--------------|
| TypeScript | ESLint config | `eslint.config.*`, `.eslintrc*` |
| TypeScript | Prettier config | `.prettierrc*`, `prettier.config.*` |
| .NET | Editor config | `.editorconfig` |
| .NET | Build props | `Directory.Build.props` |
| Python | Ruff config | `ruff.toml`, `pyproject.toml` |

**Decision Logic:**
1. If config exists and is complete: **SKIP** (inform user)
2. If config exists but incomplete: **ASK** user to merge or replace
3. If no config exists: **CREATE** from template

---

## Phase 2: Generate Configuration

Use templates from references/ folder. Customize placeholders based on project.

**TypeScript/React:**
1. Copy `eslint_template.mjs` to project root as `eslint.config.mjs`
2. Copy `prettier_template.json` as `.prettierrc`
3. Add scripts to `package.json`:
   - `"lint": "eslint ."`
   - `"lint:fix": "eslint . --fix"`
   - `"format": "prettier --write ."`
   - `"format:check": "prettier --check ."`

**.NET:**
1. Copy `editorconfig_template.ini` as `.editorconfig`
2. Copy `directory_build_props_template.xml` as `Directory.Build.props`
3. Ensure analyzers package reference included

**Python:**
1. Copy `ruff_template.toml` as `ruff.toml`
   - OR merge into existing `pyproject.toml` under `[tool.ruff]`
2. Add scripts to `pyproject.toml` or document commands

---

## Phase 3: Install Dependencies

Install required packages for each stack.

**TypeScript/React:**
```
npm install -D eslint @eslint/js typescript-eslint eslint-plugin-react eslint-plugin-react-hooks eslint-config-prettier prettier
```

> **CRITICAL:** `eslint-config-prettier` is REQUIRED to prevent ESLint/Prettier conflicts.

**.NET:**
- Analyzers configured via Directory.Build.props
- No separate install needed

**Python:**
```
pip install ruff
# OR with uv:
uv add --dev ruff
```

---

## Phase 4: Verify Setup

After configuration, verify linter works.

**TypeScript:**
```bash
npm run lint
npm run format:check
```
Expected: Exit code 0

**.NET:**
```bash
dotnet format --verify-no-changes
```
Expected: Exit code 0

**Python:**
```bash
ruff check .
ruff format --check .
```
Expected: Exit code 0

**On Failure:** Check error output, adjust config, re-verify.

---

## Critical Rules

> **RULE 1:** Always include `eslint-config-prettier` when using ESLint + Prettier together.

> **RULE 2:** Use ESLint flat config format (eslint.config.mjs), NOT legacy .eslintrc.

> **RULE 3:** Ruff replaces Black, isort, flake8, and many other Python tools. Do NOT install them separately.

> **RULE 4:** Never disable strict TypeScript rules without documented reason.

---

## Definition of Done

- [ ] Appropriate config files created for detected stack
- [ ] Dependencies installed
- [ ] Lint command runs without errors on project source
- [ ] Format command runs without errors
- [ ] No ESLint/Prettier conflicts (eslint-config-prettier installed)
- [ ] User informed of available lint/format commands

---

## Reference Files

| File | Purpose |
|------|---------|
| [eslint_template.mjs](references/eslint_template.mjs) | ESLint flat config template |
| [prettier_template.json](references/prettier_template.json) | Prettier config template |
| [editorconfig_template.ini](references/editorconfig_template.ini) | .NET editorconfig template |
| [directory_build_props_template.xml](references/directory_build_props_template.xml) | .NET analyzers template |
| [ruff_template.toml](references/ruff_template.toml) | Python Ruff config template |
| [linter_guide.md](references/linter_guide.md) | Detailed configuration guide |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| ESLint/Prettier conflict | Missing eslint-config-prettier | Install and add to config |
| TypeScript parse errors | Parser version mismatch | Align typescript-eslint with TS version |
| Ruff not found | Not installed | `pip install ruff` or `uv add ruff` |
| dotnet format fails | Missing SDK | Install .NET SDK |

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
