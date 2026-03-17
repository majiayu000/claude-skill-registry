---
name: lang-roc-dev
description: Foundational Roc patterns covering platform/application architecture, records, tags, pattern matching, abilities, and functional idioms. Use when writing Roc code, understanding the platform model, or needing guidance on which specialized Roc skill to use. This is the entry point for Roc development.
---

# Roc Fundamentals

Foundational Roc patterns and core language features. This skill serves as both a reference for common patterns and an index to specialized Roc skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Roc Skill Hierarchy                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌───────────────────┐                        │
│                    │   lang-roc-dev    │ ◄── You are here       │
│                    │   (foundation)    │                        │
│                    └─────────┬─────────┘                        │
│                              │                                  │
│              ┌───────────────┴───────────────┐                  │
│              │                               │                  │
│              ▼                               ▼                  │
│     ┌─────────────────┐            ┌─────────────────┐          │
│     │    patterns     │            │     platform    │          │
│     │      -dev       │            │       -dev      │          │
│     └─────────────────┘            └─────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Platform vs application architecture
- Records and their operations
- Tags and tag unions
- Pattern matching with when expressions
- Abilities (Roc's trait system)
- Result type and error handling
- Functional patterns and idioms
- Type inference fundamentals

**This skill does NOT cover (see specialized skills):**
- Platform development → `lang-roc-platform-dev`
- Best practices and advanced patterns → `lang-roc-patterns-dev`
- Testing strategies → `lang-roc-patterns-dev`

---

## Quick Reference

| Task | Syntax |
|------|--------|
| Define record | `{ name: "Alice", age: 30 }` |
| Record type | `{ name : Str, age : U32 }` |
| Update record | `{ user & age: 31 }` |
| Define tag | `Red` or `Custom(40, 60, 80)` |
| Tag union type | `[Red, Yellow, Green]` |
| Pattern match | `when x is ... -> ...` |
| Function type | `add : I64, I64 -> I64` |
| Error handling | `Result a err` |
| Ability constraint | `a -> Str where a implements Inspect` |
| Inline test | `expect 1 + 1 == 2` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Build custom platforms | `lang-roc-platform-dev` |
| Advanced testing strategies | `lang-roc-patterns-dev` |
| Performance optimization | `lang-roc-patterns-dev` |
| Library design patterns | `lang-roc-patterns-dev` |

---

## Platform vs Application Model

### Architecture Overview

Roc uses a unique separation between platforms and applications:

```
┌─────────────────────────────────────────────────┐
│                  Application                    │
│         (Pure functional Roc code)              │
│                                                 │
│  • Business logic                               │
│  • Data transformations                         │
│  • No direct I/O                                │
└────────────┬────────────────────────────────────┘
             │ Pure interface
             ▼
┌─────────────────────────────────────────────────┐
│                  Platform                       │
│         (Roc API + Host implementation)         │
│                                                 │
│  Roc API:    Pure functions applications use    │
│  Host:       Actual I/O implementation          │
│              (written in Rust, C, Zig, etc.)    │
└─────────────────────────────────────────────────┘
```

### Application Structure

```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.Stdout
import pf.Task exposing [Task]

main : Task {} []
main =
    Stdout.line! "Hello, World!"
```

**Key concepts:**
- `app` header declares entry point and platform
- Platform provides I/O capabilities (Stdout, File, Http, etc.)
- Application code remains pure
- Platform handles all effects

### Platform Responsibilities

Platforms provide:
- **I/O primitives**: File system, network, console
- **Memory management**: Allocation and deallocation
- **Program lifecycle**: Startup, shutdown, event loops
- **Host integration**: FFI to system libraries

### Common Platforms

| Platform | Purpose | Use Case |
|----------|---------|----------|
| `basic-cli` | CLI applications | Scripts, command-line tools |
| `basic-webserver` | Web servers | HTTP services, APIs |
| `static-site-gen` | Static sites | Documentation, blogs |

---

## Records

### Record Basics

```roc
# Record literal
user = { name: "Alice", age: 30, active: Bool.true }

# Record type annotation
user : { name : Str, age : U32, active : Bool }

# Accessing fields
userName = user.name
userAge = user.age

# Field access with destructuring
{ name, age } = user
```

### Record Updates

```roc
# Update single field
olderUser = { user & age: 31 }

# Update multiple fields
updatedUser = { user &
    age: 31,
    active: Bool.false
}

# Nested updates
person = {
    name: "Alice",
    address: { city: "NYC", zip: "10001" }
}

movedPerson = { person &
    address: { person.address & city: "SF" }
}
```

### Optional Fields

Roc uses tag unions for optional values, not special record syntax:

```roc
# Type with optional email
User : {
    name : Str,
    age : U32,
    email : [Some Str, None],
}

# Creating users
userWithEmail = {
    name: "Alice",
    age: 30,
    email: Some("alice@example.com")
}

userWithoutEmail = {
    name: "Bob",
    age: 25,
    email: None
}

# Handling optional values
emailText = when user.email is
    Some(addr) -> addr
    None -> "no email"
```

### Record Functions

```roc
# Function taking a record
greet : { name : Str, age : U32 } -> Str
greet = \user ->
    "Hello, \(user.name)! You are \(Num.toStr(user.age))"

# Destructuring in parameters
greetShort : { name : Str, age : U32 } -> Str
greetShort = \{ name, age } ->
    "Hello, \(name)! You are \(Num.toStr(age))"

# Partial destructuring
getName : { name : Str, age : U32 } -> Str
getName = \{ name } ->  # age is ignored
    name
```

---

## Tags and Tag Unions

### Tag Basics

```roc
# Simple tags (like enums)
color = Red
direction = North

# Tags with payloads
color = Custom(40, 60, 80)
result = Ok(42)
error = Err("Something went wrong")

# Tags with named payloads (records)
point = Point({ x: 10, y: 20 })
# Or more commonly
point = Point({ x: 10, y: 20 })
```

### Tag Union Types

```roc
# Type definition
Color : [Red, Yellow, Green, Custom(U8, U8, U8)]

# Union of different tag shapes
Result a e : [Ok a, Err e]

# Nested unions
Expression : [
    Num(I64),
    Add(Expression, Expression),
    Multiply(Expression, Expression),
]
```

### Pattern Matching on Tags

```roc
# Basic matching
colorName = when color is
    Red -> "red"
    Yellow -> "yellow"
    Green -> "green"
    Custom(r, g, b) -> "rgb(\(Num.toStr(r)), \(Num.toStr(g)), \(Num.toStr(b)))"

# Matching with guards
describe = when age is
    n if n < 13 -> "child"
    n if n < 20 -> "teenager"
    _ -> "adult"

# Nested pattern matching
eval : Expression -> I64
eval = \expr ->
    when expr is
        Num(n) -> n
        Add(left, right) -> eval(left) + eval(right)
        Multiply(left, right) -> eval(left) * eval(right)
```

### Structural Tag Unions

Roc uses structural (not nominal) types:

```roc
# No need to declare the type separately
handleStatus : [Pending, Approved, Rejected] -> Str
handleStatus = \status ->
    when status is
        Pending -> "Waiting..."
        Approved -> "Done!"
        Rejected -> "Failed"

# Type is inferred from patterns
# This is equivalent to:
# Status : [Pending, Approved, Rejected]
# handleStatus : Status -> Str
```

### Open vs Closed Tag Unions

```roc
# Closed tag union (exact set)
Color : [Red, Green, Blue]

# Open tag union (can accept more)
# Used for extensibility
handleColor : [Red, Green, Blue]* -> Str
handleColor = \color ->
    when color is
        Red -> "red"
        Green -> "green"
        Blue -> "blue"
        _ -> "unknown color"

# The * makes it open to additional tags
```

---

## Pattern Matching

### When Expressions

```roc
# Basic when
result = when value is
    1 -> "one"
    2 -> "two"
    _ -> "other"

# With destructuring
when point is
    { x: 0, y: 0 } -> "origin"
    { x, y: 0 } -> "on x-axis at \(Num.toStr(x))"
    { x: 0, y } -> "on y-axis at \(Num.toStr(y))"
    { x, y } -> "at (\(Num.toStr(x)), \(Num.toStr(y)))"

# Multiple values
when (x, y) is
    (0, 0) -> "origin"
    (0, _) -> "on y-axis"
    (_, 0) -> "on x-axis"
    _ -> "elsewhere"
```

### Pattern Types

```roc
# Literal patterns
when n is
    0 -> "zero"
    1 -> "one"
    _ -> "other"

# Variable binding
when result is
    Ok(value) -> value
    Err(msg) -> "Error: \(msg)"

# List patterns
when list is
    [] -> "empty"
    [first] -> "single: \(first)"
    [first, second] -> "pair: \(first), \(second)"
    [first, ..] -> "starts with: \(first)"

# Record patterns
when user is
    { name: "Alice", .. } -> "Hello Alice!"
    { name, .. } -> "Hello \(name)!"

# Guard clauses
when n is
    x if x < 0 -> "negative"
    x if x > 0 -> "positive"
    _ -> "zero"
```

### Exhaustiveness Checking

```roc
# Compiler enforces exhaustive matching
handleColor : [Red, Green, Blue] -> Str
handleColor = \color ->
    when color is
        Red -> "red"
        Green -> "green"
        # Missing Blue - compiler error!

# Must handle all cases or use wildcard
handleColorComplete : [Red, Green, Blue] -> Str
handleColorComplete = \color ->
    when color is
        Red -> "red"
        Green -> "green"
        Blue -> "blue"  # Now complete

# Or use wildcard for remaining cases
handleColorDefault : [Red, Green, Blue] -> Str
handleColorDefault = \color ->
    when color is
        Red -> "red"
        _ -> "not red"
```

---

## Abilities

### What are Abilities?

Abilities are Roc's version of traits/typeclasses:

```roc
# Using the Eq ability
areEqual : a, a -> Bool where a implements Eq
areEqual = \x, y ->
    x == y

# Using the Inspect ability (like Debug in Rust)
debug : a -> Str where a implements Inspect
debug = \value ->
    Inspect.toStr(value)
```

### Built-in Abilities

| Ability | Purpose | Example |
|---------|---------|---------|
| `Eq` | Structural equality | `x == y` |
| `Hash` | Hashing for dictionaries | `Dict.insert(dict, key, value)` |
| `Inspect` | Debug representation | `Inspect.toStr(value)` |
| `Decode` | Deserialize from bytes | `Decode.fromBytes(bytes)` |
| `Encode` | Serialize to bytes | `Encode.toBytes(value)` |

### Automatic Derivation

Records and tags automatically implement abilities:

```roc
# This type automatically has Eq, Hash, Inspect
User : {
    name : Str,
    age : U32,
    role : [Admin, User, Guest],
}

user1 = { name: "Alice", age: 30, role: Admin }
user2 = { name: "Alice", age: 30, role: Admin }

# Eq works automatically
expect user1 == user2  # true

# Inspect works automatically
dbg(user1)  # Shows: { name: "Alice", age: 30, role: Admin }
```

### Custom Ability Implementations

```roc
# Define a custom ability
Hash implements
    hash : a -> U64 where a implements Hash

# Implement for custom type
CustomType implements [Hash]
    hash = \val ->
        # Custom hashing logic
        computeHash(val)
```

### Ability Constraints in Functions

```roc
# Single constraint
toString : a -> Str where a implements Inspect
toString = \value ->
    Inspect.toStr(value)

# Multiple constraints
compare : a, a -> [Less, Equal, Greater]
    where a implements Eq & Ord
compare = \x, y ->
    if x < y then
        Less
    else if x > y then
        Greater
    else
        Equal

# Constraints on type parameters
Map k v : ... where k implements Hash & Eq
```

---

## Result Type and Error Handling

### Result Basics

```roc
# Result type definition
Result a e : [Ok a, Err e]

# Returning Results
divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

# Using Results
when divide(10, 2) is
    Ok(result) -> Num.toStr(result)
    Err(DivByZero) -> "Cannot divide by zero"
```

### Error Propagation with Try

```roc
# Using try (!) for error propagation
calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)  # Returns early on Err
    y = divide!(x, c)  # Returns early on Err
    Ok(y)

# Equivalent to:
calculateVerbose : I64, I64, I64 -> Result I64 [DivByZero]
calculateVerbose = \a, b, c ->
    when divide(a, b) is
        Err(e) -> Err(e)
        Ok(x) ->
            when divide(x, c) is
                Err(e) -> Err(e)
                Ok(y) -> Ok(y)
```

### Multiple Error Types

```roc
# Tag union for different errors
parseAndDivide : Str, Str -> Result I64 [ParseError Str, DivByZero]
parseAndDivide = \aStr, bStr ->
    a = Str.toI64!(aStr) |> Result.mapErr(\_ -> ParseError("Invalid a"))
    b = Str.toI64!(bStr) |> Result.mapErr(\_ -> ParseError("Invalid b"))
    divide!(a, b)

# Handling all error cases
when parseAndDivide("10", "2") is
    Ok(result) -> "Result: \(Num.toStr(result))"
    Err(ParseError(msg)) -> "Parse error: \(msg)"
    Err(DivByZero) -> "Division by zero"
```

### Result Helpers

```roc
# Map over Ok value
result = divide(10, 2)
    |> Result.map(\x -> x * 2)  # Ok(10)

# Map over Err value
result = divide(10, 0)
    |> Result.mapErr(\DivByZero -> "Error: division by zero")

# Provide default on error
value = divide(10, 0)
    |> Result.withDefault(0)  # Returns 0

# Chain Results
chain : Result a e, (a -> Result b e) -> Result b e
result = divide(10, 2)
    |> Result.try(\x -> divide(x, 2))
```

---

## Zero and Default Values

Roc takes a distinctive approach to null/nil/undefined: it doesn't have them. Instead, Roc uses explicit tag unions to represent the presence or absence of values.

### No Null or Nil

```roc
# Roc does NOT have:
# - null (like Java, JavaScript)
# - nil (like Ruby, Go)
# - None (like Python's None)
# - undefined (like JavaScript)

# Instead, absence is always explicit via tag unions
```

### Optional Values with Tag Unions

```roc
# The idiomatic way to represent optional values
MaybeUser : [Some User, None]

findUser : U64 -> [Some User, None]
findUser = \id ->
    # ... search logic
    if found then
        Some(user)
    else
        None

# Using the result
when findUser(1) is
    Some(user) -> "Found: \(user.name)"
    None -> "Not found"
```

### Semantic Tag Names

Unlike a generic `Maybe` type, Roc encourages descriptive tag names:

```roc
# More descriptive than Maybe:
artist : [Loading, Loaded Artist]           # Still loading vs loaded
email : [Unspecified, Specified Str]        # Never provided vs provided
result : [Pending, Completed Data, Failed]  # State machine

# Each tells you WHY the value might be absent
```

### Zero Values for Built-in Types

```roc
# Empty/zero values for collections
emptyList : List a
emptyList = []

emptyDict : Dict k v
emptyDict = Dict.empty({})

emptySet : Set a
emptySet = Set.empty({})

emptyStr : Str
emptyStr = ""

# Numbers default to 0 when type is known
zero : I64
zero = 0
```

### Default Values in Records

Roc supports default values for record fields using the `??` syntax:

```roc
# Function with default field values
table : { height : U64, width : U64, title ?? Str, description ?? Str } -> Table
table = \{ height, width, title ?? "oak", description ?? "a wooden table" } ->
    # title defaults to "oak" if not provided
    # description defaults to "a wooden table" if not provided
    buildTable(height, width, title, description)

# Calling with defaults
table({ height: 100, width: 50 })  # uses default title and description
table({ height: 100, width: 50, title: "maple" })  # overrides title only
```

### Initialization Patterns

```roc
# Builder pattern for complex initialization
Config : {
    host : Str,
    port : U16,
    timeout : U64,
    retries : U8,
}

defaultConfig : Config
defaultConfig = {
    host: "localhost",
    port: 8080,
    timeout: 30000,
    retries: 3,
}

# Create config with overrides
myConfig = { defaultConfig & host: "api.example.com", port: 443 }
```

### Safe Access Patterns

```roc
# List access returns Result (never crashes)
when List.get(myList, 0) is
    Ok(first) -> "First element: \(first)"
    Err(OutOfBounds) -> "List was empty"

# Dict access returns Result
when Dict.get(myDict, "key") is
    Ok(value) -> value
    Err(KeyNotFound) -> defaultValue

# With default fallback
value = Dict.get(myDict, "key") |> Result.withDefault("default")
```

---

## Serialization

Roc provides serialization through the `Encoding` and `Decoding` abilities, which work with format-specific encoders/decoders like JSON.

### Encoding (Serialization)

```roc
# Basic JSON encoding
import json.Json

fruitBasket : List (Str, U32)
fruitBasket = [
    ("Apples", 10),
    ("Bananas", 12),
    ("Oranges", 5),
]

# Encode to bytes
bytes : List U8
bytes = Encode.toBytes(fruitBasket, Json.utf8)
# Result: [["Apples",10],["Bananas",12],["Oranges",5]]
```

### Decoding (Deserialization)

```roc
import json.Json

bytes : List U8
bytes = "[10, 20, 30]" |> Str.toUtf8

# Decode from bytes
result : Result (List U32) _
result = Decode.fromBytes(bytes, Json.utf8)

when result is
    Ok(numbers) -> "Got: \(Inspect.toStr(numbers))"
    Err(_) -> "Failed to decode"
```

### Records and Tags

```roc
# Records automatically derive Encoding/Decoding
User : {
    name : Str,
    age : U32,
    role : [Admin, User, Guest],
}

user : User
user = { name: "Alice", age: 30, role: Admin }

# Encode record to JSON
jsonBytes = Encode.toBytes(user, Json.utf8)
# {"name":"Alice","age":30,"role":"Admin"}

# Decode back to record
decoded : Result User _
decoded = Decode.fromBytes(jsonBytes, Json.utf8)
```

### Partial Decoding

```roc
# Decode with validation
parseUser : List U8 -> Result User [InvalidJson, MissingField Str]
parseUser = \bytes ->
    when Decode.fromBytes(bytes, Json.utf8) is
        Ok(user) -> Ok(user)
        Err(_) -> Err(InvalidJson)
```

### Custom Encoding for Opaque Types

```roc
# Opaque types need explicit ability derivation
Email := Str implements [Encoding, Decoding]

# Or custom implementation
UserId := U64 implements [
    Encoding { toEncoder: userIdEncoder },
    Decoding { decoder: userIdDecoder },
]

userIdEncoder : UserId -> Encoder fmt where fmt implements EncoderFormatting
userIdEncoder = \@UserId(id) ->
    Encode.u64(id)

userIdDecoder : Decoder UserId fmt where fmt implements DecoderFormatting
userIdDecoder =
    Decode.u64 |> Decode.map(@UserId)
```

### Encoding Ability Definition

```roc
# From Encode.roc
Encoding implements
    toEncoder : val -> Encoder fmt
        where val implements Encoding, fmt implements EncoderFormatting

# From Decode.roc
Decoding implements
    decoder : Decoder val fmt
        where val implements Decoding, fmt implements DecoderFormatting
```

### Limitations

```roc
# Note: Dict encoding/decoding has limited support
# See https://github.com/roc-lang/roc/issues/5294

# Functions cannot be encoded (they don't implement Encoding)
# This won't work:
# myFunc = \x -> x + 1
# Encode.toBytes(myFunc, Json.utf8)  # Error!
```

---

## Build System

Roc's build system uses the `roc` CLI and a platform-based architecture. Understanding this is essential for project setup and development workflow.

### CLI Commands

```bash
# Run application directly (compiles and runs)
roc main.roc

# Build optimized executable
roc build main.roc
roc build main.roc --optimize  # maximum optimization

# Development mode (faster compilation, includes dbg output)
roc dev main.roc

# Run tests (executes all top-level expect expressions)
roc test main.roc

# Start REPL
roc repl

# Format code
roc format main.roc
roc format .  # format all .roc files

# Check types without building
roc check main.roc

# Generate documentation
roc docs package/*.roc
```

### Application Structure

```roc
# main.roc - Application header
app [main!] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.20.0/X73hGh05nNTkDHU06FHC0YfFaQB1pimX7gncRcao5mU.tar.br"
}

import pf.Stdout

main! = |_args|
    Stdout.line!("Hello, World!")
```

### Platform URLs

```roc
# Platform URL format
# https://host/path/HASH.tar.br
#                  ^^^^
#                  BLAKE3 hash for integrity verification

# Common platforms
pf: platform "https://github.com/roc-lang/basic-cli/..."      # CLI apps
pf: platform "https://github.com/roc-lang/basic-webserver/..." # Web servers

# Local platform (for development)
pf: platform "../my-platform/main.roc"
```

### Package Structure

```roc
# package/main.roc - Package header
package [
    MyModule,
    AnotherModule,
] {
    json: "https://github.com/lukewilliamboswell/roc-json/..."
}
```

### Multi-Module Projects

```
my-app/
├── main.roc           # Application entry point
├── User.roc           # User module
├── Database.roc       # Database module
└── Utils/
    ├── Strings.roc    # String utilities
    └── Math.roc       # Math utilities
```

```roc
# main.roc
app [main!] { pf: platform "..." }

import pf.Stdout
import User
import Database
import Utils.Strings

main! = |_args|
    user = User.create("Alice", 30)
    Stdout.line!(User.getName(user))
```

### Building for Different Targets

```bash
# Default: native executable
roc build main.roc

# WebAssembly (when platform supports it)
roc build --target wasm32 main.roc

# Specific output name
roc build main.roc --output myapp
```

### Package Management

```roc
# Packages are specified by URL with hash
app [main!] {
    pf: platform "...",
    json: "https://github.com/lukewilliamboswell/roc-json/releases/download/0.10.0/KbIfTNbxShRX1A1FgXei1SpO5Jn8sgP6HP6PXbi-xyA.tar.br",
}

# Packages are cached locally after first download
# Cache location: ~/.cache/roc (Unix) or %APPDATA%\Roc (Windows)
```

### Build Distribution

```bash
# Create distributable package
roc build --bundle .tar.br package/main.roc

# The output includes the BLAKE3 hash for the URL
```

### Common Build Issues

```bash
# Clear cache if experiencing issues
rm -rf ~/.cache/roc

# Verify platform/package integrity
# (automatic - hash mismatch will fail with error)

# Check for type errors without full build
roc check main.roc
```

---

## Type System Fundamentals

### Type Inference

```roc
# Types are inferred
double = \x -> x * 2
# Inferred type: Num a -> Num a

# Can add explicit annotations
double : I64 -> I64
double = \x -> x * 2

# Type parameters
identity : a -> a
identity = \x -> x

# Type parameters with constraints
show : a -> Str where a implements Inspect
show = \x -> Inspect.toStr(x)
```

### Number Types

```roc
# Integer types
i8, i16, i32, i64, i128  # Signed integers
u8, u16, u32, u64, u128  # Unsigned integers

# Flexible numbers (type inferred from usage)
x = 42       # Num *
y = x + 1    # Still Num *, becomes concrete when needed

# Explicit typing
x : I64
x = 42

# Floating point
f32, f64     # 32-bit and 64-bit floats
pi : F64
pi = 3.14159
```

### Function Types

```roc
# Function with single parameter
increment : I64 -> I64

# Multiple parameters (curried)
add : I64, I64 -> I64

# Function taking a function
map : List a, (a -> b) -> List b

# Function with abilities constraint
sort : List a -> List a where a implements Ord
```

### Type Aliases

```roc
# Create type aliases for clarity
UserId : U64
UserName : Str

User : {
    id : UserId,
    name : UserName,
    email : Str,
}

# Opaque types (hide implementation)
Age := U32

createAge : U32 -> Age
createAge = \n -> @Age(n)

getAge : Age -> U32
getAge = \@Age(n) -> n
```

---

## Functional Patterns

### List Operations

```roc
# Map
numbers = [1, 2, 3, 4, 5]
doubled = List.map(numbers, \n -> n * 2)
# [2, 4, 6, 8, 10]

# Filter
evens = List.keepIf(numbers, \n -> n % 2 == 0)
# [2, 4]

# Fold (reduce)
sum = List.walk(numbers, 0, \acc, n -> acc + n)
# 15

# Find
maybeFirst = List.findFirst(numbers, \n -> n > 3)
# Ok(4)

# Chain operations with pipeline
result = numbers
    |> List.map(\n -> n * 2)
    |> List.keepIf(\n -> n > 5)
    |> List.walk(0, Num.add)
```

### Pipeline Operator

```roc
# Without pipeline
result = add(multiply(2, 3), 4)

# With pipeline (left to right)
result = 2
    |> multiply(3)
    |> add(4)

# Common with list operations
users
    |> List.map(\u -> u.name)
    |> List.sortAsc
    |> Str.joinWith(", ")
```

### Dict (Dictionary/Map)

```roc
# Create dictionary
scores = Dict.empty({})
    |> Dict.insert("Alice", 100)
    |> Dict.insert("Bob", 85)
    |> Dict.insert("Charlie", 92)

# Get value
aliceScore = Dict.get(scores, "Alice")
# Ok(100)

# Update value
newScores = Dict.update(scores, "Alice", \maybeScore ->
    when maybeScore is
        Some(score) -> Some(score + 10)
        None -> None
)

# Keys and values
allNames = Dict.keys(scores)
allScores = Dict.values(scores)
```

### Set Operations

```roc
# Create sets
set1 = Set.fromList([1, 2, 3, 4])
set2 = Set.fromList([3, 4, 5, 6])

# Union
union = Set.union(set1, set2)
# {1, 2, 3, 4, 5, 6}

# Intersection
intersection = Set.intersection(set1, set2)
# {3, 4}

# Difference
diff = Set.difference(set1, set2)
# {1, 2}

# Contains
hasThree = Set.contains(set1, 3)
# Bool.true
```

---

## Testing with Expect

### Basic Expects

```roc
# Simple test
expect 1 + 1 == 2

# Test with variables
add = \a, b -> a + b
expect add(2, 3) == 5

# Multiple expects
expect
    result = divide(10, 2)
    result == Ok(5)

expect
    result = divide(10, 0)
    result == Err(DivByZero)
```

### Inline Expects

```roc
# Verify assumptions in functions
factorial : U64 -> U64
factorial = \n ->
    # Verify our assumption
    expect n <= 20  # Factorial grows quickly!

    when n is
        0 -> 1
        _ -> n * factorial(n - 1)
```

### Testing with roc test

```roc
# Top-level expects run with `roc test`
expect List.map([1, 2, 3], \x -> x * 2) == [2, 4, 6]

expect
    users = [
        { name: "Alice", age: 30 },
        { name: "Bob", age: 25 },
    ]
    oldest = List.sortWith(users, \a, b ->
        Num.compare(b.age, a.age)
    )
    List.first(oldest) == Ok({ name: "Alice", age: 30 })
```

---

## Common Idioms

### Option Pattern (Maybe)

```roc
# Roc doesn't have a built-in Maybe/Option
# Use tag unions instead
MaybeUser : [Some User, None]

findUser : U64 -> [Some User, None]
findUser = \id ->
    # ... search logic
    if found then
        Some(user)
    else
        None

# Using the result
when findUser(1) is
    Some(user) -> "Found: \(user.name)"
    None -> "Not found"
```

### Parsing Pattern

```roc
# Parser combinator style
Parser a : Str -> Result { value : a, rest : Str } [ParseError Str]

parseInt : Parser I64
parseInt = \input ->
    when Str.toI64(input) is
        Ok(n) -> Ok({ value: n, rest: "" })
        Err(_) -> Err(ParseError("Not a number"))

# Chain parsers
parsePoint : Parser { x : I64, y : I64 }
parsePoint = \input ->
    { value: x, rest: afterX } = parseInt!(input)
    { value: y, rest: afterY } = parseInt!(afterX)
    Ok({ value: { x, y }, rest: afterY })
```

### Task Pattern (Effects)

```roc
# Platform-provided Task type for effects
Task a err : [Task a err]

# Chaining tasks
main : Task {} []
main =
    # Read file
    content = File.readUtf8!("input.txt")

    # Process content
    processed = String.toUpper(content)

    # Write result
    File.writeUtf8!("output.txt", processed)

    # Log completion
    Stdout.line!("Done!")
```

### Builder Pattern

```roc
# Use records with update syntax
RequestBuilder : {
    url : Str,
    method : [Get, Post, Put, Delete],
    headers : Dict Str Str,
    body : [Some Str, None],
}

defaultRequest : Str -> RequestBuilder
defaultRequest = \url -> {
    url,
    method: Get,
    headers: Dict.empty({}),
    body: None,
}

# Build requests
request = defaultRequest("https://api.example.com")
    |> \r -> { r & method: Post }
    |> \r -> { r & headers: Dict.insert(r.headers, "Content-Type", "application/json") }
    |> \r -> { r & body: Some("{\"key\": \"value\"}") }
```

---

## Troubleshooting

### Type Mismatch Errors

**Problem:** "Type mismatch in when branch"

```roc
# Wrong - branches return different types
value = when condition is
    Bool.true -> 42
    Bool.false -> "false"  # Error!
```

**Fix:** Ensure all branches return the same type:
```roc
value = when condition is
    Bool.true -> "true"
    Bool.false -> "false"
```

### Non-Exhaustive Pattern Match

**Problem:** "Pattern match is not exhaustive"

```roc
# Wrong - missing Blue case
colorName = when color is
    Red -> "red"
    Green -> "green"
    # Missing Blue!
```

**Fix:** Add all cases or use wildcard:
```roc
# Option 1: Add missing case
colorName = when color is
    Red -> "red"
    Green -> "green"
    Blue -> "blue"

# Option 2: Use wildcard
colorName = when color is
    Red -> "red"
    _ -> "other"
```

### Circular Type Definitions

**Problem:** Type depends on itself incorrectly

```roc
# Correct recursive type
List a : [Nil, Cons a (List a)]

# Wrong - missing tag wrapper
BadList a : [a, BadList a]  # Error!
```

**Fix:** Wrap recursive references in tags:
```roc
List a : [Nil, Cons a (List a)]
```

### Ability Constraint Errors

**Problem:** "Type doesn't implement required ability"

```roc
# Wrong - function has no Eq
compare : a, a -> Bool where a implements Eq
compare = \x, y -> x == y

# Trying to use with function
fn = \x -> x + 1
result = compare(fn, fn)  # Error: function doesn't implement Eq
```

**Fix:** Only use types that implement the required ability:
```roc
result = compare(42, 42)  # OK: I64 implements Eq
```

### Task Error Propagation

**Problem:** Not handling task errors properly

```roc
# Wrong - ignoring potential errors
main =
    content = File.readUtf8!("missing.txt")  # Might fail!
    Stdout.line!(content)
```

**Fix:** Handle errors explicitly:
```roc
main =
    when File.readUtf8("missing.txt") is
        Ok(content) -> Stdout.line!(content)
        Err(err) -> Stderr.line!("Error: \(Inspect.toStr(err))")
```

---

## Module System

### Package vs Application vs Platform

Roc has three distinct module types:

```roc
# Application - Entry point with platform dependency
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

# Package - Reusable library
package [List, Dict, Set] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

# Platform - Provides I/O capabilities (advanced)
platform "my-platform"
    requires {} { main : Task {} [] }
    exposes [Stdout, File, Task]
    packages {}
    imports []
    provides [mainForHost]
```

### Exposing and Importing

```roc
# Module declaration with exports
interface MyModule
    exposes [
        User,           # Type
        createUser,     # Function
        updateUser,     # Function
    ]
    imports [
        pf.Stdout,
        pf.Task.{ Task },
    ]

# Define exports
User : {
    name : Str,
    age : U32,
}

createUser : Str, U32 -> User
createUser = \name, age -> { name, age }

updateUser : User, U32 -> User
updateUser = \user, newAge -> { user & age: newAge }
```

### Import Patterns

```roc
# Import from platform
import pf.Stdout
import pf.Task exposing [Task]

# Import multiple from same module
import pf.File exposing [readUtf8, writeUtf8]

# Import with alias (not yet implemented, but planned)
# import pf.Stdout as Out

# Import from package
import List
import Dict exposing [Dict]
import Set

# Use imported items
main : Task {} []
main =
    # Use qualified
    List.map([1, 2, 3], \n -> n * 2)

    # Use exposed directly
    task = Task.ok({})
```

### Module Organization

```
my-app/
├── main.roc           # Application entry point
├── User.roc           # User module
├── Post.roc           # Post module
└── Utils/
    ├── Strings.roc    # String utilities
    └── Math.roc       # Math utilities
```

```roc
# main.roc
app [main] {
    pf: platform "..."
}

import pf.Stdout
import pf.Task exposing [Task]
import User
import Post

main : Task {} []
main =
    user = User.create("Alice", 30)
    post = Post.create(user, "Hello, World!")
    Stdout.line!("Created post by \(User.getName(user))")

# User.roc
interface User
    exposes [User, create, getName, getAge]
    imports []

User : {
    name : Str,
    age : U32,
}

create : Str, U32 -> User
create = \name, age -> { name, age }

getName : User -> Str
getName = \user -> user.name

getAge : User -> U32
getAge = \user -> user.age
```

### Visibility and Encapsulation

```roc
# Only exposed items are public
interface Counter
    exposes [Counter, new, increment, getValue]
    imports []

# Opaque type - internal structure hidden
Counter := { count : U32 }

# Public API
new : Counter
new = @Counter({ count: 0 })

increment : Counter -> Counter
increment = \@Counter({ count }) ->
    @Counter({ count: count + 1 })

getValue : Counter -> U32
getValue = \@Counter({ count }) -> count

# Private helper (not exposed)
internalHelper : U32 -> U32
internalHelper = \n -> n * 2
```

### Package Structure

```roc
# Package with multiple modules
package [
    # Export types
    User,
    Post,
    Comment,

    # Export functions
    createUser,
    createPost,
    addComment,
] {
    pf: platform "..."
}

import User
import Post
import Comment

# Re-export from submodules
User : User.User
createUser : User.create

Post : Post.Post
createPost : Post.create

Comment : Comment.Comment
addComment : Comment.add
```

### Platform Interface

Platforms define the interface between pure Roc code and host capabilities:

```roc
# Platform exposes capabilities
platform "basic-cli"
    requires {} { main : Task {} [] }
    exposes [
        Stdout,
        Stderr,
        File,
        Path,
        Env,
        Arg,
        Task,
    ]
    packages {}
    imports []
    provides [mainForHost]

# Application imports from platform
app [main] { pf: platform "..." }

import pf.Stdout
import pf.File
import pf.Task exposing [Task]

# Application provides the required main function
main : Task {} []
main =
    content = File.readUtf8!("input.txt")
    Stdout.line!(content)
```

### Dependency Management

```roc
# Applications depend on platforms
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

# Packages depend on platforms (for types)
package [myLib] {
    pf: platform "..."
}

# Platform URLs point to packages
# Format: https://host/path/to/archive.tar.br
# Hash in URL ensures integrity
```

### Module Best Practices

```roc
# Interface - public API design
interface Database
    exposes [
        # Types
        Connection,
        QueryResult,

        # Core functions
        connect,
        disconnect,
        query,

        # Helpers
        mapRows,
    ]
    imports [
        pf.Task.{ Task },
    ]

# Clear separation of concerns
Connection := { host : Str, port : U16 }  # Opaque
QueryResult : { rows : List (Dict Str Str) }  # Transparent

# Type-driven design
connect : Str, U16 -> Task Connection [ConnectionFailed Str]
disconnect : Connection -> Task {} []
query : Connection, Str -> Task QueryResult [QueryFailed Str]
```

### Common Module Patterns

```roc
# 1. Builder pattern with module
interface RequestBuilder
    exposes [Request, new, withHeader, withBody, build]
    imports []

Request := {
    url : Str,
    headers : Dict Str Str,
    body : [Some Str, None],
}

new : Str -> Request
new = \url -> @Request({
    url,
    headers: Dict.empty({}),
    body: None,
})

withHeader : Request, Str, Str -> Request
withHeader = \@Request(req), key, value ->
    @Request({ req & headers: Dict.insert(req.headers, key, value) })

withBody : Request, Str -> Request
withBody = \@Request(req), body ->
    @Request({ req & body: Some(body) })

# 2. Smart constructors
interface Email
    exposes [Email, fromStr, toString]
    imports []

Email := Str

fromStr : Str -> Result Email [InvalidEmail]
fromStr = \str ->
    if Str.contains(str, "@") then
        Ok(@Email(str))
    else
        Err(InvalidEmail)

toString : Email -> Str
toString = \@Email(str) -> str

# 3. Namespace-style modules
interface StringUtils
    exposes [capitalize, reverse, isPalindrome]
    imports []

capitalize : Str -> Str
capitalize = \str ->
    when Str.toUtf8(str) is
        [] -> ""
        [first, .. as rest] ->
            Str.fromUtf8([Str.toUpper(first)] |> List.concat(rest))

reverse : Str -> Str
reverse = \str ->
    str
    |> Str.toUtf8
    |> List.reverse
    |> Str.fromUtf8

isPalindrome : Str -> Bool
isPalindrome = \str ->
    str == reverse(str)
```

---

## Concurrency

Roc's concurrency model is Task-based and platform-provided. Unlike languages with built-in threading, Roc delegates all concurrent execution to the platform layer. For cross-language comparison, see `patterns-concurrency-dev`.

### Task-Based Concurrency

```roc
# Task represents an effect that may run concurrently
# Type: Task ok err
#   ok  - Success type
#   err - Error type

import pf.Task exposing [Task]
import pf.Stdout
import pf.File

# Sequential execution
main : Task {} []
main =
    # Each step waits for previous
    content1 = File.readUtf8!("file1.txt")
    content2 = File.readUtf8!("file2.txt")
    Stdout.line!("Read both files sequentially")
```

### Platform-Provided Concurrency

Platforms may provide concurrent execution primitives:

```roc
# Platform might expose concurrent operations
import pf.Task exposing [Task, parallel]
import pf.File

# Hypothetical concurrent file reading
readBothFiles : Task (Str, Str) [FileErr]
readBothFiles =
    # Platform handles concurrent execution
    Task.parallel2(
        File.readUtf8("file1.txt"),
        File.readUtf8("file2.txt")
    )

# Pattern: Platform provides concurrency, app stays pure
main : Task {} []
main =
    (content1, content2) = readBothFiles!
    Stdout.line!("Read files concurrently via platform")
```

### No Built-In Threading

```roc
# Roc applications don't directly manage threads
# All concurrency is platform capability

# This is NOT possible in Roc:
# - spawn_thread()
# - async/await (no built-in)
# - goroutines
# - manual thread pools

# Instead: Platform provides concurrent primitives
# Application code remains pure and sequential
```

### Task Composition

```roc
# Tasks compose like other values
import pf.Task exposing [Task]
import pf.Http
import pf.Stdout

# Chain tasks
fetchAndPrint : Str -> Task {} [HttpErr]
fetchAndPrint = \url ->
    response = Http.get!(url)
    Stdout.line!(response.body)

# Multiple independent tasks
fetchMultiple : List Str -> Task (List Str) [HttpErr]
fetchMultiple = \urls ->
    # Platform may execute these concurrently
    List.map(urls, \url ->
        Http.get(url)
        |> Task.map(\resp -> resp.body)
    )
    |> Task.sequence  # Platform-provided
```

### Error Handling in Concurrent Tasks

```roc
# Each Task carries its error type
import pf.Task exposing [Task]

# Task that may fail
riskyOperation : Task Str [NetworkErr, ParseErr]
riskyOperation =
    data = fetchData!  # May fail with NetworkErr
    parsed = parseData!(data)  # May fail with ParseErr
    Task.ok(parsed)

# Handle errors
safeOperation : Task Str []
safeOperation =
    when riskyOperation is
        Ok(result) -> Task.ok(result)
        Err(NetworkErr) -> Task.ok("Network error occurred")
        Err(ParseErr) -> Task.ok("Parse error occurred")
```

### Concurrency Patterns

```roc
# Pattern 1: Batch processing
processBatch : List Item -> Task (List Result) [ProcessErr]
processBatch = \items ->
    # Platform may parallelize map
    items
    |> List.map(processItem)
    |> Task.sequence

# Pattern 2: Timeout
withTimeout : Task a err, U64 -> Task a [Timeout, TaskErr err]
withTimeout = \task, ms ->
    # Platform provides timeout mechanism
    Task.timeout(task, ms)

# Pattern 3: Retry
retry : Task a err, U32 -> Task a err
retry = \task, attempts ->
    when task is
        Ok(result) -> Task.ok(result)
        Err(e) if attempts > 0 -> retry(task, attempts - 1)
        Err(e) -> Task.err(e)
```

### Platform Responsibilities

Platforms handle:
- Thread pool management
- Work scheduling
- Concurrent I/O
- Synchronization primitives
- Event loops

Applications handle:
- Pure data transformations
- Task composition
- Error handling logic
- Business logic

```roc
# Clear separation
┌─────────────────────────────┐
│   Application (Pure Roc)    │
│                              │
│  • Task composition          │
│  • Business logic            │
│  • Data transformation       │
└──────────────┬───────────────┘
               │ Task interface
┌──────────────▼───────────────┐
│   Platform (Host + Roc API)  │
│                              │
│  • Thread management         │
│  • Concurrent execution      │
│  • I/O operations            │
│  • Synchronization           │
└──────────────────────────────┘
```

### Current State and Future

```roc
# As of 2025, Roc's concurrency is evolving
# Current: Task-based, platform-specific
# Expected: Standardized concurrent primitives in platform APIs

# Watch for:
# - Task.parallel, Task.race
# - Structured concurrency helpers
# - Standard async patterns

# Note: This section reflects current design
# May evolve as language matures
```

---

## Metaprogramming

Roc takes a minimalist approach to metaprogramming. Unlike languages with macro systems, Roc focuses on simplicity and relies on code generation tools outside the language. For cross-language comparison, see `patterns-metaprogramming-dev`.

### No Built-In Macros

```roc
# Roc does NOT have:
# - Macro systems (like Rust, Elixir)
# - Decorators (like Python, TypeScript)
# - Annotations (like Java)
# - Template metaprogramming (like C++)
# - Code generation directives

# Philosophy: Keep the language simple
# Metaprogramming happens outside the language
```

### Abilities as Alternative

Abilities provide some metaprogramming-like features through automatic derivation:

```roc
# Automatic implementations
User : {
    name : Str,
    age : U32,
    role : [Admin, User, Guest],
}

# These are automatically derived:
# - Eq (structural equality)
# - Hash (for Dict keys)
# - Inspect (debug representation)
# - Encode/Decode (serialization)

user1 = { name: "Alice", age: 30, role: Admin }
user2 = { name: "Alice", age: 30, role: Admin }

# Eq works automatically
expect user1 == user2  # true

# Inspect works automatically
dbg(user1)  # Shows structure
```

### Code Generation Outside Roc

```bash
# External code generation tools
# Example: Generate Roc from schema

# schema.json → generate_roc.py → types.roc

# types.roc (generated)
# DO NOT EDIT - Generated from schema.json

User : {
    name : Str,
    email : Str,
    age : U32,
}

Post : {
    title : Str,
    content : Str,
    author : User,
}
```

### Opaque Types for Encapsulation

```roc
# Opaque types provide controlled abstraction
interface UserId
    exposes [UserId, fromU64, toU64, new]
    imports []

# Internal representation hidden
UserId := U64

# Smart constructors control creation
new : -> UserId
new = @UserId(generateId())

fromU64 : U64 -> UserId
fromU64 = \id -> @UserId(id)

toU64 : UserId -> U64
toU64 = \@UserId(id) -> id

# Pattern unwrapping only in this module
# External code can't access internal U64
```

### Type-Driven Development

Instead of metaprogramming, Roc encourages type-driven design:

```roc
# Phantom types for state machines
Request state : { url : Str, headers : Dict Str Str }

# States tracked in type system
[Unsent, Prepared, Sent]

buildRequest : Str -> Request [Unsent]
buildRequest = \url -> { url, headers: Dict.empty({}) }

prepare : Request [Unsent] -> Request [Prepared]
prepare = \req -> req  # Type changes, value stays same

send : Request [Prepared] -> Task Response [HttpErr]
send = \req -> Http.send(req)

# Type system prevents:
# send(buildRequest("..."))  # Error: can't send Unsent request
```

### Workarounds for Common Metaprogramming Needs

```roc
# 1. Instead of derive macros → Use abilities
# Automatic: Eq, Hash, Inspect, Encode, Decode

# 2. Instead of decorators → Use higher-order functions
logged : (a -> b), Str -> (a -> b)
logged = \fn, name ->
    \arg ->
        dbg("Calling \(name)")
        result = fn(arg)
        dbg("Result: \(Inspect.toStr(result))")
        result

myFunction : U32 -> U32
myFunction = \x -> x + 1

loggedFunction = logged(myFunction, "myFunction")

# 3. Instead of code generation → External tools
# Use build scripts, code generators, or platform-specific tools

# 4. Instead of reflection → Static typing
# Design APIs that don't need runtime inspection
```

### Build-Time Tools

```bash
# Roc supports external build-time generation

# 1. Shell scripts
#!/bin/bash
# generate_types.sh
python3 codegen.py schema.json > generated/types.roc

# 2. Makefile
generated/types.roc: schema.json codegen.py
    python3 codegen.py schema.json > generated/types.roc

# 3. Just tasks (recommended)
generate:
    python3 codegen.py schema.json > generated/types.roc

# 4. Custom tools
roc-codegen --input schema.json --output generated/types.roc
```

### Design Philosophy

```
Why no metaprogramming in Roc?

Pros of current approach:
✓ Simpler language to learn
✓ Easier to understand code
✓ No hidden complexity
✓ Better tooling support
✓ Faster compilation
✓ Clear separation of concerns

Cons:
✗ More boilerplate for repetitive code
✗ External tools needed for generation
✗ Less flexibility than macro systems

Trade-off: Simplicity over flexibility
```

### Future Considerations

```roc
# As of 2025, Roc may evolve to include:
# - More powerful ability derivation
# - Build hooks in the package system
# - Standard code generation conventions

# Watch for:
# - Expanded automatic derivations
# - Platform-provided build tooling
# - Community code generation tools

# Note: This reflects current design philosophy
# May change as language matures and use cases emerge
```

---

## Cross-Cutting Patterns

For language-agnostic patterns and cross-language translation guides, see:

- `patterns-concurrency-dev` - Compare Roc's Task model with async/await, goroutines, and actors
- `patterns-metaprogramming-dev` - Compare Roc's minimalist approach with macros, decorators, and codegen
- `patterns-serialization-dev` - JSON, YAML encoding/decoding with Roc's Encode/Decode abilities

---

## References

- [Roc Tutorial](https://www.roc-lang.org/tutorial)
- [Roc Examples](https://www.roc-lang.org/examples/)
- [Roc Abilities Documentation](https://www.roc-lang.org/abilities)
- [Platforms and Apps](https://www.roc-lang.org/platforms)
- [Roc FAQ](https://github.com/Ivo-Balbaert/roc-lang/blob/main/FAQ.md)
- Specialized skills: `lang-roc-patterns-dev`, `lang-roc-platform-dev`
