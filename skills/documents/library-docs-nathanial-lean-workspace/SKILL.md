---
name: library-docs
description: Write prosaic, narrative-style documentation for Lean 4 libraries. Use when creating README files, user guides, tutorials, or comprehensive library documentation.
---

# Lean 4 Library Documentation

Write clear, engaging documentation that teaches users how to understand and use Lean 4 libraries effectively.

## Philosophy

Great library documentation is **prosaic**: it reads like well-written prose, not a reference manual. It tells a story—starting with the problem the library solves, building intuition through examples, and gradually revealing depth.

**Principles:**

1. **Lead with the "why"** — Before showing API, explain what problem this solves
2. **Show, then tell** — Code examples first, explanations second
3. **Progressive disclosure** — Simple cases first, advanced features later
4. **Concrete over abstract** — Real examples over type signatures
5. **Assume intelligence, not knowledge** — Readers are smart but may not know Lean idioms

## Document Structure

### README.md (Entry Point)

```markdown
# Library Name

One sentence: what this library does and why you'd use it.

## The Problem

2-3 sentences describing the pain point this library addresses.
Use concrete scenarios the reader will recognize.

## Quick Example

```lean
-- Show the library solving the problem in 5-10 lines
-- This should be copy-pasteable and immediately useful
```

## Installation

```lean
require libname from git "https://github.com/..." @ "v0.0.1"
```

## Core Concepts

Brief overview of the mental model. What are the 2-3 key ideas
a user needs to understand?

## Getting Started

Walk through a realistic use case step-by-step.

## Documentation

Link to detailed guides, API reference, examples.

## License

MIT (or appropriate license)
```

### Guide Documents

For libraries with depth, create focused guides:

| Document | Purpose | Length |
|----------|---------|--------|
| `GUIDE.md` | Complete tutorial | 500-1500 lines |
| `CONCEPTS.md` | Mental model and theory | 200-500 lines |
| `COOKBOOK.md` | Problem → solution recipes | Variable |
| `MIGRATION.md` | Upgrading from older versions | As needed |
| `ARCHITECTURE.md` | How the library works internally | For contributors |

## Writing Patterns

### The Hook Opening

Start with recognition, not definition:

```markdown
❌ "Collimator is a profunctor optics library implementing van Laarhoven lenses."

✓ "Ever written code like this?

```lean
let user := { user with
  address := { user.address with
    city := "Boston"
  }
}
```

Collimator lets you write this instead:

```lean
let user := user |> address..city .~ "Boston"
```
"
```

### The Annotated Example

Show code, then explain it line by line:

```markdown
```lean
def fetchUser (id : UserId) : IO (Option User) := do
  let response ← client.get s!"/users/{id}"  -- ①
  let .ok body := response.status | return none  -- ②
  body.parse User  -- ③
```

Let's break this down:

1. **Line 1:** We make an HTTP GET request, interpolating the user ID into the path
2. **Line 2:** Pattern match on the response status—if it's not `.ok`, return `none` early
3. **Line 3:** Parse the response body into a `User` structure
```

### The Progression Pattern

Build complexity gradually:

```markdown
## Basic Usage

Start with the simplest case that does something useful:

```lean
let color := Color.red
```

## Adding Customization

Now let's see how to create custom colors:

```lean
let color := Color.rgb 255 128 0
```

## Advanced: Color Spaces

For precise color work, you can specify the color space:

```lean
let color := Color.hsl 0.0 1.0 0.5  -- Same red in HSL
```
```

### The "What You'll Build" Preview

For tutorials, show the end result upfront:

```markdown
## What We're Building

By the end of this guide, you'll have a working CLI that:
- Parses command-line arguments
- Reads configuration from a TOML file
- Makes HTTP requests to an API
- Displays results in a formatted table

Here's a preview of the final code:

```lean
def main (args : List String) : IO Unit := do
  let config ← Config.load "config.toml"
  let results ← Api.fetch config.endpoint
  Terminal.printTable results
```

Let's build this step by step.
```

### The Comparison Table

For choosing between options:

```markdown
## Choosing a Parser

| If you need... | Use... | Example |
|----------------|--------|---------|
| Simple key-value parsing | `basic` | Config files |
| Full grammar support | `grammar` | Programming languages |
| Streaming/incremental | `streaming` | Large files |
| Error recovery | `resilient` | IDE integration |
```

### The Common Mistakes Section

Anticipate confusion:

```markdown
## Common Mistakes

### Forgetting to import the instance

```lean
-- ❌ This won't compile
def x : Json := toJson myValue

-- ✓ Import the ToJson instance
import MyLib.Json
def x : Json := toJson myValue
```

### Using `pure` instead of `return` in do-notation

Both work, but `return` short-circuits while `pure` continues:

```lean
-- These behave differently!
def f : IO Unit := do
  if condition then return  -- Exits immediately
  doMoreStuff

def g : IO Unit := do
  if condition then pure ()  -- Continues to doMoreStuff
  doMoreStuff
```
```

## Writing Style

### Voice and Tone

- **Active voice:** "The parser reads the file" not "The file is read by the parser"
- **Second person:** "You can configure..." not "One can configure..."
- **Present tense:** "This returns..." not "This will return..."
- **Direct:** "Use `map`" not "You might want to consider using `map`"

### Technical Precision

Be precise without being pedantic:

```markdown
❌ "This function takes a parameter and returns a value."
✓ "Given a user ID, returns the user's profile or `none` if not found."

❌ "The monad instance allows for sequential composition."
✓ "You can chain operations with `do` notation."
```

### Code Comments

In documentation examples, comments explain the non-obvious:

```lean
-- ❌ Redundant comment
let x := 5  -- Set x to 5

-- ✓ Explains why, not what
let x := 5  -- Default timeout in seconds

-- ✓ Clarifies Lean-specific syntax
let (a, b) := pair  -- Destructure the tuple
```

## Lean-Specific Documentation

### Documenting Type Classes

```markdown
## The `Parseable` Type Class

To make your type parseable from strings, implement `Parseable`:

```lean
class Parseable (α : Type) where
  parse : String → Option α
```

**Required method:**
- `parse`: Convert a string to your type, returning `none` on failure

**Example implementation:**

```lean
instance : Parseable MyConfig where
  parse s :=
    match s.splitOn "=" with
    | [key, value] => some { key, value }
    | _ => none
```

**Automatic derivation:**

For simple structures, use `deriving Parseable` (requires `import Lib.Derive`).
```

### Documenting Monads and Effects

```markdown
## The `Fetch` Monad

`Fetch` is a monad for making HTTP requests with automatic caching and retry.

```lean
def Fetch (α : Type) : Type := ReaderT FetchConfig (ExceptT FetchError IO) α
```

**Running a Fetch action:**

```lean
def main : IO Unit := do
  let config := FetchConfig.default
  match ← Fetch.run config myFetchAction with
  | .ok result => IO.println s!"Got: {result}"
  | .error e => IO.eprintln s!"Failed: {e}"
```

**Available operations:**

| Operation | Type | Description |
|-----------|------|-------------|
| `Fetch.get` | `String → Fetch Response` | GET request |
| `Fetch.post` | `String → Json → Fetch Response` | POST with JSON body |
| `Fetch.withTimeout` | `Nat → Fetch α → Fetch α` | Set timeout (ms) |
```

### Documenting Macros and DSLs

```markdown
## Query DSL

The `query` macro provides SQL-like syntax for building type-safe queries:

```lean
query {
  from users
  where age > 21
  select name, email
  orderBy name
  limit 10
}
```

**Clauses:**

| Clause | Required | Description |
|--------|----------|-------------|
| `from table` | Yes | Source table |
| `where condition` | No | Filter rows |
| `select fields` | No | Choose columns (default: all) |
| `orderBy field` | No | Sort results |
| `limit n` | No | Maximum rows |

**The generated type:**

The query macro produces a `Query α` where `α` is a structure containing
the selected fields. The compiler infers this from your `select` clause.
```

### Documenting Notation

```markdown
## Custom Notation

This library defines several operators for working with lenses:

| Notation | Meaning | Example |
|----------|---------|---------|
| `a..b` | Compose lenses | `user..address..city` |
| `x ^. l` | View through lens | `user ^. name` |
| `l .~ v` | Set through lens | `name .~ "Alice"` |
| `l %~ f` | Modify through lens | `age %~ (· + 1)` |

**Precedence:** `..` binds tighter than `.~` and `%~`, so:

```lean
user |> address..city .~ "Boston"
-- Parses as: user |> ((address..city) .~ "Boston")
```
```

## API Reference Style

When documenting individual functions:

```markdown
### `Array.groupBy`

Groups elements by a key function, returning a map from keys to arrays of elements.

```lean
def groupBy [BEq κ] [Hashable κ] (f : α → κ) (xs : Array α) : HashMap κ (Array α)
```

**Parameters:**
- `f`: Function to extract the grouping key from each element
- `xs`: Array of elements to group

**Returns:** A `HashMap` where each key maps to all elements that produced that key

**Example:**

```lean
let words := #["apple", "banana", "apricot", "blueberry"]
let byFirstLetter := words.groupBy (·.front)
-- { 'a' => #["apple", "apricot"], 'b' => #["banana", "blueberry"] }
```

**Performance:** O(n) where n is the array length

**See also:** `Array.partition`, `Array.filter`
```

## Complete README Template

```markdown
# LibraryName

Brief, compelling description of what this library does.

## Why LibraryName?

Describe the problem space. What's hard without this library?
What does it make easy?

## Quick Start

```lean
import LibraryName

-- Minimal working example (10 lines or less)
```

## Installation

Add to your `lakefile.lean`:

```lean
require libraryname from git "https://github.com/author/libraryname" @ "v1.0.0"
```

## Features

- **Feature One:** Brief description
- **Feature Two:** Brief description
- **Feature Three:** Brief description

## Examples

### Common Use Case

```lean
-- Example with comments
```

### Another Use Case

```lean
-- Example with comments
```

## API Overview

| Module | Purpose |
|--------|---------|
| `LibraryName.Core` | Essential types and functions |
| `LibraryName.Utils` | Helper utilities |
| `LibraryName.Derive` | Deriving instances |

## Documentation

- [User Guide](./GUIDE.md) — Complete tutorial
- [API Reference](./docs/API.md) — Full API documentation
- [Examples](./examples/) — Runnable example projects

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT License — see [LICENSE](./LICENSE)
```

## Checklist

Before finalizing documentation:

- [ ] Can a new user understand what the library does in 30 seconds?
- [ ] Is there a copy-pasteable example in the first screenful?
- [ ] Are installation instructions complete and tested?
- [ ] Do examples actually compile and run?
- [ ] Are common mistakes addressed?
- [ ] Is the writing free of jargon (or is jargon explained)?
- [ ] Does progressive disclosure work (simple → complex)?
- [ ] Are type signatures accompanied by plain-English explanations?
- [ ] Is the tone consistent throughout?
- [ ] Are all code blocks syntax-highlighted correctly?
