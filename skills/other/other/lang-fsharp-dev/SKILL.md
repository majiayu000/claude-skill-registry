---
name: lang-fsharp-dev
description: Foundational F# patterns covering functional-first programming, type providers, computation expressions, and domain modeling. Use when writing F# code, understanding functional patterns, working with type providers, or building .NET applications with F#. This is the entry point for F# development.
---

# F# Fundamentals

Foundational F# patterns and core language features. This skill serves as both a reference for common patterns and guidance for functional-first .NET development.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      F# Skill Hierarchy                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌───────────────────┐                        │
│                    │  lang-fsharp-dev  │ ◄── You are here       │
│                    │   (foundation)    │                        │
│                    └─────────┬─────────┘                        │
│                              │                                  │
│     ┌────────────┬───────────┼───────────┬────────────┐        │
│     │            │           │           │            │        │
│     ▼            ▼           ▼           ▼            ▼        │
│ ┌────────┐ ┌──────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐   │
│ │ type   │ │ domain   │ │ async  │ │ testing │ │ web-api  │   │
│ │providers│ │ modeling │ │ -dev   │ │  -dev   │ │   -dev   │   │
│ └────────┘ └──────────┘ └────────┘ └─────────┘ └──────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Functional-first programming patterns
- Type system (records, discriminated unions, options)
- Pattern matching and active patterns
- Computation expressions basics
- Type providers fundamentals
- Domain modeling with types
- Interop with C# and .NET

**This skill does NOT cover (see specialized skills):**
- Advanced type providers usage
- Domain-driven design patterns
- Async/Task programming deep dive
- Testing frameworks (Expecto, xUnit, FsUnit)
- Web development (Giraffe, Saturn, Falco)

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Define record | `type Person = { Name: string; Age: int }` |
| Define union | `type Result<'T,'E> = Ok of 'T \| Error of 'E` |
| Pattern match | `match value with \| Some x -> x \| None -> 0` |
| Define function | `let add x y = x + y` |
| Pipe operator | `value \|> function1 \|> function2` |
| Composition | `let f = function1 >> function2` |
| List comprehension | `[ for i in 1..10 -> i * i ]` |
| Async computation | `async { let! result = fetchData() return result }` |

---

## Core Types

### Records

```fsharp
// Basic record
type Person = {
    FirstName: string
    LastName: string
    Age: int
}

// Creating instances
let person = {
    FirstName = "John"
    LastName = "Doe"
    Age = 30
}

// Copy-and-update
let olderPerson = { person with Age = 31 }

// Pattern matching on records
let getFullName person =
    match person with
    | { FirstName = f; LastName = l } -> $"{f} {l}"

// Shorter: destructuring
let getFullName' { FirstName = f; LastName = l } = $"{f} {l}"
```

### Discriminated Unions

```fsharp
// Simple union
type PaymentMethod =
    | Cash
    | CreditCard of cardNumber: string
    | DebitCard of cardNumber: string * pin: int

// Using unions
let processPayment method =
    match method with
    | Cash -> "Processing cash payment"
    | CreditCard cardNumber -> $"Processing credit card {cardNumber}"
    | DebitCard (cardNumber, _) -> $"Processing debit card {cardNumber}"

// Option type (built-in union)
type Option<'T> =
    | Some of 'T
    | None

// Result type (built-in union)
type Result<'T,'E> =
    | Ok of 'T
    | Error of 'E

// Using Option
let findPerson id =
    if id = 1 then
        Some { FirstName = "John"; LastName = "Doe"; Age = 30 }
    else
        None

// Using Result
let divide x y =
    if y = 0 then
        Error "Division by zero"
    else
        Ok (x / y)
```

### Single-Case Unions (Type Safety)

```fsharp
// Wrap primitives for type safety
type EmailAddress = EmailAddress of string
type CustomerId = CustomerId of int

let sendEmail (EmailAddress email) message =
    printfn $"Sending to {email}: {message}"

let getCustomer (CustomerId id) =
    // Can't accidentally pass wrong ID type
    printfn $"Fetching customer {id}"

// Usage prevents type confusion
let email = EmailAddress "test@example.com"
let customerId = CustomerId 123
sendEmail email "Hello"
// sendEmail customerId "Hello"  // Compile error!
```

---

## Pattern Matching

### Basic Matching

```fsharp
// Match on values
let describe x =
    match x with
    | 0 -> "zero"
    | 1 -> "one"
    | 2 -> "two"
    | n when n > 0 -> "positive"
    | _ -> "negative"

// Match on types
let processValue (value: obj) =
    match value with
    | :? string as s -> $"String: {s}"
    | :? int as i -> $"Int: {i}"
    | _ -> "Unknown type"

// Match on tuples
let point = (3, 4)
match point with
| (0, 0) -> "origin"
| (x, 0) -> $"on x-axis at {x}"
| (0, y) -> $"on y-axis at {y}"
| (x, y) -> $"at ({x}, {y})"
```

### Active Patterns

```fsharp
// Single-case active pattern
let (|Even|Odd|) n =
    if n % 2 = 0 then Even else Odd

match 42 with
| Even -> "even number"
| Odd -> "odd number"

// Partial active pattern
let (|Integer|_|) (str: string) =
    match System.Int32.TryParse(str) with
    | true, value -> Some value
    | false, _ -> None

match "123" with
| Integer n -> $"Number: {n}"
| _ -> "Not a number"

// Multi-case active pattern
let (|Small|Medium|Large|) n =
    if n < 10 then Small
    elif n < 100 then Medium
    else Large

match 42 with
| Small -> "small"
| Medium -> "medium"
| Large -> "large"
```

---

## Functions

### Function Basics

```fsharp
// Simple function
let add x y = x + y

// Type annotations (optional but recommended for public APIs)
let add' (x: int) (y: int) : int = x + y

// Anonymous function (lambda)
let doubled = List.map (fun x -> x * 2) [1; 2; 3]

// Recursive function
let rec factorial n =
    if n <= 1 then 1
    else n * factorial (n - 1)

// Tail-recursive function (optimized)
let factorial' n =
    let rec loop acc n =
        if n <= 1 then acc
        else loop (acc * n) (n - 1)
    loop 1 n
```

### Partial Application and Currying

```fsharp
// All F# functions are curried by default
let add x y = x + y
let add5 = add 5  // Partial application
add5 10  // Returns 15

// Use partial application for configurable functions
let greet greeting name = $"{greeting}, {name}!"
let sayHello = greet "Hello"
let sayHi = greet "Hi"

sayHello "Alice"  // "Hello, Alice!"
sayHi "Bob"       // "Hi, Bob!"
```

### Function Composition

```fsharp
// Forward composition (>>)
let add1 x = x + 1
let double x = x * 2
let add1ThenDouble = add1 >> double

add1ThenDouble 5  // Returns 12

// Backward composition (<<)
let doubleThenAdd1 = add1 << double
doubleThenAdd1 5  // Returns 11

// Pipe operator (|>)
let result =
    5
    |> add1
    |> double
    |> fun x -> x + 10

// Pipe backward (<|)
let sum = (+) <| 1 + 2  // Equivalent to (+) (1 + 2)
```

---

## Collections

### Lists

```fsharp
// List literals
let numbers = [1; 2; 3; 4; 5]
let moreNumbers = [1..10]
let evenNumbers = [2..2..10]

// Cons operator (::)
let newList = 0 :: numbers  // [0; 1; 2; 3; 4; 5]

// List comprehensions
let squares = [ for i in 1..10 -> i * i ]
let evens = [ for i in 1..20 do if i % 2 = 0 then yield i ]

// Common list functions
let doubled = List.map (fun x -> x * 2) numbers
let evens' = List.filter (fun x -> x % 2 = 0) numbers
let sum = List.fold (+) 0 numbers
let sum' = List.sum numbers
let product = List.reduce (*) numbers
```

### Arrays

```fsharp
// Array literals
let arr = [| 1; 2; 3; 4; 5 |]

// Array comprehension
let squares = [| for i in 1..10 -> i * i |]

// Mutable updates (in-place)
arr.[0] <- 10

// Array functions (similar to List)
let doubled = Array.map (fun x -> x * 2) arr
let evens = Array.filter (fun x -> x % 2 = 0) arr
```

### Sequences (Lazy)

```fsharp
// Infinite sequence
let naturals = Seq.initInfinite id  // 0, 1, 2, 3, ...

// Lazy evaluation
let expensiveSeq = seq {
    printfn "Computing..."
    for i in 1..5 do
        printfn $"Yielding {i}"
        yield i * i
}

// Only computed when enumerated
expensiveSeq |> Seq.take 3 |> Seq.toList
```

### Map and Set

```fsharp
// Map (immutable dictionary)
let ages = Map [ ("Alice", 30); ("Bob", 25) ]
let aliceAge = ages.["Alice"]  // 30
let aliceAge' = Map.tryFind "Alice" ages  // Some 30
let updatedAges = Map.add "Charlie" 35 ages

// Set (immutable)
let set1 = Set [1; 2; 3]
let set2 = Set [3; 4; 5]
let union = Set.union set1 set2  // {1, 2, 3, 4, 5}
let intersection = Set.intersect set1 set2  // {3}
```

---

## Computation Expressions

### Option Computation Expression

```fsharp
// Option workflow
type OptionBuilder() =
    member _.Bind(x, f) = Option.bind f x
    member _.Return(x) = Some x
    member _.ReturnFrom(x) = x

let option = OptionBuilder()

let validateAge age =
    option {
        let! validAge =
            if age >= 0 && age <= 120 then Some age
            else None
        return validAge
    }
```

### Result Computation Expression

```fsharp
// Result workflow
type ResultBuilder() =
    member _.Bind(x, f) = Result.bind f x
    member _.Return(x) = Ok x
    member _.ReturnFrom(x) = x

let result = ResultBuilder()

let divideBy x y =
    if y = 0 then Error "Division by zero"
    else Ok (x / y)

let calculate =
    result {
        let! a = divideBy 10 2   // Ok 5
        let! b = divideBy 20 4   // Ok 5
        let! c = divideBy a b    // Ok 1
        return c
    }
```

### Async Computation Expression

```fsharp
// Async workflow (built-in)
let fetchData url = async {
    printfn $"Fetching {url}..."
    do! Async.Sleep 1000
    return $"Data from {url}"
}

let processUrls urls = async {
    let! results =
        urls
        |> List.map fetchData
        |> Async.Parallel

    return results |> Array.toList
}

// Run async computation
let urls = ["url1"; "url2"; "url3"]
processUrls urls |> Async.RunSynchronously
```

---

## Type Providers

### CSV Type Provider

```fsharp
open FSharp.Data

// Type provider infers schema from sample
type StockData = CsvProvider<"stocks.csv">

let data = StockData.Load("stocks.csv")
for row in data.Rows do
    printfn $"{row.Date}: {row.Close}"
```

### JSON Type Provider

```fsharp
open FSharp.Data

// Infer from sample JSON
type Weather = JsonProvider<"""
{
    "temperature": 72,
    "condition": "sunny",
    "humidity": 65
}
""">

let weather = Weather.Load("weather.json")
printfn $"Temperature: {weather.Temperature}°F"
```

### SQL Type Provider

```fsharp
open FSharp.Data.Sql

type Sql = SqlDataProvider<
    ConnectionString = "Server=localhost;Database=mydb",
    DatabaseVendor = Common.DatabaseProviderTypes.MSSQLSERVER>

let ctx = Sql.GetDataContext()
let customers =
    query {
        for customer in ctx.Dbo.Customers do
        where (customer.Age > 18)
        select customer
    }
```

---

## Domain Modeling

### Making Illegal States Unrepresentable

```fsharp
// Bad: Can represent invalid states
type EmailContactBad = {
    EmailAddress: string option
    IsVerified: bool
}
// Problem: IsVerified can be true when EmailAddress is None

// Good: Invalid states impossible
type VerifiedEmail = VerifiedEmail of string
type UnverifiedEmail = UnverifiedEmail of string

type EmailContact =
    | Verified of VerifiedEmail
    | Unverified of UnverifiedEmail

// Can only verify an unverified email
let verify (UnverifiedEmail email) =
    // Verification logic...
    VerifiedEmail email
```

### Smart Constructors

```fsharp
// Constrained types with validation
type EmailAddress = private EmailAddress of string

module EmailAddress =
    let create (email: string) =
        if email.Contains("@") then
            Ok (EmailAddress email)
        else
            Error "Invalid email format"

    let value (EmailAddress email) = email

// Usage
match EmailAddress.create "test@example.com" with
| Ok email -> printfn $"Valid: {EmailAddress.value email}"
| Error msg -> printfn $"Error: {msg}"
```

### Units of Measure

```fsharp
// Define units
[<Measure>] type kg
[<Measure>] type m
[<Measure>] type s

// Type-safe calculations
let distance = 100.0<m>
let time = 10.0<s>
let speed = distance / time  // Type: float<m/s>

// Prevents mixing units
let mass = 50.0<kg>
// let invalid = distance + mass  // Compile error!

// Converting units
let metersToKilometers (x: float<m>) : float =
    float x / 1000.0
```

---

## Interop with C#

### Calling C# from F#

```fsharp
// Use C# classes naturally
open System.Collections.Generic

let dict = Dictionary<string, int>()
dict.Add("one", 1)
dict.Add("two", 2)

// LINQ extension methods
open System.Linq

let numbers = [1..10]
let evens = numbers.Where(fun x -> x % 2 = 0).ToList()
```

### Calling F# from C#

```fsharp
// Design F# types for C# consumption
namespace MyLibrary

// Use [<CLIMutable>] for record types
[<CLIMutable>]
type Person = {
    FirstName: string
    LastName: string
    Age: int
}

// Use classes for OO APIs
type PersonService() =
    member _.GetPerson(id: int) : Person option =
        Some { FirstName = "John"; LastName = "Doe"; Age = 30 }

    // Convert Option to nullable for C#
    member this.TryGetPerson(id: int) : Person =
        match this.GetPerson(id) with
        | Some p -> p
        | None -> Unchecked.defaultof<Person>
```

---

## Module System

F# uses modules and namespaces to organize code. Modules are similar to static classes in C# but are more flexible and support nested modules, functions, and values.

### Namespaces

```fsharp
// File: Domain/User.fs
namespace MyApp.Domain

type User = {
    Id: int
    Name: string
    Email: string
}

// Can have multiple types in same namespace
type UserRepository() =
    member _.GetUser(id: int) : User option =
        None
```

### Modules

```fsharp
// Top-level module (one per file)
module MyApp.Utils

let add x y = x + y
let multiply x y = x * y

// Using from another file
open MyApp.Utils
let result = add 5 10
```

### Nested Modules

```fsharp
module MyApp.Math

// Nested module
module Arithmetic =
    let add x y = x + y
    let subtract x y = x - y

module Geometry =
    let area radius = System.Math.PI * radius * radius
    let circumference radius = 2.0 * System.Math.PI * radius

// Usage
open MyApp.Math
let sum = Arithmetic.add 5 10
let circle = Geometry.area 5.0
```

### Module Attributes

```fsharp
// AutoOpen: automatically opens when parent is opened
[<AutoOpen>]
module Helpers =
    let inline tap f x = f x; x
    let inline tee f x = f x |> ignore; x

// RequireQualifiedAccess: must use module name
[<RequireQualifiedAccess>]
module Config =
    let apiKey = "secret-key"
    let timeout = 30

// Usage:
// Can't do: open Config
// Must do: Config.apiKey
```

### Open Declarations

```fsharp
// Open entire namespace
open System.Collections.Generic

// Open specific module
open MyApp.Domain

// Open with alias
open System.Collections.Generic
open SCG = System.Collections.Generic
let dict = SCG.Dictionary<string, int>()

// Open type (type extensions available)
open type System.Math
let result = PI * 2.0  // Instead of Math.PI
```

### Signature Files (.fsi)

Signature files define the public API of a module, hiding implementation details.

```fsharp
// File: Domain.fsi (signature)
module MyApp.Domain

type User = {
    Id: int
    Name: string
}

val createUser: string -> User
val validateUser: User -> Result<User, string>
// Internal functions not exposed

// File: Domain.fs (implementation)
module MyApp.Domain

type User = {
    Id: int
    Name: string
}

// Public functions (in signature)
let createUser name = { Id = 0; Name = name }
let validateUser user =
    if user.Name.Length > 0 then Ok user
    else Error "Invalid name"

// Private helper (not in signature)
let private generateId() = System.Random().Next()
```

### Module Organization Patterns

```fsharp
// File-per-type pattern
// User.fs
namespace MyApp.Domain

type User = {
    Id: int
    Name: string
}

module User =
    let create name = { Id = 0; Name = name }
    let setName name user = { user with Name = name }

// Module-per-concept pattern
module MyApp.UserManagement

type User = { Id: int; Name: string }
type Role = Admin | User | Guest

let createUser name = { Id = 0; Name = name }
let assignRole user role = (user, role)
```

---

## Error Handling

F# provides powerful error handling through Option and Result types, enabling railway-oriented programming patterns that make error flows explicit and composable.

### Option Type

```fsharp
// Option represents optional values
type Option<'T> =
    | Some of 'T
    | None

// Returning Option from functions
let tryDivide x y =
    if y = 0 then None
    else Some (x / y)

// Pattern matching
match tryDivide 10 2 with
| Some result -> printfn $"Result: {result}"
| None -> printfn "Cannot divide by zero"

// Option module functions
let doubled = Option.map (fun x -> x * 2) (Some 5)  // Some 10
let getOrDefault = Option.defaultValue 0 None  // 0
```

### Result Type

```fsharp
// Result represents success or failure with error details
type Result<'T, 'TError> =
    | Ok of 'T
    | Error of 'TError

// Basic usage
let divide x y =
    if y = 0 then
        Error "Division by zero"
    else
        Ok (x / y)

// Pattern matching
match divide 10 2 with
| Ok result -> printfn $"Success: {result}"
| Error msg -> printfn $"Error: {msg}"

// Result module functions
let doubled = Result.map (fun x -> x * 2) (Ok 5)  // Ok 10
let chained = Ok 10 |> Result.bind (fun x -> divide x 2)  // Ok 5
```

### Railway-Oriented Programming

Railway-oriented programming treats successful and error paths as parallel railway tracks, making composition natural.

```fsharp
// Validation functions that can fail
let validateName name =
    if String.IsNullOrWhiteSpace(name) then
        Error "Name cannot be empty"
    else
        Ok name

let validateAge age =
    if age >= 0 && age <= 120 then
        Ok age
    else
        Error "Age must be between 0 and 120"

let validateEmail email =
    if email.Contains("@") then
        Ok email
    else
        Error "Invalid email format"

// Composition with Result computation expression
let createPerson name age email =
    result {
        let! validName = validateName name
        let! validAge = validateAge age
        let! validEmail = validateEmail email
        return {
            FirstName = validName
            LastName = ""
            Age = validAge
        }
    }

// Usage
match createPerson "Alice" 30 "alice@example.com" with
| Ok person -> printfn $"Created: {person.FirstName}"
| Error msg -> printfn $"Validation failed: {msg}"
```

### Custom Error Types

```fsharp
// Domain-specific errors
type ValidationError =
    | InvalidEmail of string
    | InvalidAge of int
    | InvalidName of string

type PaymentError =
    | InsufficientFunds of decimal
    | CardExpired of System.DateTime
    | NetworkError of string

// Using custom errors
let validateEmail email : Result<string, ValidationError> =
    if email.Contains("@") then
        Ok email
    else
        Error (InvalidEmail email)

// Combining different error types
type AppError =
    | Validation of ValidationError
    | Payment of PaymentError

let processPayment email amount =
    result {
        let! validEmail =
            validateEmail email
            |> Result.mapError Validation
        return "Payment successful"
    }
```

### Applicative Validation

Collect all errors instead of stopping at first failure.

```fsharp
// Validation that accumulates errors
type Validation<'T> = Result<'T, string list>

let validatePersonApplicative name age email : Validation<Person> =
    let nameResult =
        if String.IsNullOrWhiteSpace(name) then
            Error ["Name cannot be empty"]
        else
            Ok name

    let ageResult =
        if age >= 0 && age <= 120 then
            Ok age
        else
            Error ["Age must be between 0 and 120"]

    let emailResult =
        if email.Contains("@") then
            Ok email
        else
            Error ["Invalid email format"]

    // Combine all results
    match nameResult, ageResult, emailResult with
    | Ok n, Ok a, Ok e ->
        Ok { FirstName = n; LastName = ""; Age = a }
    | _ ->
        // Collect all errors
        [nameResult; ageResult; emailResult]
        |> List.choose (function Error errs -> Some errs | Ok _ -> None)
        |> List.concat
        |> Error
```

---

## Concurrency

F# provides first-class support for asynchronous and concurrent programming through async workflows, Task integration, and the MailboxProcessor (agent) model.

### Async Workflows

```fsharp
// Basic async computation
let fetchData url = async {
    printfn $"Fetching {url}..."
    do! Async.Sleep 1000  // Async sleep
    return $"Data from {url}"
}

// Run async computation
let data = fetchData "https://api.example.com" |> Async.RunSynchronously

// Parallel composition
let processParallel urls = async {
    let! results =
        urls
        |> List.map fetchData
        |> Async.Parallel
    return results |> Array.toList
}
```

### Error Handling in Async

```fsharp
// Async with Result
let safeFetchData url = async {
    try
        let! data = fetchData url
        return Ok data
    with
    | ex -> return Error ex.Message
}

// Catching specific exceptions
let fetchWithRetry url maxRetries = async {
    let rec loop retriesLeft =
        async {
            try
                let! data = fetchData url
                return Ok data
            with
            | :? System.Net.WebException when retriesLeft > 0 ->
                do! Async.Sleep 1000
                return! loop (retriesLeft - 1)
            | ex ->
                return Error $"Failed after {maxRetries} retries: {ex.Message}"
        }
    return! loop maxRetries
}
```

### Async.StartChild (Child Workflows)

```fsharp
// Start child async within parent workflow
let parentWorkflow = async {
    // Start child but don't wait yet
    let! childComputation = Async.StartChild(async {
        do! Async.Sleep 1000
        return 42
    })

    // Do other work while child runs
    printfn "Parent doing other work..."
    do! Async.Sleep 500

    // Now wait for child result
    let! result = childComputation
    return result * 2
}

// With timeout for child
let parentWithTimeout = async {
    let! childComputation =
        Async.StartChild(longRunningAsync, millisecondsTimeout = 5000)

    try
        let! result = childComputation
        return Ok result
    with
    | :? System.TimeoutException ->
        return Error "Child computation timed out"
}
```

### Task Integration

```fsharp
// Interop with .NET Task
open System.Threading.Tasks

// Task computation expression (F# 6+)
let fetchDataTask url = task {
    printfn $"Fetching {url}..."
    do! Task.Delay 1000
    return $"Data from {url}"
}

// Convert between Async and Task
let asyncToTask = fetchData "url" |> Async.StartAsTask
let taskToAsync = fetchDataTask "url" |> Async.AwaitTask
```

### Task vs Async Comparison

| Aspect | Async | Task |
|--------|-------|------|
| **Execution** | Cold (doesn't start until run) | Hot (starts immediately) |
| **Composition** | Easy with `async {}` | F# 6+ `task {}` builder |
| **Cancellation** | Built-in via CancellationToken | Via CancellationToken |
| **Exception handling** | Wrapped in Async | Direct exceptions |
| **.NET interop** | Convert with `Async.StartAsTask` | Native .NET |
| **Performance** | Slight overhead | Better for .NET interop |
| **Use when** | F#-centric code, composition | C# interop, ASP.NET Core |

```fsharp
// Prefer Async for F# composition
let processDataAsync inputs = async {
    let! results =
        inputs
        |> List.map processItemAsync
        |> Async.Parallel
    return Array.toList results
}

// Prefer Task for ASP.NET Core controllers
let handleRequest (ctx: HttpContext) = task {
    let! data = ctx.Request.ReadFromJsonAsync<InputData>()
    let result = processData data
    return! ctx.Response.WriteAsJsonAsync(result)
}
```

### MailboxProcessor (Agents)

The MailboxProcessor provides a message-based concurrency model, similar to Erlang's actors.

```fsharp
// Simple counter agent
type CounterMessage =
    | Increment
    | Decrement
    | Get of AsyncReplyChannel<int>

let counterAgent = MailboxProcessor.Start(fun inbox ->
    let rec loop count = async {
        let! msg = inbox.Receive()
        match msg with
        | Increment ->
            return! loop (count + 1)
        | Decrement ->
            return! loop (count - 1)
        | Get replyChannel ->
            replyChannel.Reply(count)
            return! loop count
    }
    loop 0)

// Using the agent
counterAgent.Post Increment
counterAgent.Post Increment
let count = counterAgent.PostAndReply(fun reply -> Get reply)  // 2
```

### Agent Patterns

```fsharp
// Request-reply pattern
type CacheMessage<'K, 'V> =
    | Get of key: 'K * AsyncReplyChannel<'V option>
    | Set of key: 'K * value: 'V
    | Clear

let createCache<'K, 'V when 'K: comparison>() =
    MailboxProcessor.Start(fun inbox ->
        let rec loop (cache: Map<'K, 'V>) = async {
            let! msg = inbox.Receive()
            match msg with
            | Get (key, replyChannel) ->
                replyChannel.Reply(Map.tryFind key cache)
                return! loop cache
            | Set (key, value) ->
                return! loop (Map.add key value cache)
            | Clear ->
                return! loop Map.empty
        }
        loop Map.empty)

// Usage
let cache = createCache<string, int>()
cache.Post (Set ("key1", 42))
let value = cache.PostAndReply(fun reply -> Get ("key1", reply))  // Some 42
```

### CancellationToken Support

```fsharp
open System.Threading

// Async with cancellation
let longRunningTask = async {
    for i in 1..100 do
        printfn $"Step {i}"
        do! Async.Sleep 100
    return "Completed"
}

// Create cancellation token
let cts = new CancellationTokenSource()

// Start with cancellation
Async.Start(longRunningTask, cts.Token)

// Cancel after 500ms
Thread.Sleep 500
cts.Cancel()
```

### Timeout Patterns

```fsharp
open System
open System.Threading

// Timeout with CancellationTokenSource
let withTimeout milliseconds computation = async {
    use cts = new CancellationTokenSource(milliseconds)
    try
        let! result = Async.StartChild(computation, millisecondsTimeout = milliseconds)
        let! value = result
        return Ok value
    with
    | :? TimeoutException -> return Error "Operation timed out"
    | :? OperationCanceledException -> return Error "Operation cancelled"
}

// Using Async.RunSynchronously with timeout
let resultWithTimeout =
    try
        fetchData "url" |> Async.RunSynchronously |> Some
    with
    | :? TimeoutException -> None

// Task timeout with Task.WhenAny
let withTaskTimeout (timeout: TimeSpan) (task: Task<'T>) = task {
    use cts = new CancellationTokenSource()
    let delayTask = Task.Delay(timeout, cts.Token)
    let! completedTask = Task.WhenAny(task, delayTask)
    if completedTask = (task :> Task) then
        cts.Cancel()
        return Ok (task.Result)
    else
        return Error "Task timed out"
}

// Combine cancellation and timeout
let fetchWithCancellationAndTimeout url (parentToken: CancellationToken) = async {
    use cts = CancellationTokenSource.CreateLinkedTokenSource(parentToken)
    cts.CancelAfter(5000)  // 5 second timeout

    try
        let! result = fetchData url
        return Ok result
    with
    | :? OperationCanceledException when parentToken.IsCancellationRequested ->
        return Error "Parent cancelled"
    | :? OperationCanceledException ->
        return Error "Timed out"
}
```

### Parallel Processing

```fsharp
// Parallel map (CPU-bound)
let numbers = [1..1000000]
let results = numbers |> Array.ofList |> Array.Parallel.map (fun x -> x * x)

// Parallel for
open System.Threading.Tasks

Parallel.For(0, 100, fun i ->
    printfn $"Iteration {i}"
) |> ignore
```

### Concurrency Model Comparison

| Model | Use Case | Characteristics |
|-------|----------|-----------------|
| **Async** | I/O-bound operations | Cooperative, composable, cold start |
| **Task** | .NET interop, hot operations | Eager, integrates with C# |
| **MailboxProcessor** | Stateful agents, actors | Message-passing, thread-safe state |
| **Array.Parallel** | CPU-bound data parallelism | Fork-join, automatic partitioning |
| **Parallel.For** | Fine-grained CPU parallelism | Loop-level parallelism |
| **Channels** | Producer-consumer | Bounded/unbounded queues |

```fsharp
// Choosing the right model
let ioWorkload urls =
    // Use Async for I/O-bound work
    urls
    |> List.map fetchAsync
    |> Async.Parallel
    |> Async.RunSynchronously

let cpuWorkload data =
    // Use Array.Parallel for CPU-bound work
    data
    |> Array.Parallel.map expensiveComputation

let statefulProcessor () =
    // Use MailboxProcessor for mutable state
    MailboxProcessor.Start(fun inbox ->
        let rec loop state = async {
            let! msg = inbox.Receive()
            let newState = processMessage state msg
            return! loop newState
        }
        loop initialState)
```

---

## Metaprogramming

F# provides powerful metaprogramming capabilities through type providers, quotations, computation expressions, and active patterns.

### Type Providers

Type providers generate types at compile-time based on external data sources, providing type-safe access to structured data.

```fsharp
// CSV Type Provider
open FSharp.Data

type Stocks = CsvProvider<"sample.csv">
let data = Stocks.Load("data.csv")

for row in data.Rows do
    printfn $"{row.Date}: ${row.Close}"

// JSON Type Provider
type Weather = JsonProvider<"""
{
    "city": "Seattle",
    "temperature": 72,
    "conditions": ["partly cloudy", "windy"]
}
""">

let weather = Weather.Load("weather.json")
printfn $"{weather.City}: {weather.Temperature}°F"
```

### Quotations

Quotations represent F# code as abstract syntax trees (AST) for manipulation and analysis.

```fsharp
open Microsoft.FSharp.Quotations

// Code quotations
let expr = <@ 1 + 2 @>  // Typed quotation
let rawExpr = <@@ 1 + 2 @@>  // Untyped quotation

// Examining quotations
let rec printExpr expr =
    match expr with
    | Patterns.Value(v, _) -> printfn $"Value: {v}"
    | Patterns.Call(_, mi, args) ->
        printfn $"Call: {mi.Name}"
        args |> List.iter printExpr
    | Patterns.Lambda(var, body) ->
        printfn $"Lambda: {var.Name}"
        printExpr body
    | _ -> printfn "Other pattern"
```

### Quotation Patterns

```fsharp
open Microsoft.FSharp.Quotations.Patterns
open Microsoft.FSharp.Quotations.DerivedPatterns

// Pattern matching on quotations
let rec evaluate expr =
    match expr with
    | Value(v, t) when t = typeof<int> ->
        v :?> int
    | Call(None, mi, [left; right]) when mi.Name = "op_Addition" ->
        evaluate left + evaluate right
    | Call(None, mi, [left; right]) when mi.Name = "op_Multiply" ->
        evaluate left * evaluate right
    | _ -> failwith "Unsupported expression"

// Usage
let result = evaluate <@ 2 + 3 * 4 @>  // 14
```

### Computation Expressions

Computation expressions provide syntactic sugar for monadic operations.

```fsharp
// Custom computation expression builder
type MaybeBuilder() =
    member _.Bind(x, f) = Option.bind f x
    member _.Return(x) = Some x
    member _.ReturnFrom(x) = x
    member _.Zero() = None
    member _.Delay(f) = f
    member _.Run(f) = f()

let maybe = MaybeBuilder()

// Usage
let result = maybe {
    let! x = Some 5
    let! y = Some 10
    return x + y
}  // Some 15
```

### Advanced Active Patterns

```fsharp
// Parameterized active patterns
let (|DivisibleBy|_|) divisor n =
    if n % divisor = 0 then Some () else None

match 15 with
| DivisibleBy 3 -> "Divisible by 3"
| DivisibleBy 5 -> "Divisible by 5"
| _ -> "Not divisible"

// Multi-case with computation
let (|Small|Medium|Large|Huge|) value =
    if value < 10 then Small
    elif value < 100 then Medium value
    elif value < 1000 then Large value
    else Huge value

match 150 with
| Small -> "small"
| Medium x -> $"medium: {x}"
| Large x -> $"large: {x}"
| Huge -> "huge"
```

### Reflection

```fsharp
open System.Reflection

// Get type information
let t = typeof<Person>
printfn $"Type: {t.Name}"
printfn $"Properties: {t.GetProperties().Length}"

// Create instance dynamically
let createInstance (t: System.Type) =
    System.Activator.CreateInstance(t)

// Invoke method
let invokeMethod obj methodName args =
    let t = obj.GetType()
    let mi = t.GetMethod(methodName)
    mi.Invoke(obj, args)
```

---

## Zero/Default Values

F# handles default and zero values differently than C#, with a strong emphasis on explicit handling through Option types rather than null references.

### Option.None vs Null

```fsharp
// Preferred: Use Option for optional values
type Person = {
    Name: string
    Email: string option  // Explicitly optional
    Age: int
}

let person = {
    Name = "Alice"
    Email = None  // Explicit absence
    Age = 30
}

// Pattern matching makes absence explicit
match person.Email with
| Some email -> printfn $"Email: {email}"
| None -> printfn "No email provided"
```

### Default Values in Records

```fsharp
// Records don't have default constructors
type Config = {
    Host: string
    Port: int
    EnableLogging: bool
}

// Create default config explicitly
let defaultConfig = {
    Host = "localhost"
    Port = 8080
    EnableLogging = false
}

// Smart constructor pattern for defaults
module Config =
    let create() = {
        Host = "localhost"
        Port = 8080
        EnableLogging = false
    }

    let withHost host config = { config with Host = host }
    let withPort port config = { config with Port = port }

// Usage with fluent API
let config =
    Config.create()
    |> Config.withHost "api.example.com"
    |> Config.withPort 443
```

### Unchecked.defaultof<'T>

```fsharp
// Get CLR default value for a type
let defaultInt = Unchecked.defaultof<int>      // 0
let defaultBool = Unchecked.defaultof<bool>    // false
let defaultString = Unchecked.defaultof<string>  // null
let defaultOption = Unchecked.defaultof<int option>  // None

// Useful for interop with .NET APIs
type MyClass() =
    let mutable value: string = Unchecked.defaultof<string>

    member _.Value
        with get() = value
        and set(v) = value <- v
```

### Null Handling for Interop

```fsharp
// Checking for null from .NET
let safeToUpper (s: string) =
    if isNull s then
        None
    else
        Some (s.ToUpper())

// Option.ofObj: convert null to None
let fromNullable (s: string) =
    Option.ofObj s

let result = fromNullable null  // None
let result2 = fromNullable "test"  // Some "test"

// Option.toObj: convert None to null
let toNullable opt =
    Option.toObj opt

let nullable = toNullable None  // null
let nullable2 = toNullable (Some "test")  // "test"
```

### Array and Collection Defaults

```fsharp
// Empty collections
let emptyList = []
let emptyArray = [||]
let emptySeq = Seq.empty
let emptyMap = Map.empty
let emptySet = Set.empty

// Arrays initialized with default values
let zeros = Array.zeroCreate<int> 10  // [|0; 0; 0; ...|]
let defaults = Array.create 5 "default"  // [|"default"; "default"; ...|]

// Using init for custom defaults
let squares = Array.init 5 (fun i -> i * i)  // [|0; 1; 4; 9; 16|]
```

### Nullable<'T> for Value Types

```fsharp
open System

// Interop with .NET Nullable
let nullableInt: Nullable<int> = Nullable()  // No value
let nullableInt2: Nullable<int> = Nullable(42)  // Has value

// Check for value
if nullableInt.HasValue then
    printfn $"Value: {nullableInt.Value}"
else
    printfn "No value"

// Convert to/from Option
let fromNullable (n: Nullable<'T>) : 'T option =
    if n.HasValue then Some n.Value else None

let toNullable (opt: 'T option) : Nullable<'T> =
    match opt with
    | Some v -> Nullable(v)
    | None -> Nullable()
```

### Best Practices

```fsharp
// Do: Use Option for optional values
type User = {
    Name: string
    Email: string option  // Explicit
    Age: int
}

// Don't: Use null for optional values
type BadUser = {
    Name: string
    Email: string  // Could be null - unclear
    Age: int
}

// Do: Provide explicit default functions
module User =
    let create name = {
        Name = name
        Email = None
        Age = 0
    }

// Don't: Rely on Unchecked.defaultof unless necessary
let badDefault = Unchecked.defaultof<User>  // Null, not a valid User
```

---

## Common Idioms

### Dependency Injection (Reader Pattern)

```fsharp
// Pass dependencies explicitly
type Dependencies = {
    GetTime: unit -> System.DateTime
    Logger: string -> unit
}

let processOrder deps orderId =
    deps.Logger $"Processing order {orderId}"
    let timestamp = deps.GetTime()
    // ... rest of logic

// Usage
let deps = {
    GetTime = fun () -> System.DateTime.Now
    Logger = printfn "%s"
}

processOrder deps 123
```

### Event Sourcing Pattern

```fsharp
// Define events
type AccountEvent =
    | AccountOpened of customerId: string * initialBalance: decimal
    | MoneyDeposited of amount: decimal
    | MoneyWithdrawn of amount: decimal

// Apply events to state
type Account = { Balance: decimal }

let apply state event =
    match event with
    | AccountOpened (_, initialBalance) ->
        { Balance = initialBalance }
    | MoneyDeposited amount ->
        { state with Balance = state.Balance + amount }
    | MoneyWithdrawn amount ->
        { state with Balance = state.Balance - amount }

// Rebuild state from events
let buildState events =
    events |> List.fold apply { Balance = 0m }
```

---

## Troubleshooting

### Type Inference Issues

**Problem:** Compiler can't infer types

```fsharp
// Error: type inference failure
let processItems items =
    items |> List.map (fun x -> x.ToString())
```

**Fix:** Add type annotations
```fsharp
let processItems (items: int list) =
    items |> List.map (fun x -> x.ToString())
```

### Option/Result Unwrapping

**Problem:** Nested Option/Result types

```fsharp
// Bad: nested Some
let findAndProcess id =
    match find id with
    | Some person ->
        match process person with
        | Some result -> Some result
        | None -> None
    | None -> None
```

**Fix:** Use computation expressions or bind
```fsharp
let findAndProcess id =
    find id
    |> Option.bind process
```

### Mutable vs Immutable

**Problem:** Need to update values

```fsharp
// Doesn't work - records are immutable
let person = { FirstName = "John"; LastName = "Doe"; Age = 30 }
person.Age <- 31  // Error!
```

**Fix:** Use copy-and-update or mutable
```fsharp
// Functional: create new record
let olderPerson = { person with Age = 31 }

// Or use mutable if really needed
type MutablePerson = {
    FirstName: string
    LastName: string
    mutable Age: int
}
```

### Recursive Type Definitions

**Problem:** Types reference each other

```fsharp
// Error: types not defined yet
type Folder = { Name: string; Items: Item list }
type Item = File of string | Folder of Folder
```

**Fix:** Use `and` keyword
```fsharp
type Folder = { Name: string; Items: Item list }
and Item = File of string | Folder of Folder
```

---

## Serialization

F# works seamlessly with .NET serialization libraries while maintaining functional idioms. For cross-language serialization patterns, see `patterns-serialization-dev`.

### System.Text.Json

```fsharp
open System.Text.Json
open System.Text.Json.Serialization

// Simple record serialization
type Person = {
    FirstName: string
    LastName: string
    Age: int
}

let person = { FirstName = "Alice"; LastName = "Smith"; Age = 30 }
let json = JsonSerializer.Serialize(person)
// {"FirstName":"Alice","LastName":"Smith","Age":30}

let parsed = JsonSerializer.Deserialize<Person>(json)

// Custom options
let options = JsonSerializerOptions()
options.PropertyNamingPolicy <- JsonNamingPolicy.CamelCase
options.WriteIndented <- true

let camelCaseJson = JsonSerializer.Serialize(person, options)
// {
//   "firstName": "alice",
//   "lastName": "smith",
//   "age": 30
// }
```

### JsonFSharpConverter for F# Types

```fsharp
open System.Text.Json
open System.Text.Json.Serialization

// Configure for F# discriminated unions and options
let options = JsonSerializerOptions()
options.Converters.Add(JsonFSharpConverter())

// Discriminated union serialization
type PaymentMethod =
    | Cash
    | CreditCard of cardNumber: string
    | DebitCard of cardNumber: string * pin: int

let payment = CreditCard "1234-5678-9012-3456"
let json = JsonSerializer.Serialize(payment, options)
// {"Case":"CreditCard","Fields":["1234-5678-9012-3456"]}

// Option type handling
type User = {
    Name: string
    Email: string option
}

let user = { Name = "Bob"; Email = Some "bob@example.com" }
let userJson = JsonSerializer.Serialize(user, options)
```

### Custom Converters

```fsharp
open System
open System.Text.Json
open System.Text.Json.Serialization

// Custom converter for EmailAddress
type EmailAddress = EmailAddress of string

type EmailAddressConverter() =
    inherit JsonConverter<EmailAddress>()

    override _.Read(reader, typeToConvert, options) =
        EmailAddress (reader.GetString())

    override _.Write(writer, value, options) =
        let (EmailAddress email) = value
        writer.WriteStringValue(email)

// Register converter
let options = JsonSerializerOptions()
options.Converters.Add(EmailAddressConverter())

let email = EmailAddress "test@example.com"
let json = JsonSerializer.Serialize(email, options)
// "test@example.com"
```

### FSharp.Json

```fsharp
open FSharp.Json

// Simple serialization
type Config = {
    Port: int
    Host: string
    Debug: bool
}

let config = { Port = 8080; Host = "localhost"; Debug = true }
let json = Json.serialize config
let parsed = Json.deserialize<Config> json

// Custom field names
type ApiResponse = {
    [<JsonField("response_code")>]
    ResponseCode: int

    [<JsonField("response_data")>]
    Data: string
}

// Transform during serialization
type Settings = {
    [<JsonField(Transform=typeof<Transforms.CamelCase>)>]
    DatabaseUrl: string

    [<JsonField(Transform=typeof<Transforms.SnakeCase>)>]
    MaxConnections: int
}
```

### Type Providers for JSON

```fsharp
open FSharp.Data

// Infer schema from sample JSON
type Weather = JsonProvider<"""
{
    "temperature": 72.5,
    "condition": "sunny",
    "humidity": 65,
    "forecast": [
        {"day": "Monday", "high": 75, "low": 60},
        {"day": "Tuesday", "high": 78, "low": 62}
    ]
}
""">

// Use with type safety
let weather = Weather.Load("weather.json")
printfn $"Temperature: {weather.Temperature}°F"
printfn $"Condition: {weather.Condition}"

weather.Forecast
|> Array.iter (fun day ->
    printfn $"{day.Day}: {day.High}°F / {day.Low}°F")

// From URL
let liveWeather = Weather.Load("https://api.weather.com/current")

// Parse from string
let jsonString = """{"temperature":68,"condition":"cloudy","humidity":70}"""
let parsed = Weather.Parse(jsonString)
```

### Validation Patterns

```fsharp
// Validation with Result
type ValidationError = string

let validateEmail (email: string) : Result<string, ValidationError> =
    if email.Contains("@") then
        Ok email
    else
        Error "Invalid email format"

let validateAge (age: int) : Result<int, ValidationError> =
    if age >= 0 && age <= 120 then
        Ok age
    else
        Error "Age must be between 0 and 120"

// Combine validations
type PersonData = {
    Name: string
    Email: string
    Age: int
}

let validatePerson data =
    result {
        let! validEmail = validateEmail data.Email
        let! validAge = validateAge data.Age
        return { data with Email = validEmail; Age = validAge }
    }

// Applicative validation (collect all errors)
type Validation<'T> = Result<'T, ValidationError list>

let validatePersonApplicative data : Validation<PersonData> =
    let validateName name =
        if String.IsNullOrWhiteSpace(name) then
            Error ["Name cannot be empty"]
        else
            Ok name

    match (validateName data.Name, validateEmail data.Email, validateAge data.Age) with
    | Ok n, Ok e, Ok a -> Ok { Name = n; Email = e; Age = a }
    | errors ->
        errors
        |> fun (n, e, a) ->
            [n; e; a]
            |> List.collect (function Error errs -> errs | Ok _ -> [])
        |> Error
```

---

## Build and Dependencies

F# uses the standard .NET build ecosystem with project files, NuGet packages, and the dotnet CLI.

### Project File (.fsproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <OutputType>Exe</OutputType>
    <RootNamespace>MyApp</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <!-- Order matters in F#! Files are compiled top-to-bottom -->
    <Compile Include="Types.fs" />
    <Compile Include="Helpers.fs" />
    <Compile Include="Domain.fs" />
    <Compile Include="Program.fs" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="FSharp.Data" Version="6.3.0" />
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  </ItemGroup>

</Project>
```

### dotnet CLI Commands

```bash
# Create new project
dotnet new console -lang F# -o MyApp
dotnet new classlib -lang F# -o MyLib
dotnet new webapi -lang F# -o MyApi

# Build and run
dotnet build
dotnet run
dotnet run -- arg1 arg2  # Pass arguments

# Watch mode (rebuild on file changes)
dotnet watch run

# Clean build artifacts
dotnet clean

# Restore packages
dotnet restore

# Create solution
dotnet new sln -n MySolution
dotnet sln add MyApp/MyApp.fsproj
dotnet sln add MyLib/MyLib.fsproj
```

### NuGet Package Management

```bash
# Add package
dotnet add package FSharp.Data
dotnet add package Newtonsoft.Json --version 13.0.3

# Remove package
dotnet remove package FSharp.Data

# Update package
dotnet add package FSharp.Data  # Gets latest

# List packages
dotnet list package

# List outdated packages
dotnet list package --outdated
```

### Package References in .fsproj

```xml
<ItemGroup>
  <!-- Exact version -->
  <PackageReference Include="FSharp.Core" Version="8.0.0" />

  <!-- Version range -->
  <PackageReference Include="FSharp.Data" Version="[6.0,7.0)" />

  <!-- Latest stable -->
  <PackageReference Include="Newtonsoft.Json" Version="*" />

  <!-- Development only -->
  <PackageReference Include="FsCheck" Version="2.16.5">
    <PrivateAssets>all</PrivateAssets>
  </PackageReference>
</ItemGroup>
```

### Project References

```xml
<!-- Reference another project -->
<ItemGroup>
  <ProjectReference Include="..\MyLib\MyLib.fsproj" />
</ItemGroup>
```

```bash
# Add project reference via CLI
dotnet add reference ../MyLib/MyLib.fsproj
```

### Paket (Alternative Package Manager)

```bash
# Install Paket
dotnet tool install paket

# Initialize Paket
dotnet paket init

# Add package
dotnet paket add FSharp.Data

# Install dependencies
dotnet paket install

# Update all packages
dotnet paket update
```

**paket.dependencies:**
```
source https://api.nuget.org/v3/index.json

nuget FSharp.Core >= 8.0
nuget FSharp.Data ~> 6.3
nuget Newtonsoft.Json

group Test
  nuget Expecto
  nuget FsCheck
```

**paket.references:**
```
FSharp.Data
Newtonsoft.Json

group Test
  Expecto
  FsCheck
```

### FAKE Build Script

```fsharp
// build.fsx
#r "paket:
nuget Fake.Core.Target
nuget Fake.DotNet.Cli //"
#load ".fake/build.fsx/intellisense.fsx"

open Fake.Core
open Fake.DotNet

let clean _ =
    !! "**/bin"
    ++ "**/obj"
    |> Shell.cleanDirs

let build _ =
    DotNet.build id ""

let test _ =
    DotNet.test id ""

let publish _ =
    DotNet.publish (fun opts ->
        { opts with
            Configuration = DotNet.BuildConfiguration.Release
            OutputPath = Some "./publish" }) ""

// Define targets
Target.create "Clean" clean
Target.create "Build" build
Target.create "Test" test
Target.create "Publish" publish

// Dependencies
open Fake.Core.TargetOperators

"Clean"
  ==> "Build"
  ==> "Test"
  ==> "Publish"

Target.runOrDefault "Build"
```

Run with:
```bash
dotnet fake build
dotnet fake build -t Publish
```

### Multi-Project Structure

```
MySolution/
├── MySolution.sln
├── src/
│   ├── MyApp/
│   │   ├── MyApp.fsproj
│   │   ├── Program.fs
│   │   └── Domain.fs
│   └── MyLib/
│       ├── MyLib.fsproj
│       ├── Types.fs
│       └── Utils.fs
├── tests/
│   └── MyApp.Tests/
│       ├── MyApp.Tests.fsproj
│       └── Tests.fs
├── paket.dependencies
└── build.fsx
```

### Publishing

```bash
# Publish for specific runtime
dotnet publish -r win-x64 -c Release
dotnet publish -r linux-x64 -c Release
dotnet publish -r osx-arm64 -c Release

# Self-contained (includes runtime)
dotnet publish -r linux-x64 -c Release --self-contained

# Framework-dependent (requires .NET runtime installed)
dotnet publish -c Release --no-self-contained

# Single file
dotnet publish -r linux-x64 -c Release /p:PublishSingleFile=true
```

### NuGet Package Creation

```xml
<!-- Add to .fsproj -->
<PropertyGroup>
  <PackageId>MyAwesomeLibrary</PackageId>
  <Version>1.0.0</Version>
  <Authors>Your Name</Authors>
  <Description>An awesome F# library</Description>
  <PackageLicenseExpression>MIT</PackageLicenseExpression>
  <RepositoryUrl>https://github.com/username/repo</RepositoryUrl>
</PropertyGroup>
```

```bash
# Create package
dotnet pack -c Release

# Publish to NuGet
dotnet nuget push bin/Release/MyAwesomeLibrary.1.0.0.nupkg --api-key YOUR_KEY --source https://api.nuget.org/v3/index.json
```

---

## Testing

F# has excellent testing support with Expecto, FsUnit, and FsCheck for property-based testing.

### Expecto

```fsharp
// Tests.fs
module Tests

open Expecto

// Simple test
let simpleTest =
    testCase "addition works" <| fun () ->
        let result = 1 + 1
        Expect.equal result 2 "1 + 1 should equal 2"

// Test list
let mathTests =
    testList "Math operations" [
        testCase "addition" <| fun () ->
            Expect.equal (2 + 2) 4 "2 + 2 = 4"

        testCase "subtraction" <| fun () ->
            Expect.equal (5 - 3) 2 "5 - 3 = 2"

        testCase "multiplication" <| fun () ->
            Expect.equal (3 * 4) 12 "3 * 4 = 12"
    ]

// Run all tests
[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args mathTests
```

### Expecto Matchers

```fsharp
open Expecto

let expectTests =
    testList "Expecto expectations" [
        testCase "equal" <| fun () ->
            Expect.equal (1 + 1) 2 "should be equal"

        testCase "not equal" <| fun () ->
            Expect.notEqual 1 2 "should not be equal"

        testCase "is true" <| fun () ->
            Expect.isTrue (5 > 3) "5 should be greater than 3"

        testCase "is false" <| fun () ->
            Expect.isFalse (3 > 5) "3 should not be greater than 5"

        testCase "contains" <| fun () ->
            Expect.contains [1; 2; 3] 2 "list should contain 2"

        testCase "sequence equal" <| fun () ->
            Expect.sequenceEqual [1; 2; 3] [1; 2; 3] "sequences should match"

        testCase "throws" <| fun () ->
            Expect.throws (fun () -> failwith "boom") "should throw"

        testCase "is some" <| fun () ->
            Expect.isSome (Some 5) "should be Some"

        testCase "is none" <| fun () ->
            Expect.isNone None "should be None"
    ]
```

### Async and Task Testing

```fsharp
open Expecto

let asyncTests =
    testList "Async tests" [
        testCaseAsync "async computation" <| async {
            let! result = async { return 42 }
            Expect.equal result 42 "async result"
        }

        testTask "task computation" {
            let! result = task { return 42 }
            Expect.equal result 42 "task result"
        }
    ]
```

### Test Organization

```fsharp
// Nested test groups
let allTests =
    testList "All tests" [
        testList "Domain" [
            testList "User" [
                testCase "create user" <| fun () ->
                    let user = createUser "Alice" "alice@example.com"
                    Expect.equal user.Name "Alice" "name matches"
            ]
            testList "Order" [
                testCase "calculate total" <| fun () ->
                    let total = calculateTotal [10m; 20m; 30m]
                    Expect.equal total 60m "total is sum"
            ]
        ]
        testList "API" [
            // API tests
        ]
    ]

// Run with filters
[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args allTests

// Run specific tests:
// dotnet run -- --filter "User"
```

### FsUnit with xUnit

```fsharp
module Tests

open Xunit
open FsUnit.Xunit

[<Fact>]
let ``2 + 2 should equal 4`` () =
    2 + 2 |> should equal 4

[<Fact>]
let ``list should contain element`` () =
    [1; 2; 3] |> should contain 2

[<Fact>]
let ``string should start with`` () =
    "hello world" |> should startWith "hello"

[<Fact>]
let ``option should be Some`` () =
    Some 5 |> should be (ofCase <@ Some @>)

[<Theory>]
[<InlineData(1, 2, 3)>]
[<InlineData(5, 5, 10)>]
[<InlineData(-1, 1, 0)>]
let ``addition works for multiple inputs`` a b expected =
    a + b |> should equal expected
```

### FsCheck Property-Based Testing

```fsharp
open Expecto
open FsCheck

// Property test with Expecto
let propertyTests =
    testList "Property tests" [
        testProperty "reverse twice equals original" <| fun (xs: int list) ->
            List.rev (List.rev xs) = xs

        testProperty "length of reverse equals length" <| fun (xs: int list) ->
            List.length (List.rev xs) = List.length xs

        testProperty "addition is commutative" <| fun (a: int) (b: int) ->
            a + b = b + a

        testProperty "list append length" <| fun (xs: int list) (ys: int list) ->
            List.length (xs @ ys) = List.length xs + List.length ys
    ]

// Custom generator
let positiveInt = Arb.generate<int> |> Gen.map abs

let customGeneratorTest =
    testProperty "square of positive is positive" <| fun () ->
        Prop.forAll (Arb.fromGen positiveInt) (fun n ->
            n * n >= 0)

// Conditional properties
let conditionalTest =
    testProperty "division by non-zero" <| fun (a: float) (b: float) ->
        b <> 0.0 ==> lazy (a / b * b = a)
```

### FsCheck with xUnit

```fsharp
open Xunit
open FsCheck
open FsCheck.Xunit

[<Property>]
let ``reverse twice gives original`` (xs: int list) =
    List.rev (List.rev xs) = xs

[<Property>]
let ``sort is idempotent`` (xs: int list) =
    List.sort (List.sort xs) = List.sort xs

[<Property(Arbitrary = [| typeof<CustomGenerators> |])>]
let ``custom generator property`` (email: string) =
    email.Contains("@")

// Custom generators
type CustomGenerators =
    static member Email() =
        let genEmail =
            gen {
                let! user = Gen.elements ["alice"; "bob"; "charlie"]
                let! domain = Gen.elements ["example.com"; "test.com"]
                return $"{user}@{domain}"
            }
        Arb.fromGen genEmail
```

### Test Setup and Teardown

```fsharp
open Expecto

// Setup/teardown pattern
let withDatabase test =
    let db = setupDatabase()  // Setup
    try
        test db
    finally
        cleanupDatabase db  // Teardown

let databaseTests =
    testList "Database tests" [
        testCase "insert user" <| fun () ->
            withDatabase (fun db ->
                insertUser db "Alice"
                let users = getUsers db
                Expect.contains users "Alice" "user should exist"
            )
    ]

// Shared fixture
type DatabaseFixture() =
    let db = setupDatabase()
    member _.Database = db
    interface System.IDisposable with
        member _.Dispose() = cleanupDatabase db

let fixtureTests =
    testSequenced <| testList "Sequenced tests" [
        let fixture = new DatabaseFixture()
        yield testCase "test 1" <| fun () ->
            // use fixture.Database
            ()
        yield testCase "test 2" <| fun () ->
            // use fixture.Database
            ()
    ]
```

### Mocking and Stubs

```fsharp
// Interface-based mocking
type IUserRepository =
    abstract member GetUser: int -> User option
    abstract member SaveUser: User -> unit

// Create stub for testing
let createStubRepository users =
    { new IUserRepository with
        member _.GetUser(id) =
            users |> List.tryFind (fun u -> u.Id = id)
        member _.SaveUser(user) =
            () // No-op for testing
    }

let testWithStub =
    testCase "get user from stub" <| fun () ->
        let users = [
            { Id = 1; Name = "Alice"; Email = "alice@example.com"; Age = 30 }
            { Id = 2; Name = "Bob"; Email = "bob@example.com"; Age = 25 }
        ]
        let repo = createStubRepository users
        let user = repo.GetUser(1)
        Expect.isSome user "should find user"
        Expect.equal user.Value.Name "Alice" "name should match"
```

### Running Tests

```bash
# Run with dotnet
dotnet run  # If entry point is defined
dotnet test  # If using xUnit/NUnit

# Expecto options
dotnet run -- --help
dotnet run -- --filter "User"
dotnet run -- --sequenced
dotnet run -- --debug
dotnet run -- --fail-on-focused-tests

# Watch mode
dotnet watch run
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-serialization-dev` - JSON/YAML handling, validation patterns
- `patterns-concurrency-dev` - Async workflows, parallel processing, Mailbox processors
- `patterns-metaprogramming-dev` - Type providers, computation expressions, quotations

---

## References

- [F# Language Reference](https://docs.microsoft.com/en-us/dotnet/fsharp/language-reference/)
- [F# for Fun and Profit](https://fsharpforfunandprofit.com/)
- [F# Style Guide](https://docs.microsoft.com/en-us/dotnet/fsharp/style-guide/)
- [Domain Modeling Made Functional](https://pragprog.com/titles/swdddf/domain-modeling-made-functional/)
