---
name: audit-cohesion
categories: [audit]
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

**The report must be plan-ready.** Every finding must contain enough detail that a `/autoskillit:make-plan` invocation can act on it without re-investigating the codebase.

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

| Directory/File | Planner Has? | Executor Has? | Symmetric? | Notes |
|---------------|-------------|--------------|------------|-------|
| `nodes/` | Yes | Yes | Yes | — |
| `checkpointer.py` | Yes (single file) | Yes (directory/) | NO | Naming: PlannerCheckpointer vs HybridCheckpointer |

List ALL directories and key files, not just divergent ones.

2. **Repository pattern comparison** — for each repository, verify:

| Repository | Extends Base? | Has Interface? | Has Factory Method? | Method Pattern |
|-----------|--------------|---------------|--------------------|--------------|

3. **Node implementation comparison** — for each node pattern:

| Pattern | Planner Implementation | Executor Implementation | Consistent? |
|---------|----------------------|------------------------|-------------|
| Worker dispatch | Send API via prep node | Send API via prep node | Yes |
| State wrapper | StatePropagatingWrapper | ... | ... |

4. **Prompt template comparison:**

| Template Type | Planner Path | Executor Path | Shared Partials | Divergence |
|--------------|-------------|--------------|----------------|-----------|

---

### C2: Interface Completeness

**Question:** Are adapter, factory, and contract chains complete with no missing links?

**Audit Strategy:**

1. **Adapter field coverage** — for each graph state field, verify adapter mapping:

| State Field | In PersistenceAdapter? | Database Column | Bidirectional? |
|------------|----------------------|----------------|---------------|

2. **Factory method coverage** — for each table model, verify factory access:

| Table Model | Has Repository? | Has Factory Method? | Factory Method Name |
|------------|----------------|--------------------|--------------------|

3. **Contract test inventory** — for each interface, verify contract exists:

| Interface | Contract Test File | Tests Count | Full Surface Covered? |
|-----------|-------------------|-------------|---------------------|

4. **Type boundary audit** — find every place SQLModel instances cross boundaries:

| Location (file:line) | SQLModel Type | Destination | Violation? |
|---------------------|--------------|------------|-----------|

---

### C3: Feature Locality

**Question:** Is related functionality co-located, or scattered across unrelated packages?

**Audit Strategy:**

1. **Feature file map** — for each major feature, enumerate ALL participating files:

| Feature | File Path | Role in Feature | Package |
|---------|----------|----------------|---------|
| Checkpointing | `agents/graph/planner/checkpointer.py` | Planner checkpointing | agents |
| Checkpointing | `agents/graph/executor/checkpointer/checkpointer.py` | Executor checkpointing | agents |
| Checkpointing | `packages/sdk/graph/checkpointer.py` | Base abstraction | sdk |

Audit at minimum: checkpointing, work package execution, plan compilation, canvas sync, test framework detection.

2. **SDK utility audit** — for each SDK module, count its importers by package:

| SDK Module | Total Importers | Planner-Only | Executor-Only | Shared | Verdict |
|-----------|----------------|-------------|--------------|--------|---------|
| `sdk/execution/executor_scope.py` | 8 | 0 | 8 | 0 | Misplaced — executor-only |

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
| `*Checkpointer` | 2 | PlannerCheckpointer, HybridCheckpointer | Mixed naming strategy |

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
| `agents/graph/executor/nodes/execute/worker.py` | `tests/agents/graph/executor/nodes/test_worker.py` | Yes | 12 |
| `packages/sdk/code_intelligence/lens.py` | — | NO | 0 |

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

**Question:** Are all registries internally consistent and complete?

**Audit Strategy:**

1. **Field registry gap analysis** — compare state schema fields vs registry:

| Field Name | In State Schema? | In Field Registry? | Lifecycle Category | Source File:Line |
|-----------|-----------------|-------------------|-------------------|-----------------|
| `session_started_at` | Yes (`unified_state.py:42`) | NO | — | Missing |

List EVERY missing field.

2. **Phase registry audit:**

| Phase | In Registry? | Hardcoded Elsewhere? | Location of Hardcode |
|-------|-------------|---------------------|---------------------|

3. **Role registry vs prompt template audit:**

| Role | In Registry? | Has Prompt Template? | Template Path | Gap |
|------|-------------|---------------------|--------------|-----|
| Provider | Yes | NO | — | Missing `provider_guidance.j2` |

4. **DevToolRegistry audit:**

| Tool | In Registry? | In pyproject.toml? | In pre-commit? | Gap |
|------|-------------|-------------------|---------------|-----|

---

### C7: Prompt-Agent Alignment

**Question:** Do prompt templates match the agents and nodes that consume them?

**Audit Strategy:**

1. **Template-consumer mapping** — for EVERY template file, find its consumer:

| Template File | Consumer (renderer method or node) | Variables Expected | Variables Provided | Gap |
|--------------|----------------------------------|-------------------|-------------------|-----|

2. **Dead template detection:**

| Template File | Any Consumer Found? | Last Modified |
|--------------|-------------------|--------------|

3. **Shared partial audit:**

| Partial File | Used by Planner? | Used by Executor? | Truly Shared? |
|-------------|-----------------|------------------|--------------|

4. **Inline prompt detection** — nodes that bypass the template system:

| Node File:Line | Prompt Construction | Should Use Template? |
|---------------|--------------------|--------------------|

---

### C8: Export Surface Coherence

**Question:** Are `__init__.py` exports consistent, complete, and intentional?

**Audit Strategy:**

1. **Symbol accessibility audit** — for key public symbols, check import depth:

| Symbol | Shallow Import (`from packages.X import Y`) | Deep Import Required? | Consumer Count |
|--------|---------------------------------------------|---------------------|---------------|
| `Plan` | Yes | No | 45 |
| `ExecutorGraphState` | No | `from packages.schema.state.executor_state import ...` | 23 |

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

| Error Field | In Planner State? | In Executor State? | Same Semantics? |
|------------|-------------------|-------------------|----------------|

3. **Broad exception handler census** — list EVERY `except Exception` or `except BaseException`:

| File:Line | Exception Caught | Handler Action | Justified? |
|-----------|-----------------|----------------|-----------|

4. **Logger initialization audit:**

| File | Logger Pattern | Consistent? |
|------|--------------|-------------|

---

## Audit Workflow

### Step 0: Initialize Code Index

```
mcp__code-index__set_project_path(path="{PROJECT_ROOT}")
```

### Step 1: Launch Parallel Subagents

Spawn subagents for each cohesion dimension. Each subagent MUST be instructed:

> "You are conducting a thorough cohesion audit. Your output must be EXHAUSTIVE — enumerate every item, do not summarize. Return structured tables, not prose. Every finding needs a file:line reference. If you find 16 missing fields, list all 16 with their source locations. If you find 48 files with broad exception handlers, list all 48. Completeness is more important than brevity. This is a research task — DO NOT modify any code."

**Grouping** (spawn 5 subagents, one dimension each or grouped by relatedness):

| Subagent | Dimensions | Focus |
|----------|-----------|-------|
| 1 | C1, C4 | Structural symmetry + naming consistency (side-by-side comparison tables) |
| 2 | C2, C8 | Interface completeness + export surface (adapter/factory chain verification) |
| 3 | C3, C9 | Feature locality + error handling (file mapping + exception census) |
| 4 | C5 | Test-source alignment (enumerate EVERY source module and its test status) |
| 5 | C6, C7 | Registration completeness + prompt-agent alignment (registry gap tables) |

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

Write to `temp/audit-cohesion/cohesion_audit_{YYYY-MM-DD_HHMMSS}.md`. (relative to the current working directory)

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
- Generated files (Alembic migrations, PowerSync DDL)
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