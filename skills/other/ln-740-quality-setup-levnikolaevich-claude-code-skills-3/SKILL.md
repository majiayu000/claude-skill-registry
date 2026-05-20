---
name: ln-740-quality-setup
description: "Sets up linters, pre-commit hooks, and test infrastructure. Use when adding code quality tooling to a project."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-740-quality-setup

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

Coordinates code quality tooling configuration for the project.

---

## Purpose & Scope

**Does:**
- Detects project technology stack (TypeScript/React, .NET, Python)
- Checks for existing quality configurations
- Delegates to specialized workers for each quality aspect
- Verifies final configuration works correctly

**Does NOT:**
- Generate configuration files directly (workers do this)
- Modify source code
- Run in isolation (requires ln-720 structure first)

---

## When to Use

| Trigger | Action |
|---------|--------|
| After ln-720-structure-migrator completes | Automatic delegation from ln-700 |
| Manual quality setup needed | Invoke directly with project path |
| Existing project needs quality tools | Run with existing config detection |

---

## Workflow Overview

| Phase | Action | Output |
|-------|--------|--------|
| 1 | Stack Detection | Identified technologies |
| 2 | Existing Config Check | Skip/merge/replace decisions |
| 3 | Parallel Delegation | Worker invocations |
| 4 | Verification | Working quality pipeline |

---

## Phase 1: Stack Detection

Detect project technologies to determine which quality tools to configure.

**Detection Rules:**

| File Pattern | Technology | Linter Stack |
|--------------|------------|--------------|
| `package.json` + `tsconfig.json` | TypeScript/React | ESLint + Prettier |
| `*.csproj` or `*.sln` | .NET | editorconfig + Roslyn |
| `pyproject.toml` or `requirements.txt` | Python | Ruff |
| Multiple detected | Mixed | Configure all detected |

**Actions:**
1. Glob for technology indicators
2. Build technology list
3. Log detected stack to user

---

## Phase 2: Existing Configuration Check

Before delegating, check what configurations already exist.

**Config Files to Check:**

| Technology | Config Files |
|------------|--------------|
| TypeScript | `eslint.config.*`, `.prettierrc*`, `tsconfig.json` |
| .NET | `.editorconfig`, `Directory.Build.props` |
| Python | `ruff.toml`, `pyproject.toml [tool.ruff]` |
| Pre-commit | `.husky/`, `.pre-commit-config.yaml` |
| Tests | `vitest.config.*`, `pytest.ini`, `*.Tests.csproj` |

**Decision Matrix:**

| Existing Config | Action | Confirmation |
|-----------------|--------|--------------|
| None found | Create from template | No |
| Exists but incomplete | Extend to match template | No |
| Exists and matches template | Skip | Inform user |

**Completeness Check (Python):** evaluate against ln-741's Completeness Check table (7 aspects: Ruff rules, per-file-ignores, advanced settings, MyPy strict, advanced tools, lint script, editorconfig). If ANY aspect is incomplete, delegate to ln-741 with instruction to EXTEND (not replace).

---

## Phase 3: Parallel Delegation

Invoke workers for each quality aspect. Workers can run in parallel as they configure independent tools.

**Delegation Order:**

```
ln-740 (this)
    |
    +---> ln-741-linter-configurator
    |         - ESLint/Prettier (TypeScript)
    |         - editorconfig/Roslyn (.NET)
    |         - Ruff (Python)
    |
    +---> ln-742-precommit-setup
    |         - Husky + lint-staged (Node.js)
    |         - pre-commit framework (Python)
    |         - commitlint
    |
    +---> ln-743-test-infrastructure
              - Vitest (TypeScript)
              - xUnit (.NET)
              - pytest (Python)
```

Pass detected stack and existing configs to workers via direct Skill tool invocation. For Python: instruct ln-741 to apply full quality stack per its Completeness Check table.

**Invocations:**
```
Skill(skill: "ln-741-linter-configurator", args: "{projectPath}")
Skill(skill: "ln-742-precommit-setup", args: "{projectPath}")
Skill(skill: "ln-743-test-infrastructure", args: "{projectPath}")
```

---

## Phase 4: Verification

After all workers complete, verify the quality pipeline works.

**Verification Steps:**

| Check | TypeScript | Python | .NET |
|-------|-----------|--------|------|
| Lint | ESLint | `ruff check` | `dotnet format --verify-no-changes` |
| Format | Prettier | `ruff format --check` | dotnet format |
| Type check | `tsc --noEmit` | `mypy` | Roslyn (build) |
| Import boundaries | depcruise | `lint-imports` | -- |
| Unused deps | knip | `deptry` | -- |
| Dead code | knip | `vulture` | -- |
| Vulnerability scan | `npm audit` | `pip-audit` | -- |
| Unified script | `bash scripts/lint.sh` | `bash scripts/lint.sh` | `bash scripts/lint.sh` |
| Tests | `npm test` | `pytest` | `dotnet test` |
| Hooks | Create test commit | Create test commit | Create test commit |

**On Failure:**
1. Log specific failure
2. Suggest fix or re-run specific worker
3. Do NOT mark as complete until verification passes

---

## Critical Rules

> **RULE 1:** Never overwrite existing user configurations without explicit confirmation.

> **RULE 2:** Workers run AFTER stack detection - do not invoke workers without knowing the stack.

> **RULE 3:** Verification phase is MANDATORY - quality setup is not complete until tools run successfully.

> **RULE 4:** eslint-config-prettier is REQUIRED when both ESLint and Prettier are configured.

---

**TodoWrite format (mandatory):**
```
- Invoke ln-741-linter-configurator (pending)
- Invoke ln-742-precommit-setup (pending)
- Invoke ln-743-test-infrastructure (pending)
- Verify quality pipeline (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 3a | ln-741-linter-configurator | Shared (Skill tool) — ESLint/Prettier, editorconfig, Ruff |
| 3b | ln-742-precommit-setup | Shared (Skill tool) — Husky, lint-staged, commitlint |
| 3c | ln-743-test-infrastructure | Shared (Skill tool) — Vitest, xUnit, pytest |

**All workers:** Invoke via Skill tool — workers see coordinator context.

## Definition of Done

- [ ] All detected technology stacks have appropriate quality tools
- [ ] Existing configurations preserved or backed up
- [ ] Lint command runs without errors
- [ ] Format command runs without errors
- [ ] Test command runs and sample tests pass
- [ ] Pre-commit hooks trigger on test commit
- [ ] User informed of all installed tools and commands

---

## Phase 5: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `execution-orchestrator`. Analyze this session per protocol §7. Output per protocol format.

---

## Reference Files

| File | Purpose |
|------|---------|
| [stack_detection.md](references/stack_detection.md) | Detailed detection rules |
| [verification_checklist.md](references/verification_checklist.md) | Full verification checklist |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No stack detected | Empty project | Ask user for intended stack |
| Worker failed | Missing dependencies | Install prerequisites, retry |
| Verification failed | Config error | Check specific tool output, fix |
| Hooks not working | Git not initialized | Run `git init` first |

---

**Version:** 3.0.0
**Last Updated:** 2026-03-18
