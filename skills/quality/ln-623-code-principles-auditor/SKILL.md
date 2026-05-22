---
name: ln-623-code-principles-auditor
description: Code principles audit worker (L3). Checks DRY (7 types), KISS/YAGNI, TODOs, error handling, DI patterns. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Principles Auditor (L3 Worker)

Specialized worker auditing code principles (DRY, KISS, YAGNI) and design patterns.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline** - invoked by ln-620-codebase-auditor
- Audit **code principles** (DRY/KISS/YAGNI, error handling, DI)
- Check DRY/KISS/YAGNI violations, TODO/FIXME, workarounds, error handling
- Return structured findings with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Code Principles category

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
    "name": "users",
    "path": "src/users"
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
   - Example: `Grep(pattern="TODO", path=scan_path)`

3) **Collect findings with severity, location, effort, recommendation**
   - Tag each finding with `domain: domain_name` (if domain-aware)

4) **Calculate score using penalty algorithm**

5) **Return JSON result to coordinator**
   - Include `domain` and `scan_path` fields (if domain-aware)

## Audit Rules (Priority: HIGH)

### 1. DRY Violations (Don't Repeat Yourself)
**What:** Duplicated logic, constants, or code blocks across files

**Detection Categories:**

#### 1.1. Identical Code Duplication
- Search for identical functions (use AST comparison or text similarity)
- Find repeated constants: same value defined in multiple files
- Detect copy-pasted code blocks (>10 lines identical)

**Severity:**
- **HIGH:** Critical business logic duplicated (payment, auth)
- **MEDIUM:** Utility functions duplicated
- **LOW:** Simple constants duplicated (<5 occurrences)

#### 1.2. Duplicated Validation Logic
**What:** Same validation patterns repeated across validators/controllers

**Detection:**
- Email validation: `/@.*\./` regex patterns in multiple files
- Password validation: `/.{8,}/`, strength checks repeated
- Phone validation: phone number regex duplicated
- Common patterns: `isValid*`, `validate*`, `check*` functions with similar logic

**Severity:**
- **HIGH:** Auth/payment validation duplicated (inconsistency risk)
- **MEDIUM:** User input validation duplicated (3+ occurrences)
- **LOW:** Simple format checks duplicated (<3 occurrences)

**Recommendation:** Extract to shared validators module (`validators/common.ts`)

**Effort:** M (extract validators, update imports)

#### 1.3. Repeated Error Messages
**What:** Hardcoded error messages instead of centralized error catalog

**Detection:**
- Grep for hardcoded strings in `throw new Error("...")`, `res.status(400).json({ error: "..." })`
- Find repeated messages: "User not found", "Invalid credentials", "Unauthorized access"
- Check for missing error constants file: `errors.ts`, `error-messages.ts`, `constants/errors.ts`

**Severity:**
- **MEDIUM:** Critical error messages hardcoded (auth, payment) - inconsistency risk
- **MEDIUM:** No centralized error messages file
- **LOW:** Same error message in <3 places

**Recommendation:**
- Create central error messages file (`constants/error-messages.ts`)
- Define error catalog: `const ERRORS = { USER_NOT_FOUND: "User not found", ... }`
- Replace hardcoded strings with constants: `throw new Error(ERRORS.USER_NOT_FOUND)`

**Effort:** M (create error catalog, replace hardcoded strings)

#### 1.4. Similar Code Patterns (>80% Similarity)
**What:** Code with similar logic but different variable names/structure

**Detection:**
- Use fuzzy matching/similarity algorithms (Levenshtein distance, Jaccard similarity)
- Compare function bodies ignoring variable names
- Threshold: >80% similarity = potential duplication

**Example:**
```typescript
// File 1
function processUser(user) { return user.name.toUpperCase(); }

// File 2
function formatUserName(u) { return u.name.toUpperCase(); }
// ✅ Same logic, different names - DETECTED
```

**Severity:**
- **MEDIUM:** Similar business logic (>80% similarity) in critical paths
- **LOW:** Similar utility functions (<3 occurrences)

**Recommendation:** Extract common logic, create shared helper function

**Effort:** M (refactor to shared module)

#### 1.5. Duplicated SQL Queries
**What:** Same SQL queries/ORM calls in different controllers/services

**Detection:**
- Find repeated raw SQL strings: `SELECT * FROM users WHERE id = ?`
- ORM duplicates: `User.findOne({ where: { email } })` in multiple files
- Grep for common patterns: `SELECT`, `INSERT`, `UPDATE`, `DELETE` with similar structure

**Severity:**
- **HIGH:** Critical queries duplicated (payment, auth)
- **MEDIUM:** Common queries duplicated (3+ occurrences)
- **LOW:** Simple queries duplicated (<3 occurrences)

**Recommendation:** Extract to Repository layer, create query methods

**Effort:** M (create repository methods, update callers)

#### 1.6. Copy-Pasted Tests
**What:** Test files with identical structure (arrange-act-assert duplicated)

**Detection:**
- Find tests with >80% similar setup/teardown
- Repeated test data: same fixtures defined in multiple test files
- Pattern: `beforeEach`, `afterEach` with identical code

**Severity:**
- **MEDIUM:** Test setup duplicated in 5+ files
- **LOW:** Similar test utilities duplicated (<5 files)

**Recommendation:** Extract to test helpers (`tests/helpers/*`), use shared fixtures

**Effort:** M (create test utilities, refactor tests)

#### 1.7. Repeated API Response Structures
**What:** Duplicated response objects instead of shared DTOs

**Detection:**
- Find repeated object structures in API responses:
  ```typescript
  return { id: user.id, name: user.name, email: user.email }
  ```
- Check for missing DTOs folder: `dtos/`, `responses/`, `models/`
- Grep for common patterns: `return { ... }` in controllers

**Severity:**
- **MEDIUM:** Response structures duplicated in 5+ endpoints (inconsistency risk)
- **LOW:** Simple response objects duplicated (<5 endpoints)

**Recommendation:** Create DTOs/Response classes, use serializers

**Effort:** M (create DTOs, update endpoints)

---

**Overall Recommendation for DRY:**
Extract to shared module, create utility function, centralize constants/messages/validators/DTOs

**Overall Effort:** M (refactor + update imports, typically 1-4 hours per duplication type)

### 2. KISS Violations (Keep It Simple, Stupid)
**What:** Over-engineered abstractions, unnecessary complexity

**Detection:**
- Abstract classes with single implementation
- Factory patterns for 2 objects
- Deep inheritance (>3 levels)
- Generic types with excessive constraints

**Severity:**
- **HIGH:** Abstraction prevents understanding core logic
- **MEDIUM:** Unnecessary pattern (factory for 2 types)
- **LOW:** Over-generic types (acceptable tradeoff)

**Recommendation:** Remove abstraction, inline implementation, flatten hierarchy

**Effort:** L (requires careful refactoring)

### 3. YAGNI Violations (You Aren't Gonna Need It)
**What:** Unused extensibility, dead feature flags, premature optimization

**Detection:**
- Feature flags that are always true/false
- Abstract methods never overridden
- Config options never used
- Interfaces with single implementation (no plans for more)

**Severity:**
- **MEDIUM:** Unused extensibility points adding complexity
- **LOW:** Dead feature flags (cleanup needed)

**Recommendation:** Remove unused code, simplify interfaces

**Effort:** M (verify no future use, then delete)

### 4. TODO/FIXME/HACK Comments
**What:** Unfinished work, temporary solutions

**Detection:**
- Grep for `TODO`, `FIXME`, `HACK`, `XXX`, `OPTIMIZE`
- Check age (git blame) - old TODOs are higher severity

**Severity:**
- **HIGH:** TODO in critical path (auth, payment) >6 months old
- **MEDIUM:** FIXME/HACK with explanation
- **LOW:** Recent TODO (<1 month) with plan

**Recommendation:** Complete TODO, remove HACK, refactor workaround

**Effort:** Varies (S for simple TODO, L for architectural HACK)

### 5. Missing Error Handling
**What:** Critical paths without try-catch, error propagation

**Detection:**
- Find async functions without error handling
- Check API routes without error middleware
- Verify database calls have error handling

**Severity:**
- **CRITICAL:** Payment/auth without error handling
- **HIGH:** User-facing operations without error handling
- **MEDIUM:** Internal operations without error handling

**Recommendation:** Add try-catch, implement error middleware, propagate errors properly

**Effort:** M (add error handling logic)

### 6. Centralized Error Handling
**What:** Errors handled inconsistently across different contexts (web requests, cron jobs, background tasks)

**Detection:**
- Search for centralized error handler class/module: `ErrorHandler`, `errorHandler`, `error-handler.ts/js/py`
- Check if error middleware delegates to handler: `errorHandler.handleError(err)` or similar
- Verify all async routes use promises or async/await (Express 5+ auto-catches rejections)
- Check for error transformation (sanitize stack traces for users in production)
- **Anti-pattern check:** Look for `process.on("uncaughtException")` usage (BAD PRACTICE per Express docs)

**Severity:**
- **HIGH:** No centralized error handler (errors handled inconsistently in multiple places)
- **HIGH:** Using `uncaughtException` listener instead of proper error propagation (Express anti-pattern)
- **MEDIUM:** Error middleware handles errors directly (doesn't delegate to central handler)
- **MEDIUM:** Async routes without proper error handling (not using promises/async-await)
- **LOW:** Stack traces exposed in production responses (security/UX issue)

**Recommendation:**
- Create single ErrorHandler class/module for ALL error contexts
- Middleware should only catch and forward to ErrorHandler (delegate pattern)
- Use async/await for async routes (framework auto-forwards errors)
- Transform errors for users: hide sensitive details (stack traces, internal paths) in production
- **DO NOT use uncaughtException listeners** - use process managers (PM2, systemd) for restart instead
- For unhandled rejections: log and restart process (use supervisor, not inline handler)

**Effort:** M-L (create error handler, refactor existing middleware)

### 7. Dependency Injection / Centralized Init
**What:** Direct imports/instantiation instead of dependency injection, scattered initialization

**Detection:**
- Check for DI container usage:
  - Node.js: `inversify`, `awilix`, `tsyringe`, `typedi` packages
  - Python: `dependency_injector`, `injector` packages
  - Java: Spring `@Autowired`, `@Inject` annotations
  - .NET: Built-in DI in ASP.NET Core, `IServiceCollection`
- Grep for direct instantiations in business logic: `new SomeService()`, `new SomeRepository()`
- Check for centralized Init/Bootstrap module: `bootstrap.ts`, `init.py`, `Startup.cs`, `app.module.ts`
- Verify controllers/services receive dependencies via constructor/parameters, not direct imports

**Severity:**
- **MEDIUM:** No DI container (hard to test, tight coupling, difficult to swap implementations)
- **MEDIUM:** Direct instantiation in business logic (`new Service()` in controllers/services)
- **LOW:** Mixed DI and direct imports (inconsistent pattern)

**Recommendation:**
- Use DI container for dependency management (Inversify, Awilix, Spring, built-in .NET DI)
- Centralize initialization in Init/Bootstrap module
- Inject dependencies via constructor/parameters (dependency injection pattern)
- Never use direct instantiation for business logic classes (only for DTOs, value objects)

**Effort:** L (refactor to DI pattern, add container, update all instantiations)

### 8. Missing Best Practices Guide
**What:** No architecture/design best practices documentation for developers

**Detection:**
- Check for architecture guide files:
  - `docs/architecture.md`, `docs/best-practices.md`, `docs/design-patterns.md`
  - `ARCHITECTURE.md`, `CONTRIBUTING.md` (architecture section)
- Verify content includes: layering rules, error handling patterns, DI usage, coding conventions

**Severity:**
- **LOW:** No architecture guide (harder for new developers to understand patterns and conventions)

**Recommendation:**
- Create `docs/architecture.md` with project-specific patterns:
  - Document layering: Controller→Service→Repository→DB
  - Error handling: centralized ErrorHandler pattern
  - Dependency Injection: how to add new services/repositories
  - Coding conventions: naming, file organization, imports
- Include examples from existing codebase
- Keep framework-agnostic (principles, not specific implementations)

**Effort:** S (create markdown file, ~1-2 hours documentation)

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
  "category": "Architecture & Design",
  "score": 6,
  "total_issues": 12,
  "critical": 2,
  "high": 4,
  "medium": 4,
  "low": 2,
  "findings": [...]
}
```

**Domain-aware mode output (NEW):**
```json
{
  "category": "Architecture & Design",
  "score": 6,
  "domain": "users",
  "scan_path": "src/users",
  "total_issues": 12,
  "critical": 2,
  "high": 4,
  "medium": 4,
  "low": 2,
  "findings": [
    {
      "severity": "CRITICAL",
      "location": "src/users/controllers/UserController.ts:45",
      "issue": "Controller directly uses Repository (layer boundary break)",
      "principle": "Layer Separation (Clean Architecture)",
      "recommendation": "Create UserService, inject into controller",
      "effort": "L",
      "domain": "users"
    },
    {
      "severity": "HIGH",
      "location": "src/users/services/UserService.ts:45",
      "issue": "DRY violation - duplicate validation logic",
      "principle": "DRY Principle",
      "recommendation": "Extract to shared validators module",
      "effort": "M",
      "domain": "users"
    }
  ]
}
```

## Critical Rules

- **Do not auto-fix:** Report only
- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path` (not entire codebase)
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Context-aware:** Use project's `principles.md` to define what's acceptable
- **Age matters:** Old TODOs are higher severity than recent ones
- **Effort realism:** S = <1h, M = 1-4h, L = >4h

## Definition of Done

- contextStore parsed (including domain_mode and current_domain)
- scan_path determined (domain path or codebase root)
- All 8 checks completed (scoped to scan_path):
  - DRY (7 subcategories), KISS, YAGNI, TODOs, Error Handling, Centralized Errors, DI/Init, Best Practices Guide
- Findings collected with severity, location, effort, recommendation, domain
- Score calculated
- JSON returned to coordinator with domain metadata

## Reference Files

- Architecture rules: [references/architecture_rules.md](references/architecture_rules.md)

---
**Version:** 4.1.0
**Last Updated:** 2026-01-29
