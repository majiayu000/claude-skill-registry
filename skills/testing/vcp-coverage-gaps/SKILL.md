---
name: vcp-coverage-gaps
description: >
  Identify untested code by mapping source files to test files.
  Finds functions without tests and tests missing edge case coverage.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, WebFetch
argument-hint: "[path]"
---

# VCP Coverage Gaps

Map source files to test files and identify untested or under-tested code.

## Step 1: Resolve Config

1. Read `.vcp/config.json` from the project root. Extract the `pluginRoot` field.
2. **If `.vcp/config.json` does not exist or `pluginRoot` is missing:** Stop and tell the user: "No VCP configuration found. Run `/vcp-init` to configure VCP for this project."
3. **Validate `pluginRoot`:** The path must be absolute, contain `/.claude/` (or `\.claude\` on Windows) as a path segment, and contain only safe path characters (letters, digits, `/`, `\`, `-`, `_`, `.`, `:`, and spaces). Reject any path with shell metacharacters (`;`, `&`, `|`, `$`, `` ` ``, `(`, `)`, `{`, `}`, `<`, `>`, `!`, `~`, `#`, `*`, `?`, `[`, `]`, `'`, `"`). If validation fails, stop and tell the user: "Invalid pluginRoot — must be within ~/.claude/ and contain no shell metacharacters. Run `/vcp-init` to fix." Also verify the file `<pluginRoot>/lib/vcp-context-core.ts` exists using Glob. If it does not exist, stop and tell the user: "pluginRoot points to an invalid VCP installation. Run `/vcp-init` to fix."
4. Run the config resolution script via Bash:
   ```bash
   bun "<pluginRoot>/lib/resolve-config.ts" "<project-root>"
   ```
5. Parse the JSON output. It contains: `applicableStandards`, `ignoredRules`, `severity`, `exclude`.

## Step 2: Fetch Applicable Standards

From the `applicableStandards` array in the resolved config, keep only entries where:
- `id` is `core-testing`, OR
- `id` is `core-error-handling`

For each selected standard, use WebFetch to fetch its content from:
```
{entry.url}
```

Extract the **Rules** section from each fetched standard.

## Step 4: Map Source to Test Files

**Target path:** `$ARGUMENTS` if provided. If not provided, scan the entire project.

1. Use Glob to find source files in the target path (exclude patterns from `exclude` in the resolved config, and also exclude test files themselves).

2. For each source file, attempt to find a corresponding test file using naming conventions:
   - `src/foo.ts` → `src/foo.test.ts`, `src/foo.spec.ts`, `tests/foo.test.ts`, `test/foo.test.ts`, `src/__tests__/foo.test.ts`
   - `src/foo.py` → `tests/test_foo.py`, `test/test_foo.py`, `src/test_foo.py`
   - `src/foo.go` → `src/foo_test.go`
   - `src/Foo.java` → `src/FooTest.java`, `test/FooTest.java`
   - `src/foo.rb` → `spec/foo_spec.rb`, `test/test_foo.rb`
   - `src/foo.rs` → `src/foo_test.rs`, `tests/foo.rs`

3. Also use Grep to search for imports/references to the source file's exports within test directories, to catch non-conventional test file locations.

## Step 5: Analyze Coverage Gaps

For each source file:

1. **Identify public functions/exports** — Read the file and list all exported functions, public methods, API endpoints, route handlers, and CLI commands.

2. **Check test existence** — Does a corresponding test file exist? Does any test file import or reference this source file?

3. **Check function-level coverage** — For each public function, search the test files for tests that call or exercise it. A function is "untested" if no test references it.

4. **Check edge case coverage** — For tested functions, check if the tests cover:
   - Error/failure conditions (per `core-error-handling` rules)
   - Boundary values and empty inputs (per `core-testing` Rule 7)
   - The function's validation rules

5. **Prioritize gaps by risk:**
   - **Critical:** Integration boundaries (API endpoints, database access, external service calls) without tests
   - **High:** Error handlers and validation logic without tests
   - **Medium:** Business logic functions without tests
   - **Low:** Simple utilities, getters/setters, configuration without tests

## Step 6: Report Findings

Output a coverage map and prioritized gaps.

```
### VCP Coverage Gaps

**Standards:** core-testing, core-error-handling
**Source files scanned:** N files
**Test files found:** M files

#### Coverage Map

| Source File | Test File | Tested Functions | Untested Functions | Priority |
|-------------|-----------|------------------|--------------------|----------|
| src/routes/users.ts | tests/users.test.ts | 3/5 | createUser, deleteUser | Critical |
| src/services/payment.ts | tests/payment.test.ts | 2/4 | refund, handleWebhook | Critical |
| src/utils/validation.ts | — | 0/6 | all | High |
| src/models/order.ts | tests/order.test.ts | 4/4 | — | — |

#### Untested Code (by priority)

##### Critical — Integration Boundaries

- **src/routes/users.ts** — `createUser` (line 25), `deleteUser` (line 78)
  - These are API endpoints handling user input. Untested endpoints are direct security risk.

- **src/services/payment.ts** — `refund` (line 42), `handleWebhook` (line 95)
  - External payment service integration. Failures here affect money.

##### High — Error Handling & Validation

- **src/utils/validation.ts** — No test file exists
  - 6 validation functions with no test coverage. Validation bugs lead to bad data entering the system.

##### Medium — Business Logic

...

#### Edge Case Gaps (tested but incomplete)

- **tests/payment.test.ts** → `processPayment`:
  - Missing: zero-amount test, currency mismatch test, duplicate payment test
- **tests/users.test.ts** → `updateUser`:
  - Missing: empty payload test, invalid email format test

**Summary:** X untested functions across Y files. Z edge case gaps in existing tests.
```

If all source files have corresponding test files and all public functions are tested: **"Full coverage mapped. N source files, M test files. No untested public functions found."** (Still note edge case gaps if found.)
