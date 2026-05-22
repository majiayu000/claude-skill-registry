---
name: convert-scala-roc
description: Convert Scala code to idiomatic Roc. Use when migrating Scala projects to Roc, translating JVM/FP patterns to pure functional patterns, or refactoring Scala codebases. Extends meta-convert-dev with Scala-to-Roc specific patterns.
---

# Convert Scala to Roc

Convert Scala code to idiomatic Roc. This skill extends `meta-convert-dev` with Scala-to-Roc specific type mappings, idiom translations, and architectural patterns for moving from JVM-based functional programming to platform-based pure functional programming.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Scala JVM types → Roc static types
- **Paradigm translation**: Object-functional hybrid → Pure functional with platform separation
- **Idiom translations**: Scala patterns → Roc functional patterns
- **Error handling**: Exceptions + Try/Either → Result types
- **Concurrency**: Futures/Actors → Platform Tasks
- **Module system**: Scala packages/objects → Roc platform/application architecture
- **Type classes**: Scala implicits/given → Roc abilities

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Scala language fundamentals - see `lang-scala-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → Scala) - see `convert-roc-scala`

---

## Quick Reference

| Scala | Roc | Notes |
|-------|-----|-------|
| `Int` | `I64` / `I32` | Specify bit width |
| `Long` | `I64` | 64-bit signed |
| `Double` | `F64` | 64-bit float |
| `Boolean` | `Bool` | Direct mapping |
| `String` | `Str` | UTF-8 strings |
| `Option[A]` | `[Some A, None]` | Tag union |
| `Either[L, R]` | `Result R L` | Note: order swapped |
| `Try[A]` | `Result A [Err Str]` | Exception → error tag |
| `List[A]` | `List A` | Immutable list |
| `Vector[A]` | `List A` | Roc List is efficient |
| `Set[A]` | `Set A` | Unique values |
| `Map[K, V]` | `Dict K V` | Key-value map |
| `case class` | Record `{ }` | Structural records |
| `sealed trait` | Tag union `[]` | Sum types |
| `trait` (interface) | Ability | Type class pattern |
| `Future[A]` | `Task A err` | Platform-provided |
| `Unit` | `{}` | Empty record |

## When Converting Code

1. **Analyze JVM semantics** before writing Roc
2. **Identify effect boundaries** - separate pure logic from I/O
3. **Map object hierarchies to data** - classes become records, inheritance becomes composition
4. **Redesign for immutability** - Scala's var becomes Roc's pure transformation
5. **Extract pure functions** - separate computation from effects
6. **Test equivalence** - verify behavior matches despite architectural differences

---

## Paradigm Translation

### Mental Model Shift: Object-Functional → Pure Functional + Platform

| Scala Concept | Roc Approach | Key Insight |
|---------------|--------------|-------------|
| Class with state | Record + functions operating on record | Data and behavior separated, no hidden state |
| Inheritance | Composition with records | Favor records and tag unions over class hierarchies |
| var (mutation) | New value creation | Explicit transformation, not mutation |
| Companion object | Module with functions | Namespace for related functions |
| Implicit parameter | Ability constraint | Type class pattern via abilities |
| Future | Platform Task | Effects are platform capability |
| Actor | Platform concern | Concurrency handled by host |
| Singleton object | Module-level constants | Global state avoided, use module scope |
| Trait mixing | Record composition | Combine records, not behaviors |

### Functional Paradigm Alignment

| Scala Pattern | Roc Pattern | Conceptual Translation |
|---------------|-------------|------------------------|
| `for` comprehension | Pipeline `\|>` or nested `when` | Monadic composition becomes explicit |
| Pattern matching | `when` expression | Similar syntax, structural matching |
| Case class | Record type | Structural types, automatic equality |
| Sealed trait ADT | Tag union | Sum types with exhaustiveness |
| Implicit conversion | No equivalent | Explicit conversions preferred |
| Higher-order function | Function types | Direct support, same concept |

---

## Type System Mapping

### Primitive Types

| Scala | Roc | Notes |
|-------|-----|-------|
| `Byte` | `I8` | 8-bit signed |
| `Short` | `I16` | 16-bit signed |
| `Int` | `I32` | 32-bit signed (common) |
| `Long` | `I64` | 64-bit signed |
| `Float` | `F32` | 32-bit float |
| `Double` | `F64` | 64-bit float |
| `Boolean` | `Bool` | Direct mapping |
| `Char` | `U32` | Unicode scalar value |
| `String` | `Str` | UTF-8 strings |
| `Unit` | `{}` | Empty record |
| `Nothing` | - | No direct equivalent |
| `Any` | - | Avoid; use tag unions |
| `AnyVal` | - | Not needed in Roc |
| `AnyRef` | - | No reference types |

### Collection Types

| Scala | Roc | Notes |
|-------|-----|-------|
| `List[A]` | `List A` | Immutable, efficient |
| `Vector[A]` | `List A` | Roc List performs well |
| `Array[A]` | `List A` | No mutable arrays |
| `Set[A]` | `Set A` | Unique values |
| `Map[K, V]` | `Dict K V` | Hash + Eq required for K |
| `Seq[A]` | `List A` | General sequence → List |
| `IndexedSeq[A]` | `List A` | Use List for indexing |
| `LazyList[A]` | Generator pattern | Lazy evaluation via functions |
| `Option[A]` | `[Some A, None]` | Optional values |
| `Either[L, R]` | `Result R L` | **Note: order reversed** |
| `Try[A]` | `Result A [Err Str]` | Exception handling |

### Composite Types

| Scala | Roc | Notes |
|-------|-----|-------|
| `case class User(...)` | `User : { name : Str, ... }` | Records are structural |
| `sealed trait Color` | `Color : [Red, Green, Blue]` | Sum types (ADTs) |
| `trait Service` | Ability or module | Depends on use case |
| `object Utils` | `interface Utils` | Module with functions |
| `(A, B)` | `(A, B)` | Tuples map directly |
| `(A, B, C)` | `(A, B, C)` | Multi-element tuples |
| Generics `[A]` | Type parameters `a` | Similar concept |
| Variance `[+A]` | - | Roc doesn't need variance |

### Function Types

| Scala | Roc | Notes |
|-------|-----|-------|
| `() => R` | `{} -> R` | Zero-arg function |
| `A => R` | `A -> R` | Single arg |
| `(A, B) => R` | `A, B -> R` | Multiple args |
| `Function1[A, B]` | `A -> B` | Function type |
| `A => B => C` | `A -> (B -> C)` | Curried functions |
| By-name `=> A` | `{} -> A` | Lazy evaluation |

---

## Idiom Translation

### Pattern 1: Simple Function and Case Class

**Scala:**
```scala
case class User(name: String, age: Int, email: String)

object User {
  def create(name: String, age: Int, email: String): User = {
    User(name, age, email)
  }

  def greet(user: User): String = {
    s"Hello, ${user.name}! You are ${user.age} years old."
  }
}
```

**Roc:**
```roc
interface User
    exposes [User, create, greet]
    imports []

User : {
    name : Str,
    age : U32,
    email : Str,
}

create : Str, U32, Str -> User
create = \name, age, email ->
    { name, age, email }

greet : User -> Str
greet = \{ name, age } ->
    "Hello, \(name)! You are \(Num.toStr(age)) years old."
```

**Why this translation:**
- Scala case class → Roc record type
- Companion object → Roc interface (module)
- String interpolation syntax differs
- Type inference works in both

### Pattern 2: Sealed Trait ADT with Pattern Matching

**Scala:**
```scala
sealed trait Result[+A]
case class Success[A](value: A) extends Result[A]
case class Failure(error: String) extends Result[Nothing]
case object Pending extends Result[Nothing]

def handle[A](result: Result[A]): String = result match {
  case Success(value) => s"Got: $value"
  case Failure(error) => s"Error: $error"
  case Pending => "Waiting..."
}
```

**Roc:**
```roc
Result a : [Success a, Failure Str, Pending]

handle : Result a -> Str where a implements Inspect
handle = \result ->
    when result is
        Success(value) -> "Got: \(Inspect.toStr(value))"
        Failure(error) -> "Error: \(error)"
        Pending -> "Waiting..."
```

**Why this translation:**
- Sealed trait → Tag union
- Case classes → Tags with payloads
- Case object → Tag without payload
- Pattern matching syntax very similar
- Roc enforces exhaustiveness at compile time

### Pattern 3: Option Handling

**Scala:**
```scala
def findUser(id: Int, users: List[User]): Option[User] = {
  users.find(_.id == id)
}

def getEmail(maybeUser: Option[User]): String = {
  maybeUser.map(_.email).getOrElse("no email")
}

// For-comprehension
def combineUsers(id1: Int, id2: Int): Option[(User, User)] = {
  for {
    user1 <- findUser(id1, users)
    user2 <- findUser(id2, users)
  } yield (user1, user2)
}
```

**Roc:**
```roc
findUser : U64, List User -> [Some User, None]
findUser = \id, users ->
    users
    |> List.findFirst(\user -> user.id == id)
    |> Result.map(Some)
    |> Result.withDefault(None)

getEmail : [Some User, None] -> Str
getEmail = \maybeUser ->
    when maybeUser is
        Some({ email }) -> email
        None -> "no email"

# Nested when for comprehension-like flow
combineUsers : U64, U64, List User -> [Some (User, User), None]
combineUsers = \id1, id2, users ->
    when findUser(id1, users) is
        Some(user1) ->
            when findUser(id2, users) is
                Some(user2) -> Some((user1, user2))
                None -> None
        None -> None
```

**Why this translation:**
- Scala Option → Roc tag union `[Some a, None]`
- `map`/`getOrElse` → pattern matching or Result helpers
- For-comprehension → nested `when` expressions
- More verbose but explicit

### Pattern 4: List Processing

**Scala:**
```scala
val numbers = List(1, 2, 3, 4, 5)

val doubled = numbers.map(_ * 2)
val evens = numbers.filter(_ % 2 == 0)
val sum = numbers.foldLeft(0)(_ + _)

// List comprehension
val squares = for {
  x <- numbers
  if x % 2 == 0
} yield x * x
```

**Roc:**
```roc
numbers = [1, 2, 3, 4, 5]

doubled = List.map(numbers, \n -> n * 2)
evens = List.keepIf(numbers, \n -> n % 2 == 0)
sum = List.walk(numbers, 0, Num.add)

# List comprehension becomes pipeline
squares = numbers
    |> List.keepIf(\x -> x % 2 == 0)
    |> List.map(\x -> x * x)
```

**Why this translation:**
- Similar higher-order functions
- `foldLeft` → `List.walk`
- `filter` → `List.keepIf`
- For-comprehension → pipeline with map/filter
- Roc uses explicit function composition

### Pattern 5: Error Handling with Either/Try

**Scala:**
```scala
def divide(a: Int, b: Int): Either[String, Int] = {
  if (b == 0) Left("Division by zero")
  else Right(a / b)
}

def calculate(a: Int, b: Int, c: Int): Either[String, Int] = {
  for {
    x <- divide(a, b)
    y <- divide(x, c)
  } yield y
}

// Try for exceptions
import scala.util.{Try, Success, Failure}

def parseInt(s: String): Try[Int] = Try(s.toInt)

def safeParse(s: String): Option[Int] = parseInt(s).toOption
```

**Roc:**
```roc
divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)
    y = divide!(x, c)
    Ok(y)

# Try equivalent
parseInt : Str -> Result I64 [ParseError]
parseInt = \s ->
    when Str.toI64(s) is
        Ok(n) -> Ok(n)
        Err(_) -> Err(ParseError)

safeParse : Str -> [Some I64, None]
safeParse = \s ->
    when parseInt(s) is
        Ok(n) -> Some(n)
        Err(_) -> None
```

**Why this translation:**
- `Either[L, R]` → `Result ok err` (note: order reversed)
- For-comprehension → try operator `!` for early returns
- `Try` → `Result` with explicit error types
- `toOption` → pattern matching to convert Result → Option-like tag union

### Pattern 6: Trait and Implicits to Abilities

**Scala:**
```scala
trait Show[A] {
  def show(a: A): String
}

object Show {
  implicit val intShow: Show[Int] = (a: Int) => a.toString
  implicit val stringShow: Show[String] = (a: String) => s"'$a'"
}

def print[A](a: A)(implicit s: Show[A]): Unit = {
  println(s.show(a))
}

print(42)      // Uses intShow
print("hello") // Uses stringShow
```

**Roc:**
```roc
# Roc abilities are automatic for basic types
# For custom behavior, use functions with ability constraints

toString : a -> Str where a implements Inspect
toString = \value ->
    Inspect.toStr(value)

# Usage - Inspect is automatically implemented
expect toString(42) == "42"
expect toString("hello") == "\"hello\""

# For custom types, abilities are derived automatically
User : { name : Str, age : U32 }
user = { name: "Alice", age: 30 }

expect Inspect.toStr(user) == "{ name: \"Alice\", age: 30 }"
```

**Why this translation:**
- Scala trait → Roc ability
- Implicit instances → automatic derivation for records/tags
- Type class pattern → ability constraint `where a implements Ability`
- Roc has fewer built-in abilities but they're more automatic

### Pattern 7: Higher-Order Functions and Currying

**Scala:**
```scala
def applyTwice[A](f: A => A, x: A): A = f(f(x))

def add(a: Int)(b: Int): Int = a + b
val add5 = add(5) _

def compose[A, B, C](f: B => C, g: A => B): A => C = {
  a => f(g(a))
}
```

**Roc:**
```roc
applyTwice : (a -> a), a -> a
applyTwice = \f, x ->
    f(f(x))

# Currying in Roc requires explicit function return
add : I64 -> (I64 -> I64)
add = \a ->
    \b -> a + b

add5 = add(5)

compose : (b -> c), (a -> b) -> (a -> c)
compose = \f, g ->
    \a -> f(g(a))
```

**Why this translation:**
- Higher-order functions work similarly
- Currying must be explicit in Roc (return a function)
- Function composition same concept
- Type signatures use arrows consistently

### Pattern 8: Records with Update

**Scala:**
```scala
case class Config(
  host: String,
  port: Int,
  timeout: Int = 5000,
  retries: Int = 3
)

val config = Config("localhost", 8080)
val updated = config.copy(port = 9090, retries = 5)
```

**Roc:**
```roc
Config : {
    host : Str,
    port : U16,
    timeout : U32,
    retries : U32,
}

defaultConfig : Str, U16 -> Config
defaultConfig = \host, port ->
    {
        host,
        port,
        timeout: 5000,
        retries: 3,
    }

config = defaultConfig("localhost", 8080)
updated = { config &
    port: 9090,
    retries: 5,
}
```

**Why this translation:**
- Case class `copy` → Roc record update `{ record & field: value }`
- Default parameters → constructor function with defaults
- Immutable updates work similarly
- Roc update syntax is explicit

---

## Concurrency Patterns

### Scala Future vs Roc Task

Scala uses Futures for async computation on the JVM. Roc delegates all concurrency to the platform.

**Scala:**
```scala
import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global

def fetchUser(id: Int): Future[User] = Future {
  // Async operation
  database.query(s"SELECT * FROM users WHERE id = $id")
}

def fetchPosts(userId: Int): Future[List[Post]] = Future {
  database.query(s"SELECT * FROM posts WHERE author = $userId")
}

// Composition
val result: Future[(User, List[Post])] = for {
  user <- fetchUser(123)
  posts <- fetchPosts(user.id)
} yield (user, posts)

// Parallel execution
val users: Future[List[User]] = Future.sequence(
  List(1, 2, 3).map(fetchUser)
)
```

**Roc:**
```roc
import pf.Task exposing [Task]
import pf.Database

# Platform provides Task type
fetchUser : U64 -> Task User [DbErr]
fetchUser = \id ->
    Database.query!("SELECT * FROM users WHERE id = \(Num.toStr(id))")

fetchPosts : U64 -> Task (List Post) [DbErr]
fetchPosts = \userId ->
    Database.query!("SELECT * FROM posts WHERE author = \(Num.toStr(userId))")

# Sequential composition using !
result : Task (User, List Post) [DbErr]
result =
    user = fetchUser!(123)
    posts = fetchPosts!(user.id)
    Task.ok((user, posts))

# Platform provides parallel primitives
users : Task (List User) [DbErr]
users =
    Task.sequence([
        fetchUser(1),
        fetchUser(2),
        fetchUser(3),
    ])
```

**Why this translation:**
- Scala Future → Roc platform Task
- For-comprehension → try operator `!` with Task
- ExecutionContext → handled by platform
- Parallel execution → platform-provided primitives
- Roc apps stay pure, platform handles concurrency

### Scala Actors (Akka) vs Roc Platform

**Scala (Akka Typed):**
```scala
import akka.actor.typed._
import akka.actor.typed.scaladsl.Behaviors

sealed trait CounterMsg
case object Increment extends CounterMsg
case class GetCount(replyTo: ActorRef[Int]) extends CounterMsg

def counter(count: Int): Behavior[CounterMsg] =
  Behaviors.receive { (context, message) =>
    message match {
      case Increment =>
        counter(count + 1)
      case GetCount(replyTo) =>
        replyTo ! count
        Behaviors.same
    }
  }
```

**Roc:**
```roc
# Roc has no built-in actors
# Design as pure state machine

State : I64

init : State
init = 0

increment : State -> State
increment = \count ->
    count + 1

getCount : State -> I64
getCount = \count ->
    count

# Platform would provide state management if needed
# Application code remains pure
```

**Why this translation:**
- Actors → pure state functions
- Message passing → function parameters
- State mutation → new state returned
- Platform handles concurrency, not application
- Simpler mental model: data transformation, not processes

---

## Module System Translation

### Scala Package/Object → Roc Interface

**Scala:**
```scala
package com.example.users

case class User(id: Int, name: String, email: String)

object UserService {
  def create(name: String, email: String): User = {
    val id = generateId()
    User(id, name, email)
  }

  def validate(user: User): Either[String, User] = {
    if (user.email.contains("@")) Right(user)
    else Left("Invalid email")
  }
}
```

**Roc:**
```roc
interface UserService
    exposes [User, create, validate]
    imports []

User : {
    id : U64,
    name : Str,
    email : Str,
}

create : Str, Str -> User
create = \name, email ->
    id = generateId({})
    { id, name, email }

validate : User -> Result User [InvalidEmail]
validate = \user ->
    if Str.contains(user.email, "@") then
        Ok(user)
    else
        Err(InvalidEmail)

# Private helper (not in exposes)
generateId : {} -> U64
generateId = \{} ->
    # Implementation
    123
```

**Why this translation:**
- Package → Roc module structure (file organization)
- Companion object → Interface exposing functions
- Private members → not in `exposes` list
- Public API → explicitly listed in `exposes`

---

## Common Pitfalls

### 1. Trying to Use Mutable State

**Scala (Anti-pattern in Roc):**
```scala
var counter = 0
def increment(): Unit = { counter += 1 }
```

**Roc Approach:**
```roc
# No mutable state - return new value
increment : I64 -> I64
increment = \counter ->
    counter + 1

# Usage
counter = 0
newCounter = increment(counter)
```

**Why:** Roc has no mutable variables. Always return new values.

### 2. Expecting JVM Collections Performance Characteristics

**Pitfall:** Assuming Scala Vector performance in Roc.

**Solution:** Roc List is the primary collection. It's efficient for most use cases. Don't over-optimize based on JVM knowledge.

### 3. Trying to Use Null

**Scala:**
```scala
var maybeUser: User = null  // Avoid!
val user: Option[User] = Option(nullableValue)
```

**Roc:**
```roc
# No null! Use tag unions
maybeUser : [Some User, None]
maybeUser = None

# When converting from nullable source
userFromNullable : [Some User, None]
userFromNullable = Some({ name: "Alice", age: 30 })
```

**Why:** Roc has no null. Always use tag unions for optional values.

### 4. Confusing Either Order

**Pitfall:** Scala `Either[L, R]` vs Roc `Result ok err`

**Scala:**
```scala
val result: Either[String, Int] = Right(42)  // Right is success
```

**Roc:**
```roc
result : Result I64 Str  # First param is success, second is error
result = Ok(42)
```

**Why:** Roc Result has opposite parameter order compared to Scala Either.

### 5. Expecting Implicit Conversions

**Pitfall:** Scala's implicit conversions don't exist in Roc.

**Solution:** All conversions must be explicit:
```roc
# Explicit conversion required
intToStr : I64 -> Str
intToStr = Num.toStr

str = intToStr(42)
```

### 6. Forgetting Platform Separation

**Pitfall:** Trying to do I/O directly in application code.

**Solution:** Use platform-provided Tasks:
```roc
# Wrong - no direct I/O
# readFile("path")  # This doesn't exist!

# Correct - platform Task
import pf.File
import pf.Task exposing [Task]

readFile : Str -> Task Str [FileErr]
readFile = \path ->
    File.readUtf8(path)
```

**Why:** Roc applications are pure. All effects go through the platform.

---

## Tooling

| Purpose | Scala | Roc | Notes |
|---------|-------|-----|-------|
| **Build tool** | sbt, Mill, Maven | `roc` CLI | Roc has built-in build |
| **Package manager** | sbt, Maven | Platform dependencies | Platforms are URLs |
| **Testing** | ScalaTest, MUnit | `roc test` | Inline `expect` statements |
| **REPL** | `scala` REPL | `roc repl` | Interactive evaluation |
| **Formatter** | Scalafmt | `roc format` | Built-in formatter |
| **Type checking** | scalac | `roc check` | Fast type checking |
| **Documentation** | Scaladoc | Comments in code | Markdown in interfaces |

---

## Examples

### Example 1: Simple HTTP Client

**Scala (Akka HTTP):**
```scala
import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model._
import scala.concurrent.Future

implicit val system = ActorSystem()
import system.dispatcher

def fetchUrl(url: String): Future[String] = {
  Http().singleRequest(HttpRequest(uri = url)).flatMap { response =>
    response.entity.toStrict(5.seconds).map(_.data.utf8String)
  }
}

val content: Future[String] = fetchUrl("https://example.com")
```

**Roc (basic-cli platform):**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.Http
import pf.Task exposing [Task]
import pf.Stdout

fetchUrl : Str -> Task Str [HttpErr]
fetchUrl = \url ->
    response = Http.get!(url)
    Task.ok(response.body)

main : Task {} []
main =
    content = fetchUrl!("https://example.com")
    Stdout.line!(content)
```

### Example 2: Data Processing Pipeline

**Scala:**
```scala
case class User(id: Int, name: String, age: Int, active: Boolean)

val users = List(
  User(1, "Alice", 30, true),
  User(2, "Bob", 25, false),
  User(3, "Charlie", 35, true)
)

val activeUserNames = users
  .filter(_.active)
  .filter(_.age >= 30)
  .map(_.name)
  .sorted

// Result: List("Alice", "Charlie")
```

**Roc:**
```roc
User : { id : U64, name : Str, age : U32, active : Bool }

users = [
    { id: 1, name: "Alice", age: 30, active: Bool.true },
    { id: 2, name: "Bob", age: 25, active: Bool.false },
    { id: 3, name: "Charlie", age: 35, active: Bool.true },
]

activeUserNames = users
    |> List.keepIf(\user -> user.active)
    |> List.keepIf(\user -> user.age >= 30)
    |> List.map(\user -> user.name)
    |> List.sortAsc

# Result: ["Alice", "Charlie"]
```

### Example 3: Error Handling Pipeline

**Scala:**
```scala
def parseAndDivide(aStr: String, bStr: String): Either[String, Int] = {
  for {
    a <- aStr.toIntOption.toRight(s"Invalid a: $aStr")
    b <- bStr.toIntOption.toRight(s"Invalid b: $bStr")
    result <- if (b != 0) Right(a / b) else Left("Division by zero")
  } yield result
}

parseAndDivide("10", "2")  // Right(5)
parseAndDivide("10", "0")  // Left("Division by zero")
parseAndDivide("abc", "2") // Left("Invalid a: abc")
```

**Roc:**
```roc
parseAndDivide : Str, Str -> Result I64 [InvalidA, InvalidB, DivByZero]
parseAndDivide = \aStr, bStr ->
    a =
        when Str.toI64(aStr) is
            Ok(n) -> Ok(n)
            Err(_) -> Err(InvalidA)

    b =
        when Str.toI64(bStr) is
            Ok(n) -> Ok(n)
            Err(_) -> Err(InvalidB)

    # Using try operator for early returns
    aVal = a!
    bVal = b!

    if bVal == 0 then
        Err(DivByZero)
    else
        Ok(aVal // bVal)

expect parseAndDivide("10", "2") == Ok(5)
expect parseAndDivide("10", "0") == Err(DivByZero)
expect parseAndDivide("abc", "2") == Err(InvalidA)
```

---

## Performance Considerations

### Scala vs Roc Performance Differences

| Aspect | Scala | Roc | Impact |
|--------|-------|-----|--------|
| **Runtime** | JVM (GC, JIT) | Native compilation | Roc generally faster startup, lower memory |
| **Collections** | Optimized for JVM | Native data structures | Different performance characteristics |
| **Concurrency** | Thread pool, async | Platform-managed | Depends on platform implementation |
| **Memory** | Heap-based, GC | Platform-managed | Lower overhead in Roc |
| **Startup** | JVM warmup time | Instant | Roc has no warmup period |

### Optimization Tips

1. **Don't over-optimize based on JVM knowledge** - Roc's performance profile is different
2. **Trust List performance** - It's the primary collection and is well-optimized
3. **Leverage platform capabilities** - Let platform handle concurrency and I/O
4. **Profile before optimizing** - Different bottlenecks than JVM code
5. **Avoid premature abstraction** - Roc encourages simple, direct code

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-scala-dev` - Scala development patterns
- `lang-roc-dev` - Roc development patterns
- `convert-erlang-roc` - Similar functional language conversion (BEAM → Roc)

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Futures/Actors vs Tasks across languages
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Implicits vs abilities vs other approaches
