---
name: fuzz-testing
description: Fuzzing for finding edge cases and crashes
category: Testing-BDD
---

# Skill: fuzz-testing

## What I do

I guide fuzzing strategy: use Go's built-in fuzz testing to discover edge cases, crashes, and unexpected behaviour by feeding random and mutated inputs to functions. Covers target selection, corpus management, and crash analysis.

## When to use me

- Testing parsers, validators, or serialisation functions
- Finding edge cases in string/data processing
- Discovering panic-inducing inputs
- Hardening public API surfaces
- After fixing a bug (add crash input to corpus)

## Core principles

1. **Fuzz boundaries** - Focus on functions that parse, validate, or transform input
2. **Start with a seed corpus** - Provide known-good inputs as starting points
3. **Run long enough** - Short runs miss rare crashes (minimum 30 seconds)
4. **Fix crashes, add to corpus** - Every crash input becomes a regression test
5. **Fuzz one function at a time** - Isolated targets give clearer results

## Target selection

```
GOOD FUZZ TARGETS (high value)
  Parsers (JSON, YAML, custom formats)
  Validators (email, URL, date strings)
  Serialisation/deserialisation
  String manipulation functions
  Type conversion functions

POOR FUZZ TARGETS (low value)
  Simple getters/setters
  Database queries (need infrastructure)
  UI rendering functions
  Functions with no error paths
```

## Patterns & examples

**Basic Go fuzz test:**
```go
func FuzzParseDate(f *testing.F) {
    // Seed corpus with known inputs
    f.Add("2024-01-15")
    f.Add("2023-12-31")
    f.Add("")
    f.Add("not-a-date")

    f.Fuzz(func(t *testing.T, input string) {
        result, err := ParseDate(input)
        if err != nil {
            return // Invalid input is fine, just don't panic
        }
        // Valid parse should round-trip
        output := result.Format("2006-01-02")
        if output != input {
            t.Errorf("round-trip failed: %q -> %q", input, output)
        }
    })
}
```

**Running fuzz tests:**
```bash
# Run for 30 seconds
go test -fuzz=FuzzParseDate -fuzztime=30s ./...

# Run until crash found
go test -fuzz=FuzzParseDate ./...

# Run specific crash case
go test -run=FuzzParseDate/corpus_entry ./...
```

**Crash analysis workflow:**
```
1. Fuzz finds crash → saved to testdata/fuzz/<TestName>/
2. Read crash input file to understand the trigger
3. Write a unit test reproducing the crash
4. Fix the code
5. Crash file stays as regression corpus
6. Re-run fuzz to verify fix
```

**Asserting properties (not values):**
```go
f.Fuzz(func(t *testing.T, input string) {
    result := Sanitise(input)
    // Property: output never contains script tags
    if strings.Contains(result, "<script") {
        t.Errorf("sanitise failed to remove script: %q", input)
    }
    // Property: output length <= input length
    if len(result) > len(input) {
        t.Errorf("sanitise expanded input: %d > %d", len(result), len(input))
    }
})
```

## Anti-patterns to avoid

- ❌ Fuzzing with no seed corpus (random inputs alone miss structured edge cases)
- ❌ Running for only a few seconds (too short to explore input space)
- ❌ Ignoring crash files (they're free regression tests)
- ❌ Fuzzing functions with external dependencies (isolate with interfaces)
- ❌ Asserting exact values instead of properties (fuzz inputs are random)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Fuzz Testing.md`

## Related skills

- `prove-correctness` - Property-based testing complements fuzzing
- `bdd-workflow` - Write unit test for crash, then fix
- `golang` - Go-specific fuzzing API
- `security` - Fuzzing for security vulnerabilities
- `benchmarking` - Performance fuzzing for algorithmic complexity
