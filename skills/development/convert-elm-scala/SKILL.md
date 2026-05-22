---
name: convert-elm-scala
description: Convert Elm code to idiomatic Scala. Use when migrating Elm frontend applications to Scala backends or full-stack Scala, translating The Elm Architecture to functional Scala patterns, or refactoring type-safe functional code from compile-time guarantees to more powerful type system features. Extends meta-convert-dev with Elm-to-Scala specific patterns.
---

# Convert Elm to Scala

Convert Elm code to idiomatic Scala. This skill extends `meta-convert-dev` with Elm-to-Scala specific type mappings, idiom translations, and tooling for translating from frontend functional programming to backend/full-stack functional programming with more expressive types.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elm's union types → Scala's sealed traits and case classes
- **Idiom translations**: The Elm Architecture → functional Scala patterns (cats-effect, ZIO)
- **Error handling**: Maybe/Result → Option/Either with rich combinators
- **Async patterns**: Cmd/Sub → Future/IO/Task with effect systems
- **Type system**: Simple types → advanced types (higher-kinded, type classes, implicits)

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Scala language fundamentals - see `lang-scala-dev`
- Reverse conversion (Scala → Elm) - see `convert-scala-elm`
- ScalaJS specific patterns - see `lang-scala-js-dev` for frontend-to-frontend conversions

---

## Quick Reference

| Elm | Scala | Notes |
|-----|-------|-------|
| `type alias User = { name : String }` | `case class User(name: String)` | Records → case classes |
| `type Msg = Increment \| Decrement` | `sealed trait Msg; case object Increment extends Msg` | Union types → sealed traits |
| `Maybe a` | `Option[A]` | Direct mapping with richer combinators |
| `Result error value` | `Either[Error, Value]` | Direct mapping, right-biased |
| `List a` | `List[A]` or `Vector[A]` | Lists or vectors |
| `Cmd Msg` | `IO[Unit]` or `Task[Unit]` | Effects with cats-effect/ZIO |
| `case x of ...` | `x match { case ... => ... }` | Pattern matching |
| `\x -> x + 1` | `x => x + 1` or `_ + 1` | Lambda syntax |
| `update : Msg -> Model -> (Model, Cmd Msg)` | `def update(model: Model, msg: Msg): (Model, IO[Unit])` | TEA → functional effects |
| `( a, b )` | `(A, B)` (Tuple2) | Tuples with named accessors |

---

## When Converting Code

1. **Analyze source thoroughly** before writing target - understand TEA flow and data dependencies
2. **Map types first** - create type equivalence table for domain models
3. **Preserve semantics** over syntax similarity - leverage Scala's richer type system
4. **Adopt target idioms** - don't write "Elm code in Scala syntax"
5. **Handle edge cases** - Option chaining, Either composition, effect management
6. **Test equivalence** - same inputs → same outputs
7. **Leverage type classes** - use implicits for compile-time guarantees Elm lacks

---

## Type System Mapping

### Primitive Types

| Elm | Scala | Notes |
|-----|-------|-------|
| `String` | `String` | Direct mapping |
| `Int` | `Int` | 32-bit integers |
| `Float` | `Double` | Scala uses Double by default |
| `Bool` | `Boolean` | Direct mapping |
| `Char` | `Char` | Direct mapping |
| `()` (unit) | `Unit` | Unit type, same semantics |

### Collection Types

| Elm | Scala | Notes |
|-----|-------|-------|
| `List a` | `List[A]` | Immutable linked list (similar semantics) |
| `List a` | `Vector[A]` | Better for indexed access (O(log n) vs O(n)) |
| `Array a` | `Vector[A]` or `Array[A]` | Vector preferred for immutability |
| `( a, b )` | `(A, B)` | Tuples, access via `._1`, `._2` |
| `( a, b, c )` | `(A, B, C)` | Scala supports tuples up to Tuple22 |
| `Dict k v` | `Map[K, V]` | Immutable map |
| `Set a` | `Set[A]` | Immutable set |

### Composite Types

| Elm | Scala | Notes |
|-----|-------|-------|
| `type alias User = { name : String }` | `case class User(name: String)` | Case classes are idiomatic |
| `type Msg = A \| B` | `sealed trait Msg; case object A extends Msg; case object B extends Msg` | Sealed trait ADTs |
| `type Msg = SetName String` | `sealed trait Msg; case class SetName(value: String) extends Msg` | ADTs with data |
| `type Result err ok = Ok ok \| Err err` | `Either[Err, Ok]` | Either is built-in, right-biased |
| `Maybe a` | `Option[A]` | Option is built-in with Some/None |

---

## Idiom Translation

### Pattern: Union Types to Sealed Traits

Elm uses union types for discriminated unions. Scala uses sealed traits with case classes/objects.

**Elm:**
```elm
type Msg
    = Increment
    | Decrement
    | SetCount Int

update : Msg -> Model -> Model
update msg model =
    case msg of
        Increment ->
            { model | count = model.count + 1 }

        Decrement ->
            { model | count = model.count - 1 }

        SetCount newCount ->
            { model | count = newCount }
```

**Scala:**
```scala
// Sealed trait ensures exhaustive pattern matching
sealed trait Msg
case object Increment extends Msg
case object Decrement extends Msg
case class SetCount(value: Int) extends Msg

case class Model(count: Int)

def update(model: Model, msg: Msg): Model = msg match {
  case Increment => model.copy(count = model.count + 1)
  case Decrement => model.copy(count = model.count - 1)
  case SetCount(newCount) => model.copy(count = newCount)
}
```

**Why this translation:**
- Sealed traits provide compile-time exhaustiveness checking like Elm
- Case objects for singleton variants are lightweight
- Case classes for variants with data provide automatic pattern matching
- The `copy` method on case classes is similar to Elm's record update syntax

---

### Pattern: Maybe to Option

Elm's Maybe type translates directly to Scala's Option with richer combinators.

**Elm:**
```elm
findUser : Int -> Maybe User
findUser id =
    if id == 1 then
        Just { name = "Alice", age = 30 }
    else
        Nothing

displayName : Maybe User -> String
displayName maybeUser =
    case maybeUser of
        Just user ->
            user.name

        Nothing ->
            "Anonymous"

-- Using Maybe.withDefault
name : String
name =
    findUser 1
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"
```

**Scala:**
```scala
case class User(name: String, age: Int)

def findUser(id: Int): Option[User] = {
  if (id == 1) Some(User("Alice", 30))
  else None
}

def displayName(maybeUser: Option[User]): String = maybeUser match {
  case Some(user) => user.name
  case None => "Anonymous"
}

// Using Option combinators
val name: String =
  findUser(1)
    .map(_.name)
    .getOrElse("Anonymous")

// Or more idiomatically with fold
val name2: String =
  findUser(1).fold("Anonymous")(_.name)
```

**Why this translation:**
- Option has the same semantics as Maybe
- Scala's Option provides richer combinators (fold, orElse, collect, etc.)
- Pattern matching syntax is similar but uses `=>` instead of `->`
- getOrElse is equivalent to withDefault

---

### Pattern: Result Type to Either

Elm's Result type maps to Scala's Either, which is right-biased for easy chaining.

**Elm:**
```elm
parseAge : String -> Result String Int
parseAge str =
    case String.toInt str of
        Just age ->
            if age >= 0 then
                Ok age
            else
                Err "Age must be non-negative"

        Nothing ->
            Err "Not a valid number"

-- Chain Results
validateAge : String -> Result String Int
validateAge str =
    parseAge str
        |> Result.andThen (\age ->
            if age < 120 then
                Ok age
            else
                Err "Age must be less than 120"
        )
```

**Scala:**
```scala
def parseAge(str: String): Either[String, Int] = {
  try {
    val age = str.toInt
    if (age >= 0) Right(age)
    else Left("Age must be non-negative")
  } catch {
    case _: NumberFormatException => Left("Not a valid number")
  }
}

// Chain Eithers with flatMap
def validateAge(str: String): Either[String, Int] = {
  parseAge(str).flatMap { age =>
    if (age < 120) Right(age)
    else Left("Age must be less than 120")
  }
}

// Or using for-comprehension (idiomatic)
def validateAge2(str: String): Either[String, Int] = for {
  age <- parseAge(str)
  validAge <- if (age < 120) Right(age)
              else Left("Age must be less than 120")
} yield validAge
```

**Why this translation:**
- Either is right-biased, so flatMap/map operate on Right values
- For-comprehensions make chaining more readable
- Exception handling with try/catch is more idiomatic in Scala than creating helper parsers
- Either provides the same type safety as Result

---

### Pattern: The Elm Architecture to Functional Effects

TEA's Model-Update-View pattern translates to functional effect systems in Scala.

**Elm:**
```elm
-- MODEL
type alias Model =
    { count : Int }

init : Model
init =
    { count = 0 }

-- UPDATE
type Msg
    = Increment
    | Decrement

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        Decrement ->
            ( { model | count = model.count - 1 }, Cmd.none )

-- VIEW
view : Model -> Html Msg
view model =
    div []
        [ button [ onClick Decrement ] [ text "-" ]
        , div [] [ text (String.fromInt model.count) ]
        , button [ onClick Increment ] [ text "+" ]
        ]
```

**Scala (with cats-effect):**
```scala
import cats.effect.IO
import cats.effect.concurrent.Ref

// MODEL
case class Model(count: Int)

def init: Model = Model(0)

// UPDATE
sealed trait Msg
case object Increment extends Msg
case object Decrement extends Msg

def update(model: Model, msg: Msg): (Model, IO[Unit]) = msg match {
  case Increment => (model.copy(count = model.count + 1), IO.unit)
  case Decrement => (model.copy(count = model.count - 1), IO.unit)
}

// Stateful version using Ref
def runApp: IO[Unit] = for {
  modelRef <- Ref.of[IO, Model](init)
  _ <- modelRef.update { model =>
    val (newModel, effect) = update(model, Increment)
    newModel
  }
  finalModel <- modelRef.get
  _ <- IO(println(s"Count: ${finalModel.count}"))
} yield ()
```

**Scala (with ZIO):**
```scala
import zio._

// MODEL
case class Model(count: Int)

// UPDATE
sealed trait Msg
case object Increment extends Msg
case object Decrement extends Msg

def update(model: Model, msg: Msg): (Model, Task[Unit]) = msg match {
  case Increment => (model.copy(count = model.count + 1), ZIO.unit)
  case Decrement => (model.copy(count = model.count - 1), ZIO.unit)
}

// Stateful version using Ref
def runApp: Task[Unit] = for {
  modelRef <- Ref.make(Model(0))
  _ <- modelRef.update { model =>
    val (newModel, effect) = update(model, Increment)
    newModel
  }
  finalModel <- modelRef.get
  _ <- Console.printLine(s"Count: ${finalModel.count}")
} yield ()
```

**Why this translation:**
- IO/Task types represent side effects like Cmd in Elm
- Ref provides mutable reference in pure FP (like Elm's managed state)
- For-comprehensions sequence effects like Elm's Cmd.batch
- Pattern separates pure logic (update) from effects

---

### Pattern: List Operations

Elm and Scala share similar list APIs due to functional roots.

**Elm:**
```elm
-- Transform
List.map (\x -> x * 2) [1, 2, 3]
List.filter (\x -> x > 2) [1, 2, 3, 4]
List.concatMap (\x -> [x, x * 10]) [1, 2]

-- Reduce
List.foldl (+) 0 [1, 2, 3, 4]
List.foldr (::) [] [1, 2, 3]

-- Utilities
List.length [1, 2, 3]
List.head [1, 2, 3]  -- Maybe Int
List.tail [1, 2, 3]  -- Maybe (List Int)
```

**Scala:**
```scala
// Transform
List(1, 2, 3).map(_ * 2)
List(1, 2, 3, 4).filter(_ > 2)
List(1, 2).flatMap(x => List(x, x * 10))

// Reduce
List(1, 2, 3, 4).foldLeft(0)(_ + _)
List(1, 2, 3).foldRight(List.empty[Int])(_ :: _)

// Utilities
List(1, 2, 3).length
List(1, 2, 3).headOption  // Option[Int]
List(1, 2, 3).tail        // List[Int] (throws on empty!)
List(1, 2, 3).drop(1)     // Safe version of tail
```

**Why this translation:**
- APIs are nearly identical due to shared FP heritage
- Scala's flatMap is equivalent to Elm's concatMap
- Use headOption instead of head for safety (returns Option)
- tail throws exception on empty list - prefer drop(1) or tailOption (via extension)

---

## Error Handling

### Elm Error Model → Scala Error Model

**Elm uses:**
- `Maybe a` for nullable values (explicit, no null)
- `Result error value` for operations that can fail with context
- No exceptions (compiler enforces handling)

**Scala uses:**
- `Option[A]` for nullable values (explicit, but null still exists in Java interop)
- `Either[E, A]` for operations that can fail with context
- `Try[A]` for exception handling
- Exceptions are available (but discouraged in FP)

**Translation strategy:**

| Elm Pattern | Scala Pattern | Notes |
|-------------|---------------|-------|
| `Maybe a` | `Option[A]` | Direct mapping |
| `Maybe.withDefault d m` | `m.getOrElse(d)` | Extract with default |
| `Maybe.map f m` | `m.map(f)` | Transform value |
| `Maybe.andThen f m` | `m.flatMap(f)` | Chain operations |
| `Result err val` | `Either[Err, Val]` | Direct mapping |
| `Result.map f r` | `r.map(f)` | Transform right value |
| `Result.andThen f r` | `r.flatMap(f)` | Chain operations |
| `Result.mapError f r` | `r.left.map(f)` | Transform left (error) |

**Advanced pattern: Accumulating errors**

```scala
// Elm doesn't have built-in error accumulation
// Scala can use Validated from cats for this

import cats.data.Validated
import cats.implicits._

case class ValidationError(message: String)

def validateAge(age: Int): Validated[ValidationError, Int] = {
  if (age >= 0 && age < 120) age.valid
  else ValidationError("Invalid age").invalid
}

def validateName(name: String): Validated[ValidationError, String] = {
  if (name.nonEmpty) name.valid
  else ValidationError("Name is empty").invalid
}

// Accumulate errors (can't do this easily in Elm)
val result = (validateAge(-1), validateName("")).mapN { (age, name) =>
  User(name, age)
}
// Result: Invalid(ValidationError("Invalid age") + ValidationError("Name is empty"))
```

---

## Concurrency Patterns

### Elm Async → Scala Async

**Elm uses:**
- `Cmd Msg` for side effects
- `Sub Msg` for subscriptions
- `Task` for composable async operations
- No direct control over concurrency (runtime manages it)

**Scala uses:**
- `Future[A]` - eager, implicit ExecutionContext
- `IO[A]` (cats-effect) - lazy, explicit runtime
- `Task[A]` (ZIO) - lazy, fiber-based
- `Stream[F, A]` (fs2) - streaming effects

**Translation strategies:**

#### Simple HTTP Request

**Elm:**
```elm
type Msg = GotUser (Result Http.Error User)

getUser : Int -> Cmd Msg
getUser id =
    Http.get
        { url = "https://api.example.com/users/" ++ String.fromInt id
        , expect = Http.expectJson GotUser userDecoder
        }
```

**Scala (with http4s + cats-effect):**
```scala
import cats.effect.IO
import org.http4s.client.Client
import org.http4s.circe.CirceEntityDecoder._
import io.circe.generic.auto._

case class User(name: String, age: Int)

def getUser(id: Int)(implicit client: Client[IO]): IO[Either[Throwable, User]] = {
  client.expect[User](s"https://api.example.com/users/$id")
    .attempt
}
```

#### Concurrent Operations

**Elm:**
```elm
-- Elm doesn't expose concurrency primitives
-- Multiple Cmds are handled by the runtime
Cmd.batch
    [ fetchUser 1
    , fetchUser 2
    , fetchUser 3
    ]
```

**Scala (cats-effect parallel):**
```scala
import cats.effect.IO
import cats.syntax.parallel._

// Run requests in parallel
val users: IO[List[User]] = List(1, 2, 3)
  .parTraverse(id => getUser(id))
```

**Scala (ZIO parallel):**
```scala
import zio._

val users: Task[List[User]] = ZIO.collectAllPar(
  List(1, 2, 3).map(id => getUser(id))
)
```

---

## Memory & Ownership

Both Elm and Scala run on garbage-collected runtimes:
- **Elm**: Compiles to JavaScript, uses JS GC
- **Scala**: Runs on JVM, uses JVM GC

**Translation considerations:**
- No ownership concerns like Rust
- Both use immutable data structures by default
- Scala allows mutable collections but discouraged
- Scala has more control over performance (lazy collections, views, iterators)

**Performance patterns:**

```scala
// Elm: Lists are always strict
List.map f (List.map g list)  -- Creates intermediate list

// Scala: Can optimize with views/iterators
list.view.map(f).map(g).toList  // No intermediate collection (Scala 2.13+)

// Or use LazyList for lazy evaluation
LazyList(1, 2, 3).map(f).map(g)  // Only computes on demand
```

---

## Common Pitfalls

1. **Null values from Java interop**: Elm has no null, but Scala inherits null from Java. Always wrap nullable Java values in Option.
   ```scala
   // BAD: Assumes non-null
   val name: String = javaObject.getName()  // Can be null!

   // GOOD: Wrap in Option
   val name: Option[String] = Option(javaObject.getName())
   ```

2. **Non-exhaustive pattern matching**: Elm enforces exhaustiveness at compile-time. Scala only warns by default.
   ```scala
   // Enable fatal warnings in build.sbt
   scalacOptions += "-Xfatal-warnings"
   scalacOptions += "-Xlint:_"

   // Use sealed traits for exhaustive checking
   sealed trait Msg  // Compiler knows all subtypes
   ```

3. **Mutability creeping in**: Elm is purely immutable. Scala allows var and mutable collections.
   ```scala
   // BAD: Mutable state
   var count = 0

   // GOOD: Immutable updates
   val count = 0
   val newCount = count + 1
   ```

4. **Exceptions instead of Either**: Elm forces explicit error handling. Scala allows exceptions.
   ```scala
   // BAD: Throwing exceptions
   def divide(a: Int, b: Int): Int = {
     if (b == 0) throw new Exception("Division by zero")
     else a / b
   }

   // GOOD: Return Either
   def divide(a: Int, b: Int): Either[String, Int] = {
     if (b == 0) Left("Division by zero")
     else Right(a / b)
   }
   ```

5. **Future vs IO confusion**: Future is eager and executes immediately. IO is lazy and needs explicit run.
   ```scala
   // EAGER: Executes on creation
   val future = Future { println("Running"); 42 }

   // LAZY: Only executes when explicitly run
   val io = IO { println("Running"); 42 }
   io.unsafeRunSync()  // Only now does it print
   ```

6. **Type inference differences**: Elm infers everything. Scala sometimes needs help with higher-kinded types.
   ```scala
   // May need explicit type annotations
   def sequence[F[_]: Applicative, A](list: List[F[A]]): F[List[A]] = ...
   ```

7. **Pattern matching on List.tail**: Scala's tail throws on empty list, unlike Elm.
   ```scala
   // BAD: Can throw exception
   val rest = list.tail

   // GOOD: Use pattern matching
   list match {
     case head :: tail => // Safe
     case Nil => // Handle empty
   }
   ```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| **sbt** | Build tool | Most common Scala build tool |
| **Scala CLI** | Scripting | Quick scripts and REPLs |
| **scalac** | Compiler | Scala compiler (usually via sbt) |
| **scalafmt** | Code formatter | Like elm-format, auto-formats code |
| **scalafix** | Linting/refactoring | Like elm-review, code quality |
| **Metals** | LSP server | IDE support (VS Code, Vim, Emacs) |
| **IntelliJ IDEA** | IDE | Full-featured Scala IDE |
| **ScalaTest** | Testing | Most popular test framework |
| **ScalaCheck** | Property testing | QuickCheck-style property tests |
| **cats** | FP library | Type classes, data types |
| **cats-effect** | Effect system | IO, concurrency primitives |
| **ZIO** | Effect system | Alternative to cats-effect |
| **http4s** | HTTP | Functional HTTP library |
| **circe** | JSON | Pure FP JSON library |

---

## Examples

Examples progress in complexity from simple type mappings to realistic applications.

### Example 1: Simple - Type Alias to Case Class

**Before (Elm):**
```elm
type alias User =
    { name : String
    , email : String
    , age : Int
    }

createUser : String -> String -> Int -> User
createUser name email age =
    { name = name
    , email = email
    , age = age
    }

updateAge : User -> Int -> User
updateAge user newAge =
    { user | age = newAge }
```

**After (Scala):**
```scala
case class User(name: String, email: String, age: Int)

def createUser(name: String, email: String, age: Int): User =
  User(name, email, age)

def updateAge(user: User, newAge: Int): User =
  user.copy(age = newAge)
```

---

### Example 2: Medium - Union Types and Pattern Matching

**Before (Elm):**
```elm
type Route
    = Home
    | Users
    | User Int
    | NotFound

type Msg
    = NavigateTo Route
    | FetchUsers
    | GotUsers (Result Http.Error (List User))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NavigateTo route ->
            ( { model | currentRoute = route }
            , case route of
                Users ->
                    fetchUsers

                User id ->
                    fetchUser id

                _ ->
                    Cmd.none
            )

        FetchUsers ->
            ( model, fetchUsers )

        GotUsers (Ok users) ->
            ( { model | users = users }, Cmd.none )

        GotUsers (Err error) ->
            ( { model | error = Just (errorToString error) }, Cmd.none )
```

**After (Scala):**
```scala
import cats.effect.IO

sealed trait Route
case object Home extends Route
case object Users extends Route
case class User(id: Int) extends Route
case object NotFound extends Route

sealed trait Msg
case class NavigateTo(route: Route) extends Msg
case object FetchUsers extends Msg
case class GotUsers(result: Either[Throwable, List[UserData]]) extends Msg

case class UserData(name: String, email: String)
case class Model(
  currentRoute: Route,
  users: List[UserData],
  error: Option[String]
)

def update(model: Model, msg: Msg): (Model, IO[Unit]) = msg match {
  case NavigateTo(route) =>
    val effect = route match {
      case Users => fetchUsers
      case User(id) => fetchUser(id)
      case _ => IO.unit
    }
    (model.copy(currentRoute = route), effect)

  case FetchUsers =>
    (model, fetchUsers)

  case GotUsers(Right(users)) =>
    (model.copy(users = users), IO.unit)

  case GotUsers(Left(error)) =>
    (model.copy(error = Some(error.getMessage)), IO.unit)
}

// Placeholder effects
def fetchUsers: IO[Unit] = IO.unit
def fetchUser(id: Int): IO[Unit] = IO.unit
```

---

### Example 3: Complex - Complete TEA Application

**Before (Elm):**
```elm
module Main exposing (main)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode as Decode

-- MODEL

type alias Model =
    { query : String
    , results : List SearchResult
    , status : Status
    }

type Status
    = Loading
    | Success
    | Failure String

type alias SearchResult =
    { title : String
    , url : String
    , snippet : String
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { query = ""
      , results = []
      , status = Success
      }
    , Cmd.none
    )

-- UPDATE

type Msg
    = UpdateQuery String
    | Search
    | GotResults (Result Http.Error (List SearchResult))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        UpdateQuery newQuery ->
            ( { model | query = newQuery }, Cmd.none )

        Search ->
            ( { model | status = Loading }
            , searchApi model.query
            )

        GotResults (Ok results) ->
            ( { model | results = results, status = Success }
            , Cmd.none
            )

        GotResults (Err error) ->
            ( { model | status = Failure (errorToString error) }
            , Cmd.none
            )

-- HTTP

searchApi : String -> Cmd Msg
searchApi query =
    Http.get
        { url = "https://api.example.com/search?q=" ++ query
        , expect = Http.expectJson GotResults resultsDecoder
        }

resultsDecoder : Decode.Decoder (List SearchResult)
resultsDecoder =
    Decode.list <|
        Decode.map3 SearchResult
            (Decode.field "title" Decode.string)
            (Decode.field "url" Decode.string)
            (Decode.field "snippet" Decode.string)

errorToString : Http.Error -> String
errorToString error =
    case error of
        Http.BadUrl url ->
            "Bad URL: " ++ url

        Http.Timeout ->
            "Request timeout"

        Http.NetworkError ->
            "Network error"

        Http.BadStatus status ->
            "Bad status: " ++ String.fromInt status

        Http.BadBody body ->
            "Bad body: " ++ body

-- VIEW

view : Model -> Html Msg
view model =
    div [ class "container" ]
        [ h1 [] [ text "Search Engine" ]
        , div [ class "search-box" ]
            [ input
                [ type_ "text"
                , placeholder "Enter search query"
                , value model.query
                , onInput UpdateQuery
                ]
                []
            , button [ onClick Search ] [ text "Search" ]
            ]
        , viewStatus model.status
        , div [ class "results" ]
            (List.map viewResult model.results)
        ]

viewStatus : Status -> Html Msg
viewStatus status =
    case status of
        Loading ->
            div [ class "loading" ] [ text "Loading..." ]

        Success ->
            text ""

        Failure error ->
            div [ class "error" ] [ text error ]

viewResult : SearchResult -> Html Msg
viewResult result =
    div [ class "result" ]
        [ h3 [] [ a [ href result.url ] [ text result.title ] ]
        , p [] [ text result.snippet ]
        ]

-- MAIN

main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = \_ -> Sub.none
        }
```

**After (Scala with cats-effect and http4s):**
```scala
import cats.effect._
import cats.effect.concurrent.Ref
import io.circe.generic.auto._
import org.http4s._
import org.http4s.circe.CirceEntityDecoder._
import org.http4s.client.Client

// MODEL

case class Model(
  query: String,
  results: List[SearchResult],
  status: Status
)

sealed trait Status
case object Loading extends Status
case object Success extends Status
case class Failure(error: String) extends Status

case class SearchResult(
  title: String,
  url: String,
  snippet: String
)

def init: Model = Model(
  query = "",
  results = List.empty,
  status = Success
)

// UPDATE

sealed trait Msg
case class UpdateQuery(newQuery: String) extends Msg
case object Search extends Msg
case class GotResults(result: Either[Throwable, List[SearchResult]]) extends Msg

def update(model: Model, msg: Msg)(implicit client: Client[IO]): (Model, IO[Unit]) = msg match {
  case UpdateQuery(newQuery) =>
    (model.copy(query = newQuery), IO.unit)

  case Search =>
    val effect = searchApi(model.query).flatMap { result =>
      processMsg(GotResults(result))
    }
    (model.copy(status = Loading), effect)

  case GotResults(Right(results)) =>
    (model.copy(results = results, status = Success), IO.unit)

  case GotResults(Left(error)) =>
    (model.copy(status = Failure(error.getMessage)), IO.unit)
}

// HTTP

def searchApi(query: String)(implicit client: Client[IO]): IO[Either[Throwable, List[SearchResult]]] = {
  val uri = Uri.unsafeFromString(s"https://api.example.com/search?q=$query")
  client.expect[List[SearchResult]](uri).attempt
}

// APPLICATION RUNTIME

def runApp(implicit client: Client[IO]): IO[Unit] = for {
  // Create mutable reference for model
  modelRef <- Ref.of[IO, Model](init)

  // Example: Simulate user actions
  _ <- processMsg(UpdateQuery("functional programming")).flatMap { msg =>
    modelRef.update { model =>
      val (newModel, effect) = update(model, msg)
      // Run effect in background
      effect.unsafeRunAsync(_ => ())
      newModel
    }
  }

  _ <- processMsg(Search).flatMap { msg =>
    modelRef.update { model =>
      val (newModel, effect) = update(model, msg)
      effect.unsafeRunAsync(_ => ())
      newModel
    }
  }

  // Get final model
  finalModel <- modelRef.get
  _ <- IO(println(s"Final model: $finalModel"))
} yield ()

// Helper to process messages
def processMsg(msg: Msg): IO[Msg] = IO.pure(msg)

// In a real application, you would integrate with a web framework
// like http4s for server-side rendering, or ScalaJS + Laminar for frontend
```

**Notes on the complex example:**
- Scala version separates pure logic (update function) from effects
- IO type represents side effects, making them explicit like Cmd in Elm
- Ref provides mutable reference in pure FP context
- In production, you'd use a web framework (http4s, ZIO HTTP) or frontend library (ScalaJS + Laminar, Outwatch)
- The pattern preserves TEA's separation of concerns: Model, Update, Effects

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-elm-clojure` - Related conversion (Elm → dynamic FP)
- `lang-elm-dev` - Elm development patterns
- `lang-scala-dev` - Scala development patterns
- `lang-scala-cats-dev` - Cats library for advanced FP
- `lang-scala-zio-dev` - ZIO effect system
- `lang-scala-js-dev` - ScalaJS for frontend (if staying in browser)

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async, channels, threads across languages
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Macros, implicits, type-level programming
