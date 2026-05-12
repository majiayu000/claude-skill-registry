---
name: domain-modeling
description: Use when introducing, reviewing, or renaming a top-level type, table, or domain concept; or choosing where state lives (in-memory vs persistent)
---

# Domain Modeling

## Overview

The names and shapes you give the concepts in your code *are* the design. **When you introduce a new domain concept, name it for what it means in the user's world, give it a real type, and decide where its state lives — before you write the methods that act on it.**

This is a **rigid** skill. Run the decisions in order. If you can't satisfy one, stop and tell the user what's blocking you. When the concept is exposed across a module/package/service boundary, also invoke `api-design` (overlap on type design and value-vs-identity).

## When to invoke

Invoke when you're about to:

- Introduce a new top-level type, class, struct, record, or table that represents a *thing in the domain* (Trader, Portfolio, Booking, Invoice, Reservation)
- Rename an existing domain concept across files
- Add a new database table or persistent collection
- Decide whether a chunk of state should live in memory, in a file, in a key-value store, or in a relational database
- Replace primitive-typed data (`int`, `string`, `Map<int, Map<int, int>>`) with named domain types
- Sketch the data model for a new feature, area, or service
- Evaluate whether an existing domain model is well-structured, or review naming and type choices

If you're not sure whether a change introduces a *new domain concept* (vs. a local helper), **invoke anyway** — the decisions are cheap, mismodeled domain concepts are not.

### Non-triggers — do NOT invoke for

- Renaming a single local variable inside one function (`x` → `count`)
- Renaming a private helper function or internal-only struct that doesn't represent a domain concept
- Adding a new field to an existing type when the field is not itself a new domain concept (a new `lastModified` timestamp on `Booking` — no; a new `CancellationPolicy` type referenced from `Booking` — yes)
- Adjusting an existing type's representation without changing its meaning (switching `int` user IDs to `long`)
- Adding a method to an existing domain type (use `clean-code` instead)
- Defining a DTO that mirrors an existing domain type one-to-one for transport (use `api-design`)

### Language guard

The typed-domain principles below (`Wlaschin/InvalidStatesUnrepresentable`, `Wlaschin/SmartConstructors`, `Wlaschin/TypesForEffects`, `Fowler/PrimitiveObsession`) fire hardest in languages with sum types and pattern matching (TypeScript, Rust, F#, Haskell, Scala, Kotlin, modern C#). They degrade gracefully in dynamic languages (Python, JavaScript, Ruby) where the agent reaches for frozen dataclasses, `pydantic`, `attrs`, `TypedDict`, or NewType where they help. **Do not be type-system-evangelical** — in a small Python script, a `dict` is the right answer.

## The domain-modeling decisions

Run every decision in order. Do not write the type's methods until decision 5 is settled.

1. **Name the concept the way the domain expert names it.** If the user says "trader", "portfolio", "booking", "policy" — that's the type name. Avoid invented programmer terms (`UserDataObject`, `BookingManager`, `PolicyHelper`) when a domain term exists. If the domain expert wouldn't recognize the name, you're inventing a secret vocabulary the next programmer will have to decode. *(North, 97/11.)*
2. **Make implicit relationships explicit as types or methods.** If the rule is "some traders cannot view some portfolios," prefer `trader.canView(portfolio)` over `portfolioIdsByTraderId.get(...)containsKey(...)`. Replace primitive obsession (raw ints, strings, nested maps standing in for relationships) with named types and operations. *(North, 97/11.)*
3. **Treat this as design, not typing.** The shape you pick now will outlive most of the code that uses it. Sketch two or three alternatives before committing. Validate the chosen shape against at least two realistic scenarios — if it forces awkward workarounds in either, it's the wrong shape. Code is design; design needs validation. *(Brush, 97/12.)*
4. **Default to immutable value types and pure transformations.** Unless the concept *intrinsically* has identity and lifetime (a `User`, a `Booking`), prefer value types you construct fresh rather than mutate. Operations that produce new domain objects from old ones are easier to test, reason about, and reuse than methods that secretly mutate shared state. *(Garson, 97/2.)*
5. **Decide where the state lives — before sketching methods.** Ask: Is this data **large** (won't fit in RAM), **persistent** (survives process restart), or **interconnected** (entities reference each other with consistency rules)? If yes to any two: it belongs in a database (embedded like SQLite is fine for small needs). If no to all three: an in-memory structure is fine. Hand-rolled `Map<int, Map<int, int>>` for what is really a relational dataset is a cost you pay forever. *(Spinellis, 97/48.)*
6. **Consider whether this concept needs its own little language.** When users keep describing the concept with a constrained vocabulary — rules, validations, query expressions, configuration — and several places in the code re-encode that vocabulary by hand, you are recreating a DSL the slow way. An internal DSL (a fluent API in the host language) lets domain experts read and sometimes write the rules directly. Don't *start* here, but recognize the smell. *(Hunger, 97/23.)*
7. **Place the concept in one canonical location.** One file, one module, one table — not three competing definitions. If you find a parallel concept already exists under a different name, stop and unify before adding a third. The next programmer should be able to find this concept by searching for the domain term and finding exactly one definition.

## Red Flags

These thoughts mean STOP — restart the decisions:

| Thought | Reality |
|---|---|
| "I'll use a `Map<int, Map<int, ...>>` — it's just an internal lookup." | Nested generic collections standing in for domain relationships are a tacit secret only you understand. Make the relationship a type or a method. (97/11) |
| "I'll call it `UserManager` / `DataHelper` / `ServiceUtil` — close enough." | If the domain expert wouldn't recognize the name, you've invented a vocabulary the next programmer has to decode. Use the domain term. (97/11) |
| "I'll write the methods first and figure out the shape as I go." | The shape *is* the design decision. Methods follow. Sketch the shape, validate it against scenarios, then add methods. (97/12) |
| "It's just a data class — five mutable fields with getters and setters." | Default to immutable value types; reach for mutability only when the concept inherently has identity over time. Mutability is a leading source of defects. (97/2) |
| "I'll keep this dataset in a `HashMap` for now — we can move it to a DB later." | "Later" rarely arrives. If the data is large, persistent, or interconnected, it belongs in a database from the start. SQLite is fine. (97/48) |
| "Let me hand-roll consistency between these in-memory collections." | Foreign keys, cascading deletes, and unique constraints are what an RDBMS does for free. Hand-rolling them produces dangling-reference bugs. (97/48) |
| "I'll add another `BookingDataObject` next to the existing `Booking` — they're slightly different." | Two competing definitions of the same domain concept guarantee they will drift. Unify first, then add. (97/11) |
| "This rule is just a one-line `if` — no need for a domain method." | If the same `if` recurs across the codebase representing the same business rule, it's a method on a domain type. Encapsulate it. (97/11) |
| "It's an internal type, naming doesn't matter." | Internal today is exposed tomorrow, and the name you pick now will appear in stack traces, logs, and PR diffs for years. Name it for the domain. (97/11, 97/12) |
| "I'll use a `string` for the email — we validate it on input." | Smart constructor instead. The type itself carries the proof; downstream code receives `EmailAddress`, not `string`, and never re-validates. (`Wlaschin/SmartConstructors`) |
| "I'll add a `bannedReason` nullable field that's only set when `status == banned`." | Boolean flags and "valid only in some states" nullables permit invalid combinations the language won't catch. Use a discriminated union; let the compiler refuse the impossible state. (`Wlaschin/InvalidStatesUnrepresentable`) |
| "Both `userId` and `accountId` are `string` — argument order is enough." | Mars Climate Orbiter. Brand the types (`UserId`, `AccountId`) so swapped arguments fail at compile time. (`Wlaschin/TypesForEffects`, `Fowler/PrimitiveObsession`) |

## What "done" looks like

You are done when **all** of the following are true:

- [ ] The new concept is named with a term a domain expert would recognize.
- [ ] Relationships between domain concepts are expressed as types or methods, not as nested primitive collections.
- [ ] You sketched at least one alternative shape and rejected it for a stated reason.
- [ ] Mutability is a deliberate choice (this concept has identity) rather than a default (it's just easier).
- [ ] You decided where the state lives based on size/persistence/interconnectedness — not by reflex.
- [ ] There is exactly one canonical definition of this concept in the codebase.

If any box is unchecked, you are not done. Either finish, or revert and re-plan.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/2 | Apply Functional Programming Principles | Edward Garson |
| 97/11 | Code in the Language of the Domain | Dan North |
| 97/12 | Code Is Design | Ryan Brush |
| 97/23 | Domain-Specific Languages | Michael Hunger |
| 97/48 | Large, Interconnected Data Belongs to a Database | Diomidis Spinellis |
| `Wlaschin/InvalidStatesUnrepresentable` | Make Invalid States Unrepresentable | Scott Wlaschin |
| `Wlaschin/SmartConstructors` | Smart Constructors | Scott Wlaschin |
| `Wlaschin/TypesForEffects` | Types for Effects | Scott Wlaschin |
| `Fowler/PrimitiveObsession` | Primitive Obsession → Replace Primitive with Object | Martin Fowler |

See `principles.md` for the long-form distillations, citations, and source links.
