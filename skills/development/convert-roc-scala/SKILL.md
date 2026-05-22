---
name: convert-roc-scala
description: Convert Roc code to idiomatic Scala. Use when migrating Roc projects to JVM/Scala, translating pure functional patterns to object-functional hybrid, or refactoring Roc codebases. Extends meta-convert-dev with Roc-to-Scala specific patterns.
---

# Convert Roc to Scala

Convert Roc code to idiomatic Scala. This skill extends `meta-convert-dev` with Roc-to-Scala specific type mappings, idiom translations, and architectural patterns for moving from platform-based pure functional programming to JVM-based object-functional hybrid programming.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Roc static types → Scala JVM types
- **Paradigm translation**: Pure functional with platform separation → Object-functional hybrid
- **Idiom translations**: Roc functional patterns → Scala patterns
- **Error handling**: Result types → Either/Try/Exceptions
- **Concurrency**: Platform Tasks → Futures/Actors
- **Module system**: Roc platform/application architecture → Scala packages/objects
- **Type classes**: Roc abilities → Scala implicits/type classes

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Scala language fundamentals - see `lang-scala-dev`
- Reverse conversion (Scala → Roc) - see `convert-scala-roc`

---

## Quick Reference

| Roc | Scala | Notes |
|-----|-------|-------|
| `I64` / `I32` | `Long` / `Int` | Specify bit width becomes JVM types |
| `F64` | `Double` | 64-bit float |
| `Bool` | `Boolean` | Direct mapping |
| `Str` | `String` | UTF-8 → UTF-16 (JVM) |
| `[Some A, None]` | `Option[A]` | Tag union → built-in type |
| `Result R L` | `Either[L, R]` | **Note: order matches** |
| `List A` | `List[A]` or `Vector[A]` | Immutable lists |
| `Set A` | `Set[A]` | Unique values |
| `Dict K V` | `Map[K, V]` | Key-value map |
| Record `{ }` | `case class` | Records → case classes |
| Tag union `[]` | `sealed trait` | Sum types |
| Ability | `trait` (type class) | Type class pattern |
| `Task A err` | `Future[A]` | Platform-provided → JVM concurrency |
| `{}` | `Unit` | Empty record |

## When Converting Code

1. **Analyze platform boundaries** before writing Scala
2. **Identify effect implementations** - convert platform capabilities to libraries
3. **Map data structures to objects** - records become case classes, consider state encapsulation
4. **Design for mutability options** - Roc's pure transformations can become Scala vars if needed
5. **Choose concurrency model** - Tasks become Futures, Akka actors, or effect systems
6. **Test equivalence** - verify behavior matches despite runtime differences

---

## Paradigm Translation

### Mental Model Shift: Pure Functional + Platform → Object-Functional Hybrid

| Roc Concept | Scala Approach | Key Insight |
|-------------|----------------|-------------|
| Record + functions | Case class with methods or separate functions | Can choose data+methods or data+functions |
| Tag unions | Sealed traits + case classes | Similar concept, class hierarchy |
| Pure transformation | val or var | Can choose immutability or mutation |
| Module-level functions | Object with methods | Companion objects as modules |
| Ability constraint | Implicit parameter or type class | Similar type class pattern |
| Platform Task | Future, IO, ZIO | Choose effect system |
| Platform capability | Library import | What was platform becomes library |
| Module scope | Package object or companion | Namespace organization |
| Record composition | Trait mixing or composition | Multiple composition strategies |

### Functional Paradigm Alignment

| Roc Pattern | Scala Pattern | Conceptual Translation |
|-------------|---------------|------------------------|
| Pipeline `\|>` | Method chaining or `andThen` | Reversed order possible |
| `when` expression | Pattern matching `match` | Very similar syntax |
| Record type | Case class | Nominal types with structural similarity |
| Tag union | Sealed trait ADT | Direct correspondence |
| No conversion | Explicit conversion or implicits | Conversion becomes explicit or automatic |
| Function types | Function types with sugar | Direct support with different syntax |

---

## Type System Mapping

### Primitive Types

| Roc | Scala | Notes |
|-----|-------|-------|
| `I8` | `Byte` | 8-bit signed |
| `I16` | `Short` | 16-bit signed |
| `I32` | `Int` | 32-bit signed (common) |
| `I64` | `Long` | 64-bit signed |
| `F32` | `Float` | 32-bit float |
| `F64` | `Double` | 64-bit float |
| `Bool` | `Boolean` | Direct mapping |
| `U32` | `Int` (careful with sign) | No unsigned in Scala 2, consider `Long` |
| `Str` | `String` | UTF-8 → UTF-16 |
| `{}` | `Unit` | Empty record |
| - | `Any` | No direct equivalent in Roc |
| - | `Nothing` | No direct equivalent in Roc |

### Collection Types

| Roc | Scala | Notes |
|-----|-------|-------|
| `List A` | `List[A]` | Immutable, efficient prepend |
| `List A` | `Vector[A]` | For random access, use Vector |
| `Set A` | `Set[A]` | Unique values |
| `Dict K V` | `Map[K, V]` | Key-value mapping |
| Generator pattern | `LazyList[A]` or `Iterator[A]` | Lazy evaluation |
| `[Some A, None]` | `Option[A]` | Optional values |
| `Result R L` | `Either[L, R]` | **Order matches** |

### Composite Types

| Roc | Scala | Notes |
|-----|-------|-------|
| `User : { name : Str, ... }` | `case class User(name: String, ...)` | Records → case classes |
| `Color : [Red, Green, Blue]` | `sealed trait Color; case object Red extends Color...` | Sum types |
| Ability or module | `trait` or `object` | Depends on use case |
| `interface Utils` | `object Utils` | Module → singleton |
| `(A, B)` | `(A, B)` | Tuples map directly |
| Type parameters `a` | Generics `[A]` | Similar concept |

### Function Types

| Roc | Scala | Notes |
|-----|-------|-------|
| `{} -> R` | `() => R` | Zero-arg function |
| `A -> R` | `A => R` | Single arg |
| `A, B -> R` | `(A, B) => R` | Multiple args (tuple) |
| `A -> (B -> C)` | `A => B => C` | Curried functions |

---

## Idiom Translation

### Pattern 1: Simple Function and Record

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

**Why this translation:**
- Roc record → Scala case class
- Roc interface (module) → Scala companion object
- String interpolation syntax differs
- Type inference works in both but Scala encourages explicit return types

### Pattern 2: Tag Union with Pattern Matching

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

**Why this translation:**
- Tag union → Sealed trait + case classes/objects
- `when` → `match`
- Ability constraint → type parameter (toString implicit)
- Exhaustiveness checking works in both

### Pattern 3: Option Handling

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

**Scala:**
```scala
def findUser(id: Long, users: List[User]): Option[User] = {
  users.find(_.id == id)
}

def getEmail(maybeUser: Option[User]): String = {
  maybeUser.map(_.email).getOrElse("no email")
}

// For-comprehension
def combineUsers(id1: Long, id2: Long, users: List[User]): Option[(User, User)] = {
  for {
    user1 <- findUser(id1, users)
    user2 <- findUser(id2, users)
  } yield (user1, user2)
}
```

**Why this translation:**
- Roc tag union `[Some a, None]` → Scala `Option[A]`
- Nested `when` → for-comprehension (more ergonomic)
- Method chaining `map`/`getOrElse` → similar in Scala
- Scala's Option is more idiomatic and has richer API

### Pattern 4: List Processing

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

**Scala:**
```scala
val numbers = List(1, 2, 3, 4, 5)

val doubled = numbers.map(n => n * 2)
val evens = numbers.filter(n => n % 2 == 0)
val sum = numbers.foldLeft(0)(_ + _)

// For-comprehension
val squares = for {
  x <- numbers
  if x % 2 == 0
} yield x * x

// Or method chaining
val squares2 = numbers.filter(_ % 2 == 0).map(x => x * x)
```

**Why this translation:**
- `List.map` → `.map` (method syntax)
- `List.keepIf` → `.filter`
- `List.walk` → `.foldLeft`
- Pipeline → method chaining or for-comprehension
- Scala offers multiple equivalent styles

### Pattern 5: Error Handling with Result

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

# Try operator for early returns
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

**Scala:**
```scala
def divide(a: Long, b: Long): Either[String, Long] = {
  if (b == 0) Left("DivByZero")
  else Right(a / b)
}

def calculate(a: Long, b: Long, c: Long): Either[String, Long] = {
  for {
    x <- divide(a, b)
    y <- divide(x, c)
  } yield y
}

// Try for exceptions
import scala.util.{Try, Success, Failure}

def parseInt(s: String): Try[Long] = Try(s.toLong)

def safeParse(s: String): Option[Long] = parseInt(s).toOption
```

**Why this translation:**
- `Result ok err` → `Either[err, ok]` (same order)
- Try operator `!` → for-comprehension for early returns
- Roc's explicit error tags → Scala's String or custom types
- `Try` captures exceptions similar to Roc's result pattern
- `.toOption` converts Result/Either/Try to Option

### Pattern 6: Abilities to Type Classes

**Roc:**
```roc
# Roc abilities are automatic for basic types
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

**Scala:**
```scala
// Type class definition
trait Show[A] {
  def show(a: A): String
}

object Show {
  implicit val intShow: Show[Int] = (a: Int) => a.toString
  implicit val stringShow: Show[String] = (a: String) => s"'$a'"
}

def toString[A](value: A)(implicit s: Show[A]): String = {
  s.show(value)
}

// Usage
toString(42)      // Uses intShow
toString("hello") // Uses stringShow

// For custom types, define implicit manually
case class User(name: String, age: Int)

implicit val userShow: Show[User] = (u: User) =>
  s"""{ name: "${u.name}", age: ${u.age} }"""

toString(User("Alice", 30))
```

**Why this translation:**
- Roc ability → Scala trait (type class)
- Automatic derivation → manual implicit instances
- Ability constraint → implicit parameter
- Roc has fewer abilities but they're automatic
- Scala requires explicit instances but more flexible

### Pattern 7: Higher-Order Functions and Currying

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

**Scala:**
```scala
def applyTwice[A](f: A => A, x: A): A = f(f(x))

// Currying is natural in Scala
def add(a: Long)(b: Long): Long = a + b
val add5 = add(5) _

def compose[A, B, C](f: B => C, g: A => B): A => C = {
  a => f(g(a))
}

// Or use built-in compose/andThen
val f: Int => Int = _ * 2
val g: Int => Int = _ + 1
val composed = f compose g  // f(g(x))
val andThen = f andThen g   // g(f(x))
```

**Why this translation:**
- Higher-order functions work similarly
- Currying is more natural in Scala (multiple parameter lists)
- Scala has built-in `compose` and `andThen` on functions
- Type signatures use `=>` vs `->`

### Pattern 8: Records with Update

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

**Why this translation:**
- Roc record update `{ record & ... }` → Scala `copy` method
- Default values can be in constructor directly
- Case class provides `copy` automatically
- Scala's syntax is more concise

---

## Concurrency Patterns

### Roc Task vs Scala Future

Roc delegates all concurrency to the platform. Scala uses JVM threads and Futures.

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

**Scala:**
```scala
import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global

def fetchUser(id: Long): Future[User] = Future {
  // Database operation
  database.query(s"SELECT * FROM users WHERE id = $id")
}

def fetchPosts(userId: Long): Future[List[Post]] = Future {
  database.query(s"SELECT * FROM posts WHERE author = $userId")
}

// Composition with for-comprehension
val result: Future[(User, List[Post])] = for {
  user <- fetchUser(123)
  posts <- fetchPosts(user.id)
} yield (user, posts)

// Parallel execution
val users: Future[List[User]] = Future.sequence(
  List(1, 2, 3).map(fetchUser)
)
```

**Why this translation:**
- Roc platform Task → Scala Future
- Try operator `!` → for-comprehension
- Platform handles concurrency → ExecutionContext manages threads
- Task.sequence → Future.sequence
- Roc apps stay pure, Scala code manages effects explicitly

### Roc Platform vs Scala Akka Actors

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

// Create actor system
val system = ActorSystem(counter(0), "counter-system")
```

**Why this translation:**
- Roc pure state functions → Akka actor behaviors
- Platform handles concurrency → Actor system handles messages
- Roc's pure approach → Akka's message-passing model
- State transformations → State transitions in actors

---

## Module System Translation

### Roc Interface → Scala Package/Object

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

**Scala:**
```scala
package com.example.users

case class User(id: Long, name: String, email: String)

object UserService {
  def create(name: String, email: String): User = {
    val id = generateId()
    User(id, name, email)
  }

  def validate(user: User): Either[String, User] = {
    if (user.email.contains("@")) Right(user)
    else Left("Invalid email")
  }

  // Private helper
  private def generateId(): Long = {
    // Implementation
    123L
  }
}
```

**Why this translation:**
- Roc interface → Scala package + companion object
- Explicit `exposes` → Scala visibility modifiers
- Not in exposes → `private` methods
- Public API → public methods

---

## Common Pitfalls

### 1. Assuming Immutability is Enforced

**Roc Guarantee:**
```roc
# No mutable state - always returns new value
increment : I64 -> I64
increment = \counter ->
    counter + 1
```

**Scala Allows Mutation:**
```scala
// Can use var if needed
var counter = 0
counter += 1  // Mutation is allowed

// But prefer immutable val
val counter = 0
val newCounter = counter + 1
```

**Why:** Scala allows both `val` (immutable) and `var` (mutable). Choose wisely.

### 2. Expecting Platform Separation

**Pitfall:** Trying to keep platform separation in Scala.

**Roc Approach:**
```roc
# Platform provides effects
import pf.File
import pf.Task exposing [Task]

readFile : Str -> Task Str [FileErr]
readFile = \path ->
    File.readUtf8(path)
```

**Scala Reality:**
```scala
// Direct I/O in application code
import scala.io.Source

def readFile(path: String): String = {
  Source.fromFile(path).mkString
}

// Or wrap in effect system if desired (Cats Effect, ZIO)
import cats.effect.IO

def readFile(path: String): IO[String] = {
  IO(Source.fromFile(path).mkString)
}
```

**Why:** Scala doesn't enforce platform separation. Effects can be anywhere.

### 3. Tag Union vs Sealed Trait Verbosity

**Pitfall:** Expecting concise tag union syntax.

**Roc:**
```roc
Result a : [Success a, Failure Str, Pending]
```

**Scala:**
```scala
// More verbose but more powerful
sealed trait Result[+A]
case class Success[A](value: A) extends Result[A]
case class Failure(error: String) extends Result[Nothing]
case object Pending extends Result[Nothing]
```

**Why:** Scala requires explicit class definitions but allows more flexibility.

### 4. Ability Derivation is Not Automatic

**Pitfall:** Expecting automatic type class instances.

**Roc:**
```roc
# Abilities derived automatically for records
User : { name : Str, age : U32 }
# Automatically has Eq, Hash, Inspect, etc.
```

**Scala:**
```scala
// Must derive explicitly or define instances
case class User(name: String, age: Int)

// Ordering must be explicit
implicit val userOrdering: Ordering[User] = Ordering.by(_.name)

// Or use libraries like cats for derivation
import cats.derived._
implicit val userShow: Show[User] = derived.semiauto.show
```

**Why:** Scala doesn't auto-derive type class instances. Must be explicit.

### 5. No Null in Roc, Null Exists in Scala

**Roc:**
```roc
# No null! Always use tag unions
maybeUser : [Some User, None]
maybeUser = None
```

**Scala:**
```scala
// Null exists but should be avoided
var user: User = null  // Bad!

// Use Option instead
val maybeUser: Option[User] = None  // Good
```

**Why:** Scala has null for Java interop. Always use Option to avoid NPEs.

### 6. Different Error Handling Philosophies

**Pitfall:** Expecting all errors as Result types.

**Roc:**
```roc
# All errors are explicit in Result
divide : I64, I64 -> Result I64 [DivByZero]
```

**Scala:**
```scala
// Can use exceptions, Either, or Try
def divide(a: Int, b: Int): Int = {
  if (b == 0) throw new ArithmeticException("Division by zero")
  else a / b
}

// Or typed errors
def divideSafe(a: Int, b: Int): Either[String, Int] = {
  if (b == 0) Left("Division by zero")
  else Right(a / b)
}
```

**Why:** Scala allows exceptions. Choose error handling strategy based on context.

---

## Tooling

| Purpose | Roc | Scala | Notes |
|---------|-----|-------|-------|
| **Build tool** | `roc` CLI | sbt, Mill, Maven | Scala has multiple build tools |
| **Package manager** | Platform dependencies | sbt, Maven Central | Scala uses JVM ecosystem |
| **Testing** | `roc test` | ScalaTest, MUnit, specs2 | Multiple testing frameworks |
| **REPL** | `roc repl` | `scala` REPL | Interactive exploration |
| **Formatter** | `roc format` | Scalafmt | Configurable formatting |
| **Type checking** | `roc check` | `scalac` | Scala compiler checks types |
| **Documentation** | Comments | Scaladoc | Generate API docs |

---

## Examples

### Example 1: Simple HTTP Client

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

**Scala (Akka HTTP):**
```scala
import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model._
import scala.concurrent.Future
import scala.concurrent.duration._

implicit val system = ActorSystem()
import system.dispatcher

def fetchUrl(url: String): Future[String] = {
  Http().singleRequest(HttpRequest(uri = url)).flatMap { response =>
    response.entity.toStrict(5.seconds).map(_.data.utf8String)
  }
}

val content: Future[String] = fetchUrl("https://example.com")
content.foreach(println)
```

### Example 2: Data Processing Pipeline

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

### Example 3: Error Handling Pipeline

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

---

## Performance Considerations

### Roc vs Scala Performance Differences

| Aspect | Roc | Scala | Impact |
|--------|-----|-------|--------|
| **Runtime** | Native compilation | JVM (GC, JIT) | Roc generally faster startup, Scala has longer warmup |
| **Collections** | Native data structures | JVM optimized | Different performance characteristics |
| **Concurrency** | Platform-managed | Thread pool, async | Platform vs runtime dependent |
| **Memory** | Platform-managed | Heap-based, GC | Scala has GC pauses |
| **Startup** | Instant | JVM warmup time | Roc has immediate performance |

### Optimization Tips

1. **Leverage JVM optimizations** - JIT compiler optimizes hot paths over time
2. **Choose appropriate collections** - Vector for random access, List for sequential
3. **Use immutable collections** - Better GC characteristics with structural sharing
4. **Consider lazy evaluation** - LazyList or Iterator for large datasets
5. **Profile JVM performance** - Different bottlenecks than native code

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-roc-dev` - Roc development patterns
- `lang-scala-dev` - Scala development patterns
- `convert-clojure-scala` - Similar functional language conversion (Clojure → Scala)

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Tasks vs Futures/Actors vs other approaches
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Abilities vs implicits vs other approaches
