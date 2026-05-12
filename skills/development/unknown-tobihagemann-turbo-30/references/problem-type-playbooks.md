# Problem Type Playbooks

Type-specific investigation strategies. Load the playbook matching the classified type from Phase 1.

## Runtime Error

**First moves**: Read the full stack trace. Identify the throwing function and read it completely. Read the caller that passed the bad input.

**Common root causes**: null/undefined access, missing error handling, race condition, stale state, incorrect type coercion, dependency version mismatch, missing environment variable.

**Tool sequence**: Read (stack trace files, full functions) → Grep (error message across codebase — is it caught elsewhere?) → Bash (`git blame` on the throwing line) → Bash (reproduce with verbose logging or `DEBUG=*`)

## Test Failure

**First moves**: Read the failing test assertion and the expected vs actual values. Read the function under test completely. Check if the test was recently modified or if the SUT was.

**Common root causes**: Logic change without test update, test relying on execution order or timing, mock returning stale data, shared mutable state between tests, assertion on wrong field.

**Tool sequence**: Bash (run single failing test in isolation) → Read (test file + SUT) → Bash (`git log -5 -- <test-file> <sut-file>`) → Grep (shared state or global setup referenced by the test)

## Build Failure

**First moves**: Read the full build error output. Identify the file and line referenced. Check for recent config changes.

**Common root causes**: Missing import/export, circular dependency, incompatible dependency version, config syntax error, missing build step, stale cache.

**Tool sequence**: Read (referenced file at error line) → Bash (`git diff HEAD~3 -- <config-files>`) → Bash (clean build: `rm -rf dist node_modules/.cache && npm run build`) → Grep (the missing symbol or module name)

## Type Error

**First moves**: Read the type error message carefully — it contains the expected and actual types. Read the function signature and the call site.

**Common root causes**: Function signature changed without updating callers, generic type inference failure, missing type narrowing (null check), incompatible library type update, `any` masking a real type mismatch.

**Tool sequence**: Read (error file at error line, plus the type definition) → Grep (the type name — find where it's defined and how it's used) → Bash (`git log -5 -- <type-definition-file>`)

## Performance

**First moves**: Establish a baseline measurement (time, memory, CPU). Identify the hot path — what operation is slow?

**Common root causes**: N+1 queries, missing index, unbounded loop, excessive re-rendering, large payload serialization, synchronous blocking on async path, memory leak from unclosed resources.

**Tool sequence**: Bash (profile or time the operation) → Read (the hot path code) → Grep (database queries, API calls, or loops in the hot path) → Bash (add timing instrumentation around suspected sections, re-run)

## Unexpected Behavior

**First moves**: Define the expected behavior precisely. Define what actually happens. Identify the code path that should produce the expected behavior and trace it.

**Common root causes**: Wrong conditional logic (off-by-one, inverted check), stale cache or memoization, event handler on wrong element, config override silently changing behavior, feature flag in unexpected state.

**Tool sequence**: Read (the code path from input to output) → Bash (add logging at decision points, reproduce) → Grep (the config key or feature flag name) → Bash (`git log --all -S '<suspicious-value>' -- <file>` to find when the behavior changed)
