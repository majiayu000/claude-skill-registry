---
name: moonbit-refactoring
description: Refactor MoonBit codebases by minimizing public APIs, modularizing packages,
  converting free functions to methods/chaining, using ArrayView/StringView pattern
  matching, adding Dafny-style loop specs,
---

---
name: moonbit-refactoring
description: Refactor MoonBit code to be idiomatic: shrink public APIs, convert functions to methods, use pattern matching with views, add loop invariants, and ensure test coverage without regressions.
---

# MoonBit Refactoring Skill

## Intent
- Preserve behavior and public contracts unless explicitly changed.
- Minimize the public API to what callers require.
- Prefer declarative style and pattern matching over incidental mutation.
- Use view types (ArrayView/StringView/BytesView) to avoid copies.
- Add tests and docs alongside refactors.

## Workflow
**Start broad, then refine locally:**

1. **Architecture first**: Review package structure, dependencies, and API boundaries.
2. **Inventory** public APIs and call sites (`moon doc`, `moon ide find-references`).
3. **Pick one refactor theme** (API minimization, package splits, pattern matching, loop style).
4. **Apply the smallest safe change**.
5. **Update docs/tests** in the same patch.
6. **Run `moon check`, then `moon test`**.
7. **Use coverage** to target missing branches.

Avoid local cleanups (renaming, pattern matching) until the high-level structure is sound.

## Improve Package Architecture
- Keep packages focused: aim for <10k lines per package.
- Keep files manageable: aim for <2k lines per file.
- Keep functions focused: aim for <200 lines per function.

### Splitting Files
Files in MoonBit are just organizational—move code freely within a package as long as each file stays focused on one concept.

### Splitting Packages
When spinning off package `A` into `A` and `B`:

1. Create the new package and re-export temporarily:
   ```mbt
   // In package B
   using @A { ... }  // re-export A's APIs
   ```
   Ensure `moon check` passes before proceeding.

2. Find and update all call sites:
   ```bash
   moon ide find-references <symbol>
   ```
   Replace bare `f` with `@B.f`.

3. Remove the `use` statement once all call sites are updated.

4. Audit and remove newly-unused `pub` APIs from both packages.

### Guidelines
- Prefer acyclic dependencies: lower-level packages should not import higher-level ones.
- Only expose what downstream packages actually need.
- Consider an `internal/` package for helpers that shouldn't leak.

## Minimize Public API and Modularize
- Remove `pub` from helpers; keep only required exports.
- Move helpers into `internal/` packages to block external imports.
- Split large files by feature; files do not define modules in MoonBit.

## Local refactoring

### Convert Free Functions to Methods + Chaining
- Move behavior onto the owning type for discoverability.
- Use `..` for fluent, mutating chains when it reads clearly.

Example:
```mbt nocheck
// Before
fn reader_next(r : Reader) -> Char? { ... }
let ch = reader_next(r)

// After
fn Reader::next(self : Reader) -> Char? { ... }
let ch = r.next()
```

Example (chaining):
```mbt nocheck
buf..write_string("#\\")..write_char(ch)
```

### Prefer Explicit Qualification
- Use `@pkg.fn` instead of `using` when clarity matters.
- Keep call sites explicit during wide refactors.

Example:
```mbt nocheck
let n = @parser.parse_number(token)
```

### Simplify Constructors When Type Is Known
- Drop `TypePath::Constr` when the surrounding type is known.

Example:
```mbt
match tree { // the type of tree is known to be Tree
  Leaf(x) => x // no need for Tree::Leaf
  Node(left~, x, right~) => left.sum() + x + right.sum()
}
```

### Pattern Matching and Views
- Pattern match arrays directly; the compiler inserts ArrayView implicitly.
- Use `..` in the middle to match prefix and suffix at once.
- Pattern match strings directly; avoid converting to `Array[Char]`.
- `String`/`StringView` indexing yields `UInt16` code units. Use `for ch in s` for Unicode-aware iteration.

Examples:
```mbt
match items {
  [] => ()
  [head, ..tail] => handle(head, tail)
  [..prefix, mid, ..suffix] => handle_mid(prefix, mid, suffix)
}
```

```mbt
match s {
  "" => ()
  [.."let", ..rest] => handle_let(rest)
  _ => ()
}
```
#### Char literal matching

MoonBit allows char literal overloading for `Char`, `UInt16`, and `Int`, so the examples below work. This is handy when matching `String` indexing results (`UInt16`) against a char range.
```mbt
test {
  let a_int : Int = 'b'
  if (a_int is 'a'..<'z') { () } else { () }
  let a_u16 : UInt16 = 'b'
  if (a_u16 is 'a'..<'z') { () } else { () }
  let a_char : Char = 'b'
  if (a_char is 'a'..<'z') { () } else { () }
}
```

#### Use Nested Patterns and `is`

- Use `is` patterns inside `if`/`guard` to keep branches concise.

Example:
```mbt
match token {
  Some(Ident([.."@", ..rest])) if process(rest) is Some(x) => handle_at(rest)
  Some(Ident(name)) => handle_ident(name)
  None => ()
}
```

#### Prefer Range Loops for Simple Indexing
- Use `for i in start..<end { ... }`, `for i in start..<=end { ... }`, `for i in large>..small`, or `for i in large>=..small` for simple index loops.
- Keep functional-state `for` loops for algorithms that update state.

Example:
```mbt
// Before
for i = 0; i < len; {
  items.push(fill)
  continue i + 1
}

// After
for i in 0..<len {
  items.push(fill)
}
```

## Loop Specs (Dafny-Style Comments)
- Add specs for functional-state loops.
- Skip invariants for simple `for x in xs` loops.
- Add TODO when a decreases clause is unclear (possible bug).

Example:
```mbt
for i = 0, acc = 0; i < xs.length(); {
  acc = acc + xs[i]
  i = i + 1
} else { acc }
where {
  invariant: 0 <= i <= xs.length(),
  reasoning: (
    #| ... rigorous explanation ...
    #| ...
  )
}
```


### Tests and Docs
- Prefer black-box tests in `*_test.mbt` or `*.mbt.md`.
- Add docstring tests with `mbt check` for public APIs.

Example:
```mbt
///|
/// Return the last element of a non-empty array.
///
/// # Example
/// ```mbt check
/// test {
///   inspect(last([1, 2, 3]), content="3")
/// }
/// ```
pub fn last(xs : Array[Int]) -> Int { ... }
```

## Coverage-Driven Refactors
- Use coverage to target missing branches through public APIs.
- Prefer small, focused tests over white-box checks.

Commands:
```bash
moon coverage analyze -- -f summary
moon coverage analyze -- -f caret -F path/to/file.mbt
```

## Moon IDE Commands

```bash
moon doc "<query>"
moon ide outline <dir|file>
moon ide find-references <symbol>
moon ide peek-def <symbol>
moon check
moon test
moon info
```
These commands are useful for reliable refactoring.

Example: spinning off `package_b` from `package_a`.

Temporary import in `package_b`:
```mbt
using @package_a { a, type B }
```

Steps:
1. Use `moon ide find-references <symbol>` to find all call sites of `a` and `B`.
2. Replace them with `@package_a.a` and `@package_a.B`.
3. Remove the `using` statement and run `moon check`.
