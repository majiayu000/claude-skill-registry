---
name: convert-roc-fsharp
description: Convert Roc code to idiomatic F#. Use when migrating Roc projects to F#, translating Roc patterns to idiomatic F#, or refactoring Roc codebases. Extends meta-convert-dev with Roc-to-F# specific patterns.
---

# Convert Roc to F#

Convert Roc code to idiomatic F#. This skill extends `meta-convert-dev` with Roc-to-F# specific type mappings, idiom translations, and architectural guidance.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Roc types → F# types
- **Idiom translations**: Roc patterns → idiomatic F#
- **Error handling**: Roc Result/tag unions → F# Result/Option
- **Platform shift**: Roc platform model → .NET runtime
- **Paradigm alignment**: Both functional-first, but different architectures

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Roc language fundamentals - see `lang-roc-dev`
- F# language fundamentals - see `lang-fsharp-dev`
- Reverse conversion (F# → Roc) - see `convert-fsharp-roc`

---

## Quick Reference

| Roc | F# | Notes |
|----------|----------|-------|
| `Str` | `string` | Immutable strings |
| `I64` | `int64` | 64-bit signed integer |
| `I32` | `int` | F# default int is 32-bit |
| `F64` | `float` or `double` | 64-bit floating point |
| `Bool` | `bool` | Boolean values |
| `List a` | `'a list` | Immutable lists |
| `Dict k v` | `Map<'k,'v>` | Immutable dictionaries |
| `Set a` | `Set<'a>` | Immutable sets |
| `[Some a, None]` | `Option<'a>` | Optional values |
| `Result a e` | `Result<'a,'e>` | Error handling |
| `{ ... }` record | `{| ... |}` or `type X = { ... }` | Structural vs nominal |
| `[...]` tag union | `type X = ...` discriminated union | Sum types |
| `Task a err` | `Async<'a>` or `Task<'a>` | Async/effects |
| `{}` | `unit` | Empty value |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Preserve semantics** over syntax similarity
4. **Adopt F# idioms** - leverage .NET ecosystem
5. **Handle edge cases** - error paths, effects, resource management
6. **Test equivalence** - same inputs → same outputs

---

## Paradigm Translation

### Mental Model Shift: Platform Model → .NET Runtime

Both Roc and F# are functional-first languages, but they differ fundamentally in how they handle effects:

| Roc Concept | F# Approach | Key Insight |
|------------------|-------------------|-------------|
| Platform provides runtime | .NET CLR runtime | Runtime is part of the application |
| `Task ok err` via platform | `Async<'a>` workflows | Effects integrated into language |
| Platform-provided I/O | Direct I/O (Console, File) | Can do I/O anywhere |
| Application remains pure | Can mix pure and impure | Flexibility over purity |
| No runtime exceptions | Exception handling | Exceptions are first-class |
| No compile-time metaprogramming | Type providers | Rich compile-time features |

### Architecture Mental Model

```
Roc (Platform Model)              F# (.NET)
┌─────────────────────┐           ┌─────────────────────┐
│   Your Roc Code     │           │   Your F# Code      │
│   (pure only)       │           │  (can do I/O)       │
│   ↓                 │           │  ↓                  │
│   Platform API      │           │   .NET BCL          │
│   ↓                 │           │   ↓                 │
│   Platform Host     │           │   CLR Runtime       │
└─────────────────────┘           └─────────────────────┘
    Clear separation                   Everything in
    between pure & effects              same runtime
```

**Key shift:** In Roc, I/O goes through the platform's `Task` type. In F#, you can call `Console.WriteLine` or perform I/O anywhere.

---

## Type System Mapping

### Primitive Types

| Roc | F# | Notes |
|----------|----------|-------|
| `Str` | `string` | Both immutable UTF-8 |
| `I8` | `sbyte` | 8-bit signed |
| `I16` | `int16` | 16-bit signed |
| `I32` | `int` | F# default int is 32-bit |
| `I64` | `int64` or `long` | 64-bit signed |
| `I128` | `System.Numerics.BigInteger` | No native 128-bit int |
| `U8` | `byte` | 8-bit unsigned |
| `U16` | `uint16` | 16-bit unsigned |
| `U32` | `uint32` | 32-bit unsigned |
| `U64` | `uint64` or `ulong` | 64-bit unsigned |
| `U128` | `System.Numerics.BigInteger` | No native 128-bit uint |
| `F32` | `float32` or `single` | 32-bit floating point |
| `F64` | `float` or `double` | 64-bit floating point (F# default) |
| `Bool` | `bool` | Direct mapping |
| `{}` | `unit` | Empty value |

### Collection Types

| Roc | F# | Notes |
|----------|----------|-------|
| `List a` | `'a list` | Both immutable, structural sharing |
| `Dict k v` | `Map<'k,'v>` | Immutable dictionaries |
| `Set a` | `Set<'a>` | Immutable sets |
| `(a, b)` | `'a * 'b` | Tuples map directly |
| `(a, b, c)` | `'a * 'b * 'c` | Multiple element tuples |

### Composite Types

| Roc | F# | Notes |
|----------|----------|-------|
| `{ ... }` record | `{| ... |}` anonymous record | Structural typing |
| `{ ... }` record | `type X = { ... }` record | Nominal typing (preferred) |
| `[A, B, C]` tag union | `type X = A \| B \| C` DU | Direct correspondence |
| `[A I64, B Str]` tag with payload | `type X = A of int64 \| B of string` | Payload mapping |
| `[Some a, None]` | `Option<'a>` | Built-in option type |
| `Result ok err` | `Result<'ok,'err>` | Built-in result type |

### Roc Specific Types → F#

| Roc Type | F# Strategy | Notes |
|----------|----------|-------|
| `Task a err` | `Async<'a>` or `Task<'a>` | Platform effects → runtime async |
| Opaque types | Single-case DU | `type Email = Email of string` |
| Tag unions (open) | Extensible DU (rare) | Use closed DU instead |
| Abilities constraints | Interface constraints | `'a when 'a :> IEquatable<'a>` |

---

## Idiom Translation

### Pattern 1: Tag Unions to Discriminated Unions

**Roc:**
```roc
Color : [Red, Green, Blue, Custom(U8, U8, U8)]

describe : Color -> Str
describe = \color ->
    when color is
        Red -> "red"
        Green -> "green"
        Blue -> "blue"
        Custom(r, g, b) -> "rgb(\(Num.toStr(r)), \(Num.toStr(g)), \(Num.toStr(b)))"
```

**F#:**
```fsharp
type Color =
    | Red
    | Green
    | Blue
    | Custom of r: byte * g: byte * b: byte

let describe color =
    match color with
    | Red -> "red"
    | Green -> "green"
    | Blue -> "blue"
    | Custom (r, g, b) -> $"rgb({r}, {g}, {b})"
```

**Why this translation:**
- Roc tag unions → F# discriminated unions (nearly identical)
- Roc `when` → F# `match` (same exhaustiveness checking)
- Roc interpolation `\(x)` → F# interpolation `$"{x}"` or `{x}`
- Both enforce exhaustive pattern matching

### Pattern 2: Optional Values

**Roc:**
```roc
findUser : I64 -> [Some User, None]
findUser = \id ->
    List.findFirst(users, \u -> u.id == id)
    |> Result.toOption

userName =
    when findUser(1) is
        Some(u) -> u.name
        None -> "Unknown"
```

**F#:**
```fsharp
let findUser id =
    users |> List.tryFind (fun u -> u.Id = id)

let userName =
    match findUser 1 with
    | Some u -> u.Name
    | None -> "Unknown"
```

**Why this translation:**
- Roc `[Some a, None]` → F# `Option<'a>` (built-in type)
- Roc pattern matching → F# pattern matching (direct mapping)
- F# has `Option.map`, `Option.bind` helpers not shown in Roc example
- Both achieve same null-safety

### Pattern 3: Result Error Handling

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
    x = divide!(a, b)
    y = divide!(x, c)
    Ok(y)
```

**F#:**
```fsharp
type DivisionError = DivByZero

let divide x y =
    if y = 0 then
        Error DivByZero
    else
        Ok (x / y)

let calculate a b c =
    result {
        let! x = divide a b
        let! y = divide x c
        return y
    }
```

**Why this translation:**
- Roc `Result ok err` → F# `Result<'ok,'err>` (built-in)
- Roc `!` try operator → F# `let!` in computation expression
- Roc tag errors `[DivByZero]` → F# DU `type DivisionError = DivByZero`
- F# computation expressions provide cleaner syntax than nested matches

### Pattern 4: List Operations

**Roc:**
```roc
result =
    items
    |> List.keepIf(\x -> x.active)
    |> List.map(\x -> x.value)
    |> List.walk(0, Num.add)
```

**F#:**
```fsharp
let result =
    items
    |> List.filter (fun x -> x.Active)
    |> List.map (fun x -> x.Value)
    |> List.sum
```

**Why this translation:**
- Roc `keepIf` → F# `filter` (different naming)
- Roc `walk(0, Num.add)` → F# `sum` (built-in helper)
- Both use pipeline operator idiomatically
- F# has more list helpers (`sum`, `average`, etc.)

### Pattern 5: Record Updates

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

**Why this translation:**
- Roc `&` operator → F# `with` keyword (copy-and-update)
- Roc uses camelCase → F# uses PascalCase (convention)
- Both create new records (immutable)
- F# uses semicolons `;` for field separators, Roc uses commas

### Pattern 6: Pipeline Operator

**Roc:**
```roc
result =
    userId
    |> fetchUser
    |> validateUser
    |> saveUser
```

**F#:**
```fsharp
// Same pipeline style
let result =
    userId
    |> fetchUser
    |> validateUser
    |> saveUser

// Or with composition
let processUser =
    fetchUser
    >> validateUser
    >> saveUser

let result = processUser userId
```

**Why this translation:**
- Both use `|>` for pipeline (identical)
- F# also has `>>` composition operator (Roc doesn't)
- Same left-to-right data flow
- F# provides more composition options

---

## Error Handling

### Roc Result Model → F# Result/Exception Model

Roc only has `Result`. F# supports both `Result<'a,'e>` and exceptions.

**Roc:**
```roc
divide : I64, I64 -> Result I64 [DivByZero]
divide = \x, y ->
    if y == 0 then
        Err(DivByZero)
    else
        Ok(x // y)

when divide(10, 0) is
    Ok(result) -> Stdout.line!("Result: \(Num.toStr(result))")
    Err(DivByZero) -> Stdout.line!("Cannot divide by zero")
```

**F# (Result style - preferred):**
```fsharp
type DivisionError = DivByZero

let divide x y =
    if y = 0 then
        Error DivByZero
    else
        Ok (x / y)

match divide 10 0 with
| Ok result -> printfn $"Result: {result}"
| Error DivByZero -> printfn "Cannot divide by zero"
```

**F# (Exception style - for interop):**
```fsharp
let divide x y =
    if y = 0 then
        raise (System.DivideByZeroException())
    else
        x / y

try
    let result = divide 10 0
    printfn $"Result: {result}"
with
| :? System.DivideByZeroException -> printfn "Cannot divide by zero"
```

**Migration strategy:**
1. Prefer F# `Result` type for functional code (matches Roc semantics)
2. Use exceptions when integrating with .NET libraries
3. Convert Roc `when ... is` to F# `match ... with`
4. Tag unions become discriminated unions

### Multiple Error Types

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

**F#:**
```fsharp
type ValidationError =
    | EmptyName
    | InvalidAge
    | InvalidEmail

type Person = {
    Name: string
    Age: int
    Email: string
}

let validatePerson name age email =
    if System.String.IsNullOrWhiteSpace(name) then
        Error EmptyName
    elif age < 0 || age > 120 then
        Error InvalidAge
    elif not (email.Contains("@")) then
        Error InvalidEmail
    else
        Ok { Name = name; Age = age; Email = email }
```

**Why this translation:**
- Roc tag unions → F# discriminated unions (direct mapping)
- Roc `if/else if` → F# `if/elif` (same control flow)
- Both use `Result` with typed errors
- Both have exhaustive pattern matching

---

## Async and Effects

### Roc Task → F# Async

This is a significant paradigm shift. Roc `Task` is platform-provided; F# `Async` is built into the language.

**Roc:**
```roc
import pf.Http
import pf.Task exposing [Task]

fetchData : Str -> Task Str [HttpErr]
fetchData = \url ->
    Http.get!(url)

processMultiple : List Str -> Task (List Str) [HttpErr]
processMultiple = \urls ->
    urls
    |> List.map(fetchData)
    |> Task.sequence

main : Task {} []
main =
    results = processMultiple!(urls)
    Stdout.line!("Done")
```

**F#:**
```fsharp
open System.Net.Http

type HttpError = HttpErr of string

let httpClient = new HttpClient()

let fetchData url = async {
    try
        let! response = httpClient.GetStringAsync(url) |> Async.AwaitTask
        return Ok response
    with
    | ex -> return Error (HttpErr ex.Message)
}

let processMultiple urls = async {
    let! results =
        urls
        |> List.map fetchData
        |> Async.Parallel
    return Array.toList results |> List.choose id  // Extract Ok values
}

[<EntryPoint>]
let main argv =
    let urls = ["url1"; "url2"; "url3"]
    processMultiple urls
    |> Async.RunSynchronously
    |> ignore
    printfn "Done"
    0
```

**Why this translation:**
- Roc `Task a err` → F# `Async<Result<'a, 'err>>` (effects + errors)
- Roc `!` operator → F# `let!` in `async { }` block
- Roc platform handles execution → F# needs `Async.RunSynchronously`
- Roc `main` is a Task → F# `main` returns int (exit code)

### Pure vs Effectful Code

**Roc:**
```roc
# Pure computation
add : I64, I64 -> I64
add = \x, y -> x + y

# Effectful computation (must return Task)
greet : Str -> Task Str []
greet = \name ->
    Stdout.line!("Hello, \(name)!")
    Task.ok(name)
```

**F#:**
```fsharp
// Pure computation
let add x y = x + y

// Effectful computation (no special type required)
let greet name =
    printfn $"Hello, {name}!"
    name  // Can return pure value directly

// Or as Async if needed
let greetAsync name = async {
    printfn $"Hello, {name}!"
    return name
}
```

**Migration strategy:**
1. Roc `Task` functions → F# `Async` or direct I/O (depends on context)
2. Roc pure functions → F# pure functions (direct mapping)
3. Roc `!` try operator → F# `let!` or `do!`
4. Separate pure logic from effects for clarity

---

## Platform Architecture

### Roc Application + Platform → .NET Application

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
    processed = processInput(input)
    Stdout.line!(processed)

processInput : Str -> Str
processInput = \input ->
    Str.toUpper(input)
```

**F# (.NET Console App):**
```fsharp
[<EntryPoint>]
let main argv =
    let input = System.Console.ReadLine()
    let processed = processInput input
    System.Console.WriteLine(processed)
    0  // Return exit code

let processInput input =
    input.ToUpper()
```

**Key differences:**
- Roc entry point is a `Task` that platform executes
- F# entry point is a function that returns int (exit code)
- Roc separates pure from effectful code; F# can mix them
- Roc uses platform imports; F# uses .NET BCL directly

---

## Common Pitfalls

1. **Forgetting F# allows mutability**
   - Roc has no mutable variables
   - F# allows `mutable` keyword and `ref` cells
   - **Benefit:** Can use mutable state when performance-critical

2. **Not leveraging F# exceptions**
   - Roc only has `Result` type
   - F# has both `Result` and exceptions
   - **Strategy:** Use `Result` for domain errors, exceptions for unexpected failures

3. **Missing .NET BCL libraries**
   - Roc only has what the platform provides
   - F# has access to entire .NET ecosystem
   - **Benefit:** Rich library support (LINQ, JSON.NET, Entity Framework, etc.)

4. **Not using F# computation expressions**
   - Roc uses pattern matching and `!` operator
   - F# has `async { }`, `result { }`, `seq { }`, etc.
   - **Strategy:** Use computation expressions for cleaner code

5. **Ignoring F# type providers**
   - Roc has no metaprogramming
   - F# has type providers for compile-time code generation
   - **Benefit:** Can generate types from SQL, JSON, CSV at compile time

6. **Assuming strict platform/application split**
   - Roc strictly separates pure (app) from effects (platform)
   - F# mixes pure and impure code freely
   - **Strategy:** Maintain separation for clarity, but leverage flexibility

7. **Not using F# units of measure**
   - Roc has no built-in units
   - F# has `[<Measure>]` for type-safe calculations
   - **Benefit:** Compile-time dimension checking

8. **Missing F# Interactive (REPL)**
   - Roc has limited REPL support
   - F# has FSI for interactive development
   - **Benefit:** Rapid prototyping and exploration

---

## Module System

### Roc Interfaces → F# Modules/Namespaces

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

**F#:**
```fsharp
// User.fs
namespace MyApp

module User =
    type User = {
        Id: int64
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

**Migration notes:**
- Roc interfaces → F# modules or namespaces
- Roc `exposes` is explicit → F# exports everything by default
- Roc file-based modules → F# file order matters in .fsproj

---

## Build System

### Roc Application → .NET Project

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
roc build main.roc
roc run main.roc
```

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

**Build commands:**
```bash
dotnet build
dotnet run
```

**Key differences:**
- Roc infers dependencies from imports
- F# needs .fsproj and explicit file ordering
- Roc uses platform URLs; F# uses NuGet packages
- F# has richer build tooling (watch mode, publish, etc.)

---

## Testing

### Roc Expect → F# Testing Frameworks

**Roc:**
```roc
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
roc test main.roc
```

**F# (Expecto):**
```fsharp
module Tests

open Expecto

let add x y = x + y

[<Tests>]
let tests =
    testList "Math tests" [
        testCase "addition" <| fun () ->
            Expect.equal (add 2 2) 4 "2 + 2 = 4"

        testCase "division by zero" <| fun () ->
            let result = divide 10L 0L
            Expect.equal result (Error DivByZero) "should error"

        testCase "division success" <| fun () ->
            let result = divide 10L 2L
            Expect.equal result (Ok 5L) "10 / 2 = 5"
    ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args tests
```

**Run tests:**
```bash
dotnet test
```

**Migration strategy:**
- Convert Roc `expect` statements to test framework assertions
- Group related expects into test lists
- F# has richer testing tools (Expecto, xUnit, FsUnit, FsCheck)

---

## Examples

### Example 1: Simple - Record and Pattern Matching

**Before (Roc):**
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

**After (F#):**
```fsharp
type User = {
    Id: int64
    Name: string
    Email: string
}

let users = [
    { Id = 1L; Name = "Alice"; Email = "alice@example.com" }
    { Id = 2L; Name = "Bob"; Email = "bob@example.com" }
]

let findUserById id =
    users |> List.tryFind (fun u -> u.Id = id)

let getUserName id =
    match findUserById id with
    | Some u -> u.Name
    | None -> "Unknown"
```

### Example 2: Medium - Result with Multiple Errors

**Before (Roc):**
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

**After (F#):**
```fsharp
type ValidationError =
    | InvalidName
    | InvalidAge

type Person = {
    Name: string
    Age: int
}

let validateName name =
    if System.String.IsNullOrWhiteSpace(name) then
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

### Example 3: Complex - Task-based File Processing

**Before (Roc):**
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
    content = readFile!(inputPath)
    processed = processContent!(content)
    writeFile!(outputPath, processed)

main : Task {} []
main =
    when processFile("input.txt", "output.txt") is
        Ok({}) -> Stdout.line!("File processed successfully")
        Err(FileReadErr(_)) -> Stdout.line!("Error reading file")
        Err(InvalidFormat(msg)) -> Stdout.line!("Invalid format: \(msg)")
        Err(FileWriteErr(_)) -> Stdout.line!("Error writing file")
```

**After (F#):**
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
    | ex ->
        return Error (FileNotFound $"Error: {ex.Message}")
}

let processContent content =
    if content.Contains("error") then
        Error (InvalidFormat "Content contains error")
    else
        Ok (content.ToUpper())

let writeFile path content = async {
    try
        do! File.WriteAllTextAsync(path, content) |> Async.AwaitTask
        return Ok ()
    with
    | ex ->
        return Error (FileNotFound $"Write error: {ex.Message}")
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

[<EntryPoint>]
let main argv =
    let result =
        processFile "input.txt" "output.txt"
        |> Async.RunSynchronously

    match result with
    | Ok () -> printfn "File processed successfully"
    | Error (FileNotFound msg) -> printfn $"File error: {msg}"
    | Error (InvalidFormat msg) -> printfn $"Invalid format: {msg}"

    0
```

**Key conversions:**
- Roc `Task a err` → F# `Async<Result<'a, 'err>>`
- Roc platform I/O → F# direct file I/O with .NET APIs
- Roc `!` operator → F# `let!` in async blocks
- Roc `main` returns Task → F# `main` returns int

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-fsharp-roc` - Reverse conversion (F# → Roc)
- `lang-roc-dev` - Roc development patterns
- `lang-fsharp-dev` - F# development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Task model vs Async workflows
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - No metaprogramming vs type providers
