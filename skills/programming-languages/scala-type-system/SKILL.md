---
name: Scala Type System
description: Use when scala's advanced type system including generics, variance, type bounds, implicit conversions, type classes, higher-kinded types, path-dependent types, and abstract type members for building type-safe, flexible APIs.
allowed-tools: []
---

# Scala Type System

## Introduction

Scala features one of the most sophisticated type systems among mainstream
programming languages, combining object-oriented and functional programming
concepts. This advanced type system enables precise modeling of domain concepts,
compile-time verification of complex constraints, and highly reusable abstractions.

Key features include parametric polymorphism (generics), variance annotations,
type bounds, implicit conversions and parameters, type classes, higher-kinded
types, path-dependent types, and abstract type members. These features enable
expressive APIs while maintaining type safety.

This skill covers generics and variance, upper and lower type bounds, view and
context bounds, implicit conversions, type classes, higher-kinded types,
path-dependent types, and practical type-level programming patterns.

## Generics and Type Parameters

Type parameters enable writing reusable code that works with multiple types while
maintaining type safety.

```scala
// Basic generic class
class Box[T](val content: T) {
  def get: T = content
  def map[U](f: T => U): Box[U] = new Box(f(content))
}

val intBox = new Box(42)
val stringBox = new Box("hello")

// Generic methods
def identity[T](x: T): T = x

def swap[A, B](pair: (A, B)): (B, A) = (pair._2, pair._1)

// Multiple type parameters
class Pair[A, B](val first: A, val second: B) {
  def swap: Pair[B, A] = new Pair(second, first)
}

// Generic collections
def first[T](list: List[T]): Option[T] = list.headOption

def last[T](list: List[T]): Option[T] = list.lastOption

// Type parameter constraints with type bounds
class NumberBox[T <: Number](val value: T) {
  def doubleValue: Double = value.doubleValue()
}

// Generic trait
trait Container[T] {
  def add(item: T): Container[T]
  def get: T
  def isEmpty: Boolean
}

class SimpleContainer[T](private var item: Option[T] = None)
  extends Container[T] {
  def add(newItem: T): Container[T] = {
    item = Some(newItem)
    this
  }

  def get: T = item.getOrElse(throw new NoSuchElementException)

  def isEmpty: Boolean = item.isEmpty
}

// Generic companion object
object Container {
  def empty[T]: Container[T] = new SimpleContainer[T]()

  def of[T](item: T): Container[T] = new SimpleContainer[T](Some(item))
}

// Type parameter inference
val box1 = new Box(42)           // Box[Int]
val box2 = new Box("hello")      // Box[String]
val list1 = List(1, 2, 3)        // List[Int]

// Explicit type parameters when needed
val box3 = new Box[Any](42)
val emptyList = List.empty[String]

// Generic functions with multiple constraints
def max[T](a: T, b: T)(implicit ord: Ordering[T]): T =
  if (ord.gt(a, b)) a else b

println(max(5, 10))              // 10
println(max("apple", "banana"))  // banana

// Type aliases for complex generic types
type StringMap[V] = Map[String, V]
type IntPair = (Int, Int)

val userAges: StringMap[Int] = Map("Alice" -> 30, "Bob" -> 25)
val point: IntPair = (10, 20)
```

Generics enable writing code once and reusing it with multiple types while
maintaining compile-time type safety.

## Variance Annotations

Variance controls how parameterized types relate to each other based on their
type parameters' subtyping relationships.

```scala
// Covariance (+T): if A <: B, then Container[A] <: Container[B]
class CovariantBox[+T](val content: T) {
  def get: T = content
  // Can't have T in contravariant position (method parameters)
  // def set(item: T): Unit = ???  // Won't compile
}

class Animal
class Dog extends Animal
class Cat extends Animal

val dogBox: CovariantBox[Dog] = new CovariantBox(new Dog)
val animalBox: CovariantBox[Animal] = dogBox  // Valid due to covariance

// Contravariance (-T): if A <: B, then Container[B] <: Container[A]
trait Printer[-T] {
  def print(item: T): Unit
}

class AnimalPrinter extends Printer[Animal] {
  def print(animal: Animal): Unit = println("Animal")
}

val animalPrinter: Printer[Animal] = new AnimalPrinter
val dogPrinter: Printer[Dog] = animalPrinter  // Valid due to contravariance

// Invariance (T): no subtyping relationship
class InvariantBox[T](private var content: T) {
  def get: T = content
  def set(item: T): Unit = { content = item }
}

// Practical variance example: Function1
trait Function1[-T, +R] {
  def apply(v: T): R
}

val animalToString: Function1[Animal, String] = animal => "Animal"
val dogToAny: Function1[Dog, Any] = animalToString  // Valid

// Collections variance
val dogs: List[Dog] = List(new Dog, new Dog)
val animals: List[Animal] = dogs  // List is covariant

// Mutable collections are invariant
val dogArray: Array[Dog] = Array(new Dog)
// val animalArray: Array[Animal] = dogArray  // Won't compile

// Option is covariant
val someDog: Option[Dog] = Some(new Dog)
val someAnimal: Option[Animal] = someDog  // Valid

// Variance with multiple type parameters
class Function2[-T1, -T2, +R] {
  def apply(v1: T1, v2: T2): R = ???
}

// Variance bounds in definition
class Box[+T](val content: T) {
  // Use lower bound to allow contravariant position
  def set[U >: T](item: U): Box[U] = new Box(item)
}

// Either is covariant in both parameters
sealed trait Either[+A, +B]
case class Left[A](value: A) extends Either[A, Nothing]
case class Right[B](value: B) extends Either[Nothing, B]

val rightInt: Either[String, Int] = Right(42)
val rightAny: Either[String, Any] = rightInt  // Valid
```

Variance annotations make parameterized types more flexible while maintaining
type safety, especially for immutable containers.

## Type Bounds

Type bounds constrain type parameters to specific type hierarchies, enabling
type-safe operations on generic types.

```scala
// Upper type bound (T <: Upper)
def findMax[T <: Ordered[T]](list: List[T]): Option[T] = {
  if (list.isEmpty) None
  else Some(list.reduce((a, b) => if (a > b) a else b))
}

// Lower type bound (T >: Lower)
class Animal
class Dog extends Animal

class Container[+T] {
  def add[U >: T](item: U): Container[U] = ???
}

// Using both bounds together
def cloneAndReset[T >: Null <: Cloneable](obj: T): T = {
  val cloned = obj.clone().asInstanceOf[T]
  cloned
}

// Complex type bounds
trait Comparable[T] {
  def compareTo(that: T): Int
}

def sort[T <: Comparable[T]](list: List[T]): List[T] =
  list.sortWith(_.compareTo(_) < 0)

// Multiple bounds with 'with'
trait Loggable {
  def log(): Unit
}

trait Serializable {
  def serialize(): String
}

def process[T <: Loggable with Serializable](item: T): String = {
  item.log()
  item.serialize()
}

// Recursive type bounds (F-bounded polymorphism)
trait Comparable2[T <: Comparable2[T]] { self: T =>
  def compare(that: T): Int
}

class Person(val name: String, val age: Int) extends Comparable2[Person] {
  def compare(that: Person): Int = this.age - that.age
}

// View bounds (deprecated but useful to understand)
// def sum[T <% Ordered[T]](list: List[T]): T = ???

// Context bounds (modern approach)
def sum[T: Numeric](list: List[T]): T = {
  val numeric = implicitly[Numeric[T]]
  list.foldLeft(numeric.zero)(numeric.plus)
}

println(sum(List(1, 2, 3)))           // 6
println(sum(List(1.5, 2.5, 3.0)))     // 7.0

// Multiple context bounds
def print[T: Ordering: Numeric](list: List[T]): Unit = {
  val ord = implicitly[Ordering[T]]
  val num = implicitly[Numeric[T]]
  println(s"Max: ${list.max(ord)}, Sum: ${sum(list)}")
}

// Abstract type members with bounds
trait Container2 {
  type Content <: AnyRef
  def get: Content
}

class StringContainer extends Container2 {
  type Content = String
  def get: String = "hello"
}

// Type bounds with variance
class Box[+T] {
  def put[U >: T](item: U): Box[U] = new Box[U]
}

// Existential types (less common)
def processAnyBox(box: Box[_]): Unit = {
  println("Processing box")
}

// Type bounds for type classes
trait Show[T] {
  def show(value: T): String
}

def display[T: Show](value: T): String = {
  val shower = implicitly[Show[T]]
  shower.show(value)
}

implicit val intShow: Show[Int] = (value: Int) => value.toString
implicit val stringShow: Show[String] = (value: String) => s"\"$value\""

println(display(42))        // "42"
println(display("hello"))   // "\"hello\""
```

Type bounds enable precise constraints on generic types while maintaining
flexibility and type safety.

## Implicit Conversions and Parameters

Implicits enable automatic type conversions, provide evidence of type
relationships, and inject dependencies.

```scala
// Implicit conversions
implicit def intToString(x: Int): String = x.toString

val s: String = 42  // Automatically converts via implicit

// Extension methods via implicit classes
implicit class RichInt(val value: Int) extends AnyVal {
  def times(f: => Unit): Unit = {
    (1 to value).foreach(_ => f)
  }

  def squared: Int = value * value
}

5.times(println("Hello"))
println(10.squared)  // 100

// Implicit parameters
def greet(name: String)(implicit greeting: String): String =
  s"$greeting, $name!"

implicit val defaultGreeting: String = "Hello"
println(greet("Alice"))  // "Hello, Alice!"

// Multiple implicit parameters
def format(value: Double)(implicit precision: Int, prefix: String): String =
  s"$prefix${BigDecimal(value).setScale(precision, BigDecimal.RoundingMode.HALF_UP)}"

implicit val precision: Int = 2
implicit val prefix: String = "$"

println(format(123.456))  // "$123.46"

// Implicit parameters for type classes
trait Monoid[T] {
  def empty: T
  def combine(a: T, b: T): T
}

implicit val intMonoid: Monoid[Int] = new Monoid[Int] {
  def empty: Int = 0
  def combine(a: Int, b: Int): Int = a + b
}

implicit val stringMonoid: Monoid[String] = new Monoid[String] {
  def empty: String = ""
  def combine(a: String, b: String): String = a + b
}

def combineAll[T](list: List[T])(implicit monoid: Monoid[T]): T =
  list.foldLeft(monoid.empty)(monoid.combine)

println(combineAll(List(1, 2, 3)))           // 6
println(combineAll(List("a", "b", "c")))     // "abc"

// Implicit evidence
def listToString[T](list: List[T])(implicit ev: T =:= String): String =
  list.mkString(", ")

println(listToString(List("a", "b", "c")))
// println(listToString(List(1, 2, 3)))  // Won't compile

// Type constraints
def onlyNumbers[T](value: T)(implicit ev: T <:< Number): Double =
  value.doubleValue()

// Implicit resolution
object Implicits {
  implicit val defaultTimeout: Int = 5000
}

def fetchData(url: String)(implicit timeout: Int): String = {
  s"Fetching $url with timeout $timeout"
}

import Implicits._
println(fetchData("http://example.com"))

// Implicit classes for DSLs
implicit class StringOps(val s: String) extends AnyVal {
  def toIntOpt: Option[Int] = try Some(s.toInt)
    catch { case _: Exception => None }
}

println("123".toIntOpt)   // Some(123)
println("abc".toIntOpt)   // None

// Implicit conversions for numeric types
implicit def intToRational(x: Int): Rational = Rational(x, 1)

case class Rational(numerator: Int, denominator: Int) {
  def +(that: Rational): Rational =
    Rational(
      numerator * that.denominator + that.numerator * denominator,
      denominator * that.denominator
    )
}

val r = Rational(1, 2) + 3  // 3 converted to Rational(3, 1)
```

Implicits enable powerful patterns like extension methods, type classes, and
dependency injection while maintaining type safety.

## Type Classes

Type classes provide ad-hoc polymorphism, enabling extension of types without
modification and separation of concerns.

```scala
// Define type class
trait Show[T] {
  def show(value: T): String
}

// Implement instances
object Show {
  implicit val intShow: Show[Int] = new Show[Int] {
    def show(value: Int): String = value.toString
  }

  implicit val stringShow: Show[String] = new Show[String] {
    def show(value: String): String = s"\"$value\""
  }

  implicit val boolShow: Show[Boolean] = new Show[Boolean] {
    def show(value: Boolean): String = value.toString
  }

  // Generic instance for List
  implicit def listShow[T: Show]: Show[List[T]] = new Show[List[T]] {
    def show(list: List[T]): String = {
      val shower = implicitly[Show[T]]
      list.map(shower.show).mkString("[", ", ", "]")
    }
  }

  // Syntax for convenient usage
  implicit class ShowOps[T](val value: T) extends AnyVal {
    def show(implicit shower: Show[T]): String = shower.show(value)
  }
}

import Show._

println(42.show)                    // "42"
println("hello".show)               // "\"hello\""
println(List(1, 2, 3).show)         // "[1, 2, 3]"

// Ordering type class
trait Ord[T] {
  def compare(a: T, b: T): Int
  def lt(a: T, b: T): Boolean = compare(a, b) < 0
  def gt(a: T, b: T): Boolean = compare(a, b) > 0
}

object Ord {
  implicit val intOrd: Ord[Int] = new Ord[Int] {
    def compare(a: Int, b: Int): Int = a - b
  }

  implicit val stringOrd: Ord[String] = new Ord[String] {
    def compare(a: String, b: String): Int = a.compareTo(b)
  }
}

def sort[T: Ord](list: List[T]): List[T] = {
  val ord = implicitly[Ord[T]]
  list.sortWith((a, b) => ord.lt(a, b))
}

// JSON serialization type class
trait JsonWriter[T] {
  def write(value: T): String
}

object JsonWriter {
  implicit val intWriter: JsonWriter[Int] =
    (value: Int) => value.toString

  implicit val stringWriter: JsonWriter[String] =
    (value: String) => s""""$value""""

  implicit val boolWriter: JsonWriter[Boolean] =
    (value: Boolean) => value.toString

  implicit def listWriter[T: JsonWriter]: JsonWriter[List[T]] =
    (list: List[T]) => {
      val writer = implicitly[JsonWriter[T]]
      list.map(writer.write).mkString("[", ",", "]")
    }

  implicit def mapWriter[T: JsonWriter]: JsonWriter[Map[String, T]] =
    (map: Map[String, T]) => {
      val writer = implicitly[JsonWriter[T]]
      map.map { case (k, v) => s""""$k":${writer.write(v)}""" }
        .mkString("{", ",", "}")
    }
}

def toJson[T: JsonWriter](value: T): String = {
  implicitly[JsonWriter[T]].write(value)
}

// Functor type class
trait Functor[F[_]] {
  def map[A, B](fa: F[A])(f: A => B): F[B]
}

object Functor {
  implicit val listFunctor: Functor[List] = new Functor[List] {
    def map[A, B](fa: List[A])(f: A => B): List[B] = fa.map(f)
  }

  implicit val optionFunctor: Functor[Option] = new Functor[Option] {
    def map[A, B](fa: Option[A])(f: A => B): Option[B] = fa.map(f)
  }
}

def increment[F[_]: Functor](container: F[Int]): F[Int] = {
  implicitly[Functor[F]].map(container)(_ + 1)
}

println(increment(List(1, 2, 3)))      // List(2, 3, 4)
println(increment(Some(5)))            // Some(6)

// Semigroup and Monoid type classes
trait Semigroup[T] {
  def combine(a: T, b: T): T
}

trait Monoid[T] extends Semigroup[T] {
  def empty: T
}

object Monoid {
  implicit val intMonoid: Monoid[Int] = new Monoid[Int] {
    def empty: Int = 0
    def combine(a: Int, b: Int): Int = a + b
  }

  implicit val stringMonoid: Monoid[String] = new Monoid[String] {
    def empty: String = ""
    def combine(a: String, b: String): String = a + b
  }

  implicit def listMonoid[T]: Monoid[List[T]] = new Monoid[List[T]] {
    def empty: List[T] = List.empty
    def combine(a: List[T], b: List[T]): List[T] = a ++ b
  }
}

def fold[T: Monoid](list: List[T]): T = {
  val monoid = implicitly[Monoid[T]]
  list.foldLeft(monoid.empty)(monoid.combine)
}

println(fold(List(1, 2, 3)))           // 6
println(fold(List("a", "b", "c")))     // "abc"
```

Type classes enable adding functionality to existing types without modification
and provide compile-time polymorphism.

## Higher-Kinded Types

Higher-kinded types abstract over type constructors, enabling generic programming
over container types.

```scala
// Higher-kinded type parameter (F[_])
trait Container[F[_]] {
  def wrap[A](value: A): F[A]
}

object Container {
  implicit val listContainer: Container[List] = new Container[List] {
    def wrap[A](value: A): List[A] = List(value)
  }

  implicit val optionContainer: Container[Option] = new Container[Option] {
    def wrap[A](value: A): Option[A] = Some(value)
  }
}

def wrapValue[F[_]: Container, A](value: A): F[A] =
  implicitly[Container[F]].wrap(value)

println(wrapValue[List, Int](42))      // List(42)
println(wrapValue[Option, String]("hi"))  // Some(hi)

// Functor with higher-kinded types
trait Functor[F[_]] {
  def map[A, B](fa: F[A])(f: A => B): F[B]
}

object Functor {
  implicit val listFunctor: Functor[List] = new Functor[List] {
    def map[A, B](fa: List[A])(f: A => B): List[B] = fa.map(f)
  }
}

def transformContainer[F[_]: Functor, A, B](container: F[A])(f: A => B): F[B] =
  implicitly[Functor[F]].map(container)(f)

// Monad with higher-kinded types
trait Monad[F[_]] {
  def pure[A](value: A): F[A]
  def flatMap[A, B](fa: F[A])(f: A => F[B]): F[B]

  def map[A, B](fa: F[A])(f: A => B): F[B] =
    flatMap(fa)(a => pure(f(a)))
}

object Monad {
  implicit val optionMonad: Monad[Option] = new Monad[Option] {
    def pure[A](value: A): Option[A] = Some(value)
    def flatMap[A, B](fa: Option[A])(f: A => Option[B]): Option[B] =
      fa.flatMap(f)
  }

  implicit val listMonad: Monad[List] = new Monad[List] {
    def pure[A](value: A): List[A] = List(value)
    def flatMap[A, B](fa: List[A])(f: A => List[B]): List[B] =
      fa.flatMap(f)
  }
}

def sequenceOperations[F[_]: Monad, A, B, C](
  fa: F[A],
  f: A => F[B],
  g: B => F[C]
): F[C] = {
  val monad = implicitly[Monad[F]]
  monad.flatMap(fa)(a => monad.flatMap(f(a))(g))
}

// Traverse type class
trait Traverse[F[_]] {
  def traverse[G[_]: Monad, A, B](fa: F[A])(f: A => G[B]): G[F[B]]
}

// Applicative with higher-kinded types
trait Applicative[F[_]] {
  def pure[A](value: A): F[A]
  def ap[A, B](ff: F[A => B])(fa: F[A]): F[B]

  def map2[A, B, C](fa: F[A], fb: F[B])(f: (A, B) => C): F[C] =
    ap(map(fa)(a => (b: B) => f(a, b)))(fb)

  def map[A, B](fa: F[A])(f: A => B): F[B] =
    ap(pure(f))(fa)
}

// Free monad pattern
sealed trait Free[F[_], A]
case class Pure[F[_], A](value: A) extends Free[F, A]
case class FlatMap[F[_], A, B](fa: Free[F, A], f: A => Free[F, B])
  extends Free[F, B]
case class Suspend[F[_], A](fa: F[A]) extends Free[F, A]
```

Higher-kinded types enable abstracting over effect types and writing highly
generic, reusable code.

## Path-Dependent Types and Abstract Type Members

Path-dependent types tie type definitions to specific instances, enabling
precise type relationships.

```scala
// Path-dependent types
class Outer {
  class Inner {
    def greet(): String = "Hello from Inner"
  }

  val inner = new Inner
}

val outer1 = new Outer
val outer2 = new Outer

val inner1: outer1.Inner = new outer1.Inner
// val inner2: outer1.Inner = new outer2.Inner  // Won't compile - different paths

// Abstract type members
trait Container3 {
  type Content
  def get: Content
  def set(value: Content): Unit
}

class StringContainer extends Container3 {
  type Content = String
  private var value: String = ""

  def get: String = value
  def set(newValue: String): Unit = { value = newValue }
}

class IntContainer extends Container3 {
  type Content = Int
  private var value: Int = 0

  def get: Int = value
  def set(newValue: Int): Unit = { value = newValue }
}

// Using abstract type members
def transfer(from: Container3,
             to: Container3 { type Content = from.Content }): Unit = {
  to.set(from.get)
}

// Type refinement
trait Animal2 {
  type SuitableFood
  def eat(food: SuitableFood): Unit
}

class Grass
class Meat

class Cow extends Animal2 {
  type SuitableFood = Grass
  def eat(food: Grass): Unit = println("Cow eats grass")
}

class Lion extends Animal2 {
  type SuitableFood = Meat
  def eat(food: Meat): Unit = println("Lion eats meat")
}

// Self-type annotations
trait User2 {
  def username: String
}

trait Tweeter {
  self: User2 =>  // Self-type: Tweeter requires User2
  def tweet(message: String): String = s"$username: $message"
}

class Account(val username: String) extends User2 with Tweeter

val account = new Account("alice")
println(account.tweet("Hello!"))

// Family polymorphism
trait Graph {
  type Node
  type Edge

  def addNode(node: Node): Unit
  def addEdge(edge: Edge): Unit
}

class DirectedGraph extends Graph {
  type Node = String
  type Edge = (String, String)

  def addNode(node: String): Unit = println(s"Adding node: $node")
  def addEdge(edge: (String, String)): Unit =
    println(s"Adding edge: ${edge._1} -> ${edge._2}")
}
```

Path-dependent types and abstract type members enable sophisticated type
relationships and family polymorphism patterns.

## Best Practices

1. **Use variance annotations appropriately** on immutable containers for
   flexibility while avoiding on mutable ones

2. **Prefer abstract type members** over type parameters when modeling families
   of related types

3. **Apply context bounds** for type class constraints to keep signatures clean
   and readable

4. **Use implicit classes** for extension methods rather than implicit
   conversions for safety

5. **Make implicit parameters explicit** in public APIs for clarity and
   documentation

6. **Leverage type bounds** to constrain generic types and enable type-safe
   operations

7. **Define type classes in companion objects** to enable automatic implicit
   resolution

8. **Use sealed traits with case classes** for ADTs to ensure exhaustive pattern
   matching

9. **Apply higher-kinded types** when abstracting over effect types like Future,
   Option, or Either

10. **Keep implicit scope small** to avoid resolution conflicts and maintain
    predictability

## Common Pitfalls

1. **Overusing implicits** makes code hard to understand and debug due to hidden
   conversions

2. **Forgetting variance annotations** on immutable containers loses flexibility
   in APIs

3. **Using upper bounds exclusively** when lower bounds needed causes compilation
   errors

4. **Creating ambiguous implicits** in scope causes resolution failures and
   confusing errors

5. **Not marking implicit conversions** with proper naming conventions makes code
   unclear

6. **Applying covariance to mutable containers** breaks type safety and enables
   runtime errors

7. **Overcomplicating with higher-kinded types** prematurely adds complexity
   without clear benefits

8. **Not using type aliases** for complex generic types reduces readability
   significantly

9. **Mixing path-dependent types** carelessly causes type incompatibility issues

10. **Forgetting type class coherence** by defining multiple instances causes
    unpredictable behavior

## When to Use This Skill

Apply advanced type system features when building reusable libraries and
frameworks requiring flexibility.

Use variance annotations when designing immutable container types or APIs that
should accept subtypes.

Leverage type classes when extending third-party types without modification or
providing ad-hoc polymorphism.

Apply higher-kinded types when abstracting over effect types in functional
programming patterns.

Use path-dependent types when modeling relationships between types tied to
specific instances.

Employ abstract type members when designing APIs with families of related types.

## Resources

- [Scala Language Specification - Types](<https://scala-lang.org/files/archive/spec/2.13/03-types.html>)
- [Scala Documentation - Generics](<https://docs.scala-lang.org/tour/generic-classes.html>)
- [Type Classes in Scala](<https://scalac.io/blog/typeclasses-in-scala/>)
- [Higher-Kinded Types Guide](<https://www.atlassian.com/blog/archives/scala-types-of-a-higher-kind>)
- [Scala with Cats - Type Classes](<https://underscore.io/books/scala-with-cats/>)
