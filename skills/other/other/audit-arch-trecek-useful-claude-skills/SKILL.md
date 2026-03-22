---
name: audit-arch
description: Audit codebase for adherence to architectural standards, practices, and rules. Use when user says "audit arch", "audit architecture", "check architecture", or "architectural review". Spawns parallel subagents to examine multiple architectural aspects and generates a structured report.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Auditing codebase architecture...'"
          once: true
---

# Architectural Audit Skill

Audit the codebase for adherence to architectural standards and rules.

## When to Use

- User says "audit arch", "audit architecture", "check architecture"

## Critical Constraints

**NEVER:**
- Modify any source code files
- Update an existing report - always generate new

**ALWAYS:**
- Use subagents for parallel exploration
- Write report to `temp/audit-arch/arch_audit_{YYYY-MM-DD_HHMMSS}.md`
- Provide file paths and line numbers
- Categorize by severity (CRITICAL, HIGH, MEDIUM, LOW)

---

## Architectural Principles

### Principle 1: Single Source of Truth

**Rule:** All state reads must come from the authoritative source (database, API, configuration management). File outputs and caches are write-only. Systems never read files back as the primary source of state.

**Audit Strategy — 3-Question SSOT Test:**

Before flagging any file read as a P1 violation, ask all three questions. **All three must be YES** to report a violation:

1. **Two competing authoritative stores?** — Are there two (or more) distinct stores that both claim to hold the same piece of state? If there is only one store (e.g., the file IS the authority, memory is just the working copy), there is no SSOT violation.
2. **Can they diverge during NORMAL operation?** — Could the two stores hold different values during steady-state operation (not crash/restart/migration)? Startup bootstrapping that only runs once on a cold start is NOT "normal operation" for this test.
3. **Undocumented winner?** — If the two stores diverge, which one wins? Is that choice undocumented or ambiguous? A system with a documented reconciliation strategy is not a violation.

**Non-SSOT Patterns — Do NOT flag these:**
- **Crash-recovery / bootstrap reads**: One-time startup reconstitution from diagnostic logs, session journals, or crash artifacts. The authoritative source is unavailable at cold-start; the file is a recovery vehicle, not a competing authority.
- **Filesystem IPC**: Hook scripts and subprocess-launched tools communicate via files because there is no shared memory. The file IS the only viable communication medium — no alternative authoritative source exists.
- **TTL-bounded caches**: In-memory caches with documented freshness contracts (explicit TTL, invalidation on write). The documentation of the tradeoff is proof of intent; absence of documentation is the finding, not the cache itself.
- **Write-through persistent stores**: Systems where the file is the canonical authority and in-memory state is the working copy (e.g., gate files, lock files, config files). File-writes and in-memory-reads are the same authority, just in two representations.
- **Derived-artifact staleness fingerprints**: Generated files with embedded hashes that signal their own staleness (e.g., diagram files containing a source-hash header). The fingerprint is the freshness mechanism, not a competing store.

**Data Flow Tracing (for confirmed SSOT candidates):**
1. Find all file read operations in core application code
2. For each read, trace: what data is being read, and does it influence system behavior or state?
3. Identify the PRIMARY source: if file is read first and authoritative source synced afterward, file is PRIMARY (violation)
4. Check write/read symmetry: if system reads back what it wrote (without the TTL/write-through exceptions above), flag it

**Cross-Reference:** Findings discovered while auditing other principles that pass the 3-question test should be reported here as P1 violations.

---

### Principle 2: Domain-Based Organization

**Rule:** Clear separation between domains with consistent structure.

**Common patterns:**
- Core domain logic separated from infrastructure
- Clear boundaries between business logic, data access, presentation
- Shared utilities in well-defined locations
- No mixing of concerns (e.g., CLI logic in database layer)

**Audit Strategy:**
- Check for misplaced components (utilities at root, API code in data layer)
- Find orphaned/empty directories from incomplete migrations
- Identify duplicates across locations
- Verify domain boundaries are respected

---

### Principle 3: Dependency Layering

**Rule:** Dependencies flow one direction. Higher layers depend on lower layers, never reverse.

**Typical layering:**
```
presentation/  -> depends on business logic, data access
business logic -> depends on data access, infrastructure
data access    -> depends on infrastructure only
infrastructure -> depends on nothing project-specific
```

**Also check internal layering:** Within a domain, core modules should not import from higher-level modules (handlers, controllers, UI).

**Audit Strategy:**
- Scan imports in each layer for boundary violations
- Look for deferred imports (indicate architectural debt)
- Check that foundational layers don't depend on higher layers
- Verify circular dependencies don't exist

---

### Principle 4: No Cross-Domain Imports

**Rule:** Separate domains/modules must be independent. Feature A cannot import from Feature B directly.

**Audit Strategy:**
- Scan each domain for imports from other domains at the same layer
- Shared functionality should be in common utilities or lower layers
- Check for tight coupling between features

---

### Principle 5: Architecture Pattern Consistency

**Rule:** When using architectural patterns (MVC, repository pattern, state machines, etc.), implementations must follow consistent patterns across the codebase.

**Audit Strategy:**
- Identify the architectural patterns in use
- Compare implementations across different modules
- Check if patterns diverge - is it intentional or inconsistency?
- Look for pattern violations (e.g., bypassing the repository layer)

**Important:** If a component bypasses the established pattern to use file-first state loading, that's a P1 violation - report it under P1, not here.

---

### Principle 6: No Code Duplication

**Rule:** Shared functionality exists in exactly one location.

**Audit Strategy:**
- Find functions/classes with same name in multiple locations
- Check migration pairs: old location should only re-export, not duplicate
- Look for copy-pasted code blocks with slight variations
- Identify logic that could be extracted to shared utilities

**Migration Awareness:** During migration, shims are acceptable only if they re-export from new location. Full duplicate implementations are violations.

---

### Principle 7: Data Access Pattern Compliance

**Rule:** All data access through designated abstraction layer (repositories, DAOs, services), never direct client usage in business logic.

**Audit Strategy:**
- Find direct database/API client usage outside designated data access layer
- Check for direct imports of database drivers, HTTP clients in business logic
- Verify all queries go through the abstraction layer

---

### Principle 8: No Monolithic Files

**Rule:** No file should exceed 1000 lines. Large files should be decomposed.

**Audit Strategy:**
- Find files exceeding 1000 lines (exclude generated/vendored)
- Flag files approaching threshold (800+ lines) as warnings

---

### Principle 9: Model Construction Integrity

**Rule:** When constructing models/objects from dicts/external data, use factory methods or full validation. Never manually select fields in constructor calls.

**Rationale:** Manual field selection silently drops unlisted fields. Optional fields are especially vulnerable since missing them causes no validation error.

**Audit Strategy:**
- Find `Model(field1=dict["x"], field2=dict.get("y"))` patterns
- Check if all source dict fields are mapped to target model
- Verify factory methods exist for cross-schema transformations
- Look for validation being skipped

**Severity:** HIGH - silent data loss breaks downstream consumers

---

### Principle 10: External Interface Compliance

**Rule:** Classes extending external framework base classes must implement ALL interface methods explicitly. Avoid mixin patterns where method resolution order affects behavior.

**Audit Strategy:**
- Find classes extending external bases (framework classes, third-party libraries)
- Check mixin ordering: mixins should come BEFORE the base class they augment
- Verify both sync AND async methods work (not inherited `NotImplementedError` stubs)
- Confirm contract tests exist for external interface compliance

**Severity:** CRITICAL - Interface mismatches only surface at runtime in specific code paths

---

### Principle 11: Dependency Currency

**Rule:** Direct dependencies should track current major versions. Minor/patch drift is acceptable; lagging a major version is not.

**Audit Strategy:**
- Compare installed major versions against current stable releases for key dependencies
- Flag any dependency more than one major version behind

**Severity:** MEDIUM - stale major versions accumulate migration debt and miss security fixes

---

## Cross-Cutting Design Guidelines

These apply across all principles when evaluating architectural decisions:

1. **Implicit correction masks upstream failures** — Reject invalid input rather than fixing it. Examples: silent type conversion, default values for required fields, translation layers that never reject, retry loops that swallow errors.

2. **Functions that accept all inputs without rejection are fallbacks, not validators** — If a "validator" or "normalizer" never raises an error, it's hiding problems.

**Standard patterns that are NOT cross-cutting violations:**
- **Error-accumulating discovery functions**: Functions that perform batch operations (directory listing, file scanning, import discovery) and log + accumulate errors into a return list rather than raising on first failure. These are correct behavior: partial results with logged failures are more useful than an abort.
- **Validator error collections**: Classes or functions that return a list of validation errors (e.g., Pydantic validators, marshmallow `ValidationError`, custom `errors: list[str]` returns). These are the standard pattern — a validator that collects all errors before returning is not "hiding" problems.
- **Module facade re-exports**: Public `__init__.py` files that re-export symbols from private submodules via `__all__`. These are gateway API contracts, not backward-compatibility shims. Only flag re-exports if the old location still contains a full duplicate implementation.

3. **System-derived values belong in code, not external input** — Values determined by workflow state (status, IDs, counts) should be set by the system that owns them, not expected from external sources.

4. **No backward compatibility** — Flag any code containing these keywords as violations: `legacy`, `deprecated`, `backward`, `compat`, `migration shim`, `old format`, `previous version`, `for compatibility`. Dead code should be deleted, not preserved with comments explaining why it exists.

---

## Audit Workflow

1. **Launch parallel subagents** for each principle
2. **Apply P1 3-question gate** before finalizing any P1 findings — confirm all three questions are YES and the pattern is not on the whitelist
3. **Apply cross-cutting whitelist** — verify CC-flagged patterns are not error accumulation, validator collections, or facade re-exports
4. **Apply severity gate** — CRITICAL requires data loss, security bypass, or correctness bug; downgrade findings that do not meet this bar
5. **★ Staleness filter** — run `git log --oneline -20` in the project root and scan commit subjects for evidence that any finding was recently resolved. Mark findings as **STALE** (with the resolving commit hash) if evidence exists. Do not remove stale findings — include them in the report with a STALE tag so the user can verify.
6. **Consolidate findings** by principle and severity
7. **Cross-reference:** Ensure findings are categorized by the principle they violate, not just where discovered
8. **Suggest new principle** (optional) — see below
9. **Write report** to `temp/audit-arch/arch_audit_{YYYY-MM-DD_HHMMSS}.md`
10. **Output summary** to terminal

---

## Principle Suggestion (Optional)

After consolidating findings, consider whether a **new** architectural principle would significantly benefit the codebase.

**Criteria - ALL must be true:**
- Not a one-off issue
- No existing principle covers it
- Would prevent recurring architectural debt or bugs
- Impact would be HIGH or CRITICAL level

**If criteria met:** Add "Suggested Principle" section to report with:
- One-sentence rule statement
- 2-3 specific locations that motivated it

**If criteria NOT met:** Omit section entirely. Do not suggest principles just to have a suggestion.

---

## Exclusions

Do NOT flag:
- Test files
- Re-export shims (thin wrappers only)
- Project config reads (package.json, build configs)
- External tool output (test runner output, build logs)

---

## Severity Guidelines

**CRITICAL** (requires at least one of):
- Silent data loss or corruption in production code paths
- Security boundary bypass (auth, isolation, trust boundary violated)
- Correctness bug that produces wrong results silently
- **NOT CRITICAL**: Infrastructure patterns that work correctly but read from disk (crash recovery, IPC, caches). Use HIGH or MEDIUM for these if they warrant a finding at all.

**HIGH:**
- Lower layers importing from higher layers
- Cross-domain imports at same layer
- Duplicate implementations
- Manual field selection causing silent data loss
- External interface contract violations (runtime surfaces at specific code paths)

**MEDIUM:**
- Code in wrong domain
- Inconsistent patterns
- Deferred imports indicating debt
- Stale major version dependencies

**LOW:**
- Naming inconsistencies
- Empty directories not cleaned up
