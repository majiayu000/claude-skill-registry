---
name: cc-data-organization
description: "Audit and fix data organization: variable declarations, data types, magic numbers, naming conventions, and global data. Three modes: CHECKER (92-item checklist -> status table), APPLIER (type selection and naming guidance), TRANSFORMER (fix violations). Cover modern types: concurrent/shared state, nullable/optional, temporal/timezone, security-sensitive. Use when reviewing code for data organization issues, choosing data types, or fixing magic numbers. Triggers on: review variables, data types, magic numbers, naming, global data, check types, fix floats, constants."
---

# Skill: cc-data-organization

## STOP - Priority 1: Never Skip

| Item | Why Critical |
|------|--------------|
| No magic numbers in business logic | Source of silent bugs |
| Currency uses integer cents, never float | Financial bugs are lawsuits |
| No float == comparisons | Non-deterministic failures |
| Variables initialized before use | Undefined behavior |
| Boolean naming is unambiguous | Logic inversion bugs |

**Skipping Priority 1 items is NEVER acceptable.** They represent latent defects that will manifest later.

---

## Modes

### CHECKER
Purpose: Execute data organization checklists against code
Triggers:
  - "review my variable declarations"
  - "check for magic numbers"
  - "review data type usage"
  - "check my variable names"
Non-Triggers:
  - "what type should I use for X" -> APPLIER
  - "how should I name this variable" -> APPLIER
  - "fix these magic numbers" -> TRANSFORMER
Checklist: **See [checklists.md](./checklists.md)**
Metrics: **See [hard-data.md](./hard-data.md)** for Span/Live Time measures (goal: minimize both)
Output Format:
  | Item | Status | Evidence | Location |
  |------|--------|----------|----------|
Severity:
  - VIOLATION: Fails checklist item
  - WARNING: Partial compliance
  - PASS: Meets requirement

### APPLIER
Purpose: Guide data type selection, variable naming, and structure design
Triggers:
  - "what data type should I use for..."
  - "how should I name this variable"
  - "best practice for enums/constants"
  - "how should I organize this data"
Non-Triggers:
  - "review my types" -> CHECKER
  - "fix this" -> TRANSFORMER
  - "audit my code" -> CHECKER
Produces: Type recommendations, naming conventions, enum patterns, constant definitions, structure designs
Constraints:
  - [p.308] **Eliminate semantic literals** - Replace business values (`86400`, `12`, `0.07`) with named constants. Loop bounds `0`, `1` and array indices are typically fine.
  - [p.295] For currency: integer cents or BCD, never float
  - [p.306] **Enums (language-dependent):**
    - C/C++: Reserve 0 for invalid, define First/Last bounds
    - TypeScript string enums: No zero-reservation needed (no uninitialized risk)
    - Rust/Kotlin: Leverage exhaustive matching instead of bounds checks
  - [p.259] **Minimize scope**: Declare variables in innermost block where all usages occur. Balance with testability—sometimes slightly wider scope enables testing.
  - [p.263] **Names describe the entity clearly**: Reader should understand purpose without searching for definition. Examples: `d` (bad) → `data` (vague) → `userData` (better) → `validatedUserSubmission` (good for complex entity)
  - [p.279] Problem Orientation: names refer to problem domain (employeeData, printerReady), not computing (inputRec, bitFlag)
  - [p.263] **Name length heuristic**: 2-4 words, long enough to describe purpose, short enough to scan. Research shows 10-16 chars minimizes debugging effort [Gorla et al. 1990], but this is guidance, not a hard rule.

### TRANSFORMER
Purpose: Fix data organization violations
Triggers:
  - CHECKER findings with VIOLATION status
  - "replace magic numbers with constants"
  - "fix float comparison"
  - "refactor these globals"
Non-Triggers:
  - Large refactorings beyond data organization -> cc-refactoring-guidance
  - Control flow restructuring -> cc-control-flow-quality
Input -> Output:
  - Magic `86400` -> `SECONDS_PER_DAY = 86400`
  - `if (a == b)` floats -> `if (Math.abs(a-b) < EPSILON)`
  - `true, false, true` params -> enum values
  - Unstructured variables -> grouped structure
  - Direct global access -> access routines
Preserves: Behavior, unrelated code
Verification: Re-run CHECKER; VIOLATION count = 0

## Rationalization Counters
| Excuse | Reality |
|--------|---------|
| "Everyone knows what 12 means" | Named constants aid maintenance [Glass 1991] |
| "Floats are close enough for ==" | 0.1 added 10 times rarely equals 1.0 |
| "Magic numbers are faster to type" | Debugging hard-coded literals takes far longer |
| "I don't need custom types" | One typedef change vs hundreds of declarations |
| "Short names are faster to type" | Code read far more than written; favor read-time convenience |
| "Global variables are more convenient" | Convenience writing trades against difficulty reading, debugging, modifying |

### Sunk Cost Counters
**For resisting changes to "working" code:**

| Excuse | Reality |
|--------|---------|
| "It works, why change it?" | Violations are latent defects; "works" means "hasn't failed yet" |
| "I already invested time in this" | Time invested in bad code is lost regardless; fix now or pay more later |
| "Refactoring will break things" | Violations already broken; you just haven't discovered how yet |
| "Currency has always used floats here" | Every penny calculation is a potential lawsuit |
| "We've had no bugs from these magic numbers" | You've had bugs—you attributed them to other causes |
| "The code passed review before" | Past reviews missed issues; evidence now shows violations |

### Success-Bias Warning
**Past success does NOT predict future safety.**

Violations that "worked for years" fail when:
- Edge cases finally occur (currency rounding in new scenarios)
- Scale changes (global variable contention under load)
- Maintenance happens (magic numbers misunderstood by new developers)
- Requirements shift (hard-coded values need changing)

**Every checklist item applies regardless of past success.** "Worked until it didn't" examples fill bug databases.

## Modern Data Types Coverage

*Beyond Code Complete's C-era focus:*

### Concurrent Access
When data may be accessed from multiple threads/async contexts:
- **Identify shared state** - Mark variables accessed across thread boundaries
- **Access routines are mandatory** - Never expose shared data directly
- **Consider immutability** - Immutable data eliminates race conditions by design
- **Document thread safety** - Comment whether type/routine is thread-safe
- Violations: Data races, torn reads, lost updates

### Nullable/Optional Types
Modern languages use `Option<T>`, `Maybe`, `T?` instead of null pointers:
- **Prefer non-nullable by default** - Make nullability explicit and intentional
- **Handle all cases** - Exhaustive matching on Option/Maybe types
- **Avoid null as "not found"** - Use Option types or result types instead
- **Document null semantics** - When null is valid, document what it means
- C-style pointer guidance still applies to unsafe code

### Temporal Data
Dates and times are a common bug source:
- **Store timestamps in UTC** - Convert to local only for display
- **Use timezone-aware types** - Never use naive datetime for user-facing data
- **Be explicit about precision** - Seconds, milliseconds, nanoseconds?
- **Name with time unit** - `timeoutMs`, `durationSeconds`, not just `timeout`
- **Avoid magic time values** - `86400` → `SECONDS_PER_DAY`

### Security-Sensitive Data
Secrets, tokens, API keys require special handling:
- **Clear from memory after use** - Don't leave secrets in variables longer than needed
- **Never log sensitive data** - Redact in all log statements
- **Use dedicated types** - `SecureString`, `SensitiveData` wrappers
- **Limit scope aggressively** - Shortest possible lifetime


---

## Chain

| After | Next |
|-------|------|
| Data organization verified | cc-control-flow-quality (CHECKER) |

