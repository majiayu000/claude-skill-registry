---
name: api-design
description: Use when designing or reviewing a public API, exported function signature, module boundary, exported type/interface, or any contract other code depends on
---

# API and Interface Design

## Overview

The headline rule, from Scott Meyers (97/55), governs everything else: **make interfaces easy to use correctly and hard to use incorrectly.** Every other decision below is a tactic for that rule — encapsulate behavior so callers can't reach past the contract, lean on the type system so wrong calls fail at compile time.

This is a **rigid** skill. Run the decisions in order. If you can't satisfy one, stop and tell the user what's blocking you.

## When to invoke

Invoke when you're about to:

- Add or change a function/method that will be called from another module, package, service, or repo
- Export a new type, interface, trait, protocol, or class
- Define a request/response schema, RPC method, or message format
- Publish a library, SDK, or plugin contract
- Change an existing public signature (parameter order, optionality, return type, thrown errors)
- Add or remove a configuration flag, CLI option, or env-var contract that other code reads
- Decide what to make `public`, `internal`, `final`, `sealed`, or `private`
- Review an API design, interface, or public contract for usability, correctness, or ergonomics

If you're not sure whether a change is "public," ask: *will any code outside this file depend on the shape of what I'm about to write?* If yes, invoke.

### Non-triggers — do NOT invoke for

- Renaming a private/local function whose only callers live in the same file
- Adding a comment or docstring to an existing public function without changing its signature
- Fixing a bug inside an existing function without changing its signature, parameters, return type, or error contract
- Reformatting, reordering imports, or other no-semantic-change edits
- Renaming a single local variable inside one function
- Adding an internal helper called only from one place that already exists

## API design decisions

Run every decision in order. Decision 1 is the headline; the rest are how you satisfy it.

1. **Headline: make it easy to use correctly, hard to use incorrectly.** *(Meyers, 97/55.)* Before the API exists, write a handful of realistic call sites — on a whiteboard, in a scratch file, in a test. The natural way to call it should be the correct way. Then ask: what mistakes will a tired caller make? Swapped argument order, forgotten cleanup, calling methods in the wrong sequence, passing a stringly-typed value that means nothing? Anticipate those, then change the *interface* (not the docs) so each one is awkward or impossible. Every later decision is a tactic for this rule.

### Make wrong code look wrong

2. **Prevent errors at the call site, not in the error message.** *(Colborne, 97/66.)* An error message is a sign that communication broke down upstream. Where you can, eliminate the error condition: take an enum instead of a string, take a parsed `Url` instead of `String`, take a non-empty list type instead of `List` plus a runtime check. Where free input is unavoidable, parse leniently and report specifically. Defaults should reflect the common case. Most caller mistakes are systematic — the API drew them in — not user incompetence.

### Encapsulate

3. **Encapsulate behavior, not just state.** *(Landre, 97/32.)* A type that exposes only getters and setters has pushed every business rule out into its callers, where the rule will be re-implemented inconsistently. If `Order.addItem` needs a credit check, the credit limit and the check belong on `Customer`, and `Order` asks `Customer`. Anti-pattern: an `OrderManager` / `OrderService` that holds all the logic while `Order`, `Customer`, and `Item` are records. When state and the behavior that depends on it live together, callers can't get the sequence wrong. And encapsulate *one* coherent behavior — a class with fourteen methods of which any caller uses two has the dual problem: every caller depends on a surface they don't all need. The exported surface should have one reason for callers to depend on it. *(Martin, 97/76 — SRP at the boundary.)*
4. **Don't extract a shared API until the contexts are actually shared.** *(Dahan, 97/7.)* Two call sites with the same four lines of code are not necessarily the same concept — they may be the same shape today and diverge tomorrow under different business pressures. A premature shared library ties the two callers together: every change now requires synchronizing both. Localize first; extract only when a real shared concept emerges and you can name it in the domain.

### Use the type system

5. **Prefer domain-specific types to primitives.** *(Landre, 97/65.)* `ship(weight: Kilograms)` and `ship(thrust: Newtons)` cannot be confused at a call site; `ship(weight: double)` and `ship(thrust: double)` can — and the Mars Climate Orbiter is the canonical example of how that ends. In statically typed languages this becomes a compile-time guarantee; in dynamic ones, a small wrapper class plus a unit test gives you the same readability and the same encapsulation point for domain rules.
6. **Model state explicitly; reject illegal operations by type or guard.** *(Nilsson, 97/84.)* If an `Order` can be in `InProgress`, `Paid`, or `Shipped`, then `addItem` is only legal in one state and `ship` is only legal in another. Pretending the state doesn't exist (one flat class with a pile of booleans) leads to nonsense like "shipped before paid" being representable. Either split into state types, or check the current state at the start of every operation that depends on it. Method signatures should reflect what's actually callable.

### API ergonomics

7. **Design vocabulary, not conveniences.** *(Hohpe, 97/19.)* `parser.processNodes(text, false)` is meaningless at the call site — the reader must consult docs to learn what `false` means. A boolean or enum flag whose value flips the meaning of the operation is two operations wearing one name. Split it: give callers two well-named methods, or a small composable vocabulary they can combine in ways you didn't anticipate. The "convenience" of one method with a switch is convenience for the implementer, not the caller.
8. **Test the code that uses your API.** *(Feathers, 97/35.)* It is not enough to write tests *of* your API; write tests of *code that calls* your API. The hurdles a caller hits when they try to mock, fake, or stub your types are the same hurdles every consumer will hit. Locking everything down with `final` / `sealed` / singleton / static may protect your future implementation choices, but it makes callers' code untestable — and your library will be replaced. Treat testability as a design constraint.

### Polymorphism over conditionals

9. **Reach for polymorphism before chains of `if`/`switch` on type tags.** *(Pepperdine, 97/59.)* When the caller has to choose behavior by inspecting an enum or type code (`if (item.kind == DOWNLOADABLE) shipByEmail(...) else shipBySurface(...)`), the API has handed responsibility for a closed set of cases back to every caller. A polymorphic interface (`item.ship(shipper)`) puts the choice inside the type that already knows the answer. Count `if`/`switch` statements that branch on type — that's roughly your count of missed polymorphism opportunities. Sometimes a conditional is genuinely simpler; default to polymorphism and justify the conditional.

## Red Flags

These thoughts mean STOP — restart the decisions:

| Thought | Reality |
|---|---|
| "I'll document the right way to call it." | If the docs have to warn callers, the interface is wrong. Change the signature so the wrong call won't compile or won't typecheck. (97/55) |
| "I'll add a `bool strict` parameter — easier than two methods." | A flag that flips the meaning of an operation is two operations wearing one name. Split it; give the caller real vocabulary. (97/19) |
| "I'll expose the field with a getter and setter — callers know what to do." | You've pushed the business rule into every caller. Encapsulate the behavior on the type that owns the state. (97/32) |
| "These two call sites do the same four lines — extract a shared helper." | Same shape today, different pressures tomorrow. Localize until a real shared concept emerges and earns a name. (97/7) |
| "It takes a `string` — callers can pass whatever." | Strings and floats are an invitation to pass the wrong thing. A named type closes the door on the Mars-Orbiter class of bugs. (97/65) |
| "The state is implicit — callers will know the order to call methods." | Implicit state means callers can call `ship` before `pay`. Make the state a type or guard every operation that depends on it. (97/84) |
| "I'll mark everything `final` / `sealed` to keep my options open." | Locked-down APIs are untestable for the code that uses them. Write a test of a *caller* before you decide what to seal. (97/35) |
| "Callers can `if` on the type tag — it's only three cases." | Three cases become thirty, scattered across every caller. Move the choice inside the type with polymorphism. (97/59) |
| "If they pass bad input, they'll see a clear error message." | Errors are a sign of broken communication, not a feature. Eliminate the error condition or accept the common formats. (97/66) |
| "It's an internal API — the rules don't apply." | Internal today is exposed tomorrow, and the wrong-use bugs accumulate either way. The rules apply. (97/55) |
| "This class is the right home for it — it's already imported here." | Wedging a second concern onto a class that's already imported gives every caller a surface they don't all need. The exported surface should have one reason for callers to depend on it; split it. (97/76) |
| "I'll add another thin method that just forwards to an internal." | Shallow modules pay no abstraction tax. Make the module deep — fewer, more-powerful methods that hide implementation, not more thin pass-throughs. (`Ousterhout/DeepModules`) |
| "I'll throw `NotFound` if the file doesn't exist on `delete`." | Define the error out of existence: idempotent delete, clamping substring, `Option<T>` lookup. Fewer error paths the caller has to remember. (`Ousterhout/DefineErrorsOutOfExistence`) |
| "I'll subclass and override the method to throw — callers shouldn't use it." | Subtype must be substitutable. If the override breaks caller assumptions, the hierarchy is wrong. Prefer composition. (`Liskov/LSP`) |
| "I'll validate the input and pass the raw `string` downstream." | Parse, don't validate. Return a parsed domain type from the boundary; downstream code receives the proven shape, not the raw primitive. (`King/ParseDontValidate`) |
| "Callers will only use the documented behavior — internals can change freely." | Hyrum's Law: any observable behavior will be depended on by someone. Reason about the new API as if its current observable behavior were private. (`Hyrum/Law`) |

## What "done" looks like

You are done when **all** of the following are true:

- [ ] You wrote at least three realistic call sites (test, scratch, or whiteboard) before finalizing the signature.
- [ ] The natural way to call the API is the correct way; common mistakes are awkward or impossible at the type level.
- [ ] Each public type encapsulates the behavior that depends on its state, not just the state.
- [ ] No public parameter is a primitive where a domain type would close a class of bugs.
- [ ] States that constrain which operations are legal are represented explicitly, not as implicit folklore.
- [ ] No public method takes a flag whose value flips the meaning of the operation.
- [ ] You wrote (or sketched) a test of a *caller* of this API and confirmed the caller's code is testable.
- [ ] Branching on type tags has been replaced by polymorphism, or you can name the reason a conditional is genuinely simpler here.
- [ ] You did not extract a shared abstraction whose two call sites are not yet provably the same concept.

If any box is unchecked, you are not done. Either finish, or revert and re-plan.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/7 | Beware the Share | Udi Dahan |
| 97/19 | Convenience Is not an -ility | Gregor Hohpe |
| 97/32 | Encapsulate Behavior, Not Just State | Einar Landre |
| 97/35 | The Golden Rule of API Design | Michael Feathers |
| 97/55 | Make Interfaces Easy to Use Correctly and Hard to Use Incorrectly | Scott Meyers |
| 97/59 | Missing Opportunities for Polymorphism | Kirk Pepperdine |
| 97/65 | Prefer Domain-Specific Types to Primitive Types | Einar Landre |
| 97/66 | Prevent Errors | Giles Colborne |
| 97/76 | The Single Responsibility Principle (at the boundary) | Robert C. Martin |
| 97/84 | Thinking in States | Niclas Nilsson |
| `Ousterhout/DeepModules` | Deep Modules | John Ousterhout |
| `Ousterhout/DefineErrorsOutOfExistence` | Define Errors Out of Existence | John Ousterhout |
| `Liskov/LSP` | Liskov Substitution Principle | Barbara Liskov |
| `King/ParseDontValidate` | Parse, Don't Validate | Alexis King |

See `principles.md` for the long-form distillations, citations, and source links.
