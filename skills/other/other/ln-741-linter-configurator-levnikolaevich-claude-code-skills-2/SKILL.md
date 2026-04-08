---
name: ln-741-linter-configurator
description: "Configures ESLint, Prettier, Ruff, mypy, and .NET analyzers. Use when setting up linting and formatting for a project."
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-741-linter-configurator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap

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
- Configure pre-commit hooks (separate worker)
- Set up test infrastructure (separate worker)
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
1. If no config exists: **CREATE** from template
2. If config exists but incomplete (fewer rules/tools than template): **EXTEND** to match template
3. If config matches template: **SKIP** (inform user)

**Completeness Check (Python):**

| Aspect | Check | Template Standard |
|--------|-------|-------------------|
| Ruff rules | Count `select` entries | 23+ categories (see `ruff_template.toml`) |
| Ruff per-file-ignores | Tests section exists | `tests/**/*.py` with S101,S105,S106,T201 |
| Ruff advanced | mccabe, flake8-bugbear, isort | All present |
| MyPy | `strict = true` | Enabled |
| Advanced tools | import-linter, deptry, vulture in dev deps | All installed |
| Lint script | `scripts/lint.sh` with 7 checks | All 7 active |
| .editorconfig | File exists | Present |

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
5. Generate advanced tool configs in `pyproject.toml`:
   - `[tool.importlinter]` from `importlinter_template.toml` -- adapt `root_packages` and contracts to project layer structure
   - `[tool.vulture]` from `vulture_template.toml` -- adapt `paths` to project source directory
   - `[tool.deptry]` from `deptry_template.toml` -- adapt `extend_exclude`
6. Generate `.editorconfig` from `editorconfig_template.ini` -- adapt `max_line_length` to match ruff `line-length`

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
uv add --dev ruff mypy import-linter deptry vulture pip-audit
```
```
# OR without uv:
pip install ruff mypy import-linter deptry vulture pip-audit
```

---

## Phase 4: Generate Lint Script

Generate `scripts/lint.sh` from `lint_script_template.sh` with ALL checks for the detected stack.

1. Copy `lint_script_template.sh` to `scripts/lint.sh`
2. Uncomment ALL check lines matching detected stack -- both basic AND advanced tools:

| Stack | Checks | TOTAL |
|-------|--------|-------|
| Python | ruff check, ruff format, mypy, lint-imports, deptry, vulture, pip-audit | 7 |
| TypeScript | typecheck, eslint, prettier, knip, depcruise | 5 |
| .NET | dotnet build, dotnet format | 2 |

3. Set `TOTAL` to match active checks count
4. Uncomment matching auto-fix commands in `--fix` block
5. Make executable: `chmod +x scripts/lint.sh`
6. For TypeScript: ensure `"lint:all"` script exists in `package.json`

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

## Phase 6: Fix Lint Errors

After generating all configs and installing tools, run `bash scripts/lint.sh --all` to see all violations.

1. Run `bash scripts/lint.sh --fix` to auto-fix what ruff can
2. Fix remaining errors manually (file by file)
3. For C901 (complexity) on functions that cannot be refactored now: add `# noqa: C901`
4. For deptry false positives: add `[tool.deptry.per_rule_ignores]` entries
5. Repeat until `bash scripts/lint.sh` passes with 0 failures

---

## Critical Rules

> **RULE 1:** Always include `eslint-config-prettier` (last in config) when using ESLint + Prettier together.

> **RULE 2:** Use ESLint flat config format (`eslint.config.ts`), NOT legacy `.eslintrc`.

> **RULE 3:** Ruff replaces Black, isort, flake8, and many other Python tools. Do NOT install them separately.

> **RULE 4:** Never disable strict TypeScript rules without documented reason.

> **RULE 5:** Always run mypy alongside Ruff for Python projects. Ruff handles style/bugs, mypy handles type safety.

> **RULE 6:** Use `recommendedTypeChecked` as ESLint default, not just `recommended`. Downgrade individual rules if needed.

> **RULE 7:** Never pin dependency versions in install commands -- always install latest.

> **RULE 8:** Advanced static analysis tools (import-linter, deptry, vulture, pip-audit) are MANDATORY for Python projects, not optional.

---

## Definition of Done

- [ ] Appropriate config files created for detected stack
- [ ] Dependencies installed (latest versions)
- [ ] `scripts/lint.sh` generated with correct checks for stack
- [ ] Lint command runs without errors on project source
- [ ] Format command runs without errors
- [ ] Type checker runs without errors (mypy for Python, tsc for TypeScript)
- [ ] No ESLint/Prettier conflicts (eslint-config-prettier installed)
- [ ] Advanced tools installed and configured (import-linter, deptry, vulture, pip-audit)
- [ ] `scripts/lint.sh` runs ALL checks (7 for Python) with exit code 0
- [ ] `.editorconfig` created with settings matching ruff config
- [ ] User informed of available lint/format commands

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
| [importlinter_template.toml](references/importlinter_template.toml) | Python import-linter config template |
| [vulture_template.toml](references/vulture_template.toml) | Python vulture config template |
| [deptry_template.toml](references/deptry_template.toml) | Python deptry config template |
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

**Version:** 4.0.0
**Last Updated:** 2026-03-18
