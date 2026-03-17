---
name: convert-python-elm
description: Convert Python code to idiomatic Elm. Use when migrating Python backends to Elm frontends, translating Python logic to type-safe frontend code, or refactoring Python codebases into functional-first Elm applications. Extends meta-convert-dev with Python-to-Elm specific patterns focused on The Elm Architecture (TEA).
---

# Convert Python to Elm

Convert Python code to idiomatic Elm for type-safe frontend applications. This skill extends `meta-convert-dev` with Python-to-Elm specific type mappings, idiom translations, and patterns for transforming dynamic, imperative Python code into functional, purely-functional Elm code with The Elm Architecture.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Python types → Elm types (dynamic → static, runtime → compile-time)
- **Idiom translations**: Imperative/OOP Python → functional-first Elm
- **Error handling**: try/except → Result/Maybe with pattern matching
- **Concurrency**: Python async/threading → The Elm Architecture (Cmd/Sub)
- **Metaprogramming**: Python decorators/metaclasses → elm-codegen and derivation patterns
- **Architecture translation**: Any Python pattern → The Elm Architecture (TEA)
- **Platform differences**: Backend/CLI Python → Frontend browser-based Elm
- **No runtime exceptions**: All errors handled at compile-time or through types
- **JSON serialization**: Pydantic → Json.Decode/Json.Encode pipelines

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Python language fundamentals - see `lang-python-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → Python) - not typically needed
- Fable.Python (F# to Python via Fable) - different toolchain

---

## Quick Reference

| Python | Elm | Notes |
|--------|------|-------|
| `int` | `Int` | Elm Int is JavaScript number (53-bit precision) |
| `float` | `Float` | IEEE 754 double precision |
| `bool` | `Bool` | Direct mapping |
| `str` | `String` | UTF-8 in Elm vs Python's unicode |
| `bytes` | - | No direct equivalent; use String or Array Int |
| `list[T]` | `List a` | Immutable linked list |
| `tuple` | `( a, b )` / `( a, b, c )` | Max 3-tuple in Elm |
| `dict[K, V]` | `Dict comparable v` | Key must be comparable |
| `set[T]` | `Set comparable` | Value must be comparable |
| `None` | `Nothing` (in `Maybe a`) | Explicit optional |
| `Union[T, U]` | `type X = A T \| B U` | Discriminated union |
| `Callable` | `a -> b` | Function type |
| `async def` | `Cmd Msg` / `Task error value` | No async/await; effects at edges |
| `@dataclass` | `type alias Record = { }` | Records with structural equality |
| `try/except` | `Result error value` | No exceptions; use Result/Maybe |
| `class` | N/A (use TEA) | No OOP; use Model-Update-View pattern |

## When Converting Code

1. **Analyze source thoroughly** before writing target - understand data flow
2. **Map types first** - create type equivalence table
3. **Identify side effects** - all effects go through Cmd/Sub in Elm
4. **Embrace immutability** - Elm has no mutable state
5. **Adopt The Elm Architecture** - don't write "Python code in Elm syntax"
6. **No runtime exceptions** - compiler catches all errors
7. **JSON handling is explicit** - write decoders/encoders for all data
8. **Test equivalence** - same inputs → same outputs (for pure functions)

---

## Critical Paradigm Shift: Python → Elm

### What Makes This Conversion Different

Python to Elm is not just a syntax translation - it represents a fundamental shift in programming paradigm:

| Aspect | Python | Elm |
|--------|--------|-----|
| **Type System** | Dynamic, runtime | Static, compile-time |
| **Null Safety** | None everywhere, NoneType errors | Maybe type, no null |
| **Error Handling** | Exceptions | Result/Maybe, no exceptions |
| **Mutability** | Mutable by default | Immutable always |
| **Side Effects** | Anywhere | Only through Cmd/Sub at edges |
| **Concurrency** | async/await, threading | N/A - single-threaded with Cmd/Sub |
| **OOP** | Classes, inheritance | N/A - data and functions separate |
| **Runtime** | CPython, PyPy (backend) | JavaScript (browser) |
| **Package Manager** | pip, poetry | elm.json |
| **REPL** | Interactive Python shell | elm repl (limited) |

### The Elm Philosophy

**"If it compiles, it works"** - Elm's compiler is so strict that runtime exceptions are virtually impossible:

- **No null pointer exceptions** - Maybe type makes absence explicit
- **No undefined is not a function** - All types known at compile time
- **No runtime type errors** - Static types prevent mismatches
- **No silent failures** - Result type makes errors explicit

**Making Impossible States Impossible** - Elm encourages modeling your domain such that invalid states cannot be represented:

```python
# Python: Invalid states possible
class User:
    def __init__(self):
        self.loading = False
        self.data = None
        self.error = None

    # Problem: Can have loading=True, data=X, error=Y simultaneously!
```

```elm
-- Elm: Invalid states impossible
type UserState
    = Loading
    | Success User
    | Failure Http.Error

-- Can only be in ONE state at a time
```

---

## The 10 Pillars of Conversion

This skill organizes Python → Elm conversion patterns into 10 pillars based on the `meta-convert-dev` framework:

1. **Module System** - Python packages → Elm modules
2. **Error Handling** - Exceptions → Result/Maybe
3. **Concurrency** - async/await → Cmd/Sub (Elm Architecture)
4. **Metaprogramming** - Decorators/metaclasses → elm-codegen
5. **Zero/Default Values** - None/defaults → Maybe/withDefault
6. **Serialization** - Pydantic → Json.Decode/Json.Encode
7. **Build & Dependencies** - pip/poetry → elm.json
8. **Testing** - pytest → elm-test
9. **Dev Workflow & REPL** - Python REPL → elm repl/reactor
10. **FFI/Interop** - C extensions → Ports (JavaScript interop)

Each pillar is covered in detail below.

---

## Pillar 1: Module System Translation

Python's flexible module system with dynamic imports contrasts with Elm's strict, static module system.

### Module Declaration

**Python:**
```python
# mymodule.py - filename determines module name
# No explicit declaration needed

def public_function():
    pass

def _private_function():
    pass

__all__ = ['public_function']  # Optional export control
```

**Elm:**
```elm
-- MyModule.elm - filename must match module name
module MyModule exposing (publicFunction)

-- Must explicitly declare what's exposed
publicFunction : String -> String
publicFunction input =
    privateFunction input

-- Not exposed, module-private
privateFunction : String -> String
privateFunction input =
    String.toUpper input
```

### Import Patterns

| Python | Elm | Notes |
|--------|------|-------|
| `import json` | `import Json.Decode` | Qualified import |
| `import json as j` | `import Json.Decode as Decode` | Alias |
| `from json import loads` | `import Json.Decode exposing (decodeString)` | Specific items |
| `from json import *` | `import Json.Decode exposing (..)` | All items (discouraged) |
| `import .relative` | - | No relative imports in Elm |

### Package Structure

**Python:**
```
myproject/
  myproject/
    __init__.py       # Package marker
    core.py
    utils/
      __init__.py
      helpers.py
```

**Elm:**
```
myproject/
  src/
    Main.elm          # Entry point
    Core.elm          # No __init__ needed
    Utils/
      Helpers.elm     # Capitalized names
```

### Avoiding Import Cycles

**Python:**
```python
# a.py
from b import B
class A:
    def use_b(self, b: B):
        pass

# b.py
from a import A  # Circular import!
class B:
    def use_a(self, a: A):
        pass

# Solution: Move to separate types.py or use TYPE_CHECKING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from a import A
```

**Elm:**
```elm
-- Elm PROHIBITS circular imports at compile time

-- Solution: Extract shared types
-- Types.elm
module Types exposing (User, Msg(..))

type alias User = { name : String }
type Msg = UpdateUser User

-- ModuleA.elm
import Types exposing (User, Msg)

-- ModuleB.elm
import Types exposing (User, Msg)
```

### Opaque Types (Encapsulation)

**Python:**
```python
# email.py
class Email:
    def __init__(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._value = value  # Convention: _ = private

    @property
    def value(self) -> str:
        return self._value

# Users can still access _value directly (no true privacy)
```

**Elm:**
```elm
-- Email.elm
module Email exposing (Email, fromString, toString)

-- Opaque type: constructor NOT exposed
type Email = Email String

fromString : String -> Maybe Email
fromString str =
    if String.contains "@" str then
        Just (Email str)
    else
        Nothing

toString : Email -> String
toString (Email str) =
    str

-- Users CANNOT construct Email directly
-- Email "invalid" → Compile error!
```

---

## Pillar 2: Error Handling Translation

Python's exception-based error handling fundamentally differs from Elm's type-based error handling.

### Exception Model → Result/Maybe Types

**Python exceptions:**
- Thrown anywhere
- Propagate up the stack
- Can crash if not caught
- Types not tracked

**Elm Result/Maybe:**
- Explicit in type signature
- Must be handled explicitly
- Cannot crash (compiler enforces handling)
- Types tracked at compile time

### Try/Except → Pattern Matching

**Python:**
```python
def parse_user(json_str: str) -> User:
    try:
        data = json.loads(json_str)
        return User(
            name=data['name'],
            email=data['email']
        )
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Failed to parse user: {e}")
    except Exception as e:
        # Unexpected error
        raise
```

**Elm:**
```elm
-- All errors are values, not exceptions
parseUser : String -> Result String User
parseUser jsonStr =
    Decode.decodeString userDecoder jsonStr
        |> Result.mapError (\err -> "Failed to parse user: " ++ Decode.errorToString err)

-- Type signature SHOWS this can fail
-- Compiler FORCES caller to handle Result
```

### None/AttributeError → Maybe

**Python:**
```python
def get_user_email(user_id: int) -> str | None:
    user = database.get(user_id)  # Returns None if not found
    if user is None:
        return None
    return user.email

# Usage:
email = get_user_email(123)
if email is not None:
    send_email(email)
else:
    print("User not found")
```

**Elm:**
```elm
getUserEmail : Int -> Maybe String
getUserEmail userId =
    Dict.get userId database
        |> Maybe.map .email

-- Usage: Explicit handling required
case getUserEmail 123 of
    Just email ->
        sendEmail email

    Nothing ->
        "User not found"

-- Or use Maybe combinators
getUserEmail 123
    |> Maybe.withDefault "no-reply@example.com"
    |> sendEmail
```

### Result Combinators vs Try/Except Chains

**Python:**
```python
def process_order(order_id: int) -> Order:
    try:
        raw_order = fetch_order(order_id)
    except HTTPError as e:
        raise OrderError(f"Failed to fetch: {e}")

    try:
        validated = validate_order(raw_order)
    except ValidationError as e:
        raise OrderError(f"Validation failed: {e}")

    try:
        saved = save_order(validated)
    except DatabaseError as e:
        raise OrderError(f"Save failed: {e}")

    return saved
```

**Elm:**
```elm
-- Railway-Oriented Programming
processOrder : Int -> Task Error Order
processOrder orderId =
    fetchOrder orderId
        |> Task.andThen validateOrder
        |> Task.andThen saveOrder

-- All errors flow through the Result/Task
-- No hidden exceptions
-- Type signature shows Error possibility
```

### Error Types Translation

**Python:**
```python
class AppError(Exception):
    pass

class NotFoundError(AppError):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found")

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}")

# Usage:
raise NotFoundError("User")
```

**Elm:**
```elm
-- Use discriminated unions for errors
type AppError
    = NotFound String
    | ValidationError String String
    | NetworkError Http.Error

-- Usage: Return error as value
findUser : Int -> Result AppError User
findUser id =
    case Dict.get id users of
        Just user ->
            Ok user

        Nothing ->
            Err (NotFound "User")

-- Pattern match to handle
case findUser 123 of
    Ok user ->
        viewUser user

    Err (NotFound resource) ->
        text ("Not found: " ++ resource)

    Err (ValidationError field msg) ->
        text (field ++ ": " ++ msg)

    Err (NetworkError httpErr) ->
        text "Network error"
```

### Validation Patterns

**Python (with Pydantic):**
```python
from pydantic import BaseModel, validator, ValidationError

class User(BaseModel):
    name: str
    email: str
    age: int

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v

# Usage:
try:
    user = User(name="Alice", email="alice@example.com", age=30)
except ValidationError as e:
    print(e.errors())
```

**Elm:**
```elm
-- Validation returns Result
type alias User =
    { name : String
    , email : String
    , age : Int
    }

type ValidationError
    = InvalidEmail
    | InvalidAge

validateEmail : String -> Result ValidationError String
validateEmail email =
    if String.contains "@" email then
        Ok email
    else
        Err InvalidEmail

validateAge : Int -> Result ValidationError Int
validateAge age =
    if age >= 0 then
        Ok age
    else
        Err InvalidAge

createUser : String -> String -> Int -> Result ValidationError User
createUser name email age =
    Result.map3 User
        (Ok name)
        (validateEmail email)
        (validateAge age)

-- Usage: Must handle Result
case createUser "Alice" "alice@example.com" 30 of
    Ok user ->
        -- Success
        viewUser user

    Err InvalidEmail ->
        text "Invalid email address"

    Err InvalidAge ->
        text "Age must be positive"
```

---

## Pillar 3: Concurrency Translation

**Critical Note:** Elm has NO concurrency model in the traditional sense. Elm is single-threaded and runs in the browser's event loop. All "async" operations are managed through **The Elm Architecture** via `Cmd` and `Sub`.

### Python Async/Threading → Elm Architecture

**Python async/await:**
```python
import asyncio
import aiohttp

async def fetch_users():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com/users') as response:
            return await response.json()

async def main():
    users = await fetch_users()
    print(f"Fetched {len(users)} users")

asyncio.run(main())
```

**Elm with Cmd (no async/await):**
```elm
-- ALL effects happen at the edges via Cmd
type Msg
    = FetchUsers
    | GotUsers (Result Http.Error (List User))

type alias Model =
    { users : List User
    , status : String
    }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | status = "Loading..." }
            , Http.get
                { url = "https://api.example.com/users"
                , expect = Http.expectJson GotUsers usersDecoder
                }
            )

        GotUsers (Ok users) ->
            ( { model | users = users, status = "Success" }
            , Cmd.none
            )

        GotUsers (Err error) ->
            ( { model | status = "Failed to fetch users" }
            , Cmd.none
            )

-- No "await" - results come back as Msg
```

### Threading → No Threading

**Python threading:**
```python
import threading
import queue

def worker(q):
    while True:
        item = q.get()
        if item is None:
            break
        process(item)
        q.task_done()

q = queue.Queue()
threads = []
for i in range(4):
    t = threading.Thread(target=worker, args=(q,))
    t.start()
    threads.append(t)

# Add work
for item in items:
    q.put(item)

# Wait for completion
q.join()
```

**Elm (no threading):**
```elm
-- Elm is single-threaded
-- All operations happen in sequence in the event loop
-- For "parallel" HTTP requests, use batch:

type Msg
    = FetchAll
    | GotUser1 (Result Http.Error User)
    | GotUser2 (Result Http.Error User)
    | GotUser3 (Result Http.Error User)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchAll ->
            ( model
            , Cmd.batch
                [ Http.get { url = "/user/1", expect = Http.expectJson GotUser1 userDecoder }
                , Http.get { url = "/user/2", expect = Http.expectJson GotUser2 userDecoder }
                , Http.get { url = "/user/3", expect = Http.expectJson GotUser3 userDecoder }
                ]
            )

        -- Handle each response separately
        GotUser1 result ->
            -- ...

        GotUser2 result ->
            -- ...

        GotUser3 result ->
            -- ...

-- Requests happen "in parallel" (browser manages concurrency)
-- But results are processed sequentially in update function
```

### Background Tasks → Subscriptions

**Python (background polling):**
```python
import asyncio

async def poll_status():
    while True:
        status = await fetch_status()
        print(f"Status: {status}")
        await asyncio.sleep(5)

asyncio.create_task(poll_status())
```

**Elm (subscriptions):**
```elm
-- Subscriptions provide ongoing effects
import Time

type Msg
    = Tick Time.Posix
    | GotStatus (Result Http.Error Status)

subscriptions : Model -> Sub Msg
subscriptions model =
    Time.every 5000 Tick  -- Every 5 seconds

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Tick time ->
            ( model
            , Http.get
                { url = "/status"
                , expect = Http.expectJson GotStatus statusDecoder
                }
            )

        GotStatus (Ok status) ->
            ( { model | status = status }
            , Cmd.none
            )

        GotStatus (Err _) ->
            ( model, Cmd.none )
```

### WebSockets

**Python (websockets library):**
```python
import asyncio
import websockets

async def listen():
    async with websockets.connect('ws://localhost:8000') as ws:
        async for message in ws:
            print(f"Received: {message}")

asyncio.run(listen())
```

**Elm (ports for WebSockets):**
```elm
-- WebSockets via ports (JavaScript interop)
port module Main exposing (..)

-- Outgoing: Send to JavaScript
port sendMessage : String -> Cmd msg

-- Incoming: Receive from JavaScript
port receiveMessage : (String -> msg) -> Sub msg

type Msg
    = Send String
    | Receive String

subscriptions : Model -> Sub Msg
subscriptions model =
    receiveMessage Receive

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Send message ->
            ( model, sendMessage message )

        Receive message ->
            ( { model | messages = message :: model.messages }
            , Cmd.none
            )
```

```javascript
// JavaScript side (ports)
const app = Elm.Main.init({ node: document.getElementById('elm') });

const ws = new WebSocket('ws://localhost:8000');

ws.onmessage = (event) => {
    app.ports.receiveMessage.send(event.data);
};

app.ports.sendMessage.subscribe((message) => {
    ws.send(message);
});
```

### Concurrency Checklist

When converting Python concurrency to Elm:

- [ ] Identify all async operations (HTTP, timers, WebSockets)
- [ ] Model each async result as a Msg variant
- [ ] Use `Cmd` for one-off effects (HTTP requests)
- [ ] Use `Sub` for ongoing effects (timers, WebSocket messages)
- [ ] Use `Cmd.batch` for "parallel" operations
- [ ] Use ports for complex async (WebSockets, file I/O)
- [ ] Remove all threading code (Elm is single-threaded)
- [ ] Remove all mutexes/locks (Elm is immutable)

---

## Pillar 4: Metaprogramming Translation

**Critical Note:** Elm has NO runtime metaprogramming. No decorators, no metaclasses, no `eval()`, no dynamic code generation at runtime.

### Python Metaprogramming → Elm Alternatives

| Python Metaprogramming | Elm Alternative | Notes |
|------------------------|-----------------|-------|
| Decorators | Higher-order functions | Wrap functions at compile time |
| Metaclasses | elm-codegen | Generate code before compilation |
| `@property` | Record fields | Direct field access |
| `__getattr__` | N/A | No dynamic attribute access |
| `type()` / `isinstance()` | Discriminated unions | Pattern matching |
| `eval()` / `exec()` | N/A | No runtime code evaluation |
| Descriptor protocol | N/A | No dynamic behavior |
| Context managers | N/A | Use explicit cleanup in ports |

### Decorators → Higher-Order Functions

**Python decorators:**
```python
import time
from functools import wraps

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timing
def slow_function(n):
    time.sleep(n)
    return n * 2

result = slow_function(2)  # Prints timing info
```

**Elm (higher-order functions):**
```elm
-- Elm has no side effects in functions, so timing must go through Cmd
-- But the pattern of wrapping functions works:

type alias Logger msg =
    { log : String -> Cmd msg
    }

withLogging : Logger msg -> (a -> b) -> a -> ( b, Cmd msg )
withLogging logger func input =
    let
        result =
            func input

        logMsg =
            "Function executed with input: " ++ Debug.toString input
    in
    ( result, logger.log logMsg )

-- Usage:
slowFunction : Int -> Int
slowFunction n =
    n * 2

-- In update function:
let
    ( result, cmd ) =
        withLogging logger slowFunction 2
in
( { model | result = result }, cmd )
```

### Code Generation: Python → elm-codegen

**Python (dynamic code generation):**
```python
# Generate classes dynamically
def make_model(fields):
    class DynamicModel:
        def __init__(self, **kwargs):
            for field in fields:
                setattr(self, field, kwargs.get(field))

    return DynamicModel

User = make_model(['name', 'email', 'age'])
user = User(name="Alice", email="alice@example.com", age=30)
```

**Elm (elm-codegen):**
```elm
-- Elm cannot generate code at runtime
-- Use elm-codegen to generate Elm code before compilation

-- codegen/Generate.elm (runs before compilation)
module Generate exposing (main)

import Elm
import Elm.Annotation as Type

main : Program {} () ()
main =
    Elm.generate "src/Generated/Models.elm"
        [ Elm.file [ "Generated", "Models" ]
            [ Elm.alias "User"
                (Type.record
                    [ ( "name", Type.string )
                    , ( "email", Type.string )
                    , ( "age", Type.int )
                    ]
                )
            ]
        ]

-- Run: elm-codegen run
-- Generates src/Generated/Models.elm with type alias User
```

### Property Accessors → Record Fields

**Python:**
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

    @property
    def circumference(self):
        return 2 * 3.14159 * self._radius

circle = Circle(5)
print(circle.area)  # Computed property
```

**Elm:**
```elm
-- No computed properties
-- Use functions instead

type alias Circle =
    { radius : Float
    }

area : Circle -> Float
area circle =
    pi * circle.radius ^ 2

circumference : Circle -> Float
circumference circle =
    2 * pi * circle.radius

-- Usage:
circle = { radius = 5 }
area circle |> Debug.toString
```

### Type Introspection → Pattern Matching

**Python:**
```python
from typing import Union

def process(value: Union[int, str, list]):
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    elif isinstance(value, list):
        return len(value)
    else:
        raise TypeError(f"Unexpected type: {type(value)}")
```

**Elm:**
```elm
-- Use discriminated unions + pattern matching
type Value
    = IntValue Int
    | StringValue String
    | ListValue (List a)

process : Value -> Int
process value =
    case value of
        IntValue n ->
            n * 2

        StringValue str ->
            String.length str  -- Can't return different types

        ListValue list ->
            List.length list

-- Note: All branches must return same type
-- This is a FEATURE - prevents type confusion
```

### Metaprogramming Checklist

When converting Python metaprogramming to Elm:

- [ ] Replace decorators with higher-order functions
- [ ] Move code generation to elm-codegen (pre-compilation)
- [ ] Replace `@property` with explicit functions
- [ ] Replace `isinstance()` checks with discriminated unions
- [ ] Remove all `eval()`/`exec()` code (no equivalent)
- [ ] Document which metaprogramming patterns have no Elm equivalent
- [ ] Consider if JavaScript interop (ports) is needed

---

## Pillar 5: Zero and Default Values Translation

Python and Elm have fundamentally different approaches to "absence of value."

### None → Maybe

**Python:**
```python
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    if user_id in users:
        return users[user_id]
    else:
        return None

# Usage:
user = find_user(123)
if user is not None:
    print(user['name'])
else:
    print("Not found")

# Or with walrus operator:
if (user := find_user(123)) is not None:
    print(user['name'])
```

**Elm:**
```elm
findUser : Int -> Maybe User
findUser userId =
    Dict.get userId users

-- Usage: Must handle Maybe explicitly
case findUser 123 of
    Just user ->
        text user.name

    Nothing ->
        text "Not found"

-- Or with Maybe.withDefault:
findUser 123
    |> Maybe.map .name
    |> Maybe.withDefault "Not found"
    |> text
```

### Default Arguments → Record Update

**Python:**
```python
def create_user(name: str, email: str = "no-reply@example.com", age: int = 0):
    return {
        'name': name,
        'email': email,
        'age': age
    }

user1 = create_user("Alice")
user2 = create_user("Bob", email="bob@example.com")
user3 = create_user("Charlie", age=30)
```

**Elm:**
```elm
-- No default arguments in Elm
-- Pattern 1: Multiple constructor functions

type alias User =
    { name : String
    , email : String
    , age : Int
    }

createUser : String -> String -> Int -> User
createUser name email age =
    { name = name, email = email, age = age }

createUserWithDefaults : String -> User
createUserWithDefaults name =
    { name = name
    , email = "no-reply@example.com"
    , age = 0
    }

-- Pattern 2: Builder pattern with record update
defaultUser : User
defaultUser =
    { name = ""
    , email = "no-reply@example.com"
    , age = 0
    }

user1 = { defaultUser | name = "Alice" }
user2 = { defaultUser | name = "Bob", email = "bob@example.com" }
user3 = { defaultUser | name = "Charlie", age = 30 }

-- Pattern 3: Config record
type alias UserConfig =
    { name : String
    , email : Maybe String
    , age : Maybe Int
    }

createUserFromConfig : UserConfig -> User
createUserFromConfig config =
    { name = config.name
    , email = Maybe.withDefault "no-reply@example.com" config.email
    , age = Maybe.withDefault 0 config.age
    }

user1 = createUserFromConfig { name = "Alice", email = Nothing, age = Nothing }
user2 = createUserFromConfig { name = "Bob", email = Just "bob@example.com", age = Nothing }
```

### Mutable Default Arguments (Gotcha!)

**Python (dangerous pattern):**
```python
def append_to(element, target=[]):  # DANGEROUS!
    target.append(element)
    return target

# Gotcha: Default list is shared!
list1 = append_to(1)  # [1]
list2 = append_to(2)  # [1, 2] ← Shared state!

# Correct pattern:
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target
```

**Elm (impossible to have this bug):**
```elm
-- Elm has no mutable defaults or mutable anything
appendTo : a -> List a -> List a
appendTo element target =
    target ++ [ element ]

-- Always creates new list
list1 = appendTo 1 []       -- [1]
list2 = appendTo 2 []       -- [2]
list3 = appendTo 3 list1    -- [1, 3]
-- list1 is still [1] - immutable!
```

### Dictionary Defaults

**Python:**
```python
from collections import defaultdict

# Pattern 1: defaultdict
counts = defaultdict(int)
counts['apples'] += 1  # 0 + 1 = 1

# Pattern 2: dict.get with default
counts = {}
counts['apples'] = counts.get('apples', 0) + 1

# Pattern 3: dict.setdefault
counts = {}
counts.setdefault('apples', 0)
counts['apples'] += 1
```

**Elm:**
```elm
-- Dict.update pattern (functional)
counts : Dict String Int
counts =
    Dict.empty

incrementCount : String -> Dict String Int -> Dict String Int
incrementCount key dict =
    Dict.update key
        (\maybeValue ->
            case maybeValue of
                Just count ->
                    Just (count + 1)

                Nothing ->
                    Just 1
        )
        dict

-- Usage:
newCounts = incrementCount "apples" counts

-- Or helper function:
incrementDefault : comparable -> Int -> Dict comparable Int -> Dict comparable Int
incrementDefault key default dict =
    Dict.insert key
        (Dict.get key dict |> Maybe.withDefault default |> (+) 1)
        dict
```

### Falsy Values

**Python (truthy/falsy):**
```python
# Many values are "falsy" in Python
if not value:  # Could be: None, False, 0, "", [], {}, etc.
    print("Falsy!")

# Explicit checks often better:
if value is None:
    print("Actually None")

if value == "":
    print("Empty string")

if len(value) == 0:
    print("Empty collection")
```

**Elm (no truthiness):**
```elm
-- ONLY Bool values can be used in conditions
-- No truthiness/falsiness concept

-- Check for Maybe:
case maybeValue of
    Just value -> "Has value"
    Nothing -> "No value"

-- Check for empty:
if String.isEmpty str then
    "Empty string"
else
    "Has content"

if List.isEmpty list then
    "Empty list"
else
    "Has items"

-- No implicit boolean conversion
-- This is a COMPILE ERROR:
-- if someString then ...  ← ERROR: String is not Bool
```

---

## Pillar 6: Serialization Translation

Python's Pydantic and JSON handling is runtime-based; Elm's JSON decoders/encoders are compile-time safe.

### Pydantic → Json.Decode

**Python (Pydantic):**
```python
from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    zip_code: Optional[str] = None

class User(BaseModel):
    id: int
    name: str
    email: str
    address: Optional[Address] = None

# Automatic parsing:
json_str = '{"id": 1, "name": "Alice", "email": "alice@example.com"}'
user = User.parse_raw(json_str)  # Automatic!
print(user.name)  # Alice
```

**Elm (Json.Decode):**
```elm
import Json.Decode as Decode exposing (Decoder)
import Json.Decode.Pipeline exposing (required, optional)

type alias Address =
    { street : String
    , city : String
    , zipCode : Maybe String
    }

type alias User =
    { id : Int
    , name : String
    , email : String
    , address : Maybe Address
    }

-- Must write explicit decoder
addressDecoder : Decoder Address
addressDecoder =
    Decode.succeed Address
        |> required "street" Decode.string
        |> required "city" Decode.string
        |> optional "zip_code" (Decode.nullable Decode.string) Nothing

userDecoder : Decoder User
userDecoder =
    Decode.succeed User
        |> required "id" Decode.int
        |> required "name" Decode.string
        |> required "email" Decode.string
        |> optional "address" (Decode.nullable addressDecoder) Nothing

-- Usage:
jsonStr = """{"id": 1, "name": "Alice", "email": "alice@example.com"}"""

case Decode.decodeString userDecoder jsonStr of
    Ok user ->
        text user.name

    Err error ->
        text ("Decode failed: " ++ Decode.errorToString error)
```

### JSON Encoding

**Python:**
```python
import json
from dataclasses import dataclass, asdict

@dataclass
class User:
    id: int
    name: str
    email: str

user = User(id=1, name="Alice", email="alice@example.com")
json_str = json.dumps(asdict(user))
# {"id": 1, "name": "Alice", "email": "alice@example.com"}
```

**Elm:**
```elm
import Json.Encode as Encode

type alias User =
    { id : Int
    , name : String
    , email : String
    }

encodeUser : User -> Encode.Value
encodeUser user =
    Encode.object
        [ ( "id", Encode.int user.id )
        , ( "name", Encode.string user.name )
        , ( "email", Encode.string user.email )
        ]

-- Usage:
user = { id = 1, name = "Alice", email = "alice@example.com" }
jsonStr = Encode.encode 0 (encodeUser user)
-- {"id":1,"name":"Alice","email":"alice@example.com"}
```

### Nested JSON

**Python:**
```python
from pydantic import BaseModel
from typing import List

class Comment(BaseModel):
    author: str
    text: str

class Post(BaseModel):
    title: str
    comments: List[Comment]

json_data = {
    "title": "Hello",
    "comments": [
        {"author": "Alice", "text": "Great!"},
        {"author": "Bob", "text": "Thanks!"}
    ]
}

post = Post(**json_data)
print(post.comments[0].author)  # Alice
```

**Elm:**
```elm
import Json.Decode as Decode exposing (Decoder)
import Json.Decode.Pipeline exposing (required)

type alias Comment =
    { author : String
    , text : String
    }

type alias Post =
    { title : String
    , comments : List Comment
    }

commentDecoder : Decoder Comment
commentDecoder =
    Decode.succeed Comment
        |> required "author" Decode.string
        |> required "text" Decode.string

postDecoder : Decoder Post
postDecoder =
    Decode.succeed Post
        |> required "title" Decode.string
        |> required "comments" (Decode.list commentDecoder)

-- Usage:
jsonStr = """
{
  "title": "Hello",
  "comments": [
    {"author": "Alice", "text": "Great!"},
    {"author": "Bob", "text": "Thanks!"}
  ]
}
"""

case Decode.decodeString postDecoder jsonStr of
    Ok post ->
        case List.head post.comments of
            Just firstComment ->
                text firstComment.author

            Nothing ->
                text "No comments"

    Err error ->
        text ("Decode failed: " ++ Decode.errorToString error)
```

### Handling API Variants

**Python:**
```python
from typing import Union, Literal
from pydantic import BaseModel

class SuccessResponse(BaseModel):
    status: Literal["success"]
    data: dict

class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str

Response = Union[SuccessResponse, ErrorResponse]

def handle_response(response: Response):
    if isinstance(response, SuccessResponse):
        print(response.data)
    elif isinstance(response, ErrorResponse):
        print(f"Error: {response.message}")
```

**Elm:**
```elm
-- Use discriminated union + oneOf decoder
type ApiResponse
    = Success (Dict String String)
    | Error String

apiResponseDecoder : Decoder ApiResponse
apiResponseDecoder =
    Decode.field "status" Decode.string
        |> Decode.andThen
            (\status ->
                case status of
                    "success" ->
                        Decode.map Success
                            (Decode.field "data" (Decode.dict Decode.string))

                    "error" ->
                        Decode.map Error
                            (Decode.field "message" Decode.string)

                    _ ->
                        Decode.fail ("Unknown status: " ++ status)
            )

-- Usage:
handleResponse : ApiResponse -> String
handleResponse response =
    case response of
        Success data ->
            "Got data: " ++ Debug.toString data

        Error message ->
            "Error: " ++ message
```

### Serialization Checklist

When converting Python serialization to Elm:

- [ ] Replace Pydantic models with Elm type aliases + decoders
- [ ] Write explicit decoder for each type
- [ ] Write explicit encoder for each type (if sending JSON)
- [ ] Use `Json.Decode.Pipeline` for complex decoders
- [ ] Handle optional fields with `optional` from pipeline
- [ ] Use `andThen` for conditional decoding (union types)
- [ ] Test decoders with sample JSON data
- [ ] Document field name mappings (snake_case → camelCase)

---

## Pillar 7: Build & Dependencies Translation

### Package Management

| Python | Elm | Notes |
|--------|-----|-------|
| `requirements.txt` | `elm.json` | Dependency manifest |
| `pyproject.toml` | `elm.json` | Modern Python ≈ Elm manifest |
| `pip install` | `elm install` | Install dependency |
| `pip install -e .` | N/A | No editable installs |
| `venv` / `virtualenv` | N/A | Elm dependencies are per-project |
| `poetry` / `pipenv` | N/A | elm.json is the only tool |

### elm.json Structure

**Python (pyproject.toml):**
```toml
[project]
name = "myapp"
version = "0.1.0"
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
]
```

**Elm (elm.json):**
```json
{
    "type": "application",
    "source-directories": [
        "src"
    ],
    "elm-version": "0.19.1",
    "dependencies": {
        "direct": {
            "elm/core": "1.0.5",
            "elm/html": "1.0.0",
            "elm/http": "2.0.0",
            "elm/json": "1.1.3"
        },
        "indirect": {
            "elm/time": "1.0.0",
            "elm/url": "1.0.0"
        }
    },
    "test-dependencies": {
        "direct": {
            "elm-explorations/test": "1.2.2"
        },
        "indirect": {}
    }
}
```

### Common Dependency Translations

| Python Package | Elm Package | Purpose |
|----------------|-------------|---------|
| `requests` | `elm/http` | HTTP requests |
| `pydantic` | `elm/json` + custom decoders | JSON validation |
| `pytest` | `elm-explorations/test` | Testing |
| `typing` | Built-in type system | Type annotations |
| `dataclasses` | Built-in records | Data structures |
| `enum` | Built-in union types | Enumerations |
| `datetime` | `elm/time` | Date/time handling |
| `re` | `elm/regex` | Regular expressions |
| `asyncio` | `elm/core` (Cmd/Sub) | Async operations |

### Adding Dependencies

**Python:**
```bash
# Add to requirements.txt:
requests>=2.28.0
pydantic>=2.0.0

# Or with poetry:
poetry add requests pydantic
```

**Elm:**
```bash
# Elm installs and updates elm.json automatically:
elm install elm/http
elm install elm/json

# Always uses exact versions (no semver ranges in direct deps)
```

### Build Process

**Python:**
```bash
# No build step (interpreted)
python main.py

# Or package:
python -m build
pip install dist/myapp-0.1.0-py3-none-any.whl
```

**Elm:**
```bash
# Compile to JavaScript:
elm make src/Main.elm --output=main.js

# Compile optimized:
elm make src/Main.elm --optimize --output=main.js

# Development server:
elm reactor  # Opens http://localhost:8000
```

### Project Structure

**Python:**
```
myproject/
  myproject/
    __init__.py
    main.py
    models.py
    api.py
  tests/
    __init__.py
    test_main.py
  pyproject.toml
  README.md
```

**Elm:**
```
myproject/
  src/
    Main.elm
    Types.elm
    Api.elm
  tests/
    MainTest.elm
  elm.json
  README.md
```

---

## Pillar 8: Testing Translation

### pytest → elm-test

**Python (pytest):**
```python
import pytest
from myapp import add, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_divide():
    assert divide(10, 2) == 5

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

**Elm (elm-test):**
```elm
module MainTest exposing (..)

import Expect
import Test exposing (..)
import Main exposing (add, divide)

suite : Test
suite =
    describe "Math functions"
        [ describe "add"
            [ test "adds two positive numbers" <|
                \_ ->
                    add 2 3
                        |> Expect.equal 5

            , test "adds negative and positive" <|
                \_ ->
                    add -1 1
                        |> Expect.equal 0
            ]

        , describe "divide"
            [ test "divides two numbers" <|
                \_ ->
                    divide 10 2
                        |> Expect.equal (Ok 5)

            , test "returns error on division by zero" <|
                \_ ->
                    divide 10 0
                        |> Expect.err  -- Expects Result to be Err
            ]
        ]

-- Parametrized tests (manually):
addTests : Test
addTests =
    describe "add (parametrized)"
        (List.map
            (\( a, b, expected ) ->
                test ("add " ++ String.fromInt a ++ " " ++ String.fromInt b) <|
                    \_ ->
                        add a b
                            |> Expect.equal expected
            )
            [ ( 2, 3, 5 )
            , ( 0, 0, 0 )
            , ( -1, 1, 0 )
            ]
        )
```

### Fuzz Testing (Property-Based)

**Python (Hypothesis):**
```python
from hypothesis import given
from hypothesis.strategies import integers

@given(integers(), integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)

@given(integers())
def test_add_identity(a):
    assert add(a, 0) == a
```

**Elm (elm-test fuzz):**
```elm
import Fuzz exposing (int)
import Test exposing (..)

suite : Test
suite =
    describe "add properties"
        [ fuzz2 int int "add is commutative" <|
            \a b ->
                add a b
                    |> Expect.equal (add b a)

        , fuzz int "add has identity element (0)" <|
            \a ->
                add a 0
                    |> Expect.equal a
        ]
```

### Mocking/Fixtures

**Python:**
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def user():
    return {"id": 1, "name": "Alice"}

def test_get_user_name(user):
    assert user['name'] == "Alice"

@patch('myapp.api.fetch_user')
def test_fetch_user_name(mock_fetch):
    mock_fetch.return_value = {"id": 1, "name": "Alice"}
    result = fetch_user_name(1)
    assert result == "Alice"
```

**Elm (no mocking - use test data):**
```elm
-- Elm has no mocking - use dependency injection and test data

-- Instead of mocking, pass functions as arguments:
getUserName : (Int -> Maybe User) -> Int -> String
getUserName getUser userId =
    case getUser userId of
        Just user ->
            user.name

        Nothing ->
            "Unknown"

-- Test with fake function:
testGetUserName : Test
testGetUserName =
    test "returns user name if found" <|
        \_ ->
            let
                fakeGetUser id =
                    if id == 1 then
                        Just { id = 1, name = "Alice" }
                    else
                        Nothing
            in
            getUserName fakeGetUser 1
                |> Expect.equal "Alice"
```

### Running Tests

**Python:**
```bash
# Run all tests:
pytest

# Run specific test:
pytest tests/test_main.py::test_add

# Run with coverage:
pytest --cov=myapp
```

**Elm:**
```bash
# Run all tests:
elm-test

# Run specific file:
elm-test tests/MainTest.elm

# Watch mode:
elm-test --watch
```

---

## Pillar 9: Dev Workflow & REPL Translation

### Python REPL → elm repl

**Python REPL:**
```python
$ python
>>> import math
>>> math.sqrt(16)
4.0
>>> [x**2 for x in range(5)]
[0, 1, 4, 9, 16]
>>> def greet(name):
...     return f"Hello, {name}!"
...
>>> greet("Alice")
'Hello, Alice!'
>>>
```

**Elm REPL:**
```elm
$ elm repl
> import String
> String.toUpper "hello"
"HELLO" : String
> List.map (\x -> x * x) (List.range 0 4)
[0,1,4,9,16] : List Int
> greet name = "Hello, " ++ name ++ "!"
<function> : String -> String
> greet "Alice"
"Hello, Alice!" : String
>
```

**Key Differences:**

| Feature | Python REPL | Elm REPL |
|---------|-------------|----------|
| Multi-line input | Yes | Limited |
| Import side effects | Yes | No (pure) |
| Modify definitions | Yes | Yes (but must redefine) |
| Type inference | Runtime | Compile-time (shown) |
| Persistence | Can save to file | REPL-only |

### Development Workflow

**Python (typical workflow):**
```bash
# 1. Edit code in editor
vim myapp.py

# 2. Run directly (no compilation)
python myapp.py

# 3. Interactive debugging
python -m pdb myapp.py

# 4. Tests
pytest

# 5. Iterate
```

**Elm (typical workflow):**
```bash
# 1. Edit code in editor
vim src/Main.elm

# 2. Compile (catches errors immediately)
elm make src/Main.elm

# 3. Run in browser
elm reactor  # OR serve the compiled main.js

# 4. Tests
elm-test

# 5. Iterate with fast feedback
```

### Hot Reload / Live Coding

**Python (Flask example):**
```python
# Flask auto-reloads on file change
from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)  # Auto-reload enabled
```

**Elm (elm-watch):**
```bash
# elm-watch for hot reload during development
npm install --save-dev elm-watch

# Add to package.json:
{
  "scripts": {
    "dev": "elm-watch hot"
  }
}

# elm-watch.json:
{
  "targets": {
    "Main": {
      "inputs": ["src/Main.elm"],
      "output": "build/main.js"
    }
  }
}

# Run:
npm run dev
# Auto-reloads browser on file change
```

### Debugging

**Python:**
```python
# Print debugging:
print(f"User: {user}")

# Debugger:
import pdb; pdb.set_trace()

# Logging:
import logging
logging.debug(f"User: {user}")
```

**Elm:**
```elm
-- Debug.log (removed in production builds):
update msg model =
    let
        _ = Debug.log "msg" msg
        _ = Debug.log "model" model
    in
    case msg of
        ...

-- Debug.todo (compile-time placeholder):
viewUser : User -> Html msg
viewUser user =
    Debug.todo "Implement viewUser"

-- Elm debugger (time-travel):
-- Automatically available in elm reactor
-- Shows all Msgs and Model states
```

### Editor Integration

**Python:**
- Linters: `pylint`, `flake8`, `ruff`
- Formatters: `black`, `autopep8`
- Type checking: `mypy`, `pyright`
- LSP: `python-lsp-server`, `pyright`

**Elm:**
- Formatter: `elm-format` (official, enforced)
- Linter: `elm-review` (extensible)
- LSP: `elm-language-server`
- All editors have Elm plugins (VSCode, Vim, Emacs, IntelliJ)

---

## Pillar 10: FFI/Interoperability Translation

**Critical Note:** Elm has NO C FFI like Python. Elm only has **Ports** for JavaScript interop.

### Python C Extensions → Elm Ports (JavaScript)

**Python (C extension via ctypes):**
```python
import ctypes

# Load shared library:
libc = ctypes.CDLL("libc.so.6")

# Call C function:
result = libc.printf(b"Hello from C!\n")
```

**Elm (ports to JavaScript):**
```elm
-- Elm can only call JavaScript, not C directly
port module Main exposing (..)

-- Port to send data to JavaScript:
port callNativeFunction : String -> Cmd msg

-- Port to receive data from JavaScript:
port receiveResult : (Int -> msg) -> Sub msg

type Msg
    = CallNative
    | GotResult Int

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        CallNative ->
            ( model, callNativeFunction "Hello from Elm!" )

        GotResult result ->
            ( { model | result = result }, Cmd.none )

subscriptions : Model -> Sub Msg
subscriptions model =
    receiveResult GotResult
```

```javascript
// JavaScript side:
const app = Elm.Main.init({ node: document.getElementById('elm') });

app.ports.callNativeFunction.subscribe((message) => {
    console.log(message);  // "Hello from Elm!"

    // Call some JavaScript/native code:
    const result = someNativeFunction(message);

    // Send result back to Elm:
    app.ports.receiveResult.send(result);
});
```

### Python → JavaScript Interop Patterns

**Python (with PyScript or similar):**
```python
# In browser with PyScript
from js import console, fetch

console.log("Hello from Python in browser!")

response = await fetch("https://api.example.com/users")
data = await response.json()
print(data)
```

**Elm (built for browser):**
```elm
-- No need for special interop - Elm compiles to JavaScript
-- For things Elm doesn't support, use ports:

port module Main exposing (..)

-- Send to JavaScript:
port logToConsole : String -> Cmd msg

-- Receive from JavaScript:
port receiveFetchResult : (String -> msg) -> Sub msg

type Msg
    = FetchData
    | GotData String

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchData ->
            ( model, logToConsole "Fetching data..." )

        GotData data ->
            ( { model | data = data }, Cmd.none )

subscriptions : Model -> Sub Msg
subscriptions model =
    receiveFetchResult GotData
```

```javascript
// JavaScript side:
const app = Elm.Main.init({ node: document.getElementById('elm') });

app.ports.logToConsole.subscribe((message) => {
    console.log(message);
});

// Fetch data and send to Elm:
fetch('https://api.example.com/users')
    .then(res => res.json())
    .then(data => {
        app.ports.receiveFetchResult.send(JSON.stringify(data));
    });
```

### File I/O (Impossible in Elm)

**Python:**
```python
# Read file:
with open('data.txt', 'r') as f:
    data = f.read()

# Write file:
with open('output.txt', 'w') as f:
    f.write("Hello, file!")
```

**Elm (no file I/O - use ports):**
```elm
-- Elm CANNOT access filesystem directly
-- Use ports to JavaScript, which calls Node.js or browser File API

port module Main exposing (..)

-- Request file read:
port requestFileRead : String -> Cmd msg

-- Receive file contents:
port receiveFileContents : (String -> msg) -> Sub msg

type Msg
    = ReadFile String
    | GotFileContents String

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ReadFile filename ->
            ( model, requestFileRead filename )

        GotFileContents contents ->
            ( { model | fileContents = contents }, Cmd.none )

subscriptions : Model -> Sub Msg
subscriptions model =
    receiveFileContents GotFileContents
```

```javascript
// JavaScript (Node.js):
const fs = require('fs');
const app = Elm.Main.init();

app.ports.requestFileRead.subscribe((filename) => {
    fs.readFile(filename, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
        } else {
            app.ports.receiveFileContents.send(data);
        }
    });
});
```

### Database Access (Use Ports)

**Python:**
```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM users WHERE id = ?', (1,))
user = cursor.fetchone()
```

**Elm (via ports to backend):**
```elm
-- Elm frontend cannot access database directly
-- Send HTTP request to backend:

type Msg
    = FetchUser Int
    | GotUser (Result Http.Error User)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser userId ->
            ( model
            , Http.get
                { url = "/api/users/" ++ String.fromInt userId
                , expect = Http.expectJson GotUser userDecoder
                }
            )

        GotUser (Ok user) ->
            ( { model | user = Just user }, Cmd.none )

        GotUser (Err error) ->
            ( { model | error = Just error }, Cmd.none )

-- Backend (Python/Node/etc.) handles database access
```

### FFI Checklist

When converting Python FFI/interop to Elm:

- [ ] Identify all C extensions or native code usage
- [ ] Determine if functionality can be replaced with Elm packages
- [ ] For required native code, create JavaScript wrapper
- [ ] Define Elm ports for communication with JavaScript
- [ ] Write JavaScript glue code to call native functionality
- [ ] Handle errors gracefully (ports don't guarantee type safety)
- [ ] Document port contracts clearly
- [ ] Consider moving backend logic to actual backend (not frontend)

---

## Idiom Translation Patterns

### Pattern 1: List Comprehension → List Functions

**Python:**
```python
# List comprehension with filter and map
squared_evens = [x * x for x in numbers if x % 2 == 0]

# Nested comprehension
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
```

**Elm:**
```elm
-- Pipe operator + List functions
squaredEvens =
    numbers
        |> List.filter (\x -> modBy 2 x == 0)
        |> List.map (\x -> x * x)

-- Nested List.concatMap
pairs =
    List.range 0 2
        |> List.concatMap (\x ->
            List.range 0 2
                |> List.filter (\y -> x /= y)
                |> List.map (\y -> ( x, y ))
           )
```

### Pattern 2: Dictionary Operations

**Python:**
```python
# Get with default
value = my_dict.get('key', 'default')

# Update
my_dict['key'] = 'new_value'

# Merge
merged = {**dict1, **dict2}

# Filter
filtered = {k: v for k, v in my_dict.items() if v > 10}
```

**Elm:**
```elm
-- Get with default
value =
    Dict.get "key" myDict
        |> Maybe.withDefault "default"

-- Update (returns new dict)
newDict =
    Dict.insert "key" "new_value" myDict

-- Merge (union favors first dict)
merged =
    Dict.union dict1 dict2

-- Filter
filtered =
    Dict.filter (\k v -> v > 10) myDict
```

### Pattern 3: String Formatting

**Python:**
```python
# f-strings
message = f"Hello, {name}! You are {age} years old."

# format method
message = "Hello, {}! You are {} years old.".format(name, age)

# % formatting
message = "Hello, %s! You are %d years old." % (name, age)
```

**Elm:**
```elm
-- String concatenation (no interpolation)
message =
    "Hello, " ++ name ++ "! You are " ++ String.fromInt age ++ " years old."

-- Or helper function for clarity
formatMessage : String -> Int -> String
formatMessage name age =
    "Hello, " ++ name ++ "! You are " ++ String.fromInt age ++ " years old."

message = formatMessage name age
```

### Pattern 4: Unpacking / Destructuring

**Python:**
```python
# Tuple unpacking
x, y = (1, 2)

# List unpacking
first, *rest = [1, 2, 3, 4]

# Dict unpacking
{name, email} = user  # Not standard, but shown for concept
```

**Elm:**
```elm
-- Tuple destructuring
(x, y) = (1, 2)

-- List pattern matching (in case expression)
case myList of
    first :: rest ->
        -- first is head, rest is tail
        ...

    [] ->
        -- empty list
        ...

-- Record destructuring
{ name, email } = user
-- Or in function parameter:
viewUser { name, email } =
    div [] [ text name, text email ]
```

### Pattern 5: Iteration

**Python:**
```python
# For loop with side effects
for user in users:
    print(user.name)
    send_email(user.email)

# Enumerate
for i, user in enumerate(users):
    print(f"{i}: {user.name}")

# While loop
i = 0
while i < 10:
    print(i)
    i += 1
```

**Elm:**
```elm
-- No for loops (pure functions)
-- Use List.map for transformation:
viewUsers : List User -> List (Html msg)
viewUsers users =
    List.map (\user -> div [] [ text user.name ]) users

-- Use List.indexedMap for index:
viewUsersIndexed : List User -> List (Html msg)
viewUsersIndexed users =
    List.indexedMap
        (\i user -> div [] [ text (String.fromInt i ++ ": " ++ user.name) ])
        users

-- No while loops
-- Use recursion:
count : Int -> List Int
count n =
    if n <= 0 then
        []
    else
        n :: count (n - 1)

-- count 5 = [5, 4, 3, 2, 1]
```

### Pattern 6: Classes → Records + Functions

**Python:**
```python
class Counter:
    def __init__(self, initial=0):
        self.value = initial

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def reset(self):
        self.value = 0

counter = Counter(10)
counter.increment()
counter.increment()
print(counter.value)  # 12
```

**Elm:**
```elm
-- Separate data from behavior
type alias Counter =
    { value : Int
    }

init : Int -> Counter
init initial =
    { value = initial }

increment : Counter -> Counter
increment counter =
    { counter | value = counter.value + 1 }

decrement : Counter -> Counter
decrement counter =
    { counter | value = counter.value - 1 }

reset : Counter -> Counter
reset counter =
    { counter | value = 0 }

-- Usage (immutable):
counter = init 10
newCounter =
    counter
        |> increment
        |> increment
-- newCounter.value == 12
-- counter.value == 10 (unchanged!)
```

### Pattern 7: Context Managers → Explicit Resource Handling

**Python:**
```python
# Context manager for file I/O
with open('file.txt', 'r') as f:
    data = f.read()
# File automatically closed

# Custom context manager
class Transaction:
    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

with Transaction() as txn:
    txn.execute("INSERT INTO ...")
```

**Elm:**
```elm
-- Elm has no context managers or automatic cleanup
-- Resource management happens in JavaScript (via ports)

port module Main exposing (..)

port openFile : String -> Cmd msg
port readFile : (String -> msg) -> Sub msg
port closeFile : () -> Cmd msg

type Msg
    = OpenFile String
    | FileOpened String
    | CloseFile

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        OpenFile filename ->
            ( model, openFile filename )

        FileOpened contents ->
            -- Process contents
            ( { model | contents = contents }, closeFile () )

        CloseFile ->
            ( model, Cmd.none )

-- Cleanup must be explicit in JavaScript
```

### Pattern 8: Generators → Lazy Lists (Streams)

**Python:**
```python
# Generator function
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Usage:
fib = fibonacci()
print(next(fib))  # 0
print(next(fib))  # 1
print(next(fib))  # 1

# Or with itertools:
from itertools import islice
first_10 = list(islice(fibonacci(), 10))
```

**Elm:**
```elm
-- Elm has no generators
-- Use explicit recursion or elm-community/list-extra for infinite lists

-- Recursive approach (limited by stack):
fibonacci : Int -> List Int
fibonacci n =
    fibHelper n 0 1 []

fibHelper : Int -> Int -> Int -> List Int -> List Int
fibHelper n a b acc =
    if n <= 0 then
        List.reverse acc
    else
        fibHelper (n - 1) b (a + b) (a :: acc)

-- fibonacci 10 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

-- For truly lazy evaluation, use elm-community/lazy-list (third-party)
```

---

## Common Pitfalls

### Pitfall 1: Trying to Mutate State

**Wrong (Python thinking):**
```elm
-- This does NOT work - Elm has no mutation
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            model.count = model.count + 1  -- COMPILE ERROR!
            ( model, Cmd.none )
```

**Correct (Elm way):**
```elm
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )
```

### Pitfall 2: Expecting Dynamic Types

**Wrong:**
```elm
-- Trying to store different types in a list
myList = [ 1, "two", 3.0 ]  -- COMPILE ERROR!
```

**Correct:**
```elm
-- Use discriminated union for heterogeneous data
type Value
    = IntValue Int
    | StringValue String
    | FloatValue Float

myList : List Value
myList =
    [ IntValue 1
    , StringValue "two"
    , FloatValue 3.0
    ]
```

### Pitfall 3: Trying to Use Exceptions

**Wrong:**
```elm
-- No exceptions in Elm
divide : Int -> Int -> Int
divide a b =
    if b == 0 then
        throw "Division by zero"  -- NO throw in Elm!
    else
        a // b
```

**Correct:**
```elm
-- Use Result type
divide : Int -> Int -> Result String Int
divide a b =
    if b == 0 then
        Err "Division by zero"
    else
        Ok (a // b)
```

### Pitfall 4: Forgetting to Handle All Cases

**Wrong:**
```elm
-- Non-exhaustive pattern match
case maybeUser of
    Just user ->
        text user.name
    -- Missing Nothing case - COMPILE ERROR!
```

**Correct:**
```elm
-- Exhaustive pattern matching
case maybeUser of
    Just user ->
        text user.name

    Nothing ->
        text "No user"
```

### Pitfall 5: Trying to Do Side Effects Anywhere

**Wrong:**
```elm
-- Trying to do HTTP in view function
view : Model -> Html Msg
view model =
    let
        user = Http.get { ... }  -- Can't do this!
    in
    div [] [ text "Hello" ]
```

**Correct:**
```elm
-- Side effects only through update function
type Msg
    = FetchUser
    | GotUser (Result Http.Error User)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser ->
            ( model
            , Http.get
                { url = "/user"
                , expect = Http.expectJson GotUser userDecoder
                }
            )

        GotUser (Ok user) ->
            ( { model | user = Just user }, Cmd.none )

        GotUser (Err _) ->
            ( model, Cmd.none )
```

---

## Complete Example: Python → Elm

### Python (Flask + Pydantic)

```python
from flask import Flask, jsonify, request
from pydantic import BaseModel
from typing import Optional
import requests

app = Flask(__name__)

class User(BaseModel):
    id: int
    name: str
    email: str

users_cache: dict[int, User] = {}

@app.route('/users/<int:user_id>')
def get_user(user_id: int):
    if user_id in users_cache:
        return jsonify(users_cache[user_id].dict())

    try:
        response = requests.get(f'https://api.example.com/users/{user_id}')
        response.raise_for_status()
        user_data = response.json()
        user = User(**user_data)
        users_cache[user_id] = user
        return jsonify(user.dict())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### Elm (Frontend Application)

```elm
module Main exposing (main)

import Browser
import Html exposing (..)
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Decode exposing (Decoder)
import Json.Decode.Pipeline exposing (required)
import Dict exposing (Dict)

-- MODEL

type alias User =
    { id : Int
    , name : String
    , email : String
    }

type alias Model =
    { userId : String
    , usersCache : Dict Int User
    , status : Status
    }

type Status
    = Idle
    | Loading
    | Success User
    | Failure String

init : () -> ( Model, Cmd Msg )
init _ =
    ( { userId = ""
      , usersCache = Dict.empty
      , status = Idle
      }
    , Cmd.none
    )

-- UPDATE

type Msg
    = InputUserId String
    | FetchUser
    | GotUser Int (Result Http.Error User)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        InputUserId userId ->
            ( { model | userId = userId }, Cmd.none )

        FetchUser ->
            case String.toInt model.userId of
                Just userId ->
                    case Dict.get userId model.usersCache of
                        Just user ->
                            -- Found in cache
                            ( { model | status = Success user }, Cmd.none )

                        Nothing ->
                            -- Fetch from API
                            ( { model | status = Loading }
                            , Http.get
                                { url = "https://api.example.com/users/" ++ String.fromInt userId
                                , expect = Http.expectJson (GotUser userId) userDecoder
                                }
                            )

                Nothing ->
                    ( { model | status = Failure "Invalid user ID" }, Cmd.none )

        GotUser userId (Ok user) ->
            ( { model
                | status = Success user
                , usersCache = Dict.insert userId user model.usersCache
              }
            , Cmd.none
            )

        GotUser _ (Err error) ->
            ( { model | status = Failure (httpErrorToString error) }
            , Cmd.none
            )

-- DECODER

userDecoder : Decoder User
userDecoder =
    Decode.succeed User
        |> required "id" Decode.int
        |> required "name" Decode.string
        |> required "email" Decode.string

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ h1 [] [ text "User Lookup" ]
        , input [ onInput InputUserId ] []
        , button [ onClick FetchUser ] [ text "Fetch User" ]
        , viewStatus model.status
        ]

viewStatus : Status -> Html Msg
viewStatus status =
    case status of
        Idle ->
            text ""

        Loading ->
            text "Loading..."

        Success user ->
            div []
                [ h2 [] [ text user.name ]
                , p [] [ text ("Email: " ++ user.email) ]
                ]

        Failure error ->
            div [] [ text ("Error: " ++ error) ]

-- HELPERS

httpErrorToString : Http.Error -> String
httpErrorToString error =
    case error of
        Http.BadUrl url ->
            "Bad URL: " ++ url

        Http.Timeout ->
            "Request timeout"

        Http.NetworkError ->
            "Network error"

        Http.BadStatus statusCode ->
            "Bad status: " ++ String.fromInt statusCode

        Http.BadBody body ->
            "Bad body: " ++ body

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

## Tooling Reference

### Code Quality Tools

| Purpose | Python | Elm |
|---------|--------|-----|
| Formatter | `black`, `autopep8` | `elm-format` (official) |
| Linter | `pylint`, `flake8`, `ruff` | `elm-review` |
| Type Checker | `mypy`, `pyright` | Built-in compiler |
| LSP | `python-lsp-server` | `elm-language-server` |
| Test Runner | `pytest` | `elm-test` |
| Coverage | `coverage.py` | N/A (compiler ensures coverage) |

### Build Tools

| Purpose | Python | Elm |
|---------|--------|-----|
| Package Manager | `pip`, `poetry`, `pipenv` | `elm install` |
| Task Runner | `make`, `invoke`, `just` | `just`, npm scripts |
| Dev Server | `flask run`, `uvicorn` | `elm reactor`, `elm-watch` |
| Bundler | N/A (or webpack for frontend) | `elm make` |
| Minifier | N/A | `elm make --optimize` + terser |

### Editor Setup (VS Code Example)

**Python:**
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.languageServer": "Pylance"
}
```

**Elm:**
```json
{
  "elm.formatOnSave": true,
  "elm.compiler": "elm",
  "elm.makeCommand": "elm make"
}
```

---

## Conversion Checklist

Use this checklist when converting Python code to Elm:

### Pre-Conversion

- [ ] Understand the Python code thoroughly
- [ ] Identify all side effects (I/O, state mutations, exceptions)
- [ ] Map Python types to Elm types
- [ ] Identify which parts belong in frontend vs backend
- [ ] Plan The Elm Architecture (Model, Msg, update, view)

### Type System

- [ ] Convert classes to records or union types
- [ ] Replace `None` with `Maybe`
- [ ] Replace exceptions with `Result`
- [ ] Map Python dicts to Elm `Dict` (check key comparability)
- [ ] Convert dynamic types to static discriminated unions

### Error Handling

- [ ] Replace all `try/except` with `Result` or `Maybe`
- [ ] Map exception types to custom error types
- [ ] Use pattern matching for exhaustive error handling
- [ ] Remove all `raise` statements (use `Err` instead)

### Concurrency

- [ ] Remove all `async/await` code
- [ ] Model async operations as Msg variants
- [ ] Use `Cmd` for one-off effects
- [ ] Use `Sub` for continuous effects
- [ ] Remove all threading code

### JSON Handling

- [ ] Write decoders for all JSON input
- [ ] Write encoders for all JSON output
- [ ] Test decoders with sample JSON
- [ ] Handle decode errors with `Result`

### Architecture

- [ ] Define Model type
- [ ] Define Msg type (one variant per action)
- [ ] Write `init` function
- [ ] Write `update` function
- [ ] Write `view` function
- [ ] Wire up with `Browser.element` or `Browser.application`

### Testing

- [ ] Convert pytest tests to elm-test
- [ ] Add fuzz tests for property-based testing
- [ ] Test pure functions independently
- [ ] Test update function with different Msg variants

### Post-Conversion

- [ ] Run `elm-format` on all files
- [ ] Run `elm-review` for best practices
- [ ] Verify no runtime exceptions possible
- [ ] Document any Python features with no Elm equivalent
- [ ] Performance test if critical

---

## References

### This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

### Related Conversion Skills

- `convert-python-rust` - Python → Rust (backend focus)
- `convert-python-fsharp` - Python → F# (functional .NET)
- `convert-fsharp-elm` - F# → Elm (similar paradigms)
- `convert-typescript-elm` - TypeScript → Elm (frontend focus)

### Language Skills

- `lang-python-dev` - Python development patterns
- `lang-elm-dev` - Elm development patterns
- `lang-elm-library-dev` - Elm library development

### External Resources

- [Elm Guide](https://guide.elm-lang.org/) - Official Elm guide
- [Elm Packages](https://package.elm-lang.org/) - Package registry
- [Elm JSON](https://package.elm-lang.org/packages/elm/json/latest/) - JSON encoding/decoding
- [elm-test](https://package.elm-lang.org/packages/elm-explorations/test/latest/) - Testing framework
- [elm-review](https://package.elm-lang.org/packages/jfmengels/elm-review/latest/) - Linter
- [The Elm Architecture](https://guide.elm-lang.org/architecture/) - Core architecture pattern
- [Elm Discourse](https://discourse.elm-lang.org/) - Community forum
- [Elm Slack](https://elmlang.herokuapp.com/) - Community chat

---

## Summary

Converting Python to Elm represents a fundamental paradigm shift:

- **Dynamic → Static**: All types known at compile time
- **Mutable → Immutable**: No mutation, only transformations
- **Exceptions → Types**: Errors are values, not exceptions
- **Imperative → Functional**: Pure functions, explicit effects
- **OOP → TEA**: The Elm Architecture replaces classes
- **Backend → Frontend**: Elm is browser-focused

**Key Takeaways:**

1. **Compiler as Guide**: Let the Elm compiler guide you - if it compiles, it works
2. **Make Impossible States Impossible**: Model your domain to prevent invalid states
3. **Explicit is Better**: No hidden side effects, no implicit nulls
4. **Embrace The Elm Architecture**: Model-Update-View pattern is core to Elm
5. **JSON is Explicit**: Write decoders and encoders for all data
6. **No Runtime Exceptions**: Elm's type system prevents runtime errors
7. **JavaScript Interop via Ports**: Use ports for things Elm can't do natively

**When to Convert Python → Elm:**

- Building type-safe frontend applications
- Need guaranteed no runtime exceptions
- Want excellent compile-time error messages
- Prefer functional programming
- Building interactive UIs with complex state

**When NOT to Convert:**

- Backend services (Elm is frontend-only)
- CLI tools (Elm targets browser)
- Need dynamic metaprogramming
- Heavy numerical/scientific computing
- Existing Python ecosystem is critical
