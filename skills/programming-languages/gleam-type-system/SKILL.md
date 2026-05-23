---
name: Gleam Type System
description: Use when gleam's type system including algebraic data types, custom types, pattern matching, generic types, type inference, opaque types, exhaustive checking, and functional error handling for building type-safe Erlang VM applications.
allowed-tools: []
---

# Gleam Type System

## Introduction

Gleam is a statically-typed functional language that compiles to Erlang and
JavaScript, bringing modern type safety to the BEAM ecosystem. Its type system
prevents entire categories of runtime errors while maintaining the concurrency
and fault-tolerance benefits of the Erlang VM.

The type system features algebraic data types, parametric polymorphism, type
inference, exhaustive pattern matching, and no null values. Every value is typed,
and the compiler enforces type safety at compile time, eliminating common bugs
before code runs.

This skill covers custom types and ADTs, pattern matching, generic types, Result
and Option types, type aliases, opaque types, type inference, and patterns for
type-safe error handling on the BEAM.

## Custom Types and Records

Custom types define structured data with named fields, providing type-safe
access and pattern matching.

```gleam
// Simple custom type (record)
pub type User {
  User(name: String, age: Int, email: String)
}

// Creating instances
pub fn create_user() -> User {
  User(name: "Alice", age: 30, email: "alice@example.com")
}

// Accessing fields
pub fn get_user_name(user: User) -> String {
  user.name
}

pub fn get_user_age(user: User) -> Int {
  user.age
}

// Updating records (immutable)
pub fn birthday(user: User) -> User {
  User(..user, age: user.age + 1)
}

pub fn change_email(user: User, new_email: String) -> User {
  User(..user, email: new_email)
}

// Multiple constructors
pub type Shape {
  Circle(radius: Float)
  Rectangle(width: Float, height: Float)
  Triangle(base: Float, height: Float)
}

pub fn area(shape: Shape) -> Float {
  case shape {
    Circle(radius) -> 3.14159 *. radius *. radius
    Rectangle(width, height) -> width *. height
    Triangle(base, height) -> base *. height /. 2.0
  }
}

// Tuple structs (unlabeled fields)
pub type Point {
  Point(Float, Float)
}

pub fn distance(p1: Point, p2: Point) -> Float {
  let Point(x1, y1) = p1
  let Point(x2, y2) = p2
  let dx = x2 -. x1
  let dy = y2 -. y1
  float.square_root(dx *. dx +. dy *. dy)
}

// Nested custom types
pub type Address {
  Address(street: String, city: String, zip: String)
}

pub type Person {
  Person(name: String, age: Int, address: Address)
}

pub fn get_city(person: Person) -> String {
  person.address.city
}

// Generic custom types
pub type Box(a) {
  Box(value: a)
}

pub fn box_map(box: Box(a), f: fn(a) -> b) -> Box(b) {
  Box(value: f(box.value))
}

pub fn unbox(box: Box(a)) -> a {
  box.value
}

// Recursive types
pub type Tree(a) {
  Leaf(value: a)
  Branch(left: Tree(a), right: Tree(a))
}

pub fn tree_depth(tree: Tree(a)) -> Int {
  case tree {
    Leaf(_) -> 1
    Branch(left, right) -> 1 + int.max(tree_depth(left), tree_depth(right))
  }
}

// Phantom types for type-safe APIs
pub type Validated
pub type Unvalidated

pub type Email(state) {
  Email(value: String)
}

pub fn create_email(value: String) -> Email(Unvalidated) {
  Email(value: value)
}

pub fn validate_email(email: Email(Unvalidated)) ->
  Result(Email(Validated), String) {
  case string.contains(email.value, "@") {
    True -> Ok(Email(value: email.value))
    False -> Error("Invalid email format")
  }
}

pub fn send_email(email: Email(Validated)) -> Nil {
  // Only validated emails can be sent
  io.println("Sending email to: " <> email.value)
}
```

Custom types provide named, type-safe data structures with exhaustive pattern
matching guarantees.

## Algebraic Data Types

ADTs model data with multiple variants, enabling exhaustive pattern matching and
making invalid states unrepresentable.

```gleam
// Sum type (enum)
pub type Status {
  Pending
  Approved
  Rejected
}

pub fn status_to_string(status: Status) -> String {
  case status {
    Pending -> "Pending"
    Approved -> "Approved"
    Rejected -> "Rejected"
  }
}

// Result type (built-in ADT)
pub type Result(ok, error) {
  Ok(ok)
  Error(error)
}

pub fn parse_int(str: String) -> Result(Int, String) {
  case int.parse(str) {
    Ok(n) -> Ok(n)
    Error(_) -> Error("Not a valid integer")
  }
}

pub fn handle_result(result: Result(Int, String)) -> String {
  case result {
    Ok(n) -> "Got number: " <> int.to_string(n)
    Error(msg) -> "Error: " <> msg
  }
}

// Option type pattern
pub type Option(a) {
  Some(a)
  None
}

pub fn find_user(id: Int) -> Option(User) {
  case id {
    1 -> Some(User(name: "Alice", age: 30, email: "alice@example.com"))
    _ -> None
  }
}

pub fn option_map(opt: Option(a), f: fn(a) -> b) -> Option(b) {
  case opt {
    Some(value) -> Some(f(value))
    None -> None
  }
}

pub fn option_unwrap_or(opt: Option(a), default: a) -> a {
  case opt {
    Some(value) -> value
    None -> default
  }
}

// Complex ADTs
pub type HttpResponse {
  Ok200(body: String)
  Created201(body: String, location: String)
  BadRequest400(message: String)
  NotFound404
  ServerError500(message: String)
}

pub fn handle_response(response: HttpResponse) -> String {
  case response {
    Ok200(body) -> "Success: " <> body
    Created201(body, location) -> "Created at " <> location <> ": " <> body
    BadRequest400(message) -> "Bad request: " <> message
    NotFound404 -> "Resource not found"
    ServerError500(message) -> "Server error: " <> message
  }
}

// Linked list ADT
pub type List(a) {
  Nil
  Cons(head: a, tail: List(a))
}

pub fn list_length(list: List(a)) -> Int {
  case list {
    Nil -> 0
    Cons(_, tail) -> 1 + list_length(tail)
  }
}

pub fn list_map(list: List(a), f: fn(a) -> b) -> List(b) {
  case list {
    Nil -> Nil
    Cons(head, tail) -> Cons(f(head), list_map(tail, f))
  }
}

// Either type
pub type Either(left, right) {
  Left(left)
  Right(right)
}

pub fn partition_either(list: List(Either(a, b))) -> #(List(a), List(b)) {
  case list {
    Nil -> #(Nil, Nil)
    Cons(Left(a), tail) -> {
      let #(lefts, rights) = partition_either(tail)
      #(Cons(a, lefts), rights)
    }
    Cons(Right(b), tail) -> {
      let #(lefts, rights) = partition_either(tail)
      #(lefts, Cons(b, rights))
    }
  }
}

// State machine with ADTs
pub type ConnectionState {
  Disconnected
  Connecting(attempt: Int)
  Connected(session_id: String)
  Disconnecting
}

pub fn handle_connect_event(state: ConnectionState) -> ConnectionState {
  case state {
    Disconnected -> Connecting(attempt: 1)
    Connecting(attempt) if attempt < 3 -> Connecting(attempt: attempt + 1)
    Connecting(_) -> Disconnected
    Connected(_) -> state
    Disconnecting -> state
  }
}

// Expression tree ADT
pub type Expr {
  Number(Float)
  Add(left: Expr, right: Expr)
  Subtract(left: Expr, right: Expr)
  Multiply(left: Expr, right: Expr)
  Divide(left: Expr, right: Expr)
}

pub fn evaluate(expr: Expr) -> Result(Float, String) {
  case expr {
    Number(n) -> Ok(n)
    Add(left, right) -> {
      use l <- result.try(evaluate(left))
      use r <- result.try(evaluate(right))
      Ok(l +. r)
    }
    Subtract(left, right) -> {
      use l <- result.try(evaluate(left))
      use r <- result.try(evaluate(right))
      Ok(l -. r)
    }
    Multiply(left, right) -> {
      use l <- result.try(evaluate(left))
      use r <- result.try(evaluate(right))
      Ok(l *. r)
    }
    Divide(left, right) -> {
      use l <- result.try(evaluate(left))
      use r <- result.try(evaluate(right))
      case r {
        0.0 -> Error("Division by zero")
        _ -> Ok(l /. r)
      }
    }
  }
}
```

ADTs enable type-safe modeling of complex domain logic with compiler-verified
exhaustiveness.

## Pattern Matching

Pattern matching provides exhaustive, type-safe conditional logic with
destructuring capabilities.

```gleam
// Basic pattern matching
pub fn describe_number(n: Int) -> String {
  case n {
    0 -> "zero"
    1 -> "one"
    2 -> "two"
    _ -> "many"
  }
}

// Pattern matching with guards
pub fn classify_age(age: Int) -> String {
  case age {
    n if n < 0 -> "Invalid"
    n if n < 13 -> "Child"
    n if n < 20 -> "Teen"
    n if n < 65 -> "Adult"
    _ -> "Senior"
  }
}

// Destructuring tuples
pub fn swap(pair: #(a, b)) -> #(b, a) {
  let #(first, second) = pair
  #(second, first)
}

pub fn tuple_pattern(tuple: #(Int, String, Bool)) -> String {
  case tuple {
    #(0, _, _) -> "First is zero"
    #(_, "hello", _) -> "Second is hello"
    #(_, _, True) -> "Third is true"
    _ -> "Something else"
  }
}

// Destructuring custom types
pub fn greet_user(user: User) -> String {
  let User(name: name, age: age, email: _) = user
  "Hello " <> name <> ", you are " <> int.to_string(age)
}

pub fn is_circle(shape: Shape) -> Bool {
  case shape {
    Circle(_) -> True
    _ -> False
  }
}

// Nested pattern matching
pub type Nested {
  Outer(inner: Inner)
}

pub type Inner {
  Value(Int)
  Empty
}

pub fn extract_value(nested: Nested) -> Option(Int) {
  case nested {
    Outer(Value(n)) -> Some(n)
    Outer(Empty) -> None
  }
}

// List pattern matching
pub fn list_sum(list: List(Int)) -> Int {
  case list {
    [] -> 0
    [head] -> head
    [first, second] -> first + second
    [head, ..tail] -> head + list_sum(tail)
  }
}

pub fn list_head(list: List(a)) -> Option(a) {
  case list {
    [] -> None
    [head, ..] -> Some(head)
  }
}

// Multiple case expressions
pub fn compare_results(r1: Result(Int, String),
                       r2: Result(Int, String)) -> String {
  case r1, r2 {
    Ok(n1), Ok(n2) -> "Both ok: " <> int.to_string(n1 + n2)
    Ok(n), Error(_) -> "First ok: " <> int.to_string(n)
    Error(_), Ok(n) -> "Second ok: " <> int.to_string(n)
    Error(e1), Error(e2) -> "Both failed: " <> e1 <> ", " <> e2
  }
}

// Pattern matching with alternative patterns
pub fn is_weekend(day: String) -> Bool {
  case day {
    "Saturday" | "Sunday" -> True
    _ -> False
  }
}

// Matching on string patterns
pub fn parse_command(input: String) -> String {
  case string.lowercase(input) {
    "quit" | "exit" | "q" -> "Exiting..."
    "help" | "h" | "?" -> "Help message"
    _ -> "Unknown command"
  }
}

// Use expressions for result handling
pub fn divide_and_double(a: Int, b: Int) -> Result(Int, String) {
  use quotient <- result.try(case b {
    0 -> Error("Division by zero")
    _ -> Ok(a / b)
  })
  Ok(quotient * 2)
}

// Exhaustive matching on enums
pub fn status_code(status: Status) -> Int {
  case status {
    Pending -> 0
    Approved -> 1
    Rejected -> 2
  }
}
```

Pattern matching enables concise, exhaustive conditional logic with compile-time
verification.

## Generic Types and Polymorphism

Generic types enable writing reusable code that works with multiple types while
maintaining type safety.

```gleam
// Generic function
pub fn identity(value: a) -> a {
  value
}

pub fn const(a: a, b: b) -> a {
  a
}

// Generic data structure
pub type Pair(a, b) {
  Pair(first: a, second: b)
}

pub fn pair_map_first(pair: Pair(a, b), f: fn(a) -> c) -> Pair(c, b) {
  Pair(first: f(pair.first), second: pair.second)
}

pub fn pair_map_second(pair: Pair(a, b), f: fn(b) -> c) -> Pair(a, c) {
  Pair(first: pair.first, second: f(pair.second))
}

pub fn pair_swap(pair: Pair(a, b)) -> Pair(b, a) {
  Pair(first: pair.second, second: pair.first)
}

// Generic container
pub type Container(a) {
  Empty
  Full(value: a)
}

pub fn container_map(cont: Container(a), f: fn(a) -> b) -> Container(b) {
  case cont {
    Empty -> Empty
    Full(value) -> Full(f(value))
  }
}

pub fn container_unwrap_or(cont: Container(a), default: a) -> a {
  case cont {
    Empty -> default
    Full(value) -> value
  }
}

// Higher-order functions
pub fn map(list: List(a), f: fn(a) -> b) -> List(b) {
  case list {
    [] -> []
    [head, ..tail] -> [f(head), ..map(tail, f)]
  }
}

pub fn filter(list: List(a), predicate: fn(a) -> Bool) -> List(a) {
  case list {
    [] -> []
    [head, ..tail] -> case predicate(head) {
      True -> [head, ..filter(tail, predicate)]
      False -> filter(tail, predicate)
    }
  }
}

pub fn fold(list: List(a), initial: b, f: fn(b, a) -> b) -> b {
  case list {
    [] -> initial
    [head, ..tail] -> fold(tail, f(initial, head), f)
  }
}

// Generic Result operations
pub fn result_map(result: Result(a, e), f: fn(a) -> b) -> Result(b, e) {
  case result {
    Ok(value) -> Ok(f(value))
    Error(err) -> Error(err)
  }
}

pub fn result_map_error(result: Result(a, e), f: fn(e) -> f) -> Result(a, f) {
  case result {
    Ok(value) -> Ok(value)
    Error(err) -> Error(f(err))
  }
}

pub fn result_and_then(
  result: Result(a, e),
  f: fn(a) -> Result(b, e),
) -> Result(b, e) {
  case result {
    Ok(value) -> f(value)
    Error(err) -> Error(err)
  }
}

pub fn result_unwrap_or(result: Result(a, e), default: a) -> a {
  case result {
    Ok(value) -> value
    Error(_) -> default
  }
}

// Combining Results
pub fn result_all(results: List(Result(a, e))) -> Result(List(a), e) {
  case results {
    [] -> Ok([])
    [Ok(value), ..rest] -> {
      use tail <- result_and_then(result_all(rest))
      Ok([value, ..tail])
    }
    [Error(err), ..] -> Error(err)
  }
}

// Generic tree operations
pub fn tree_map(tree: Tree(a), f: fn(a) -> b) -> Tree(b) {
  case tree {
    Leaf(value) -> Leaf(f(value))
    Branch(left, right) -> Branch(tree_map(left, f), tree_map(right, f))
  }
}

pub fn tree_fold(tree: Tree(a), initial: b, f: fn(b, a) -> b) -> b {
  case tree {
    Leaf(value) -> f(initial, value)
    Branch(left, right) -> {
      let left_result = tree_fold(left, initial, f)
      tree_fold(right, left_result, f)
    }
  }
}

// Functor pattern
pub fn functor_compose(
  fa: Container(a),
  f: fn(a) -> b,
  g: fn(b) -> c,
) -> Container(c) {
  container_map(container_map(fa, f), g)
}
```

Generic types enable writing reusable, type-safe abstractions that work across
different concrete types.

## Type Aliases and Opaque Types

Type aliases create readable names for complex types, while opaque types hide
implementation details.

```gleam
// Type aliases
pub type UserId = Int
pub type Email = String
pub type Age = Int

pub type UserData = #(UserId, String, Email, Age)

pub fn create_user_data(id: UserId, name: String, email: Email, age: Age) ->
  UserData {
  #(id, name, email, age)
}

// Function type aliases
pub type Validator(a) = fn(a) -> Result(a, String)
pub type Transformer(a, b) = fn(a) -> b

pub fn validate_age(age: Age) -> Result(Age, String) {
  case age >= 0 && age <= 150 {
    True -> Ok(age)
    False -> Error("Invalid age")
  }
}

// Collection type aliases
pub type StringList = List(String)
pub type IntResult = Result(Int, String)
pub type UserMap = Dict(UserId, User)

// Opaque types (hide internal representation)
pub opaque type Password {
  Password(hash: String)
}

pub fn create_password(plain: String) -> Password {
  // Hash password (simplified)
  Password(hash: hash_string(plain))
}

pub fn verify_password(password: Password, plain: String) -> Bool {
  let Password(hash: stored_hash) = password
  stored_hash == hash_string(plain)
}

fn hash_string(s: String) -> String {
  // Implementation hidden
  s <> "_hashed"
}

// Opaque type for validated data
pub opaque type ValidatedEmail {
  ValidatedEmail(value: String)
}

pub fn validate_and_create_email(value: String) ->
  Result(ValidatedEmail, String) {
  case string.contains(value, "@") {
    True -> Ok(ValidatedEmail(value: value))
    False -> Error("Invalid email format")
  }
}

pub fn email_to_string(email: ValidatedEmail) -> String {
  let ValidatedEmail(value: value) = email
  value
}

// Opaque type for units
pub opaque type Meters {
  Meters(Float)
}

pub opaque type Feet {
  Feet(Float)
}

pub fn meters(value: Float) -> Meters {
  Meters(value)
}

pub fn feet(value: Float) -> Feet {
  Feet(value)
}

pub fn meters_to_feet(m: Meters) -> Feet {
  let Meters(value) = m
  Feet(value *. 3.28084)
}

pub fn feet_to_meters(f: Feet) -> Meters {
  let Feet(value) = f
  Meters(value /. 3.28084)
}

// Opaque type for IDs
pub opaque type OrderId {
  OrderId(Int)
}

pub fn new_order_id(id: Int) -> OrderId {
  OrderId(id)
}

pub fn order_id_to_int(id: OrderId) -> Int {
  let OrderId(value) = id
  value
}

// Builder pattern with opaque types
pub opaque type Query {
  Query(table: String, conditions: List(String), limit: Option(Int))
}

pub fn new_query(table: String) -> Query {
  Query(table: table, conditions: [], limit: None)
}

pub fn where(query: Query, condition: String) -> Query {
  let Query(table: table, conditions: conditions, limit: limit) = query
  Query(table: table, conditions: [condition, ..conditions], limit: limit)
}

pub fn limit(query: Query, n: Int) -> Query {
  let Query(table: table, conditions: conditions, limit: _) = query
  Query(table: table, conditions: conditions, limit: Some(n))
}

pub fn to_sql(query: Query) -> String {
  let Query(table: table, conditions: conditions, limit: limit) = query
  let where_clause = case conditions {
    [] -> ""
    _ -> " WHERE " <> string.join(conditions, " AND ")
  }
  let limit_clause = case limit {
    None -> ""
    Some(n) -> " LIMIT " <> int.to_string(n)
  }
  "SELECT * FROM " <> table <> where_clause <> limit_clause
}
```

Type aliases improve readability while opaque types enforce invariants and hide
implementation details.

## Best Practices

1. **Use custom types for domain modeling** to make invalid states
   unrepresentable at compile time

2. **Leverage pattern matching exhaustiveness** to ensure all cases are handled
   without runtime checks

3. **Prefer Result over exceptions** for expected errors to make error handling
   explicit

4. **Use opaque types for validation** to prevent creating invalid values outside
   the module

5. **Apply generic types** when algorithms work across multiple types to maximize
   code reuse

6. **Use type aliases** for complex types to improve readability and
   maintainability

7. **Pattern match on specific variants** rather than using catch-all patterns
   for safety

8. **Use phantom types** for compile-time state tracking in state machines or
   workflows

9. **Avoid nested Results** by using result.try or use expressions for cleaner
   error handling

10. **Document opaque type invariants** to clarify constraints enforced by the
    abstraction

## Common Pitfalls

1. **Overusing generic types** adds complexity without benefits when specific
   types suffice

2. **Not using opaque types** exposes internal representation and breaks
   encapsulation

3. **Ignoring compiler warnings** about non-exhaustive patterns leads to runtime
   crashes

4. **Creating redundant type aliases** for simple types reduces clarity

5. **Not validating at boundaries** when using opaque types allows invalid data
   creation

6. **Using underscore in patterns** excessively misses valuable destructuring
   opportunities

7. **Nesting too many Results** creates callback-like complexity; use use
   expressions

8. **Not using guards in patterns** when conditions are needed causes verbose
   case expressions

9. **Creating overly complex ADTs** with too many variants reduces
   maintainability

10. **Forgetting type annotations** on public functions reduces documentation
    clarity

## When to Use This Skill

Apply custom types when modeling domain entities with specific fields and
behaviors.

Use ADTs when data can exist in multiple states or variants with different
properties.

Leverage pattern matching for all conditional logic requiring destructuring or
exhaustiveness.

Apply generic types when implementing reusable algorithms or data structures.

Use opaque types when enforcing invariants or hiding implementation details from
module users.

Employ Result types for all operations that can fail to make error handling
explicit.

## Resources

- [Gleam Language Tour](<https://tour.gleam.run/>)
- [Gleam Documentation](<https://gleam.run/documentation/>)
- [Gleam Standard Library](<https://hexdocs.pm/gleam_stdlib/>)
- [Gleam Book](<https://gleam.run/book/>)
- [Awesome Gleam](<https://github.com/gleam-lang/awesome-gleam>)
