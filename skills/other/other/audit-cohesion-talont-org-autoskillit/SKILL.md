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
- Final report: `temp/audit-cohesion/cohesion_audit_{YYYY-MM-DD_HHMMSS}.md` — always one file, never split
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

3. **Node implementation comparison** — for each node pattern:

| Pattern | Module A Implementation | Module B Implementation | Consistent? |
|---------|----------------------|------------------------|-------------|
| Request dispatch | Send via handler chain | Send via handler chain | Yes |
| State wrapper | StateManager | ... | ... |

4. **Prompt template comparison:**

| Template Type | Module A Path | Module B Path | Shared Partials | Divergence |
|--------------|-------------|--------------|----------------|-----------|

---

### C2: Interface Completeness

**Question:** Are Protocol/ABC contracts complete — every interface fully implemented, every DI slot wired?

**Audit Strategy:**

1. **Protocol → concrete implementation mapping** — find every `Protocol` and `ABC` class, then find its concrete implementation(s):

| Protocol/ABC | File:Line | Methods Defined | Concrete Implementation | Impl File:Line | All Methods Implemented? |
|---|---|---|---|---|---|

Flag any protocol with zero implementations, or any concrete class missing an abstract method.

2. **DI container field population** — for the main dependency injection container(s), compare declared fields vs factory wiring:

| Field | Type | Optional? | Wired in Factory? | Factory Value | Notes |
|---|---|---|---|---|---|

Flag any field that is declared but not populated in the composition root factory.

3. **Abstract method coverage** — for ABC hierarchies with multiple levels (base → sub-ABC → concrete), verify each concrete class implements all inherited abstract methods:

| Concrete Class | Inherits From | Abstract Methods Required | Methods Implemented | Complete? |
|---|---|---|---|---|

4. **Factory function completeness** — for each factory/builder pattern:

| Factory Function | File:Line | Returns | All Fields Populated? | Stale Comments? |
|---|---|---|---|---|

Flag any factory whose docstring or inline comments claim a different field count than the actual implementation.

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

2. **SDK utility audit** — for each SDK module, count its importers by package:

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

2. **Method verb audit** — for each verb used in repository/node methods:

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

### C6: Registration Completeness

**Question:** Are all registries internally consistent and complete — every registered entry has an implementation, every implementation is registered?

**Audit Strategy:**

1. **MCP tool registry completeness** — find the gate frozensets (`GATED_TOOLS`, `UNGATED_TOOLS`) and cross-reference every tool name against handler functions and documentation:

| Tool Name | In Gate Frozenset (which) | Handler Function | Handler File:Line | @app.tool() registered? | In CLAUDE.md? | Notes |
|---|---|---|---|---|---|---|

Flag any tool in the frozenset without a handler, any handler not in the frozenset, and any CLAUDE.md attribution to the wrong file.

2. **Decorator-based rule registry** — for `@semantic_rule` (or equivalent auto-registration decorator) find all decorated functions vs all emitted finding IDs:

| Decorator `name=` | Registered Under | Emitted Finding IDs | Mismatch? |
|---|---|---|---|

Flag cases where one decorated function emits findings under different IDs than the one it is registered under.

3. **CLI command registration** — enumerate all `@app.command()` (or equivalent) decorators and cross-reference against documentation:

| Command | Registered at File:Line | Documented? | Notes |
|---|---|---|---|

Flag commands registered in code but absent from CLAUDE.md.

4. **Skill/plugin registry completeness** — count skill directories (those with `SKILL.md`) and verify count matches documented claim:

| Skill Directory | Has SKILL.md? | Listed in CLAUDE.md? | Name Match? |
|---|---|---|---|

---

### C7: Recipe-to-Skill Coherence

**Question:** Are pipeline recipe YAML definitions internally consistent — do all external references (skills, tools, Python callables, capture keys) resolve?

**Audit Strategy:**

1. **Skill reference resolution** — for every `run_skill` step in every recipe, verify the `skill_command` resolves to an existing skill:

| Recipe | Step Name | Skill Command | Is Dynamic (`${{...}}`)? | Skill Directory Exists? | Has SKILL.md? |
|---|---|---|---|---|---|

Flag any static reference that does not resolve. Flag dynamic references as unverifiable and note the input variable that controls them.

2. **Tool name validity** — for every step that specifies a tool type (`run_cmd`, `run_skill`, `run_python`, etc.), verify the tool name appears in the registry (GATED_TOOLS or UNGATED_TOOLS):

| Recipe | Step Name | Tool Name | In Registry? |
|---|---|---|---|

3. **Python callable resolution** — for every `run_python` step, verify the dotted module path and function name resolve to an importable callable:

| Recipe | Step Name | Module Path | Function Name | Module Importable? | Function Exists? |
|---|---|---|---|---|---|

4. **Capture key coherence** — for every `${{ captures.X }}` reference in a recipe step (in `skill_command`, `cwd`, `python_args`, etc.), verify that key `X` was declared as a `capture_key` in an upstream step:

| Recipe | Step Name | References `captures.X` | X Defined Upstream? | Defining Step |
|---|---|---|---|---|

Flag forward references (using a key before the step that defines it) and phantom references (key never defined).

---

### C8: Export Surface Coherence

**Question:** Are `__init__.py` exports consistent, complete, and intentional?

**Audit Strategy:**

1. **Symbol accessibility audit** — for key public symbols, check import depth:

| Symbol | Shallow Import (`from lib.X import Y`) | Deep Import Required? | Consumer Count |
|--------|---------------------------------------------|---------------------|---------------|
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

| Exception Class | Base Class | Defined In | Used In (files) | Agent-Specific? |
|----------------|-----------|-----------|----------------|----------------|

Flag duplicates (same name in different agents).

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

### C10: Documentation-Code Alignment

**Question:** Does the project's primary architectural documentation (CLAUDE.md) accurately describe the actual code — no stale attributions, wrong names, or missing entries?

This dimension is distinct from audit-arch (which checks rule violations) and from C6 (which checks registry completeness). C10 checks whether PROSE DOCUMENTATION matches CODE REALITY. In this repo, CLAUDE.md is loaded as context in every Claude Code session, so inaccuracies there are directly load-bearing: a wrong file attribution misleads every investigation that uses CLAUDE.md as a starting point.

**Audit Strategy:**

1. **Tool-to-file attribution** — for every tool listed in the CLAUDE.md MCP tools table or server module descriptions, verify the documented handler file matches the actual location:

| Tool Name | CLAUDE.md Claims File | Actual Handler File:Line | Match? |
|---|---|---|---|

2. **`__init__.py` re-export descriptions** — for every sub-package whose CLAUDE.md description mentions re-exported symbols, verify the named symbols actually appear in that package's `__all__`:

| Sub-package | CLAUDE.md States Exports | Actual `__all__` | Missing from Docs | Wrong Names |
|---|---|---|---|---|

3. **Test file listing accuracy** — compare the `tests/` section of CLAUDE.md against actual test files on disk:

| Test File (CLAUDE.md) | Exists on Disk? | | Test File (on disk) | In CLAUDE.md? |
|---|---|---|---|---|

Flag files listed in CLAUDE.md that do not exist, and files on disk not listed in CLAUDE.md.

4. **Key Components description accuracy** — for each module entry in CLAUDE.md's Key Components section, verify:
   - The described functions/classes actually exist at the stated location
   - The described public API matches the actual function signatures (param names, return types)
   - Any numeric claims (e.g., "7 checks", "15 gated tools") match the actual count in code

| CLAUDE.md Claim | File:Line | Verified? | Actual |
|---|---|---|---|

---

## Audit Workflow

### Step 0: Initialize Code Index

```
mcp__code-index__set_project_path(path="{PROJECT_ROOT}")
```

### Step 1: Launch Parallel Subagents

Spawn subagents for each cohesion dimension. Each subagent MUST be instructed:

> "You are conducting a thorough cohesion audit. Your output must be EXHAUSTIVE — enumerate every item, do not summarize. Return structured tables, not prose. Every finding needs a file:line reference. If you find 16 missing fields, list all 16 with their source locations. If you find 48 files with broad exception handlers, list all 48. Completeness is more important than brevity. This is a research task — DO NOT modify any code."

**Grouping** (spawn 6 subagents, one dimension each or grouped by relatedness):

| Subagent | Dimensions | Focus |
|----------|-----------|-------|
| 1 | C1, C4 | Structural symmetry + naming consistency (side-by-side comparison tables) |
| 2 | C2, C8 | Interface completeness + export surface (Protocol/DI audit + __init__ gaps) |
| 3 | C3, C9 | Feature locality + error handling (file mapping + exception census) |
| 4 | C5, C10 | Test-source alignment + documentation-code alignment (enumerate EVERY source module, cross-reference CLAUDE.md) |
| 5 | C6, C7 | Registration completeness + recipe-to-skill coherence (registry gap tables + YAML reference resolution) |

### Step 2: Consolidate Findings

After all subagents return:

1. **Verify completeness** — if a subagent returned summaries instead of enumerations, note it as an audit gap
2. Collect findings per dimension into structured tables
3. Assign dimension scores based on the enumerated data
4. Compute overall cohesion score:
   - STRONG = 4, ADEQUATE = 3, WEAK = 2, FRACTURED = 1
   - Average across dimensions, weighted: C2 gets 2x weight (interface completeness is foundational), C10 gets 2x weight (documentation drift is load-bearing in a Claude Code context repo)
5. Identify **cross-dimension patterns** — same subsystem appearing as a gap in multiple dimensions

### Step 3: Write Report

Ensure `temp/audit-cohesion/` exists (`mkdir -p`).

Write to `temp/audit-cohesion/cohesion_audit_{YYYY-MM-DD_HHMMSS}.md` — **always one file, never split**.

The report WILL be long. This is expected and correct — thoroughness over brevity. Do not reduce content to stay under any line count.

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
- Test fixtures and cached LLM responses
- Temporary/debug files in `temp/`
- Configuration template files in `config/`

---

## Score Guidelines

**STRONG:** Components fit together cleanly. Patterns are consistent, interfaces are complete. No action needed.

**ADEQUATE:** Minor gaps or inconsistencies that don't impede development. Low-priority cleanup opportunities.

**WEAK:** Noticeable friction when working across components. Developers need tribal knowledge to navigate inconsistencies. Should be addressed in next refactor cycle.

**FRACTURED:** Components don't fit together. Patterns are inconsistent, interfaces have gaps. Active impediment to development. Requires dedicated remediation effort.
