---
name: integration-checker
description: "Verify cross-component wiring and data flow."
user-invocable: false
command: /integration-checker
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - integration check
    - check integration
    - verify wiring
    - are components connected
    - check connections
    - integration-checker
    - wiring check
  pairs_with:
    - feature-lifecycle
    - systematic-code-review
  complexity: Medium
  category: process
---

# Integration Checker Skill

**Existence does not equal integration.** A component existing is implementation-level verification; a component being connected is integration-level verification. Both are necessary. Neither is sufficient alone.

This skill catches the most common class of real-world bugs in AI-generated code: components that are individually correct but not connected to each other. A function can exist, contain real logic, pass correctness verification, and never be imported or called. An API endpoint can be defined but never wired into the router. An event handler can be registered but never receive events.

This is a read-only analysis skill -- it reads and reports but does not fix wiring issues. Fixes route back to /feature-lifecycle (implement phase) or the user, because integration fixes often require design decisions about which component should call which.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| classifying exports/imports and tracing data flow (Phases 0-2) | `wiring-checks.md` | Loads detailed guidance from `wiring-checks.md`. |

## Instructions

### Phase 0: PRIME

**Goal**: Establish context, detect language, identify scope.

**Step 1: Read repository CLAUDE.md** (if present) and follow any project-specific conventions before proceeding.

**Step 2: Detect execution context**

Determine if running within the feature pipeline or standalone:
- **Pipeline**: Check for `.feature/state/implement/` artifact. If present, load it to understand what was built and scope the check to changed/added files. Scoping to changed files prevents wasting time analyzing unchanged code in large repositories.
- **Standalone**: Scope to the current working directory or user-specified path. Analyze all source files.

**Step 3: Detect project language(s)**

Detect language(s) before applying any verification techniques -- different languages have fundamentally different import/export patterns.

> See `references/wiring-checks.md` for language detection indicators, per-language export/import patterns, and common integration failures per language.

Multiple languages may coexist. Run all applicable techniques for each.

**Gate**: Language(s) detected. Scope established. Proceed to Phase 1.

---

### Phase 1: EXPORT/IMPORT MAP

**Goal**: For every export in scope, determine its wiring status. Every export gets exactly one of three states -- no ambiguous classifications.

**Step 1: Discover exports**

Scan source files for exported symbols. Be language-aware:

- **Go**: Find all capitalized function, type, const, and var declarations at package level. Include method receivers on exported types.
- **Python**: Find all module-level function/class/variable definitions. Check `__all__` if present (it restricts the public API). Check `__init__.py` for re-exports.
- **TypeScript/JavaScript**: Find all `export` declarations, `export default`, and barrel file re-exports.

Skip `node_modules/`, `vendor/`, `.git/`, `__pycache__/`, `dist/`, `build/`, test fixtures, and generated files. These contain intentionally unused exports (library code, vendored deps) that would flood the report with false positives.

Record each export as: `{file, name, kind (function/type/const/var), line}`.

**Step 2: Discover imports and usages**

For each export found, search the codebase for:
1. **Import**: The symbol is imported (appears in an import statement referencing the exporting module)
2. **Usage**: The imported symbol is actually used (called, referenced, assigned, passed as argument) beyond the import statement itself

Both checks are required. An import without usage is a distinct failure mode from an orphan -- it signals someone intended to use the component but didn't finish wiring it.

**Step 3: Classify each export**

> See `references/wiring-checks.md` for the full classification table, exclusion list, and files to skip during discovery.

**Step 4: Build the export/import map**

Report failures first -- users need to see ORPHANED before IMPORTED_NOT_USED before WIRED.

```
## Export/Import Map

### ORPHANED (Failure)
| File | Export | Kind | Imported By |
|------|--------|------|-------------|
| api/handlers.go | HandleUserDelete | func | (none) |
| utils/format.py | format_currency | func | (none) |

### IMPORTED_NOT_USED (Warning)
| File | Export | Kind | Imported By | Used? |
|------|--------|------|-------------|-------|
| api/handlers.go | HandleUserUpdate | func | routes/api.go | No |

### WIRED (Pass) — [N] components
(Shown only in verbose mode)
```

**Gate**: All in-scope exports classified. Map produced. Proceed to Phase 2.

---

### Phase 2: DATA FLOW AND CONTRACT CHECK

**Goal**: For WIRED components, verify that real data flows through the connections and that output shapes match input expectations. A component wired to always receive empty data is functionally disconnected.

This phase checks two things simultaneously because they both operate on the same set of WIRED connections identified in Phase 1.

This is structural analysis, not semantic verification. Contract checking verifies shape and naming compatibility, not whether data is logically correct -- semantic correctness would require runtime information that static analysis cannot provide.

#### Data Flow Tracing

For each WIRED connection, check whether real data actually reaches the component.

> See `references/wiring-checks.md` for the full catalog of data flow failure patterns (hardcoded empty data, placeholder data, dead parameters, mock remnants) and contract mismatch patterns (shape, type, event/message mismatches) with confidence level guidance.

**Gate**: Data flow and contract findings recorded. Proceed to Phase 3.

---

### Phase 3: REPORT

**Goal**: Produce a structured integration report with actionable findings. Report facts and show the wiring map -- not prose about the wiring map.

**Step 1: Requirements integration map (pipeline mode only)**

If running within the feature pipeline and a task plan exists in `.feature/state/plan/`, trace each requirement from entry point to implementation using WIRED / PARTIAL / UNWIRED status.

> See `references/wiring-checks.md` for the requirements integration map format and status definitions.

**Step 2: Compile integration report**

```markdown
# Integration Check Report

## Summary
- Components checked: [N]
- WIRED: [N]
- IMPORTED_NOT_USED: [N]
- ORPHANED: [N]
- Data flow issues: [N]
- Contract mismatches: [N]
- Integration score: [WIRED / (WIRED + IMPORTED_NOT_USED + ORPHANED) * 100]%

## Verdict: PASS / WARN / FAIL

PASS: No ORPHANED components, no data flow issues, no contract mismatches
WARN: No ORPHANED, but has IMPORTED_NOT_USED or low-confidence contract findings
FAIL: Has ORPHANED components, data flow issues, or high-confidence contract mismatches

## Export/Import Map
[From Phase 1 — only issues, unless verbose mode]

## Data Flow Issues
[From Phase 2 — data flow findings]

## Contract Mismatches
[From Phase 2 — contract findings with confidence level]

## Requirements Integration Map
[From Step 1 — if in pipeline mode]

## Recommended Actions
1. [Specific action for each ORPHANED component]
2. [Specific action for each IMPORTED_NOT_USED]
3. [Specific action for each data flow issue]
4. [Specific action for each contract mismatch]
```

Only fail the verdict on high-confidence contract mismatches. Low-confidence findings in dynamic languages are informational -- they belong in the WARN tier, not FAIL.

**Step 3: Verdict and next steps**

| Verdict | Next Step |
|---------|-----------|
| **PASS** | Proceed to /feature-lifecycle (validate phase) |
| **WARN** | Review warnings. Proceed if warnings are intentional (unused imports for future use, etc.). Fix if unintentional. |
| **FAIL** | Route back to /feature-lifecycle (implement phase) with specific wiring tasks so validation runs only after the wiring is in place. |

**Gate**: Report produced with verdict and actionable recommendations.

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No source files found | Wrong scope path or empty project | Verify working directory, check scope parameter |
| Language not detected | No recognizable build files or source extensions | Specify language manually or check project structure |
| Too many exports to analyze | Large monorepo or library with thousands of exports | Narrow scope to changed files (use `git diff --name-only` against base branch) |
| False positive ORPHANED | Library code, plugin interfaces, or entry points | Check exclusion patterns. If legitimate public API, add to exclusions. |
| Circular import detected | Python circular imports or Go import cycles | Report as separate finding -- circular imports are integration issues themselves |
| No implementation artifact | Running in pipeline mode but implement phase didn't checkpoint | Fall back to standalone mode using git diff to identify changed files |

## References

- [Feature State Conventions](../feature-lifecycle/references/shared.md)
- [ADR-078: Integration Checker](../../adr/078-integration-checker.md)
