---
name: moonbit
description: MoonBit language development best practices for AI agents. Use when writing, refactoring, or testing MoonBit code, working with moon tooling (build/check/test/fmt/info), navigating MoonBit projects, or following MoonBit-specific conventions for syntax, testing, and project layout.
---

# MoonBit Development Guide

## Quick Start

MoonBit is an expression-oriented language with garbage collection (no lifetimes/ownership). Key characteristics:
- **Expression-oriented**: `if`, `match`, loops return values
- **Block separator**: Use `///|` between top-level declarations
- **Error handling**: Checked errors with `raise` keyword, automatic propagation
- **Packages**: No `import` in code; configure in `moon.pkg`/`moon.pkg.json`

## Agent Workflow

Follow this order for reliable task execution:

1. **Clarify goal** - Confirm expected behavior and constraints
2. **Locate boundaries** - Find `moon.mod.json` (module root) and relevant `moon.pkg` files
3. **Discover APIs** - Use `moon ide doc` before coding
4. **Refactor semantically** - Use `moon ide rename` for symbol renaming
5. **Edit locally** - Keep changes package-local with `///|` delimiters
6. **Validate** - Run `moon check` regularly, then targeted tests
7. **Finalize** - Run `moon fmt` and `moon info` before completion

## Essential Commands

| Command | Purpose |
|---------|---------|
| `moon check` | Fast type check (use frequently) |
| `moon test` | Run tests |
| `moon test -u` | Update snapshot tests |
| `moon test --filter 'glob'` | Run specific tests |
| `moon fmt` | Format code |
| `moon info` | Generate `.mbti` interface files |
| `moon ide doc "query"` | Discover APIs |
| `moon ide outline .` | List package symbols |
| `moon ide rename sym new` | Rename symbol project-wide |

## Common Syntax

```moonbit
///|
/// Block separator (///|) required between top-level items

///|
/// Function with type parameter
fn[T] identity(val: T) -> T { val }

///|
/// Error handling with raise
fn parse(s: String) -> Int raise ParseError {
  if s.is_empty() { raise ParseError::InvalidEof }
  // errors propagate automatically
  s.to_int()
}

///|
/// Struct with derive
struct Point {
  x: Int
  y: Int
} derive(Show, Eq, ToJson)

///|
/// Method syntax
fn Point::distance(self: Point, other: Point) -> Double {
  // ...
}
```

## Code Navigation: Prefer `moon ide` over Read/Grep

```bash
# ❌ Avoid: Reading files directly or grep
Read src/parser.mbt
grep -r "fn parse" .

# ✅ Use: Semantic navigation
moon ide peek-def Parser::parse
moon ide outline src/parser.mbt
moon ide find-references parse
moon ide doc "String::*rev*"
```

**Why**: `moon ide` provides semantic search, distinguishes definitions from call sites, and is more accurate than grep (which picks up comments).

## Critical Pitfalls to Avoid

See [references/pitfalls.md](references/pitfalls.md) for detailed explanations.

- **Variables/functions**: lowercase only (uppercase = compilation error)
- **Mutability**: `mut` only for reassignment, not field mutation (Array push doesn't need it)
- **Return**: Last expression is return value; don't use `return` unnecessarily
- **Methods**: Require `Type::` prefix
- **Operators**: No `++`/`--`; use `i += 1`
- **Error propagation**: No explicit `try` needed (unlike Swift)
- **Async**: No `await` keyword; just declare `async fn`
- **String indexing**: Returns `UInt16`, not `Char`. Use `s.get_char(i)` for `Char?`

## Project Structure

```
my_module/
├── moon.mod.json          # Module metadata
├── moon.pkg               # Root package config (or moon.pkg.json)
├── lib/
│   ├── moon.pkg           # Package config
│   └── utils.mbt
├── cmd/main/
│   ├── moon.pkg           # {"is_main": true}
│   └── main.mbt
├── lib_test.mbt           # Black-box tests
└── lib_wbtest.mbt         # White-box tests (access private members)
```

**Key rules**:
- `moon.mod.json` = module root (like Go module)
- `moon.pkg`/`moon.pkg.json` = package boundary (each directory = one package)
- File names are organizational only; all files in a package share namespace
- Move declarations freely between files in the same package

## Testing

### Snapshot Tests

```moonbit
///|
test "example" {
  let result = compute([1, 2, 3])
  inspect(result, content="")  // Run `moon test -u` to auto-fill
}
```

After `moon test -u`:
```moonbit
inspect(result, content="6")
```

Use `@json.inspect()` for complex nested structures.

### Test Organization

- Black-box by default (`*_test.mbt`) - test public APIs only
- White-box when needed (`*_wbtest.mbt`) - access private members
- Group related checks in one test block
- Panic tests: `test "panic ..." { ignore(panic_fn()) }`

## References

- [Language Fundamentals](references/language-fundamentals.md) - Core syntax and types
- [Common Pitfalls](references/pitfalls.md) - Mistakes to avoid
- [Build Configuration](references/build-config.md) - moon.mod.json and moon.pkg
- [IDE Tools](references/ide-tools.md) - moon ide commands
- [API Discovery](references/api-discovery.md) - Using moon doc
- [Testing Guide](references/testing-guide.md) - Comprehensive testing patterns
- [Refactoring Guide](references/refactoring.md) - Safe refactoring workflows

## Task Playbooks

### Bug Fix (No API Change)

1. Reproduce failing behavior
2. Locate symbols with `moon ide`
3. Implement minimal fix
4. Validate: `moon check`, `moon test [scope]`, `moon fmt`, `moon info`

### Refactor (Behavior Preserving)

1. Confirm behavior invariants
2. Use `moon ide rename` for semantic refactoring
3. Keep edits package-local
4. Validate: API unchanged in `.mbti` files

### New Feature/Public API

1. Discover idioms with `moon ide doc`
2. Add implementation with docstring examples
3. Add black-box tests
4. Validate: `moon check`, `moon test`, `moon fmt`, `moon info` (review `.mbti` changes)
