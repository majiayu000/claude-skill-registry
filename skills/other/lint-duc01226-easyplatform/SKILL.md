---
name: lint
version: 1.0.0
description: '[Code Quality] Run linters and fix issues for backend or frontend'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`

## Quick Summary

**Goal:** Run linters (.NET analyzers and/or ESLint/Prettier) and report or auto-fix code quality issues.

**Workflow:**

1. **Parse** — Determine scope from arguments: backend, frontend, or both; fix mode or report-only
2. **Execute** — Run `dotnet build` for .NET analyzers or `nx lint` / `prettier` for Angular
3. **Report** — Group issues by severity (error/warning/info) with file paths and line numbers

**Key Rules:**

- No argument = run both backend + frontend in report-only mode
- `fix` argument = apply safe auto-fixes, report remaining manual items
- Always show file paths and line numbers in output

Run linting: $ARGUMENTS

## Instructions

1. **Parse arguments**:
    - `backend` or `be` → Run .NET analyzers
    - `frontend` or `fe` → Run ESLint/Prettier
    - `fix` → Auto-fix issues where possible
    - No argument → Run both, report only

2. **For Backend (.NET)**:

    ```bash
    dotnet build EasyPlatform.sln /p:TreatWarningsAsErrors=false
    ```

    - Check for analyzer warnings (CA*, IDE*, etc.)
    - Report code style violations

3. **For Frontend (Angular/Nx)**:

    ```bash
    cd src/PlatformExampleAppWeb
    nx lint playground-text-snippet
    nx lint platform-core
    ```

    With auto-fix:

    ```bash
    nx lint playground-text-snippet --fix
    npx prettier --write "apps/**/*.{ts,html,scss}" "libs/**/*.{ts,html,scss}"
    ```

4. **Report format**:
    - Group issues by severity (error, warning, info)
    - Show file paths and line numbers
    - Suggest fixes for common issues

5. **Auto-fix behavior**:
    - If `fix` argument provided, apply safe auto-fixes
    - Report what was fixed vs what needs manual attention

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
