---
name: ln-624-code-quality-auditor
description: Code quality audit worker (L3). Checks cyclomatic complexity, deep nesting, long methods, god classes, O(n²) algorithms, N+1 queries, magic numbers, decentralized constants, duplicate constants. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Quality Auditor (L3 Worker)

Specialized worker auditing code complexity, algorithms, and constants management.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline** - invoked by ln-620-codebase-auditor
- Audit **code quality** (Categories 5+6+NEW: Medium Priority)
- Check complexity metrics, algorithmic efficiency, constants management
- Return structured findings with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Code Quality category

## Inputs (from Coordinator)

Receives `contextStore` with:
- `tech_stack` - detected tech stack (languages, frameworks)
- `best_practices` - researched best practices from MCP
- `principles` - project-specific principles from docs/principles.md
- `codebase_root` - root path of codebase

**Domain-aware fields (NEW):**
- `domain_mode`: `"domain-aware"` | `"global"` (optional, defaults to "global")
- `current_domain`: `{name, path}` when domain_mode="domain-aware"

**Example contextStore (domain-aware):**
```json
{
  "tech_stack": {...},
  "best_practices": {...},
  "principles": {...},
  "codebase_root": "/project",
  "domain_mode": "domain-aware",
  "current_domain": {
    "name": "orders",
    "path": "src/orders"
  }
}
```

## Workflow

1) **Parse context from contextStore**
   - Extract tech_stack, best_practices, principles
   - **Determine scan_path (NEW):**
     ```
     IF domain_mode == "domain-aware":
       scan_path = codebase_root + "/" + current_domain.path
       domain_name = current_domain.name
     ELSE:
       scan_path = codebase_root
       domain_name = null
     ```

2) **Scan codebase for violations**
   - All Grep/Glob patterns use `scan_path` (not codebase_root)
   - Example: `Grep(pattern="if.*if.*if", path=scan_path)` for nesting detection

3) **Collect findings with severity, location, effort, recommendation**
   - Tag each finding with `domain: domain_name` (if domain-aware)

4) **Calculate score using penalty algorithm**

5) **Return JSON result to coordinator**
   - Include `domain` and `scan_path` fields (if domain-aware)

## Audit Rules (Priority: MEDIUM)

### 1. Cyclomatic Complexity
**What:** Too many decision points in single function (> 10)

**Detection:**
- Count if/else, switch/case, ternary, &&, ||, for, while
- Use tools: `eslint-plugin-complexity`, `radon` (Python), `gocyclo` (Go)

**Severity:**
- **HIGH:** Complexity > 20 (extremely hard to test)
- **MEDIUM:** Complexity 11-20 (refactor recommended)
- **LOW:** Complexity 8-10 (acceptable but monitor)

**Recommendation:** Split function, extract helper methods, use early returns

**Effort:** M-L (depends on complexity)

### 2. Deep Nesting (> 4 levels)
**What:** Nested if/for/while blocks too deep

**Detection:**
- Count indentation levels
- Pattern: if { if { if { if { if { ... } } } } }

**Severity:**
- **HIGH:** > 6 levels (unreadable)
- **MEDIUM:** 5-6 levels
- **LOW:** 4 levels

**Recommendation:** Extract functions, use guard clauses, invert conditions

**Effort:** M (refactor structure)

### 3. Long Methods (> 50 lines)
**What:** Functions too long, doing too much

**Detection:**
- Count lines between function start and end
- Exclude comments, blank lines

**Severity:**
- **HIGH:** > 100 lines
- **MEDIUM:** 51-100 lines
- **LOW:** 40-50 lines (borderline)

**Recommendation:** Split into smaller functions, apply Single Responsibility

**Effort:** M (extract logic)

### 4. God Classes/Modules (> 500 lines)
**What:** Files with too many responsibilities

**Detection:**
- Count lines in file (exclude comments)
- Check number of public methods/functions

**Severity:**
- **HIGH:** > 1000 lines
- **MEDIUM:** 501-1000 lines
- **LOW:** 400-500 lines

**Recommendation:** Split into multiple files, apply separation of concerns

**Effort:** L (major refactor)

### 5. Too Many Parameters (> 5)
**What:** Functions with excessive parameters

**Detection:**
- Count function parameters
- Check constructors, methods

**Severity:**
- **MEDIUM:** 6-8 parameters
- **LOW:** 5 parameters (borderline)

**Recommendation:** Use parameter object, builder pattern, default parameters

**Effort:** S-M (refactor signature + calls)

### 6. O(n²) or Worse Algorithms
**What:** Inefficient nested loops over collections

**Detection:**
- Nested for loops: `for (i) { for (j) { ... } }`
- Nested array methods: `arr.map(x => arr.filter(...))`

**Severity:**
- **HIGH:** O(n²) in hot path (API request handler)
- **MEDIUM:** O(n²) in occasional operations
- **LOW:** O(n²) on small datasets (n < 100)

**Recommendation:** Use hash maps, optimize with single pass, use better data structures

**Effort:** M (algorithm redesign)

### 7. N+1 Query Patterns
**What:** ORM lazy loading causing N+1 queries

**Detection:**
- Find loops with database queries inside
- Check ORM patterns: `users.forEach(u => u.getPosts())`

**Severity:**
- **CRITICAL:** N+1 in API endpoint (performance disaster)
- **HIGH:** N+1 in frequent operations
- **MEDIUM:** N+1 in admin panel

**Recommendation:** Use eager loading, batch queries, JOIN

**Effort:** M (change ORM query)

### 8. Constants Management (NEW)
**What:** Magic numbers/strings, decentralized constants, duplicates

**Detection:**

| Issue | Pattern | Example |
|-------|---------|---------|
| Magic numbers | Hardcoded numbers in conditions/calculations | `if (status === 2)` |
| Magic strings | Hardcoded strings in comparisons | `if (role === 'admin')` |
| Decentralized | Constants scattered across files | `MAX_SIZE = 100` in 5 files |
| Duplicates | Same value multiple times | `STATUS_ACTIVE = 1` in 3 places |
| No central file | Missing `constants.ts` or `config.py` | No single source of truth |

**Severity:**
- **HIGH:** Magic numbers in business logic (payment amounts, statuses)
- **MEDIUM:** Duplicate constants (same value defined 3+ times)
- **MEDIUM:** No central constants file
- **LOW:** Magic strings in logging/debugging

**Recommendation:**
- Create central constants file (`constants.ts`, `config.py`, `constants.go`)
- Extract magic numbers to named constants: `const STATUS_ACTIVE = 1`
- Consolidate duplicates, import from central file
- Use enums for related constants

**Effort:** M (extract constants, update imports, consolidate)

## Scoring Algorithm

```
penalty = (critical * 2.0) + (high * 1.0) + (medium * 0.5) + (low * 0.2)
score = max(0, 10 - penalty)
```

## Output Format

Return JSON to coordinator:

**Global mode output:**
```json
{
  "category": "Code Quality",
  "score": 6,
  "total_issues": 12,
  "critical": 1,
  "high": 3,
  "medium": 5,
  "low": 3,
  "findings": [...]
}
```

**Domain-aware mode output (NEW):**
```json
{
  "category": "Code Quality",
  "score": 7,
  "domain": "orders",
  "scan_path": "src/orders",
  "total_issues": 8,
  "critical": 0,
  "high": 2,
  "medium": 4,
  "low": 2,
  "findings": [
    {
      "severity": "HIGH",
      "location": "src/orders/services/OrderService.ts:120",
      "issue": "Cyclomatic complexity 22 (threshold: 10)",
      "principle": "Code Complexity / Maintainability",
      "recommendation": "Split into smaller methods",
      "effort": "M",
      "domain": "orders"
    },
    {
      "severity": "MEDIUM",
      "location": "src/orders/controllers/OrderController.ts:45",
      "issue": "Magic number '3' used for order status",
      "principle": "Constants Management",
      "recommendation": "Extract: const ORDER_STATUS_SHIPPED = 3",
      "effort": "S",
      "domain": "orders"
    }
  ]
}
```

## Critical Rules

- **Do not auto-fix:** Report only
- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path` (not entire codebase)
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Context-aware:** Small functions (n < 100) with O(n²) may be acceptable
- **Constants detection:** Exclude test files, configs, examples
- **Metrics tools:** Use existing tools when available (ESLint complexity plugin, radon, gocyclo)

## Definition of Done

- contextStore parsed (including domain_mode and current_domain)
- scan_path determined (domain path or codebase root)
- All 8 checks completed (scoped to scan_path):
  - complexity, nesting, length, god classes, parameters, O(n²), N+1, constants
- Findings collected with severity, location, effort, recommendation, domain
- Score calculated
- JSON returned to coordinator with domain metadata

## Reference Files

- Code quality rules: [references/code_quality_rules.md](references/code_quality_rules.md)

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
