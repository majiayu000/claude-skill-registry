---
name: CODE_QUALITY_CHECK
description: Apply the code-quality checklist to audit files or directories and produce a Markdown report with findings and suggested fixes. Use when asked to "audit these files", "run a quality check", "code quality review", or "check against the code-quality checklist".
---

# CODE QUALITY CHECK

**Owner:** QA

## Goal
Audit a target (file set or directory) against `.github/checklists/code-quality-checklist.yaml` and deliver a Markdown report with evidence and actionable fixes.

## Workflow

### 1. Load Inputs
- Read `target_path` (file, directory, or list).
- Respect checklist `meta.scope` (default: changed files + directly impacted dependencies).

### 2. Evaluate Rules
- Process rules top-down.
- Apply `activation_hint` and `stop_condition`:
  - Stop on first HIGH unless `--exhaustive` is requested.
  - Stop if findings_count > 25.

- Enforce modern, pragmatic (non-enterprise) code quality standards by ensuring the checklist includes (or is extended to include) rules in these areas:
  - **Correctness & Safety (baseline)**: input validation, error handling, edge cases, deterministic behavior, safe defaults.
  - **Readability & Maintainability**: naming, small focused functions, clear control flow, avoid cleverness, consistent conventions.
  - **Negative Space (readability-by-absence)**:
    - Visual: paragraph rule (blank lines), avoid wall-of-code, consistent formatting.
    - Structural: minimize public API surface, keep helpers private/internal.
    - Absence: prefer deleting/reducing code; avoid “just in case” abstractions.
  - **DRY / Single Source of Truth**: eliminate duplicated logic/data, centralize constants and domain rules.
  - **KISS**: simplest working solution, avoid unnecessary patterns/framework layers.
  - **YAGNI**: reject speculative features and premature generalization.
  - **SOLID (lightweight)**: primarily SRP and clear boundaries; avoid over-engineering in small projects.
  - **Complexity control**: avoid deep nesting, use guard clauses/early returns, limit cyclomatic complexity.
  - **Testability**: dependency boundaries, pure functions where possible, deterministic units, easy-to-mock seams.
  - **Testing (pragmatic)**: unit tests for business logic, integration tests for critical paths; avoid low-value test bloat.
  - **Type Safety (if applicable)**: avoid `any`, narrow types, prefer explicit interfaces, validate at boundaries.
  - **Performance (only when justified)**: avoid obvious inefficiencies, but do not micro-optimize without evidence.
  - **Security (baseline)**: secrets handling, injection risks, auth/permission checks, safe logging.
  - **Observability (baseline)**: meaningful errors, structured logs, no noisy logging, clear failure modes.
  - **Dependencies**: avoid unnecessary deps, keep versions updated, remove unused.
  - **Docs (just enough)**: READMEs for modules, docstrings only where behavior is non-obvious.

- For each rule:
  - Mark PASS/FAIL with evidence (file path + line/snippet).
  - For FAIL, provide a concrete fix that matches the rule’s `fix` guidance.
  - Preserve `severity` and `autofix` flags from the checklist.

- When proposing fixes, prioritize changes that maximize clarity and negative space:
  - Prefer guard clauses over nested conditionals.
  - Prefer extracting small, named helpers over long inline logic.
  - Prefer removing dead/duplicate code over refactoring into new abstractions.
  - Prefer consolidating domain rules/constants into a single place.

### 3. Apply Lean Guards
- Do not expand scope beyond `meta.scope`.
- Prefer small, safe fixes.
- Refactor only when required by a rule.
- Skip large migrations.
- Do not enforce enterprise-grade process (e.g., mandatory ADRs, heavy frameworks) unless explicitly requested.
- Prefer "small surface area" design: fewer public functions/classes, fewer configuration knobs.
- Avoid recommending new abstractions unless they remove duplication or reduce complexity.
- If a standard conflicts (e.g., DRY vs KISS), explain the trade-off and choose the simpler option unless the duplication is high-risk.

### 4. Produce Report
- Follow the checklist `output_schema`.
- Include:
  - **Summary**: counts by severity + decision.
  - **Findings**: list items with `id`, `severity`, `file`, `symbol` (if known), `evidence`, `fix`, `autofix`.
  - **Suggestions**: targeted next steps based on findings.

### 5. Save Output
- Write Markdown to `docs/qa/reports/code-quality-{{target_slug}}.md`.
- Create directories if missing.

## Anti-Patterns
- Do not mark PASS without evidence.
- Do not invent IDs, symbols, or file paths.
- Do not change scope unless the user explicitly requests it.
- Do not recommend “best practice” patterns without tying them to a concrete risk.
- Do not propose premature architecture (microservices, event buses, complex DDD) for small projects.
- Do not optimize performance without evidence (profiling, metrics, clear bottleneck).
- Do not add tests that duplicate coverage or only assert implementation details.
- Do not increase API surface area unless it improves usability and reduces coupling.
