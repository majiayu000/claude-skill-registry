---
name: ln-741-linter-configurator
description: Configures ESLint, Prettier, Ruff, mypy, and .NET analyzers
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-741-linter-configurator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-740-quality-setup

Configures code linting, formatting, and type checking tools for TypeScript, Python, and .NET projects.

---

## Purpose & Scope

**Does:**
- Detects which linter stack to configure based on project type
- Checks for existing linter configurations
- Generates appropriate config files from templates
- Installs required dependencies (always latest versions, no pinning)
- Generates unified lint script (`scripts/lint.sh`)
- Verifies all linters run without errors

**Does NOT:**
- Configure pre-commit hooks (ln-742 does this)
- Set up test infrastructure (ln-743 does this)
- Modify source code

---

## Supported Stacks

| Technology | Linter | Type Checker | Formatter | Config Files |
|------------|--------|-------------|-----------|--------------|
| TypeScript | ESLint 9+ (flat config) | TypeScript (tsc) | Prettier | `eslint.config.ts`, `.prettierrc` |
| .NET | Roslyn Analyzers | Roslyn | dotnet format | `.editorconfig`, `Directory.Build.props` |
| Python | Ruff | mypy | Ruff (built-in) | `ruff.toml`, `mypy.toml` (or `pyproject.toml`) |

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
| Python | mypy config | `mypy.toml`, `mypy.ini`, `pyproject.toml [tool.mypy]` |

**Decision Logic:**
1. If config exists and is complete: **SKIP** (inform user)
2. If config exists but incomplete: **ASK** user to merge or replace
3. If no config exists: **CREATE** from template

---

## Phase 2: Generate Configuration

Use templates from references/ folder. Customize placeholders based on project.

**TypeScript:**
1. Copy `eslint_template.ts` to project root as `eslint.config.ts`
2. Copy `prettier_template.json` as `.prettierrc`
3. Add scripts to `package.json`:
   - `"lint": "eslint ."`
   - `"lint:fix": "eslint . --fix"`
   - `"format": "prettier --write ."`
   - `"format:check": "prettier --check ."`
   - `"typecheck": "tsc --noEmit"`
   - `"lint:all": "npm run typecheck && npm run lint && npm run format:check"`
4. For React projects: uncomment React sections in template

**.NET:**
1. Copy `editorconfig_template.ini` as `.editorconfig`
2. Copy `directory_build_props_template.xml` as `Directory.Build.props`
3. Ensure analyzers are included (SDK 5+ includes them by default)

**Python:**
1. Copy `ruff_template.toml` as `ruff.toml`
   - OR merge into existing `pyproject.toml` under `[tool.ruff]`
2. Copy `mypy_template.toml` as `mypy.toml`
   - OR merge into existing `pyproject.toml` under `[tool.mypy]`
3. Update `known-first-party` in isort config to match project package name
4. Update `files` in mypy config to match project source directories

---

## Phase 3: Install Dependencies

Install required packages. **Always install latest versions — no version pinning.**

**TypeScript:**
```
npm install -D eslint @eslint/js typescript-eslint eslint-config-prettier prettier eslint-plugin-unicorn jiti
```

> For React projects, also install: `npm install -D eslint-plugin-react eslint-plugin-react-hooks`

> **Note on jiti:** Required for `eslint.config.ts` on Node.js < 22.10. On Node.js 22.10+ TypeScript configs are supported natively.

**.NET:**
- Analyzers included in SDK 5+ — no separate install needed

**Python:**
```
uv add --dev ruff mypy
```
```
# OR without uv:
pip install ruff mypy
```

---

## Phase 4: Generate Lint Script

Generate `scripts/lint.sh` from `lint_script_template.sh` with checks for the detected stack.

1. Copy `lint_script_template.sh` to `scripts/lint.sh`
2. Uncomment the check lines matching the detected stack (Python/TypeScript/.NET)
3. Set `TOTAL` variable to match the number of active checks
4. Make file executable: `chmod +x scripts/lint.sh`
5. For TypeScript: ensure `"lint:all"` script exists in `package.json`

---

## Phase 5: Verify Setup

After configuration, verify everything works.

**TypeScript:**
```bash
npx tsc --noEmit
npx eslint .
npx prettier --check .
```

**.NET:**
```bash
dotnet format --verify-no-changes
```

**Python:**
```bash
ruff check .
ruff format --check .
mypy
```

**Unified verification:**
```bash
bash scripts/lint.sh
```
Expected: Exit code 0 for all checks.

**On Failure:** Check error output, adjust config, re-verify.

---

## Phase 6: Optional Advanced Tools

Suggest but do not auto-install. Inform user and add as commented lines in `scripts/lint.sh`.

| Stack | Tool | Purpose | Install |
|-------|------|---------|---------|
| TypeScript | dependency-cruiser | Architecture boundary validation | `npm install -D dependency-cruiser` |
| TypeScript | knip | Unused code/dependency detection | `npm install -D knip` |
| Python | vulture / deadcode | Dead code detection | `uv add --dev vulture` |
| Python | import-linter | Circular import prevention | `uv add --dev import-linter` |
| Python | deptry | Unused/missing dependency detection | `uv add --dev deptry` |
| .NET | CSharpier | Opinionated formatter (Prettier for C#) | `dotnet tool install csharpier` |

---

## Critical Rules

> **RULE 1:** Always include `eslint-config-prettier` (last in config) when using ESLint + Prettier together.

> **RULE 2:** Use ESLint flat config format (`eslint.config.ts`), NOT legacy `.eslintrc`.

> **RULE 3:** Ruff replaces Black, isort, flake8, and many other Python tools. Do NOT install them separately.

> **RULE 4:** Never disable strict TypeScript rules without documented reason.

> **RULE 5:** Always run mypy alongside Ruff for Python projects. Ruff handles style/bugs, mypy handles type safety.

> **RULE 6:** Use `recommendedTypeChecked` as ESLint default, not just `recommended`. Downgrade individual rules if needed.

> **RULE 7:** Never pin dependency versions in install commands — always install latest.

---

## Definition of Done

- [ ] Appropriate config files created for detected stack
- [ ] Dependencies installed (latest versions)
- [ ] `scripts/lint.sh` generated with correct checks for stack
- [ ] Lint command runs without errors on project source
- [ ] Format command runs without errors
- [ ] Type checker runs without errors (mypy for Python, tsc for TypeScript)
- [ ] No ESLint/Prettier conflicts (eslint-config-prettier installed)
- [ ] User informed of available lint/format commands and optional advanced tools

---

## Reference Files

| File | Purpose |
|------|---------|
| [eslint_template.ts](references/eslint_template.ts) | ESLint flat config template (TypeScript) |
| [prettier_template.json](references/prettier_template.json) | Prettier config template |
| [ruff_template.toml](references/ruff_template.toml) | Python Ruff config template |
| [mypy_template.toml](references/mypy_template.toml) | Python mypy config template |
| [lint_script_template.sh](references/lint_script_template.sh) | Unified lint script template |
| [editorconfig_template.ini](references/editorconfig_template.ini) | .NET editorconfig template |
| [directory_build_props_template.xml](references/directory_build_props_template.xml) | .NET analyzers template |
| [linter_guide.md](references/linter_guide.md) | Detailed configuration guide |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| ESLint/Prettier conflict | Missing eslint-config-prettier | Install and add as last config |
| ESLint projectService error | Config file not in tsconfig | Add to `allowDefaultProject` list |
| ESLint `.ts` config fails | Missing jiti | `npm install -D jiti` |
| TypeScript parse errors | Parser version mismatch | Align typescript-eslint with TS version |
| mypy missing stubs | Third-party library without types | Add `[[mypy.overrides]]` with `ignore_missing_imports` |
| mypy strict too strict | Hundreds of errors on first run | Start with relaxed config, enable strict gradually |
| Ruff not found | Not installed | `pip install ruff` or `uv add ruff` |
| dotnet format fails | Missing SDK | Install .NET SDK |

---

**Version:** 3.0.0
**Last Updated:** 2026-02-26
