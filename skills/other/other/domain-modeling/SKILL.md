---
name: domain-modeling
description: >-
  Domain modeling principles: parse-don't-validate, make invalid states
  unrepresentable, primitive obsession detection, semantic types, and domain
  veto authority. Activate when designing types, reviewing code for domain
  integrity, or when domain review is needed in a TDD cycle.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [domain-types, source-files]
  phase: decide
  standalone: true
---

# Domain Modeling

**Value:** Communication -- domain types make code speak the language of the
business. They turn implicit knowledge into explicit, compiler-verified
contracts that humans and AI can reason about.

## Purpose

Teaches how to build rich domain models that prevent bugs at compile time
rather than catching them at runtime. Covers primitive obsession detection,
parse-don't-validate, making invalid states unrepresentable, and semantic
type design. Independently useful for any code review or design task, and
provides the principles that domain review checks for in the TDD cycle.

## Practices

### Avoid Primitive Obsession

Do not use raw primitives (`String`, `int`, `number`) for domain concepts.
Create types that express business meaning.

**Do:**
```
fn transfer(from: AccountId, to: AccountId, amount: Money) -> Result<Receipt, TransferError>
```

**Do not:**
```
fn transfer(from: String, to: String, amount: i64) -> Result<(), String>
```

When reviewing code, flag every parameter, field, or return type where a
primitive represents a domain concept. The fix is a newtype or value object
that validates on construction.

### Parse, Don't Validate

Validate at the boundary. Use strong types internally. Never re-validate
data that a type already guarantees.

1. Accept raw input at system boundaries (user input, API responses).
2. Parse it into a domain type that enforces validity at construction.
3. Pass the domain type through the system. No further validation needed.

```python
# Boundary: parse raw input into domain type
email = Email(raw_input)  # raises if invalid

# Interior: trust the type
def send_welcome(email: Email) -> None:
    # No need to validate -- Email guarantees validity
```

If you find validation logic deep inside business logic, it belongs at the
construction boundary instead.

### Make Invalid States Unrepresentable

Use the type system to make illegal combinations impossible to construct.

**Problem -- boolean flags create invalid combinations:**
```
struct User { email: Option<String>, email_verified: bool }
# Can have email_verified=true with email=None
```

**Solution -- encode state in the type:**
```
enum User {
    Unverified { email: Email },
    Verified { email: Email, verified_at: Timestamp },
}
```

When reviewing code, ask: "Can this type represent a state that is
meaningless in the domain?" If yes, redesign it.

### Semantic Types Over Structural Types

Name types for what they ARE in the domain, not what they are made of.

| Wrong (structural) | Right (semantic) |
|--------------------|------------------|
| `NonEmptyString` | `UserName` |
| `PositiveInteger` | `OrderQuantity` |
| `ValidatedEmail` | `CustomerEmail` |

The test: if two fields have the same structural type, the compiler cannot
catch you swapping them. Semantic types prevent this.

```typescript
// BAD: title and name are both NonEmptyString -- swappable
{ title: NonEmptyString, name: NonEmptyString }

// GOOD: distinct types catch mix-ups at compile time
{ title: UserTitle, name: UserName }
```

Structural types are useful as building blocks that semantic types wrap.
The semantic type adds domain identity; the structural type provides
reusable validation.

### Newtypes for Identifiers

Every identifier gets its own type. Never use raw `String` or `int` for IDs.

```rust
struct AccountId(Uuid);
struct UserId(Uuid);

// Compiler catches: transfer(user_id, account_id) won't compile
fn transfer(from: AccountId, to: AccountId, user: UserId) -> Result<(), Error>
```

### Ergonomic Conversions

Make construction validated and extraction easy.

- **Construction (IN):** Always through a validating constructor. No automatic
  conversion from primitives.
- **Extraction (OUT):** Provide `Display`, `AsRef`, `Into` or equivalent so
  the type is convenient to use. Getting the inner value out should be trivial.

Never provide an automatic conversion FROM a primitive -- that bypasses
validation and undermines parse-don't-validate.

### Exhaustive Matching

Use enums with exhaustive match/switch to ensure all cases are handled.
Never use a catch-all default for domain states -- it silently swallows
new variants.

### Veto Authority

When reviewing code (whether in a TDD cycle or a standalone review), you
have authority to reject designs that violate these principles. When
exercising this authority:

1. State the specific violation (e.g., "primitive obsession: `email` is
   `String`, should be `Email` type").
2. Propose the alternative with a concrete type definition.
3. Explain the impact in one sentence.
4. If the other party disagrees, engage substantively for up to two rounds.
   Then escalate to the human.

Do not back down from valid domain concerns to avoid conflict. Do not
silently accept designs that violate these principles.

## Enforcement Note

This skill provides advisory guidance on domain modeling quality. It cannot
mechanically prevent an agent from using primitives or creating invalid state
representations. On harnesses with plugin support, enforcement plugins can
add file-type restrictions (domain agent edits only type definitions) and
mandatory review gates. On other harnesses, these principles are followed
by convention and verified through code review. For available enforcement
plugins, see the [Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After applying domain modeling principles, verify:

- [ ] No primitive types (`String`, `int`, `number`) used for domain concepts
- [ ] All identifiers use newtype wrappers, not raw primitives
- [ ] Invalid states are unrepresentable (no contradictory field combinations)
- [ ] Validation occurs at construction boundaries, not deep in business logic
- [ ] Types are named for domain meaning (semantic), not structure
- [ ] Two fields with the same underlying type cannot be accidentally swapped
- [ ] Enum matching is exhaustive with no catch-all defaults for domain states

If any criterion is not met, create or refine the domain type before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **tdd-cycle:** Domain review is a mandatory checkpoint in the TDD cycle.
  This skill provides the principles that review checks for.
- **code-review:** Domain integrity is stage 3 of the three-stage review.
  This skill defines what to look for.
- **architecture-decisions:** Architectural patterns (event sourcing, CQRS,
  hexagonal) affect where domain boundaries fall.

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill tdd-cycle
```
