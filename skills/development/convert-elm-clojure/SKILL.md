---
name: convert-elm-clojure
description: Convert Elm code to idiomatic Clojure. Use when migrating Elm frontend applications to Clojure/ClojureScript, translating The Elm Architecture to Clojure patterns, or refactoring type-safe functional code to dynamic functional style. Extends meta-convert-dev with Elm-to-Clojure specific patterns.
---

# Convert Elm to Clojure

Convert Elm code to idiomatic Clojure. This skill extends `meta-convert-dev` with Elm-to-Clojure specific type mappings, idiom translations, and tooling for translating from compile-time type safety to runtime validation.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elm's union types → Clojure's keywords and maps
- **Idiom translations**: The Elm Architecture → Clojure state management patterns
- **Error handling**: Maybe/Result → nil/keywords with spec validation
- **Async patterns**: Cmd/Sub → core.async channels or callback patterns
- **Type safety**: Compile-time guarantees → runtime validation with clojure.spec

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Clojure language fundamentals - see `lang-clojure-dev`
- Reverse conversion (Clojure → Elm) - see `convert-clojure-elm`
- ClojureScript specific patterns - see `convert-elm-clojurescript` for frontend-to-frontend conversions

---

## Quick Reference

| Elm | Clojure | Notes |
|-----|---------|-------|
| `type alias User = { name : String }` | `(defrecord User [name])` or `{:name ""}` | Records or plain maps |
| `type Msg = Increment \| Decrement` | `#{:increment :decrement}` or keywords | Keywords for discriminated unions |
| `Maybe a` | `nil` or value | nil represents Nothing, value is Just |
| `Result error value` | `{:ok value}` or `{:error err}` | Map with :ok/:error keys |
| `List a` | `[a]` (vector) or `'(a)` (list) | Vectors more common |
| `Cmd Msg` | `(go ...)` (core.async) or callback | Depends on approach |
| `case x of ...` | `(case x ...)` or `(cond ...)` | Pattern matching |
| `Html Msg` | Hiccup `[:div ...]` | ClojureScript's Hiccup syntax |
| `update : Msg -> Model -> (Model, Cmd Msg)` | `(defn update [model msg] ...)` | Return new model, effects separate |
| `\x -> x + 1` | `#(+ % 1)` or `(fn [x] (+ x 1))` | Anonymous functions |

---

## When Converting Code

1. **Analyze source thoroughly** before writing target - understand TEA flow
2. **Map types first** - create type equivalence table for domain models
3. **Preserve semantics** over syntax similarity - embrace dynamic typing
4. **Adopt target idioms** - don't write "Elm code in Clojure syntax"
5. **Handle edge cases** - nil safety, validation, error paths
6. **Test equivalence** - same inputs → same outputs
7. **Add runtime validation** - use spec to replace compile-time guarantees

---

## Type System Mapping

### Primitive Types

| Elm | Clojure | Notes |
|-----|---------|-------|
| `String` | `String` (java.lang.String) | Direct mapping |
| `Int` | `Long` (default) or `Integer` | JVM integers |
| `Float` | `Double` | JVM floating point |
| `Bool` | `Boolean` (true/false) | Direct mapping |
| `Char` | `Character` | Less common in Clojure |
| `()` (unit) | `nil` | Unit type → nil |

### Collection Types

| Elm | Clojure | Notes |
|-----|---------|-------|
| `List a` | `[a]` (vector) | Vectors preferred over lists |
| `List a` | `'(a)` (list) | For sequential processing |
| `Array a` | `[a]` (vector) | Vectors have O(1) indexed access |
| `( a, b )` | `[a b]` (2-element vector) | Tuples → vectors |
| `( a, b, c )` | `[a b c]` | Multi-element tuples |
| `Dict k v` | `{k v}` (hash-map) | Keywords as keys preferred |
| `Set a` | `#{a}` (hash-set) | Direct mapping |

### Composite Types

| Elm | Clojure | Notes |
|-----|---------|-------|
| `type alias User = { name : String }` | `{:name ""}` (map) | Plain maps most idiomatic |
| `type alias User = { name : String }` | `(defrecord User [name])` | Records for performance/protocols |
| `type Msg = A \| B` | `:a` / `:b` (keywords) | Union types → keywords |
| `type Msg = SetName String` | `{:type :set-name :value "x"}` | Tagged data with maps |
| `type Result err ok = Ok ok \| Err err` | `{:ok val}` / `{:error err}` | Result pattern with maps |
| `Maybe a` | `nil` or `a` | Nothing → nil, Just x → x |

---

## Idiom Translation

### Pattern: Union Types to Keywords

Elm uses union types for discriminated unions. Clojure uses keywords or maps.

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

**Clojure:**
```clojure
;; Simple union → keywords
(defn update [model msg]
  (case msg
    :increment (update model :count inc)
    :decrement (update model :count dec)
    ;; For variants with data, use maps
    (if (map? msg)
      (case (:type msg)
        :set-count (assoc model :count (:value msg))
        model)
      model)))

;; Usage:
(update {:count 0} :increment) ; => {:count 1}
(update {:count 5} {:type :set-count :value 10}) ; => {:count 10}
```

**Why this translation:**
- Keywords are lightweight and idiomatic for simple discriminated unions
- Maps with `:type` key pattern for unions with associated data
- More flexible than static types but requires runtime validation

---

### Pattern: Maybe/Nothing to nil

Elm's Maybe type is explicit. Clojure uses nil idiomatically.

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

**Clojure:**
```clojure
(defn find-user [id]
  (when (= id 1)
    {:name "Alice" :age 30}))

(defn display-name [user]
  (if user
    (:name user)
    "Anonymous"))

;; Using threading with some->
(def name
  (some-> (find-user 1)
          :name
          (or "Anonymous")))

;; Or more idiomatically:
(def name
  (or (some-> (find-user 1) :name)
      "Anonymous"))
```

**Why this translation:**
- nil is idiomatic in Clojure for "no value"
- `some->` stops threading on nil (similar to Maybe chaining)
- `or` provides default values
- Less verbose than explicit Just/Nothing pattern matching

---

### Pattern: Result Type to Maps

Elm's Result type makes errors explicit. Clojure uses maps with `:ok`/`:error` keys or throws exceptions.

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

**Clojure:**
```clojure
(defn parse-age [s]
  (if-let [age (try (Long/parseLong s) (catch Exception _ nil))]
    (cond
      (neg? age) {:error "Age must be non-negative"}
      :else {:ok age})
    {:error "Not a valid number"}))

;; Chain results with threading
(defn validate-age [s]
  (let [result (parse-age s)]
    (if (:ok result)
      (let [age (:ok result)]
        (if (< age 120)
          {:ok age}
          {:error "Age must be less than 120"}))
      result)))

;; Alternative: using monadic pattern
(defn and-then [result f]
  (if (:ok result)
    (f (:ok result))
    result))

(defn validate-age [s]
  (-> (parse-age s)
      (and-then (fn [age]
                  (if (< age 120)
                    {:ok age}
                    {:error "Age must be less than 120"})))))
```

**Why this translation:**
- Maps with `:ok`/`:error` keys preserve Result semantics
- More explicit than throwing exceptions
- Allows chaining similar to Result.andThen
- Can also use exceptions for truly exceptional cases

---

### Pattern: The Elm Architecture to Atom + Functions

TEA's Model-Update-View pattern translates to stateful atoms with pure update functions.

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

update : Msg -> Model -> Model
update msg model =
    case msg of
        Increment ->
            { model | count = model.count + 1 }

        Decrement ->
            { model | count = model.count - 1 }

-- VIEW (simplified)
view : Model -> Html Msg
view model =
    div []
        [ button [ onClick Decrement ] [ text "-" ]
        , div [] [ text (String.fromInt model.count) ]
        , button [ onClick Increment ] [ text "+" ]
        ]
```

**Clojure:**
```clojure
;; MODEL - Use atom for state
(def app-state (atom {:count 0}))

;; UPDATE - Pure functions that return new state
(defn update [model msg]
  (case msg
    :increment (update model :count inc)
    :decrement (update model :count dec)
    model))

;; Dispatch - Modifies atom
(defn dispatch! [msg]
  (swap! app-state update msg))

;; Usage:
(dispatch! :increment) ; => {:count 1}
(dispatch! :increment) ; => {:count 2}
(dispatch! :decrement) ; => {:count 1}

;; VIEW (ClojureScript with Reagent/Hiccup)
(defn view [model]
  [:div
   [:button {:on-click #(dispatch! :decrement)} "-"]
   [:div (str (:count model))]
   [:button {:on-click #(dispatch! :increment)} "+"]])
```

**Why this translation:**
- Atoms provide mutable reference to immutable data (like Elm's runtime)
- Update functions remain pure (testable)
- `swap!` ensures atomic updates
- Similar separation of concerns as TEA

---

### Pattern: Pattern Matching

Elm's case expressions are comprehensive. Clojure has case, cond, and destructuring.

**Elm:**
```elm
describe : List a -> String
describe list =
    case list of
        [] ->
            "empty"

        [ x ] ->
            "singleton"

        [ x, y ] ->
            "pair"

        x :: xs ->
            "list with multiple elements"

-- Destructuring records
greet : User -> String
greet user =
    case user of
        { name, age } ->
            "Hello " ++ name ++ ", age " ++ String.fromInt age
```

**Clojure:**
```clojure
(defn describe [lst]
  (case (count lst)
    0 "empty"
    1 "singleton"
    2 "pair"
    "list with multiple elements"))

;; Or with pattern matching using match
;; deps.edn: {:deps {org.clojure/core.match {:mvn/version "1.0.1"}}}
(require '[clojure.core.match :refer [match]])

(defn describe [lst]
  (match [(vec lst)]
    [[]] "empty"
    [[_]] "singleton"
    [[_ _]] "pair"
    [[x & xs]] "list with multiple elements"))

;; Destructuring in function args
(defn greet [{:keys [name age]}]
  (str "Hello " name ", age " age))

(greet {:name "Alice" :age 30})
; => "Hello Alice, age 30"
```

**Why this translation:**
- core.match library provides ML-style pattern matching
- Destructuring in function arguments is idiomatic
- case works for simple value matching
- cond for complex conditions

---

## Error Handling

### Elm Maybe/Result → Clojure nil and Maps

Elm's type system prevents null pointer errors at compile time. Clojure requires runtime discipline and validation.

**Comparison:**

| Aspect | Elm | Clojure |
|--------|-----|---------|
| Null safety | Compile-time via Maybe | Runtime via nil checks |
| Error representation | Result type | Maps with :ok/:error or exceptions |
| Chaining | Maybe.andThen, Result.andThen | some->, and-then helper, or monads |
| Default values | Maybe.withDefault | or, some->, if-let |

**Elm:**
```elm
type Result error value
    = Ok value
    | Err error

fetchUser : Int -> Task Error User
fetchUser id =
    Http.get
        { url = "/api/users/" ++ String.fromInt id
        , decoder = userDecoder
        }
        |> Task.mapError (\_ -> "Network error")

processUser : Task Error String
processUser =
    fetchUser 1
        |> Task.andThen (\user ->
            if String.length user.name > 0 then
                Task.succeed user.name
            else
                Task.fail "Invalid user"
        )
```

**Clojure:**
```clojure
;; Using maps for Result pattern
(defn fetch-user [id]
  (try
    (let [response (http/get (str "/api/users/" id))]
      {:ok (parse-user (:body response))})
    (catch Exception e
      {:error "Network error"})))

(defn process-user []
  (let [result (fetch-user 1)]
    (if (:ok result)
      (let [user (:ok result)]
        (if (pos? (count (:name user)))
          {:ok (:name user)}
          {:error "Invalid user"}))
      result)))

;; Alternative: use exceptions (less functional)
(defn fetch-user! [id]
  (try
    (let [response (http/get (str "/api/users/" id))]
      (parse-user (:body response)))
    (catch Exception e
      (throw (ex-info "Network error" {:id id} e)))))

(defn process-user! []
  (let [user (fetch-user! 1)]
    (when-not (pos? (count (:name user)))
      (throw (ex-info "Invalid user" {:user user})))
    (:name user)))
```

**Best Practices:**
- Use nil idiomatically for optional values
- Use `:ok`/`:error` maps for explicit error handling
- Use exceptions for truly exceptional cases
- Validate at boundaries with clojure.spec

---

## Concurrency Patterns

### Elm Cmd/Sub → Clojure core.async or Callbacks

Elm manages all side effects through Cmd and Sub. Clojure has multiple options: core.async channels, callbacks, or promises.

**Comparison:**

| Aspect | Elm | Clojure |
|--------|-----|---------|
| Async model | Cmd/Sub managed by runtime | core.async channels, callbacks, promises |
| Concurrency | Managed by Elm runtime | Explicit with go blocks or thread pools |
| Message passing | Built-in with Cmd | core.async channels |
| State updates | Always synchronous in update | Atoms, refs, agents for async |

**Elm:**
```elm
-- Cmd: Commands that produce effects
type Msg
    = GotUsers (Result Http.Error (List User))

getUsers : Cmd Msg
getUsers =
    Http.get
        { url = "https://api.example.com/users"
        , expect = Http.expectJson GotUsers (Decode.list userDecoder)
        }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | loading = True }, getUsers )

        GotUsers result ->
            case result of
                Ok users ->
                    ( { model | users = users, loading = False }, Cmd.none )

                Err error ->
                    ( { model | error = Just error, loading = False }, Cmd.none )
```

**Clojure (with core.async):**
```clojure
(require '[clojure.core.async :as async :refer [go chan >! <!]])

;; Message channel
(def msg-chan (chan))

;; Async effect
(defn get-users! [ch]
  (go
    (try
      (let [response (http/get "https://api.example.com/users")
            users (parse-users (:body response))]
        (>! ch {:type :got-users :result {:ok users}}))
      (catch Exception e
        (>! ch {:type :got-users :result {:error e}})))))

;; Update function (pure)
(defn update [model msg]
  (case (:type msg)
    :fetch-users
    (assoc model :loading true)

    :got-users
    (let [result (:result msg)]
      (if (:ok result)
        (assoc model :users (:ok result) :loading false)
        (assoc model :error (:error result) :loading false)))

    model))

;; Dispatch with effects
(defn dispatch! [msg]
  (swap! app-state update msg)
  (when (= (:type msg) :fetch-users)
    (get-users! msg-chan)))

;; Message loop
(go
  (while true
    (let [msg (<! msg-chan)]
      (dispatch! msg))))
```

**Clojure (with callbacks - simpler):**
```clojure
(defn get-users! [on-success on-error]
  (future
    (try
      (let [response (http/get "https://api.example.com/users")
            users (parse-users (:body response))]
        (on-success users))
      (catch Exception e
        (on-error e)))))

(defn fetch-users! []
  (swap! app-state assoc :loading true)
  (get-users!
    (fn [users]
      (swap! app-state assoc :users users :loading false))
    (fn [error]
      (swap! app-state assoc :error error :loading false))))
```

**Why this translation:**
- core.async channels provide Elm-like message passing
- Callbacks are simpler for straightforward async
- Both preserve separation between effects and state updates
- Future/promise patterns also common in Clojure

---

## Common Pitfalls

### 1. Losing Type Safety

**Problem:** Elm's compiler prevents many errors. Clojure requires discipline.

```clojure
;; BAD: No validation
(defn update-user [user]
  (assoc user :age (inc (:age user))))

;; Crashes if :age is nil or not a number
```

**Fix:** Use clojure.spec for runtime validation

```clojure
(require '[clojure.spec.alpha :as s])

(s/def ::name string?)
(s/def ::age (s/and int? pos?))
(s/def ::user (s/keys :req-un [::name ::age]))

(defn update-user [user]
  {:pre [(s/valid? ::user user)]}
  (update user :age inc))

;; Or instrument during development
(s/fdef update-user
  :args (s/cat :user ::user)
  :ret ::user)
```

### 2. Forgetting nil Checks

**Problem:** Maybe forces you to handle Nothing. nil doesn't.

```clojure
;; BAD: Assumes user exists
(defn greet [user]
  (str "Hello, " (:name user)))

(greet nil) ; => "Hello, " (silent bug)
```

**Fix:** Use nil-safe operations

```clojure
;; GOOD: Explicit nil handling
(defn greet [user]
  (if user
    (str "Hello, " (:name user))
    "Hello, stranger"))

;; Or with some->
(defn greet [user]
  (or (some-> user :name (str "Hello, " ,))
      "Hello, stranger"))
```

### 3. Mutable State Confusion

**Problem:** Elm's Model is immutable. Atoms are references to immutable values.

```clojure
;; BAD: Mutating data directly
(def model {:count 0})
(def model {:count 1}) ; Rebinding, not ideal in production

;; GOOD: Use atoms
(def model (atom {:count 0}))
(swap! model update :count inc)
```

### 4. Over-nesting with Threading

**Problem:** Elm's pipeline |> is clear. Clojure's -> can be overused.

```clojure
;; BAD: Deep nesting
(-> user
    :address
    :city
    :name
    .toUpperCase)

;; GOOD: Nil-safe
(some-> user :address :city :name .toUpperCase)

;; BETTER: With validation
(when-let [city (get-in user [:address :city :name])]
  (.toUpperCase city))
```

### 5. Ignoring core.async Blocking

**Problem:** Blocking operations in go blocks can deadlock.

```clojure
;; BAD: Blocking in go block
(go
  (Thread/sleep 1000) ; Blocks thread pool
  (println "Done"))

;; GOOD: Use <! with timeout
(require '[clojure.core.async :as async])
(go
  (<! (async/timeout 1000))
  (println "Done"))

;; Or use thread for blocking operations
(async/thread
  (Thread/sleep 1000)
  (println "Done"))
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| elm-format | Elm code formatter | No direct equivalent; use cljfmt |
| cljfmt | Clojure code formatter | `lein cljfmt` or CLI tool |
| elm-review | Elm linter | Use clj-kondo for Clojure |
| clj-kondo | Clojure linter | Catches common errors |
| elm-test | Elm testing | Use clojure.test, test.check, or Midje |
| clojure.test | Built-in testing | Basic unit testing |
| test.check | Property-based testing | Similar to elm-explorations/test |
| clojure.spec | Runtime validation | Replaces compile-time types |
| Eastwood | Clojure linter | Additional static analysis |
| kibit | Idiom checker | Suggests idiomatic Clojure |

---

## Examples

### Example 1: Simple - Type Alias to Map

Convert a simple Elm type alias to a Clojure map.

**Before (Elm):**
```elm
type alias User =
    { name : String
    , email : String
    , age : Int
    }

user : User
user =
    { name = "Alice"
    , email = "alice@example.com"
    , age = 30
    }

getName : User -> String
getName user =
    user.name
```

**After (Clojure):**
```clojure
;; Option 1: Plain map (most idiomatic)
(def user
  {:name "Alice"
   :email "alice@example.com"
   :age 30})

(defn get-name [user]
  (:name user))

;; Option 2: With spec for validation
(require '[clojure.spec.alpha :as s])

(s/def ::name string?)
(s/def ::email string?)
(s/def ::age pos-int?)
(s/def ::user (s/keys :req-un [::name ::email ::age]))

(defn create-user [name email age]
  (let [user {:name name :email email :age age}]
    (if (s/valid? ::user user)
      user
      (throw (ex-info "Invalid user" (s/explain-data ::user user))))))

;; Option 3: With defrecord (for performance)
(defrecord User [name email age])

(def user (->User "Alice" "alice@example.com" 30))

(defn get-name [user]
  (:name user))
```

---

### Example 2: Medium - Union Types and Pattern Matching

Convert Elm's discriminated unions to Clojure keywords and maps.

**Before (Elm):**
```elm
type Visibility
    = Public
    | Private
    | FriendsOnly

type Post
    = TextPost String Visibility
    | ImagePost String String Visibility  -- url, caption, visibility
    | VideoPost String Int Visibility     -- url, duration, visibility

canView : User -> Post -> Bool
canView user post =
    case post of
        TextPost _ Public ->
            True

        ImagePost _ _ Public ->
            True

        VideoPost _ _ Public ->
            True

        TextPost _ Private ->
            user.isAuthor

        ImagePost _ _ Private ->
            user.isAuthor

        VideoPost _ _ Private ->
            user.isAuthor

        _ ->
            user.isFriend
```

**After (Clojure):**
```clojure
;; Visibility as keywords
;; Post types as maps with :type discriminator

(defn can-view? [user post]
  (case (:visibility post)
    :public true
    :private (:is-author user)
    :friends-only (:is-friend user)
    false))

;; Creating posts
(def text-post
  {:type :text-post
   :content "Hello world"
   :visibility :public})

(def image-post
  {:type :image-post
   :url "https://example.com/image.jpg"
   :caption "Beautiful sunset"
   :visibility :friends-only})

(def video-post
  {:type :video-post
   :url "https://example.com/video.mp4"
   :duration 120
   :visibility :private})

;; With spec validation
(s/def ::visibility #{:public :private :friends-only})
(s/def ::post-type #{:text-post :image-post :video-post})

(s/def ::text-post
  (s/keys :req-un [::type ::content ::visibility]))

(s/def ::image-post
  (s/keys :req-un [::type ::url ::caption ::visibility]))

(s/def ::video-post
  (s/keys :req-un [::type ::url ::duration ::visibility]))

(s/def ::post
  (s/or :text ::text-post
        :image ::image-post
        :video ::video-post))
```

---

### Example 3: Complex - The Elm Architecture to Reagent

Complete conversion of a TEA application to ClojureScript with Reagent.

**Before (Elm):**
```elm
module Main exposing (main)

import Browser
import Html exposing (Html, button, div, input, text)
import Html.Attributes exposing (placeholder, value)
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Decode

-- MODEL

type alias Model =
    { query : String
    , results : List String
    , status : Status
    }

type Status
    = NotAsked
    | Loading
    | Success
    | Failure String

init : () -> ( Model, Cmd Msg )
init _ =
    ( { query = ""
      , results = []
      , status = NotAsked
      }
    , Cmd.none
    )

-- UPDATE

type Msg
    = SetQuery String
    | Search
    | GotResults (Result Http.Error (List String))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        SetQuery newQuery ->
            ( { model | query = newQuery }, Cmd.none )

        Search ->
            ( { model | status = Loading }
            , searchApi model.query
            )

        GotResults result ->
            case result of
                Ok results ->
                    ( { model | results = results, status = Success }
                    , Cmd.none
                    )

                Err error ->
                    ( { model | status = Failure "Search failed" }
                    , Cmd.none
                    )

-- HTTP

searchApi : String -> Cmd Msg
searchApi query =
    Http.get
        { url = "https://api.example.com/search?q=" ++ query
        , expect = Http.expectJson GotResults resultsDecoder
        }

resultsDecoder : Decode.Decoder (List String)
resultsDecoder =
    Decode.field "results" (Decode.list Decode.string)

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ input
            [ placeholder "Search..."
            , value model.query
            , onInput SetQuery
            ]
            []
        , button [ onClick Search ] [ text "Search" ]
        , viewStatus model.status
        , viewResults model.results
        ]

viewStatus : Status -> Html Msg
viewStatus status =
    case status of
        NotAsked ->
            text ""

        Loading ->
            text "Loading..."

        Success ->
            text "Success!"

        Failure error ->
            text error

viewResults : List String -> Html Msg
viewResults results =
    div []
        (List.map (\result -> div [] [ text result ]) results)

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

**After (Clojure/ClojureScript with Reagent):**
```clojure
(ns myapp.core
  (:require [reagent.core :as r]
            [ajax.core :refer [GET]]))

;; MODEL - Use reagent atom for reactive state
(defonce app-state
  (r/atom {:query ""
           :results []
           :status :not-asked}))

;; UPDATE - Pure functions
(defn update-query [model query]
  (assoc model :query query))

(defn start-search [model]
  (assoc model :status :loading))

(defn search-success [model results]
  (assoc model
         :results results
         :status :success))

(defn search-failure [model error]
  (assoc model :status {:failure "Search failed"}))

;; EFFECTS
(defn search-api! [query]
  (GET "https://api.example.com/search"
       {:params {:q query}
        :handler (fn [response]
                   (swap! app-state search-success (:results response)))
        :error-handler (fn [error]
                         (swap! app-state search-failure error))}))

;; DISPATCH
(defn dispatch! [msg]
  (case (:type msg)
    :set-query
    (swap! app-state update-query (:value msg))

    :search
    (do
      (swap! app-state start-search)
      (search-api! (:query @app-state)))

    nil))

;; VIEW COMPONENTS
(defn view-status [status]
  (cond
    (= status :not-asked) [:div]
    (= status :loading) [:div "Loading..."]
    (= status :success) [:div "Success!"]
    (map? status) [:div (:failure status)]
    :else [:div]))

(defn view-results [results]
  [:div
   (for [result results]
     ^{:key result}
     [:div result])])

(defn view []
  (let [model @app-state]
    [:div
     [:input {:placeholder "Search..."
              :value (:query model)
              :on-change #(dispatch! {:type :set-query
                                     :value (-> % .-target .-value)})}]
     [:button {:on-click #(dispatch! {:type :search})}
      "Search"]
     [view-status (:status model)]
     [view-results (:results model)]]))

;; MAIN
(defn mount-root []
  (r/render [view]
            (.getElementById js/document "app")))

(defn init []
  (mount-root))
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-elm-clojurescript` - Elm to ClojureScript (frontend-to-frontend)
- `lang-elm-dev` - Elm development patterns
- `lang-clojure-dev` - Clojure development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async, channels, threads across languages
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Type-driven design vs macros
