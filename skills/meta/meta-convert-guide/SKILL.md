---
name: meta-convert-guide
description: Guide for translating code between programming languages. Use when converting code from one language to another, planning language migrations, understanding conversion challenges, asking about type mappings, idiom translations, or referencing pattern mappings. Covers APTV workflow, type systems, error handling, concurrency, and language-specific gotchas.
---

# Language Conversion Guide

Comprehensive patterns and strategies for converting code between programming languages.

## Quick Navigation

| Resource                                                 | Purpose                               |
| -------------------------------------------------------- | ------------------------------------- |
| [FORMS.md](./FORMS.md)                                   | Templates, checklists, decision trees |
| [tables/quick-reference.md](./tables/quick-reference.md) | Condensed lookup tables               |

### Examples

| File                                                             | Content                                      |
| ---------------------------------------------------------------- | -------------------------------------------- |
| [examples/idiom-translation.md](./examples/idiom-translation.md) | Null handling, collections, pattern matching |
| [examples/error-handling.md](./examples/error-handling.md)       | Exception→Result, error hierarchies          |
| [examples/concurrency.md](./examples/concurrency.md)             | Promise/Future, parallel execution           |
| [examples/metaprogramming.md](./examples/metaprogramming.md)     | Decorators, macros, DI patterns              |
| [examples/serialization.md](./examples/serialization.md)         | JSON, validation, polymorphic types          |

### Reference Guides

| File                                                                           | Content                            |
| ------------------------------------------------------------------------------ | ---------------------------------- |
| [reference/difficulty-matrix.md](./reference/difficulty-matrix.md)             | Conversion difficulty ratings      |
| [reference/type-system-mapping.md](./reference/type-system-mapping.md)         | Primitives, composites, generics   |
| [reference/error-handling.md](./reference/error-handling.md)                   | Error models, let-it-crash         |
| [reference/concurrency.md](./reference/concurrency.md)                         | Async models, channels, goroutines |
| [reference/dev-workflow-repl.md](./reference/dev-workflow-repl.md)             | 9th pillar, REPL patterns          |
| [reference/memory-ownership.md](./reference/memory-ownership.md)               | GC→ownership, borrowing            |
| [reference/evaluation-strategy.md](./reference/evaluation-strategy.md)         | Lazy vs eager patterns             |
| [reference/metaprogramming.md](./reference/metaprogramming.md)                 | Macros, reflection, code gen       |
| [reference/type-system-translation.md](./reference/type-system-translation.md) | Static↔dynamic, inference         |
| [reference/paradigm-translation.md](./reference/paradigm-translation.md)       | OOP→FP, FP→FP                      |
| [reference/serialization.md](./reference/serialization.md)                     | Library mapping, attributes        |
| [reference/typescript-patterns.md](./reference/typescript-patterns.md)         | Type guards, mapped types          |
| [reference/hkt-type-classes.md](./reference/hkt-type-classes.md)               | HKTs, Functor, Monad               |
| [reference/async-patterns.md](./reference/async-patterns.md)                   | Cancellation, streams              |
| [reference/dependency-management.md](./reference/dependency-management.md)     | Package ecosystems                 |
| [reference/performance.md](./reference/performance.md)                         | Pitfalls, benchmarking             |

### Gotchas

| File                                                                   | Content                              |
| ---------------------------------------------------------------------- | ------------------------------------ |
| [reference/gotchas/by-family.md](./reference/gotchas/by-family.md)     | OOP→FP, Dynamic→Static, GC→Ownership |
| [reference/gotchas/by-language.md](./reference/gotchas/by-language.md) | Python→Rust, TypeScript→Rust, etc.   |

---

## When to Use This Skill

- Converting code from one language to another
- Planning a language migration
- Understanding conversion challenges between languages
- Looking up type mappings or idiom translations
- Referencing error handling, concurrency, or async patterns across languages
- Learning about gotchas when converting between specific language families

## This Skill Does NOT Cover

- Creating new conversion skills (see `meta-convert-dev`)
- Language tutorials (see `lang-*-dev` skills)
- Runtime interop/FFI (see language-specific interop skills)

## Related Skills

- `meta-convert-dev` - For creating new `convert-X-Y` skills
- `convert-*` skills - Language-pair specific conversion skills

---

## Core Conversion Methodology

### The APTV Workflow

Every conversion follows: **Analyze → Plan → Transform → Validate**

```asciidoc
┌─────────────────────────────────────────────────────────────┐
│                    CONVERSION WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│  1. ANALYZE    │  Understand source code structure          │
│                │  • Parse and identify components            │
│                │  • Map dependencies                         │
│                │  • Identify language-specific patterns      │
├─────────────────────────────────────────────────────────────┤
│  2. PLAN       │  Design the target architecture            │
│                │  • Create type mapping table                │
│                │  • Identify idiom translations              │
│                │  • Plan module/package structure            │
├─────────────────────────────────────────────────────────────┤
│  3. TRANSFORM  │  Convert code systematically               │
│                │  • Types and interfaces first               │
│                │  • Core logic second                        │
│                │  • Adopt target idioms (don't transliterate)│
├─────────────────────────────────────────────────────────────┤
│  4. VALIDATE   │  Verify functional equivalence             │
│                │  • Run original tests against new code      │
│                │  • Property-based testing for edge cases    │
│                │  • Performance comparison if relevant       │
└─────────────────────────────────────────────────────────────┘
```

> **See also:** [FORMS.md](./FORMS.md) for APTV phase checklists

### Analyze Phase

Before writing any target code:

1. **Parse the source** - Understand structure, not just syntax
2. **Identify components**:
   - Types/interfaces/classes
   - Functions/methods
   - Module boundaries
   - External dependencies
3. **Note language-specific features**:
   - Generics usage
   - Error handling patterns
   - Async patterns
   - Memory management approach

### Plan Phase

Create explicit mappings before transforming. Use the templates in [FORMS.md](./FORMS.md):

```markdown
## Type Mapping Table

| Source (TypeScript) | Target (Rust)      | Notes             |
| ------------------- | ------------------ | ----------------- |
| `string`            | `String` / `&str`  | Owned vs borrowed |
| `number`            | `i32` / `f64`      | Specify precision |
| `T[]`               | `Vec<T>`           | Owned collection  |
| `T \| null`         | `Option<T>`        | Nullable handling |
| `Promise<T>`        | `Future<Output=T>` | Async handling    |
```

> **See also:** [reference/type-system-mapping.md](./reference/type-system-mapping.md) for complete mappings

### Transform Phase

**Golden Rule: Adopt target idioms, don't write "Source code in Target syntax"**

```typescript
// Source: TypeScript
function findUser(id: string): User | null {
  const user = users.find((u) => u.id === id);
  return user || null;
}
```

```rust
// BAD: Transliterated (TypeScript in Rust clothing)
fn find_user(id: String) -> Option<User> {
    let user = users.iter().find(|u| u.id == id);
    match user {
        Some(u) => Some(u.clone()),
        None => None,
    }
}

// GOOD: Idiomatic Rust
fn find_user(id: &str) -> Option<&User> {
    users.iter().find(|u| u.id == id)
}
```

> **See also:** [examples/idiom-translation.md](./examples/idiom-translation.md) for more patterns

### Validate Phase

1. **Functional equivalence**: Same inputs → same outputs
2. **Edge case coverage**: Property-based tests
3. **Error behavior**: Same error conditions trigger appropriately
4. **Performance baseline**: Comparable or better performance

> **See also:** [FORMS.md](./FORMS.md) for testing strategy checklist

---

## The 8 Pillars of Conversion

Every comprehensive conversion addresses these domains:

| Pillar                     | What to Convert                | Reference                                                                  |
| -------------------------- | ------------------------------ | -------------------------------------------------------------------------- |
| 1. **Module System**       | Imports, exports, packages     | [reference/type-system-mapping.md](./reference/type-system-mapping.md)     |
| 2. **Error Handling**      | Exceptions, Results, panics    | [reference/error-handling.md](./reference/error-handling.md)               |
| 3. **Concurrency**         | Async, threads, channels       | [reference/concurrency.md](./reference/concurrency.md)                     |
| 4. **Metaprogramming**     | Decorators, macros, reflection | [reference/metaprogramming.md](./reference/metaprogramming.md)             |
| 5. **Zero/Default Values** | Nullability, defaults          | [reference/type-system-mapping.md](./reference/type-system-mapping.md)     |
| 6. **Serialization**       | JSON, validation, schemas      | [reference/serialization.md](./reference/serialization.md)                 |
| 7. **Build System**        | Package managers, dependencies | [reference/dependency-management.md](./reference/dependency-management.md) |
| 8. **Testing**             | Test frameworks, assertions    | [FORMS.md](./FORMS.md)                                                     |

### The 9th Pillar: Dev Workflow

For REPL-centric languages (Clojure, Elixir, Haskell), add:

| Source          | Target    | Consideration             |
| --------------- | --------- | ------------------------- |
| REPL-centric    | Compiled  | Document workflow changes |
| Hot reload      | Recompile | Faster incremental builds |
| Live inspection | Debugging | Logger, debugger setup    |

> **See also:** [reference/dev-workflow-repl.md](./reference/dev-workflow-repl.md)

---

## Quick Reference Tables

### Type System Comparison

| Language   | Typing      | Null Safety         | Generics   |
| ---------- | ----------- | ------------------- | ---------- |
| TypeScript | Static      | Optional (`strict`) | Full       |
| Python     | Dynamic     | None (runtime)      | Type hints |
| Rust       | Static      | Enforced (`Option`) | Full       |
| Go         | Static      | Nil pointers        | 1.18+      |
| Elixir     | Dynamic     | nil atoms           | None       |
| Haskell    | Static (HM) | Enforced (`Maybe`)  | Full + HKT |

> **See also:** [tables/quick-reference.md](./tables/quick-reference.md) for complete tables

### Error Model Comparison

| Language   | Model         | Propagation                |
| ---------- | ------------- | -------------------------- |
| TypeScript | Exceptions    | `throw` / `try-catch`      |
| Python     | Exceptions    | `raise` / `try-except`     |
| Rust       | Result type   | `?` operator               |
| Go         | Error returns | `if err != nil`            |
| Elixir     | Pattern match | `{:ok, _}` / `{:error, _}` |
| Haskell    | Either/Maybe  | Monadic bind               |

> **See also:** [reference/error-handling.md](./reference/error-handling.md)

### Concurrency Model Comparison

| Language   | Model      | Primitives            |
| ---------- | ---------- | --------------------- |
| TypeScript | Event loop | Promises, async/await |
| Python     | Event loop | asyncio, await        |
| Rust       | Futures    | tokio, async/await    |
| Go         | CSP        | Goroutines, channels  |
| Elixir     | Actors     | Processes, GenServer  |
| Erlang     | Actors     | Processes, mailboxes  |

> **See also:** [reference/concurrency.md](./reference/concurrency.md)

---

## Common Conversion Patterns

### Null Handling

| Source           | Target Rust            | Pattern           |
| ---------------- | ---------------------- | ----------------- |
| `x ?? default`   | `x.unwrap_or(default)` | Default value     |
| `x?.prop`        | `x.map(\|v\| v.prop)`  | Optional chaining |
| `if (x != null)` | `if let Some(v) = x`   | Null check        |

> **See also:** [examples/idiom-translation.md](./examples/idiom-translation.md)

### Error Propagation

| Source                 | Target                                         | Pattern           |
| ---------------------- | ---------------------------------------------- | ----------------- |
| `throw new Error(msg)` | `return Err(Error::new(msg))`                  | Throw → Result    |
| `try { } catch { }`    | `match result { Ok(_) => ..., Err(_) => ... }` | Try/catch → match |
| Rethrow                | `?` operator                                   | Propagate error   |

> **See also:** [examples/error-handling.md](./examples/error-handling.md)

### Collection Operations

| Source (JS/TS)     | Target (Rust)           | Notes               |
| ------------------ | ----------------------- | ------------------- |
| `.map(f)`          | `.iter().map(f)`        | Lazy in Rust        |
| `.filter(f)`       | `.iter().filter(f)`     | Lazy in Rust        |
| `.reduce(f, init)` | `.iter().fold(init, f)` | Different arg order |
| `.find(f)`         | `.iter().find(f)`       | Returns Option      |

> **See also:** [tables/quick-reference.md](./tables/quick-reference.md)

---

## Decision Trees

### When to Clone vs Borrow

```
Is the data needed after the function returns?
├─ NO → Borrow (&T)
└─ YES → Does caller need to keep using it?
         ├─ NO → Move (T)
         └─ YES → Clone (.clone())
```

> **See also:** [FORMS.md](./FORMS.md) for complete decision trees

### GC → Ownership Strategy

```
Is this data shared across components?
├─ YES → Consider Arc<T> or Rc<T>
└─ NO → Single owner, use moves

Is this data mutated by multiple parts?
├─ YES → Arc<Mutex<T>> or channels
└─ NO → Immutable borrows (&T)
```

> **See also:** [reference/memory-ownership.md](./reference/memory-ownership.md)

---

## Common Pitfalls

| Pitfall                   | Wrong                           | Right                 |
| ------------------------- | ------------------------------- | --------------------- |
| **Transliteration**       | Write TypeScript in Rust syntax | Write idiomatic Rust  |
| **Ignoring idioms**       | Port class hierarchies to Rust  | Use enums and traits  |
| **1:1 mapping**           | Every function maps exactly     | Restructure as needed |
| **Preserve inefficiency** | Port inefficient algorithms     | Optimize for target   |
| **Ignore conventions**    | camelCase in Python             | snake_case (Python)   |

> **See also:** [reference/gotchas/by-family.md](./reference/gotchas/by-family.md)

---

## Testing Conversions

### Testing Pyramid

```asciidoc
         ┌───────────────┐
         │  Integration  │  Same API behavior
         └───────────────┘
    ┌─────────────────────────┐
    │    Property-Based       │  Invariants hold
    └─────────────────────────┘
 ┌───────────────────────────────────┐
 │           Unit Tests              │  Logic matches
 └───────────────────────────────────┘
┌─────────────────────────────────────────┐
│        Input/Output Comparison          │  Golden tests
└─────────────────────────────────────────┘
```

### Golden Testing

1. Generate test cases from original implementation
2. Save as JSON fixtures
3. Run converted code against same inputs
4. Compare outputs

> **See also:** [FORMS.md](./FORMS.md) for testing checklist

---

## Language-Specific Quick Links

### Converting FROM

| Source     | Key Gotchas                  | Reference                                                                           |
| ---------- | ---------------------------- | ----------------------------------------------------------------------------------- |
| Python     | Duck typing, None everywhere | [reference/gotchas/by-language.md](./reference/gotchas/by-language.md#python--rust) |
| TypeScript | Optional properties, any     | [reference/typescript-patterns.md](./reference/typescript-patterns.md)              |
| Go         | Zero values, nil             | [reference/gotchas/by-language.md](./reference/gotchas/by-language.md#go--rust)     |
| Java       | Null, checked exceptions     | [reference/gotchas/by-language.md](./reference/gotchas/by-language.md#java--rust)   |
| Haskell    | HKTs, laziness               | [reference/hkt-type-classes.md](./reference/hkt-type-classes.md)                    |
| Elixir     | Pattern matching, processes  | [reference/gotchas/by-language.md](./reference/gotchas/by-language.md#elixir--rust) |

### Converting TO

| Target | Key Considerations          | Reference                                                                      |
| ------ | --------------------------- | ------------------------------------------------------------------------------ |
| Rust   | Ownership, borrowing        | [reference/memory-ownership.md](./reference/memory-ownership.md)               |
| Go     | Simplicity, explicit errors | [reference/error-handling.md](./reference/error-handling.md)                   |
| Python | Dynamic typing              | [reference/type-system-translation.md](./reference/type-system-translation.md) |
| Elixir | Functional, BEAM            | [reference/paradigm-translation.md](./reference/paradigm-translation.md)       |

---

## References

### Related Skills

- `meta-convert-dev` - For creating new `convert-X-Y` skills
- `convert-typescript-rust` - TypeScript → Rust conversion
- `convert-python-rust` - Python → Rust conversion
- `convert-golang-rust` - Go → Rust conversion

### Language Skills

For language-specific fundamentals (not conversion):

- `lang-typescript-dev` - TypeScript development patterns
- `lang-python-dev` - Python development patterns
- `lang-rust-dev` - Rust development patterns
- `lang-elixir-dev` - Elixir development patterns
