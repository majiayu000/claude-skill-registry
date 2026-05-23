---
name: clojure-write
description: Guide Clojure and ClojureScript development using REPL-driven workflow, coding conventions, and best practices. Use when writing, developing, or refactoring Clojure/ClojureScript code.
---

# Clojure Development Skill

## Tool Preference

When `clojure-mcp` tools are available (e.g., `clojure_eval`, `clojure_edit`), **always use them**
instead of shell commands like `./bin/mage -repl`. The MCP tools provide:
- Direct REPL integration without shell escaping issues
- Better error messages and feedback
- Structural Clojure editing that prevents syntax errors

Only fall back to `./bin/mage` commands when clojure-mcp is not available.
# Autonomous Development Workflow

- Do not attempt to read or edit files outside the project folder
- Add failing tests first, then fix them
- Work autonomously in small, testable increments
- Run targeted tests, and lint continuously during development
- Prioritize understanding existing patterns before implementing
- Don't commit changes, leave it for the user to review and make commits
# Metabase Clojure Style Guide

This guide covers Clojure and ClojureScript coding conventions for Metabase. See also: `CLOJURE_STYLE_GUIDE.adoc` for the Community Clojure Style Guide.

## Naming Conventions

**General Naming:**

- Acceptable abbreviations: `acc`, `i`, `pred`, `coll`, `n`, `s`, `k`, `f`
- Use `kebab-case` for all variables, functions, and constants

**Function Naming:**

- Pure functions should be nouns describing the value they return (e.g., `age` not `calculate-age` or `get-age`)
- Functions with side effects must end with `!`
- Don't repeat namespace alias in function names

**Destructuring:**

- Map destructuring should use kebab-case local bindings even if the map uses `snake_case` keys

## Documentation Standards

**Docstrings:**

- Every public var in `src` or `enterprise/backend/src` must have docstring
- Format using Markdown conventions
- Reference other vars with `[[other-var]]` not backticks

**Comments:**

- `TODO` format: `;; TODO (Name M/D/YY) -- description`

## Code Organization

**Visibility:**

- Make everything `^:private` unless it is used elsewhere
- Try to organize namespaces to avoid `declare` (put public functions near the end)

**Size and Structure:**

- Break up functions > 20 lines
- Lines ≤ 120 characters
- No blank lines within definition forms (except pairwise `let`/`cond`)

## Style Conventions

**Keywords and Metadata:**

- Prefer namespaced keywords for internal use: `:query-type/normal` not `:normal`
- Tag variables with `:arglists` metadata if they're functions but wouldn't otherwise have it

## Tests

**Organization:**

- Break large tests into separate `deftest` forms for logically separate test cases
- Test names should end in `-test` or `-test-<number>`

**Performance:**

- Mark pure function tests `^:parallel`

## Modules

**OSS Modules:**

- Follow `metabase.<module>.*` pattern
- Source in `src/metabase/<module>/`

**Enterprise Modules:**

- Follow `metabase-enterprise.<module>.*` pattern
- Source in `enterprise/backend/src/metabase_enterprise/<module>/`

**Module Structure:**

- REST API endpoints go in `<module>.api` or `<module>.api.*` namespaces
- Put module public API in `<module>.core` using Potemkin imports
- Put Toucan models in `<module>.models.*`
- Put settings in `<module>.settings`
- Put schemas in `<module>.schema`

**Module Linters:**

- Do not cheat module linters with `:clj-kondo/ignore [:metabase/modules]`

## REST API Endpoints

**Required Elements:**

- All new endpoints must have response schemas (`:- <schema>` after route string)
- All endpoints need Malli schemas for parameters (detailed and complete)
- All new REST API endpoints MUST HAVE TESTS

**Naming Conventions:**

- Query parameters use kebab-case
- Request bodies use `snake_case`
- Routes use singular nouns (e.g., `/api/dashboard/:id`)

**Behavior:**

- `GET` endpoints should not have side effects (except analytics)
- `defendpoint` forms should be small wrappers around Toucan model code

## MBQL (Metabase Query Language)

**Restrictions:**

- No raw MBQL introspection outside of `lib`, `lib-be`, or `query-processor` modules
- Use Lib and MBQL 5 in new source code; avoid legacy MBQL

## Database and Models

**Naming:**

- Model names and table names should be singular nouns
- Application database uses `snake_case` identifiers

**Best Practices:**

- Use `t2/select-one-fn` instead of fetching entire rows for one column
- Put correct behavior in Toucan methods, not separate helper functions

## Drivers

**Documentation:**

- New driver multimethods must be mentioned in `docs/developers-guide/driver-changelog.md`

**Implementation:**

- Driver implementations should pass `driver` argument to other driver multimethods
- Don't hardcode driver names in implementations
- Minimize logic inside `read-column-thunk` in JDBC-based drivers

## Miscellaneous

**Examples:**

- Example data should be bird-themed if possible

**Linter Suppressions:**

- Use proper format for kondo suppressions
- No `#_:clj-kondo/ignore` (keyword form)

**Configurable Options:**

- Don't define configurable options that can only be set with environment variables
- Use `:internal` `defsetting` instead
## Linting and Formatting

- **Lint PR:** `./bin/mage kondo-updated master` (or whatever target branch)
  - Call the command one time at the beginning, record the results, then work through the problems one at a time.
  - If the solution is obvious, then please apply the fix. Otherwise skip it.
  - If you fix all the issues (and verify by rerunning the kondo-updated command):
    - commit the change with a succinct and descriptive commit message
- **Lint File:** `./bin/mage kondo <file or files>`
  - Use the linter as a way to know that you are adhering to conventions in place in the codebase
- **Lint Changes:** `./bin/mage kondo-updated HEAD`
- **Format:** `./bin/mage cljfmt-files [path]`

## Testing

- **Run a test:** `./bin/mage run-tests namespace/test-name`
- **Run all tests in a namespace:** `./bin/mage run-tests namespace`
- **Run all tests for a module:** `./bin/mage run-tests test/metabase/notification` Because the module lives in that directory.

Note: the `./bin/mage run-tests` command accepts multiple args, so you can pass
`./bin/mage run-tests namespace/test-name namespace/other-test namespace/third-test`
to run 3 tests, or
`./bin/mage run-tests test/metabase/module1 test/metabase/module2` to run 2 modules.

## Code Readability

- **Check Code Readability:** `./bin/mage -check-readable <file> [line-number]`
  - Run after every change to Clojure code
  - Check specific line first, then entire file if readable

## REPL Usage

> **Note:** If you have `clojure-mcp` tools available (check for tools like `clojure_eval`),
> **always prefer those over `./bin/mage -repl`**. The MCP tools provide better integration,
> richer feedback, and avoid shell escaping issues. Only use `./bin/mage -repl` as a fallback
> when clojure-mcp is not available.

- **Evaluating Clojure Code:** `./bin/mage -repl '<code>'`
  - See "Sending Code to the REPL" section for more details

### Sending Code to the REPL

- Send code to the metabase process REPL using: `./bin/mage -repl '(+ 1 1)'` where `(+ 1 1)` is your Clojure code.
  - See `./bin/mage -repl -h` for more details.
  - If the Metabase backend is not running, you'll see an error message with instructions on how to start it.

#### Working with Files and Namespaces

1. **Load a file and call functions with fully qualified names**:

To call `your.namespace/your-function` on `arg1` and `arg2`:

```
./bin/mage -repl --namespace your.namespace '(your-function arg1 arg2)'
```

DO NOT use "require", "load-file" etc in the code string argument.

#### Understanding the Response

The `./bin/mage -repl` command returns three separate, independent outputs:

- `value`: The return value of the last expression (best for data structures)
- `stdout`: Any printed output from `println` etc. (best for messages)
- `stderr`: Any error messages (best for warnings and errors)

Example call:

```bash
./bin/mage -repl '(println "Hello, world!") '\''({0 1, 1 3, 2 0, 3 2} {0 2, 1 0, 2 3, 3 1})'
```

Example response:

```
ns: user
session: 32a35206-871c-4553-9bc9-f49491173d1c
value:  ({0 1, 1 3, 2 0, 3 2} {0 2, 1 0, 2 3, 3 1})
stdout:  Hello, world!
stderr:
```

For effective REPL usage:

- Return data structures as function return values
- Use `println` for human-readable messages
- Print errors to stderr

## REPL-Driven Development Workflow

- Start with small, fundamental functions:
- Identify the core features or functionalities required for your task.
- Break each feature down into the smallest, most basic functions that can be developed and tested independently.
- Write and test in the REPL:
  - Write the code for each small function directly in the REPL (Read-Eval-Print Loop).
  - Test it thoroughly with a variety of inputs, including typical use cases and relevant edge cases, to ensure it
    behaves as expected.
- Integrate into source code:
  - Once a function works correctly in the REPL, move it from the REPL environment into your source code files (e.g.,
    within appropriate namespaces).
- Gradually increase complexity:
  - Build upon tested, basic functions to create more complex functions or components.
  - Compose smaller functions together, testing each new composition in the REPL to verify correctness step by step.
- Ensure dependency testing:
  - Make sure every function is fully tested in the REPL before it is depended upon by other functions.
  - This ensures that each layer of your application is reliable before you build on it.
- Use the REPL fully:
  - Use the REPL as your primary tool to experiment with different approaches, iterate quickly, and get immediate
    feedback on your code.
- Follow functional programming principles:
  - Keep functions small, focused, and composable.
  - Use Clojure's functional programming features—like immutability, higher-order functions, and the standard
    library—to write concise, effective code.

## How to Evaluate Code

### Bottom-up Dev Loop

1. Write code into a file.
2. Evaluate the file's namespace and make sure it loads correctly with:

```
./bin/mage -repl --namespace metabase.app-db.connection
```

3. Call functions in the namespace with test inputs, and observe that the outputs are correct
   Feel free to copy these REPL session trials into actual test cases using `deftest` and `is`.
4. Once you know these functions are good, return to 1, and compose them into the task that you need to build.

## Critical Rules for Editing

- Be careful with parentheses counts when editing Clojure code
- After EVERY change to Clojure code, verify readability with `-check-readable`
- End all files with a newline
- When editing tabular code, where the columns line up, try to keep them aligned
- Spaces on a line with nothing after it is not allowed
