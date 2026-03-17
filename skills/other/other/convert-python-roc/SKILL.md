---
name: convert-python-roc
description: Convert Python code to idiomatic Roc. Use when migrating Python projects to Roc, translating Python patterns to idiomatic Roc, or refactoring Python codebases for type safety, functional purity, and native performance. Extends meta-convert-dev with Python-to-Roc specific patterns.
---

# Convert Python to Roc

Convert Python code to idiomatic Roc. This skill extends `meta-convert-dev` with Python-to-Roc specific type mappings, idiom translations, and architectural guidance for transforming dynamic, garbage-collected Python code into statically-typed, pure functional Roc with platform-separated effects.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Python types → Roc types (dynamic → static with inference)
- **Idiom translations**: Python patterns → idiomatic Roc
- **Error handling**: Exceptions → Result types
- **Platform architecture**: Python runtime → Roc platform/application model
- **Async patterns**: asyncio → Task-based effects
- **Class hierarchy**: OOP → records + functions
- **Dev workflow**: REPL-driven → expect-driven development

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Python language fundamentals - see `lang-python-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → Python) - not recommended

---

## Quick Reference

| Python | Roc | Notes |
|--------|-----|-------|
| `int` | `I64` or `U64` | Roc uses fixed-size integers; Python has arbitrary precision |
| `float` | `F64` | 64-bit floating point |
| `bool` | `Bool` | Direct mapping |
| `str` | `Str` | UTF-8 strings |
| `bytes` | `List U8` | Byte arrays become lists |
| `list[T]` | `List a` | Immutable lists |
| `tuple` | `(a, b)` or record | Tuples or named records |
| `dict[K, V]` | `Dict k v` | Immutable dictionaries |
| `set[T]` | `Set a` | Immutable sets |
| `None` | `[Some a, None]` | Use tag unions for optional |
| `Union[T, U]` | `[A a, B b]` tag union | Tagged unions |
| `Optional[T]` | `[Some a, None]` | Optional values |
| `Callable[[Args], Ret]` | `args -> ret` | Functions |
| `class` | `record + module` | Data + behavior separated |
| `async def` | `Task a err` | Platform-provided effects |
| `@dataclass` | `{ ... }` record | Structural records |
| `Exception` | `Result a err` | No exceptions in Roc |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - Python's dynamic types need explicit Roc types
3. **Separate pure from effectful** - Roc strictly enforces purity
4. **Embrace immutability** - no `mutable` keyword in Roc
5. **Adopt Roc idioms** - don't write "Python code in Roc syntax"
6. **Think in pattern matching** - replace if/elif chains
7. **Let types guide** - use Roc's type inference
8. **Test equivalence** - same inputs → same outputs
9. **Consider platform model** - effects go through platform boundary

---

## Paradigm Translation

### Mental Model Shift: Python Runtime → Roc Platform Model

The biggest conceptual shift is how effects (I/O, async, state) are handled:

| Python Concept | Roc Approach | Key Insight |
|----------------|--------------|-------------|
| Python runtime with GC | Platform provides runtime | Runtime external to application |
| Direct I/O anywhere | Platform-provided Task | Application stays pure |
| `async/await` | `Task ok err` via platform | Effects delegated to platform |
| Mutable by default | Immutable by default | No mutation operators |
| Duck typing | Static structural typing | Compiler infers types |
| Dynamic introspection | Compile-time types only | No runtime type inspection |
| Exception handling | Result type only | No runtime exceptions |
| Classes with state | Records + module functions | Data and behavior separated |

### Architecture Mental Model

```
Python                             Roc (Platform Model)
┌─────────────────────┐           ┌─────────────────────┐
│   Your Python Code  │           │   Your Roc Code     │
│   (can do I/O)      │           │   (pure only)       │
│   ↓                 │           │   ↓                 │
│   Python stdlib     │           │   Platform API      │
│   ↓                 │           │   ↓                 │
│   CPython runtime   │           │   Platform Host     │
└─────────────────────┘           └─────────────────────┘
     Everything in                    Clear separation
     same runtime                     between pure & effects
```

**Key shift:** In Python, you can call `print()` anywhere. In Roc, all I/O goes through the platform's `Task` type. This enforces functional purity in your application code.

---

## Type System Mapping

### Primitive Types

| Python | Roc | Notes |
|--------|-----|-------|
| `int` | `I64` | Python has arbitrary precision; Roc uses 64-bit signed |
| `int` | `U64` | For positive-only values |
| `int` | `I32`, `I16`, `I8` | Smaller sizes for memory efficiency |
| `int` | `U32`, `U16`, `U8` | Unsigned variants |
| `float` | `F64` | Default 64-bit floating point |
| `float` | `F32` | 32-bit for memory efficiency |
| `bool` | `Bool` | Direct mapping |
| `str` | `Str` | UTF-8 strings (both immutable) |
| `bytes` | `List U8` | Byte arrays as lists |
| `None` | Tag in union | Use `[Some a, None]` pattern |

**Critical differences:**
- Python `int` has arbitrary precision; Roc integers have fixed sizes (choose appropriately)
- Python strings are unicode; Roc strings are UTF-8 (compatible but mind encoding)
- Python `None` is a singleton; Roc uses tag unions for optional values

### Collection Types

| Python | Roc | Notes |
|--------|-----|-------|
| `list[T]` | `List a` | Both are ordered; Roc is immutable |
| `tuple[T, U]` | `(a, b)` | Fixed-size tuples map directly |
| `dict[K, V]` | `Dict k v` | Immutable dictionaries |
| `set[T]` | `Set a` | Immutable sets |
| `frozenset[T]` | `Set a` | All Roc collections are immutable |
| `collections.deque` | `List a` | Use list; platform-specific for performance |
| `collections.Counter` | `Dict a U64` | Map to counts |
| `collections.defaultdict` | `Dict.get(key, default)` | Use default parameter |

**Key insight:** All Roc collections are immutable by default. Operations return new collections.

### Composite Types

| Python | Roc | Notes |
|--------|-----|-------|
| `@dataclass` | `{ ... }` record | Structural records |
| `class` (data) | `{ ... }` record | Data-only classes |
| `class` (behavior) | `record + module` | Separate data and functions |
| `TypedDict` | `{ ... }` record | Named fields |
| `NamedTuple` | `{ ... }` record | Named record preferred |
| `enum.Enum` | `[A, B, C]` tag union | Discriminated unions |
| `Union[T, U]` | `[A a, B b]` tag | Tagged unions |
| `Optional[T]` | `[Some a, None]` | Optional pattern |
| `Literal["a", "b"]` | `[A, B]` tag union | Enumerated values |
| `Callable[[Args], Ret]` | `args -> ret` | Function types |

### Type Annotations → Type Signatures

| Python | Roc | Notes |
|--------|-----|-------|
| `def f(x: int) -> int` | `f : I64 -> I64` | Function type signature |
| `def f(x: T) -> T` | `f : a -> a` | Generic type variable |
| `x: Any` | `a` (generic) | Use generics instead of Any |
| `x: list[int]` | `List I64` | List of integers |
| `x: Optional[int]` | `[Some I64, None]` | Optional via tag union |
| `x: Union[int, str]` | `[Int I64, Str Str]` | Discriminated union |

---

## Idiom Translation

### Pattern 1: None/Optional Handling

**Python:**
```python
def find_user(user_id: int) -> Optional[dict]:
    for user in users:
        if user["id"] == user_id:
            return user
    return None

# Usage with walrus operator
if user := find_user(1):
    name = user["name"]
else:
    name = "Unknown"

# Or with ternary
name = user["name"] if user else "Unknown"
```

**Roc:**
```roc
findUser : I64 -> [Some User, None]
findUser = \userId ->
    when List.findFirst(users, \u -> u.id == userId) is
        Ok(user) -> Some(user)
        Err(_) -> None

# Usage with pattern matching
name = when findUser(1) is
    Some(user) -> user.name
    None -> "Unknown"
```

**Why this translation:**
- Python uses `None` and truthy checks; Roc uses tag unions `[Some a, None]`
- Python allows property access on potentially-None values (runtime error); Roc requires pattern matching (compile-time safety)
- Roc's exhaustive pattern matching prevents forgetting the None case

### Pattern 2: Result for Error Handling

**Python:**
```python
def divide(x: int, y: int) -> int:
    if y == 0:
        raise ValueError("Division by zero")
    return x // y

# Exception handling
try:
    result = divide(10, 2)
    print(f"Result: {result}")
except ValueError as e:
    print(f"Error: {e}")
```

**Roc:**
```roc
divide : I64, I64 -> Result I64 [DivByZero]
divide = \x, y ->
    if y == 0 then
        Err(DivByZero)
    else
        Ok(x // y)

# Pattern matching
when divide(10, 2) is
    Ok(result) -> Stdout.line!("Result: \(Num.toStr(result))")
    Err(DivByZero) -> Stdout.line!("Error: Division by zero")
```

**Why this translation:**
- Python uses exceptions; Roc uses Result type (compile-time error handling)
- Python `try/except` → Roc `when ... is` pattern matching
- Roc errors are typed (DivByZero tag, not string), enabling exhaustive checking

### Pattern 3: List Comprehensions

**Python:**
```python
# List comprehension
squared_evens = [x * x for x in numbers if x % 2 == 0]

# Generator expression with sum
total = sum(x * x for x in numbers if x % 2 == 0)

# Nested comprehension
matrix = [[i+j for j in range(3)] for i in range(3)]
```

**Roc:**
```roc
# List operations
squaredEvens =
    numbers
    |> List.keepIf(\x -> x % 2 == 0)
    |> List.map(\x -> x * x)

# Fold for aggregation
total =
    numbers
    |> List.keepIf(\x -> x % 2 == 0)
    |> List.map(\x -> x * x)
    |> List.walk(0, Num.add)

# Nested - use map
matrix =
    List.range({ start: At(0), end: Before(3) })
    |> List.map(\i ->
        List.range({ start: At(0), end: Before(3) })
        |> List.map(\j -> i + j)
    )
```

**Why this translation:**
- Python comprehensions are concise but limited; Roc uses explicit pipeline of operations
- Roc's `List.keepIf` (filter) + `List.map` composes clearly
- For aggregation, use `List.walk` (fold) instead of built-in `sum`
- Pipeline operator `|>` provides left-to-right data flow like comprehensions

### Pattern 4: Dictionary Operations

**Python:**
```python
# Get with default
value = config.get("timeout", 30)

# Dictionary comprehension
squared = {k: v * v for k, v in items.items()}

# Update
config["timeout"] = 60  # Mutable

# Merge dictionaries
merged = {**dict1, **dict2}
```

**Roc:**
```roc
# Get with default
value = Dict.get(config, "timeout") |> Result.withDefault(30)

# Map values (transform dictionary)
squared = Dict.map(items, \_, v -> v * v)

# Update (returns new dictionary)
newConfig = Dict.insert(config, "timeout", 60)

# Merge dictionaries
merged = Dict.insertAll(dict1, dict2)
```

**Why this translation:**
- Python dicts are mutable; Roc dicts are immutable (operations return new dicts)
- Python `dict.get(key, default)` → Roc `Dict.get` returns Result, use `withDefault`
- Dict comprehensions → `Dict.map` for value transformation
- Roc's functional style makes data flow explicit

### Pattern 5: String Formatting

**Python:**
```python
# f-strings (Python 3.6+)
message = f"User {user['name']} has {count} items"

# format method
message = "User {} has {} items".format(user['name'], count)

# % formatting
message = "User %s has %d items" % (user['name'], count)
```

**Roc:**
```roc
# String interpolation
message = "User \(user.name) has \(Num.toStr(count)) items"

# String concatenation (avoid for complex strings)
message = Str.concat([
    "User ",
    user.name,
    " has ",
    Num.toStr(count),
    " items",
])
```

**Why this translation:**
- Python f-strings auto-convert to string; Roc requires explicit `Num.toStr` for numbers
- Roc uses `\(expr)` for interpolation (similar to f-string braces)
- String concatenation is available but interpolation is cleaner

### Pattern 6: Class → Record + Module Functions

**Python:**
```python
@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True

    def deactivate(self):
        self.active = False

    def get_display_name(self) -> str:
        return f"{self.name} ({self.email})"

# Usage
user = User(id=1, name="Alice", email="alice@example.com")
user.deactivate()
display = user.get_display_name()
```

**Roc:**
```roc
# Record type
User : {
    id : I64,
    name : Str,
    email : Str,
    active : Bool,
}

# Module functions
deactivate : User -> User
deactivate = \user ->
    { user & active: Bool.false }

getDisplayName : User -> Str
getDisplayName = \user ->
    "\(user.name) (\(user.email))"

# Usage
user = { id: 1, name: "Alice", email: "alice@example.com", active: Bool.true }
deactivatedUser = deactivate(user)
display = getDisplayName(deactivatedUser)
```

**Why this translation:**
- Python classes combine data and behavior; Roc separates into records (data) and module functions (behavior)
- Python methods mutate `self`; Roc functions return new values (immutability)
- No `self` in Roc - pass the record explicitly as a parameter
- Roc's approach is more functional: data + pure functions

### Pattern 7: Async/Await → Task

**Python:**
```python
import asyncio

async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.1)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}

async def process_users(user_ids: list[int]) -> list[dict]:
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)

# Run
result = asyncio.run(process_users([1, 2, 3]))
```

**Roc:**
```roc
import pf.Task exposing [Task]
import pf.Http

fetchUser : I64 -> Task User [HttpErr]*
fetchUser = \userId ->
    # Platform handles I/O
    Http.get!("https://api.example.com/users/\(Num.toStr(userId))")

processUsers : List I64 -> Task (List User) [HttpErr]*
processUsers = \userIds ->
    # Platform may parallelize
    userIds
    |> List.map(fetchUser)
    |> Task.sequence

# main is already a Task - no explicit run
main : Task {} []
main =
    users = processUsers!([1, 2, 3])
    Stdout.line!("Processed \(Num.toStr(List.len(users))) users")
```

**Why this translation:**
- Python `async def` → Roc `Task a err` (platform-provided)
- Python `await` → Roc `!` suffix (try operator)
- Python `asyncio.gather` → Roc `Task.sequence` (platform controls parallelism)
- Python needs `asyncio.run`; Roc `main` is already a Task that platform executes
- Roc's platform model separates pure code from effectful I/O

### Pattern 8: Context Managers → Try with Cleanup

**Python:**
```python
# with statement for automatic cleanup
with open("file.txt") as f:
    content = f.read()
# File automatically closed

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")

with timer():
    # Code to time
    expensive_operation()
```

**Roc:**
```roc
# File I/O with platform Task
readFile : Str -> Task Str [FileReadErr]*
readFile = \path ->
    File.readUtf8!(Path.fromStr(path))
    # Platform handles file closing

# No direct equivalent to context managers
# Resource cleanup handled by platform
# For custom timing, use explicit start/end
processWithTiming : {} -> Task {} []
processWithTiming = \{} ->
    start = getCurrentTime!
    expensiveOperation!
    end = getCurrentTime!
    elapsed = end - start
    Stdout.line!("Elapsed: \(Num.toStr(elapsed))s")
```

**Why this translation:**
- Python context managers (`with`) → Roc platforms handle resource cleanup
- Python's `__enter__`/`__exit__` protocol → No direct equivalent; platform manages resources
- File operations return Task; platform ensures proper cleanup
- For custom resource management, structure as explicit acquisition/release in Task chains

### Pattern 9: Exception Hierarchy → Tagged Errors

**Python:**
```python
class ValidationError(Exception):
    pass

class InvalidName(ValidationError):
    pass

class InvalidAge(ValidationError):
    pass

def validate_person(name: str, age: int) -> dict:
    if not name:
        raise InvalidName("Name cannot be empty")
    if age < 0 or age > 120:
        raise InvalidAge("Age must be 0-120")
    return {"name": name, "age": age}

try:
    person = validate_person("", 30)
except InvalidName as e:
    print(f"Name error: {e}")
except InvalidAge as e:
    print(f"Age error: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
```

**Roc:**
```roc
ValidationError : [InvalidName Str, InvalidAge Str]

Person : { name : Str, age : I64 }

validatePerson : Str, I64 -> Result Person ValidationError
validatePerson = \name, age ->
    if Str.isEmpty(name) then
        Err(InvalidName("Name cannot be empty"))
    else if age < 0 || age > 120 then
        Err(InvalidAge("Age must be 0-120"))
    else
        Ok({ name, age })

# Pattern matching on errors
when validatePerson("", 30) is
    Ok(person) -> Stdout.line!("Valid: \(person.name)")
    Err(InvalidName(msg)) -> Stdout.line!("Name error: \(msg)")
    Err(InvalidAge(msg)) -> Stdout.line!("Age error: \(msg)")
```

**Why this translation:**
- Python exception hierarchies → Roc tag unions for error types
- Python `raise` → Roc `Err(tag)`
- Python `try/except` with hierarchy → Roc pattern matching on all error variants
- Roc's exhaustive matching ensures all error cases are handled at compile time

### Pattern 10: Decorators → Higher-Order Functions

**Python:**
```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

@log_calls
def add(a: int, b: int) -> int:
    return a + b

result = add(2, 3)
```

**Roc:**
```roc
# Higher-order function approach
logCalls : (a -> b), Str -> (a -> b)
logCalls = \fn, name ->
    \arg ->
        Stdout.line!("Calling \(name)")
        result = fn(arg)
        Stdout.line!("Result: \(Inspect.toStr(result))")
        result

# Note: The above won't work because Stdout.line! is effectful
# In Roc, decorators with side effects need Task wrapping

# For pure logging (accumulated), use:
loggedAdd : I64, I64 -> (I64, List Str)
loggedAdd = \a, b ->
    result = a + b
    logs = ["Calling add", "Result: \(Num.toStr(result))"]
    (result, logs)
```

**Why this translation:**
- Python decorators can have side effects anywhere; Roc enforces purity
- For logging with I/O, wrap in Task (not shown above for simplicity)
- For pure transformations, use higher-order functions
- Roc has no built-in decorator syntax; use explicit function composition

---

## Error Handling

### Python Exceptions → Roc Result

Python relies heavily on exceptions for error handling. Roc has no exceptions - all errors are values via the Result type.

**Conversion strategy:**
1. Identify all `raise` statements → Convert to `Err(tag)` returns
2. Identify all `try/except` blocks → Convert to `when ... is` pattern matching
3. Define error tag unions for related errors
4. Use `!` (try operator) for error propagation up the call stack

**Python:**
```python
def parse_and_divide(a_str: str, b_str: str) -> int:
    try:
        a = int(a_str)
        b = int(b_str)
        if b == 0:
            raise ValueError("Division by zero")
        return a // b
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")

try:
    result = parse_and_divide("10", "2")
    print(f"Result: {result}")
except ValueError as e:
    print(f"Error: {e}")
```

**Roc:**
```roc
ParseError : [InvalidNumber Str, DivByZero]

parseAndDivide : Str, Str -> Result I64 ParseError
parseAndDivide = \aStr, bStr ->
    a = Str.toI64!(aStr)
        |> Result.mapErr(\_ -> InvalidNumber("Invalid number: \(aStr)"))

    b = Str.toI64!(bStr)
        |> Result.mapErr(\_ -> InvalidNumber("Invalid number: \(bStr)"))

    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

# Usage
when parseAndDivide("10", "2") is
    Ok(result) -> Stdout.line!("Result: \(Num.toStr(result))")
    Err(InvalidNumber(msg)) -> Stdout.line!("Error: \(msg)")
    Err(DivByZero) -> Stdout.line!("Error: Division by zero")
```

**Key differences:**
- Python exceptions can be raised from anywhere; Roc Result must be explicitly returned
- Python exception hierarchy (base/derived); Roc tag unions (flat structure with tags)
- Python `try/except` is runtime; Roc pattern matching is compile-time verified (exhaustiveness)

---

## Concurrency & Async Patterns

### Python Threading/Asyncio → Roc Task

Python has multiple concurrency models (threading, multiprocessing, asyncio). Roc delegates all concurrency to the platform via Task.

**Python (Threading):**
```python
import threading

def worker(name: str, result_list: list):
    # Simulate work
    result = f"Worker {name} done"
    result_list.append(result)

results = []
threads = [
    threading.Thread(target=worker, args=(f"T{i}", results))
    for i in range(3)
]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(results)
```

**Python (Asyncio):**
```python
import asyncio

async def worker(name: str) -> str:
    await asyncio.sleep(0.1)
    return f"Worker {name} done"

async def main():
    tasks = [worker(f"T{i}") for i in range(3)]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

**Roc:**
```roc
import pf.Task exposing [Task]

worker : Str -> Task Str []
worker = \name ->
    # Platform handles concurrency
    Task.ok("Worker \(name) done")

main : Task {} []
main =
    tasks = List.range({ start: At(0), end: Before(3) })
        |> List.map(\i -> worker("T\(Num.toStr(i))"))

    results = Task.sequence!(tasks)  # Platform may parallelize

    Stdout.line!(Inspect.toStr(results))
```

**Why this translation:**
- Python explicit threading/asyncio → Roc platform-controlled concurrency
- Python `asyncio.gather` → Roc `Task.sequence` (platform decides how to execute)
- Python threads share memory (GIL); Roc Task isolates effects via platform
- Roc applications don't manage threads - the platform does

### GIL Considerations

Python's Global Interpreter Lock (GIL) limits true parallelism for CPU-bound tasks. Roc has no GIL - parallelism is platform-dependent.

| Python Limitation | Roc Advantage |
|-------------------|---------------|
| Threading blocked by GIL | Platform can use true parallelism |
| Need multiprocessing for CPU-bound | Platform handles scheduling |
| Async only for I/O-bound | Task can be I/O or compute |

**Key insight:** When converting from Python, you may gain concurrency benefits if the Roc platform implements parallel task execution.

---

## Dev Workflow Translation

### REPL-Driven Development → Expect-Driven Development

Python has a strong REPL culture (IPython, Jupyter). Roc has `roc repl` but it's more limited. The conversion requires adapting workflows.

| Python Workflow | Roc Equivalent | Notes |
|-----------------|----------------|-------|
| IPython REPL | `roc repl` | Limited compared to IPython |
| Jupyter notebooks | N/A | No notebook support |
| Interactive debugging | `dbg` function | Print-style debugging |
| Hot reload | `roc dev` | Watches and rebuilds |
| `python script.py` | `roc run script.roc` | Direct execution |
| `pytest -k test_name` | `roc test` | Runs all expect statements |

**Python (REPL-driven):**
```python
# IPython session
>>> def double(x):
...     return x * 2
>>> double(5)  # Immediate feedback
10
>>> [double(x) for x in range(5)]  # Experiment
[0, 2, 4, 6, 8]
```

**Roc (Expect-driven):**
```roc
# In file
double : I64 -> I64
double = \x -> x * 2

# Inline tests provide rapid feedback
expect double(5) == 10
expect List.map([0, 1, 2, 3, 4], double) == [0, 2, 4, 6, 8]

# Run with: roc test file.roc
```

**Migration strategy:**
1. Convert interactive REPL experiments to `expect` statements
2. Use `roc test` for rapid feedback (similar to running code in REPL)
3. Use `roc dev` for watch mode during development
4. For exploration, write small test files instead of REPL sessions

---

## Common Pitfalls

1. **Trying to mutate variables**
   - Python allows `x = x + 1` on existing variable
   - Roc has no mutation - you'd create new bindings in new scopes
   - **Fix:** Embrace immutability; use recursion or fold for accumulation

2. **Assuming exceptions work**
   - Python: `raise ValueError("message")`
   - Roc has no exceptions
   - **Fix:** Use `Result a err` for all fallible operations

3. **Expecting duck typing**
   - Python: "If it has a .read() method, it's file-like"
   - Roc uses static structural typing
   - **Fix:** Define explicit record types or use abilities

4. **Forgetting to handle all error cases**
   - Python: Can catch broad `Exception` or miss cases
   - Roc enforces exhaustive pattern matching
   - **Fix:** Handle all variants in `when ... is` blocks

5. **Using mutable data structures**
   - Python: `list.append()`, `dict[key] = value`
   - Roc collections are immutable
   - **Fix:** Operations return new collections: `List.append`, `Dict.insert`

6. **Mixing pure and effectful code**
   - Python allows I/O anywhere
   - Roc enforces purity; I/O must be in `Task`
   - **Fix:** Separate pure business logic from effectful I/O at platform boundaries

7. **Expecting arbitrary precision integers**
   - Python `int` has unlimited precision
   - Roc integers have fixed sizes (I64, U64, etc.)
   - **Fix:** Choose appropriate size or handle overflow explicitly

8. **Assuming REPL workflow**
   - Python: IPython, interactive development
   - Roc REPL is more limited
   - **Fix:** Use `expect` for inline tests, `roc test` for rapid feedback

9. **Trying to use `None` directly**
   - Python: `value = None`, `if value is None:`
   - Roc has no `None` type
   - **Fix:** Use tag unions: `[Some a, None]` and pattern matching

10. **Forgetting platform/application split**
    - Python code is all in same runtime
    - Roc separates pure (app) from effects (platform)
    - **Fix:** Keep business logic pure, delegate I/O to platform Task

---

## Module System

### Python Modules → Roc Interfaces

**Python:**
```python
# user.py
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str

def create_user(name: str, email: str) -> User:
    return User(id=generate_id(), name=name, email=email)

def get_name(user: User) -> str:
    return user.name
```

**Roc:**
```roc
# User.roc
interface User
    exposes [User, createUser, getName]
    imports []

User : {
    id : I64,
    name : Str,
    email : Str,
}

createUser : Str, Str -> User
createUser = \name, email -> {
    id: generateId(),
    name,
    email,
}

getName : User -> Str
getName = \user -> user.name
```

**Migration notes:**
- Python modules → Roc interfaces (file-based modules)
- Python implicit exports → Roc explicit `exposes`
- Python imports → Roc `imports` clause

---

## Build System

### Python Project → Roc Application

**Python (pyproject.toml):**
```toml
[project]
name = "myproject"
version = "1.0.0"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
]
```

**Roc:**
```roc
# main.roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.Task exposing [Task]
import pf.Stdout

main : Task {} []
main =
    Stdout.line!("Hello, Roc!")
```

**Build commands:**
```bash
# Python
pip install .
pip install .[dev]
python -m myproject

# Roc
roc build main.roc
roc run main.roc
roc test main.roc
```

**Key differences:**
- Python uses pyproject.toml + pip/uv; Roc uses platform URLs
- Python has rich dependency ecosystem (PyPI); Roc uses platforms (more limited)
- Roc infers dependencies from imports; no separate manifest needed

---

## Testing

### pytest → expect

**Python (pytest):**
```python
# test_math.py
import pytest

def add(a: int, b: int) -> int:
    return a + b

def test_addition():
    assert add(2, 2) == 4

def test_addition_negative():
    assert add(-1, 1) == 0

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 3, 5),
    (10, -5, 5),
])
def test_addition_parametrized(a, b, expected):
    assert add(a, b) == expected
```

**Roc:**
```roc
# math.roc
add : I64, I64 -> I64
add = \a, b -> a + b

# Inline tests
expect add(2, 2) == 4
expect add(-1, 1) == 0

# Multiple test cases
expect add(1, 1) == 2
expect add(2, 3) == 5
expect add(10, -5) == 5
```

**Run tests:**
```bash
# Python
pytest

# Roc
roc test math.roc
```

**Migration strategy:**
- Convert pytest test functions to `expect` statements
- Place expects near the functions they test
- Parametrized tests become multiple `expect` statements
- Run with `roc test`

---

## Examples

### Example 1: Simple - Optional Handling

**Before (Python):**
```python
from typing import Optional

def find_first_even(numbers: list[int]) -> Optional[int]:
    for n in numbers:
        if n % 2 == 0:
            return n
    return None

numbers = [1, 3, 5, 6, 7, 8]
result = find_first_even(numbers)

if result is not None:
    print(f"Found: {result}")
else:
    print("No even number found")
```

**After (Roc):**
```roc
findFirstEven : List I64 -> [Some I64, None]
findFirstEven = \numbers ->
    when List.findFirst(numbers, \n -> n % 2 == 0) is
        Ok(n) -> Some(n)
        Err(_) -> None

numbers = [1, 3, 5, 6, 7, 8]
result = findFirstEven(numbers)

when result is
    Some(n) -> Stdout.line!("Found: \(Num.toStr(n))")
    None -> Stdout.line!("No even number found")
```

### Example 2: Medium - Result Error Handling with Chain

**Before (Python):**
```python
from typing import Union

def parse_int(s: str) -> Union[int, str]:
    try:
        return int(s)
    except ValueError:
        return f"Invalid number: {s}"

def divide(a: int, b: int) -> Union[int, str]:
    if b == 0:
        return "Division by zero"
    return a // b

def calculate(a_str: str, b_str: str) -> Union[int, str]:
    a = parse_int(a_str)
    if isinstance(a, str):  # Error
        return a

    b = parse_int(b_str)
    if isinstance(b, str):  # Error
        return b

    return divide(a, b)

result = calculate("10", "2")
if isinstance(result, int):
    print(f"Result: {result}")
else:
    print(f"Error: {result}")
```

**After (Roc):**
```roc
CalcError : [ParseError Str, DivByZero]

parseInt : Str -> Result I64 [ParseError Str]
parseInt = \s ->
    Str.toI64(s)
    |> Result.mapErr(\_ -> ParseError("Invalid number: \(s)"))

divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

calculate : Str, Str -> Result I64 CalcError
calculate = \aStr, bStr ->
    a = parseInt!(aStr)
    b = parseInt!(bStr)
    divide!(a, b)

main : Task {} []
main =
    when calculate("10", "2") is
        Ok(result) -> Stdout.line!("Result: \(Num.toStr(result))")
        Err(ParseError(msg)) -> Stdout.line!("Error: \(msg)")
        Err(DivByZero) -> Stdout.line!("Error: Division by zero")
```

### Example 3: Complex - Async File Processing

**Before (Python):**
```python
import asyncio
from typing import List
from pathlib import Path

async def read_file(path: str) -> str:
    # Simulate async file read
    await asyncio.sleep(0.01)
    with open(path) as f:
        return f.read()

async def process_line(line: str) -> str:
    # Simulate async processing
    await asyncio.sleep(0.01)
    return line.upper()

async def process_file(input_path: str, output_path: str) -> None:
    # Read file
    content = await read_file(input_path)

    # Process lines concurrently
    lines = content.split('\n')
    tasks = [process_line(line) for line in lines]
    processed_lines = await asyncio.gather(*tasks)

    # Write result
    result = '\n'.join(processed_lines)
    with open(output_path, 'w') as f:
        f.write(result)

    print(f"Processed {len(lines)} lines")

async def main():
    try:
        await process_file("input.txt", "output.txt")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

**After (Roc):**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.File
import pf.Path
import pf.Task exposing [Task]
import pf.Stdout

# Pure function - process a line
processLine : Str -> Str
processLine = \line ->
    Str.toUpper(line)

# Task-based file processing
processFile : Str, Str -> Task {} [FileReadErr Path.ReadErr, FileWriteErr Path.WriteErr]*
processFile = \inputPath, outputPath ->
    # Read file (Task)
    content = File.readUtf8!(Path.fromStr(inputPath))

    # Process lines (pure)
    lines = Str.split(content, "\n")
    processedLines = List.map(lines, processLine)
    result = Str.joinWith(processedLines, "\n")

    # Write file (Task)
    File.writeUtf8!(Path.fromStr(outputPath), result)

    # Log completion
    Stdout.line!("Processed \(Num.toStr(List.len(lines))) lines")

main : Task {} []
main =
    when processFile("input.txt", "output.txt") is
        Ok({}) -> Stdout.line!("Success!")
        Err(FileReadErr(_)) -> Stdout.line!("Error: Could not read file")
        Err(FileWriteErr(_)) -> Stdout.line!("Error: Could not write file")
```

**Key conversions demonstrated:**
- Python `async/await` → Roc `Task` with `!` operator
- Python `asyncio.gather` for concurrency → Roc uses pure `List.map` (no async needed for CPU-bound processing)
- Python exception handling → Roc `when ... is` with typed errors
- Python mixes I/O and logic → Roc separates pure (`processLine`) from effectful (`File.read`, `File.write`)

---

## Limitations

Due to gaps in the `lang-roc-dev` skill (6/8 pillars), external research and inference were used for:

### Coverage Gaps

| Pillar | Python | Roc | Mitigation |
|--------|--------|-----|------------|
| Module | ✓ | ✓ | Both well-documented |
| Error | ✓ | ✓ | Result pattern clear |
| Concurrency | ✓ | ✓ | Task model documented |
| Metaprogramming | ~ | ✓ | Roc minimalist approach clear |
| Zero/Default | ✓ | ~ | Used tag union pattern |
| Serialization | ✓ | ~ | Inferred from abilities |
| Build | ✓ | ~ | Inferred from examples |
| Testing | ✓ | ✓ | Both covered |
| Dev Workflow | ✓ | ~ | Python REPL → Roc expect |

**Combined Score:** 14.5/18 (Good) - 8 pillars + dev workflow pillar

**Known Limitations:**

1. **Serialization:** Roc Encode/Decode abilities exist but aren't fully documented in lang-roc-dev; patterns inferred from platform usage
2. **Build System:** Roc build is simpler than Python's but emerging; limited packaging guidance
3. **Zero/Default:** Roc handles via tag unions and pattern matching; no dedicated section in lang-roc-dev

### External Resources Used

| Resource | What It Provided | Reliability |
|----------|------------------|-------------|
| Roc Tutorial | Platform model, Task usage | High |
| lang-python-dev | Comprehensive Python patterns | High |
| lang-roc-dev | Type system, records, tags | High |
| convert-python-erlang | REPL → compiled workflow | High |
| convert-fsharp-roc | Functional → Roc patterns | High |

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| `roc` CLI | Build, run, test, format | All-in-one tool |
| `roc build` | Compile to binary | Fast incremental builds |
| `roc run` | Execute directly | Like `python script.py` |
| `roc test` | Run expect statements | Inline testing |
| `roc format` | Code formatting | Like `black` or `ruff format` |
| `roc repl` | Interactive shell | More limited than IPython |
| `roc dev` | Watch mode | Rebuild on file changes |
| Roc LSP | Editor support | VS Code, vim integration |

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-python-rust` - Python → Rust conversion for ownership focus
- `convert-python-erlang` - Python → Erlang for BEAM runtime patterns
- `convert-fsharp-roc` - F# → Roc for .NET to native functional conversion
- `lang-python-dev` - Python development patterns
- `lang-roc-dev` - Roc development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async, Task, threading across languages
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Decorators, code generation across languages

---

## References

- [Roc Tutorial](https://www.roc-lang.org/tutorial)
- [Roc Platform Model](https://www.roc-lang.org/platforms)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Python to Functional Programming](https://docs.python.org/3/howto/functional.html)
