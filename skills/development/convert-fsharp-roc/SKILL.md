---
name: convert-fsharp-roc
description: Convert F# code to idiomatic Roc. Use when migrating F# projects to Roc, translating F# patterns to idiomatic Roc, or refactoring F# codebases. Extends meta-convert-dev with F#-to-Roc specific patterns.
---

# Convert F# to Roc

Convert F# code to idiomatic Roc. This skill extends `meta-convert-dev` with F#-to-Roc specific type mappings, idiom translations, and architectural guidance.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: F# types → Roc types
- **Idiom translations**: F# patterns → idiomatic Roc
- **Error handling**: F# Result/Option → Roc Result/tag unions
- **Platform shift**: .NET runtime → Roc platform model
- **Paradigm alignment**: Both functional-first, but different architectures

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- F# language fundamentals - see `lang-fsharp-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → F#) - see `convert-roc-fsharp`

---

## Quick Reference

| F# | Roc | Notes |
|----------|----------|-------|
| `string` | `Str` | Immutable strings |
| `int` | `I64` | Default signed integer |
| `float` | `F64` | 64-bit floating point |
| `bool` | `Bool` | Boolean values |
| `'a list` | `List a` | Immutable lists |
| `'a array` | `List a` | Arrays become lists |
| `Map<'k,'v>` | `Dict k v` | Immutable dictionaries |
| `Set<'a>` | `Set a` | Immutable sets |
| `Option<'a>` | `[Some a, None]` | Optional values |
| `Result<'a,'e>` | `Result a e` | Error handling |
| `{| ... |}` anonymous record | `{ ... }` record | Structural records |
| `type X = ...` discriminated union | `[...]` tag union | Sum types |
| `Async<'a>` | `Task a err` | Async/effects via platform |
| `unit` | `{}` | Empty record (not quite `()`) |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Preserve semantics** over syntax similarity
4. **Adopt Roc idioms** - understand platform/application split
5. **Handle edge cases** - null handling, error paths, effects
6. **Test equivalence** - same inputs → same outputs

---

## Paradigm Translation

### Mental Model Shift: .NET Runtime → Platform Model

Both F# and Roc are functional-first languages, but they differ fundamentally in how they handle effects:

| F# Concept | Roc Approach | Key Insight |
|------------------|-------------------|-------------|
| .NET runtime with GC | Platform provides runtime | Runtime is external to application |
| `Async<'a>` workflows | `Task ok err` via platform | Effects delegated to platform |
| Direct I/O (Console, File) | Platform-provided I/O | Application remains pure |
| Mutable state allowed | Immutable by default | No mutable keyword |
| Exception handling | Result type only | No runtime exceptions |
| Type providers | Code generation external | No compile-time metaprogramming |

### Architecture Mental Model

```
F# (.NET)                          Roc (Platform Model)
┌─────────────────────┐           ┌─────────────────────┐
│   Your F# Code      │           │   Your Roc Code     │
│  (can do I/O)       │           │   (pure only)       │
│  ↓                  │           │   ↓                 │
│  .NET BCL           │           │   Platform API      │
│  ↓                  │           │   ↓                 │
│  CLR Runtime        │           │   Platform Host     │
└─────────────────────┘           └─────────────────────┘
     Everything in                    Clear separation
     same runtime                     between pure & effects
```

**Key shift:** In F#, you can call `Console.WriteLine` anywhere. In Roc, all I/O goes through the platform's `Task` type.

---

## Type System Mapping

### Primitive Types

| F# | Roc | Notes |
|----------|----------|-------|
| `string` | `Str` | Both immutable UTF-8 |
| `int` | `I64` | F# int is 32-bit, Roc defaults to 64 |
| `int16`, `int32`, `int64` | `I16`, `I32`, `I64` | Explicit sizes match |
| `uint16`, `uint32`, `uint64` | `U16`, `U32`, `U64` | Unsigned variants |
| `byte` | `U8` | 8-bit unsigned |
| `sbyte` | `I8` | 8-bit signed |
| `float`, `double` | `F32`, `F64` | F# float is F64 |
| `decimal` | No direct equivalent | Use external library or F64 |
| `bool` | `Bool` | Direct mapping |
| `char` | Use `Str` | Roc has no char type |
| `unit` | `{}` | Empty record, not `()` |

### Collection Types

| F# | Roc | Notes |
|----------|----------|-------|
| `'a list` | `List a` | Both immutable, structural sharing |
| `'a array` | `List a` | Roc lists handle array use cases |
| `'a seq` | `List a` | Lazy sequences become lists |
| `Map<'k,'v>` | `Dict k v` | Immutable maps |
| `Set<'a>` | `Set a` | Immutable sets |
| `('a * 'b)` tuple | `(a, b)` | Tuples map directly |
| `ResizeArray<'a>` | `List a` | Mutable becomes immutable |

### Composite Types

| F# | Roc | Notes |
|----------|----------|-------|
| `type X = { ... }` record | `{ ... }` record | Structural typing in both |
| `{| ... |}` anonymous record | `{ ... }` record | All Roc records are structural |
| `type X = A \| B \| C` DU | `[A, B, C]` tag union | Direct correspondence |
| `type X = A of int` single-case DU | `[A I64]` or opaque type | For newtype, use opaque |
| `Option<'a>` | `[Some a, None]` | Built-in DU vs tag union |
| `Result<'ok,'err>` | `Result ok err` | Built-in DU vs tag union |
| `Choice<'a,'b>` | `[A a, B b]` tag union | No built-in Choice |

### F# Specific Types → Roc

| F# Type | Roc Strategy | Notes |
|----------|----------|-------|
| `Async<'a>` | `Task a err` | Platform-provided |
| `Task<'a>` (.NET Task) | `Task a err` | Platform-provided |
| `Lazy<'a>` | Thunks `({} -> a)` | No built-in lazy |
| `ref<'a>` | Not needed | No mutable references |
| `'a -> 'b` function | `a -> b` | Functions map directly |
| Type providers | External codegen | No compile-time metaprogramming |
| Units of measure | Custom validation | No built-in units |

---

## Idiom Translation

### Pattern 1: Option Handling

**F#:**
```fsharp
let findUser id =
    users |> List.tryFind (fun u -> u.Id = id)

let userName =
    findUser 1
    |> Option.map (fun u -> u.Name)
    |> Option.defaultValue "Unknown"
```

**Roc:**
```roc
findUser : I64 -> [Some User, None]
findUser = \id ->
    List.findFirst(users, \u -> u.id == id)
    |> Result.toOption  # Convert Result to Option-like tag

userName =
    when findUser(1) is
        Some(u) -> u.name
        None -> "Unknown"
```

**Why this translation:**
- F# has built-in `Option<'a>` type; Roc uses tag unions `[Some a, None]`
- F# has `Option.map`; Roc uses pattern matching with `when`
- Both are structural sum types under the hood

### Pattern 2: Result for Error Handling

**F#:**
```fsharp
let divide x y =
    if y = 0 then
        Error "Division by zero"
    else
        Ok (x / y)

let calculate a b c =
    result {
        let! x = divide a b
        let! y = divide x c
        return y
    }
```

**Roc:**
```roc
divide : I64, I64 -> Result I64 [DivByZero]
divide = \x, y ->
    if y == 0 then
        Err(DivByZero)
    else
        Ok(x // y)

calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)  # Try operator for error propagation
    y = divide!(x, c)
    Ok(y)
```

**Why this translation:**
- F# has computation expressions (`result { ... }`); Roc uses try operator (`!`)
- F# `Error "msg"` uses strings; Roc `Err(DivByZero)` uses typed tags
- Both propagate errors up the call stack

### Pattern 3: List Operations

**F#:**
```fsharp
let result =
    items
    |> List.filter (fun x -> x.Active)
    |> List.map (fun x -> x.Value)
    |> List.sum
```

**Roc:**
```roc
result =
    items
    |> List.keepIf(\x -> x.active)  # filter → keepIf
    |> List.map(\x -> x.value)
    |> List.walk(0, Num.add)  # sum via walk (fold)
```

**Why this translation:**
- F# `filter` → Roc `keepIf` (more descriptive name)
- F# `sum` → Roc `walk(0, Num.add)` (explicit fold)
- Both use pipeline operator (`|>`) idiomatically

### Pattern 4: Pattern Matching

**F#:**
```fsharp
type Color =
    | Red
    | Green
    | Blue
    | Custom of r: int * g: int * b: int

let describe color =
    match color with
    | Red -> "red"
    | Green -> "green"
    | Blue -> "blue"
    | Custom (r, g, b) -> $"rgb({r}, {g}, {b})"
```

**Roc:**
```roc
Color : [Red, Green, Blue, Custom(I64, I64, I64)]

describe : Color -> Str
describe = \color ->
    when color is
        Red -> "red"
        Green -> "green"
        Blue -> "blue"
        Custom(r, g, b) -> "rgb(\(Num.toStr(r)), \(Num.toStr(g)), \(Num.toStr(b)))"
```

**Why this translation:**
- F# discriminated unions → Roc tag unions (nearly identical)
- F# `match` → Roc `when` (same exhaustiveness checking)
- F# interpolation `$"{x}"` → Roc interpolation `\(x)` (different syntax)

### Pattern 5: Record Updates

**F#:**
```fsharp
type Person = {
    FirstName: string
    LastName: string
    Age: int
}

let person = { FirstName = "Alice"; LastName = "Smith"; Age = 30 }
let olderPerson = { person with Age = 31 }
```

**Roc:**
```roc
Person : {
    firstName : Str,
    lastName : Str,
    age : U32,
}

person = { firstName: "Alice", lastName: "Smith", age: 30 }
olderPerson = { person & age: 31 }
```

**Why this translation:**
- F# uses `with` keyword; Roc uses `&` operator
- Both create new records (copy-on-write)
- F# uses PascalCase by convention; Roc uses camelCase

### Pattern 6: Pipeline Composition

**F#:**
```fsharp
let processUser =
    fetchUser
    >> validateUser
    >> saveUser

// Or with pipe
let result =
    userId
    |> fetchUser
    |> validateUser
    |> saveUser
```

**Roc:**
```roc
# Roc doesn't have >> composition operator
# Use pipeline instead
result =
    userId
    |> fetchUser
    |> validateUser
    |> saveUser
```

**Why this translation:**
- F# has both `>>` (forward composition) and `|>` (pipeline)
- Roc only has `|>` (pipeline) - prefer this style
- Same left-to-right data flow

---

## Error Handling

### F# Exception Model → Roc Result Model

F# supports both exceptions and `Result<'a,'e>`. Roc only has `Result`.

**F#:**
```fsharp
// Style 1: Exceptions
let divide x y =
    if y = 0 then
        raise (DivideByZeroException())
    else
        x / y

try
    let result = divide 10 0
    printfn $"Result: {result}"
with
| :? DivideByZeroException -> printfn "Cannot divide by zero"

// Style 2: Result (preferred for F# interop)
let safeDivide x y =
    if y = 0 then
        Error "Division by zero"
    else
        Ok (x / y)
```

**Roc:**
```roc
# Only Result style - no exceptions
divide : I64, I64 -> Result I64 [DivByZero]
divide = \x, y ->
    if y == 0 then
        Err(DivByZero)
    else
        Ok(x // y)

# Handling
when divide(10, 0) is
    Ok(result) -> Stdout.line!("Result: \(Num.toStr(result))")
    Err(DivByZero) -> Stdout.line!("Cannot divide by zero")
```

**Migration strategy:**
1. Convert all F# exceptions to Roc `Result` types
2. Convert F# `try/with` to Roc `when ... is` pattern matching
3. Use `!` (try operator) for error propagation instead of exception bubbling

### Multiple Error Types

**F#:**
```fsharp
type ValidationError =
    | EmptyName
    | InvalidAge
    | InvalidEmail

let validatePerson name age email =
    if String.IsNullOrWhiteSpace(name) then
        Error EmptyName
    elif age < 0 || age > 120 then
        Error InvalidAge
    elif not (email.Contains("@")) then
        Error InvalidEmail
    else
        Ok { Name = name; Age = age; Email = email }
```

**Roc:**
```roc
ValidationError : [EmptyName, InvalidAge, InvalidEmail]

validatePerson : Str, I64, Str -> Result Person ValidationError
validatePerson = \name, age, email ->
    if Str.isEmpty(name) then
        Err(EmptyName)
    else if age < 0 || age > 120 then
        Err(InvalidAge)
    else if !(Str.contains(email, "@")) then
        Err(InvalidEmail)
    else
        Ok({ name, age, email })
```

**Why this translation:**
- Both use discriminated unions/tag unions for error types
- Both use `Result` for success/failure
- Both have exhaustive pattern matching

---

## Async and Effects

### F# Async → Roc Task

This is a significant paradigm shift. F# `Async` runs on the .NET runtime; Roc `Task` is platform-provided.

**F#:**
```fsharp
let fetchData url = async {
    let! response = httpClient.GetStringAsync(url) |> Async.AwaitTask
    return response
}

let processMultiple urls = async {
    let! results =
        urls
        |> List.map fetchData
        |> Async.Parallel
    return Array.toList results
}

// Run the async
let result = processMultiple urls |> Async.RunSynchronously
```

**Roc:**
```roc
# Platform provides Task and Http
import pf.Http
import pf.Task exposing [Task]

fetchData : Str -> Task Str [HttpErr]
fetchData = \url ->
    Http.get!(url)  # Platform handles async

processMultiple : List Str -> Task (List Str) [HttpErr]
processMultiple = \urls ->
    # Platform may parallelize this
    urls
    |> List.map(fetchData)
    |> Task.sequence  # Platform-provided

# main is already a Task - no explicit run
main : Task {} []
main =
    results = processMultiple!(urls)
    Stdout.line!("Done")
```

**Why this translation:**
- F# `Async<'a>` → Roc `Task a err` (platform-provided)
- F# `let!` → Roc `!` suffix (try operator)
- F# `Async.Parallel` → Roc `Task.sequence` (platform decides parallelism)
- F# needs `Async.RunSynchronously`; Roc `main` is already a Task

### Pure vs Effectful Code

**F#:**
```fsharp
// Pure computation
let add x y = x + y

// Effectful computation (can do I/O anywhere)
let greet name =
    printfn $"Hello, {name}!"
    name
```

**Roc:**
```roc
# Pure computation
add : I64, I64 -> I64
add = \x, y -> x + y

# Effectful computation (must return Task)
greet : Str -> Task Str []
greet = \name ->
    Stdout.line!("Hello, \(name)!")
    Task.ok(name)  # Return pure value in Task
```

**Migration strategy:**
1. Identify all F# code that does I/O
2. Restructure to separate pure logic from effects
3. Move effects to platform Task boundaries
4. Keep business logic pure

---

## Platform Architecture

### .NET Application → Roc Application + Platform

**F# (.NET Console App):**
```fsharp
[<EntryPoint>]
let main argv =
    let input = Console.ReadLine()
    let processed = processInput input
    Console.WriteLine(processed)
    0  // Return exit code
```

**Roc (Platform-based):**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.Stdin
import pf.Stdout
import pf.Task exposing [Task]

main : Task {} []
main =
    input = Stdin.line!
    processed = processInput(input)  # Pure function
    Stdout.line!(processed)

# Pure helper (no effects)
processInput : Str -> Str
processInput = \input ->
    Str.toUpper(input)
```

**Key differences:**
- F# entry point is a function that returns int (exit code)
- Roc entry point is a `Task` that the platform executes
- F# can call I/O anywhere; Roc separates pure from effectful code

---

## Common Pitfalls

1. **Assuming F# mutability works in Roc**
   - F# allows `mutable` keyword and `ref` cells
   - Roc has no mutable variables
   - **Fix:** Redesign with immutable data structures

2. **Trying to use F# exceptions**
   - F# has `raise`, `try/with`, exception types
   - Roc only has `Result` type
   - **Fix:** Convert all exceptions to `Result` with typed errors

3. **Expecting .NET BCL libraries**
   - F# has access to entire .NET Base Class Library
   - Roc only has what the platform provides
   - **Fix:** Check platform docs for available APIs

4. **Using F# computation expressions freely**
   - F# has `async { }`, `result { }`, `seq { }`, etc.
   - Roc only has pattern matching and `!` operator
   - **Fix:** Use `when ... is` and `!` for control flow

5. **Assuming type providers exist**
   - F# type providers generate types at compile time
   - Roc has no metaprogramming
   - **Fix:** Use external code generation tools

6. **Forgetting platform/application split**
   - F# code is all in the same runtime
   - Roc strictly separates pure (app) from effects (platform)
   - **Fix:** Keep business logic pure, push effects to boundaries

7. **Using F# units of measure**
   - F# has `[<Measure>]` attribute for type-safe calculations
   - Roc has no built-in units
   - **Fix:** Use opaque types with smart constructors for validation

8. **Expecting REPL-driven development**
   - F# has F# Interactive (FSI) for REPL workflows
   - Roc supports `roc repl` but it's more limited
   - **Fix:** Use `expect` for inline tests instead

---

## Module System

### F# Modules/Namespaces → Roc Interfaces

**F#:**
```fsharp
// UserModule.fs
namespace MyApp

module User =
    type User = {
        Id: int
        Name: string
        Email: string
    }

    let create name email = {
        Id = generateId()
        Name = name
        Email = email
    }

    let getName user = user.Name
```

**Roc:**
```roc
# User.roc
interface User
    exposes [User, create, getName]
    imports []

User : {
    id : I64,
    name : Str,
    email : Str,
}

create : Str, Str -> User
create = \name, email -> {
    id: generateId(),
    name,
    email,
}

getName : User -> Str
getName = \user -> user.name
```

**Migration notes:**
- F# namespaces → Not needed in Roc (file-based modules)
- F# modules → Roc interfaces
- F# `exposes` is explicit in Roc, implicit in F#

---

## Build System

### .NET Project → Roc Application

**F# (.fsproj):**
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <Compile Include="Types.fs" />
    <Compile Include="Logic.fs" />
    <Compile Include="Program.fs" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="FSharp.Data" Version="6.3.0" />
  </ItemGroup>
</Project>
```

**Roc:**
```roc
# main.roc - single file or multiple interfaces
app [main] {
    pf: platform "https://..."
}

import Types
import Logic

main : Task {} []
main =
    Logic.run
```

**Build commands:**
```bash
# F#
dotnet build
dotnet run

# Roc
roc build main.roc
roc run main.roc
```

**Key differences:**
- F# needs .fsproj and explicit file ordering
- Roc infers dependencies from imports
- F# uses NuGet for packages; Roc uses platform URLs

---

## Testing

### F# Testing → Roc Expect

**F# (Expecto):**
```fsharp
module Tests

open Expecto

[<Tests>]
let tests =
    testList "Math tests" [
        testCase "addition" <| fun () ->
            Expect.equal (2 + 2) 4 "2 + 2 = 4"

        testCase "division by zero" <| fun () ->
            let result = divide 10 0
            Expect.equal result (Error "Division by zero") "should error"
    ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args tests
```

**Roc:**
```roc
# Inline tests with expect
add : I64, I64 -> I64
add = \x, y -> x + y

expect add(2, 2) == 4

divide : I64, I64 -> Result I64 [DivByZero]
divide = \x, y ->
    if y == 0 then
        Err(DivByZero)
    else
        Ok(x // y)

expect divide(10, 0) == Err(DivByZero)
expect divide(10, 2) == Ok(5)
```

**Run tests:**
```bash
# F#
dotnet test

# Roc
roc test main.roc
```

**Migration strategy:**
- Convert Expecto/xUnit/NUnit tests to Roc `expect` statements
- Place expects near the functions they test
- Run with `roc test`

---

## Limitations

### Coverage Gaps

| Pillar | F# Skill | Roc Skill | Mitigation |
|--------|--------------|--------------|------------|
| Module | ✓ | ✓ | Both well-documented |
| Error | ✓ (Result + exceptions) | ✓ (Result only) | See Error Handling section |
| Concurrency | ~ (Async covered) | ✓ | See Async and Effects section |
| Metaprogramming | ~ (Type providers) | ✓ (minimalist) | External code generation |
| Zero/Default | ✓ (implicit) | ~ (via pattern matching) | Use tag unions for nullable |
| Serialization | ✓ | ~ (via abilities) | See patterns-serialization-dev |
| Build | ✓ | ~ (emerging) | Roc build system is simpler |
| Testing | ✓ | ✓ | Both covered adequately |

**Combined Score:** 14/16 (Good)

**Known Limitations:**

1. **Metaprogramming:** F# type providers have no Roc equivalent; use external codegen
2. **Serialization:** F# has rich JSON/XML libraries; Roc relies on platform Encode/Decode abilities
3. **Concurrency:** F# Async is mature; Roc Task model is platform-dependent

### External Resources Used

| Resource | What It Provided | Reliability |
|----------|------------------|-------------|
| F# for Fun and Profit | Idiom examples | High |
| Roc Tutorial | Platform model guidance | High |
| lang-fsharp-dev | Type system details | High |
| lang-roc-dev | Task and platform patterns | High |

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| `roc` CLI | Build, run, test, format | Equivalent to `dotnet` CLI |
| Roc LSP | Editor support | VS Code, vim, etc. |
| `roc format` | Code formatting | Like `fantomas` for F# |
| `roc test` | Run inline expects | Like `dotnet test` |
| External codegen | Type generation | Replaces F# type providers |

---

## Examples

### Example 1: Simple - Option Handling

**Before (F#):**
```fsharp
type User = { Id: int; Name: string; Email: string }

let users = [
    { Id = 1; Name = "Alice"; Email = "alice@example.com" }
    { Id = 2; Name = "Bob"; Email = "bob@example.com" }
]

let findUserById id =
    users |> List.tryFind (fun u -> u.Id = id)

let getUserName id =
    findUserById id
    |> Option.map (fun u -> u.Name)
    |> Option.defaultValue "Unknown"
```

**After (Roc):**
```roc
User : { id : I64, name : Str, email : Str }

users = [
    { id: 1, name: "Alice", email: "alice@example.com" },
    { id: 2, name: "Bob", email: "bob@example.com" },
]

findUserById : I64 -> [Some User, None]
findUserById = \id ->
    when List.findFirst(users, \u -> u.id == id) is
        Ok(user) -> Some(user)
        Err(_) -> None

getUserName : I64 -> Str
getUserName = \id ->
    when findUserById(id) is
        Some(u) -> u.name
        None -> "Unknown"
```

### Example 2: Medium - Result Error Handling

**Before (F#):**
```fsharp
type ValidationError =
    | InvalidName
    | InvalidAge

type Person = { Name: string; Age: int }

let validateName name =
    if String.IsNullOrWhiteSpace(name) then
        Error InvalidName
    else
        Ok name

let validateAge age =
    if age < 0 || age > 120 then
        Error InvalidAge
    else
        Ok age

let createPerson name age =
    result {
        let! validName = validateName name
        let! validAge = validateAge age
        return { Name = validName; Age = validAge }
    }
```

**After (Roc):**
```roc
ValidationError : [InvalidName, InvalidAge]

Person : { name : Str, age : I64 }

validateName : Str -> Result Str [InvalidName]
validateName = \name ->
    if Str.isEmpty(name) then
        Err(InvalidName)
    else
        Ok(name)

validateAge : I64 -> Result I64 [InvalidAge]
validateAge = \age ->
    if age < 0 || age > 120 then
        Err(InvalidAge)
    else
        Ok(age)

createPerson : Str, I64 -> Result Person [InvalidName, InvalidAge]
createPerson = \name, age ->
    validName = validateName!(name)
    validAge = validateAge!(age)
    Ok({ name: validName, age: validAge })
```

### Example 3: Complex - Async File Processing

**Before (F#):**
```fsharp
open System.IO

type ProcessingError =
    | FileNotFound of string
    | InvalidFormat of string

let readFile path = async {
    try
        let! content = File.ReadAllTextAsync(path) |> Async.AwaitTask
        return Ok content
    with
    | :? FileNotFoundException ->
        return Error (FileNotFound path)
}

let processContent content =
    if content.Contains("error") then
        Error (InvalidFormat "Content contains error")
    else
        Ok (content.ToUpper())

let writeFile path content = async {
    do! File.WriteAllTextAsync(path, content) |> Async.AwaitTask
    return Ok ()
}

let processFile inputPath outputPath = async {
    let! contentResult = readFile inputPath
    match contentResult with
    | Error e -> return Error e
    | Ok content ->
        match processContent content with
        | Error e -> return Error e
        | Ok processed ->
            return! writeFile outputPath processed
}

// Usage
let result =
    processFile "input.txt" "output.txt"
    |> Async.RunSynchronously
```

**After (Roc):**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.File
import pf.Path
import pf.Task exposing [Task]
import pf.Stdout

ProcessingError : [FileNotFound Str, InvalidFormat Str]

readFile : Str -> Task Str [FileReadErr Path.ReadErr]*
readFile = \path ->
    File.readUtf8(Path.fromStr(path))

processContent : Str -> Result Str [InvalidFormat Str]
processContent = \content ->
    if Str.contains(content, "error") then
        Err(InvalidFormat("Content contains error"))
    else
        Ok(Str.toUpper(content))

writeFile : Str, Str -> Task {} [FileWriteErr Path.WriteErr]*
writeFile = \path, content ->
    File.writeUtf8(Path.fromStr(path), content)

processFile : Str, Str -> Task {} [FileReadErr Path.ReadErr, InvalidFormat Str, FileWriteErr Path.WriteErr]*
processFile = \inputPath, outputPath ->
    # Read file (returns Task)
    content = readFile!(inputPath)

    # Process content (pure function, returns Result)
    processed = processContent!(content)

    # Write file (returns Task)
    writeFile!(outputPath, processed)

main : Task {} []
main =
    when processFile("input.txt", "output.txt") is
        Ok({}) -> Stdout.line!("File processed successfully")
        Err(FileReadErr(_)) -> Stdout.line!("Error reading file")
        Err(InvalidFormat(msg)) -> Stdout.line!("Invalid format: \(msg)")
        Err(FileWriteErr(_)) -> Stdout.line!("Error writing file")
```

**Key conversions:**
- F# `Async<'a>` → Roc `Task a err` (platform-provided)
- F# `try/with` → Roc Result type with pattern matching
- F# computation expression → Roc `!` try operator
- F# can mix pure/async; Roc separates Task boundaries

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-elm-clojure` - Another functional language pair conversion (similar paradigm shifts)
- `lang-fsharp-dev` - F# development patterns
- `lang-roc-dev` - Roc development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async workflows, Task model across languages
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Type providers vs code generation
