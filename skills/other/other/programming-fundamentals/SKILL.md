---
name: programming-fundamentals
description: Core programming concepts from variables through recursion. Covers data types (integers, floats, strings, booleans, arrays, objects), variables and scope (lexical, dynamic, block, function, global), control flow (conditionals, loops, pattern matching), functions (parameters, return values, closures, higher-order functions), recursion (base cases, call stack, tail recursion, mutual recursion), type systems (static vs dynamic, strong vs weak, type inference, generics), and error handling (exceptions, Result types, defensive programming). Use when teaching, reviewing, or diagnosing issues with fundamental programming constructs.
type: skill
category: coding
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/coding/programming-fundamentals/SKILL.md
superseded_by: null
---
# Programming Fundamentals

Programming is the act of giving precise instructions to a machine. Every program, from a one-line script to a distributed system, is built from a small set of fundamental constructs: variables that name values, control flow that directs execution, functions that encapsulate logic, types that constrain data, and error handling that manages the unexpected. This skill catalogs these constructs with emphasis on the mental models that make them learnable and the pitfalls that make them treacherous.

**Agent affinity:** hopper (practical language implementation, debugging), papert (pedagogical scaffolding, constructionist learning)

**Concept IDs:** code-variables-data-types, code-control-flow, code-input-output, code-syntax-style

## Part 1 -- Variables and Data Types

A variable is a name bound to a value. The binding may be mutable (the name can be rebound to a different value) or immutable (the binding is permanent). The value itself has a type that determines what operations are valid.

### Primitive Types

| Type | Examples | Key operations | Gotchas |
|---|---|---|---|
| Integer | 42, -7, 0 | Arithmetic, comparison, bitwise | Overflow (wrapping vs saturating vs panic) |
| Float | 3.14, -0.001, NaN | Arithmetic, comparison | IEEE 754 precision: 0.1 + 0.2 != 0.3 |
| Boolean | true, false | AND, OR, NOT, short-circuit | Truthy/falsy coercion in dynamic languages |
| Character | 'a', '\n', Unicode code point | Comparison, encoding/decoding | Char != string of length 1 in all languages |
| String | "hello", "" | Concatenation, slicing, search | Mutable vs immutable, encoding (UTF-8 vs UTF-16) |

**The floating-point trap.** IEEE 754 floats represent real numbers in binary. Most decimal fractions (0.1, 0.2, 0.3) have no exact binary representation. Comparing floats with == is almost always wrong. Use an epsilon tolerance: abs(a - b) < epsilon. For money, use integers (cents) or decimal types.

### Composite Types

**Arrays / Lists.** Ordered, indexed collections. Fixed-size arrays (C, Rust) vs dynamic arrays (Python list, JavaScript array, Java ArrayList). Index from 0 in most languages (Lua and MATLAB from 1).

**Objects / Records / Structs.** Named fields grouping related data. In OOP languages, objects also carry methods. In functional languages, records are plain data without behavior.

**Tuples.** Fixed-size, heterogeneous, ordered collections. Useful for returning multiple values from a function. Destructuring assignment extracts components.

**Maps / Dictionaries.** Key-value pairs with O(1) average lookup. Keys must be hashable (immutable in Python). Ordered by insertion in Python 3.7+ and JavaScript, unordered in most other languages.

### Scope and Lifetime

**Lexical (static) scope.** A variable is visible in the block where it is defined and all nested blocks. This is the default in most modern languages. The scope is determined by the program text, not the runtime call chain.

**Dynamic scope.** A variable is visible to the function that defined it and all functions it calls (transitively). Rare in modern languages. Emacs Lisp uses dynamic scope by default; Common Lisp offers it via special variables.

**Block scope vs function scope.** JavaScript's var is function-scoped; let and const are block-scoped. This distinction is the source of many bugs involving closures and loops.

**Lifetime.** How long a value exists in memory. Stack-allocated values live until the enclosing function returns. Heap-allocated values live until freed (manual in C, automatic via garbage collection or ownership in Rust).

**The closure capture question.** When a closure captures a variable, does it capture the variable itself (by reference) or its current value (by value)? This matters critically in loops. In JavaScript, `var` in a loop captures by reference (all closures see the same variable); `let` captures by value per iteration.

## Part 2 -- Control Flow

### Conditionals

**if/else** is the fundamental branch. Every programming language has it. The condition must evaluate to a boolean (in statically typed languages) or a truthy/falsy value (in dynamically typed languages).

**Switch/match.** Multi-way branching. C-style switch requires explicit break (fall-through by default). Modern languages (Rust match, Python match, Kotlin when) do not fall through and support pattern matching.

**Pattern matching.** Destructures values while testing conditions. Rust's match and Haskell's case are exhaustive -- the compiler ensures all patterns are covered. This eliminates entire classes of bugs.

**Ternary operator.** `condition ? true_value : false_value`. Syntactic sugar for a simple if/else that returns a value. Overuse reduces readability.

### Loops

**for loop.** Iterate a known number of times or over a collection. C-style `for (init; test; step)` vs for-each `for (item of collection)`.

**while loop.** Iterate while a condition holds. Checked before each iteration. The condition must eventually become false, or the loop never terminates.

**do-while.** Like while but the body executes at least once. Less common in modern code.

**Loop invariants.** A property that is true before the loop, maintained by each iteration, and true after the loop. Stating the invariant explicitly is the most reliable way to reason about loop correctness. Dijkstra emphasized this throughout his career.

**Infinite loops.** `while (true)` with an internal break. Used in event loops, servers, and REPL implementations. Always ensure there is a reachable exit condition.

**The off-by-one problem.** The most common loop bug. "Should I use < or <=? Start at 0 or 1?" The fix is to state the loop invariant and verify the boundary conditions: does the first iteration do the right thing? Does the last iteration do the right thing? What happens on empty input?

### Iteration vs Recursion

Every loop can be rewritten as recursion and vice versa. Loops are typically more efficient (no call stack overhead) and more readable for sequential traversal. Recursion is more natural for tree structures, mathematical definitions, and divide-and-conquer algorithms.

## Part 3 -- Functions

A function takes inputs (parameters), performs computation, and produces an output (return value). Functions are the primary unit of abstraction in programming.

### Parameters and Arguments

**Positional vs keyword.** Positional arguments are matched by order; keyword arguments by name. Python and Ruby support both. Keyword arguments improve readability for functions with many parameters.

**Default values.** Parameters with defaults can be omitted at call sites. Common pitfall in Python: mutable default arguments are shared across calls (use None as sentinel, create the mutable value inside the function).

**Variadic functions.** Accept a variable number of arguments. Python `*args`, JavaScript `...rest`, C `va_list`. Use sparingly -- they make the function signature less informative.

**Pass by value vs pass by reference.** In pass-by-value, the function receives a copy. In pass-by-reference, it receives an alias to the original. Most languages use pass-by-value for primitives and pass-by-reference (or pass-by-object-reference) for objects. Rust's ownership system makes this explicit: borrow (&T, &mut T) vs move.

### Return Values

Every function returns something. Functions that return "nothing" return a unit type (void in C/Java, () in Rust, None in Python). Multiple return values are supported via tuples (Python, Go), destructuring, or out parameters.

**Early return.** Returning from the middle of a function when a condition is met. Reduces nesting and makes guard clauses possible. Dijkstra disliked it; modern style embraces it for readability.

### Closures

A closure is a function that captures variables from its enclosing scope. Closures are the mechanism behind callbacks, event handlers, higher-order function patterns, and module privacy.

**Mental model.** A closure is a function plus an environment. The environment maps free variables (those not defined as parameters or locals) to their values or references at the time the closure is created.

### Higher-Order Functions

Functions that take functions as arguments or return functions. The three canonical higher-order functions:

**map** -- apply a function to every element of a collection, producing a new collection. `[1,2,3].map(x => x * 2)` produces `[2,4,6]`.

**filter** -- retain only elements that satisfy a predicate. `[1,2,3,4].filter(x => x % 2 == 0)` produces `[2,4]`.

**reduce (fold)** -- accumulate a collection into a single value. `[1,2,3,4].reduce((acc, x) => acc + x, 0)` produces `10`.

These three operations compose to handle the vast majority of collection transformations without explicit loops.

## Part 4 -- Recursion

Recursion is a function calling itself. Every recursive function has two parts: a base case (termination) and a recursive case (reduction toward the base case).

### The Call Stack

Each recursive call pushes a new frame onto the call stack. The frame holds the function's local variables and the return address. When the base case is reached, frames are popped and results are propagated back up.

**Stack overflow.** If recursion is too deep (no base case, or the problem is too large), the call stack exceeds its limit. Python defaults to 1,000 frames. C/Rust depends on the thread stack size (typically 1-8 MB).

### Tail Recursion

A function is tail-recursive if the recursive call is the last operation -- no computation happens after the call returns. Tail-recursive functions can be optimized to use constant stack space (tail call optimization, TCO). Scheme and Haskell guarantee TCO. JavaScript specifies it but few engines implement it. Python explicitly does not support it.

**Converting to tail recursion.** Introduce an accumulator parameter that carries the result-so-far. The classic example:

```
// Not tail-recursive: multiplication after the recursive call
factorial(n) = if n == 0 then 1 else n * factorial(n - 1)

// Tail-recursive: accumulator carries the product
factorial(n, acc = 1) = if n == 0 then acc else factorial(n - 1, n * acc)
```

### Mutual Recursion

Two or more functions that call each other. Example: `isEven(n) = if n == 0 then true else isOdd(n - 1)` and `isOdd(n) = if n == 0 then false else isEven(n - 1)`. Less common but natural for parsers (expression calls term, term calls factor, factor calls expression).

### Recursion vs Iteration

| Dimension | Recursion | Iteration |
|---|---|---|
| Natural fit | Trees, graphs, divide-and-conquer | Sequential traversal, counting |
| Stack usage | O(depth) unless tail-optimized | O(1) |
| Readability | Clearer for recursive structures | Clearer for linear processes |
| Performance | Call overhead per frame | Minimal overhead |
| Debugging | Stack traces show call chain | Loop state harder to inspect |

## Part 5 -- Type Systems

### Static vs Dynamic

**Static typing.** Types are checked at compile time. Type errors are caught before the program runs. Examples: Java, C, Rust, TypeScript, Haskell.

**Dynamic typing.** Types are checked at runtime. Variables can hold any type at any time. Type errors surface as runtime exceptions. Examples: Python, JavaScript, Ruby, Lua.

**The tradeoff.** Static typing catches more bugs earlier but requires more annotation. Dynamic typing enables faster prototyping but defers errors to runtime. Type inference (Rust, Haskell, TypeScript) gives much of static typing's safety with less annotation burden.

### Strong vs Weak

**Strong typing.** Operations between incompatible types are errors. Python is strongly typed: `"3" + 4` raises TypeError.

**Weak typing.** The language implicitly coerces types. JavaScript is weakly typed: `"3" + 4` produces `"34"` (string concatenation), but `"3" - 4` produces `-1` (numeric subtraction). This inconsistency is a major source of bugs.

### Generics

Parameterize a type or function over the types it operates on. `Array<T>` works for any type T. Without generics, you write separate implementations for each type or resort to unsafe casts.

## Part 6 -- Error Handling

### Exceptions

**throw/catch (try/catch).** Throw an exception at the point of failure, catch it at the point of recovery. The call stack is unwound between throw and catch. Used in Java, Python, JavaScript, C++.

**The problem with exceptions.** They create invisible control flow. A function that throws looks like it returns normally until it doesn't. The caller must know which exceptions are possible -- and this is not always documented. Checked exceptions (Java) attempt to solve this but create verbosity problems.

### Result Types

**Algebraic error handling.** Rust's `Result<T, E>`, Haskell's `Either a b`, Go's `(value, error)` tuple. The error case is part of the return type, making it impossible to forget.

**Rust's ? operator.** Propagates errors without explicit match statements. `let value = risky_function()?;` returns early with the error if the function fails, or unwraps the success value if it succeeds.

### Defensive Programming

**Preconditions.** Check inputs before using them. `assert(index >= 0 && index < length)`. Fail fast with a clear error message rather than corrupting state silently.

**Postconditions.** Verify outputs before returning them. More common in contract-based languages (Eiffel, D).

**The billion-dollar mistake.** Tony Hoare called null references his "billion-dollar mistake." Languages that use null (Java, JavaScript, C) suffer from NullPointerExceptions. Languages with Option/Maybe types (Rust, Haskell, Kotlin) force explicit handling of the absent-value case.

## Strategy Selection: What Construct Do I Need?

| Situation | Construct | Why |
|---|---|---|
| Name a value for reuse | Variable | Clarity, DRY |
| Choose between alternatives | if/else or match | Conditional logic |
| Repeat an operation | Loop (for, while) | Sequential repetition |
| Encapsulate reusable logic | Function | Abstraction, reuse, testing |
| Process a collection | map/filter/reduce | Declarative, composable |
| Handle tree/recursive structures | Recursion | Natural mapping to structure |
| Prevent invalid operations | Type system + error handling | Safety |
| Represent absent values | Option/Maybe (not null) | Explicit handling |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Mutable default arguments (Python) | Shared across calls | Use None sentinel, create inside function |
| == vs === in JavaScript | == coerces types | Always use === |
| Forgetting base case in recursion | Stack overflow | Define base case first, verify termination |
| Off-by-one in loops | Wrong number of iterations | State loop invariant, test boundaries |
| Catching all exceptions | Masks bugs | Catch specific exception types |
| Null without checking | NullPointerException/segfault | Use Option types or null checks |
| Shadowing variables unintentionally | Hard-to-find bugs | Use different names or enable linter warnings |

## Cross-References

- **hopper agent:** Practical implementation across multiple programming languages. Primary agent for language-specific questions.
- **papert agent:** Pedagogical scaffolding for learners encountering these concepts for the first time.
- **dijkstra agent:** Software design principles that govern how fundamentals are composed into larger programs.
- **kay agent:** Object-oriented perspective on encapsulation, message passing, and abstraction.
- **algorithms-data-structures skill:** Builds on fundamentals to study algorithm design and analysis.
- **debugging-testing skill:** Techniques for finding and preventing errors in fundamental constructs.

## References

- Abelson, H. & Sussman, G. J. (1996). *Structure and Interpretation of Computer Programs*. 2nd edition. MIT Press.
- Kernighan, B. W. & Ritchie, D. M. (1988). *The C Programming Language*. 2nd edition. Prentice Hall.
- Klabnik, S. & Nichols, C. (2023). *The Rust Programming Language*. 2nd edition. No Starch Press.
- Hopper, G. M. (1952). "The Education of a Computer." *Proceedings of the ACM National Conference*.
- Van Roy, P. & Haridi, S. (2004). *Concepts, Techniques, and Models of Computer Programming*. MIT Press.
- Pierce, B. C. (2002). *Types and Programming Languages*. MIT Press.
