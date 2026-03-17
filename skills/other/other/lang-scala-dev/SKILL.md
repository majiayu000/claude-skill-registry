---
name: lang-scala-dev
description: Foundational Scala patterns covering immutability, pattern matching, traits, case classes, for-comprehensions, and functional programming. Use when writing Scala code, understanding the type system, or needing guidance on which specialized Scala skill to use. This is the entry point for Scala development.
---

# Scala Fundamentals

## Overview

This is the **foundational skill** for Scala development. Use this skill when writing Scala code, understanding core language features, or determining which specialized Scala skill to use.

### Skill Hierarchy

```
lang-scala-dev (YOU ARE HERE - Foundational)
├── lang-scala-akka-dev (Akka actors, streams, clustering)
├── lang-scala-cats-dev (Cats FP library, type classes, effects)
├── lang-scala-zio-dev (ZIO effects, fibers, resources)
├── lang-scala-spark-dev (Apache Spark, distributed computing)
├── lang-scala-play-dev (Play Framework web applications)
└── lang-scala-testing-dev (ScalaTest, ScalaCheck, property testing)
```

### When to Use This Skill

- **Writing basic Scala code** - syntax, types, control flow
- **Understanding core language features** - pattern matching, traits, case classes
- **Learning Scala fundamentals** - immutability, functional programming
- **Determining skill routing** - which specialized skill to use
- **Troubleshooting common errors** - compilation issues, type errors

---

## Quick Reference

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| **Immutable val** | `val x = 42` | Default variable declaration |
| **Mutable var** | `var x = 42` | When mutation is necessary |
| **Case class** | `case class User(name: String, age: Int)` | Data containers with pattern matching |
| **Pattern match** | `x match { case ... => ... }` | Destructuring, conditional logic |
| **Option** | `Option[A]`, `Some(value)`, `None` | Nullable value handling |
| **Either** | `Either[L, R]`, `Left(error)`, `Right(value)` | Error handling with context |
| **Try** | `Try { riskyOp }` | Exception handling |
| **For-comprehension** | `for { x <- opt1; y <- opt2 } yield x + y` | Sequential monadic operations |
| **Higher-order fn** | `list.map(f).filter(p)` | Function composition |
| **Trait** | `trait Logging { ... }` | Interface with implementation |
| **Object** | `object Utils { ... }` | Singleton, companion object |
| **Implicit (2.x)** | `implicit val ord: Ordering[A]` | Type class instances |
| **Given/Using (3.x)** | `given Ordering[A] with { ... }` | Scala 3 implicits |

---

## Skill Routing

| Task | Use This Skill | Rationale |
|------|---------------|-----------|
| Akka actors, streams, clustering | `lang-scala-akka-dev` | Specialized actor model patterns |
| Cats library, type classes, MTL | `lang-scala-cats-dev` | Advanced FP abstractions |
| ZIO effects, fibers, layers | `lang-scala-zio-dev` | Effect system patterns |
| Spark jobs, RDDs, DataFrames | `lang-scala-spark-dev` | Distributed computing |
| Play web apps, controllers, routes | `lang-scala-play-dev` | Web framework patterns |
| ScalaTest, ScalaCheck, mocking | `lang-scala-testing-dev` | Testing strategies |
| **Core language features** | **This skill** | Foundational patterns |

---

## Core Language Features

### Val vs Var - Immutability

**Prefer immutable `val` over mutable `var`:**

```scala
// Good - immutable
val name = "Alice"
val age = 30
val user = User(name, age)

// Avoid - mutable
var counter = 0
counter += 1  // Mutation creates complexity

// Better - functional update
val counter = 0
val newCounter = counter + 1
```

**When to use `var`:**

```scala
// Loop counters (prefer for-comprehensions)
var i = 0
while (i < 10) {
  println(i)
  i += 1
}

// Mutable accumulators (prefer foldLeft)
var sum = 0
list.foreach(x => sum += x)

// Better alternatives
(0 until 10).foreach(println)
val sum = list.foldLeft(0)(_ + _)
```

**Immutable collections:**

```scala
// Immutable by default
val list = List(1, 2, 3)
val newList = list :+ 4        // Creates new list
val map = Map("a" -> 1, "b" -> 2)
val newMap = map + ("c" -> 3)  // Creates new map

// Mutable collections (import required)
import scala.collection.mutable

val buffer = mutable.ListBuffer(1, 2, 3)
buffer += 4  // In-place mutation
val mutableMap = mutable.Map("a" -> 1)
mutableMap("b") = 2  // In-place mutation
```

---

### Case Classes and Pattern Matching

**Case classes** provide automatic implementations of `equals`, `hashCode`, `toString`, and `copy`:

```scala
// Case class definition
case class User(name: String, age: Int, email: String)

// Automatic features
val user = User("Alice", 30, "alice@example.com")
println(user)  // User(Alice,30,alice@example.com)

val updated = user.copy(age = 31)  // Immutable update

val User(name, age, email) = user  // Destructuring
```

**Pattern matching:**

```scala
// Match on case classes
def describe(user: User): String = user match {
  case User("Admin", _, _) => "Administrator"
  case User(name, age, _) if age < 18 => s"$name is a minor"
  case User(name, age, _) => s"$name is $age years old"
}

// Match on types
def process(value: Any): String = value match {
  case s: String => s.toUpperCase
  case i: Int => (i * 2).toString
  case d: Double => f"$d%.2f"
  case _ => "Unknown"
}

// Match on collections
def sumFirst(list: List[Int]): Int = list match {
  case Nil => 0
  case head :: Nil => head
  case head :: tail => head + sumFirst(tail)
}

// Guards and alternatives
def classify(n: Int): String = n match {
  case x if x < 0 => "negative"
  case 0 => "zero"
  case x if x % 2 == 0 => "even positive"
  case _ => "odd positive"
}
```

**Sealed traits for ADTs:**

```scala
sealed trait Result[+A]
case class Success[A](value: A) extends Result[A]
case class Failure(error: String) extends Result[Nothing]
case object Pending extends Result[Nothing]

def handle[A](result: Result[A]): String = result match {
  case Success(value) => s"Got: $value"
  case Failure(error) => s"Error: $error"
  case Pending => "Waiting..."
  // Compiler ensures exhaustiveness
}
```

---

### Traits and Mixins

**Traits as interfaces:**

```scala
trait Logging {
  def log(message: String): Unit
}

trait Auditing {
  def audit(event: String): Unit
}

class Service extends Logging with Auditing {
  def log(message: String): Unit = println(s"[LOG] $message")
  def audit(event: String): Unit = println(s"[AUDIT] $event")
}
```

**Traits with implementation:**

```scala
trait Logging {
  def log(message: String): Unit = {
    println(s"${java.time.Instant.now()}: $message")
  }
}

trait ErrorHandling {
  def handleError(error: Throwable): Unit = {
    System.err.println(s"Error: ${error.getMessage}")
  }
}

class Application extends Logging with ErrorHandling {
  def run(): Unit = {
    log("Application starting")
    try {
      // Application logic
    } catch {
      case e: Exception => handleError(e)
    }
  }
}
```

**Self-types for dependency declaration:**

```scala
trait DatabaseAccess {
  def query(sql: String): List[String]
}

trait UserService {
  self: DatabaseAccess =>  // Requires DatabaseAccess

  def getUsers(): List[String] = {
    query("SELECT * FROM users")  // Can use DatabaseAccess methods
  }
}

class Application extends UserService with DatabaseAccess {
  def query(sql: String): List[String] = {
    // Database implementation
    List("user1", "user2")
  }
}
```

**Linearization (method resolution order):**

```scala
trait A { def msg = "A" }
trait B extends A { override def msg = "B" + super.msg }
trait C extends A { override def msg = "C" + super.msg }

class D extends B with C  // Linearization: D -> C -> B -> A
val d = new D
println(d.msg)  // "CBA"
```

---

### For-Comprehensions

**Desugaring to map/flatMap/filter:**

```scala
// For-comprehension
val result = for {
  x <- Some(1)
  y <- Some(2)
  z <- Some(3)
} yield x + y + z

// Desugars to
val result = Some(1).flatMap { x =>
  Some(2).flatMap { y =>
    Some(3).map { z =>
      x + y + z
    }
  }
}
```

**With filters:**

```scala
val result = for {
  x <- List(1, 2, 3, 4, 5)
  if x % 2 == 0
  y <- List(10, 20)
} yield x * y

// Desugars to
val result = List(1, 2, 3, 4, 5)
  .filter(_ % 2 == 0)
  .flatMap(x => List(10, 20).map(y => x * y))
// Result: List(20, 40, 40, 80)
```

**With pattern matching:**

```scala
case class User(name: String, age: Int)

val users = List(User("Alice", 30), User("Bob", 25))

val names = for {
  User(name, age) <- users
  if age >= 30
} yield name.toUpperCase

// Result: List("ALICE")
```

**Combining different monadic types:**

```scala
def findUser(id: Int): Option[User] = ???
def getPermissions(user: User): List[String] = ???

val result = for {
  user <- findUser(123)
  permission <- getPermissions(user)
} yield s"${user.name} has $permission"
// Result type: Option[List[String]]
```

---

### Option, Either, Try

**Option - handling nullable values:**

```scala
// Creating Options
val some: Option[Int] = Some(42)
val none: Option[Int] = None

// From nullable
val maybeValue: Option[String] = Option(nullableString)

// Pattern matching
def describe(opt: Option[Int]): String = opt match {
  case Some(value) => s"Got $value"
  case None => "Nothing"
}

// Combinators
val doubled = some.map(_ * 2)           // Some(84)
val filtered = some.filter(_ > 50)      // None
val orElse = none.orElse(Some(0))       // Some(0)
val getOrElse = none.getOrElse(0)       // 0

// For-comprehensions
val result = for {
  x <- Some(1)
  y <- Some(2)
} yield x + y  // Some(3)
```

**Either - error handling with context:**

```scala
// Right for success, Left for failure
type Result[A] = Either[String, A]

def divide(a: Int, b: Int): Result[Int] = {
  if (b == 0) Left("Division by zero")
  else Right(a / b)
}

// Pattern matching
divide(10, 2) match {
  case Right(value) => println(s"Result: $value")
  case Left(error) => println(s"Error: $error")
}

// Combinators (right-biased)
val result = divide(10, 2)
  .map(_ * 2)                    // Right(10)
  .flatMap(x => divide(x, 5))    // Right(2)

// For-comprehensions
val calculation = for {
  a <- divide(10, 2)
  b <- divide(a, 5)
  c <- divide(b, 1)
} yield c  // Right(1)
```

**Try - exception handling:**

```scala
import scala.util.{Try, Success, Failure}

// Creating Try
val attempt = Try {
  "123".toInt  // Might throw NumberFormatException
}

// Pattern matching
attempt match {
  case Success(value) => println(s"Parsed: $value")
  case Failure(exception) => println(s"Error: ${exception.getMessage}")
}

// Combinators
val result = Try("123".toInt)
  .map(_ * 2)
  .recover { case _: NumberFormatException => 0 }
  .getOrElse(-1)

// Converting to Option or Either
val opt: Option[Int] = attempt.toOption
val either: Either[Throwable, Int] = attempt.toEither
```

**Choosing between Option, Either, Try:**

| Type | Use When | Error Info |
|------|----------|------------|
| `Option[A]` | Value may be absent | No error context |
| `Either[E, A]` | Need error details | Custom error type `E` |
| `Try[A]` | Catching exceptions | `Throwable` exception |

---

### Collections

**Immutable collections (default):**

```scala
// List - linked list
val list = List(1, 2, 3)
val prepended = 0 :: list        // O(1) prepend
val appended = list :+ 4         // O(n) append
val concatenated = list ++ List(4, 5)

// Vector - indexed sequence
val vector = Vector(1, 2, 3)
val updated = vector.updated(1, 42)  // O(log n) update
val accessed = vector(1)             // O(log n) access

// Set - unique elements
val set = Set(1, 2, 3, 2)  // Set(1, 2, 3)
val added = set + 4
val removed = set - 2

// Map - key-value pairs
val map = Map("a" -> 1, "b" -> 2)
val updated = map + ("c" -> 3)
val removed = map - "a"
val value = map.get("a")  // Option[Int]
val valueOrDefault = map.getOrElse("z", 0)
```

**Common operations:**

```scala
val list = List(1, 2, 3, 4, 5)

// Transformations
list.map(_ * 2)                    // List(2, 4, 6, 8, 10)
list.filter(_ % 2 == 0)            // List(2, 4)
list.flatMap(x => List(x, x * 10)) // List(1, 10, 2, 20, ...)

// Reductions
list.foldLeft(0)(_ + _)            // 15
list.foldRight(0)(_ + _)           // 15
list.reduce(_ + _)                 // 15
list.scan(0)(_ + _)                // List(0, 1, 3, 6, 10, 15)

// Grouping
list.groupBy(_ % 2)                // Map(0 -> List(2,4), 1 -> List(1,3,5))
list.partition(_ % 2 == 0)         // (List(2, 4), List(1, 3, 5))

// Searching
list.find(_ > 3)                   // Some(4)
list.exists(_ > 3)                 // true
list.forall(_ > 0)                 // true

// Sorting
list.sorted                        // List(1, 2, 3, 4, 5)
list.sortBy(-_)                    // List(5, 4, 3, 2, 1)
list.sortWith(_ > _)               // List(5, 4, 3, 2, 1)

// Zipping
list.zip(List("a", "b", "c"))      // List((1,a), (2,b), (3,c))
list.zipWithIndex                  // List((1,0), (2,1), (3,2), ...)
```

**Performance characteristics:**

| Collection | Access | Prepend | Append | Update |
|------------|--------|---------|--------|--------|
| List | O(n) | O(1) | O(n) | O(n) |
| Vector | O(log n) | O(log n) | O(log n) | O(log n) |
| Array | O(1) | O(n) | O(n) | O(1) |
| Set | O(log n) | O(log n) | O(log n) | - |
| Map | O(log n) | O(log n) | O(log n) | O(log n) |

---

### Higher-Order Functions

**Functions as values:**

```scala
// Function literals
val add: (Int, Int) => Int = (a, b) => a + b
val square: Int => Int = x => x * x
val greet: String => Unit = name => println(s"Hello, $name")

// Method to function
def multiply(a: Int, b: Int): Int = a * b
val multiplyFn = multiply _  // Eta expansion

// Placeholder syntax
val add1 = (_: Int) + 1
val sum = (_: Int) + (_: Int)
```

**Higher-order functions:**

```scala
// Taking functions as parameters
def applyTwice(f: Int => Int, x: Int): Int = f(f(x))
applyTwice(_ * 2, 3)  // 12

def repeat(n: Int)(action: => Unit): Unit = {
  (1 to n).foreach(_ => action)
}
repeat(3) { println("Hello") }

// Returning functions
def multiplier(factor: Int): Int => Int = {
  x => x * factor
}
val double = multiplier(2)
double(5)  // 10

// Currying
def add(a: Int)(b: Int): Int = a + b
val add5 = add(5) _
add5(3)  // 8

// Partial application
def sum3(a: Int, b: Int, c: Int): Int = a + b + c
val sumWith10 = sum3(10, _: Int, _: Int)
sumWith10(20, 30)  // 60
```

**Common higher-order patterns:**

```scala
// Map, filter, fold
List(1, 2, 3)
  .map(_ * 2)
  .filter(_ > 3)
  .foldLeft(0)(_ + _)

// Composition
val f: Int => Int = _ * 2
val g: Int => Int = _ + 1
val composed = f compose g  // f(g(x))
val andThen = f andThen g   // g(f(x))

composed(5)  // 12 = (5 + 1) * 2
andThen(5)   // 11 = (5 * 2) + 1
```

---

### Implicits and Given/Using

**Scala 2 implicits:**

```scala
// Implicit parameters
def greet(name: String)(implicit greeting: String): String = {
  s"$greeting, $name"
}

implicit val defaultGreeting: String = "Hello"
greet("Alice")  // "Hello, Alice"

// Implicit conversions (use sparingly)
implicit def intToString(x: Int): String = x.toString
val s: String = 42  // Implicit conversion

// Implicit classes (extension methods)
implicit class RichInt(x: Int) {
  def squared: Int = x * x
}
42.squared  // 1764

// Type classes
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

print(42)      // "42"
print("hello") // "'hello'"
```

**Scala 3 given/using:**

```scala
// Given instances
trait Show[A] {
  def show(a: A): String
}

given Show[Int] with {
  def show(a: Int): String = a.toString
}

given Show[String] with {
  def show(a: String): String = s"'$a'"
}

// Using clauses
def print[A](a: A)(using s: Show[A]): Unit = {
  println(s.show(a))
}

print(42)      // "42"
print("hello") // "'hello'"

// Extension methods (Scala 3)
extension (x: Int) {
  def squared: Int = x * x
  def cubed: Int = x * x * x
}

42.squared  // 1764
```

**Implicit resolution rules:**

1. **Local scope** - implicits defined in current scope
2. **Imported scope** - explicitly imported implicits
3. **Companion objects** - companion of type or type class
4. **Implicit scope** - package objects, parent types

```scala
// Resolution example
trait Ordering[A]

object Ordering {
  // Companion object - implicit scope
  implicit val intOrdering: Ordering[Int] = ???
}

class MyClass {
  // Local scope takes precedence
  implicit val localOrdering: Ordering[Int] = ???

  def sort[A](list: List[A])(implicit ord: Ordering[A]): List[A] = ???

  sort(List(3, 1, 2))  // Uses localOrdering
}
```

---

### Type System

**Type variance:**

```scala
// Covariance (+A) - subtyping preserved
trait Producer[+A] {
  def produce(): A
}

class Animal
class Dog extends Animal

val dogProducer: Producer[Dog] = ???
val animalProducer: Producer[Animal] = dogProducer  // OK

// Contravariance (-A) - subtyping reversed
trait Consumer[-A] {
  def consume(a: A): Unit
}

val animalConsumer: Consumer[Animal] = ???
val dogConsumer: Consumer[Dog] = animalConsumer  // OK

// Invariance (A) - no subtyping
trait Box[A] {
  def get: A
  def set(a: A): Unit
}

// List is covariant, Array is invariant
val dogs: List[Dog] = List()
val animals: List[Animal] = dogs  // OK

val dogArray: Array[Dog] = Array()
// val animalArray: Array[Animal] = dogArray  // Compile error
```

**Type bounds:**

```scala
// Upper bound (A <: B) - A must be subtype of B
def findMax[A <: Comparable[A]](list: List[A]): A = {
  list.reduce((a, b) => if (a.compareTo(b) > 0) a else b)
}

// Lower bound (A >: B) - A must be supertype of B
sealed trait Animal
case class Dog(name: String) extends Animal
case class Cat(name: String) extends Animal

def prepend[A, B >: A](elem: B, list: List[A]): List[B] = {
  elem :: list
}

val dogs: List[Dog] = List(Dog("Fido"))
val animals: List[Animal] = prepend(Cat("Whiskers"), dogs)

// Context bounds (requires implicit)
def sort[A: Ordering](list: List[A]): List[A] = {
  list.sorted  // Uses implicit Ordering[A]
}

// Multiple bounds
def process[A <: Animal with Comparable[A]: Show](a: A): String = ???
```

**Type aliases and abstract types:**

```scala
// Type alias
type UserId = Int
type Result[A] = Either[String, A]

val id: UserId = 123
val result: Result[Int] = Right(42)

// Abstract types
trait Container {
  type Element
  def add(e: Element): Unit
  def get(): Element
}

class IntContainer extends Container {
  type Element = Int
  private var value: Int = 0
  def add(e: Int): Unit = value = e
  def get(): Int = value
}

// Path-dependent types
class Outer {
  class Inner
  def process(inner: Inner): Unit = ???
}

val outer1 = new Outer
val outer2 = new Outer

val inner1 = new outer1.Inner
// outer2.process(inner1)  // Compile error - type mismatch
```

---

## Module System

Scala uses packages and objects to organize code. The module system provides flexible import mechanisms, visibility modifiers, and companion objects for namespace management.

### Packages

```scala
// Package declaration
package com.example.myapp

// Or nested (less common)
package com.example {
  package myapp {
    class MyClass
  }
}

// Package objects - shared utilities for a package
// File: com/example/package.scala
package object example {
  type UserId = Long
  val DefaultTimeout = 30.seconds

  def log(message: String): Unit = println(s"[LOG] $message")
}

// Usage - available to all code in com.example
package com.example.myapp

class Service {
  val id: UserId = 123L  // From package object
  log("Service created")  // From package object
}
```

### Import Patterns

```scala
// Basic import
import java.time.LocalDate

// Import all members
import java.time._

// Import multiple specific members
import java.time.{LocalDate, LocalTime, ZonedDateTime}

// Rename on import (avoid conflicts)
import java.util.{List => JList}
import scala.collection.immutable.List

// Exclude on import
import java.util.{Date => _, _}  // Import all except Date

// Import object members
object Utils {
  def helper(): Unit = ???
}
import Utils.helper

// Import with alias (Scala 3)
import java.time.LocalDate as Date

// Import given instances (Scala 3)
import MyCodecs.given
import MyCodecs.{given JsonEncoder[_]}
```

### Visibility Modifiers

```scala
class Example {
  private val privateField = 1      // This class only
  protected val protectedField = 2  // This class and subclasses

  private[this] val instanceOnly = 3      // This instance only
  private[Example] val sameAsPrivate = 4  // This class (same as private)
  private[myapp] val packagePrivate = 5   // Package-visible
  protected[myapp] val packageProtected = 6

  val publicField = 7  // Public (default)
}

// Package-private class
private[myapp] class InternalHelper

// Sealed for ADTs (visible in same file)
sealed trait Result
case class Success(value: Int) extends Result
case class Failure(error: String) extends Result
```

### Companion Objects

```scala
// Class and companion object share private access
class User private (val name: String, val age: Int)

object User {
  // Factory method
  def apply(name: String, age: Int): User = new User(name, age)

  // Smart constructor with validation
  def create(name: String, age: Int): Either[String, User] = {
    if (name.isEmpty) Left("Name cannot be empty")
    else if (age < 0) Left("Age cannot be negative")
    else Right(new User(name, age))
  }

  // Extractor for pattern matching
  def unapply(user: User): Option[(String, Int)] =
    Some((user.name, user.age))

  // Constants
  val Anonymous: User = new User("Anonymous", 0)
}

// Usage
val user = User("Alice", 30)  // Uses apply
val result = User.create("Bob", 25)

user match {
  case User(name, age) => println(s"$name is $age")  // Uses unapply
}
```

### Module Patterns

```scala
// Object as module
object StringUtils {
  def capitalize(s: String): String = s.capitalize
  def reverse(s: String): String = s.reverse

  // Nested module
  object Validators {
    def isEmail(s: String): Boolean = s.contains("@")
    def isNotEmpty(s: String): Boolean = s.nonEmpty
  }
}

// Usage
import StringUtils._
import StringUtils.Validators._

capitalize("hello")
isEmail("test@example.com")
```

### Scala 3 Exports

```scala
// Export delegates to another object
class UserRepository {
  def findById(id: Int): Option[User] = ???
  def save(user: User): Unit = ???
  def delete(id: Int): Unit = ???
}

class UserService(repo: UserRepository) {
  // Export selected members
  export repo.{findById, save}

  // Export all members
  // export repo._

  // Export with rename
  export repo.{delete as removeUser}

  def businessLogic(): Unit = {
    // Uses repo internally
  }
}

// Clients can call userService.findById directly
val service = new UserService(new UserRepository)
service.findById(123)  // Delegated to repo
```

### File Organization

```
// Typical project structure
src/main/scala/
├── com/example/myapp/
│   ├── Main.scala           // Entry point
│   ├── domain/
│   │   ├── User.scala       // User case class + companion
│   │   ├── Order.scala      // Order case class + companion
│   │   └── package.scala    // Package object with shared types
│   ├── service/
│   │   ├── UserService.scala
│   │   └── OrderService.scala
│   ├── repository/
│   │   ├── UserRepository.scala
│   │   └── OrderRepository.scala
│   └── util/
│       └── StringUtils.scala

// One public class/trait/object per file (convention)
// File name should match primary type name
```

### Import Best Practices

```scala
// Standard ordering convention
import java.time._                     // 1. Java stdlib
import scala.concurrent._              // 2. Scala stdlib
import cats.effect._                   // 3. Third-party libraries
import com.example.myapp.domain._      // 4. Project imports

// Avoid wildcard imports for large namespaces
import java.util._  // Avoid - pollutes namespace

// Prefer explicit imports
import java.util.{List, Map, Optional}  // Better

// Exception: well-known small namespaces
import cats.syntax.all._  // OK - common in FP code
import scala.concurrent.ExecutionContext.Implicits.global  // OK - well-known
```

---

## Common Patterns

### Builder Pattern

**Using copy method (case classes):**

```scala
case class User(
  name: String,
  age: Int,
  email: String,
  phone: Option[String] = None,
  address: Option[String] = None
)

// Building with copy
val user = User("Alice", 30, "alice@example.com")
  .copy(phone = Some("555-1234"))
  .copy(address = Some("123 Main St"))
```

**Explicit builder:**

```scala
class UserBuilder private (
  private var name: String = "",
  private var age: Int = 0,
  private var email: String = "",
  private var phone: Option[String] = None
) {
  def withName(name: String): UserBuilder = {
    this.name = name
    this
  }

  def withAge(age: Int): UserBuilder = {
    this.age = age
    this
  }

  def withEmail(email: String): UserBuilder = {
    this.email = email
    this
  }

  def withPhone(phone: String): UserBuilder = {
    this.phone = Some(phone)
    this
  }

  def build(): User = {
    require(name.nonEmpty, "Name is required")
    require(email.nonEmpty, "Email is required")
    User(name, age, email, phone, None)
  }
}

object UserBuilder {
  def apply(): UserBuilder = new UserBuilder()
}

// Usage
val user = UserBuilder()
  .withName("Alice")
  .withAge(30)
  .withEmail("alice@example.com")
  .withPhone("555-1234")
  .build()
```

---

### Type Classes

**Definition and implementation:**

```scala
// Type class definition
trait Show[A] {
  def show(a: A): String
}

// Type class instances
object Show {
  // Summoner method
  def apply[A](implicit instance: Show[A]): Show[A] = instance

  // Constructor method
  def instance[A](f: A => String): Show[A] = new Show[A] {
    def show(a: A): String = f(a)
  }

  // Instances
  implicit val intShow: Show[Int] = instance(_.toString)
  implicit val stringShow: Show[String] = instance(s => s"'$s'")
  implicit val boolShow: Show[Boolean] = instance(_.toString)

  // Derived instance
  implicit def listShow[A](implicit sa: Show[A]): Show[List[A]] = {
    instance(list => list.map(sa.show).mkString("[", ", ", "]"))
  }
}

// Extension methods (Scala 2)
implicit class ShowOps[A](val a: A) extends AnyVal {
  def show(implicit s: Show[A]): String = s.show(a)
}

// Usage
42.show                    // "42"
"hello".show               // "'hello'"
List(1, 2, 3).show         // "[1, 2, 3]"
```

**Type class with operations:**

```scala
trait Monoid[A] {
  def empty: A
  def combine(x: A, y: A): A
}

object Monoid {
  def apply[A](implicit instance: Monoid[A]): Monoid[A] = instance

  implicit val intAddMonoid: Monoid[Int] = new Monoid[Int] {
    def empty: Int = 0
    def combine(x: Int, y: Int): Int = x + y
  }

  implicit val stringMonoid: Monoid[String] = new Monoid[String] {
    def empty: String = ""
    def combine(x: String, y: String): String = x + y
  }

  implicit def listMonoid[A]: Monoid[List[A]] = new Monoid[List[A]] {
    def empty: List[A] = Nil
    def combine(x: List[A], y: List[A]): List[A] = x ++ y
  }
}

def combineAll[A](list: List[A])(implicit m: Monoid[A]): A = {
  list.foldLeft(m.empty)(m.combine)
}

combineAll(List(1, 2, 3, 4))           // 10
combineAll(List("a", "b", "c"))        // "abc"
combineAll(List(List(1), List(2, 3))) // List(1, 2, 3)
```

---

### Cake Pattern

**Dependency injection using self-types:**

```scala
// Component definitions
trait UserRepositoryComponent {
  def userRepository: UserRepository

  trait UserRepository {
    def findById(id: Int): Option[User]
    def save(user: User): Unit
  }
}

trait EmailServiceComponent {
  def emailService: EmailService

  trait EmailService {
    def sendEmail(to: String, subject: String, body: String): Unit
  }
}

// Implementations
trait UserRepositoryComponentImpl extends UserRepositoryComponent {
  def userRepository: UserRepository = new UserRepositoryImpl

  class UserRepositoryImpl extends UserRepository {
    def findById(id: Int): Option[User] = {
      // Database access
      Some(User("Alice", 30, "alice@example.com"))
    }

    def save(user: User): Unit = {
      // Database access
      println(s"Saving user: $user")
    }
  }
}

trait EmailServiceComponentImpl extends EmailServiceComponent {
  def emailService: EmailService = new EmailServiceImpl

  class EmailServiceImpl extends EmailService {
    def sendEmail(to: String, subject: String, body: String): Unit = {
      println(s"Sending email to $to: $subject")
    }
  }
}

// Application component with dependencies
trait UserServiceComponent {
  self: UserRepositoryComponent with EmailServiceComponent =>

  def userService: UserService = new UserServiceImpl

  class UserServiceImpl extends UserService {
    def registerUser(user: User): Unit = {
      userRepository.save(user)
      emailService.sendEmail(user.email, "Welcome", "Thanks for registering!")
    }
  }

  trait UserService {
    def registerUser(user: User): Unit
  }
}

// Wiring
object Application extends UserServiceComponent
  with UserRepositoryComponentImpl
  with EmailServiceComponentImpl {

  def main(args: Array[String]): Unit = {
    val user = User("Bob", 25, "bob@example.com")
    userService.registerUser(user)
  }
}
```

---

### Algebraic Data Types (ADTs)

**Sum types (sealed traits):**

```scala
// Enumeration-like ADT
sealed trait Color
case object Red extends Color
case object Green extends Color
case object Blue extends Color

// Pattern matching is exhaustive
def describe(color: Color): String = color match {
  case Red => "red"
  case Green => "green"
  case Blue => "blue"
  // Compiler ensures all cases covered
}

// ADT with data
sealed trait Shape
case class Circle(radius: Double) extends Shape
case class Rectangle(width: Double, height: Double) extends Shape
case class Triangle(base: Double, height: Double) extends Shape

def area(shape: Shape): Double = shape match {
  case Circle(r) => math.Pi * r * r
  case Rectangle(w, h) => w * h
  case Triangle(b, h) => 0.5 * b * h
}
```

**Product types (case classes):**

```scala
// Simple product type
case class Point(x: Double, y: Double)

// Nested product types
case class Address(street: String, city: String, zip: String)
case class Person(name: String, age: Int, address: Address)

// Generic product type
case class Pair[A, B](first: A, second: B)
```

**Combining sum and product types:**

```scala
sealed trait Expression
case class Number(value: Int) extends Expression
case class Add(left: Expression, right: Expression) extends Expression
case class Multiply(left: Expression, right: Expression) extends Expression
case class Divide(left: Expression, right: Expression) extends Expression

def evaluate(expr: Expression): Either[String, Int] = expr match {
  case Number(value) => Right(value)
  case Add(left, right) =>
    for {
      l <- evaluate(left)
      r <- evaluate(right)
    } yield l + r
  case Multiply(left, right) =>
    for {
      l <- evaluate(left)
      r <- evaluate(right)
    } yield l * r
  case Divide(left, right) =>
    for {
      l <- evaluate(left)
      r <- evaluate(right)
      result <- if (r != 0) Right(l / r) else Left("Division by zero")
    } yield result
}

// Usage
val expr = Divide(Add(Number(10), Number(5)), Number(3))
evaluate(expr)  // Right(5)
```

**Recursive ADTs:**

```scala
sealed trait List[+A]
case object Nil extends List[Nothing]
case class Cons[A](head: A, tail: List[A]) extends List[A]

def sum(list: List[Int]): Int = list match {
  case Nil => 0
  case Cons(head, tail) => head + sum(tail)
}

// Binary tree
sealed trait Tree[+A]
case object Empty extends Tree[Nothing]
case class Node[A](value: A, left: Tree[A], right: Tree[A]) extends Tree[A]

def size[A](tree: Tree[A]): Int = tree match {
  case Empty => 0
  case Node(_, left, right) => 1 + size(left) + size(right)
}
```

---

## Troubleshooting

### Common Compilation Errors

**Type mismatch:**

```scala
// Error: type mismatch
val x: String = 42

// Fix: convert types
val x: String = 42.toString

// Error: cannot prove that A =:= B
def process[A](a: A): String = a.toString  // Fine
def process[A](a: A): A = "string"         // Error

// Fix: specify correct return type
def process[A](a: A): String = "string"
```

**Missing implicit parameter:**

```scala
// Error: could not find implicit value
def sort[A](list: List[A])(implicit ord: Ordering[A]): List[A] = {
  list.sorted
}

sort(List(1, 2, 3))  // OK - Ordering[Int] exists
// sort(List(Person("Alice", 30)))  // Error - no Ordering[Person]

// Fix: provide implicit
implicit val personOrdering: Ordering[Person] = Ordering.by(_.name)
sort(List(Person("Alice", 30)))  // OK now
```

**Pattern match not exhaustive:**

```scala
sealed trait Result
case class Success(value: Int) extends Result
case class Failure(error: String) extends Result

// Warning: match may not be exhaustive
def handle(result: Result): String = result match {
  case Success(value) => s"Got $value"
  // Missing Failure case
}

// Fix: add all cases
def handle(result: Result): String = result match {
  case Success(value) => s"Got $value"
  case Failure(error) => s"Error: $error"
}
```

**Recursive value needs type:**

```scala
// Error: recursive value x needs type
val x = x + 1

// Fix: specify type
val x: Int = {
  def helper: Int = helper + 1
  helper
}

// Or avoid recursion
val x = 1
```

**Variance errors:**

```scala
// Error: covariant type A occurs in contravariant position
trait Producer[+A] {
  def produce(): A           // OK - covariant position
  // def consume(a: A): Unit // Error - contravariant position
}

// Fix: use lower bound
trait Producer[+A] {
  def produce(): A
  def consume[B >: A](b: B): Unit  // OK
}
```

### Runtime Issues

**NullPointerException:**

```scala
// Dangerous - nullable
val name: String = null
// name.toUpperCase  // NullPointerException

// Better - use Option
val name: Option[String] = None
name.map(_.toUpperCase)  // Safe
```

**StackOverflowError in recursion:**

```scala
// Not tail recursive
def factorial(n: Int): Int = {
  if (n <= 1) 1
  else n * factorial(n - 1)  // Not in tail position
}

// factorial(10000)  // StackOverflowError

// Fix: use tail recursion
@scala.annotation.tailrec
def factorial(n: Int, acc: Int = 1): Int = {
  if (n <= 1) acc
  else factorial(n - 1, n * acc)  // Tail call
}

factorial(10000)  // OK
```

**ClassCastException:**

```scala
// Dangerous - type erasure
def castList(list: Any): List[Int] = list.asInstanceOf[List[Int]]

val stringList = List("a", "b", "c")
val intList = castList(stringList)  // No error yet
// intList.head + 1  // ClassCastException at runtime

// Better - use pattern matching
def safeToIntList(value: Any): Option[List[Int]] = value match {
  case list: List[_] if list.forall(_.isInstanceOf[Int]) =>
    Some(list.asInstanceOf[List[Int]])
  case _ => None
}
```

---

## Performance Tips

**Prefer immutable collections:**

```scala
// Immutable operations create new instances
val list = List(1, 2, 3)
val newList = list :+ 4  // Structural sharing, efficient

// For building, use builders
val builder = List.newBuilder[Int]
(1 to 1000).foreach(builder += _)
val result = builder.result()
```

**Use tail recursion:**

```scala
// Stack-safe tail recursion
@scala.annotation.tailrec
def sum(list: List[Int], acc: Int = 0): Int = list match {
  case Nil => acc
  case head :: tail => sum(tail, acc + head)
}
```

**Avoid unnecessary Option wrapping:**

```scala
// Inefficient
val result = Some(value).map(transform).getOrElse(default)

// Better
val result = if (condition) transform(value) else default
```

**Use views for large collections:**

```scala
// Eager evaluation - multiple passes
val result = list.map(_ * 2).filter(_ > 10).take(5)

// Lazy evaluation - single pass
val result = list.view.map(_ * 2).filter(_ > 10).take(5).toList
```

---

## Best Practices

### Code Organization

1. **Use package objects for package-level definitions:**

```scala
package com.example

package object utils {
  type UserId = Int
  type Result[A] = Either[String, A]

  implicit class StringOps(s: String) {
    def toUserId: UserId = s.toInt
  }
}
```

2. **Companion objects for factory methods:**

```scala
case class User private (name: String, age: Int)

object User {
  def create(name: String, age: Int): Either[String, User] = {
    if (age < 0) Left("Age must be positive")
    else if (name.isEmpty) Left("Name cannot be empty")
    else Right(new User(name, age))
  }
}
```

3. **Sealed traits in same file:**

```scala
// All implementations must be in this file
sealed trait Result[+A]
case class Success[A](value: A) extends Result[A]
case class Failure(error: String) extends Result[Nothing]
case object Pending extends Result[Nothing]
```

### Naming Conventions

- **Classes/Traits:** PascalCase (`UserService`, `HttpClient`)
- **Objects:** PascalCase (`DatabaseConfig`)
- **Methods/Values:** camelCase (`findUser`, `maxRetries`)
- **Type parameters:** Single uppercase letter (`A`, `B`, `T`)
- **Implicits:** Descriptive names (`userOrdering`, `jsonEncoder`)

### Error Handling

**Prefer typed errors over exceptions:**

```scala
// Good
sealed trait UserError
case object UserNotFound extends UserError
case object InvalidEmail extends UserError

def findUser(id: Int): Either[UserError, User] = ???

// Avoid
def findUser(id: Int): User = {
  throw new UserNotFoundException(s"User $id not found")
}
```

---

## Concurrency

Scala provides multiple concurrency models: Futures for simple async operations, Akka actors for complex concurrent systems, and modern effect systems like Cats Effect and ZIO.

### Futures - Basic Async

**Creating and using Futures:**

```scala
import scala.concurrent.{Future, Await}
import scala.concurrent.duration._
import scala.concurrent.ExecutionContext.Implicits.global

// Create Future
val future = Future {
  Thread.sleep(1000)
  42
}

// Transform with map
val doubled = future.map(_ * 2)

// Chain with flatMap
val chained = future.flatMap { value =>
  Future(value + 10)
}

// For-comprehension
val result = for {
  a <- Future(10)
  b <- Future(20)
  c <- Future(30)
} yield a + b + c

// Blocking (avoid in production)
val value = Await.result(future, 5.seconds)
```

**Combining Futures:**

```scala
// Sequence - converts List[Future[A]] to Future[List[A]]
val futures = List(Future(1), Future(2), Future(3))
val combined: Future[List[Int]] = Future.sequence(futures)

// Traverse - map then sequence
val ids = List(1, 2, 3)
val users: Future[List[User]] = Future.traverse(ids)(id => fetchUser(id))

// First completed
val fastest = Future.firstCompletedOf(List(
  fetchFromPrimary(),
  fetchFromBackup()
))

// Recover from failures
val safe = future.recover {
  case _: TimeoutException => 0
  case _: Exception => -1
}

val safeWith = future.recoverWith {
  case _: Exception => fetchFromCache()
}
```

**Promise - explicit completion:**

```scala
import scala.concurrent.Promise

val promise = Promise[Int]()
val future = promise.future

// Complete in another thread
Future {
  Thread.sleep(1000)
  promise.success(42)
}

// Or fail
promise.failure(new Exception("Failed"))

// Try complete (doesn't throw if already completed)
promise.trySuccess(100)
```

### Akka Actors - Message Passing

**Typed actors (Akka Typed):**

```scala
import akka.actor.typed._
import akka.actor.typed.scaladsl.Behaviors

// Define protocol
sealed trait CounterMessage
case object Increment extends CounterMessage
case object Decrement extends CounterMessage
case class GetCount(replyTo: ActorRef[Int]) extends CounterMessage

// Define behavior
def counter(count: Int): Behavior[CounterMessage] = Behaviors.receive { (context, message) =>
  message match {
    case Increment =>
      counter(count + 1)
    case Decrement =>
      counter(count - 1)
    case GetCount(replyTo) =>
      replyTo ! count
      Behaviors.same
  }
}

// Create actor system
val system = ActorSystem(counter(0), "counter-system")

// Send messages
system ! Increment
system ! Increment
```

**Actor patterns:**

```scala
// Ask pattern (request-response)
import akka.actor.typed.scaladsl.AskPattern._
import akka.util.Timeout
import scala.concurrent.duration._

implicit val timeout: Timeout = 3.seconds

val futureCount: Future[Int] = system.ask(ref => GetCount(ref))

// Supervision
def supervisedBehavior(): Behavior[String] = {
  Behaviors.supervise {
    Behaviors.receive[String] { (context, message) =>
      if (message == "fail") throw new Exception("Failed!")
      else Behaviors.same
    }
  }.onFailure[Exception](SupervisorStrategy.restart)
}
```

### Cats Effect - Functional Effects

**IO monad for side effects:**

```scala
import cats.effect._

// Create IO
val printHello: IO[Unit] = IO.println("Hello")
val readLine: IO[String] = IO.readLine

// Compose with for-comprehension
val program = for {
  _ <- IO.println("What's your name?")
  name <- IO.readLine
  _ <- IO.println(s"Hello, $name!")
} yield ()

// Parallel execution
import cats.effect.syntax.parallel._
import cats.syntax.apply._

val parallel = (
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
).parMapN((u1, u2, u3) => List(u1, u2, u3))

// Resource management
def useFile(path: String): IO[String] = {
  Resource.make(
    IO(scala.io.Source.fromFile(path))  // Acquire
  )(source => IO(source.close()))        // Release
    .use(source => IO(source.mkString))  // Use
}

// Error handling
val safeIO = IO.raiseError(new Exception("Error"))
  .handleErrorWith(_ => IO.pure(0))
  .attempt  // Returns IO[Either[Throwable, Int]]
```

**Fibers - lightweight threads:**

```scala
import cats.effect.IO

def task(n: Int): IO[Unit] = IO.sleep(1.second) >> IO.println(s"Task $n")

val program = for {
  fiber1 <- task(1).start  // Start fiber
  fiber2 <- task(2).start
  _ <- fiber1.join         // Wait for completion
  _ <- fiber2.join
} yield ()

// Cancellation
val cancelable = for {
  fiber <- IO.sleep(10.seconds).start
  _ <- IO.sleep(1.second)
  _ <- fiber.cancel  // Cancel after 1 second
} yield ()
```

### ZIO - Effect System

**ZIO basics:**

```scala
import zio._

// Create ZIO
val hello: ZIO[Any, Nothing, Unit] = ZIO.succeed(println("Hello"))
val readLine: ZIO[Any, IOException, String] = ZIO.attempt(scala.io.StdIn.readLine())

// Composition
val program = for {
  _ <- Console.printLine("What's your name?")
  name <- Console.readLine
  _ <- Console.printLine(s"Hello, $name!")
} yield ()

// Parallel execution
val parallel = ZIO.collectAllPar(List(
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
))

// Racing
val raced = fetchFromPrimary() race fetchFromBackup()

// Timeout
val withTimeout = fetchData().timeout(5.seconds)
```

**ZIO Layers - dependency injection:**

```scala
trait UserService {
  def getUser(id: Int): ZIO[Any, Throwable, User]
}

case class UserServiceLive(database: Database) extends UserService {
  def getUser(id: Int): ZIO[Any, Throwable, User] =
    ZIO.attempt(database.query(s"SELECT * FROM users WHERE id = $id"))
}

object UserServiceLive {
  val layer: ZLayer[Database, Nothing, UserService] =
    ZLayer.fromFunction(UserServiceLive.apply _)
}

// Use the service
val program = for {
  user <- ZIO.serviceWithZIO[UserService](_.getUser(123))
  _ <- Console.printLine(s"User: $user")
} yield ()

// Provide dependencies
program.provide(UserServiceLive.layer, DatabaseLive.layer)
```

**See also:** `patterns-concurrency-dev` for cross-language concurrency comparison

---

## Build and Dependencies

Scala uses sbt (Simple Build Tool) as the primary build tool, with Mill as a modern alternative. Dependencies are published to Maven Central and Sonatype.

### sbt - Simple Build Tool

**build.sbt basics:**

```scala
// Project metadata
name := "my-project"
version := "0.1.0"
scalaVersion := "3.3.1"

// Organization (for publishing)
organization := "com.example"

// Dependencies
libraryDependencies ++= Seq(
  "org.typelevel" %% "cats-core" % "2.10.0",
  "org.typelevel" %% "cats-effect" % "3.5.2",
  "com.lihaoyi" %% "upickle" % "3.1.3",

  // Test dependencies
  "org.scalatest" %% "scalatest" % "3.2.17" % Test,
  "org.scalatestplus" %% "mockito-4-11" % "3.2.17.0" % Test
)

// Compiler options (Scala 3)
scalacOptions ++= Seq(
  "-deprecation",
  "-feature",
  "-unchecked",
  "-Xfatal-warnings"
)

// Resolvers (if needed)
resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
```

**Dependency syntax:**

```scala
// %% - Scala version appended automatically
"org.typelevel" %% "cats-core" % "2.10.0"
// Resolves to: org.typelevel:cats-core_3:2.10.0

// % - Exact artifact name (Java libraries)
"com.google.guava" % "guava" % "32.1.3-jre"

// Cross-version dependencies
"org.scala-lang" % "scala-reflect" % scalaVersion.value

// Test scope
"org.scalatest" %% "scalatest" % "3.2.17" % Test

// Provided scope (available at compile, not packaged)
"javax.servlet" % "javax.servlet-api" % "4.0.1" % Provided
```

**Multi-module projects:**

```scala
// build.sbt root project
lazy val root = (project in file("."))
  .aggregate(core, api, client)
  .settings(
    name := "my-project"
  )

lazy val core = (project in file("core"))
  .settings(
    name := "my-project-core",
    libraryDependencies ++= coreDeps
  )

lazy val api = (project in file("api"))
  .dependsOn(core)
  .settings(
    name := "my-project-api",
    libraryDependencies ++= apiDeps
  )

lazy val client = (project in file("client"))
  .dependsOn(core)
  .settings(
    name := "my-project-client"
  )
```

**Common sbt tasks:**

```bash
# Compile
sbt compile

# Run application
sbt run

# Run tests
sbt test

# Interactive mode
sbt
> compile
> test
> ~test  # Watch mode - rerun on file change

# Package JAR
sbt package

# Create fat JAR (with dependencies)
sbt assembly  # Requires sbt-assembly plugin

# Show dependency tree
sbt dependencyTree

# Update dependencies
sbt update

# Clean build
sbt clean

# Publish to local Ivy repository
sbt publishLocal

# Publish to Maven Central
sbt publishSigned
```

**project/plugins.sbt - sbt plugins:**

```scala
// Assembly - fat JAR
addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "2.1.5")

// Coverage
addSbtPlugin("org.scoverage" % "sbt-scoverage" % "2.0.9")

// Publishing
addSbtPlugin("com.github.sbt" % "sbt-pgp" % "2.2.1")
addSbtPlugin("org.xerial.sbt" % "sbt-sonatype" % "3.9.21")

// Formatting
addSbtPlugin("org.scalameta" % "sbt-scalafmt" % "2.5.2")

// Native compilation
addSbtPlugin("org.scala-native" % "sbt-scala-native" % "0.4.16")
```

### Mill - Modern Build Tool

**build.sc (Mill build file):**

```scala
import mill._
import mill.scalalib._

object core extends ScalaModule {
  def scalaVersion = "3.3.1"

  def ivyDeps = Agg(
    ivy"org.typelevel::cats-core:2.10.0",
    ivy"org.typelevel::cats-effect:3.5.2"
  )

  object test extends Tests with TestModule.ScalaTest {
    def ivyDeps = Agg(
      ivy"org.scalatest::scalatest:3.2.17"
    )
  }
}

object api extends ScalaModule {
  def scalaVersion = "3.3.1"
  def moduleDeps = Seq(core)
}
```

**Mill commands:**

```bash
# Compile
mill core.compile

# Run tests
mill core.test

# Run application
mill core.run

# Assembly (fat JAR)
mill core.assembly

# Watch mode
mill -w core.test
```

### Cross-Compilation

**Building for multiple Scala versions:**

```scala
// build.sbt
lazy val core = (project in file("core"))
  .settings(
    name := "my-library",
    crossScalaVersions := Seq("2.12.18", "2.13.12", "3.3.1"),
    scalaVersion := "3.3.1"  // Default
  )
```

```bash
# Compile for all versions
sbt +compile

# Test all versions
sbt +test

# Publish all versions
sbt +publish
```

**Version-specific code:**

```scala
// src/main/scala-2.13/compat.scala
object Compat {
  def collect[A](list: List[Option[A]]): List[A] = list.flatten
}

// src/main/scala-3/compat.scala
object Compat {
  def collect[A](list: List[Option[A]]): List[A] = list.flatten
}
```

### Publishing to Maven Central

**build.sbt publishing configuration:**

```scala
// Metadata
organization := "io.github.username"
homepage := Some(url("https://github.com/username/project"))
scmInfo := Some(
  ScmInfo(
    url("https://github.com/username/project"),
    "scm:git@github.com:username/project.git"
  )
)
developers := List(
  Developer(
    id = "username",
    name = "Your Name",
    email = "you@example.com",
    url = url("https://github.com/username")
  )
)
licenses := Seq("Apache-2.0" -> url("http://www.apache.org/licenses/LICENSE-2.0"))

// Publishing
publishMavenStyle := true
publishTo := {
  val nexus = "https://oss.sonatype.org/"
  if (isSnapshot.value)
    Some("snapshots" at nexus + "content/repositories/snapshots")
  else
    Some("releases" at nexus + "service/local/staging/deploy/maven2")
}

// PGP signing
usePgpKeyHex("YOUR_KEY_ID")
```

---

## Testing

Scala has multiple testing frameworks: ScalaTest (most popular), MUnit (lightweight), specs2 (BDD-style), and ScalaCheck for property-based testing.

### ScalaTest - Comprehensive Testing

**Basic test suites:**

```scala
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class CalculatorSpec extends AnyFlatSpec with Matchers {

  "A Calculator" should "add two numbers" in {
    val calc = new Calculator
    calc.add(2, 3) shouldBe 5
  }

  it should "subtract two numbers" in {
    val calc = new Calculator
    calc.subtract(5, 3) shouldBe 2
  }

  it should "throw on division by zero" in {
    val calc = new Calculator
    assertThrows[ArithmeticException] {
      calc.divide(10, 0)
    }
  }
}
```

**Test styles:**

```scala
// FlatSpec - flat, BDD-style
class UserServiceFlatSpec extends AnyFlatSpec with Matchers {
  "UserService" should "find user by id" in {
    // test
  }
}

// FunSpec - nested describe/it
class UserServiceFunSpec extends AnyFunSpec with Matchers {
  describe("UserService") {
    describe("findById") {
      it("should return user when found") {
        // test
      }
      it("should return None when not found") {
        // test
      }
    }
  }
}

// WordSpec - BDD "should" style
class UserServiceWordSpec extends AnyWordSpec with Matchers {
  "UserService" should {
    "find user by id" in {
      // test
    }
    "handle missing users" in {
      // test
    }
  }
}

// FeatureSpec - acceptance testing
class UserFeatureSpec extends AnyFeatureSpec with GivenWhenThen {
  Feature("User management") {
    Scenario("Creating a new user") {
      Given("a user registration form")
      When("the user submits valid data")
      Then("a new user is created")
    }
  }
}
```

**Matchers:**

```scala
// Equality
result shouldBe 42
result should equal(42)
result shouldEqual 42

// Comparison
value should be > 10
value should be <= 100

// Collections
list should contain(42)
list should have size 5
list shouldBe empty
list should contain allOf (1, 2, 3)
list should contain oneOf (1, 2, 3)

// Options
option shouldBe defined
option shouldBe empty
option should contain(42)

// Strings
string should startWith("Hello")
string should endWith("World")
string should include("middle")
string should fullyMatch regex "\\d+".r

// Exceptions
the [IllegalArgumentException] thrownBy {
  service.process(null)
} should have message "Input cannot be null"

// Custom matchers
val beEven = be >= 0 and (x => x % 2 == 0)
value should beEven
```

**Fixtures and lifecycle:**

```scala
class DatabaseSpec extends AnyFlatSpec with Matchers with BeforeAndAfter {
  var db: Database = _

  before {
    db = Database.connect()
    db.migrate()
  }

  after {
    db.close()
  }

  "Database" should "insert records" in {
    db.insert(Record("test"))
    db.count() shouldBe 1
  }
}

// Or use BeforeAndAfterEach
class ServiceSpec extends AnyFlatSpec with BeforeAndAfterEach {
  override def beforeEach(): Unit = {
    // Setup before each test
  }

  override def afterEach(): Unit = {
    // Cleanup after each test
  }
}
```

### MUnit - Lightweight Testing

**MUnit basics:**

```scala
import munit.FunSuite

class CalculatorSuite extends FunSuite {
  test("addition works") {
    assertEquals(2 + 3, 5)
  }

  test("division by zero fails") {
    intercept[ArithmeticException] {
      10 / 0
    }
  }

  test("async operation".tag(new Tag("async"))) {
    Future(42).map { result =>
      assertEquals(result, 42)
    }
  }
}
```

**Fixtures:**

```scala
class DatabaseSuite extends FunSuite {
  val db = FunFixture[Database](
    setup = { _ => Database.connect() },
    teardown = { db => db.close() }
  )

  db.test("insert works") { db =>
    db.insert(Record("test"))
    assertEquals(db.count(), 1)
  }
}
```

### specs2 - BDD Style

**specs2 basics:**

```scala
import org.specs2.mutable.Specification

class CalculatorSpec extends Specification {
  "Calculator" should {
    "add two numbers" in {
      val calc = new Calculator
      calc.add(2, 3) must_== 5
    }

    "handle division by zero" in {
      val calc = new Calculator
      calc.divide(10, 0) must throwA[ArithmeticException]
    }
  }
}
```

### ScalaCheck - Property-Based Testing

**Property testing basics:**

```scala
import org.scalacheck.Properties
import org.scalacheck.Prop.forAll

object StringProperties extends Properties("String") {

  property("reverse twice is identity") = forAll { (s: String) =>
    s.reverse.reverse == s
  }

  property("length of concatenation") = forAll { (s1: String, s2: String) =>
    (s1 + s2).length == s1.length + s2.length
  }

  property("startsWith") = forAll { (s: String, prefix: String) =>
    (prefix + s).startsWith(prefix)
  }
}
```

**Custom generators:**

```scala
import org.scalacheck.Gen
import org.scalacheck.Arbitrary

case class User(name: String, age: Int)

val genUser: Gen[User] = for {
  name <- Gen.alphaStr
  age <- Gen.choose(0, 120)
} yield User(name, age)

implicit val arbUser: Arbitrary[User] = Arbitrary(genUser)

property("user age is valid") = forAll { (user: User) =>
  user.age >= 0 && user.age <= 120
}
```

**Integration with ScalaTest:**

```scala
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatestplus.scalacheck.ScalaCheckPropertyChecks

class ListPropertiesSpec extends AnyFlatSpec with Matchers with ScalaCheckPropertyChecks {

  "List" should "maintain length on reverse" in {
    forAll { (list: List[Int]) =>
      list.reverse.length shouldBe list.length
    }
  }

  it should "preserve elements on sort" in {
    forAll { (list: List[Int]) =>
      list.sorted.toSet shouldBe list.toSet
    }
  }
}
```

### Mocking

**Using Mockito with ScalaTest:**

```scala
import org.scalatestplus.mockito.MockitoSugar
import org.mockito.Mockito._
import org.mockito.ArgumentMatchers._

class UserServiceSpec extends AnyFlatSpec with MockitoSugar with Matchers {

  "UserService" should "fetch user from repository" in {
    val repo = mock[UserRepository]
    val service = new UserService(repo)

    val user = User("Alice", 30)
    when(repo.findById(123)).thenReturn(Some(user))

    val result = service.getUser(123)

    result shouldBe Some(user)
    verify(repo).findById(123)
  }

  it should "handle repository failures" in {
    val repo = mock[UserRepository]
    val service = new UserService(repo)

    when(repo.findById(anyInt())).thenThrow(new DatabaseException("Connection failed"))

    assertThrows[DatabaseException] {
      service.getUser(123)
    }
  }
}
```

**Using ScalaMock:**

```scala
import org.scalamock.scalatest.MockFactory

class EmailServiceSpec extends AnyFlatSpec with MockFactory with Matchers {

  "EmailService" should "send email via SMTP" in {
    val smtp = mock[SmtpClient]
    val service = new EmailService(smtp)

    (smtp.send _)
      .expects("alice@example.com", "Hello", "Message body")
      .returning(true)
      .once()

    service.sendEmail("alice@example.com", "Hello", "Message body") shouldBe true
  }
}
```

### Async Testing

**Testing Futures:**

```scala
import org.scalatest.concurrent.ScalaFutures
import org.scalatest.time.{Seconds, Span}

class AsyncServiceSpec extends AnyFlatSpec with ScalaFutures with Matchers {
  implicit val patience = PatienceConfig(timeout = Span(5, Seconds))

  "AsyncService" should "fetch data asynchronously" in {
    val future = service.fetchData()

    whenReady(future) { result =>
      result shouldBe "data"
    }
  }

  it should "handle failures" in {
    val future = service.fetchInvalid()

    whenReady(future.failed) { exception =>
      exception shouldBe a [NotFoundException]
    }
  }
}
```

**Testing Cats Effect IO:**

```scala
import cats.effect.testing.scalatest.AsyncIOSpec

class IOServiceSpec extends AsyncIOSpec with Matchers {

  "IOService" should "process data" in {
    service.processData().asserting { result =>
      result shouldBe "processed"
    }
  }

  it should "handle errors" in {
    service.processInvalid().assertThrows[ValidationError]
  }
}
```

---

## Error Handling

Scala provides multiple error handling strategies, from basic Option/Either to advanced effect system error channels. Choose the right abstraction based on your needs.

### Error Handling Strategies

**Comparison of error handling approaches:**

| Strategy | Use Case | Error Info | Composable | Stack Safe |
|----------|----------|------------|------------|------------|
| `Option[A]` | Absence vs presence | No context | Yes | Yes |
| `Either[E, A]` | Typed errors | Custom error type | Yes | Yes |
| `Try[A]` | Exception catching | Throwable | Yes | No |
| `Cats EitherT` | Stacked Either/Future | Custom error type | Yes | Yes |
| `Cats IO` | Effect errors | Throwable | Yes | Yes |
| `ZIO[R, E, A]` | Effect with typed errors | Custom error type | Yes | Yes |
| Scala 3 boundary/break | Early return | Value-based | Limited | Yes |

### Option - Handling Absence

**Basic Option patterns:**

```scala
// Creating Options
val some: Option[Int] = Some(42)
val none: Option[Int] = None
val fromNullable: Option[String] = Option(nullableValue)

// Transforming Options
val doubled = some.map(_ * 2)              // Some(84)
val filtered = some.filter(_ > 50)         // None
val flatMapped = some.flatMap(x => Some(x + 1))  // Some(43)

// Extracting values
val value = some.getOrElse(0)              // 42
val orElse = none.orElse(Some(0))          // Some(0)

// Pattern matching
def describe(opt: Option[Int]): String = opt match {
  case Some(value) if value > 0 => s"Positive: $value"
  case Some(value) => s"Non-positive: $value"
  case None => "No value"
}

// For-comprehension
val result = for {
  a <- Some(1)
  b <- Some(2)
  c <- Some(3)
} yield a + b + c  // Some(6)

// Short-circuits on None
val shortCircuit = for {
  a <- Some(1)
  b <- None  // Stops here
  c <- Some(3)
} yield a + b + c  // None
```

**Advanced Option patterns:**

```scala
// Folding Options
val folded = some.fold(0)(_ * 2)           // 42 * 2 = 84
val foldedNone = none.fold(0)(_ * 2)       // 0

// Collecting from Lists
val list = List(Some(1), None, Some(3), None, Some(5))
val collected = list.flatten               // List(1, 3, 5)

// Traversing Lists to Option
def safeDivide(a: Int, b: Int): Option[Int] =
  if (b == 0) None else Some(a / b)

val divisions = List(10, 20, 30).traverse(safeDivide(_, 5))  // Some(List(2, 4, 6))
val failed = List(10, 20, 30).traverse(safeDivide(_, 0))     // None

// Converting to Either
val asEither: Either[String, Int] = some.toRight("No value")
val asLeft: Either[Int, String] = none.toLeft("Default")
```

### Either - Typed Error Handling

**Either basics (right-biased in Scala 2.12+):**

```scala
// Creating Either values
val success: Either[String, Int] = Right(42)
val failure: Either[String, Int] = Left("Error occurred")

// Transforming Right values
val doubled = success.map(_ * 2)           // Right(84)
val chained = success.flatMap(x => Right(x + 1))  // Right(43)

// Pattern matching
def handle[E, A](either: Either[E, A]): String = either match {
  case Right(value) => s"Success: $value"
  case Left(error) => s"Error: $error"
}

// For-comprehension (short-circuits on Left)
def divide(a: Int, b: Int): Either[String, Int] =
  if (b == 0) Left("Division by zero") else Right(a / b)

val computation = for {
  a <- divide(10, 2)   // Right(5)
  b <- divide(a, 5)    // Right(1)
  c <- divide(b, 1)    // Right(1)
} yield c              // Right(1)

val failed = for {
  a <- divide(10, 2)   // Right(5)
  b <- divide(a, 0)    // Left - stops here
  c <- divide(b, 1)    // Never executed
} yield c              // Left("Division by zero")
```

**Advanced Either patterns:**

```scala
// Custom error types
sealed trait AppError
case class ValidationError(message: String) extends AppError
case class DatabaseError(cause: Throwable) extends AppError
case class NotFoundError(id: String) extends AppError

def findUser(id: String): Either[AppError, User] = {
  if (id.isEmpty) Left(ValidationError("ID cannot be empty"))
  else if (id == "999") Left(NotFoundError(id))
  else Right(User(id, "Name"))
}

// Accumulating errors (requires Cats)
import cats.implicits._

def validateName(name: String): Either[String, String] =
  if (name.nonEmpty) Right(name) else Left("Name is empty")

def validateAge(age: Int): Either[String, Int] =
  if (age >= 0) Right(age) else Left("Age is negative")

// Sequential validation (stops at first error)
val user = for {
  name <- validateName("")     // Stops here
  age <- validateAge(-5)
} yield User(name, age)        // Left("Name is empty")

// Parallel validation (with Validated)
import cats.data.Validated
import cats.data.ValidatedNec  // NonEmptyChain

def validateNameV(name: String): ValidatedNec[String, String] =
  if (name.nonEmpty) Validated.validNec(name) else Validated.invalidNec("Name is empty")

def validateAgeV(age: Int): ValidatedNec[String, Int] =
  if (age >= 0) Validated.validNec(age) else Validated.invalidNec("Age is negative")

val validated = (validateNameV(""), validateAgeV(-5)).mapN(User.apply)
// Invalid(NonEmptyChain("Name is empty", "Age is negative"))

// Converting to Either
validated.toEither  // Left(NonEmptyChain("Name is empty", "Age is negative"))
```

**Either combinators:**

```scala
// Recovering from Left
val recovered = failure.recover {
  case "specific error" => 0
}

val recoveredWith = failure.recoverWith {
  case "error" => Right(0)
}

// Folding
val folded = success.fold(
  error => s"Failed: $error",
  value => s"Success: $value"
)

// Swapping sides
val swapped = success.swap  // Left(42)

// BiMap - transform both sides
val bimapped = success.bimap(
  error => s"Error: $error",
  value => value * 2
)

// Filtering to Option
val filtered = success.filterOrElse(_ > 50, "Too small")  // Left("Too small")
```

### Try - Exception Handling

**Try basics:**

```scala
import scala.util.{Try, Success, Failure}

// Creating Try
val tryValue = Try("123".toInt)            // Success(123)
val tryFailed = Try("abc".toInt)           // Failure(NumberFormatException)

// Pattern matching
tryValue match {
  case Success(value) => println(s"Parsed: $value")
  case Failure(exception) => println(s"Failed: ${exception.getMessage}")
}

// Transforming Success
val doubled = tryValue.map(_ * 2)          // Success(246)

// Chaining operations
val chained = tryValue.flatMap { value =>
  Try(value / 10)
}

// For-comprehension
val computation = for {
  a <- Try("10".toInt)
  b <- Try("5".toInt)
  c <- Try(a / b)
} yield c  // Success(2)

// Short-circuits on Failure
val failed = for {
  a <- Try("10".toInt)
  b <- Try("abc".toInt)  // Failure - stops here
  c <- Try(a / b)
} yield c  // Failure(NumberFormatException)
```

**Try recovery patterns:**

```scala
// Recover with default value
val recovered = tryFailed.recover {
  case _: NumberFormatException => 0
}

// Recover with another Try
val recoveredWith = tryFailed.recoverWith {
  case _: NumberFormatException => Try("456".toInt)
}

// Fallback to another Try
val fallback = tryFailed.orElse(Try("456".toInt))

// Converting to Option and Either
val asOption = tryValue.toOption           // Some(123)
val asEither = tryValue.toEither           // Right(123)

// Filtering
val filtered = tryValue.filter(_ > 100)    // Success(123)
val failedFilter = tryValue.filter(_ > 200)  // Failure(NoSuchElementException)

// Folding
val folded = tryValue.fold(
  exception => s"Error: ${exception.getMessage}",
  value => s"Success: $value"
)
```

### Cats Effect Error Handling

**IO error handling:**

```scala
import cats.effect._

// Creating IO that might fail
val io: IO[Int] = IO.raiseError(new Exception("Failed"))
val successful: IO[Int] = IO.pure(42)

// Handling errors
val handled = io.handleError { error =>
  println(s"Error: ${error.getMessage}")
  0
}

val handledWith = io.handleErrorWith { error =>
  IO.pure(0)
}

// Recovering from specific errors
val recovered = io.recover {
  case _: IllegalArgumentException => 0
}

val recoveredWith = io.recoverWith {
  case _: IllegalArgumentException => IO.pure(0)
}

// Attempt - convert to Either
val attempt: IO[Either[Throwable, Int]] = io.attempt

val processed = attempt.flatMap {
  case Right(value) => IO.println(s"Success: $value")
  case Left(error) => IO.println(s"Error: ${error.getMessage}")
}

// Redeem - handle both success and failure
val redeemed = io.redeem(
  error => s"Failed: ${error.getMessage}",
  value => s"Success: $value"
)

// RedeemWith - effectful version
val redeemedWith = io.redeemWith(
  error => IO.pure(s"Failed: ${error.getMessage}"),
  value => IO.pure(s"Success: $value")
)

// Timeout
val withTimeout = io.timeout(5.seconds)

// Retry
val retried = io.handleErrorWith { error =>
  IO.sleep(1.second) >> io  // Retry after delay
}

// Retry with exponential backoff (requires cats-retry)
import retry._

val policy = RetryPolicies.exponentialBackoff[IO](1.second)
val retriedWithPolicy = retryingOnAllErrors[Int](policy, onError = (_, _) => IO.unit)(io)
```

**MonadError type class:**

```scala
import cats.MonadError
import cats.syntax.all._

def safeDivide[F[_]](a: Int, b: Int)(implicit F: MonadError[F, Throwable]): F[Int] = {
  if (b == 0) F.raiseError(new ArithmeticException("Division by zero"))
  else F.pure(a / b)
}

// Works with any F[_] that has MonadError instance
val ioResult: IO[Int] = safeDivide[IO](10, 2)
val eitherResult: Either[Throwable, Int] = safeDivide[Either[Throwable, *]](10, 2)

// Generic error handling
def handleDivision[F[_]: MonadError[*[_], Throwable]](a: Int, b: Int): F[String] = {
  safeDivide[F](a, b)
    .map(result => s"Result: $result")
    .handleError(error => s"Error: ${error.getMessage}")
}
```

### ZIO Error Channel

**ZIO typed errors:**

```scala
import zio._

// ZIO[R, E, A] - R=environment, E=error type, A=success type
sealed trait AppError
case class ValidationError(message: String) extends AppError
case class DatabaseError(cause: Throwable) extends AppError

// Creating ZIO with typed errors
val success: ZIO[Any, AppError, Int] = ZIO.succeed(42)
val failure: ZIO[Any, AppError, Int] = ZIO.fail(ValidationError("Invalid input"))

// Handling errors
val handled = failure.catchAll { error =>
  error match {
    case ValidationError(msg) => ZIO.succeed(0)
    case DatabaseError(cause) => ZIO.succeed(-1)
  }
}

// Catching specific error types
val catchSome = failure.catchSome {
  case ValidationError(msg) => ZIO.succeed(0)
}

// Converting to Either
val either: ZIO[Any, Nothing, Either[AppError, Int]] = success.either

// Fold - handle both success and failure
val folded = success.fold(
  error => s"Error: $error",
  value => s"Success: $value"
)

// FoldZIO - effectful version
val foldedZIO = success.foldZIO(
  error => ZIO.succeed(s"Error: $error"),
  value => ZIO.succeed(s"Success: $value")
)

// Mapping errors
val mappedError = failure.mapError {
  case ValidationError(msg) => DatabaseError(new Exception(msg))
  case other => other
}

// Retrying
val retried = failure.retry(Schedule.recurs(3))

// Retry with backoff
val retriedWithBackoff = failure.retry(
  Schedule.exponential(1.second) && Schedule.recurs(5)
)

// Timeout
val withTimeout = success.timeout(5.seconds)
```

**Error accumulation with ZIO:**

```scala
import zio._
import zio.prelude.Validation

def validateName(name: String): IO[String, String] =
  if (name.nonEmpty) ZIO.succeed(name) else ZIO.fail("Name is empty")

def validateAge(age: Int): IO[String, Int] =
  if (age >= 0) ZIO.succeed(age) else ZIO.fail("Age is negative")

// Sequential validation (fails fast)
val sequential = for {
  name <- validateName("")     // Fails here
  age <- validateAge(-5)       // Not executed
} yield User(name, age)

// Parallel validation (accumulates errors)
val parallel = ZIO.validatePar(
  validateName(""),
  validateAge(-5)
)(User.apply)  // Fails with both errors

// Using Validation
val validated = Validation.validateWith(
  Validation.fromEither(validateName("").either),
  Validation.fromEither(validateAge(-5).either)
)(User.apply)
```

### For-Comprehension Error Propagation

**Short-circuiting behavior:**

```scala
// Option - short-circuits on None
val optionChain = for {
  a <- Some(1)
  b <- Some(2)
  c <- None        // Stops here
  d <- Some(4)     // Never executed
} yield a + b + c + d  // None

// Either - short-circuits on Left
def divide(a: Int, b: Int): Either[String, Int] =
  if (b == 0) Left("Division by zero") else Right(a / b)

val eitherChain = for {
  a <- divide(10, 2)   // Right(5)
  b <- divide(a, 0)    // Left - stops here
  c <- divide(10, 2)   // Never executed
} yield c              // Left("Division by zero")

// Try - short-circuits on Failure
val tryChain = for {
  a <- Try("10".toInt)
  b <- Try("abc".toInt)  // Failure - stops here
  c <- Try("5".toInt)    // Never executed
} yield a + b + c         // Failure(NumberFormatException)
```

**Mixing error types in for-comprehensions:**

```scala
// Converting between types
val mixed = for {
  a <- Some(10)
  b <- Right(5).toOption  // Convert Either to Option
  c <- Try(a / b).toOption  // Convert Try to Option
} yield c  // Some(2)

// Using EitherT to stack Either and Future
import cats.data.EitherT
import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global

def findUser(id: Int): Future[Either[String, User]] = ???
def findPosts(userId: Int): Future[Either[String, List[Post]]] = ???

val result = for {
  user <- EitherT(findUser(123))
  posts <- EitherT(findPosts(user.id))
} yield (user, posts)

val unwrapped: Future[Either[String, (User, List[Post])]] = result.value
```

### Scala 3 Boundary and Break

**Early return with boundary/break:**

```scala
import scala.util.boundary, boundary.break

// Early return from computation
def findFirst[A](list: List[A])(predicate: A => Boolean): Option[A] = {
  boundary {
    for (elem <- list) {
      if (predicate(elem)) break(Some(elem))
    }
    None
  }
}

findFirst(List(1, 2, 3, 4, 5))(_ > 3)  // Some(4)

// Labeled boundaries
def processData(data: List[Int]): Either[String, Int] = {
  boundary[Either[String, Int]] {
    var sum = 0
    for (value <- data) {
      if (value < 0) break(Left("Negative value found"))
      sum += value
    }
    Right(sum)
  }
}

processData(List(1, 2, -3, 4))  // Left("Negative value found")

// Nested boundaries
def nestedSearch(matrix: List[List[Int]]): Option[Int] = {
  boundary {
    for (row <- matrix) {
      boundary {
        for (elem <- row) {
          if (elem > 10) break(break(Some(elem)))  // Break both boundaries
        }
      }
    }
    None
  }
}

nestedSearch(List(List(1, 2), List(3, 15)))  // Some(15)
```

**Comparison with traditional approaches:**

```scala
// Traditional approach with recursion
def findFirstRecursive[A](list: List[A])(predicate: A => Boolean): Option[A] = {
  list match {
    case Nil => None
    case head :: tail =>
      if (predicate(head)) Some(head)
      else findFirstRecursive(tail)(predicate)
  }
}

// Traditional approach with fold
def findFirstFold[A](list: List[A])(predicate: A => Boolean): Option[A] = {
  list.foldLeft[Option[A]](None) { (acc, elem) =>
    acc.orElse(if (predicate(elem)) Some(elem) else None)
  }
}

// Boundary/break is more imperative and familiar
// Use when converting Java code or for performance-critical loops
```

### Error Handling Best Practices

**Choosing the right abstraction:**

```scala
// Use Option for simple absence/presence
def findUser(id: Int): Option[User] = ???

// Use Either for typed errors
def validateUser(user: User): Either[ValidationError, User] = ???

// Use Try when catching exceptions
def parseJson(json: String): Try[JsonObject] = Try(Json.parse(json))

// Use IO/ZIO for effectful computations
def saveToDatabase(user: User): IO[User] = ???

// Use boundary/break for imperative-style early returns
def processLargeDataset(data: List[Data]): Result = {
  boundary {
    // Complex imperative logic with early returns
  }
}
```

**Error composition:**

```scala
// Combining multiple error-prone operations
def registerUser(data: UserData): Either[AppError, User] = {
  for {
    validated <- validateUserData(data)
    hashed <- hashPassword(validated.password)
    user <- createUser(validated.copy(password = hashed))
    _ <- sendWelcomeEmail(user)
  } yield user
}

// Parallel execution with error accumulation
import cats.implicits._

def validateUserParallel(data: UserData): ValidatedNec[ValidationError, User] = {
  (
    validateName(data.name),
    validateEmail(data.email),
    validateAge(data.age)
  ).mapN(User.apply)
}
```

---

## Metaprogramming

Scala provides powerful metaprogramming capabilities, evolving from Scala 2's macro system to Scala 3's safer and more principled approach with inline, transparent inline, and the new macro system.

### Metaprogramming Evolution

**Scala 2 vs Scala 3 metaprogramming:**

| Feature | Scala 2 | Scala 3 |
|---------|---------|---------|
| **Macros** | def macros (blackbox/whitebox) | inline + quoted code |
| **Compile-time** | Limited | Rich compile-time operations |
| **Type-level** | Shapeless library | Built-in match types, unions |
| **Derivation** | Manual implicit derivation | `derives` keyword |
| **Safety** | Hygiene issues possible | Hygienic by default |
| **Complexity** | High learning curve | More principled |

### Scala 2 Macros (Legacy)

**Def macros (avoid in new code):**

```scala
// Scala 2 blackbox macro example
import scala.language.experimental.macros
import scala.reflect.macros.blackbox.Context

object DebugMacros {
  def debug(value: Any): Unit = macro debugImpl

  def debugImpl(c: Context)(value: c.Expr[Any]): c.Expr[Unit] = {
    import c.universe._

    val valueTree = value.tree
    val valueString = show(valueTree)

    reify {
      println(s"$valueString = ${value.splice}")
    }
  }
}

// Usage
val x = 42
DebugMacros.debug(x + 10)  // Prints: "x + 10 = 52"

// Whitebox macro - can refine return type
def mkArray[T](elements: T*): Array[T] = macro mkArrayImpl[T]

def mkArrayImpl[T: c.WeakTypeTag](c: Context)(elements: c.Expr[T]*): c.Expr[Array[T]] = {
  import c.universe._

  c.Expr[Array[T]](
    q"Array(..${elements.map(_.tree)})"
  )
}
```

**Macro bundles (Scala 2):**

```scala
import scala.language.experimental.macros
import scala.reflect.macros.blackbox

trait JsonMacros {
  val c: blackbox.Context
  import c.universe._

  def encodeImpl[T: c.WeakTypeTag]: c.Expr[JsonEncoder[T]] = {
    val tpe = weakTypeOf[T]

    val fields = tpe.decls.collect {
      case m: MethodSymbol if m.isCaseAccessor =>
        val name = m.name.toString
        val returnType = m.returnType
        q"($name, encode(value.$m))"
    }

    c.Expr[JsonEncoder[T]](q"""
      new JsonEncoder[$tpe] {
        def encode(value: $tpe): Json = Json.obj(..$fields)
      }
    """)
  }
}

object JsonEncoder {
  def derived[T]: JsonEncoder[T] = macro JsonMacrosImpl.encodeImpl[T]
}

class JsonMacrosImpl(val c: blackbox.Context) extends JsonMacros
```

### Scala 3 Inline

**Inline definitions:**

```scala
// Simple inline method
inline def square(x: Int): Int = x * x

// Compiler inlines the code at call site:
val result = square(5)  // Becomes: val result = 5 * 5

// Inline parameters
inline def repeat(inline n: Int)(body: => Unit): Unit = {
  if (n > 0) {
    body
    repeat(n - 1)(body)
  }
}

repeat(3)(println("Hello"))
// Expands to:
// println("Hello")
// println("Hello")
// println("Hello")

// Inline values
inline val DEBUG = true

inline def log(msg: String): Unit = {
  if (DEBUG) println(s"[DEBUG] $msg")
  // If DEBUG is false, entire if-statement is eliminated
}
```

**Inline match (type-based specialization):**

```scala
inline def process[T](value: T): String = inline value match {
  case _: String => s"String: $value"
  case _: Int => s"Int: $value"
  case _: Boolean => s"Boolean: $value"
  case _ => s"Other: $value"
}

// Specialized at compile time
process("hello")  // String: hello
process(42)       // Int: 42

// Inline match on types
inline def defaultValue[T]: T = inline erasedValue[T] match {
  case _: Int => 0.asInstanceOf[T]
  case _: String => "".asInstanceOf[T]
  case _: Boolean => false.asInstanceOf[T]
  case _ => null.asInstanceOf[T]
}
```

**Compile-time operations:**

```scala
import scala.compiletime._

// Compile-time error
inline def requirePositive(inline x: Int): Int = {
  inline if (x <= 0) {
    error("Value must be positive")
  }
  x
}

val good = requirePositive(5)     // OK
// val bad = requirePositive(-1)  // Compile error: Value must be positive

// Compile-time assertions
inline def assertType[T, U](value: T): Unit = {
  inline if (!constValue[T =:= U]) {
    error("Type mismatch")
  }
}

// Summon implicits
inline def summonAll[T <: Tuple]: List[Any] = inline erasedValue[T] match {
  case _: EmptyTuple => Nil
  case _: (t *: ts) => summonInline[t] :: summonAll[ts]
}
```

### Transparent Inline

**Transparent inline for type refinement:**

```scala
// Regular inline - return type is fixed
inline def choose(inline b: Boolean, x: Int, y: String): Any =
  if (b) x else y

val result1 = choose(true, 42, "hello")  // Type: Any

// Transparent inline - return type is refined
transparent inline def chooseT(inline b: Boolean, x: Int, y: String) =
  if (b) x else y

val result2 = chooseT(true, 42, "hello")   // Type: Int
val result3 = chooseT(false, 42, "hello")  // Type: String

// Generic transparent inline
transparent inline def transformOrKeep[T](inline transform: Boolean, value: T) =
  inline if (transform) {
    value.toString
  } else {
    value
  }

val a = transformOrKeep(true, 42)   // Type: String
val b = transformOrKeep(false, 42)  // Type: Int
```

**Type-level computations:**

```scala
// Transparent inline for type-level arithmetic
transparent inline def toIntSingleton(inline x: Int): x.type = x

val five = toIntSingleton(5)  // Type: 5

// Tuple operations
transparent inline def head[T <: Tuple](t: T): Any = inline t match {
  case t: (h *: tail) => t.head
}

val tuple = (1, "hello", true)
val h = head(tuple)  // Type: Int (refined!)

// Dependent types via transparent inline
trait Size[N <: Int]

transparent inline def sizedArray[N <: Int](inline n: N): Array[Int] = {
  new Array[Int](n)
}
```

### Scala 3 Macros

**Quote and splice:**

```scala
import scala.quoted._

// Simple macro
inline def debug(inline expr: Any): Unit = ${debugImpl('expr)}

def debugImpl(expr: Expr[Any])(using Quotes): Expr[Unit] = {
  import quotes.reflect._

  val exprString = expr.show
  '{
    println(s"$exprString = ${$expr}")
  }
}

// Usage
val x = 42
debug(x + 10)  // Prints: "x.+(10) = 52"

// Macro with type parameter
inline def createInstance[T]: T = ${createInstanceImpl[T]}

def createInstanceImpl[T: Type](using Quotes): Expr[T] = {
  import quotes.reflect._

  val tpe = TypeRepr.of[T]
  tpe.classSymbol match {
    case Some(cls) =>
      // Generate code to construct instance
      New(Inferred(tpe)).select(cls.primaryConstructor).appliedToNone.asExprOf[T]
    case None =>
      report.errorAndAbort(s"Cannot create instance of ${tpe.show}")
  }
}
```

**Pattern matching on code:**

```scala
import scala.quoted._

inline def optimize(inline expr: Int): Int = ${optimizeImpl('expr)}

def optimizeImpl(expr: Expr[Int])(using Quotes): Expr[Int] = {
  expr match {
    // Optimize x + 0 to x
    case '{($x: Int) + 0} => x

    // Optimize x * 1 to x
    case '{($x: Int) * 1} => x

    // Optimize x * 0 to 0
    case '{($x: Int) * 0} => '{0}

    // No optimization
    case _ => expr
  }
}

val x = 5
val a = optimize(x + 0)  // Optimized to: x
val b = optimize(x * 1)  // Optimized to: x
val c = optimize(x * 0)  // Optimized to: 0
```

**Generating code:**

```scala
import scala.quoted._

// Generate a method that sums N integers
inline def sumN(inline n: Int): (Int*) => Int = ${sumNImpl('n)}

def sumNImpl(n: Expr[Int])(using Quotes): Expr[(Int*) => Int] = {
  import quotes.reflect._

  n.value match {
    case Some(count) =>
      val params = (1 to count).map(i => s"x$i").toList

      // Generate: (x1, x2, ..., xN) => x1 + x2 + ... + xN
      '{
        (args: Seq[Int]) => args.sum
      }

    case None =>
      report.errorAndAbort("n must be a constant")
  }
}

val sum3 = sumN(3)
sum3(1, 2, 3)  // 6
```

### Type-Level Programming

**Match types:**

```scala
// Type-level pattern matching
type Elem[X] = X match {
  case String => Char
  case Array[t] => t
  case Iterable[t] => t
  case AnyVal => X
}

val charElem: Elem[String] = 'a'
val intElem: Elem[Array[Int]] = 42
val stringElem: Elem[List[String]] = "hello"

// Recursive match types
type LeafElem[X] = X match {
  case String => Char
  case Array[t] => LeafElem[t]
  case Iterable[t] => LeafElem[t]
  case AnyVal => X
}

val deepElem: LeafElem[List[Array[String]]] = 'x'  // Char
```

**Union and intersection types:**

```scala
// Union types
def process(value: Int | String): String = value match {
  case i: Int => s"Int: $i"
  case s: String => s"String: $s"
}

process(42)       // "Int: 42"
process("hello")  // "String: hello"

// Intersection types
trait Readable {
  def read(): String
}

trait Writable {
  def write(data: String): Unit
}

def copy(source: Readable, dest: Writable): Unit = {
  dest.write(source.read())
}

// Require both traits
def processFile(file: Readable & Writable): Unit = {
  val data = file.read()
  file.write(data.toUpperCase)
}
```

**Dependent types:**

```scala
// Path-dependent types
trait Container {
  type Element
  def add(e: Element): Unit
  def get(): Element
}

def transfer(from: Container, to: Container { type Element = from.Element }): Unit = {
  to.add(from.get())
}

// Dependent function types
trait Entry {
  type Key
  def key: Key
}

// Function that returns type dependent on input
val extractKey: (e: Entry) => e.Key = (e: Entry) => e.key

case class StringEntry(key: String) extends Entry {
  type Key = String
}

val entry = StringEntry("test")
val key: String = extractKey(entry)  // Type refined to String
```

**Type-level arithmetic:**

```scala
// Church numerals (compile-time numbers)
sealed trait Nat
case object Zero extends Nat
case class Succ[N <: Nat](n: N) extends Nat

type _0 = Zero.type
type _1 = Succ[_0]
type _2 = Succ[_1]
type _3 = Succ[_2]

// Type-level addition
type Add[N <: Nat, M <: Nat] <: Nat = N match {
  case Zero.type => M
  case Succ[n] => Succ[Add[n, M]]
}

val three: Add[_1, _2] = Succ(Succ(Succ(Zero)))

// Sized collections
case class Vec[N <: Nat, A](values: List[A]) {
  def append[M <: Nat](other: Vec[M, A]): Vec[Add[N, M], A] =
    Vec(values ++ other.values)
}

val vec1 = Vec[_2, Int](List(1, 2))
val vec2 = Vec[_3, Int](List(3, 4, 5))
val vec5: Vec[Add[_2, _3], Int] = vec1.append(vec2)  // Type: Vec[_5, Int]
```

### Derivation with Derives

**Automatic type class derivation:**

```scala
// Define derivable type class
trait Show[T] {
  def show(value: T): String
}

object Show {
  // Primitive instances
  given Show[Int] = (value: Int) => value.toString
  given Show[String] = (value: String) => s"\"$value\""
  given Show[Boolean] = (value: Boolean) => value.toString

  // Derive for case classes
  import scala.deriving._

  inline def derived[T](using m: Mirror.Of[T]): Show[T] = {
    inline m match {
      case p: Mirror.ProductOf[T] => productShow(p)
      case s: Mirror.SumOf[T] => sumShow(s)
    }
  }

  private def productShow[T](p: Mirror.ProductOf[T]): Show[T] = {
    new Show[T] {
      def show(value: T): String = {
        val values = value.asInstanceOf[Product].productIterator.toList
        val labels = constValueTuple[p.MirroredElemLabels].toList
        val fields = labels.zip(values).map { case (label, value) =>
          s"$label = $value"
        }
        s"${constValue[p.MirroredLabel]}(${fields.mkString(", ")})"
      }
    }
  }

  private def sumShow[T](s: Mirror.SumOf[T]): Show[T] = {
    new Show[T] {
      def show(value: T): String = value.toString
    }
  }
}

// Use derives keyword
case class Person(name: String, age: Int) derives Show

val person = Person("Alice", 30)
summon[Show[Person]].show(person)  // "Person(name = Alice, age = 30)"

// Multiple derivations
enum Color derives Show, Eq, Ordering {
  case Red, Green, Blue
}

// Generic derivation
case class Box[T](value: T) derives Show

given [T: Show]: Show[Box[T]] = Show.derived
```

**Common derivable type classes:**

```scala
// Eq - equality
trait Eq[T] {
  def eqv(x: T, y: T): Boolean
}

case class User(id: Int, name: String) derives Eq

val user1 = User(1, "Alice")
val user2 = User(1, "Alice")
summon[Eq[User]].eqv(user1, user2)  // true

// Ordering
case class Score(value: Int) derives Ordering

val scores = List(Score(10), Score(5), Score(20))
scores.sorted  // List(Score(5), Score(10), Score(20))

// Encoder/Decoder (JSON libraries)
import io.circe.Codec

case class Event(id: String, timestamp: Long) derives Codec
// Automatically derives JSON encoder and decoder
```

### Compile-Time Operations

**Compile-time values:**

```scala
import scala.compiletime._

// Extract constant values
inline val SIZE = 100
transparent inline def arraySize: Int = constValue[SIZE.type]

val size: 100 = arraySize  // Type refined to literal 100

// Const operations
transparent inline def add(inline a: Int, inline b: Int): Int = {
  inline val result = constValue[a.type] + constValue[b.type]
  result
}

val sum: 5 = add(2, 3)  // Type refined to 5

// Error reporting
inline def assertPositive(inline x: Int): Int = {
  inline if (constValue[x.type] <= 0) {
    error("Value must be positive at compile time")
  }
  x
}

val good = assertPositive(5)     // OK
// val bad = assertPositive(-1)  // Compile error
```

**Tuple operations:**

```scala
import scala.compiletime.ops.int._

// Type-level size
type Size[T <: Tuple] = T match {
  case EmptyTuple => 0
  case _ *: tail => S[Size[tail]]
}

val size: Size[(Int, String, Boolean)] = 3  // Type: 3

// Type-level concat
type Concat[A <: Tuple, B <: Tuple] <: Tuple = A match {
  case EmptyTuple => B
  case h *: t => h *: Concat[t, B]
}

val concat: Concat[(Int, String), (Boolean, Double)] = (1, "hi", true, 3.14)

// Type-level reverse
type Reverse[T <: Tuple] <: Tuple = T match {
  case EmptyTuple => EmptyTuple
  case h *: t => Concat[Reverse[t], h *: EmptyTuple]
}

val reversed: Reverse[(Int, String, Boolean)] = (true, "hi", 1)
```

**Code generation:**

```scala
import scala.quoted._

// Generate boilerplate code
inline def generateGetters[T]: Unit = ${generateGettersImpl[T]}

def generateGettersImpl[T: Type](using Quotes): Expr[Unit] = {
  import quotes.reflect._

  val tpe = TypeRepr.of[T]
  val fields = tpe.typeSymbol.caseFields

  fields.foreach { field =>
    println(s"def get${field.name.capitalize}(): ${field.termRef.widenTermRefByName.show}")
  }

  '{}
}

case class User(name: String, age: Int, email: String)

generateGetters[User]
// Prints at compile time:
// def getName(): String
// def getAge(): Int
// def getEmail(): String
```

**Compile-time reflection:**

```scala
import scala.quoted._

inline def inspectType[T]: Unit = ${inspectTypeImpl[T]}

def inspectTypeImpl[T: Type](using Quotes): Expr[Unit] = {
  import quotes.reflect._

  val tpe = TypeRepr.of[T]

  println(s"Type: ${tpe.show}")
  println(s"Base classes: ${tpe.baseClasses.map(_.name)}")
  println(s"Members: ${tpe.typeSymbol.declaredMethods.map(_.name)}")

  tpe.typeSymbol.caseFields.foreach { field =>
    println(s"Field: ${field.name}: ${field.termRef.widenTermRefByName.show}")
  }

  '{}
}

case class Person(name: String, age: Int)
inspectType[Person]
// Compile-time output:
// Type: Person
// Base classes: List(Person, Product, Serializable, Equals, Object, Any)
// Members: List(name, age, copy, productElementNames, ...)
// Field: name: String
// Field: age: Int
```

### Metaprogramming Best Practices

**When to use metaprogramming:**

```scala
// Good use cases:
// 1. Eliminating boilerplate
case class User(name: String, age: Int) derives JsonCodec

// 2. Performance optimization
inline def fastSum(xs: Array[Int]): Int = {
  var sum = 0
  var i = 0
  while (i < xs.length) {
    sum += xs(i)
    i += 1
  }
  sum
}

// 3. Type-safe APIs
val query = sql"SELECT * FROM users WHERE id = $userId"  // Compile-time SQL checking

// 4. Configuration validation
inline val config = validateConfig("config.json")  // Compile-time validation

// Bad use cases:
// - Obscuring simple code
// - When runtime reflection would suffice
// - Overly complex type-level programming
```

**Comparison with other languages:**

| Feature | Scala 3 | Rust | Haskell | C++ |
|---------|---------|------|---------|-----|
| Macros | Quote/splice | Procedural/declarative | Template Haskell | Preprocessor |
| Inline | inline keyword | inline attribute | INLINE pragma | inline keyword |
| Type-level | Match types, unions | Traits, associated types | Type families | Template metaprogramming |
| Derivation | derives keyword | derive macros | deriving clause | Not built-in |
| Safety | Hygienic | Hygienic | Hygienic | Not hygienic |

---

## Serialization

Scala has excellent serialization support with multiple libraries for JSON, XML, and binary formats. This section covers common serialization patterns and library choices.

### Library Comparison

| Library | Style | Performance | Type Safety | Derivation |
|---------|-------|-------------|-------------|------------|
| **circe** | FP-first | Good | Excellent | Semi-auto/auto |
| **upickle** | Simple | Excellent | Good | Automatic |
| **play-json** | Familiar | Good | Good | Macro-based |
| **jsoniter-scala** | Performance | Best | Good | Compile-time |
| **zio-json** | ZIO ecosystem | Excellent | Excellent | Derives |

### Circe (Most Popular)

```scala
import io.circe._
import io.circe.generic.semiauto._
import io.circe.syntax._
import io.circe.parser._

// Case class
case class User(name: String, age: Int, email: Option[String])

// Semi-automatic derivation (recommended)
object User {
  implicit val encoder: Encoder[User] = deriveEncoder[User]
  implicit val decoder: Decoder[User] = deriveDecoder[User]
}

// Or combined codec
object User {
  implicit val codec: Codec[User] = deriveCodec[User]
}

// Encoding
val user = User("Alice", 30, Some("alice@example.com"))
val json: Json = user.asJson
val jsonString: String = user.asJson.noSpaces
// {"name":"Alice","age":30,"email":"alice@example.com"}

// Decoding
val parsed: Either[Error, User] = decode[User](jsonString)
parsed match {
  case Right(user) => println(s"Got user: $user")
  case Left(error) => println(s"Parse error: $error")
}

// Custom field names
case class ApiResponse(
  @JsonKey("user_id") userId: Long,
  @JsonKey("created_at") createdAt: String
)
```

### Circe with ADTs

```scala
import io.circe._
import io.circe.generic.semiauto._

// Sealed trait hierarchy
sealed trait PaymentMethod
case class CreditCard(number: String, expiry: String) extends PaymentMethod
case class BankTransfer(iban: String) extends PaymentMethod
case object Cash extends PaymentMethod

object PaymentMethod {
  implicit val encoder: Encoder[PaymentMethod] = deriveEncoder[PaymentMethod]
  implicit val decoder: Decoder[PaymentMethod] = deriveDecoder[PaymentMethod]
}

// Custom discriminator
import io.circe.generic.extras.semiauto._
import io.circe.generic.extras.Configuration

implicit val config: Configuration = Configuration.default
  .withDiscriminator("type")
  .withSnakeCaseMemberNames

// Result: {"type":"CreditCard","number":"1234","expiry":"12/25"}
```

### Upickle (Simple & Fast)

```scala
import upickle.default._

// Automatic derivation for case classes
case class User(name: String, age: Int, email: Option[String])
object User {
  implicit val rw: ReadWriter[User] = macroRW[User]
}

// Or inline
implicit val userRW: ReadWriter[User] = macroRW

// Encoding
val user = User("Alice", 30, Some("alice@example.com"))
val json: String = write(user)
val prettyJson: String = write(user, indent = 2)

// Decoding
val parsed: User = read[User](json)

// Handle errors
val result: Either[Throwable, User] = scala.util.Try(read[User](json)).toEither

// Custom field names
case class ApiUser(
  @key("user_name") userName: String,
  @key("user_age") userAge: Int
)
object ApiUser {
  implicit val rw: ReadWriter[ApiUser] = macroRW
}
```

### Play JSON

```scala
import play.api.libs.json._

// Case class with companion
case class User(name: String, age: Int, email: Option[String])

object User {
  // Automatic format
  implicit val format: Format[User] = Json.format[User]

  // Or separate reads/writes
  implicit val reads: Reads[User] = Json.reads[User]
  implicit val writes: Writes[User] = Json.writes[User]
}

// Encoding
val user = User("Alice", 30, Some("alice@example.com"))
val json: JsValue = Json.toJson(user)
val jsonString: String = Json.stringify(json)

// Decoding
val parsed: JsResult[User] = Json.parse(jsonString).validate[User]
parsed match {
  case JsSuccess(user, _) => println(s"Got user: $user")
  case JsError(errors) => println(s"Errors: $errors")
}

// Custom format
implicit val customFormat: Format[User] = (
  (__ \ "user_name").format[String] and
  (__ \ "user_age").format[Int] and
  (__ \ "email_address").formatNullable[String]
)(User.apply, unlift(User.unapply))
```

### Jsoniter-Scala (High Performance)

```scala
import com.github.plokhotnyuk.jsoniter_scala.core._
import com.github.plokhotnyuk.jsoniter_scala.macros._

case class User(name: String, age: Int, email: Option[String])

// Compile-time codec generation
implicit val codec: JsonValueCodec[User] = JsonCodecMaker.make

// Encoding
val user = User("Alice", 30, Some("alice@example.com"))
val bytes: Array[Byte] = writeToArray(user)
val json: String = writeToString(user)

// Decoding
val parsed: User = readFromString[User](json)
val fromBytes: User = readFromArray[User](bytes)

// Configuration
implicit val customCodec: JsonValueCodec[User] = JsonCodecMaker.make(
  CodecMakerConfig
    .withFieldNameMapper(JsonCodecMaker.EnforcePascalCase)
    .withDiscriminatorFieldName(Some("type"))
)
```

### ZIO JSON

```scala
import zio.json._

case class User(name: String, age: Int, email: Option[String])

object User {
  implicit val encoder: JsonEncoder[User] = DeriveJsonEncoder.gen[User]
  implicit val decoder: JsonDecoder[User] = DeriveJsonDecoder.gen[User]

  // Or combined
  implicit val codec: JsonCodec[User] = DeriveJsonCodec.gen[User]
}

// Encoding
val user = User("Alice", 30, Some("alice@example.com"))
val json: String = user.toJson
val prettyJson: String = user.toJsonPretty

// Decoding
val parsed: Either[String, User] = json.fromJson[User]

// With custom field names
case class ApiUser(
  @jsonField("user_name") userName: String,
  @jsonField("user_age") userAge: Int
)
```

### Validation Patterns

```scala
import io.circe._
import io.circe.generic.semiauto._

// Custom decoder with validation
case class Email private (value: String)

object Email {
  def apply(value: String): Either[String, Email] =
    if (value.contains("@")) Right(new Email(value))
    else Left("Invalid email format")

  implicit val decoder: Decoder[Email] = Decoder.decodeString.emap(apply)
  implicit val encoder: Encoder[Email] = Encoder.encodeString.contramap(_.value)
}

// Refined types integration
import eu.timepit.refined._
import eu.timepit.refined.api.Refined
import eu.timepit.refined.string._

type ValidEmail = String Refined MatchesRegex["^[\\w.-]+@[\\w.-]+\\.[a-z]{2,}$"]

case class User(
  name: String,
  email: ValidEmail,
  age: Int
)

// Accumulating validation with cats
import cats.data.ValidatedNec
import cats.syntax.all._

def validateUser(json: Json): ValidatedNec[String, User] = {
  (
    validateName(json),
    validateEmail(json),
    validateAge(json)
  ).mapN(User.apply)
}
```

### XML Serialization

```scala
import scala.xml._

case class User(name: String, age: Int)

// Manual XML generation
def toXml(user: User): Elem =
  <user>
    <name>{user.name}</name>
    <age>{user.age}</age>
  </user>

// Manual XML parsing
def fromXml(xml: Elem): User = User(
  name = (xml \ "name").text,
  age = (xml \ "age").text.toInt
)

// With scala-xml
val xml = <users>
  <user id="1">
    <name>Alice</name>
    <age>30</age>
  </user>
</users>

val users = (xml \ "user").map { node =>
  User((node \ "name").text, (node \ "age").text.toInt)
}
```

### Binary Formats

```scala
// Protocol Buffers with ScalaPB
// build.sbt: libraryDependencies += "com.thesamet.scalapb" %% "scalapb-runtime" % "..."

// user.proto
// message User {
//   string name = 1;
//   int32 age = 2;
// }

// Generated code usage
import myapp.proto.user.User

val user = User(name = "Alice", age = 30)
val bytes: Array[Byte] = user.toByteArray
val parsed: User = User.parseFrom(bytes)

// Avro with avro4s
import com.sksamuel.avro4s._

case class User(name: String, age: Int)

val schema = AvroSchema[User]
val record = RecordFormat[User].to(User("Alice", 30))
val bytes = AvroOutputStream.binary[User].to(outputStream).write(user).close()

// MessagePack with msgpack4s
import org.msgpack.core._

// Custom binary protocol
trait BinaryCodec[A] {
  def encode(a: A): Array[Byte]
  def decode(bytes: Array[Byte]): A
}
```

### Streaming JSON

```scala
import io.circe.fs2._
import fs2.Stream
import cats.effect.IO

// Stream JSON array
val jsonStream: Stream[IO, Byte] = ???

val users: Stream[IO, User] = jsonStream
  .through(byteStreamParser)
  .through(decoder[IO, User])

// Process large files
import java.nio.file.Paths
import fs2.io.file.Files

Files[IO]
  .readAll(Paths.get("users.json"))
  .through(byteStreamParser)
  .through(decoder[IO, User])
  .evalMap(user => IO(println(user)))
  .compile
  .drain
```

### Best Practices

```scala
// 1. Use semi-automatic derivation for control
object User {
  implicit val codec: Codec[User] = deriveCodec[User]  // Explicit
}

// 2. Define codecs in companion objects
case class User(name: String, age: Int)
object User {
  implicit val codec: Codec[User] = deriveCodec
}

// 3. Use Either for parsing results
def parseUser(json: String): Either[Error, User] = decode[User](json)

// 4. Validate on deserialization
implicit val emailDecoder: Decoder[Email] =
  Decoder.decodeString.emap(Email.apply)

// 5. Use consistent naming conventions
implicit val config: Configuration = Configuration.default
  .withSnakeCaseMemberNames

// 6. Handle optional fields explicitly
case class Config(
  required: String,
  optional: Option[String] = None,
  withDefault: Int = 42
)
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Futures, actors, effects comparison across languages
- `patterns-serialization-dev` - JSON handling, schema validation patterns
- `patterns-metaprogramming-dev` - Macros, implicits, type classes vs other languages

---

## References

### Official Documentation

- **Scala Documentation:** https://docs.scala-lang.org/
- **Scala 3 Book:** https://docs.scala-lang.org/scala3/book/introduction.html
- **API Docs:** https://www.scala-lang.org/api/current/

### Books

- **Programming in Scala (Odersky, Spoon, Venners)**
- **Functional Programming in Scala (Chiusano, Bjarnason)**
- **Scala with Cats (Underscore)**

### Community Resources

- **Scala Center:** https://scala.epfl.ch/
- **Scala Users Forum:** https://users.scala-lang.org/
- **ScalaDex (package index):** https://index.scala-lang.org/

### Build Tools

- **sbt:** https://www.scala-sbt.org/
- **Mill:** https://mill-build.org/
- **Maven:** https://maven.apache.org/
- **Gradle:** https://gradle.org/

### Testing

- **ScalaTest:** https://www.scalatest.org/
- **Specs2:** https://etorreborre.github.io/specs2/
- **MUnit:** https://scalameta.org/munit/
- **ScalaCheck:** https://scalacheck.org/

### Related Skills

When you need specialized functionality:

- **Akka (actors, streams):** Use `lang-scala-akka-dev`
- **Cats (FP library):** Use `lang-scala-cats-dev`
- **ZIO (effects):** Use `lang-scala-zio-dev`
- **Spark (distributed):** Use `lang-scala-spark-dev`
- **Play Framework:** Use `lang-scala-play-dev`
- **Testing:** Use `lang-scala-testing-dev`

---

## Summary

This skill covers **foundational Scala development**:

- Immutability - val vs var, immutable collections
- Pattern matching - case classes, sealed traits, ADTs
- Traits - interfaces with implementation, mixins
- For-comprehensions - monadic composition
- Error handling - Option, Either, Try
- Collections - List, Vector, Set, Map operations
- Higher-order functions - map, filter, fold, composition
- Type system - variance, bounds, type classes
- Common patterns - builder, type classes, cake, ADTs

For specialized topics, route to the appropriate skill from the hierarchy.
