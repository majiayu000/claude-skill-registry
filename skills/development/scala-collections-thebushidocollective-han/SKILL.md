---
name: Scala Collections
description: Use when scala collections including immutable/mutable variants, List, Vector, Set, Map operations, collection transformations, lazy evaluation with views, parallel collections, and custom collection builders for efficient data processing.
allowed-tools: []
---

# Scala Collections

## Introduction

Scala's collections library is one of its most powerful features, providing a
rich, unified API for working with sequences, sets, and maps. The library
emphasizes immutability by default while offering mutable alternatives when
needed for performance-critical code.

The collections hierarchy distinguishes between immutable and mutable variants,
with immutable collections being the default. Key collection types include List,
Vector, Set, Map, Array, and their specialized variants. The library provides
consistent transformation operations across all collection types.

This skill covers immutable vs mutable collections, sequences (List, Vector,
Array), sets and maps, collection operations (map, filter, fold), for-comprehensions,
lazy evaluation, parallel collections, and performance characteristics.

## Immutable vs Mutable Collections

Immutable collections provide thread safety and predictability, while mutable
collections offer performance benefits for intensive updates.

```scala
// Immutable List (default)
val immutableList = List(1, 2, 3, 4, 5)
val newList = immutableList :+ 6  // Creates new list
val prepended = 0 :: immutableList  // Prepends element

// Original unchanged
println(immutableList)  // List(1, 2, 3, 4, 5)
println(newList)        // List(1, 2, 3, 4, 5, 6)

// Mutable ListBuffer
import scala.collection.mutable

val mutableList = mutable.ListBuffer(1, 2, 3)
mutableList += 4        // Mutates in place
mutableList ++= List(5, 6)
mutableList -= 2

println(mutableList)    // ListBuffer(1, 3, 4, 5, 6)

// Immutable Set
val immutableSet = Set(1, 2, 3)
val addedSet = immutableSet + 4
val removedSet = immutableSet - 2

// Mutable Set
val mutableSet = mutable.Set(1, 2, 3)
mutableSet += 4
mutableSet -= 2

// Immutable Map
val immutableMap = Map("a" -> 1, "b" -> 2, "c" -> 3)
val updatedMap = immutableMap + ("d" -> 4)
val removedMap = immutableMap - "b"

// Mutable Map
val mutableMap = mutable.Map("a" -> 1, "b" -> 2)
mutableMap("c") = 3
mutableMap += ("d" -> 4)
mutableMap -= "b"

// Converting between immutable and mutable
val immutable = List(1, 2, 3)
val asMutable = immutable.toBuffer  // Mutable copy
asMutable += 4

val backToImmutable = asMutable.toList

// Immutable Vector (efficient random access)
val vector = Vector(1, 2, 3, 4, 5)
val updatedVector = vector.updated(2, 10)  // Efficiently creates new vector

// Choosing between immutable and mutable
// Use immutable for:
// - Default choice
// - Concurrent access
// - Functional transformations
// - Public APIs

// Use mutable for:
// - Performance-critical loops
// - Large-scale updates
// - Local scope only
// - Builder patterns

// Builder pattern with immutable result
def buildList(): List[Int] = {
  val builder = List.newBuilder[Int]
  for (i <- 1 to 100) {
    builder += i
  }
  builder.result()
}

// Immutable collection with updates
case class User(name: String, age: Int, email: String)

val users = List(
  User("Alice", 30, "alice@example.com"),
  User("Bob", 25, "bob@example.com")
)

val updatedUsers = users.map { user =>
  if (user.name == "Alice") user.copy(age = 31)
  else user
}
```

Prefer immutable collections by default for safety and simplicity, using mutable
collections only when profiling shows performance bottlenecks.

## Sequences: List, Vector, and Array

Different sequence types offer varying performance characteristics for different
access patterns.

```scala
// List: Linked list, O(1) prepend, O(n) random access
val list = List(1, 2, 3, 4, 5)

val prepended = 0 :: list           // O(1)
val concatenated = list ::: List(6, 7)  // O(n)
val appended = list :+ 6            // O(n)

// Pattern matching on lists
def sumList(list: List[Int]): Int = list match {
  case Nil => 0
  case head :: tail => head + sumList(tail)
}

// List construction
val range = List.range(1, 11)       // List(1, 2, ..., 10)
val filled = List.fill(5)(0)        // List(0, 0, 0, 0, 0)
val tabulated = List.tabulate(5)(i => i * i)  // List(0, 1, 4, 9, 16)

// Vector: Indexed sequence, O(log32 n) for all operations
val vector = Vector(1, 2, 3, 4, 5)

val vectorUpdated = vector.updated(2, 10)  // O(log n)
val vectorAppended = vector :+ 6            // O(log n)
val vectorPrepended = 0 +: vector           // O(log n)

// Random access
println(vector(3))  // O(log n) - efficient

// Vector is better for:
// - Random access
// - Both-end operations
// - Large collections

// Array: Mutable, fixed-size, O(1) random access
val array = Array(1, 2, 3, 4, 5)

array(2) = 10  // Mutable update
println(array.mkString(", "))

// Array operations return Arrays
val doubled = array.map(_ * 2)

// ArrayBuffer: Mutable, resizable
import scala.collection.mutable.ArrayBuffer

val buffer = ArrayBuffer(1, 2, 3)
buffer += 4
buffer ++= Array(5, 6)
buffer.insert(0, 0)
buffer.remove(2)

// Seq: General sequence trait
def processSeq(seq: Seq[Int]): Int = seq.sum

println(processSeq(List(1, 2, 3)))
println(processSeq(Vector(1, 2, 3)))
println(processSeq(Array(1, 2, 3)))

// IndexedSeq for efficient random access
def processIndexed(seq: IndexedSeq[Int]): Int = {
  var sum = 0
  for (i <- seq.indices) {
    sum += seq(i)
  }
  sum
}

// LinearSeq for efficient head/tail operations
def processLinear(seq: collection.LinearSeq[Int]): Int = seq match {
  case head :: tail => head + processLinear(tail)
  case _ => 0
}

// Range: Lazy, memory-efficient sequences
val range1 = 1 to 10          // 1 to 10 inclusive
val range2 = 1 until 10       // 1 to 9
val range3 = 1 to 100 by 10   // 1, 11, 21, ..., 91

// Stream (deprecated, use LazyList)
val lazyList = LazyList.from(1).take(5)
println(lazyList.toList)

// Choosing the right sequence:
// List - Default, functional style, prepend-heavy
// Vector - Large, random access, both-end operations
// Array - Interop with Java, mutable, performance-critical
// ArrayBuffer - Mutable, frequent updates
```

Choose List for functional programming, Vector for random access, and Array for
Java interop or performance-critical code.

## Sets and Maps

Sets provide unique element storage while maps store key-value pairs, both with
efficient lookup operations.

```scala
// Immutable Set
val set1 = Set(1, 2, 3, 4, 5)
val set2 = Set(4, 5, 6, 7, 8)

// Set operations
val union = set1 union set2         // Set(1, 2, 3, 4, 5, 6, 7, 8)
val intersection = set1 intersect set2  // Set(4, 5)
val difference = set1 diff set2     // Set(1, 2, 3)

// Set methods
println(set1.contains(3))           // true
println(set1(3))                    // true (same as contains)

val added = set1 + 6
val removed = set1 - 3
val multiAdd = set1 ++ Set(6, 7, 8)

// Mutable Set
import scala.collection.mutable

val mutableSet = mutable.Set(1, 2, 3)
mutableSet += 4
mutableSet ++= Set(5, 6)
mutableSet -= 2

// Different Set implementations
val hashSet = mutable.HashSet(1, 2, 3)      // Unordered, fast
val linkedHashSet = mutable.LinkedHashSet(1, 2, 3)  // Maintains insertion order
val treeSet = collection.immutable.TreeSet(1, 2, 3)  // Sorted

// SortedSet
val sortedSet = collection.immutable.SortedSet(5, 2, 8, 1)
println(sortedSet)  // TreeSet(1, 2, 5, 8)

// Immutable Map
val map = Map(
  "Alice" -> 30,
  "Bob" -> 25,
  "Charlie" -> 35
)

// Map access
println(map("Alice"))               // 30
println(map.get("Alice"))           // Some(30)
println(map.get("David"))           // None
println(map.getOrElse("David", 0))  // 0

// Map operations
val updated = map + ("David" -> 28)
val removed = map - "Bob"
val merged = map ++ Map("Eve" -> 32)

// Map transformations
val ages = map.values.toList
val names = map.keys.toList
val pairs = map.toList

val incremented = map.map { case (name, age) => (name, age + 1) }
val filtered = map.filter { case (_, age) => age > 30 }

// Mutable Map
val mutableMap = mutable.Map("a" -> 1, "b" -> 2)
mutableMap("c") = 3
mutableMap += ("d" -> 4)
mutableMap.update("e", 5)

// Map variants
val hashMap = mutable.HashMap("a" -> 1, "b" -> 2)  // Unordered, fast
val linkedHashMap = mutable.LinkedHashMap("a" -> 1, "b" -> 2)  // Insertion order
val treeMap = collection.immutable.TreeMap("c" -> 3, "a" -> 1, "b" -> 2)  // Sorted

// SortedMap
val sortedMap = collection.immutable.SortedMap(
  "charlie" -> 35,
  "alice" -> 30,
  "bob" -> 25
)
println(sortedMap)  // TreeMap(alice -> 30, bob -> 25, charlie -> 35)

// MultiMap pattern
val multiMap = mutable.Map[String, mutable.Set[Int]]()

def addToMultiMap(key: String, value: Int): Unit = {
  multiMap.getOrElseUpdate(key, mutable.Set()) += value
}

addToMultiMap("even", 2)
addToMultiMap("even", 4)
addToMultiMap("odd", 1)
addToMultiMap("odd", 3)

// Grouping into Map
val numbers = List(1, 2, 3, 4, 5, 6)
val grouped = numbers.groupBy(_ % 2 == 0)
// Map(false -> List(1, 3, 5), true -> List(2, 4, 6))

// Word frequency count
val text = "the quick brown fox jumps over the lazy dog"
val wordFreq = text.split(" ")
  .groupBy(identity)
  .view.mapValues(_.length)
  .toMap

// Map with default values
val withDefault = map.withDefaultValue(0)
println(withDefault("Unknown"))  // 0

val withDefaultFunc = map.withDefault(key => key.length)
println(withDefaultFunc("Unknown"))  // 7
```

Use Sets for uniqueness constraints and fast membership testing, Maps for
key-value lookups and grouping operations.

## Collection Transformations

Scala provides rich transformation methods that work consistently across all
collection types.

```scala
// Map: Transform each element
val numbers = List(1, 2, 3, 4, 5)
val squared = numbers.map(x => x * x)
val doubled = numbers.map(_ * 2)

// FlatMap: Map and flatten
val nested = List(List(1, 2), List(3, 4), List(5))
val flattened = nested.flatMap(identity)  // List(1, 2, 3, 4, 5)

val pairs = numbers.flatMap(x => numbers.map(y => (x, y)))

// Filter: Select elements
val evens = numbers.filter(_ % 2 == 0)
val odds = numbers.filterNot(_ % 2 == 0)

// Partition: Split into two collections
val (evenPart, oddPart) = numbers.partition(_ % 2 == 0)

// Take and Drop
val first3 = numbers.take(3)        // List(1, 2, 3)
val last3 = numbers.takeRight(3)    // List(3, 4, 5)
val skip2 = numbers.drop(2)         // List(3, 4, 5)

// TakeWhile and DropWhile
val taken = numbers.takeWhile(_ < 4)  // List(1, 2, 3)
val dropped = numbers.dropWhile(_ < 4)  // List(4, 5)

// Slice: Extract range
val slice = numbers.slice(1, 4)     // List(2, 3, 4)

// Fold and Reduce
val sum = numbers.foldLeft(0)(_ + _)
val product = numbers.foldLeft(1)(_ * _)

// FoldRight: Right-associative
val rightFold = numbers.foldRight(0)(_ + _)

// Reduce: Like fold but no initial value
val reduced = numbers.reduce(_ + _)
val max = numbers.reduce((a, b) => if (a > b) a else b)

// Scan: Fold with intermediate results
val cumulative = numbers.scan(0)(_ + _)  // List(0, 1, 3, 6, 10, 15)

// Zip: Combine collections
val letters = List("a", "b", "c")
val zipped = numbers.zip(letters)  // List((1,a), (2,b), (3,c))

val withIndex = numbers.zipWithIndex  // List((1,0), (2,1), (3,2), ...)

// Unzip: Split pairs
val (nums, chars) = zipped.unzip

// GroupBy: Create Map of groups
val grouped = numbers.groupBy(_ % 3)
// Map(0 -> List(3), 1 -> List(1, 4), 2 -> List(2, 5))

// Sorted, SortBy, SortWith
val sorted = List(3, 1, 4, 1, 5).sorted
val sortedDesc = List(3, 1, 4, 1, 5).sorted(Ordering[Int].reverse)

case class Person(name: String, age: Int)
val people = List(Person("Alice", 30), Person("Bob", 25))
val byAge = people.sortBy(_.age)
val byName = people.sortWith(_.name < _.name)

// Distinct: Remove duplicates
val withDups = List(1, 2, 2, 3, 3, 3, 4)
val unique = withDups.distinct  // List(1, 2, 3, 4)

// Find, Exists, ForAll
val found = numbers.find(_ > 3)        // Some(4)
val exists = numbers.exists(_ > 10)    // false
val all = numbers.forall(_ > 0)        // true

// Count: Number of matching elements
val count = numbers.count(_ % 2 == 0)  // 2

// Collect: Partial function transformation
val result = numbers.collect {
  case x if x % 2 == 0 => x * 2
}

// Sliding: Sliding windows
val windows = numbers.sliding(2).toList
// List(List(1, 2), List(2, 3), List(3, 4), List(4, 5))

val windows3 = numbers.sliding(3, 2).toList
// List(List(1, 2, 3), List(3, 4, 5))

// Grouped: Fixed-size chunks
val chunks = numbers.grouped(2).toList
// List(List(1, 2), List(3, 4), List(5))

// Transpose: Matrix transposition
val matrix = List(List(1, 2, 3), List(4, 5, 6))
val transposed = matrix.transpose  // List(List(1, 4), List(2, 5), List(3, 6))

// Combinations and Permutations
val combinations = List(1, 2, 3).combinations(2).toList
// List(List(1, 2), List(1, 3), List(2, 3))

val permutations = List(1, 2, 3).permutations.toList
// All permutations of the list

// String-specific operations
val words = List("hello", "world", "scala")
val concatenated = words.mkString(", ")  // "hello, world, scala"
val joined = words.mkString("[", ", ", "]")  // "[hello, world, scala]"
```

Master these transformations to write expressive, functional data processing
pipelines with minimal code.

## For-Comprehensions with Collections

For-comprehensions provide elegant syntax for complex collection operations,
especially with multiple sequences.

```scala
// Basic for-comprehension
val numbers = List(1, 2, 3)
val letters = List("a", "b")

val combined = for {
  num <- numbers
  letter <- letters
} yield (num, letter)
// List((1,a), (1,b), (2,a), (2,b), (3,a), (3,b))

// With filtering
val filtered = for {
  num <- numbers
  if num % 2 != 0
  letter <- letters
} yield (num, letter)

// Multiple generators
val result = for {
  i <- 1 to 3
  j <- 1 to 3
  if i < j
} yield (i, j)

// De-sugaring to flatMap and map
val manual = numbers.flatMap { num =>
  letters.map { letter =>
    (num, letter)
  }
}

// Nested for-comprehensions
val matrix = List(List(1, 2), List(3, 4), List(5, 6))
val flattened = for {
  row <- matrix
  elem <- row
} yield elem * 2

// Pattern matching in generators
case class Person(name: String, age: Int)
val people = List(Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35))

val names = for {
  Person(name, age) <- people
  if age > 26
} yield name

// Combining Options
def getUserById(id: Int): Option[Person] =
  if (id == 1) Some(Person("Alice", 30)) else None

def getEmail(person: Person): Option[String] =
  Some(s"${person.name.toLowerCase}@example.com")

val email = for {
  person <- getUserById(1)
  email <- getEmail(person)
} yield email

// Cartesian product
val xs = List(1, 2, 3)
val ys = List(10, 20)

val products = for {
  x <- xs
  y <- ys
} yield x * y

// With variable binding
val computed = for {
  x <- List(1, 2, 3)
  y = x * 2
  z <- List(y, y + 1)
} yield z

// Parallel assignment
val pairs = for {
  (x, y) <- List((1, 2), (3, 4), (5, 6))
} yield x + y

// For loops (side effects)
for {
  i <- 1 to 5
  j <- 1 to 5
} {
  print(s"($i,$j) ")
}

// Reading files with for-comprehension
import scala.io.Source

def readLines(filename: String): List[String] = {
  val source = Source.fromFile(filename)
  try {
    source.getLines().toList
  } finally {
    source.close()
  }
}

// Complex data transformation
case class Order(id: Int, userId: Int, total: Double)
case class User(id: Int, name: String)

val users = List(User(1, "Alice"), User(2, "Bob"))
val orders = List(Order(1, 1, 100), Order(2, 1, 150), Order(3, 2, 200))

val userTotals = for {
  user <- users
  userOrders = orders.filter(_.userId == user.id)
  total = userOrders.map(_.total).sum
} yield (user.name, total)
```

For-comprehensions make complex collection operations readable and maintainable,
especially with multiple nested operations.

## Lazy Evaluation and Views

Lazy evaluation defers computation until results are needed, improving
performance for large datasets and infinite sequences.

```scala
// Views: Lazy collection transformations
val numbers = (1 to 1000000).toList

// Eager evaluation (creates intermediate lists)
val eager = numbers
  .map(_ + 1)
  .filter(_ % 2 == 0)
  .map(_ * 2)
  .take(10)

// Lazy evaluation with view (no intermediate collections)
val lazy = numbers.view
  .map(_ + 1)
  .filter(_ % 2 == 0)
  .map(_ * 2)
  .take(10)
  .toList

// LazyList (formerly Stream)
val infiniteNums = LazyList.from(1)
val first10 = infiniteNums.take(10).toList

// Fibonacci with LazyList
def fibonacci: LazyList[BigInt] = {
  def fib(a: BigInt, b: BigInt): LazyList[BigInt] =
    a #:: fib(b, a + b)
  fib(0, 1)
}

val fibs = fibonacci.take(20).toList

// Prime numbers with LazyList
def sieve(nums: LazyList[Int]): LazyList[Int] =
  nums.head #:: sieve(nums.tail.filter(_ % nums.head != 0))

val primes = sieve(LazyList.from(2))
val first20Primes = primes.take(20).toList

// Iterator: One-time lazy traversal
val iterator = Iterator(1, 2, 3, 4, 5)
val doubled = iterator.map(_ * 2)
// Can only traverse once
println(doubled.toList)
// println(doubled.toList)  // Empty - already consumed

// View for large transformations
val largeList = (1 to 1000000).toList

val result = largeList.view
  .filter(_ % 2 == 0)
  .map(x => x * x)
  .filter(_ % 3 == 0)
  .take(100)
  .toList

// Combining eager and lazy
val mixed = numbers.view
  .map(_ * 2)
  .filter(_ > 100)
  .force  // Force evaluation, returns strict collection

// Lazy evaluation with Options
def expensiveComputation(x: Int): Int = {
  println(s"Computing for $x")
  x * 2
}

lazy val lazyValue = expensiveComputation(5)
// Not computed yet
println("Before access")
println(lazyValue)  // Now computed
println(lazyValue)  // Cached, not recomputed

// Performance comparison
def timeIt[T](block: => T): (T, Long) = {
  val start = System.nanoTime()
  val result = block
  val elapsed = (System.nanoTime() - start) / 1000000
  (result, elapsed)
}

val data = (1 to 10000000).toList

val (eagerResult, eagerTime) = timeIt {
  data
    .map(_ + 1)
    .filter(_ % 2 == 0)
    .map(_ * 2)
    .take(10)
}

val (lazyResult, lazyTime) = timeIt {
  data.view
    .map(_ + 1)
    .filter(_ % 2 == 0)
    .map(_ * 2)
    .take(10)
    .toList
}

println(s"Eager time: ${eagerTime}ms")
println(s"Lazy time: ${lazyTime}ms")
```

Use views for chaining multiple transformations on large collections to avoid
intermediate collection creation.

## Parallel Collections

Parallel collections automatically distribute operations across multiple threads
for performance on multi-core systems.

```scala
import scala.collection.parallel.CollectionConverters._

// Convert to parallel collection
val numbers = (1 to 1000000).toList
val parallelNumbers = numbers.par

// Parallel operations
val sum = parallelNumbers.sum
val doubled = parallelNumbers.map(_ * 2)
val filtered = parallelNumbers.filter(_ % 2 == 0)

// Parallel fold (associative operations only)
val total = parallelNumbers.fold(0)(_ + _)

// Aggregate: More flexible than fold
val result = parallelNumbers.aggregate(0)(
  (acc, x) => acc + x,           // Sequential operation
  (acc1, acc2) => acc1 + acc2    // Parallel combine
)

// Task support for controlling parallelism
import scala.collection.parallel.ForkJoinTaskSupport
import java.util.concurrent.ForkJoinPool

val customParallel = numbers.par
customParallel.tasksupport = new ForkJoinTaskSupport(new ForkJoinPool(4))

// Performance comparison
def benchmark[T](name: String)(block: => T): T = {
  val start = System.nanoTime()
  val result = block
  val elapsed = (System.nanoTime() - start) / 1000000
  println(s"$name: ${elapsed}ms")
  result
}

val data = (1 to 10000000).toList

benchmark("Sequential") {
  data.map(x => x * x).filter(_ % 2 == 0).sum
}

benchmark("Parallel") {
  data.par.map(x => x * x).filter(_ % 2 == 0).sum
}

// When to use parallel collections:
// - Large datasets (> 10,000 elements)
// - CPU-intensive operations
// - Associative and commutative operations
// - Multi-core available

// When to avoid:
// - Small datasets (overhead > benefit)
// - I/O operations (not CPU-bound)
// - Non-associative operations
// - Order-dependent operations

// Grouping with parallel collections
val grouped = parallelNumbers.groupBy(_ % 10)

// Side effects in parallel (unsafe)
var counter = 0
// parallelNumbers.foreach(x => counter += 1)  // Race condition

// Safe accumulation
val counts = parallelNumbers.aggregate(0)(
  (count, _) => count + 1,
  _ + _
)
```

Use parallel collections for CPU-intensive operations on large datasets with
multiple cores available.

## Best Practices

1. **Prefer immutable collections** by default for thread safety and functional
   programming benefits

2. **Choose the right collection type** based on access patterns: List for
   sequential, Vector for random access

3. **Use for-comprehensions** for complex transformations with multiple
   generators and filters

4. **Apply views for large transformations** to avoid creating intermediate
   collections

5. **Leverage groupBy and partition** for categorizing data instead of manual
   filtering

6. **Use parallel collections** only for large, CPU-intensive operations on
   multi-core systems

7. **Avoid size on lazy collections** as it forces evaluation of the entire
   sequence

8. **Prefer foldLeft over mutable accumulation** for aggregating values
   functionally

9. **Use Option instead of null** when working with potentially missing
   collection elements

10. **Apply consistent transformation patterns** across all collection types for
    maintainable code

## Common Pitfalls

1. **Using List for random access** causes O(n) performance instead of O(1) with
   Vector

2. **Forgetting to convert views back** leaves lazy collections that compute on
   every access

3. **Mutating collections in parallel** causes race conditions and
   non-deterministic results

4. **Not handling empty collections** in reduce operations causes runtime
   exceptions

5. **Using var with immutable collections** defeats the purpose of immutability

6. **Calling head on empty collections** throws exceptions instead of using
   headOption

7. **Inefficient string concatenation** in folds should use StringBuilder or
   mkString

8. **Not considering memory** with large lazy sequences that retain references

9. **Overusing parallel collections** on small datasets adds overhead without
   benefits

10. **Mixing mutable and immutable collections** leads to unexpected mutations
    and bugs

## When to Use This Skill

Apply collection operations throughout Scala development for data transformation
and processing.

Use immutable collections for concurrent applications and public APIs to ensure
thread safety.

Leverage for-comprehensions when working with multiple sequences or nested
structures.

Apply lazy evaluation with views for large datasets or when chaining many
transformations.

Use parallel collections when processing large datasets with CPU-intensive
operations on multi-core systems.

Choose specialized collection types (Set, Map, Vector) based on specific access
patterns and performance requirements.

## Resources

- [Scala Collections Documentation](<https://docs.scala-lang.org/overviews/collections-2.13/introduction.html>)
- [Scala Collections Performance](<https://docs.scala-lang.org/overviews/collections-2.13/performance-characteristics.html>)
- [Parallel Collections Guide](<https://docs.scala-lang.org/overviews/parallel-collections/overview.html>)
- [Scala Cookbook - Collections](<https://www.oreilly.com/library/view/scala-cookbook/9781449340292/>)
- [Twitter Scala School - Collections](<https://twitter.github.io/scala_school/collections.html>)
