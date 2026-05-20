---
name: racket-programmer
description: Racket-specific tooling, libraries, idioms, and language-oriented programming philosophy. Use when working with Racket code. Emphasizes LOP, contracts, macros, and design methodology.
---

# Racket Programmer

Expert-level Racket programming skill focused on judgment frameworks, language-oriented programming philosophy, and production practices.

**Related skills:**
- `software-engineer` - Core programming philosophy and SICP principles that underpin Racket's design
- `functional-programmer` - FP patterns and thinking (Racket is fundamentally functional)
- `test-driven-development` - General testing philosophy; this skill covers RackUnit specifics

## Version Targeting

**Always target the latest stable Racket version** unless explicitly working on a codebase with version constraints.

- Latest stable: Racket 8.18 (as of August 2025)
- Download: https://download.racket-lang.org/
- Version history: https://github.com/racket/racket/releases
- For historical context: https://en.wikipedia.org/wiki/Racket_(programming_language)#History

**Racket CS (Chez Scheme-based) is the default implementation since 8.0.** Strong backward compatibility commitment means minimal version fragmentation.

**For owned codebases:** Aggressive upgrade philosophy. Use latest features and libraries.

**For third-party codebases:** Respect existing version targets and conventions. When contributing to open source, follow the project's existing standards. Don't introduce modern features to projects targeting older versions. Propose improvements through proper channels (issues, governance).

<language_oriented_programming>
## Language-Oriented Programming: Racket's Core Philosophy

**Central Insight**: Racket's defining characteristic is building solutions as languages, not just libraries. Every problem is approached by asking "what's the right notation?" before "what's the implementation?"

This is not a feature of Racket—it IS Racket's design philosophy. Understanding this distinction separates using Racket from merely writing Scheme with extra features.

### From "The Racket Manifesto" (Felleisen et al., SNAPL 2015)

**"A programmable programming language."** Racket is designed to let programmers create languages tailored to specific problem domains. The language grows through the creation of new languages, not just new libraries.

**Key principle**: "If builders built buildings the way programmers wrote programs, then the first woodpecker that came along would destroy civilization." —Gerald Weinberg

The right notation eliminates entire classes of errors at compile time. Language design is not an esoteric activity—it's the solution to the problem of making correct code easy to write and incorrect code hard to write.

### Decision Framework: #lang vs Library vs Macro

```
Does solution need non-S-expression syntax?
  → Reader extension needed → #lang

Does solution benefit from compile-time validation of entire program?
  → Custom #%module-begin → #lang

Just adding new operations/abstractions?
  → Macros + provide → library

Need IDE integration (syntax coloring, specialized checks)?
  → #lang with language info

Notation precision outweighs learning curve?
  → #lang
```

### When Language-Oriented Design Excels

1. **Novice interfaces** - Create simpler notations for less-skilled programmers (HtDP teaching languages)
2. **Simplified notation** - Regular expressions, configuration DSLs where domain notation is clearer
3. **Existing notation** - BNF grammars (brag package), standard formats that users already know
4. **Intermediate compilation targets** - JSON with embedded computation, specialized formats
5. **Configuration-heavy domains** - Test specifications, API definitions where structure matters

**Essential Reading:**
- Beautiful Racket: https://beautifulracket.com/ (comprehensive LOP tutorial—**read this**)
- "Why Language-Oriented Programming?": https://beautifulracket.com/appendix/why-lop-why-racket.html
- "Creating Languages in Racket" (Flatt): https://queue.acm.org/detail.cfm?id=2068896

**Trade-offs:**
- ✅ Perfect notation-to-problem fit, early error detection via compiler, domain expert usability
- ❌ Learning curve, infrastructure maintenance overhead, tooling support complexity
- **Decision heuristic**: Use when minimum notation with maximum precision is critical

### Language Towers: Composable Language Abstractions

**Pattern**: Build languages on languages, creating towers where each layer provides abstractions for the next. Unlike traditional macros that compete, Racket macros cooperate through shared compile-time information.

**Key Paper**: "Macros that Work Together" (Flatt et al., 2012)

Racket achieves this through:
- **Partial expansion**: Macros can expand sub-forms partially, inspect results, continue with additional context
- **Definition contexts**: Macros cooperate by maintaining lexical scope through hygiene
- **Phase separation**: Compile-time vs runtime code cleanly separated

**Example**: Racket's class system is implemented as macros over struct, which is itself a macro. Each layer maintains proper scoping and composition.

This is a fundamental difference from other Lisp macro systems where macros often interfere with each other.
</language_oriented_programming>

<contracts_and_blame>
## Code as Contracts: Module Boundaries and Blame

**Core Pattern**: Modules are units of abstraction AND units of blame for contracts. Design module boundaries intentionally with this in mind.

Contracts in Racket are not optional documentation—they are executable specifications that assign blame when violated. This is fundamentally different from assertions (which blame the entire program) or types (which reject programs statically).

### Contract-Out: The Standard Pattern

```racket
(provide
  (contract-out
    [my-function (→ number? (>/c 0) boolean?)]
    [my-struct (struct/c point [real? real?])]
    [complex-fn (→i ([x number?]
                      [y (x) (>/c x)])  ; dependent contract
                     [result number?])]))
```

### Decision Framework for Contracts

```
Public API boundary?
  → REQUIRED: contract-out with precise contracts

Internal module function?
  → Optional: Consider for complex invariants

Performance-critical inner loop?
  → Profile first (contracts typically cheap, but measure)

Complex invariant (e.g., balanced tree)?
  → Use dependent contracts (→i)

Simple type-like guarantee?
  → Flat contracts (number?, string?)
```

### Contract Hierarchy

1. **Always**: Module boundaries (public APIs) - **MANDATORY for production**
2. **Often**: Complex data structures with invariants
3. **Sometimes**: Internal boundaries in large modules
4. **Rarely**: Simple, obvious functions

**Chaperone vs Impersonator Contracts:**
- **Chaperone**: Monitoring only, guarantees no behavior change (preferred)
- **Impersonator**: Can change behavior, heavier weight
- Use chaperones unless you need interposition

**Key Resources:**
- Contracts Guide: https://docs.racket-lang.org/guide/contracts.html
- Contract Reference: https://docs.racket-lang.org/reference/contracts.html
- "Contracts for Higher-Order Functions" (Findler & Felleisen): Foundational paper
</contracts_and_blame>

<macro_system>
## Macro System: Production Standards

### Decision Matrix

| Need | Tool | When to Use |
|------|------|-------------|
| Simple substitution | `define-syntax-rule` | One-off macros, prototyping |
| Multiple patterns | `syntax-rules` | Standard pattern matching, no validation |
| Validation + errors | `syntax/parse` | **Production macros (recommended)** |
| Complex compile logic | `define-syntax` + procedure | Programmatic code generation |
| Syntax templates | `with-syntax`, `quasisyntax` | Building syntax from data |

### Syntax/Parse: The Production Standard

```racket
(define-syntax (my-let stx)
  (syntax-parse stx
    [(_ ([var:id rhs:expr] ...) body:expr ...+)
     #:fail-when (check-duplicate-identifier (syntax->list #'(var ...)))
                 "duplicate variable name"
     #'(let ([var rhs] ...) body ...)]))
```

**Why syntax/parse for production:**
- ✅ Declarative pattern matching with side conditions
- ✅ Domain-specific error messages via `#:fail-when`
- ✅ Syntax classes enable reusable patterns
- ✅ Better than syntax-rules for anything non-trivial

**Essential Resources:**
- "Fear of Macros" (Greg Hendershott): https://www.greghendershott.com/fear-of-macros/all.html **(best macro tutorial—read this)**
- syntax/parse docs: https://docs.racket-lang.org/syntax/stxparse.html
- Macro debugger: https://docs.racket-lang.org/macro-debugger/

**Hygiene**: Racket macros are hygienic by default. This prevents variable capture but means you must understand syntax objects. Use `datum→syntax` only when intentionally breaking hygiene (rare cases like anaphoric macros).

### Reader Extensions: High Power, High Cost

**Decision Tree:**

```
Modify single character interpretation?
  → Readtable (make-readtable)

Embedded DSL with different syntax?
  → Readtable + #reader

Complete language with custom notation?
  → #lang + reader module

Compatible with S-expressions?
  → DON'T use reader - use macros instead!
```

**When to Extend Reader:**
- Need non-S-expression syntax (BNF, JSON-like, etc.)
- Domain notation is well-established and incompatible with parens
- Target audience uncomfortable with S-expressions
- Notation is fundamentally incompatible with Lisp syntax

**When NOT to:**
- Macros suffice (most cases!)
- Syntax is still S-expressions with new forms
- Team not ready for the complexity
- Tool support matters more than notation

**Trade-offs:**
- ✅ Perfect notation for domain, can parse existing formats
- ❌ Complexity, harder debugging, less tool support, team must learn custom syntax
</macro_system>

<structs_vs_classes>
## Structs vs Classes: The 90/10 Rule

**Decision Framework:**

```
Representing data with operations?
  → Struct (90% of use cases)

Need inheritance-based polymorphism with method overriding?
  → Class

Building GUI application?
  → Class (Racket GUI framework uses classes)

Need polymorphism but not inheritance?
  → Struct with generic interfaces (#:methods gen:custom)

Porting OO codebase?
  → Class (but consider refactoring to structs)
```

### Struct Advantages

- ✅ Lighter weight, faster
- ✅ Work with pattern matching
- ✅ Simpler mental model
- ✅ Can add methods via `#:methods` with generics
- ✅ Transparent/opaque control

### Class Use Cases

- Full OO with inheritance
- Method overriding, super calls
- Mixins and traits
- GUI programming (required by framework)

### Hybrid Approach: Structs + Generic Interfaces

```racket
(define-generics printable
  (print-it printable port))

(struct point (x y)
  #:methods gen:printable
  [(define (print-it p port)
     (fprintf port "(~a,~a)" (point-x p) (point-y p)))])
```

**Staff Guidance**: Default to structs. Only use classes when working with GUI framework, need true inheritance, or building OO framework for others. When unsure, start with structs + generics.
</structs_vs_classes>

<typed_racket>
## Typed Racket: When and Why

### Decision Framework

```
Performance-critical numeric code?
  → YES (25-50× speedups possible)

Large-scale refactoring/maintenance?
  → YES (types document invariants)

Complex data structure invariants?
  → YES (occurrence typing + refinements)

Heavy typed/untyped interaction?
  → CAUTION (contract overhead can be severe)

Exploratory/prototype code?
  → NO (friction not worth it)

Macro-heavy DSLs?
  → NO (limitations on macro usage)
```

### Language Declaration

```racket
#lang typed/racket              ; Deep types (default, full checking)
#lang typed/racket/shallow      ; Shallow types (lower overhead)
#lang typed/racket/optional     ; Optional types (no runtime cost)
```

### Occurrence Typing (Unique Feature)

Racket's type system has occurrence typing—type refinement based on predicates:

```racket
(: flexible-length (→ (U String (Listof Any)) Integer))
(define (flexible-length x)
  (if (string? x)
      (string-length x)  ; x refined to String here
      (length x)))       ; x refined to (Listof Any) here
```

This is a distinctive feature compared to most gradual type systems.

### Performance Best Practices

- Use `Float` not `Real` for numeric optimization
- Prefer structs to vectors (always optimized)
- Use typed versions of standard libraries
- Minimize boundary crossings

**Essential Resources:**
- Typed Racket Guide: https://docs.racket-lang.org/ts-guide/
- Contract Profiler: https://docs.racket-lang.org/contract-profile/
- Optimization Coach: https://docs.racket-lang.org/optimization-coach/
</typed_racket>

<functional_idioms>
## Racket-Specific Functional Idioms

**What Makes Racket FP Unique** (not generic FP advice that you already know):

### 1. Contracts as First-Class Behavioral Specifications

Not just type checking; express behavioral constraints. Contracts are values that can be computed and composed.

### 2. Macros Enable Compile-Time FP

Compile-time computation is functional programming. Phase separation keeps concerns clean.

### 3. Parameters for Dynamic Binding

Better than global variables for cross-cutting concerns:

```racket
;; Standard pattern for context
(parameterize ([current-output-port (open-output-file "log.txt")])
  (displayln "logged"))
```

Example: `current-output-port`, `current-directory`

### 4. Sequence Abstractions

```racket
;; Prefer for/* comprehensions over explicit recursion
(for/list ([x (in-range 10)]
           #:when (even? x))
  (* x x))
```

### 5. Match-Based Dispatch

```racket
(define (eval expr)
  (match expr
    [(? number? n) n]
    [`(+ ,a ,b) (+ (eval a) (eval b))]
    [`(* ,a ,b) (* (eval a) (eval b))]))
```

### When to Mutate in Racket

- Algorithm is inherently stateful (union-find, hash table implementation)
- Performance-critical after profiling shows bottleneck
- Implementing imperative interface for interop
- **Default**: Prefer functional style at module boundaries, mutation only internally
</functional_idioms>

<pattern_matching>
## Pattern Matching: When and How

**Use match when:**
- Deconstructing structured data (lists, structs, syntax)
- Dispatch on data shape
- Working with recursive data structures
- Replacing verbose accessor chains

**Don't use match for:**
- Simple conditionals (use `cond` or `if`)
- Single binding extraction (use `let`)
- Just checking predicates (use predicate directly)

**Key Patterns:**

```racket
;; Struct patterns
(match point
  [(point x y) ...])

;; Quasiquote for S-expressions
(match expr
  [`(if ,cond ,then ,else) ...])

;; Guards
(match x
  [(? number? n) ...]
  [(list a b) #:when (> a b) ...])

;; Or patterns
(match expr
  [(or (list 'add x y) (list '+ x y)) ...])
```
</pattern_matching>

<tooling_and_standards>
## Mandatory Tooling and Standards

### #lang racket/base vs #lang racket (CRITICAL)

**Decision Rule:**

```
Production library code → #lang racket/base (REQUIRED)
Scripts/demos/exploration → #lang racket (acceptable)
```

**Why racket/base for libraries:**
- Faster startup (loads only core)
- Explicit dependencies (clearer what's needed)
- Smaller dependency footprint
- Better practice for maintainability

**Quote from Beautiful Racket**: "As a rule of thumb, it's better practice to start with racket/base and use require to import what you need."

### raco fmt: The Automatic Formatter (Mandatory)

**Installation**: `raco pkg install fmt`

**Usage:**
```bash
raco fmt -i file.rkt                  # Format in-place
raco fmt --width 102 file.rkt         # Custom width (style guide default)
raco fmt --check file.rkt             # Check without modifying (CI usage)
```

**CI Integration**: Add `raco fmt --check` to fail builds on formatting violations

**What it Enforces:**
- Default 80-character width (use `--width 102` for style guide compliance)
- Max 1 consecutive blank line
- Converts to brackets `[...]` in specific contexts: `let`, `for`, `cond`, `match`, `case`
- Handles 183+ standard forms

### raco review: Linting (Mandatory for CI)

**Installation**: `raco pkg install review`

**Usage:**
```bash
raco review file.rkt
raco review .                # Review entire directory
```

**What It Detects:**
- Syntax errors
- Unused identifiers
- Variable shadowing
- Missing else clauses
- Incorrect require ordering
- Style issues

**Ignoring Warnings:**
```racket
#|review: ignore|#           ; Ignore entire file
(define x 5)  ;; review: ignore  ; Ignore line
```

### RackUnit: Testing (Mandatory)

**For general testing philosophy, see the test-driven-development skill.** Core principle: Tests are contracts that document expected behavior at module boundaries. This skill covers RackUnit-specific patterns.

**Basic Usage:**

```racket
(require rackunit)

;; Simple checks
(check-equal? actual expected "message")
(check-= actual expected epsilon)
(check-true value)
(check-pred predicate value)
(check-exn exn-predicate (thunk ...))
```

**Test Suites:**

```racket
(define my-tests
  (test-suite
   "Suite name"
   (test-case "Test 1"
     (check-equal? (foo 5) 10))
   (test-case "Test 2"
     (check-true (bar "test")))))

(run-tests my-tests)
```

**module+ test Pattern:**

```racket
#lang racket/base

(define (my-function x)
  (+ x 1))

(provide my-function)

(module+ test
  (require rackunit)
  (check-equal? (my-function 5) 6)
  (check-equal? (my-function 0) 1))
```

**Running Tests:**
```bash
raco test file.rkt              # Test single file
raco test -p package-name       # Test entire package
```

### Scribble: Documentation (Mandatory for Production)

**Basic Document Structure:**

```racket
#lang scribble/manual
@(require (for-label racket my-lib))

@title{My Library}

@defmodule[my-lib]

@defproc[(my-function [arg1 string?] [arg2 integer?])
         boolean?]{
  Description of what the function does.

  @examples[
    #:eval my-eval
    (my-function "hello" 42)
  ]
}
```

**MANDATORY**: All exported bindings in production code must have Scribble documentation.

**Building:**
```bash
scribble --html manual.scrbl
raco setup --doc-index --pkgs my-package
```

## Code Style: Mandatory for Production

### Official Style Guide

**Primary Resource**: https://docs.racket-lang.org/style/index.html

**Critical Rules:**

1. **Parentheses**: ALL closing parens on LAST line (never on separate lines)
2. **Indentation**: Use DrRacket's "indent all" as STANDARD (no tabs, spaces only)
3. **Line width**: 102 characters maximum
4. **Naming**: kebab-case with full English words (NOT camelCase, NOT snake_case)
5. **End files with newline**, no trailing whitespace

### Naming Conventions (Mandatory)

| Character | Meaning | Example |
|-----------|---------|---------|
| `?` | Predicates | `boolean?`, `even?` |
| `!` | Mutators | `set!`, `vector-set!` |
| `%` | Classes | `button%`, `frame%` |
| `<>` | Interfaces | `dc<%>`, `window<%>` |
| `^` | Unit signatures | `game-context^` |
| `@` | Units | `testing-context@` |
| `#%` | Kernel forms | `#%app`, `#%module-begin` |
| `/` | "with" preposition | `call/cc`, `for/list` |

**Standard Pattern**: `type-operation` (e.g., `string-append`, `hash-ref`, `list->vector`)

### File Organization

```racket
#lang racket/base          ; Language line (first line)

;; Exports (provide forms first, ideally)
(provide (contract-out
           [function (→ Type Type)]
           [struct-name ...]))

;; Imports (require forms grouped)
(require racket/list
         racket/match
         (for-syntax racket/base))

;; Implementation
(define ...)
(struct ...)
```

## Project Layout: The lib/test/doc Pattern

### Multi-Collection Package Structure (Production Standard)

For non-trivial libraries:

```
my-library/
  my-library-lib/         # Runtime code only
    info.rkt
    main.rkt
    core/
      module1.rkt

  my-library-test/        # Tests only
    info.rkt
    tests/
      test-module1.rkt

  my-library-doc/         # Documentation only
    info.rkt
    scribblings/
      my-library.scrbl

  my-library/             # Composite meta-package
    info.rkt              # Aggregates all components
```

**Why This Pattern:**
1. ✅ **Focused dependencies** - Apps depend only on `-lib`, not test/doc deps
2. ✅ **Minimizes failure points** - Doc build failures don't break library installation
3. ✅ **Efficiency** - Users download only what they need
4. ✅ **Flexibility** - Can install just tests or just docs

**Authoritative Resource**: https://countvajhula.com/2022/02/22/how-to-organize-your-racket-library/

### Single-Collection Package (Simple Projects)

For small libraries:

```
my-simple-lib/
  main.rkt
  helper.rkt
  tests/
    main-test.rkt
  scribblings/
    my-simple-lib.scrbl
  info.rkt
```

## Package Management: raco pkg

**Core Commands:**
```bash
raco pkg install package-name     # From catalog
raco pkg install github://user/repo/branch
raco pkg update package-name
raco pkg update --all
raco pkg remove package-name --auto  # Remove + unused deps
raco pkg show --all                  # List all packages
```

**Declaring Dependencies in info.rkt (MANDATORY):**

```racket
#lang info

(define deps
  '("base"                           # Always required
    "rackunit-lib"
    "web-server-lib"
    ["other-package" "2.0"]))        # Version constraint

(define build-deps
  '("scribble-lib"                   # For docs
    "racket-doc"))                   # For doc cross-refs
```

**Key Fields:**
- `deps`: Runtime dependencies (REQUIRED)
- `build-deps`: Build-time only (tests, docs)
- `implies`: Re-exports for meta-packages
</tooling_and_standards>

<ci_cd_integration>
## CI/CD Integration (MANDATORY for Production)

**GitHub Actions Standard Setup:**

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        racket-version: ['8.16', '8.17', 'stable']
        variant: ['CS']

    steps:
      - uses: actions/checkout@v3

      - name: Setup Racket
        uses: Bogdanp/setup-racket@v1.14
        with:
          architecture: 'x64'
          distribution: 'full'
          variant: ${{ matrix.variant }}
          version: ${{ matrix.racket-version }}

      - name: Install Dependencies
        run: raco pkg install --auto --batch

      - name: Check Dependencies
        run: raco setup --check-pkg-deps --pkgs my-package

      - name: Run Tests
        run: raco test --package my-package

      - name: Build Documentation
        run: raco setup --doc-index --pkgs my-package

      - name: Lint Code
        run: |
          raco pkg install --auto review
          raco review .

      - name: Check Formatting
        run: |
          raco pkg install --auto fmt
          raco fmt --check .
```

**What MUST Fail Builds:**
1. ✅ `raco test` failures (REQUIRED)
2. ✅ `raco setup --check-pkg-deps` failures (REQUIRED)
3. ✅ `raco review` violations (RECOMMENDED)
4. ✅ `raco fmt --check` failures (if using formatter)
5. ✅ Documentation build failures (RECOMMENDED)
</ci_cd_integration>

<common_mistakes>
## Common Mistakes from Other Languages

<from_scheme>
### From Scheme (R5RS/R6RS/R7RS)

**Key Differences:**

1. **Immutable Pairs by Default**: Racket pairs are immutable. No `set-car!`/`set-cdr!`. Use `mcons`/`mcar`/`mcdr` for mutable pairs.

2. **Module System**: Racket's modules are NOT R6RS-compatible. Must use `#lang racket` not R6RS module syntax.

3. **Letrec Semantics**: Racket's `letrec` is sequential (like R6RS `letrec*`), not R5RS `letrec`.

4. **Case Sensitivity**: Racket is case-sensitive by default (R5RS was case-insensitive).

5. **Pattern Matching**: Not in standard Scheme; heavily used in Racket. Learn `match`.

**Resources:**
- Standards Compatibility: https://docs.racket-lang.org/guide/standards.html
</from_scheme>

<from_common_lisp>
### From Common Lisp

**Major Differences:**

1. **Lisp-1 vs Lisp-2**: Racket has unified namespace. No `funcall`, no `#'` notation. Functions are first-class values.
   ```racket
   ;; Racket (Lisp-1):
   (map f list)

   ;; NOT: (mapcar #'f list)
   ```

2. **Hygienic Macros**: Racket uses `syntax-case`/`syntax-rules` (hygienic), not `defmacro` (unhygienic). Variable capture prevented automatically.

3. **nil vs #f**: CL conflates false and empty list. Racket separates `#f` and `'()`.

4. **No CLOS**: Racket's class system is fundamentally different from CLOS. Prefer structs in Racket.

5. **Package vs Module**: Different semantics. Racket modules are lexically scoped, not global like CL packages.
</from_common_lisp>

<from_clojure>
### From Clojure

**The #1 Issue: Collections**

**Clojure Advantages Racket Lacks:**
- Persistent data structures for ALL collections (vectors, maps, sets)
- Uniform polymorphic interface (`assoc`, `conj`, `get`)
- Syntactic support: `{:a 1}` for maps, `[1 2 3]` for vectors
- Hash tables as lightweight objects
- Lazy sequences by default

**Racket Weaknesses:**
- Lists are primary; vectors are mutable, fixed-length arrays
- Hash tables have inconsistent interface
- No built-in lazy sequences (library needed)
- Each collection type needs different functions

**Anti-Pattern**: Trying to use Racket hash tables like Clojure maps
```racket
;; Awkward in Racket:
(hash-set (hash-set h 'a 1) 'b 2)  ; nested updates

;; vs Clojure:
(assoc h :a 1 :b 2)
```

**Other Differences:**
- No STM (Software Transactional Memory)
- No threading macros `→` and `→→` (can be added via library)
- Vectors not persistent
- Keyword arguments different syntax

**Essential Reading**: Mark Engelberg's "Racket vs. Clojure": http://programming-puzzler.blogspot.com/2010/08/racket-vs-clojure.html
</from_clojure>

<from_haskell>
### From Haskell/FP Languages

**Type System Differences:**

1. **Dynamic by Default**: Racket is dynamically typed. Typed Racket is optional, gradual typing (not inference-based).

2. **No Purity Enforcement**: Racket allows mutation. Functions ending in `!` mutate by convention. No `IO` monad.

3. **No Automatic Currying**: Must use `curry` explicitly or lambda.

4. **Strict Evaluation**: Lists are strict, not lazy. Must explicitly use streams/generators for laziness.

5. **Pattern Matching Not in Function Definitions**: Use `match` or `cond`, not Haskell-style definition patterns.

6. **No Type Classes**: Use generic interfaces or struct methods instead.

**Anti-Patterns:**
- Expecting Haskell-level type inference
- Writing everything point-free (less readable in Racket)
- Assuming lists are lazy
- Looking for purity everywhere
</from_haskell>

<from_python>
### From Python/Imperative Languages

**The Functional Paradigm Shift:**

**Anti-Pattern #1: Global Mutable State**
```racket
;; BAD (imperative):
(define stack '())
(define (push-stack! item)
  (set! stack (cons item stack)))

;; GOOD (functional):
(define (push-stack item stack)
  (cons item stack))
```

**Anti-Pattern #2: Loops Instead of Recursion**
```python
# Python approach
def sum_list(lst):
    total = 0
    for item in lst:
        total += item
    return total
```

```racket
;; Racket approaches:
;; Recursion
(define (sum-list lst)
  (if (null? lst) 0
      (+ (car lst) (sum-list (cdr lst)))))

;; Higher-order functions
(define (sum-list lst)
  (foldl + 0 lst))
```

**Other Mistakes:**
- Looking for while/for loops → use recursion or `for/*` comprehensions
- Using `set!` frequently → prefer `define` with constants
- Ignoring tail recursion → Racket guarantees TCO, use it!
- Not using higher-order functions → learn `map`, `filter`, `fold`
</from_python>

<general_anti_patterns>
### General Anti-Patterns

**Code Organization:**
1. ❌ Closing parens on separate lines → ALL on last line
2. ❌ camelCase or snake_case → kebab-case
3. ❌ Not using pattern matching → use `match` for structured data

**Performance:**
1. ❌ `(append result (list item))` in loop → O(n²), use cons + reverse
2. ❌ `(= (length lst) 0)` → use `(null? lst)` instead
3. ❌ Duplicate recursion without memoization → exponential time

**Testing:**
1. ❌ No tests → ALWAYS write tests for production code
2. ❌ Testing implementation details → test public API only
</general_anti_patterns>
</common_mistakes>

<units_and_signatures>
## Units and Signatures: When NOT to Use

**Historical Context**: Units were inspired by ML functors. Modern Racket uses them rarely (niche feature).

**Use units ONLY when:**
- Need recursive linking between components (modules can't do this)
- Building plugin system with dynamic linking/unlinking
- Need ML-style functors for parameterization over interfaces

**Don't use for:**
- Simple module composition (99% of cases) → use modules
- Dependency injection → use parameters or functions
- Most abstraction needs → higher-order modules suffice

**Modern Alternatives:**
1. **First-class modules** - Pass modules as values
2. **Parameters** - Dynamic binding
3. **Dependency injection** - Via higher-order functions
4. **Mixins** - For OO-style composition
</units_and_signatures>

<concurrency>
## Concurrency: Places, Futures, Threads

### Futures: Parallel Computation

**Use For**: Pure computation that can run in parallel

**Common Mistakes:**

1. **Blocking Operations Kill Parallelism**
   - I/O operations block futures (not parallel)
   - Operations on shared mutable data block
   - Continuations inspection blocks

2. **Not Using futures-visualizer**
   ```bash
   racket -l future-visualizer
   ```
   Shows which operations blocked parallelism.

3. **Expecting Parallel GC**
   - GC events synchronize all futures

### Places: OS-Level Parallelism

**Use For**: True OS-level parallelism, separate memory spaces

**Common Mistakes:**

1. **Trying to Share Mutable State**
   - Places are OS processes, can't share memory
   - Use `place-channel` for message passing

### Threads: Concurrency (Not Parallelism)

**Use For**: Concurrency (I/O, event handling), not CPU parallelism

**Key Points:**
- Green threads (scheduled by runtime)
- Don't provide parallelism on their own
- Use semaphores, channels for synchronization
</concurrency>

<performance_profiling>
## Performance Profiling

**Statistical Profiler:**
```racket
(require profile)

(profile
  (my-expensive-function))
```

**Command-Line:**
```bash
PLTSTDERR="debug@profile" racket program.rkt
```

**Feature-Specific Profiler:**
```bash
raco feature-profile file.rkt     # Costs by feature (match, contracts, etc.)
raco contract-profile file.rkt    # Contract overhead breakdown
```

**Optimization Coach (DrRacket):**
- Enable: View → Show Optimization Coach
- Shows optimization opportunities
- Post-profiling mode recommends targeted changes
</performance_profiling>

<production_checklist>
## Production Code Requirements (Mandatory Checklist)

### For Production/Released Code:

**MUST HAVE:**
- ✅ Use `#lang racket/base` (not `#lang racket`) for libraries
- ✅ Complete Scribble documentation for ALL exported bindings
- ✅ Contracts on all public APIs (`contract-out`)
- ✅ Tests achieving good coverage (`rackunit`, `module+ test`)
- ✅ Correct dependency declarations in `info.rkt`
- ✅ README with installation and basic usage
- ✅ Consistent formatting via `raco fmt`
- ✅ Pass `raco review` without violations
- ✅ CI/CD setup with mandatory checks:
  - `raco test` (MUST pass)
  - `raco setup --check-pkg-deps` (MUST pass)
  - `raco review` (SHOULD pass)
  - `raco fmt --check` (SHOULD pass)
  - Documentation build (SHOULD succeed)

**SHOULD HAVE:**
- ✅ lib/test/doc package structure (for non-trivial libraries)
- ✅ Comprehensive examples in documentation
- ✅ Multiple Racket version testing (8.14+)
- ✅ Proper semantic versioning
</production_checklist>

<resources>
## Essential Resources by Category

### Core Documentation
- **Racket Guide**: https://docs.racket-lang.org/guide/ (tutorial)
- **Racket Reference**: https://docs.racket-lang.org/reference/ (specification)
- **Racket Style Guide**: https://docs.racket-lang.org/style/
- **Package Catalog**: https://pkgs.racket-lang.org/

### Language-Oriented Programming
- **Beautiful Racket**: https://beautifulracket.com/ (ESSENTIAL for LOP)
- **"Creating Languages in Racket"** (Flatt): https://queue.acm.org/detail.cfm?id=2068896
- **Racket Manifesto**: https://felleisen.org/matthias/manifesto/

### Macros
- **"Fear of Macros"**: https://www.greghendershott.com/fear-of-macros/all.html (BEST tutorial)
- **syntax/parse docs**: https://docs.racket-lang.org/syntax/stxparse.html
- **"Macros that Work Together"**: https://www.cambridge.org/core/journals/journal-of-functional-programming/article/macros-that-work-together/375043C6746405B22014D235FA4C90C3

### Typed Racket
- **Guide**: https://docs.racket-lang.org/ts-guide/
- **Reference**: https://docs.racket-lang.org/ts-reference/
- **"Design and Implementation of Typed Scheme" (POPL 2008)**: https://arxiv.org/abs/1106.2575

### Tooling
- **raco pkg**: https://docs.racket-lang.org/pkg/
- **RackUnit**: https://docs.racket-lang.org/rackunit/
- **Scribble**: https://docs.racket-lang.org/scribble/
- **raco fmt**: https://docs.racket-lang.org/fmt/
- **raco review**: https://github.com/Bogdanp/racket-review
- **Contract Profiler**: https://docs.racket-lang.org/contract-profile/

### Project Organization
- **"How to Organize Your Racket Library"**: https://countvajhula.com/2022/02/22/how-to-organize-your-racket-library/ (ESSENTIAL)

### Books
- **How to Design Programs** (HtDP): https://htdp.org/ (design methodology)
- **Beautiful Racket**: https://beautifulracket.com/ (language-oriented programming)

### Community
- **Racket Discourse**: https://racket.discourse.group/ (primary forum)
- **Discord**: https://discord.gg/6Zq8sH5
</resources>

<decision_frameworks_summary>
## Key Decision Frameworks Summary

### Language Design

```
Problem needs custom notation?
  → Try macros first
  → If macros insufficient → #lang
  → If compatible with S-expressions → definitely just macros
```

### Type System

```
Performance-critical numeric code OR large codebase?
  → Typed Racket (Deep types)

Heavy typed/untyped boundaries?
  → Shallow types or profile-guided migration

Exploratory code?
  → Stay untyped
```

### Data Structures

```
Representing data?
  → Struct (90% of cases)

Need inheritance + method overriding?
  → Class

Need polymorphism without inheritance?
  → Struct + generic interfaces
```

### Contracts

```
Public API?
  → REQUIRED: contract-out

Internal function?
  → Optional unless complex invariants

Performance critical?
  → Profile first (usually not a problem)
```

### Testing Strategy

```
Small project?
  → module+ test in same file

Library?
  → Separate test package (lib/test/doc pattern)

Always run in CI?
  → YES: raco test --package name
```
</decision_frameworks_summary>

<core_principles>
**Core Principles:**

1. **Language-oriented programming** is Racket's core strength
2. **Contracts are mandatory** for production code boundaries
3. **Tooling must run in CI/CD** with builds failing on violations
4. **Target latest stable** with aggressive upgrade philosophy
5. **Use racket/base** for libraries, save `racket` for scripts
6. **Default to structs** over classes (90% rule)
7. **Documentation is mandatory**, not optional
8. **Test everything** with rackunit in module+ test

When in doubt, study how Racket's own core libraries are organized and follow those patterns.
</core_principles>
