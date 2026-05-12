# Detection Patterns for Code Principles Audit

Language-specific detection patterns for DRY/KISS/YAGNI violations. All patterns use `scan_path` as root.

## Exclusions (Skip These)

Before scanning, exclude false-positive sources:

| Exclude | Glob Pattern | Reason |
|---------|-------------|--------|
| Generated code | `dist/`, `build/`, `.next/`, `__generated__/`, `*.gen.*` | Auto-generated, not human-written |
| Lock files | `package-lock.json`, `yarn.lock`, `poetry.lock` | Package manager artifacts |
| Vendor/deps | `vendor/`, `node_modules/`, `.venv/` | Third-party code |
| Config per-env | `*.config.js`, `docker-compose.*.yml` | Intentional per-environment duplication |
| Migrations | `migrations/`, `**/migrate/*.py` | Sequential DB migrations are inherently repetitive |
| Test snapshots | `__snapshots__/`, `*.snap` | Auto-generated test output |

## DRY Violations (10 Types)

### 1.1 Identical Code Duplication

**Preferred:** Use `audit_workspace(verbosity="minimal", limit=5, clone_member_limit=3)` and inspect returned clone groups for exact matches — see `two_layer_detection.md` § Layer 1 Acceleration. Raise limits only for deliberate drill-down. Fall back to Grep patterns below when hex-graph unavailable.


**Strategy:** Find functions/methods with identical names in different files, then Read bodies to confirm duplication.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Find duplicate function names | Grep | `function\s+(\w+)\|const\s+(\w+)\s*=` (JS/TS) | Functions defined in multiple files |
| | Grep | `def\s+(\w+)\s*\(` (Python) | Same function name in different modules |
| | Grep | `func\s+(\w+)\s*\(` (Go) | Duplicate function declarations |
| | Grep | `(public\|private\|protected)\s+\w+\s+(\w+)\s*\(` (C#/Java) | Method declarations |
| 2. Cross-reference | Grep (files_with_matches) | Same function name → check if >1 file matches | Confirm multi-file duplication |
| 3. Verify bodies | Read | Read both function bodies, compare line-by-line | Confirm identical logic (not just name) |
| 4. Find repeated constants | Grep | Same literal string/number grep: `"[specific_value]"` | Constants defined in >1 file |

**Threshold:** >10 identical consecutive lines = duplication. >3 files with same constant = centralization needed.

**pattern_signature format:** `identical_{function_name}` or `identical_constant_{value_hash}`

### 1.2 Duplicated Validation Logic

**Strategy:** Grep for validation function patterns, then compare logic.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Find validators | Grep | `isValid\|validate\|check` + function declaration | All validation functions |
| 2. Email patterns | Grep | `/@\|email.*regex\|email.*pattern\|email.*match` | Email validation scattered across files |
| 3. Password patterns | Grep | `password.*length\|password.*regex\|\.{8,}\|minLength` | Password strength checks |
| 4. Phone patterns | Grep | `phone.*regex\|phone.*pattern\|\+?\d{10}` | Phone number validation |
| 5. URL patterns | Grep | `url.*regex\|https?:\/\/\|isUrl\|isURL` | URL validation |
| 6. Date patterns | Grep | `isDate\|parseDate\|dateFormat\|moment\(.*valid` | Date validation/parsing |

**Threshold:** Same validation type in 2+ files = duplication. Auth/payment validation = always HIGH.

**pattern_signature format:** `validation_{type}` (e.g., `validation_email`, `validation_password`)

### 1.3 Repeated Error Messages

**Strategy:** Grep for hardcoded strings in error contexts.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Thrown errors | Grep | `throw new Error\("` (JS/TS), `raise \w+Error\("` (Python) | Hardcoded error strings |
| 2. HTTP responses | Grep | `res\.status\(\d+\)\.json\(.*error\|message` | API error responses with hardcoded text |
| 3. Count repeats | Grep (count mode) | Exact error string from step 1-2 | Same message in multiple locations |
| 4. Check for error catalog | Glob | `**/errors.{ts,js,py}\|**/error-messages.*\|**/constants/errors.*` | Existing centralized error file |

**Threshold:** Same error string in 3+ places = violation. No error catalog file = MEDIUM.

**pattern_signature format:** `error_message_{normalized_text}` (first 30 chars, lowercase, underscored)

### 1.4 Similar Code Patterns (Structural Similarity)

**Preferred:** Use `audit_workspace(verbosity="minimal", limit=5, clone_member_limit=3)` and inspect returned clone groups for `normalized` or `near_miss` matches — see `two_layer_detection.md` § Layer 1 Acceleration. Raise limits only for deliberate drill-down. Fall back to Grep patterns below when hex-graph unavailable.


**Strategy:** Find functions with similar names/prefixes, then compare call sequences.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Group by prefix | Grep | `process\w+\|handle\w+\|create\w+\|update\w+\|delete\w+\|get\w+` | Functions with similar naming patterns |
| 2. Read function bodies | Read | Functions from step 1, read ~30 lines each | Full function content |
| 3. Compare structure | Manual | Count: if-statements, method calls, return patterns | Structural similarity indicators |

**Similarity indicators (check at least 3):**
- Same sequence of method calls (e.g., both call `validate → transform → save`)
- Same control flow structure (same number of if/else branches)
- Same error handling pattern (try-catch wrapping same operations)
- Same parameter count and types
- Different only in entity name (processUser vs processOrder with same logic)

**Threshold:** 3+ matching indicators = similar pattern. Report as potential extraction candidate.

**pattern_signature format:** `similar_{prefix}_{call_sequence_hash}`

### 1.5 Duplicated SQL Queries

**Strategy:** Grep for SQL keywords and ORM patterns, group by similarity.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Raw SQL | Grep | `SELECT\s+.*\s+FROM\|INSERT\s+INTO\|UPDATE\s+\w+\s+SET\|DELETE\s+FROM` | Raw SQL strings |
| 2. ORM findOne/findMany | Grep | `\.findOne\(\|\.findMany\(\|\.find\(\{.*where\|\.filter\(` (JS/TS ORMs) | Repeated ORM queries |
| 3. Django ORM | Grep | `\.objects\.filter\(\|\.objects\.get\(\|\.objects\.exclude\(` (Python) | Django query patterns |
| 4. LINQ / EF | Grep | `\.Where\(\|\.FirstOrDefault\(\|\.SingleOrDefault\(` (C#) | Entity Framework queries |
| 5. Cross-reference | Compare | Same table + same WHERE conditions in >1 file | Identical query logic |

**Threshold:** Same query pattern in 2+ services = extraction to Repository layer.

**pattern_signature format:** `sql_{table}_{operation}_{where_columns}`

### 1.6 Copy-Pasted Tests

**Strategy:** Find repeated test setup/teardown and fixture data.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Setup blocks | Grep | `beforeEach\|beforeAll\|setUp\|@Before\|SetUp` | Test setup functions |
| 2. Teardown blocks | Grep | `afterEach\|afterAll\|tearDown\|@After\|TearDown` | Test teardown functions |
| 3. Fixture data | Grep | `const mock\|const fake\|const stub\|factory\.\|faker\.` | Test data creation |
| 4. Read & compare | Read | Read setup blocks from multiple test files | Compare for identical logic |

**Threshold:** Identical setup in 5+ test files = extract to test helpers. Same fixture data in 3+ files = create shared fixtures.

**pattern_signature format:** `test_setup_{hash}` or `test_fixture_{entity}`

### 1.7 Repeated API Response Structures

**Strategy:** Find return statements in controllers/handlers building response objects.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Response objects | Grep | `return\s*\{.*id.*name\|res\.json\(\{` (JS/TS) | Inline response construction |
| 2. Serializers | Grep | `to_dict\|as_dict\|serialize\|toJSON` (Python/JS) | Custom serialization methods |
| 3. Missing DTOs | Glob | `**/dto/**\|**/dtos/**\|**/responses/**` | Check if DTO layer exists |
| 4. Compare structures | Read | Read response objects from controllers | Same field sets = duplication |

**Threshold:** Same response shape in 5+ endpoints = create DTO. No DTO/responses folder = MEDIUM.

**pattern_signature format:** `response_{entity}_{fields_hash}`

### 1.8 Duplicated Middleware/Decorator Chains

**Strategy:** Find route definitions with inline middleware arrays or stacked decorators.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Express middleware | Grep | `router\.\(get\|post\|put\|delete\)\(.*,\s*\[` (JS/TS) | Routes with middleware arrays |
| 2. FastAPI deps | Grep | `Depends\(.*\).*Depends\(` (Python) | Stacked FastAPI dependencies |
| 3. Python decorators | Grep | `@login_required\|@permission_required\|@auth` | Stacked auth decorators |
| 4. Spring annotations | Grep | `@PreAuthorize\|@Secured\|@RolesAllowed` (Java) | Stacked security annotations |
| 5. .NET filters | Grep | `\[Authorize\|ServiceFilter\|TypeFilter` (C#) | Stacked action filters |
| 6. Compare chains | Read | Read matched routes, compare middleware lists | Identical chains on multiple routes |

**Threshold:** Same middleware chain on 5+ routes = extract to router-level middleware or named chain.

**pattern_signature format:** `middleware_{chain_hash}`

### 1.9 Duplicated Type Definitions

**Strategy:** Find interfaces/types/structs with similar field sets.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. TS interfaces | Grep (multiline) | `interface\s+\w+\s*\{` | TypeScript interface declarations |
| 2. TS type aliases | Grep | `type\s+\w+\s*=\s*\{` | TypeScript type aliases |
| 3. Go structs | Grep (multiline) | `type\s+\w+\s+struct\s*\{` | Go struct definitions |
| 4. Python dataclasses | Grep | `@dataclass\|class\s+\w+\(BaseModel\)` | Python Pydantic/dataclass models |
| 5. C# records/classes | Grep | `(record\|class)\s+\w+Dto\|(record\|class)\s+\w+Response` | C# DTO definitions |
| 6. Compare fields | Read | Read type bodies, list fields | Same field names/types in >1 definition |

**Threshold:** 2+ types with 80%+ same fields = consolidate or create shared base type.

**pattern_signature format:** `type_{sorted_field_names_hash}`

### 1.10 Duplicated Mapping/Transformation Logic

**Strategy:** Find entity-to-DTO and DTO-to-entity conversion patterns.

| Step | Tool | Pattern | What It Finds |
|------|------|---------|---------------|
| 1. Object construction | Grep | `\{\s*id:\s*\w+\.id,\s*name:\s*\w+\.name` (JS/TS) | Inline entity→DTO mapping |
| 2. Spread + pick | Grep | `\.\.\.\w+,\s*\w+:\s*\w+\.\w+` (JS/TS) | Spread-based transformations |
| 3. Dict comprehension | Grep | `\{.*for\s+\w+\s+in\|dict\(\w+=\w+\.` (Python) | Python dict construction from objects |
| 4. Mapper methods | Grep | `toDto\|toEntity\|toModel\|fromDto\|fromEntity\|mapTo\|mapFrom` | Existing mapping methods |
| 5. LINQ Select | Grep | `\.Select\(.*=>\s*new\s+\w+Dto` (C#) | C# projection patterns |
| 6. Compare mappings | Read | Read mapping code, compare field assignments | Same fields mapped in multiple locations |

**Threshold:** Same mapping in 3+ locations = create dedicated mapper class/function.

**pattern_signature format:** `mapping_{source_type}_to_{target_type}`

## KISS Violation Detection

| Violation | Tool | Detection Pattern | Confirm |
|-----------|------|-------------------|---------|
| Abstract class, 1 impl | Grep | `abstract class\s+(\w+)` → count classes extending it | Read: only 1 subclass found |
| Factory for <3 types | Grep | `Factory\|factory\|create\w+` → Read body | Factory switch/if has <3 branches |
| Deep inheritance >3 | Grep | `extends\s+\w+` → trace chain via multiple Grep | Chain length >3 classes |
| Excessive generics | Grep | `<\w+\s+extends\s+.*&\s+` | >2 generic constraints |
| Wrapper-only classes | Grep | class with single method delegating to another class | Read: all methods just call `this.inner.*` |

## YAGNI Violation Detection

| Violation | Tool | Detection Pattern | Confirm |
|-----------|------|-------------------|---------|
| Dead feature flags | Grep | `FEATURE_\|feature_flag\|isEnabled\(` | Grep: flag always `true` or `false`, never toggled |
| Abstract methods, 0 override | Grep | `abstract\s+\w+\(` → search for implementations | No concrete implementation found |
| Unused config options | Grep | Config key defined → Grep for usage across codebase | 0 references outside definition |
| Interface, 1 impl | Grep | `interface\s+(\w+)` → `implements\s+\1` | Only 1 class implements |
| Premature generics | Grep | Generic class/function → usage count | Used with only 1 type parameter |

---
**Version:** 1.0.0
**Last Updated:** 2026-02-08
