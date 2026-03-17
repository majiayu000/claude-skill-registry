---
name: planning
description: Provides expertise on how to plan for work in this repo
---


## Overview

This skill provides comprehensive guidance on how to plan a new feature in this repo.

- We always use a Test-Driven Development (TDD) approach
- We emphasize not only runtime tests but also "type tests"
- We track our progress through the phased based work with a LOG file

## When to Use Sub-Agents

For complex, multi-phase work, consider delegating to specialized sub-agents:

### Project Manager Agent (`.claude/agents/project-manager.md`)

**Delegate planning work when:**
- User requests a new feature requiring multiple phases
- Current work would create a 5+ phase plan
- You need specialized planning expertise
- Context is getting large and planning is complex

**How to invoke:**
```typescript
await Task({
    description: "Create plan for X",
    subagent_type: "general-purpose",
    prompt: "You are the Project Manager Agent. Create plan for: [requirement]"
});
```

### Phase Executor Agent (`.claude/agents/phase-executor.md`)

**Delegate phase execution when:**
- Executing a single phase from an approved plan
- Want to ensure TDD workflow is followed strictly
- Need all quality checks (TODO scan, type tests, etc.)
- Want to preserve context between phases

**How to invoke:**
```typescript
await Task({
    description: "Execute Phase N",
    subagent_type: "general-purpose",
    prompt: "You are Phase Executor Agent. Execute Phase N from: [plan file]"
});
```

**See `.claude/agents/README.md` for detailed sub-agent architecture and usage patterns.**

---

## Types of Testing

### 1. Runtime Tests

Runtime tests verify the **actual behavior** of code during execution.

**When to use:**

- Testing function outputs with various inputs
- Verifying error handling and edge cases
- Checking side effects (file I/O, API calls, state mutations)
- Validating business logic and algorithms
- Testing class instance behavior and methods

**Tools:**

- Test runner: [Vitest](https://vitest.dev)
- Commands:
  - `pnpm test` - runs all runtime tests
  - `pnpm test GLOB` - runs tests matching the glob pattern
  - `pnpm test:watch` - runs tests in watch mode

**Example structure:**

```typescript
import { describe, it, expect } from "vitest";
import { prettyPath } from "~/utils";

describe("prettyPath()", () => {
    it("should format a path with directory and filename", () => {
        const result = prettyPath("/path/to/file.ts");
        expect(result).toBe("/path/to/file.ts"); // Expected formatting
    });

    it("should handle edge case: empty string", () => {
        const result = prettyPath("");
        expect(result).toBe("");
    });

    it("should handle edge case: root path", () => {
        const result = prettyPath("/");
        expect(result).toBe("/");
    });
});
```

---


### 2. Type Tests

Type tests verify the **type correctness** of TypeScript code at _design_ time.

#### **When to use:**

- Testing type utility functions (always)
- Verifying generic type constraints work as expected
- Ensuring conditional types resolve correctly
- Testing that complex inferred types are accurate
- Validating discriminated unions and type narrowing
- Checking that function signatures accept/reject correct types

#### **Tools:**

- Commands:
  - `pnpm test:types` - runs all type tests
  - `pnpm test:types GLOB` - runs type tests matching the glob pattern

#### Type Test Structure

This section will show you, layer by layer, how to compose and build good type tests.

##### `cases` block

All type tests in a given `it` test block (defined by Vitest) will have a type called `cases` defined as an array of _type tests_. 

```ts
type cases = [
    // ... type tests go here
]
```

> Note: our linting rules allow for the name `cases` to be defined _without being used_; this is intentional and a good thing.

##### `Expect<...>` wrapper

Every type test will be wrapped by an `Expect` type utility.

```ts
type cases = [
    Expect<...>,
    Expect<...>,
    // ...
]
```

##### Available Type Test Assertions

The `inferred-types` library provides a number of useful assertion utilities you can use to create your tests:

- `AssertTrue<T>`  ****
   - tests whether the **tested type** `T` is the type `true`
- `AssertFalse<T>`
   - tests whether the **tested type** `T` is the type `false`
- `AssertEqual<T,E>`
   - tests that the **tested type** `T` _equals_ the **expected type** `E`
- `AssertExtends<T,E>`
   - tests that the **tested type** `T` _extends_ the **expected type** `E`
- `AssertSameValues<T,E>`
   - tests that the **tested type** `T` is an array type and every element of `E` and `T` are the same but the order in which they arrive does not matter
- `AssertContains<T,E>`
   - when the **tested type** `T` is a `string`:
       - this utility will pass when `E` is also a `string` and represents a _sub-string_ of the sting literal `T`
   - when the **tested type** `T` is an array then:
       - this utility 

In all cases you put the test assertion _inside_ of the `Expect` utility:

```ts
type cases [
    Expect<AssertTrue<T>>,
    Expect<AssertExtends<T, string>>,
    // ...
]
```


##### Example 1

In our example we'll just test a _built-in_ type utility of Typescript's named `Capitalize<T>`.

- this utility simply capitalizes the first letter in a string literal

```ts
import type { Expect, Equal } from "inferred-types/types";

describe("Example 1", () => {
    it("string literals", () => {
        type Lowercase = Capitalize<"foo">;
        type AlreadyCapitalized = Capitalize<"Foo">;

        type cases = [
            Expect<AssertEqual<Lowercase, "Foo">>,
            Expect<AssertEqual<AlreadyCapitalized, "Foo">>,
        ]
    });

    it("wide string", () => {
        type Wide = Capitalize<string>;

        type cases = [
            Expect<AssertEqual<Wide, string>>
        ]
    })

    it("only first letter capitalized", () => {
        type SpaceThenLetter = Capitalize<" foo">;
        type TabThenLetter = Capitalize<"\tfoo">;

        type cases = [
            Expect<AssertEqual<SpaceThenLetter, " foo">>,
            Expect<AssertEqual<TabThenLetter, "\tfoo">>,
        ]
    })
});
```

**IMPORTANT:** in the example above we were testing a type utility (where a type utility is any type which accepts generics and uses them to produce a type); and with type utilities you CAN'T do runtime testing because there is no runtime component to test. However, we do still use the `Vitest` primitives of `describe` and `it` to organize the test.

##### Example 2

Let's imagine we create a simple function:

- `capitalize<T extends string>(text: T): Capitalize<T>`.
- here we have a VERY common situation for library authors: 
    - _a function which provides a narrow type return_
- in this situation we will want to have BOTH runtime and type tests

```ts
describe("example", () => {
    it("leading alpha character", () => {
        const lowercase = capitalize("foo");
        const alreadyCapitalized = capitalize("Foo");

        expect(lowercase).toEqual("Foo");
        expect(alreadyCapitalized).toEqual("Foo");

        type cases = [
            Expect<AssertEqual<typeof lowercase, "Foo">>,
            Expect<AssertEqual<typeof alreadyCapitalized, "Foo">>,
        ]
    });

    it("wide string", () => {
        const wide = capitalize("foo" as string);

        expect(wide).toBe("Foo");

        type cases = [
            Expect<AssertEqual<typeof wide, string>>
        ]
    })

    it("non-alpha leading character", () => {
        const spaceThenLetter = capitalize(" foo");
        const tabThenLetter = capitalize("\tfoo");

        expect(spaceThenLetter).toBe(" foo");
        expect(tabThenLetter).toBe("\tfoo");

        type cases = [
            Expect<AssertEqual<typeof spaceThenLetter, " foo">>,
            Expect<AssertEqual<typeof tabThenLetter, "\tfoo">>,
        ]
    })
})
```

**IMPORTANT:** in these sorts of tests the runtime and type tests naturally fit into the same `describe`/`it` blocks. You should almost NEVER have a set of runtime tests in one structure, and then a set of type tests in another. This almost always indicates someone who doesn't understand type testing well enough yet.

**IMPORTANT:** in both examples we've see a test structure where define intermediate variable/types which assume the value/type of the "test". Then we use the variable/type in our tests. We could possibly just inline the expression you're testing into the runtime and type tests but this can actually have undesirable side effects in some cases but having the intermediate variables/types defined first allows a human observer to hover over the variable to see what type resolution there was. This is highly valuable!

---

## Common Type Testing Mistakes

### Mistake #1: Separated "Type Tests" Blocks (MOST COMMON)

**❌ WRONG - Separated structure:**

```typescript
describe("myFunction()", () => {
    describe("Runtime tests", () => {
        it("should work", () => {
            expect(myFunction("test")).toBe("result");
        });
    });

    describe("Type Tests", () => {  // ❌ WRONG!
        it("should have correct type", () => {
            const result = myFunction("test");
            const _check: typeof result extends string ? true : false = true;
            expect(_check).toBe(true);  // ❌ This is NOT a type test!
        });
    });
});
```

**✅ CORRECT - Integrated structure:**

```typescript
describe("myFunction()", () => {
    it("should work with string input", () => {
        const result = myFunction("test");

        // Runtime test
        expect(result).toBe("result");

        // Type test - in the SAME it() block
        type cases = [
            Expect<AssertEqual<typeof result, "result">>
        ];
    });
});
```

### Mistake #2: Using Runtime Checks for Type Testing

**❌ WRONG:**
```typescript
const result = myFunction("test");
const _isString: typeof result extends string ? true : false = true;
expect(_isString).toBe(true);  // This is runtime testing, not type testing!
```

**✅ CORRECT:**
```typescript
const result = myFunction("test");
type cases = [
    Expect<AssertExtends<typeof result, string>>
];
```

### Mistake #3: No `cases` Array

**❌ WRONG:**
```typescript
Expect<AssertEqual<typeof result, "expected">>;  // Not in cases array!
```

**✅ CORRECT:**
```typescript
type cases = [
    Expect<AssertEqual<typeof result, "expected">>
];
```

---

## Type Test Validation

Before submitting ANY work with type tests, verify:

1. **Pattern check**: Does every type test use `type cases = [...]`?
2. **Assertion check**: Does every assertion use `Expect<Assert...>`?
3. **Structure check**: Are type tests side-by-side with runtime tests?
4. **Import check**: Do files import from `inferred-types/types`?
5. **No separation**: Are there ZERO "Type Tests" describe blocks?
6. **Tests pass**: Does `pnpm test:types` show "🎉 No errors!"?

**If any check fails, the type tests are incorrect and must be rewritten.**

---

## Decision Framework: Which Tests to Write?

Use this flowchart to determine what tests you need:

```text
Is the symbol exported from the module?
│
├─ NO → Consider if it needs tests at all
│        (internal helpers may not need dedicated tests)
│
└─ YES → What kind of symbol is it?
          │
          ├─ Type Utility (e.g., a type which takes generics)
          │  └─ Write TYPE TESTS always; no RUNTIME tests are even possible!
          │
          ├─ Constant (literal value)
          │  └─ Usually NO tests needed
          │     (unless it's a complex computed value)
          │
          ├─ Function / Arrow Function
          │  └─ Does it return a literal type?
          │     ├─ YES → Write BOTH runtime AND type tests
          │     └─ NO → Write RUNTIME tests (minimum); possibly write type tests
          │
          ├─ Class
          │  └─ Does it use generics or have methods which return literal types?
          │     ├─ YES → Write BOTH runtime AND type tests
          │     └─ NO → Write RUNTIME tests primarily
          │
          └─ Interface / Type Definition (e.g., a type without a generic input)
             └─ Usually NO test needed; if there is no generic then there is no variance to test
             └─ Only exception might be when the type being defined uses a lot of type utilities in it's definition. In these cases, you _might_ test that the type is not an `any` or `never` type because the underlying utilities 
```

**Rule of thumb:** When in doubt, write tests. It's better to have coverage than to skip it.


---

## Test Organization and Structure

### File Structure

Tests are organized by feature/command area:

```text
tests/
├── unit/
│   ├── test-command/       # Tests for the 'test' CLI command
│   ├── symbol-command/     # Tests for the 'symbols' CLI command
│   ├── source-command/     # Tests for the 'source' CLI command
│   ├── utils/              # Tests for utility functions
│   └── WIP/                # Temporary location for in-progress phase tests
├── integration/
│   ├── fast/               # Fast integration tests (<2s each)
│   └── *.test.ts           # Full integration tests
└── fixtures/               # Test fixtures and sample projects
```

### Naming Conventions

- **Test files:** `*.test.ts`
- **Fast integration tests:** `*.fast.test.ts`
- **Test descriptions:**
  - Use "should" statements: `it("should return true when...)`
  - Be specific about the scenario: `it("should handle empty arrays")`
  - Describe the behavior, not the implementation

### Test Structure Principles

**DO:**

- Keep tests focused on a single behavior
- Use descriptive test names that explain the scenario
- Group related tests in `describe` blocks
- Test edge cases (empty, null, undefined, boundary values)
- Test error conditions and failure modes
- Make tests independent (no shared state between tests)

**DON'T:**

- Test implementation details (test behavior, not internals)
- Add logic to tests (no conditionals, loops, or complex computations)
- Share mutable state between tests
- Make tests depend on execution order
- Skip asserting the results (every test needs expectations)

---

## Plans using TDD Workflow for Phase-Based Development

When implementing a new feature, ALWAYS follow this comprehensive TDD workflow:

### Phase Structure Overview

0. **PLAN FORMALIZATION** - Improve upon the user's plan definition
1. **SNAPSHOT** - Capture current test state
2. **CREATE LOG** - Document starting position
3. **WRITE TESTS** - Create tests first (TDD)
4. **IMPLEMENTATION** - Build to pass tests
5. **CLOSE OUT** - Verify, migrate tests, document completion

---

### Step 0: PLAN FORMALIZATION

When a user provides you with a new feature or plan idea, the first step is always to take that as an input into making a more structured and formalized plan:

1. The initial request for a plan/feature/etc. should be analyzed and a reasonable name for the plan should be made. 
    -  A good name is between a 2-3 words up to a full sentence but never more.
2. Unless the plan is VERY simple the plan should be broken up into multiple phases
    - Each phase of the plan should follow a TDD workflow unless there is an explicit reason not to
3. Your improved plan should be written as a Markdown file with a filename of:
    - `.ai/plans/${YYYY}-${MM}-${DD}-${NAME}.md`
    - all date based variables should use the user's local time not UTC
    - Formatting should follow good Markdown practices:
        - Never use a code block without a name; you can use `txt` if you are simply using the block as a text output.
        - Always include a blank line after headings
    - Once you've written the plan you should ask the user to review it unless they have expressly stated that you can execute it upon completion of the plan
        - If the user HAS granted you the right to execute the plan without review then you should execute the plan phase by phase
        - Never start a new phase if the previous phase is somehow incomplete; this indicates that you should checkpoint with the user

The remaining steps represent how each PHASE of the plan should be structured.

### Step 1: PHASE SNAPSHOT

Capture the current state of all tests before making any changes.

**Actions:**

1. Run all runtime tests:

   ```bash
   pnpm test
   ```

2. Run all type tests:

   ```bash
   pnpm test:types
   ```

3. Create a simple XML representation of test results distinguishing between runtime and type test runs
4. Document any existing failures (these are your baseline - don't fix yet)

**Purpose:** Establish a clear baseline so you can detect regressions and measure progress.

---

### Step 2: CREATE LOG

Create a log file to track this phase of work.

**Actions:**

1. Create log file with naming convention:

   **🚨 CRITICAL: Phase log files MUST follow this exact naming pattern:**

   ```bash
   mkdir -p .ai/logs
   touch .ai/logs/${project-name}-${phase-identifier}-log.md
   ```

   **Pattern Rules:**
   - **Project name comes FIRST** (not the date, not the phase)
   - Use kebab-case for project name
   - Phase identifier should clearly indicate which phase (e.g., `phase1`, `phase7.5`, `phase-remediation`)
   - End with `-log.md`

   **✅ CORRECT Examples:**
   - `.ai/logs/say-phase1-foundation-log.md`
   - `.ai/logs/say-phase4-say-mapper-log.md`
   - `.ai/logs/say-phase7.5-type-system-refinement-log.md`
   - `.ai/logs/tts-library-phase2-voice-discovery-log.md`

   **❌ WRONG Examples:**
   - `.ai/logs/2025-10-22-phase1-log.md` (date first, no project name)
   - `.ai/logs/phase4-say-mapper-log.md` (no project name)
   - `.ai/logs/2025-10-22-say-phase4-log.md` (date should not be in filename)

   **Why This Matters:**
   - Consistent naming allows easy filtering: `ls .ai/logs/say-*.md`
   - Project context is immediately visible
   - Logs are naturally grouped by project in alphabetical listings
   - Easier to find specific phase logs across different projects

2. Add `## Starting Test Position` section with XML code block containing test results from SNAPSHOT

3. Add `## Repo Starting Position` section

4. Run the start-position script to capture git state:

   ```bash
   bun run .claude/skills/scripts/start-position.ts planName phaseNumber
   ```

   This returns markdown content showing:
   - Last local commit hash
   - Last remote commit hash
   - Dirty files (uncommitted changes)
   - File snapshot (if not using --dry-run flag)

5. Append the start-position output to the log file

**Purpose:** Create a detailed record of the starting point for debugging and tracking progress.

---

### Step 3: WRITE TESTS

Write tests FIRST before any implementation. This is true Test-Driven Development.

**Actions:**

1. **Understand existing test structure:**
   - Review similar tests in the codebase
   - Identify patterns and conventions
   - Determine where your tests should eventually live

2. **Create tests in WIP directory:**
   - All new test files for this phase go in `tests/unit/WIP/`
   - This isolation allows:
     - Easy GLOB pattern targeting: `pnpm test WIP`
     - Regression testing by exclusion: `pnpm test --exclude WIP`
     - Clear separation of work-in-progress from stable tests

3. **Write comprehensive test coverage:**
   - Start with happy path (expected successful behavior)
   - Add edge cases (empty, null, undefined, boundaries)
   - Add error conditions
   - Include both runtime and type tests if applicable

4. **Verify tests FAIL initially:**
   - Run your new tests: `pnpm test WIP`
   - Confirm they fail (you haven't implemented yet)
   - Failing tests prove they're valid and will detect when implementation is complete

**Example WIP structure:**

```text
tests/unit/WIP/
├── phase1-cli-options.test.ts
├── phase1-filter-logic.test.ts
└── phase1-integration.test.ts
```

**Purpose:** Tests define the contract and expected behavior before any code is written.

---

### Step 4: IMPLEMENTATION

Use the tests to guide your implementation.

**Actions:**

1. **Implement minimal code to pass each test:**
   - Work on one test at a time (or small group)
   - Write the simplest code that makes the test pass
   - Don't over-engineer or add features not covered by tests

2. **Iterate rapidly:**
   - Run tests frequently: `pnpm test WIP`
   - For type tests: `pnpm test:types WIP`
   - Fix failures immediately
   - Keep the feedback loop tight

3. **Continue until all phase tests pass:**
   - All tests in `tests/unit/WIP/` should be green
   - No shortcuts - every test must pass

4. **Refactor with confidence:**
   - Once tests pass, improve code quality
   - Tests act as a safety net
   - Re-run tests after each refactor

**Purpose:** Let tests drive the implementation, ensuring you build exactly what's needed.

---

### Step 4.5: CRITICAL - TODO Markers and Incomplete Types

**🚨 THIS IS A BLOCKING REQUIREMENT - DO NOT PROCEED WITHOUT ADDRESSING ALL TODOs 🚨**

Before considering implementation complete, you MUST perform a comprehensive scan for TODO markers and incomplete type utilities.

**Actions:**

1. **Search for TODO markers in ALL files touched during this phase:**

   ```bash
   # Search all source files
   rg -i "TODO|FIXME|XXX|HACK" modules/lib/src

   # Search type files specifically
   rg -i "TODO|FIXME" modules/lib/src/types
   ```

2. **Identify incomplete type utilities:**
   - Any type utility that is a simple pass-through (e.g., `type Foo<T> = T`)
   - Any type utility with a TODO comment
   - Any type utility that should do type-level computation but doesn't
   - Any exported type that has `any`, `unknown`, or `never` as a default/fallback

3. **Common patterns of incomplete types to watch for:**

   ```typescript
   // ❌ UNACCEPTABLE - These are NOT complete implementations

   // #TODO
   export type StripSimpleTags<T extends string> = T;  // Should strip tags!

   // TODO
   export type HasSimpleTags<T extends string> = false;  // Should detect tags!

   export type MyUtility<T> = any;  // Lazy cop-out

   export type ParseSomething<T> = T;  // No parsing happening
   ```

4. **For EACH TODO or incomplete type found:**
   - **STOP implementation immediately**
   - Add it as a blocking task to your todo list
   - Implement the complete solution before proceeding
   - Add comprehensive type tests to verify the solution works
   - Document why it was initially incomplete (learning for future)

5. **Verification checklist:**
   - [ ] Searched all modified files for TODO/FIXME/XXX/HACK
   - [ ] Inspected all type utilities in `modules/lib/src/types/`
   - [ ] Verified no pass-through type utilities exist (unless intentional)
   - [ ] Confirmed all exported types provide value, not just aliases
   - [ ] Added type tests for any newly implemented type utilities
   - [ ] `pnpm test:types` passes with all new type utilities working

**Why This Matters:**

This is a **type-driven library** that emphasizes:
- Narrow types and type-level computation
- Compile-time guarantees through the type system
- Using `inferred-types` for sophisticated type utilities

Leaving TODO markers or stub type utilities is:
- ❌ A broken contract with library users
- ❌ Defeats the entire purpose of type-driven design
- ❌ Creates technical debt that compounds
- ❌ Shows lack of attention to detail

**Example of proper type utility implementation:**

```typescript
// ✅ CORRECT - Full implementation with tests

/**
 * Strips simple tags like <soft>, <loud>, <fast> from a string literal type
 */
export type StripSimpleTags<T extends string> =
    T extends `${infer Before}<soft>${infer After}`
        ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
        : T extends `${infer Before}</soft>${infer After}`
            ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
            : T extends `${infer Before}<loud>${infer After}`
                ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
                : T extends `${infer Before}</loud>${infer After}`
                    ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
                    // ... continue for all tags
                    : T;

// Type tests to verify it works
type cases = [
    Expect<AssertEqual<StripSimpleTags<"hello <soft>world</soft>">, "hello world">>,
    Expect<AssertEqual<StripSimpleTags<"<loud>HELLO</loud>">, "HELLO">>,
    Expect<AssertEqual<StripSimpleTags<"no tags">, "no tags">>
];
```

**If you find TODOs during implementation:**

1. **DO NOT move forward** - Address them immediately
2. **Add them to your TODO list** - Track as blocking items
3. **Implement proper solutions** - No shortcuts or workarounds
4. **Add tests** - Verify the solution actually works
5. **Document the fix** - Explain the approach in code comments

**This is non-negotiable. A phase with unresolved TODOs is an INCOMPLETE phase.**

**Purpose:** Ensure type utilities are fully implemented and the library maintains its type-safety guarantees.

---

### Step 5: CLOSE OUT

Verify completeness, check for regressions, and finalize the phase.

**Actions:**

1. **Run full test suite:**

   ```bash
   pnpm test        # All runtime tests
   pnpm test:types  # All type tests
   ```

2. **Handle any regressions:**

   If existing tests now fail:
   - **STOP and think deeply** - understand WHY the test is failing, not just the error message
   - Document the regression in the log file under `## Regressions Found`
   - Determine root cause:
     - Is your implementation incorrect?
     - Does the existing test need updating (only if requirements changed)?
     - Is there a side effect you didn't anticipate?
   - Fix the root cause, not just the symptom
   - Re-run all tests to confirm fix

3. **If no regressions, migrate tests to permanent locations:**

   - **Think carefully** about the right permanent location for each test
   - Consider if a new subdirectory is needed in the test structure
   - Move tests from `tests/unit/WIP/` to their permanent homes
   - Delete the `tests/unit/WIP/` directory
   - **Rerun tests** to ensure nothing broke during migration

4. **Update the log file:**

   Add a `## Phase Completion` section with:
   - Date and time completed
   - Final test count (passing/total)
   - Any notable issues or decisions made
   - Location where tests were migrated to

5. **Report completion:**

   Inform the user that the phase is complete with a summary of:
   - What was implemented
   - Test coverage added
   - Any important notes or caveats

**Purpose:** Ensure quality, prevent regressions, and properly integrate work into the codebase.

---

## Testing Best Practices

### General Principles

- **Prefer real implementations over mocks**: Only mock external dependencies (APIs, file system, databases). Keep internal code integration real.

- **Use realistic test data**: Mirror actual usage patterns. If your function processes user objects, use realistic user data in tests.

- **One behavior per test**: Each `it()` block should test a single specific behavior. This makes failures easier to diagnose.

- **Tests should be deterministic**: Same input = same output, every time. Avoid depending on current time, random values, or external state unless that's what you're testing.

- **Keep tests independent**: Each test should be able to run in isolation. Use `beforeEach()` for setup, not shared variables.

- **Test the contract, not the implementation**: If you change HOW something works but it still behaves the same, tests shouldn't break.

### Error Handling

- **Prioritize fixing source code over changing tests**: When tests fail, your first instinct should be to fix the implementation to meet the test's expectation, not to change the test to match the implementation.

- **Understand failures deeply**: Don't just read the error message - understand WHY the test is failing. Use debugging, logging, or step through the code if needed.

- **Document complex test scenarios**: If a test needs explanation, add a comment describing what scenario it's covering and why it matters.

### Performance

- **Keep unit tests fast**: Unit tests should run in milliseconds. If a test is slow, it's likely testing too much or hitting external resources.

- **Separate fast and slow tests**: Integration tests can be slower. Keep them in separate files (e.g., `*.fast.test.ts` vs `*.test.ts`).

- **Use focused test runs during development**: Don't run the entire suite on every change. Use glob patterns to run just what you're working on.

### Type Testing Specifics

- **Always test the positive case**: Verify that valid types are accepted and produce the expected result type.

- **Test the negative case when relevant**: Use `@ts-expect-error` to verify that invalid types are properly rejected.

- **Test edge cases in type logic**: Empty objects, `never`, `unknown`, union types, etc.

- **Keep type tests close to runtime tests**: When testing a function with both runtime and type tests, keep them in the same file within the same `describe` block for cohesion.

---

## Common Patterns and Examples

### Testing Error Cases

```typescript
it("should throw error for invalid input", () => {
    expect(() => parseConfig("invalid")).toThrow("Invalid config format");
});

it("should return error result for invalid type", () => {
    const result = safeParseConfig("invalid");
    expect(result.success).toBe(false);
    if (!result.success) {
        expect(result.error).toContain("Invalid config");
    }
});
```

### Testing Async Functions

```typescript
it("should resolve with data on success", async () => {
    const result = await fetchUser(123);
    expect(result.id).toBe(123);
    expect(result.name).toBeDefined();
});

it("should reject with error on failure", async () => {
    await expect(fetchUser(-1)).rejects.toThrow("User not found");
});
```

### Testing Type Narrowing

```typescript
it("should narrow type based on discriminant", () => {
    type Result = { success: true; data: string } | { success: false; error: string };

    const handleResult = (result: Result) => {
        if (result.success) {
            type Test = Expect<Equal<typeof result, { success: true; data: string }>>;
            return result.data;
        } else {
            type Test = Expect<Equal<typeof result, { success: false; error: string }>>;
            return result.error;
        }
    };
});
```

---

## Quick Reference

### Commands

```bash
# Runtime tests
pnpm test                    # Run all runtime tests
pnpm test path/to/test       # Run specific test file
pnpm test WIP                # Run only WIP tests
pnpm test --exclude WIP      # Run all except WIP (regression check)
pnpm test:watch              # Run in watch mode
pnpm test:ui                 # Run with UI

# Type tests
pnpm test:types              # Run all type tests
pnpm test:types GLOB         # Run type tests matching pattern
pnpm test:types WIP          # Run only WIP type tests

# Common patterns during development
pnpm test utils              # Test all utils
pnpm test:types utils        # Type test all utils
```

### Test Quality Checklist

Before considering tests complete, verify:

- [ ] All exported functions have runtime tests
- [ ] Functions with complex types have type tests
- [ ] Happy path is tested
- [ ] Edge cases are covered (empty, null, undefined, boundaries)
- [ ] Error conditions are tested
- [ ] Tests are independent (can run in any order)
- [ ] Tests are deterministic (consistent results)
- [ ] Test names clearly describe what's being tested
- [ ] No regressions in existing tests
- [ ] Tests run quickly (unit tests < 100ms per test)

### Phase Completion Checklist

Before closing out a phase:

- [ ] SNAPSHOT captured
- [ ] Log file created with starting position
- [ ] Tests written in `tests/unit/WIP/`
- [ ] Tests initially failed (proving validity)
- [ ] Implementation completed
- [ ] **🚨 CRITICAL: ALL TODO markers addressed and resolved**
- [ ] **🚨 CRITICAL: ALL type utilities fully implemented (no stub pass-throughs)**
- [ ] **🚨 CRITICAL: Type tests added for all new type utilities**
- [ ] All WIP tests passing
- [ ] Full test suite run (no regressions)
- [ ] Tests migrated from WIP to permanent locations
- [ ] `tests/unit/WIP/` directory removed
- [ ] Log file updated with completion notes
- [ ] User notified of phase completion

---

## Summary

Effective testing requires understanding **what** to test, **how** to test it, and **when** to use different testing approaches:

- **Type utilities** → Type tests only
- **Simple functions** → Runtime tests (minimum)
- **Complex functions** → Both runtime and type tests
- **Classes** → Primarily runtime tests, add type tests for complex generics

Follow TDD principles: write tests first, implement to pass them, then refactor with confidence. Keep tests fast, focused, and independent.

For phase-based development, use the five-step workflow: SNAPSHOT → CREATE LOG → WRITE TESTS → IMPLEMENTATION → CLOSE OUT. This ensures comprehensive test coverage, prevents regressions, and maintains clear documentation of your progress.

When tests fail, **understand why** before fixing. Prioritize fixing implementation over changing tests, unless the test itself was wrong.

## Sub-Agent Architecture

For complex multi-phase projects, leverage specialized sub-agents:

- **Project Manager Agent** - Creates detailed phased plans (see `.claude/agents/project-manager.md`)
- **Phase Executor Agent** - Executes complete TDD cycles for single phases (see `.claude/agents/phase-executor.md`)

See `.claude/agents/README.md` for complete architecture guide, invocation patterns, and examples.
