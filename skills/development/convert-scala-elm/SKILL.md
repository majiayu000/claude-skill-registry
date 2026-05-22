---
name: convert-scala-elm
description: Convert Scala code to idiomatic Elm. Use when migrating Scala backend logic to Elm frontend applications, translating functional Scala patterns to The Elm Architecture, or refactoring from advanced type system features to simpler compile-time guarantees. Extends meta-convert-dev with Scala-to-Elm specific patterns.
---

# Convert Scala to Elm

Convert Scala code to idiomatic Elm. This skill extends `meta-convert-dev` with Scala-to-Elm specific type mappings, idiom translations, and tooling for translating from backend/full-stack functional programming to frontend functional programming with simpler, safer types.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Scala's sealed traits and case classes → Elm's union types
- **Idiom translations**: Functional Scala patterns → The Elm Architecture (TEA)
- **Error handling**: Option/Either with rich combinators → Maybe/Result with simpler API
- **Async patterns**: Future/IO/Task with effect systems → Cmd/Sub with TEA
- **Type system**: Advanced types (higher-kinded, type classes, implicits) → simple types with guarantees

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Scala language fundamentals - see `lang-scala-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → Scala) - see `convert-elm-scala`
- ScalaJS specific patterns - see `lang-scala-js-dev` for frontend-to-frontend conversions

---

## Quick Reference

| Scala | Elm | Notes |
|-------|-----|-------|
| `case class User(name: String)` | `type alias User = { name : String }` | Case classes → records |
| `sealed trait Msg; case object Increment extends Msg` | `type Msg = Increment \| Decrement` | Sealed traits → union types |
| `Option[A]` | `Maybe a` | Direct mapping with simpler API |
| `Either[Error, Value]` | `Result error value` | Direct mapping, same right-bias |
| `List[A]` or `Vector[A]` | `List a` | Lists (Elm uses linked lists) |
| `IO[Unit]` or `Task[Unit]` | `Cmd Msg` | Effects → commands |
| `x match { case ... => ... }` | `case x of ...` | Pattern matching |
| `x => x + 1` or `_ + 1` | `\x -> x + 1` | Lambda syntax |
| `def update(model: Model, msg: Msg): (Model, IO[Unit])` | `update : Msg -> Model -> (Model, Cmd Msg)` | Functional effects → TEA |
| `(A, B)` (Tuple2) | `( a, b )` | Tuples with anonymous access |

---

## When Converting Code

1. **Analyze source thoroughly** before writing target - understand Scala's abstractions and data flow
2. **Map types first** - create type equivalence table, simplifying advanced features
3. **Preserve semantics** over syntax similarity - embrace Elm's simpler model
4. **Adopt target idioms** - don't write "Scala code in Elm syntax"
5. **Handle edge cases** - simplify Option/Either to Maybe/Result, manage effect boundaries
6. **Test equivalence** - same inputs → same outputs
7. **Simplify type system usage** - remove higher-kinded types, implicits, type classes

---

## Type System Mapping

### Primitive Types

| Scala | Elm | Notes |
|-------|-----|-------|
| `String` | `String` | Direct mapping |
| `Int` | `Int` | 32-bit integers (same semantics) |
| `Double` | `Float` | Elm uses Float for all floating-point |
| `Boolean` | `Bool` | Direct mapping |
| `Char` | `Char` | Direct mapping |
| `Unit` | `()` (unit) | Unit type, same semantics |

### Collection Types

| Scala | Elm | Notes |
|-------|-----|-------|
| `List[A]` | `List a` | Immutable linked list (same semantics) |
| `Vector[A]` | `List a` | Elm only has linked lists (O(n) indexed access) |
| `Array[A]` | `Array a` | Elm has Array for O(log n) indexed access |
| `(A, B)` | `( a, b )` | Tuples, access via pattern matching or `Tuple.first`/`Tuple.second` |
| `(A, B, C)` | `( a, b, c )` | Elm supports tuples up to 3 elements natively |
| `Map[K, V]` | `Dict k v` | Immutable dictionary (requires comparable keys in Elm) |
| `Set[A]` | `Set a` | Immutable set (requires comparable values in Elm) |

### Composite Types

| Scala | Elm | Notes |
|-------|-----|-------|
| `case class User(name: String)` | `type alias User = { name : String }` | Type aliases for records |
| `sealed trait Msg; case object A extends Msg; case object B extends Msg` | `type Msg = A \| B` | Union types for ADTs |
| `sealed trait Msg; case class SetName(value: String) extends Msg` | `type Msg = SetName String` | ADTs with data |
| `Either[Err, Ok]` | `Result err ok` | Result type (Ok/Err constructors) |
| `Option[A]` | `Maybe a` | Maybe type (Just/Nothing constructors) |

---

## Idiom Translation

### Pattern: Sealed Traits to Union Types

Scala uses sealed traits with case classes/objects for discriminated unions. Elm uses simpler union types.

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

**Elm:**
```elm
-- Union type with simple syntax
type Msg
    = Increment
    | Decrement
    | SetCount Int

type alias Model =
    { count : Int }

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

**Why this translation:**
- Elm's union types are simpler and don't require separate declarations for each variant
- Elm's record update syntax `{ model | count = ... }` is more concise than Scala's `copy`
- Both provide compile-time exhaustiveness checking
- Elm enforces purity at the type system level (no side effects in update)

---

### Pattern: Option to Maybe

Scala's Option type with rich combinators translates to Elm's Maybe with simpler API.

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

**Elm:**
```elm
type alias User =
    { name : String
    , age : Int
    }

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

-- Using Maybe combinators
name : String
name =
    findUser 1
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"
```

**Why this translation:**
- Maybe has the same semantics as Option (Just/Nothing vs Some/None)
- Elm uses `Maybe.withDefault` instead of `getOrElse`
- Elm doesn't have `fold` on Maybe, use `map` + `withDefault` instead
- Elm's pipe operator `|>` is similar to method chaining
- Property access `.name` is more concise than Scala's `_.name`

---

### Pattern: Either to Result

Scala's Either type (right-biased) maps to Elm's Result, which is designed for error handling.

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

-- Chain Results with andThen
validateAge : String -> Result String Int
validateAge str =
    parseAge str
        |> Result.andThen
            (\age ->
                if age < 120 then
                    Ok age
                else
                    Err "Age must be less than 120"
            )
```

**Why this translation:**
- Result has the same semantics as Either (Ok/Err vs Right/Left)
- Elm uses `Result.andThen` instead of `flatMap` for chaining
- Elm doesn't have for-comprehensions; use pipe chains instead
- Elm doesn't have exceptions, so parsing returns Maybe, not throws
- Elm Result is explicitly for error handling, not general sum types

---

### Pattern: Functional Effects to The Elm Architecture

Scala's functional effect systems (cats-effect, ZIO) translate to The Elm Architecture's Cmd/Sub.

**Scala (with cats-effect):**
```scala
import cats.effect.IO

// MODEL
case class Model(count: Int)

def init: Model = Model(0)

// UPDATE
sealed trait Msg
case object Increment extends Msg
case object Decrement extends Msg
case object LoadData extends Msg
case class DataLoaded(data: String) extends Msg

def update(model: Model, msg: Msg): (Model, IO[Unit]) = msg match {
  case Increment => (model.copy(count = model.count + 1), IO.unit)
  case Decrement => (model.copy(count = model.count - 1), IO.unit)
  case LoadData => (model, loadDataEffect)
  case DataLoaded(data) => (model, IO.unit) // handle loaded data
}

def loadDataEffect: IO[Unit] =
  IO(println("Loading data..."))

// VIEW
def view(model: Model): String =
  s"Count: ${model.count}"
```

**Elm:**
```elm
import Http

-- MODEL
type alias Model =
    { count : Int }

init : ( Model, Cmd Msg )
init =
    ( { count = 0 }, Cmd.none )

-- UPDATE
type Msg
    = Increment
    | Decrement
    | LoadData
    | DataLoaded (Result Http.Error String)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        Decrement ->
            ( { model | count = model.count - 1 }, Cmd.none )

        LoadData ->
            ( model, loadDataCmd )

        DataLoaded result ->
            case result of
                Ok data ->
                    ( model, Cmd.none )  -- handle loaded data

                Err _ ->
                    ( model, Cmd.none )  -- handle error

loadDataCmd : Cmd Msg
loadDataCmd =
    Http.get
        { url = "https://api.example.com/data"
        , expect = Http.expectString DataLoaded
        }

-- VIEW
view : Model -> Html Msg
view model =
    div []
        [ text ("Count: " ++ String.fromInt model.count) ]
```

**Why this translation:**
- TEA's `( Model, Cmd Msg )` return type is similar to Scala's `(Model, IO[Unit])`
- `Cmd.none` is equivalent to `IO.unit` (no effect)
- Elm enforces the TEA pattern at the type system level
- Effects in Elm are always async and message-based (no synchronous IO)
- Elm runtime manages all effects; you describe what to do, runtime executes

---

## Paradigm Translation

### Mental Model Shift: Backend/Full-Stack FP → Frontend FP

| Scala Concept | Elm Approach | Key Insight |
|---------------|--------------|-------------|
| Effect systems (IO, Task, ZIO) | Cmd/Sub in TEA | Effects are managed by runtime, not type-level |
| Higher-kinded types | Simple parametric types | Elm lacks HKTs; use concrete types |
| Type classes (implicits/given) | No type classes | Use explicit function passing or modules |
| For-comprehensions | Pipe chains with `andThen` | Similar monadic chaining, different syntax |
| Rich combinator libraries | Smaller standard library | Elm prefers simplicity over completeness |

### Type System Mental Model

| Scala Feature | Elm Translation | Conceptual Translation |
|---------------|-----------------|------------------------|
| Sealed traits + case classes | Union types | ADTs with simpler syntax |
| Implicits/given | Explicit parameters | No automatic resolution |
| Type classes | Module functions | Polymorphism via modules, not constraints |
| Higher-kinded types | Not supported | Use concrete types (List, Maybe, etc.) |
| Variance annotations | Not needed | All types are invariant |

---

## Error Handling

### Scala Error Model → Elm Error Model

**Scala approach:**
- Multiple error types: `Option`, `Either`, `Try`, exceptions
- Rich combinators: `fold`, `flatMap`, `recover`, `recoverWith`
- For-comprehensions for sequencing
- Type classes for generic error handling

**Elm approach:**
- Two error types: `Maybe` (no error info), `Result` (with error info)
- Simpler combinators: `map`, `andThen`, `withDefault`
- Pipe chains for sequencing
- Explicit pattern matching for error handling

**Translation strategy:**

| Scala | Elm | When to Use |
|-------|-----|-------------|
| `Option[A]` | `Maybe a` | When error context doesn't matter |
| `Either[E, A]` | `Result e a` | When you need error information |
| `Try[A]` | `Result String a` | Elm has no exceptions; use Result with String error |
| For-comprehension | Pipe chain with `andThen` | Sequential error-prone operations |

**Example:**

```scala
// Scala
def getUser(id: Int): Option[User] = ???
def getOrders(user: User): Either[String, List[Order]] = ???
def processOrders(orders: List[Order]): Try[Summary] = ???

val result: Either[String, Summary] = for {
  user <- getUser(1).toRight("User not found")
  orders <- getOrders(user)
  summary <- processOrders(orders).toEither.left.map(_.getMessage)
} yield summary
```

```elm
-- Elm
getUser : Int -> Maybe User
getOrders : User -> Result String (List Order)
processOrders : List Order -> Result String Summary

result : Result String Summary
result =
    getUser 1
        |> Result.fromMaybe "User not found"
        |> Result.andThen getOrders
        |> Result.andThen processOrders
```

---

## Concurrency Patterns

### Scala Async → Elm Async

**Scala concurrency models:**
- `Future` (eager, callback-based)
- `IO` / `Task` (lazy, referentially transparent)
- Akka actors (message-passing)
- Parallel execution with `parMapN`, `parTraverse`

**Elm concurrency model:**
- `Cmd` (command to runtime, always async)
- `Sub` (subscription to events)
- No parallelism control (runtime manages)
- Everything goes through TEA update loop

**Translation strategy:**

| Scala Pattern | Elm Pattern | Notes |
|---------------|-------------|-------|
| `Future[A]` | `Cmd Msg` + callback | Future result becomes a Msg |
| `IO[A]` | `Cmd Msg` | Elm runtime executes commands |
| Sequential effects | `Cmd.batch [cmd1, cmd2]` | Multiple commands issued at once |
| Parallel effects | `Cmd.batch [cmd1, cmd2]` | Runtime decides execution strategy |
| HTTP request | `Http.get` → `Cmd Msg` | Built-in HTTP module |
| WebSocket | `Browser.Events.onVisibilityChange` | Subscriptions for streaming |

**Example:**

```scala
// Scala (cats-effect)
def fetchUser(id: Int): IO[User] = ???
def fetchOrders(userId: Int): IO[List[Order]] = ???

val program: IO[String] = for {
  user <- fetchUser(1)
  orders <- fetchOrders(user.id)
} yield s"${user.name} has ${orders.length} orders"

program.unsafeRunSync()
```

```elm
-- Elm
type Msg
    = UserFetched (Result Http.Error User)
    | OrdersFetched (Result Http.Error (List Order))

fetchUser : Int -> Cmd Msg
fetchUser id =
    Http.get
        { url = "/api/users/" ++ String.fromInt id
        , expect = Http.expectJson UserFetched userDecoder
        }

fetchOrders : Int -> Cmd Msg
fetchOrders userId =
    Http.get
        { url = "/api/orders?userId=" ++ String.fromInt userId
        , expect = Http.expectJson OrdersFetched ordersDecoder
        }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        UserFetched (Ok user) ->
            ( { model | user = Just user }
            , fetchOrders user.id
            )

        UserFetched (Err _) ->
            ( model, Cmd.none )

        OrdersFetched (Ok orders) ->
            ( { model | orders = orders }, Cmd.none )

        OrdersFetched (Err _) ->
            ( model, Cmd.none )
```

**Why this translation:**
- Elm doesn't allow synchronous effects; everything is async via Cmd
- Sequential effects become chained messages in the update loop
- Elm runtime manages all async execution; no manual thread management
- Type safety is preserved through Result types in message variants

---

## Advanced Feature Translation

### Type Classes to Module Functions

Scala's type classes (via implicits/given) don't exist in Elm. Use explicit module functions.

**Scala:**
```scala
// Type class
trait Show[A] {
  def show(a: A): String
}

object Show {
  implicit val intShow: Show[Int] = (a: Int) => a.toString
  implicit val stringShow: Show[String] = (a: String) => s""""$a""""

  def show[A](a: A)(implicit ev: Show[A]): String = ev.show(a)
}

// Usage
Show.show(42)        // "42"
Show.show("hello")   // "\"hello\""
```

**Elm:**
```elm
-- Explicit functions per type
showInt : Int -> String
showInt n =
    String.fromInt n

showString : String -> String
showString s =
    "\"" ++ s ++ "\""

-- No polymorphic show function; use type-specific functions
result1 = showInt 42           -- "42"
result2 = showString "hello"   -- "\"hello\""
```

**Why this translation:**
- Elm doesn't have type classes or ad-hoc polymorphism
- Use concrete functions for each type
- This is more explicit but less generic
- Consider using custom types to unify different representations

---

### Higher-Kinded Types - Not Supported

Scala's higher-kinded types (type constructors as parameters) don't exist in Elm.

**Scala:**
```scala
trait Functor[F[_]] {
  def map[A, B](fa: F[A])(f: A => B): F[B]
}

def mapTwice[F[_]: Functor, A, B, C](fa: F[A])(f: A => B)(g: B => C): F[C] = {
  val fb = Functor[F].map(fa)(f)
  Functor[F].map(fb)(g)
}

// Works with List, Option, Either, etc.
mapTwice(List(1, 2, 3))(_ + 1)(_ * 2)
mapTwice(Some(5))(_ + 1)(_ * 2)
```

**Elm - Use concrete types:**
```elm
-- Separate implementations for each type
mapTwiceList : (a -> b) -> (b -> c) -> List a -> List c
mapTwiceList f g list =
    list
        |> List.map f
        |> List.map g

mapTwiceMaybe : (a -> b) -> (b -> c) -> Maybe a -> Maybe c
mapTwiceMaybe f g maybe =
    maybe
        |> Maybe.map f
        |> Maybe.map g

-- Usage
mapTwiceList (\x -> x + 1) (\x -> x * 2) [1, 2, 3]
mapTwiceMaybe (\x -> x + 1) (\x -> x * 2) (Just 5)
```

**Why this translation:**
- Elm prioritizes simplicity over abstraction
- Code is more explicit and easier to understand
- No accidental complexity from type-level programming
- Duplicate code is acceptable if it improves clarity

---

## Common Pitfalls

1. **Trying to use type classes**: Elm has no type classes. Use explicit function passing or modules for polymorphism.

2. **Expecting exceptions**: Elm has no runtime exceptions. All errors must be represented as Maybe or Result.

3. **Using mutable state**: Elm is purely functional with immutable data. Use record updates and model state instead.

4. **Synchronous side effects**: All effects in Elm are async via Cmd/Sub. You can't perform IO directly in functions.

5. **Advanced type features**: Elm doesn't have higher-kinded types, variance, existential types, or path-dependent types. Keep it simple.

6. **For-comprehensions**: Elm doesn't have for-comprehensions. Use pipe chains with `andThen` for monadic sequencing.

7. **Lazy evaluation**: Elm is strict (eager) by default. Use lazy values explicitly with `Lazy.lazy`.

8. **Tuple size limits**: Elm tuples are limited to 3 elements. Use records for larger structures.

9. **Dict/Set key constraints**: In Elm, Dict keys and Set values must be `comparable` (Int, Float, String, etc.). Can't use custom types as keys without workarounds.

10. **Missing standard library functions**: Elm's standard library is intentionally small. You may need to implement common utilities yourself or use packages.

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| `elm` | Compiler and CLI | Fast compiler with excellent error messages |
| `elm-format` | Code formatter | Enforces consistent style, integrates with editors |
| `elm-test` | Testing framework | Unit and fuzz testing |
| `elm-review` | Linter | Customizable code review tool |
| `elm-json` | Package manager helper | Manage dependencies more easily |
| `elm-spa` | SPA framework | Higher-level abstractions for single-page apps |
| ScalaJS → Elm | Manual rewrite | No automatic transpiler exists |

**Migration strategy:**
1. Extract pure business logic from Scala
2. Identify data types and ADTs
3. Map types to Elm equivalents
4. Rewrite logic using Elm idioms
5. Structure as TEA (Model-Update-View)
6. Use elm-test to verify behavior equivalence

---

## Examples

Examples should progress in complexity:

### Example 1: Simple - ADT Translation

**Before (Scala):**
```scala
sealed trait Status
case object Pending extends Status
case object Active extends Status
case object Completed extends Status

def statusToString(status: Status): String = status match {
  case Pending => "Pending"
  case Active => "Active"
  case Completed => "Completed"
}

val current: Status = Active
println(statusToString(current))  // "Active"
```

**After (Elm):**
```elm
type Status
    = Pending
    | Active
    | Completed

statusToString : Status -> String
statusToString status =
    case status of
        Pending ->
            "Pending"

        Active ->
            "Active"

        Completed ->
            "Completed"

current : Status
current =
    Active

-- Usage: statusToString current  => "Active"
```

---

### Example 2: Medium - Option/Maybe and Error Handling

**Before (Scala):**
```scala
case class User(name: String, age: Int)

def findUser(id: Int): Option[User] =
  if (id == 1) Some(User("Alice", 30))
  else None

def validateAge(age: Int): Either[String, Int] =
  if (age >= 18) Right(age)
  else Left("Must be 18 or older")

def getUserAge(id: Int): Either[String, Int] =
  findUser(id)
    .toRight("User not found")
    .flatMap(user => validateAge(user.age))

getUserAge(1)  // Right(30)
getUserAge(2)  // Left("User not found")
```

**After (Elm):**
```elm
type alias User =
    { name : String
    , age : Int
    }

findUser : Int -> Maybe User
findUser id =
    if id == 1 then
        Just { name = "Alice", age = 30 }
    else
        Nothing

validateAge : Int -> Result String Int
validateAge age =
    if age >= 18 then
        Ok age
    else
        Err "Must be 18 or older"

getUserAge : Int -> Result String Int
getUserAge id =
    findUser id
        |> Result.fromMaybe "User not found"
        |> Result.andThen (\user -> validateAge user.age)

-- getUserAge 1  => Ok 30
-- getUserAge 2  => Err "User not found"
```

---

### Example 3: Complex - TEA Application with HTTP

**Before (Scala with cats-effect):**
```scala
import cats.effect.IO
import io.circe.generic.auto._
import org.http4s._
import org.http4s.circe._
import org.http4s.client._

case class Post(id: Int, title: String, body: String)

case class Model(
  posts: List[Post],
  loading: Boolean,
  error: Option[String]
)

sealed trait Msg
case object FetchPosts extends Msg
case class PostsFetched(posts: List[Post]) extends Msg
case class FetchFailed(error: String) extends Msg

def update(model: Model, msg: Msg): (Model, IO[Msg]) = msg match {
  case FetchPosts =>
    (model.copy(loading = true), fetchPosts)

  case PostsFetched(posts) =>
    (model.copy(posts = posts, loading = false, error = None), IO.pure(FetchPosts))

  case FetchFailed(error) =>
    (model.copy(loading = false, error = Some(error)), IO.pure(FetchPosts))
}

def fetchPosts(implicit client: Client[IO]): IO[Msg] = {
  val uri = Uri.unsafeFromString("https://jsonplaceholder.typicode.com/posts")
  client.expect[List[Post]](uri)
    .map(PostsFetched)
    .handleErrorWith(err => IO.pure(FetchFailed(err.getMessage)))
}

def view(model: Model): String = {
  if (model.loading) "Loading..."
  else if (model.error.isDefined) s"Error: ${model.error.get}"
  else s"Posts: ${model.posts.map(_.title).mkString(", ")}"
}
```

**After (Elm):**
```elm
import Browser
import Html exposing (Html, div, text, button, ul, li)
import Html.Events exposing (onClick)
import Http
import Json.Decode as Decode exposing (Decoder, field, int, string)

-- MODEL
type alias Post =
    { id : Int
    , title : String
    , body : String
    }

type alias Model =
    { posts : List Post
    , loading : Bool
    , error : Maybe String
    }

init : ( Model, Cmd Msg )
init =
    ( { posts = []
      , loading = False
      , error = Nothing
      }
    , Cmd.none
    )

-- UPDATE
type Msg
    = FetchPosts
    | PostsFetched (Result Http.Error (List Post))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchPosts ->
            ( { model | loading = True, error = Nothing }
            , fetchPosts
            )

        PostsFetched (Ok posts) ->
            ( { model | posts = posts, loading = False }
            , Cmd.none
            )

        PostsFetched (Err error) ->
            ( { model | loading = False, error = Just (errorToString error) }
            , Cmd.none
            )

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

-- HTTP
fetchPosts : Cmd Msg
fetchPosts =
    Http.get
        { url = "https://jsonplaceholder.typicode.com/posts"
        , expect = Http.expectJson PostsFetched postsDecoder
        }

postsDecoder : Decoder (List Post)
postsDecoder =
    Decode.list postDecoder

postDecoder : Decoder Post
postDecoder =
    Decode.map3 Post
        (field "id" int)
        (field "title" string)
        (field "body" string)

-- VIEW
view : Model -> Html Msg
view model =
    div []
        [ button [ onClick FetchPosts ] [ text "Fetch Posts" ]
        , viewContent model
        ]

viewContent : Model -> Html Msg
viewContent model =
    if model.loading then
        text "Loading..."

    else
        case model.error of
            Just error ->
                text ("Error: " ++ error)

            Nothing ->
                ul []
                    (List.map viewPost model.posts)

viewPost : Post -> Html Msg
viewPost post =
    li [] [ text post.title ]

-- MAIN
main : Program () Model Msg
main =
    Browser.element
        { init = \_ -> init
        , update = update
        , view = view
        , subscriptions = \_ -> Sub.none
        }
```

**Why this translation:**
- Scala's IO effects become Elm's Cmd in TEA
- HTTP client becomes `Http.get` with JSON decoder
- Error handling via Result instead of IO error handling
- View is pure HTML (no side effects)
- Elm runtime manages all effects and rendering
- Type safety maintained throughout with no runtime exceptions

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-elm-scala` - Reverse conversion (Elm → Scala)
- `lang-scala-dev` - Scala development patterns
- `lang-elm-dev` - Elm development patterns

Cross-cutting pattern skills (for areas not fully covered by lang-*-dev):
- `patterns-concurrency-dev` - Async, channels, threads across languages
- `patterns-serialization-dev` - JSON, validation, struct tags across languages
