---
name: convert-clojure-elm
description: Convert Clojure code to idiomatic Elm. Use when migrating Clojure projects to Elm, translating functional patterns from JVM to browser, or building type-safe frontends from Clojure logic. Extends meta-convert-dev with Clojure-to-Elm specific patterns for handling dynamic-to-static typing, REPL-driven to TEA architecture, and side effects to managed effects.
---

# Convert Clojure to Elm

Convert Clojure code to idiomatic Elm. This skill extends `meta-convert-dev` with Clojure-to-Elm specific type mappings, idiom translations, and architectural patterns.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Dynamic Clojure types → Static Elm types
- **Architecture translation**: REPL-driven development → The Elm Architecture (TEA)
- **Effect handling**: Side effects anywhere → Cmd/Sub managed effects
- **Null handling**: nil → Maybe/Nothing pattern
- **Error handling**: Exceptions → Result types
- **Data structures**: Persistent collections → Immutable records
- **Macro translation**: Compile-time macros → Type-driven design

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Clojure language fundamentals - see `lang-clojure-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → Clojure) - see `convert-elm-clojure`
- ClojureScript → Elm (similar but with JS runtime considerations)

---

## Quick Reference

| Clojure | Elm | Notes |
|---------|-----|-------|
| `nil` | `Nothing` | Explicit Maybe type |
| `{:key "value"}` | `{ key = "value" }` | Records are explicit types |
| `(defn f [x] ...)` | `f : a -> b`<br/>`f x = ...` | Type signatures required |
| `(map f coll)` | `List.map f list` | Module-qualified |
| `(try ... (catch ...))` | `Result` type | No exceptions |
| `(atom 0)` | Model in TEA | State in architecture |
| `(assoc m :k v)` | `{ model \| k = v }` | Record update syntax |
| `(get m :k)` | `model.k` | Field access |
| `(or x y)` | `Maybe.withDefault y x` | Explicit Maybe handling |
| `(when pred ...)` | `if pred then ... else ...` | Always need else |

---

## 8 Pillars Validation

Before converting, verify coverage of the 8 pillars essential for code conversion:

| Pillar | lang-clojure-dev | lang-elm-dev | Coverage |
|--------|------------------|--------------|----------|
| **Module System** | ✓ `ns`, `:require` | ✓ `module`, `import` | Green |
| **Error Handling** | ✓ `try/catch`, `ex-info` | ✓ `Result`, `Maybe` | Green |
| **Concurrency Model** | ✓ atoms, refs, agents | ✓ Cmd/Sub, Task | Green |
| **Metaprogramming** | ✓ Macros, syntax quote | ✓ No macros (intentional) | Green |
| **Zero/Default Values** | ~ nil everywhere | ✓ Explicit Maybe, no null | Green |
| **Serialization** | ✓ EDN, JSON, Transit, spec | ✓ JSON decoders/encoders | Green |
| **Build/Deps** | ✓ Leiningen, deps.edn | ✓ elm.json, elm install | Green |
| **Testing** | ✓ clojure.test, test.check | ✓ elm-test, fuzz testing | Green |

**Status**: Green (8/8 pillars covered)

**Recommendation**: Proceed with conversion - both skills have comprehensive coverage.

---

## When Converting Code

1. **Define types first** - Clojure is dynamic, Elm requires explicit types for everything
2. **Map nil → Maybe** - Identify all nullable values and make them explicit
3. **Extract pure functions** - Separate logic from side effects
4. **Design TEA architecture** - Model, View, Update before writing code
5. **Handle all cases** - Elm's exhaustive pattern matching replaces runtime checks
6. **No runtime errors** - Elm guarantees no null pointers, no type mismatches

---

## Type System Mapping

### Primitive Types

| Clojure | Elm | Notes |
|---------|-----|-------|
| `nil` | `Nothing` | Part of Maybe type |
| `true`/`false` | `True`/`False` | Capitalized in Elm |
| `"string"` | `"string"` | Strings are identical |
| `42` (integer) | `42 : Int` | Explicit type |
| `3.14` (double) | `3.14 : Float` | Explicit type |
| `:keyword` | No direct equivalent | Use String or custom type |
| `'symbol` | No equivalent | Use String or custom type |

### Collection Types

| Clojure | Elm | Notes |
|---------|-----|-------|
| `[1 2 3]` (vector) | `[ 1, 2, 3 ] : List Int` | Lists are linked, not vectors |
| `'(1 2 3)` (list) | `[ 1, 2, 3 ] : List Int` | Same as vector in Elm |
| `{:a 1 :b 2}` (map) | `{ a = 1, b = 2 }` | Record with type alias |
| `#{1 2 3}` (set) | `Set.fromList [ 1, 2, 3 ]` | Import Set module |
| `[x y]` (tuple) | `( x, y )` | Parentheses, max 3 elements |
| `(seq coll)` | `list` | All lists are lazy-ish in Elm |

### Composite Types

| Clojure | Elm | Notes |
|---------|-----|-------|
| `{:name "Alice" :age 30}` | `type alias User = { name : String, age : Int }` | Explicit type required |
| `(defrecord User [name age])` | `type alias User = { name : String, age : Int }` | Type alias for records |
| `(deftype Point [x y])` | `type Point = Point Float Float` | Custom type |
| Tagged literal | `type Msg = Clicked \| Typed String` | Union types |
| `nil`-able value | `Maybe User` | Explicit optional |

### Function Types

| Clojure | Elm | Notes |
|---------|-----|-------|
| `(defn f [x] ...)` | `f : a -> b` | Type signature required |
| `(fn [x] ...)` | `\x -> ...` | Anonymous function |
| `#(* % 2)` | `\x -> x * 2` | Lambda syntax |
| Multi-arity `(defn f ([x] ...) ([x y] ...))` | Separate functions | No multi-arity |
| Variadic `(defn f [& args])` | `List a` parameter | No varargs |

---

## Idiom Translation

### Pattern: Dynamic Map → Typed Record

**Clojure:**
```clojure
;; Maps are dynamic - any keys, any values
(def user {:name "Alice" :email "alice@example.com"})

(defn greet [user]
  (str "Hello, " (:name user)))

(defn update-email [user email]
  (assoc user :email email))
```

**Elm:**
```elm
-- Records have explicit types - all fields known at compile time
type alias User =
    { name : String
    , email : String
    }

greet : User -> String
greet user =
    "Hello, " ++ user.name

updateEmail : User -> String -> User
updateEmail user email =
    { user | email = email }
```

**Why this translation:**
- Elm requires all record fields to be declared in a type alias
- Field access is compile-time checked
- No runtime key errors possible
- Type inference helps but explicit types are idiomatic

---

### Pattern: nil Handling → Maybe

**Clojure:**
```clojure
;; nil can appear anywhere
(defn find-user [id users]
  (first (filter #(= (:id %) id) users)))
  ;; Returns user or nil

(defn display-name [user]
  (or (:name user) "Anonymous"))
```

**Elm:**
```elm
-- Explicit Maybe for optional values
findUser : Int -> List User -> Maybe User
findUser id users =
    users
        |> List.filter (\u -> u.id == id)
        |> List.head  -- Returns Maybe User

displayName : Maybe User -> String
displayName maybeUser =
    maybeUser
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"
```

**Why this translation:**
- Elm has no null/nil - compiler forces you to handle absence
- Maybe makes optionality explicit in type signatures
- Pattern matching ensures all cases are handled
- No NullPointerException possible

---

### Pattern: Sequence Operations

**Clojure:**
```clojure
;; Lazy sequences with threading
(->> data
     (filter active?)
     (map :value)
     (reduce +))

;; List comprehension
(for [x (range 10)
      :when (even? x)]
  (* x 2))
```

**Elm:**
```elm
-- List pipeline (not lazy by default)
data
    |> List.filter active
    |> List.map .value
    |> List.foldl (+) 0

-- No list comprehension - use map/filter
List.range 0 9
    |> List.filter (\x -> modBy 2 x == 0)
    |> List.map (\x -> x * 2)
```

**Why this translation:**
- Elm's pipeline operator `|>` is similar to Clojure's `->>`
- Elm lists are not lazy (except for user-defined streams)
- Use explicit List module functions
- No `for` comprehension - compose map/filter instead

---

### Pattern: Atoms/State → TEA Model

**Clojure:**
```clojure
;; Mutable state with atom
(def counter (atom 0))

(defn increment! []
  (swap! counter inc))

(defn get-count []
  @counter)
```

**Elm:**
```elm
-- Immutable model in TEA
type alias Model =
    { counter : Int
    }

type Msg
    = Increment

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | counter = model.counter + 1 }, Cmd.none )

-- No direct "get" - view is pure function of model
view : Model -> Html Msg
view model =
    div [] [ text (String.fromInt model.counter) ]
```

**Why this translation:**
- Elm has no mutable state - all state in Model
- Updates happen through messages (Msg type)
- State changes are pure functions: `Msg -> Model -> (Model, Cmd Msg)`
- View is always pure function: `Model -> Html Msg`

---

### Pattern: Macros → Type-Driven Design

**Clojure:**
```clojure
;; Macro for compile-time abstraction
(defmacro unless [condition & body]
  `(if (not ~condition)
     (do ~@body)))

(unless false
  (println "This runs"))
```

**Elm:**
```elm
-- No macros - use types and functions instead
unless : Bool -> (() -> a) -> Maybe a
unless condition thunk =
    if not condition then
        Just (thunk ())
    else
        Nothing

-- Or just use if directly (more idiomatic)
if not condition then
    Debug.log "This runs"
else
    ()
```

**Why this translation:**
- Elm has no macros - all code is explicit
- Use higher-order functions for abstraction
- Phantom types encode compile-time constraints
- Code generation (elm-codegen) for repetitive code

---

### Pattern: Destructuring

**Clojure:**
```clojure
;; Map destructuring
(let [{:keys [name age]} user]
  (str name " is " age))

;; Vector destructuring
(let [[first & rest] coll]
  (process first rest))
```

**Elm:**
```elm
-- Record destructuring
let
    { name, age } = user
in
    name ++ " is " ++ String.fromInt age

-- List pattern matching (not destructuring)
case list of
    first :: rest ->
        process first rest

    [] ->
        -- Must handle empty list
        defaultValue
```

**Why this translation:**
- Elm's record destructuring is similar to Clojure's map destructuring
- List destructuring requires pattern matching with `case`
- Must handle all cases - compiler enforces exhaustiveness
- Can destructure in function parameters: `greet { name } = ...`

---

## Error Handling

### Clojure Exception Model → Elm Result Model

**Clojure uses exceptions:**
```clojure
(defn parse-int [s]
  (try
    (Integer/parseInt s)
    (catch NumberFormatException e
      (throw (ex-info "Invalid number" {:input s})))))

(defn divide [a b]
  (if (zero? b)
    (throw (ex-info "Division by zero" {:a a :b b}))
    (/ a b)))
```

**Elm uses Result type:**
```elm
parseInt : String -> Result String Int
parseInt s =
    String.toInt s
        |> Result.fromMaybe ("Invalid number: " ++ s)

divide : Float -> Float -> Result String Float
divide a b =
    if b == 0 then
        Err "Division by zero"
    else
        Ok (a / b)

-- Chaining Results
parseAndDivide : String -> String -> Result String Float
parseAndDivide numStr denomStr =
    Result.map2 divide
        (parseInt numStr)
        (parseInt denomStr)
        |> Result.andThen identity
```

**Why this approach:**
- Elm has no exceptions - all errors are values
- Result type makes error handling explicit
- Compiler forces you to handle Err case
- No try/catch needed - pattern match on Result

### Error Propagation

**Clojure:**
```clojure
;; Exceptions bubble up automatically
(defn process-user [id]
  (let [user (fetch-user id)        ;; May throw
        validated (validate user)   ;; May throw
        saved (save-user validated)] ;; May throw
    saved))
```

**Elm:**
```elm
-- Results must be explicitly chained
processUser : Int -> Cmd Msg
processUser id =
    fetchUser id
        |> Task.andThen validateUser
        |> Task.andThen saveUser
        |> Task.attempt ProcessUserComplete

-- Or with Result in update:
case fetchUser id of
    Ok user ->
        case validateUser user of
            Ok validated ->
                case saveUser validated of
                    Ok saved ->
                        ( { model | user = Just saved }, Cmd.none )

                    Err saveError ->
                        ( { model | error = Just saveError }, Cmd.none )

            Err validationError ->
                ( { model | error = Just validationError }, Cmd.none )

    Err fetchError ->
        ( { model | error = Just fetchError }, Cmd.none)

-- Better: use Result helpers
processUser : Int -> Result String User
processUser id =
    fetchUser id
        |> Result.andThen validateUser
        |> Result.andThen saveUser
```

**Translation strategy:**
1. Map Clojure exceptions to Elm Result types
2. Use `Result.andThen` for sequential error handling
3. Use `Result.map2/map3` for combining multiple Results
4. Pattern match in update function to handle errors

---

## Architecture Translation

### REPL-Driven Development → The Elm Architecture (TEA)

**Clojure approach:**
```clojure
;; Direct interaction with state
(def app-state (atom {:count 0 :users []}))

;; Functions mutate state directly
(defn increment! []
  (swap! app-state update :count inc))

(defn add-user! [user]
  (swap! app-state update :users conj user))

;; REPL experimentation
(increment!)
@app-state ;; => {:count 1 :users []}
```

**Elm approach (TEA):**
```elm
-- 1. Define Model (all state)
type alias Model =
    { count : Int
    , users : List User
    }

-- 2. Define Msg (all possible actions)
type Msg
    = Increment
    | AddUser User

-- 3. Define Update (pure state transitions)
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        AddUser user ->
            ( { model | users = model.users ++ [ user ] }, Cmd.none )

-- 4. Define View (pure render function)
view : Model -> Html Msg
view model =
    div []
        [ div [] [ text ("Count: " ++ String.fromInt model.count) ]
        , button [ onClick Increment ] [ text "+" ]
        , div [] (List.map viewUser model.users)
        ]
```

**Translation strategy:**
1. Identify Clojure atoms/refs → Elm Model fields
2. Map mutation functions → Msg constructors
3. Extract pure logic into update branches
4. Build view as pure function of Model

---

### Side Effects → Cmd and Sub

**Clojure (side effects anywhere):**
```clojure
(defn fetch-and-save-user [id]
  (let [user (http/get (str "/api/users/" id))  ;; Side effect
        parsed (json/parse-string (:body user))] ;; Pure
    (db/save! parsed)  ;; Side effect
    parsed))
```

**Elm (managed effects):**
```elm
-- Side effects ONLY through Cmd
type Msg
    = FetchUser Int
    | GotUser (Result Http.Error User)
    | SaveUser User
    | UserSaved (Result Http.Error ())

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser id ->
            ( { model | loading = True }
            , Http.get
                { url = "/api/users/" ++ String.fromInt id
                , expect = Http.expectJson GotUser userDecoder
                }
            )

        GotUser (Ok user) ->
            ( model, saveUserCmd user )

        GotUser (Err error) ->
            ( { model | error = Just error }, Cmd.none )

        SaveUser user ->
            ( model, saveUserCmd user )

        UserSaved (Ok ()) ->
            ( { model | saved = True }, Cmd.none )

        UserSaved (Err error) ->
            ( { model | error = Just error }, Cmd.none )

-- Cmd constructors
saveUserCmd : User -> Cmd Msg
saveUserCmd user =
    Http.post
        { url = "/api/users"
        , body = Http.jsonBody (encodeUser user)
        , expect = Http.expectWhatever UserSaved
        }
```

**Translation strategy:**
1. Extract all side effects → Cmd in update
2. Define Msg for each async result
3. Chain effects through Msg flow
4. Use Task for sequential async operations

---

## Common Pitfalls

### 1. Assuming Dynamic Typing

**Problem:** Treating Elm like dynamically-typed Clojure

```elm
-- ❌ WRONG: Can't have heterogeneous lists
users = [ { name = "Alice" }, { name = "Bob", age = 30 } ]
-- ERROR: Record fields must match

-- ✓ CORRECT: Define explicit type with Maybe for optional fields
type alias User =
    { name : String
    , age : Maybe Int
    }

users =
    [ { name = "Alice", age = Nothing }
    , { name = "Bob", age = Just 30 }
    ]
```

### 2. Forgetting to Handle All Cases

**Problem:** Incomplete pattern matching

```elm
-- ❌ WRONG: Missing Nothing case
getName : Maybe User -> String
getName maybeUser =
    case maybeUser of
        Just user ->
            user.name
-- ERROR: Missing pattern: Nothing

-- ✓ CORRECT: Handle all cases
getName : Maybe User -> String
getName maybeUser =
    case maybeUser of
        Just user ->
            user.name

        Nothing ->
            "Anonymous"
```

### 3. Trying to Mutate State

**Problem:** Thinking of Elm Model like Clojure atom

```elm
-- ❌ WRONG: Can't mutate model
update msg model =
    model.count = model.count + 1  -- ERROR: No assignment in Elm
    ( model, Cmd.none )

-- ✓ CORRECT: Create new record with updated field
update msg model =
    ( { model | count = model.count + 1 }, Cmd.none )
```

### 4. Expecting Macros

**Problem:** Looking for Clojure-style macros

```elm
-- ❌ WRONG: No macros in Elm
-- Can't write:
-- defmacro myWhen [condition & body] ...

-- ✓ CORRECT: Use functions or code generation
myWhen : Bool -> (() -> a) -> Maybe a
myWhen condition thunk =
    if condition then
        Just (thunk ())
    else
        Nothing

-- Or just use if directly (more idiomatic)
```

### 5. Missing Type Annotations

**Problem:** Relying too much on type inference

```elm
-- ❌ BAD: No type signature
add x y =
    x + y
-- Inferred type might not be what you want

-- ✓ GOOD: Explicit type signature
add : Int -> Int -> Int
add x y =
    x + y
```

### 6. Forgetting Else Branch

**Problem:** Clojure `when` has no else; Elm `if` requires it

```clojure
;; Clojure: when has implicit nil
(when condition
  (do-thing))
```

```elm
-- ❌ WRONG: Missing else
if condition then
    doThing
-- ERROR: if needs else branch

-- ✓ CORRECT: Provide else (even if unit)
if condition then
    doThing
else
    ()
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| `elm-format` | Auto-format Elm code | Like cljfmt |
| `elm-test` | Unit and property testing | Similar to test.check |
| `elm-review` | Custom linting rules | Like clj-kondo |
| `elm-json` | Package manager | Like lein or deps.edn |
| `elm-live` | Development server with hot reload | Like figwheel |
| `elm-analyse` (deprecated) | Code analysis | Use elm-review instead |
| `elm-codegen` | Generate Elm code | For repetitive boilerplate |

---

## Examples

### Example 1: Simple - Data Transformation

**Before (Clojure):**
```clojure
;; Transform list of maps
(defn process-users [users]
  (->> users
       (filter :active)
       (map :name)
       (map str/upper-case)))

(process-users [{:name "alice" :active true}
                {:name "bob" :active false}
                {:name "charlie" :active true}])
;; => ("ALICE" "CHARLIE")
```

**After (Elm):**
```elm
-- Transform list of records
type alias User =
    { name : String
    , active : Bool
    }

processUsers : List User -> List String
processUsers users =
    users
        |> List.filter .active
        |> List.map .name
        |> List.map String.toUpper

-- Usage
processUsers
    [ { name = "alice", active = True }
    , { name = "bob", active = False }
    , { name = "charlie", active = True }
    ]
-- => [ "ALICE", "CHARLIE" ]
```

---

### Example 2: Medium - Error Handling with HTTP

**Before (Clojure):**
```clojure
(require '[clj-http.client :as http]
         '[cheshire.core :as json])

(defn fetch-user [id]
  (try
    (-> (http/get (str "https://api.example.com/users/" id))
        :body
        (json/parse-string true))
    (catch Exception e
      (println "Error fetching user:" (.getMessage e))
      nil)))

(defn display-user [id]
  (if-let [user (fetch-user id)]
    (str "User: " (:name user))
    "User not found"))
```

**After (Elm):**
```elm
import Http
import Json.Decode as Decode exposing (Decoder)

-- Model includes loading states
type alias Model =
    { user : RemoteData Http.Error User
    }

type RemoteData error value
    = NotAsked
    | Loading
    | Success value
    | Failure error

-- Messages for async flow
type Msg
    = FetchUser Int
    | GotUser (Result Http.Error User)

-- User decoder
userDecoder : Decoder User
userDecoder =
    Decode.map2 User
        (Decode.field "name" Decode.string)
        (Decode.field "email" Decode.string)

-- Update handles side effects
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser id ->
            ( { model | user = Loading }
            , Http.get
                { url = "https://api.example.com/users/" ++ String.fromInt id
                , expect = Http.expectJson GotUser userDecoder
                }
            )

        GotUser (Ok user) ->
            ( { model | user = Success user }, Cmd.none )

        GotUser (Err error) ->
            ( { model | user = Failure error }, Cmd.none )

-- View renders based on state
view : Model -> Html Msg
view model =
    case model.user of
        NotAsked ->
            button [ onClick (FetchUser 1) ] [ text "Load User" ]

        Loading ->
            div [] [ text "Loading..." ]

        Success user ->
            div [] [ text ("User: " ++ user.name) ]

        Failure error ->
            div [] [ text "User not found" ]
```

---

### Example 3: Complex - Full Application with State Management

**Before (Clojure):**
```clojure
(ns app.core
  (:require [clojure.string :as str]))

;; Application state
(def state (atom {:users []
                  :search ""
                  :filter :all}))

;; State mutations
(defn add-user! [user]
  (swap! state update :users conj user))

(defn set-search! [query]
  (swap! state assoc :search query))

(defn set-filter! [filter-type]
  (swap! state assoc :filter filter-type))

;; Pure logic
(defn matches-search? [user query]
  (str/includes? (str/lower-case (:name user))
                 (str/lower-case query)))

(defn matches-filter? [user filter-type]
  (case filter-type
    :all true
    :active (:active user)
    :inactive (not (:active user))))

(defn filtered-users [users search filter-type]
  (->> users
       (filter #(matches-search? % search))
       (filter #(matches-filter? % filter-type))))

;; Usage
(add-user! {:name "Alice" :active true})
(add-user! {:name "Bob" :active false})
(set-search! "ali")
(set-filter! :active)

(let [{:keys [users search filter]} @state]
  (filtered-users users search filter))
;; => ({:name "Alice" :active true})
```

**After (Elm):**
```elm
module Main exposing (main)

import Browser
import Html exposing (Html, button, div, input, text)
import Html.Attributes exposing (placeholder, value)
import Html.Events exposing (onClick, onInput)

-- MODEL

type alias User =
    { name : String
    , active : Bool
    }

type FilterType
    = All
    | Active
    | Inactive

type alias Model =
    { users : List User
    , search : String
    , filter : FilterType
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { users = []
      , search = ""
      , filter = All
      }
    , Cmd.none
    )

-- UPDATE

type Msg
    = AddUser User
    | SetSearch String
    | SetFilter FilterType

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        AddUser user ->
            ( { model | users = model.users ++ [ user ] }, Cmd.none )

        SetSearch query ->
            ( { model | search = query }, Cmd.none )

        SetFilter filterType ->
            ( { model | filter = filterType }, Cmd.none )

-- VIEW HELPERS (Pure logic)

matchesSearch : String -> User -> Bool
matchesSearch query user =
    String.contains
        (String.toLower query)
        (String.toLower user.name)

matchesFilter : FilterType -> User -> Bool
matchesFilter filterType user =
    case filterType of
        All ->
            True

        Active ->
            user.active

        Inactive ->
            not user.active

filteredUsers : Model -> List User
filteredUsers model =
    model.users
        |> List.filter (matchesSearch model.search)
        |> List.filter (matchesFilter model.filter)

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ div []
            [ input
                [ placeholder "Search users..."
                , value model.search
                , onInput SetSearch
                ]
                []
            ]
        , div []
            [ button [ onClick (SetFilter All) ] [ text "All" ]
            , button [ onClick (SetFilter Active) ] [ text "Active" ]
            , button [ onClick (SetFilter Inactive) ] [ text "Inactive" ]
            ]
        , div []
            [ button
                [ onClick (AddUser { name = "Alice", active = True }) ]
                [ text "Add Alice" ]
            , button
                [ onClick (AddUser { name = "Bob", active = False }) ]
                [ text "Add Bob" ]
            ]
        , div []
            (filteredUsers model
                |> List.map viewUser
            )
        ]

viewUser : User -> Html Msg
viewUser user =
    div []
        [ text (user.name ++ if user.active then " ✓" else " ✗")
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

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-elm-clojure` - Reverse conversion (Elm → Clojure)
- `lang-clojure-dev` - Clojure development patterns
- `lang-elm-dev` - Elm development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async, state management across languages
- `patterns-serialization-dev` - JSON, validation, encoding/decoding
- `patterns-metaprogramming-dev` - Compile-time abstractions across languages
