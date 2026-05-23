---
name: audit-cohesion
description: Audit codebase for internal cohesion - how well components fit together and maintain consistent patterns. Distinct from audit-arch (which checks rule violations); this checks integration fitness and convergence. Use when user says "audit cohesion", "check cohesion", "cohesion audit", or "alignment check".
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: audit-cohesion] Auditing codebase cohesion and integration fitness...'"
          once: true
---

# Cohesion Audit Skill

Audit the codebase for internal cohesion: how well components integrate and maintain consistent patterns across boundaries.

**Key Distinction:** `audit-arch` checks whether architectural **rules** are followed (violations). `audit-cohesion` checks whether components **fit together** (alignment, consistency, completeness). A codebase can pass all architectural rules yet still have poor cohesion — parallel structures that diverge, registries with missing entries, or scattered features.

## When to Use

- User says "audit cohesion", "check cohesion", "cohesion audit", "alignment check"
- After major refactors to verify integration fitness
- Before planning new features to understand current alignment state

## Critical Constraints

**NEVER:**
- Modify any source code files
- Update an existing report — always generate new
- Duplicate findings that belong in audit-arch (rule violations)

**ALWAYS:**
- Use subagents for parallel exploration (one per cohesion dimension)
- All output goes under `temp/audit-cohesion/` (create if needed)
- Final report: `temp/audit-cohesion/cohesion_audit_{YYYY-MM-DD_HHMMSS}.md`
- Subagents must NOT create their own files — they return findings in their response text only
- Score each dimension (STRONG, ADEQUATE, WEAK, FRACTURED)

---

## Output Quality Standard

**The report must be plan-ready.** Every finding must contain enough detail that a `/make-plan` invocation can act on it without re-investigating the codebase.

**ENUMERATE, do not summarize.** The following are NOT acceptable findings:

| Bad (anemic) | Good (actionable) |
|---|---|
| "16 fields missing from registry" | Table listing each missing field name, its source file:line, and suggested lifecycle category |
| "Several source modules without tests" | Table listing each untested module path and what it does |
| "Export depth inconsistent" | Table listing each symbol that requires deep imports, its deep path, and where consumers import it from |
| "48 files use broad exception handlers" | Table listing each file:line, the exception type caught, and what it catches |

**Minimum per dimension:** Each dimension section MUST contain:
1. A **findings table** (markdown table with columns appropriate to the dimension)
2. Specific **file:line** references for every gap, violation, or inconsistency
3. Enough context that someone unfamiliar could locate and fix each issue

**If a dimension has no findings** (scores STRONG), still provide the evidence: what was checked, how many items passed, and key file paths examined.

---

## Subagent Output Requirements

Each subagent MUST structure its response as:

```
## Dimension: C{N} — {Name}
### Score: {STRONG|ADEQUATE|WEAK|FRACTURED}

### Methodology
{What was searched, how many items checked, key directories examined}

### Findings Table
| {columns appropriate to dimension} |
|---|
| {row per finding} |

### Evidence
{For each finding, the specific file:line, what was expected, what was found}

### Compliant Patterns
{Specific examples of things that ARE working well, with file:line}
```

**Subagents must NOT return prose summaries.** They must return structured data (tables, lists with file:line). If a subagent returns "X items are inconsistent" without listing each item, the finding is incomplete and must be expanded before inclusion in the report.

---

## Cohesion Dimensions

### C1: Structural Symmetry

**Question:** Do parallel structures maintain consistent patterns, or have they diverged?

**Audit Strategy:**

1. **Directory-level comparison** — produce a side-by-side table:

| Directory/File | Module A Has? | Module B Has? | Symmetric? | Notes |
|---------------|-------------|--------------|------------|-------|
| `handlers/` | Yes | Yes | Yes | — |
| `config.py` | Yes (single file) | Yes (directory/) | NO | Naming: BaseConfig vs ConfigManager |

List ALL directories and key files, not just divergent ones.

2. **Repository pattern comparison** — for each repository, verify:

| Repository | Extends Base? | Has Interface? | Has Factory Method? | Method Pattern |
|-----------|--------------|---------------|--------------------|--------------|

3. **Node/handler implementation comparison** — for each parallel pattern:

| Pattern | Module A Implementation | Module B Implementation | Consistent? |
|---------|----------------------|------------------------|-------------|

4. **Template/config comparison:**

| Config Type | Module A Path | Module B Path | Shared Components | Divergence |
|------------|-------------|--------------|------------------|-----------|

---

### C2: Interface Completeness

**Question:** Are adapter, factory, and contract chains complete with no missing links?

**Audit Strategy:**

1. **Adapter field coverage** — for each domain model field, verify adapter mapping:

| Field | In Adapter? | External Representation | Bidirectional? |
|-------|-------------|------------------------|---------------|

2. **Factory method coverage** — for each entity model, verify factory access:

| Model | Has Repository? | Has Factory Method? | Factory Method Name |
|-------|----------------|--------------------|--------------------|

3. **Contract test inventory** — for each interface, verify contract exists:

| Interface | Contract Test File | Tests Count | Full Surface Covered? |
|-----------|-------------------|-------------|---------------------|

4. **Type boundary audit** — find every place internal model instances cross boundaries:

| Location (file:line) | Model Type | Destination | Violation? |
|---------------------|-----------|------------|-----------|

---

### C3: Feature Locality

**Question:** Is related functionality co-located, or scattered across unrelated packages?

**Audit Strategy:**

1. **Feature file map** — for each major feature, enumerate ALL participating files:

| Feature | File Path | Role in Feature | Package |
|---------|----------|----------------|---------|
| Caching | `src/module_a/cache.py` | Module A caching | core |
| Caching | `src/module_b/cache/manager.py` | Module B caching | core |
| Caching | `lib/shared/cache_base.py` | Base abstraction | shared |

Audit the major cross-cutting features in the project.

2. **Shared utility audit** — for each shared module, count its importers by package:

| Shared Module | Total Importers | Module A Only | Module B Only | Shared | Verdict |
|-----------|----------------|-------------|--------------|--------|---------|
| `lib/shared/scope.py` | 8 | 0 | 8 | 0 | Misplaced — module B only |

3. **Import fan-in** — list every module with 10+ importers:

| Module | Importer Count | Is Shared Infrastructure? |
|--------|---------------|-------------------------|

---

### C4: Naming Convention Consistency

**Question:** Are naming patterns consistent across the codebase?

**Audit Strategy:**

1. **Class suffix inventory** — group all classes by their suffix pattern:

| Suffix | Count | Examples | Exceptions |
|--------|-------|---------|-----------|
| `*Repository` | 27 | PlanRepository, PhaseRepository | — |
| `*Manager` | 2 | CacheManager, StateManager | Mixed naming strategy |

2. **Method verb audit** — for each verb used in repository/handler methods:

| Verb | Count | Files | Synonym Conflicts |
|------|-------|-------|------------------|
| `get_` | 218 | 32 files | None |
| `fetch_` | ? | ? | Conflicts with get_? |

3. **File naming audit** — find files that break the dominant pattern:

| File | Pattern Expected | Pattern Found | Location |
|------|-----------------|---------------|----------|

4. **Enum audit:**

| Enum Class | Value Style | Location | Consistent? |
|-----------|------------|----------|-------------|

---

### C5: Test-Source Alignment

**Question:** Does the test structure mirror the source structure, with no orphans or gaps?

**Audit Strategy:**

1. **Source-to-test mapping** — for EVERY source module, find its test:

| Source Module | Test File | Exists? | Test Count |
|--------------|-----------|---------|-----------|
| `src/module_a/handler.py` | `tests/module_a/test_handler.py` | Yes | 12 |
| `lib/shared/utils.py` | — | NO | 0 |

List ALL gaps — every source file without a corresponding test file.

2. **Orphan detection** — test files whose source no longer exists:

| Test File | Expected Source | Source Exists? |
|-----------|----------------|---------------|

3. **Classification audit** — tests in wrong directories:

| Test File | Current Dir | Expected Dir | Reason |
|-----------|-------------|-------------|--------|

4. **Stale fixture detection:**

| Fixture File | Referenced By | Still Valid? |
|-------------|-------------|-------------|

---

### C6: Registry & Catalog Completeness

**Question:** Are all registries, catalogs, or lookup tables internally consistent and complete?

**Audit Strategy:**

Identify all registry patterns in the project (plugin registries, command catalogs, event handler tables, route maps, enum registries, feature flags, etc.), then for each:

1. **Registry gap analysis** — compare registered entries vs. implementations:

| Registry | Entry | Implementation Exists? | Implementation Location | Gap |
|----------|-------|----------------------|------------------------|-----|
| CommandRegistry | `export` | Yes | `commands/export.py:12` | — |
| CommandRegistry | `import` | NO | — | Missing implementation |

List EVERY missing entry.

2. **Reverse gap analysis** — implementations that should be registered but aren't:

| Implementation | Expected Registry | Registered? | Location |
|---------------|------------------|-------------|----------|

3. **Registry consistency audit** — registries with inconsistent entry formats:

| Registry | Entry | Format Expected | Format Found | Consistent? |
|----------|-------|----------------|-------------|-------------|

4. **Cross-registry consistency** — where multiple registries must stay synchronized:

| Primary Registry Entry | Secondary Registry | Appears in Secondary? | Gap |
|-----------------------|-------------------|----------------------|-----|

---

### C7: Configuration-Driven Behavior Alignment

**Question:** Do configuration-driven components stay synchronized with the behavior they control?

**Audit Strategy:**

Identify all places where configuration (schemas, settings, flags, manifests) drives runtime behavior, then verify alignment:

1. **Config-to-handler mapping** — for each config key/value that dispatches behavior:

| Config Key/Value | Handler/Behavior | Handler Exists? | Handler Location | Gap |
|-----------------|-----------------|----------------|-----------------|-----|

2. **Schema-to-model mapping** — for each schema field, verify the consuming model:

| Schema Field | Consumer Model | Field Mapped? | Type Match? | Gap |
|-------------|---------------|--------------|------------|-----|

3. **Dead configuration detection** — config entries with no active consumer:

| Config Entry | Any Consumer Found? | Last Modified |
|-------------|-------------------|--------------|

4. **Undocumented behavior detection** — behavior not covered by any config schema:

| Behavior (file:line) | Config Pathway | Documented in Schema? |
|---------------------|---------------|----------------------|

---

### C8: Export Surface Coherence

**Question:** Are `__init__.py` exports (or equivalent) consistent, complete, and intentional?

**Audit Strategy:**

1. **Symbol accessibility audit** — for key public symbols, check import depth:

| Symbol | Shallow Import Available? | Deep Import Required? | Consumer Count |
|--------|--------------------------|---------------------|---------------|
| `Config` | Yes | No | 45 |
| `AppState` | No | `from lib.schema.state.app_state import ...` | 23 |

List EVERY symbol that requires deep imports but has 5+ consumers.

2. **`__all__` consistency:**

| Package | Has `__all__`? | `__all__` Count | Actual Public Symbols | Delta |
|---------|---------------|----------------|---------------------|-------|

3. **Import pattern census** — how do consumers actually import:

| Symbol | Import Variants Found | Count Each | Dominant Pattern |
|--------|---------------------|-----------|-----------------|

4. **Stale re-export detection:**

| Re-export | Source Location | Target Location | Target Exists? |
|-----------|----------------|----------------|---------------|

---

### C9: Error Handling Uniformity

**Question:** Are error patterns (exceptions, logging, error states) consistent across the codebase?

**Audit Strategy:**

1. **Exception class inventory:**

| Exception Class | Base Class | Defined In | Used In (files) | Duplicate Elsewhere? |
|----------------|-----------|-----------|----------------|---------------------|

Flag duplicates (same name in different modules).

2. **Error state field comparison:**

| Error Field | In Module A State? | In Module B State? | Same Semantics? |
|------------|-------------------|-------------------|----------------|

3. **Broad exception handler census** — list EVERY `except Exception` or `except BaseException`:

| File:Line | Exception Caught | Handler Action | Justified? |
|-----------|-----------------|----------------|-----------|

4. **Logger initialization audit:**

| File | Logger Pattern | Consistent? |
|------|--------------|-------------|

---

## Audit Workflow

### Step 1: Launch Parallel Subagents

Spawn subagents for each cohesion dimension. Each subagent MUST be instructed:

> "You are conducting a thorough cohesion audit. Your output must be EXHAUSTIVE — enumerate every item, do not summarize. Return structured tables, not prose. Every finding needs a file:line reference. If you find 16 missing fields, list all 16 with their source locations. If you find 48 files with broad exception handlers, list all 48. Completeness is more important than brevity. This is a research task — DO NOT modify any code."

**Grouping** (spawn 5 subagents, dimensions grouped by relatedness):

| Subagent | Dimensions | Focus |
|----------|-----------|-------|
| 1 | C1, C4 | Structural symmetry + naming consistency (side-by-side comparison tables) |
| 2 | C2, C8 | Interface completeness + export surface (adapter/factory chain verification) |
| 3 | C3, C9 | Feature locality + error handling (file mapping + exception census) |
| 4 | C5 | Test-source alignment (enumerate EVERY source module and its test status) |
| 5 | C6, C7 | Registry completeness + config-driven behavior alignment (gap tables) |

### Step 2: Consolidate Findings

After all subagents return:

1. **Verify completeness** — if a subagent returned summaries instead of enumerations, note it as an audit gap
2. Collect findings per dimension into structured tables
3. Assign dimension scores based on the enumerated data
4. Compute overall cohesion score:
   - STRONG = 4, ADEQUATE = 3, WEAK = 2, FRACTURED = 1
   - Average across dimensions, weighted: C2 gets 2x weight (interface completeness is foundational)
5. Identify **cross-dimension patterns** — same subsystem appearing as a gap in multiple dimensions

### Step 3: Write Report

Ensure `temp/audit-cohesion/` exists (`mkdir -p`).

Write to `temp/audit-cohesion/cohesion_audit_{YYYY-MM-DD_HHMMSS}.md`.

The report WILL be long. This is expected and correct — thoroughness over brevity.

If report exceeds 500 lines, split into parts at natural dimension boundaries:
- `_scorecard.md` — scorecard, cross-dimension patterns, recommended focus areas
- `_c1_c4.md` — dimensions C1 through C4 with full tables
- `_c5_c9.md` — dimensions C5 through C9 with full tables

Each part must reference the other parts by filename.

### Step 4: Output Summary to Terminal

Display:
- Overall cohesion score (numeric + label)
- Per-dimension score table
- Top 5 most impactful findings (with file:line)
- Report file path(s)

---

## Report Structure

Each dimension section in the report MUST follow this structure:

```markdown
## C{N}: {Dimension Name}

### Score: {STRONG|ADEQUATE|WEAK|FRACTURED}

### Methodology
- Directories examined: {list}
- Items checked: {count}
- Tools used: {grep patterns, glob patterns}

### Findings

#### {Finding Category 1}

| {Column Headers Appropriate to Finding} |
|---|
| {One row per item — EVERY item, not a sample} |

#### {Finding Category 2}
{... same pattern ...}

### Compliant Patterns
- {file:line} — {what's working well and why}

### Remediation Checklist
- [ ] {Specific action item with file path}
- [ ] {Next action item}
```

---

## Exclusions

Do NOT flag:
- Generated files (migrations, schema DDL)
- Third-party vendored code
- Test fixtures and cached responses
- Temporary/debug files in `temp/`
- Configuration template files in `config/`

---

## Score Guidelines

**STRONG:** Components fit together cleanly. Patterns are consistent, interfaces are complete. No action needed.

**ADEQUATE:** Minor gaps or inconsistencies that don't impede development. Low-priority cleanup opportunities.

**WEAK:** Noticeable friction when working across components. Developers need tribal knowledge to navigate inconsistencies. Should be addressed in next refactor cycle.

**FRACTURED:** Components don't fit together. Patterns are inconsistent, interfaces have gaps. Active impediment to development. Requires dedicated remediation effort.
