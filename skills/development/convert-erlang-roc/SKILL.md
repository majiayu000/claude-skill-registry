---
name: convert-erlang-roc
description: Convert Erlang code to idiomatic Roc. Use when migrating Erlang projects to Roc, translating BEAM/OTP patterns to functional patterns, or refactoring Erlang codebases. Extends meta-convert-dev with Erlang-to-Roc specific patterns.
---

# Convert Erlang to Roc

Convert Erlang code to idiomatic Roc. This skill extends `meta-convert-dev` with Erlang-to-Roc specific type mappings, idiom translations, and architectural patterns for moving from process-based concurrency to pure functional programming.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Erlang dynamic types → Roc static types
- **Paradigm translation**: Process-based concurrency → Pure functional with Tasks
- **Idiom translations**: OTP patterns → Roc functional patterns
- **Error handling**: Let-it-crash + supervisors → Result types
- **Concurrency**: Erlang processes → Roc platform Tasks
- **Module system**: Erlang modules → Roc platform/application architecture

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Erlang language fundamentals - see `lang-erlang-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → Erlang) - see `convert-roc-erlang`

---

## Quick Reference

| Erlang | Roc | Notes |
|--------|-----|-------|
| `atom()` | `[TagName]` | Atoms become tags |
| `integer()` | `I64` / `U64` | Specify signedness |
| `float()` | `F64` | 64-bit float |
| `binary()` | `List U8` | Byte sequences |
| `list()` | `List a` | Homogeneous lists |
| `tuple()` | `(a, b, c)` | Fixed-size tuples |
| `map()` | `Dict k v` | Key-value maps |
| `{ok, Value}` | `Ok(value)` | Success result |
| `{error, Reason}` | `Err(reason)` | Error result |
| `pid()` | - | No direct equivalent (use platform) |
| `fun(() -> T)` | `({} -> T)` | Zero-arg function |
| `undefined` | `None` in tag union | Optional values |

## When Converting Code

1. **Analyze BEAM semantics** before writing Roc
2. **Identify process boundaries** - these become platform interactions
3. **Map dynamic patterns to static types** - use tag unions for variants
4. **Redesign supervision trees** - Roc platforms handle failure differently
5. **Extract pure logic** - separate computation from effects
6. **Test equivalence** - verify behavior matches despite different architecture

---

## Paradigm Translation

### Mental Model Shift: BEAM Processes → Pure Functions + Platform Tasks

| Erlang Concept | Roc Approach | Key Insight |
|----------------|--------------|-------------|
| Process with state | Record + functions operating on record | Data and behavior separated, no hidden state |
| Message passing | Function parameters and results | Explicit data flow, no mailboxes |
| Spawn process | Platform task | Effects are platform capability, not language feature |
| gen_server | Pure state machine + platform Task | Business logic pure, I/O delegated to platform |
| Supervisor | Platform-level concern | Fault tolerance handled by host, not application |
| Hot code reload | Platform capability | Not a language feature in Roc |
| Distributed Erlang | Platform networking | Distribution is platform responsibility |

### Concurrency Mental Model

| Erlang Model | Roc Model | Conceptual Translation |
|--------------|-----------|------------------------|
| Lightweight processes | Platform Tasks | Concurrency is platform capability |
| Process mailbox | Function composition | Messages become function parameters |
| Selective receive | Pattern matching on values | Match on data, not messages in mailbox |
| Process monitoring | Result types | Failure becomes explicit error values |
| Links and trapping exits | Error propagation with Result | Explicit error handling replaces process signals |

---

## Type System Mapping

### Primitive Types

| Erlang | Roc | Notes |
|--------|-----|-------|
| `atom()` | `[Tag]` or `Str` | Atoms as tags for enums, Str for dynamic atoms |
| `integer()` | `I64` | Default signed 64-bit |
| `integer()` | `U64` | Unsigned variant |
| `integer()` (small) | `I32` / `U32` | For smaller values |
| `integer()` (big) | `I128` / `U128` | For very large values |
| `float()` | `F64` | 64-bit floating point |
| `boolean()` | `Bool` | Direct mapping |
| `binary()` | `List U8` | Byte sequence as list |
| `bitstring()` | `List U8` | Byte-aligned only in Roc |
| `reference()` | - | No direct equivalent |
| `pid()` | - | Processes don't exist in Roc |
| `port()` | - | Platform handles I/O |
| `fun()` | Function types | See function mappings below |

### Collection Types

| Erlang | Roc | Notes |
|--------|-----|-------|
| `list()` | `List a` | Homogeneous lists |
| `[T]` notation | `List T` | Type-safe, uniform elements |
| `tuple()` | `(A, B, C)` | Fixed-size tuples |
| `{A, B, C}` | `(A, B, C)` | Direct structural mapping |
| `map()` | `Dict k v` | Key-value dictionary |
| `#{K => V}` | `Dict K V` | Must have Hash + Eq for keys |
| `sets:set()` | `Set a` | Unique values |
| `ordsets:set()` | `Set a` | Roc sets are always ordered |
| `queue:queue()` | `List a` | Use list operations |
| `array:array()` | `List a` | Lists in Roc are efficient |

### Composite Types

| Erlang | Roc | Notes |
|--------|-----|-------|
| `-record(name, {field :: type()})` | `{ field : Type }` | Records become record types |
| `#name{field = Value}` | `{ field: value }` | Record literals |
| Tagged tuple `{tag, Value}` | `Tag(value)` | Tags with payloads |
| Union types (spec) | `[Tag1, Tag2, Tag3]` | Tag unions |
| `-type name() :: spec.` | `Name : Type` | Type alias |
| `-opaque name() :: spec.` | Opaque type `Name := Type` | Hidden implementation |

### Function Types

| Erlang | Roc | Notes |
|--------|-----|-------|
| `fun(() -> R)` | `({} -> R)` | Zero-argument function |
| `fun((A) -> R)` | `(A -> R)` | Single argument |
| `fun((A, B) -> R)` | `(A, B -> R)` | Multiple arguments |
| `fun((A, ...) -> R)` | - | Roc doesn't support varargs |

### Error Types

| Erlang | Roc | Notes |
|--------|-----|-------|
| `{ok, Value}` | `Ok(value)` | Success case |
| `{error, Reason}` | `Err(reason)` | Error case |
| `ok` atom | `Ok({})` | Success with no value |
| `{ok, V} \| {error, R}` | `Result V R` | Result type |
| Exception throw | `Err` variant | No exceptions, use Result |

---

## Idiom Translation

### Pattern 1: Simple Function Conversion

**Erlang:**
```erlang
-module(math_utils).
-export([add/2, square/1]).

add(A, B) -> A + B.

square(N) -> N * N.
```

**Roc:**
```roc
interface MathUtils
    exposes [add, square]
    imports []

add : I64, I64 -> I64
add = \a, b -> a + b

square : I64 -> I64
square = \n -> n * n
```

**Why this translation:**
- Erlang modules become Roc interfaces
- Exported functions go in `exposes`
- Type signatures are inferred but can be explicit
- Function definitions use lambda syntax

### Pattern 2: Pattern Matching on Tagged Tuples

**Erlang:**
```erlang
process_result({ok, Data}) ->
    {success, Data};
process_result({error, Reason}) ->
    {failure, Reason};
process_result(unknown) ->
    {failure, unknown_result}.
```

**Roc:**
```roc
processResult : [Ok Data, Err Reason, Unknown] -> [Success Data, Failure Reason]
processResult = \result ->
    when result is
        Ok(data) -> Success(data)
        Err(reason) -> Failure(reason)
        Unknown -> Failure(UnknownResult)
```

**Why this translation:**
- Erlang tagged tuples map to Roc tags
- Pattern matching syntax is similar
- Tag unions make all cases explicit
- Type system ensures exhaustiveness

### Pattern 3: List Processing

**Erlang:**
```erlang
sum([]) -> 0;
sum([H|T]) -> H + sum(T).

map(_, []) -> [];
map(F, [H|T]) -> [F(H) | map(F, T)].

filter(_, []) -> [];
filter(Pred, [H|T]) ->
    case Pred(H) of
        true -> [H | filter(Pred, T)];
        false -> filter(Pred, T)
    end.
```

**Roc:**
```roc
sum : List I64 -> I64
sum = \list ->
    List.walk(list, 0, Num.add)

map : List a, (a -> b) -> List b
map = \list, fn ->
    List.map(list, fn)

filter : List a, (a -> Bool) -> List a
filter = \list, pred ->
    List.keepIf(list, pred)
```

**Why this translation:**
- Roc provides built-in list functions
- `List.walk` is fold/reduce
- Explicit recursion not needed for common operations
- Higher-order functions are idiomatic

### Pattern 4: Records to Records

**Erlang:**
```erlang
-record(user, {
    name :: string(),
    age :: integer(),
    email :: string()
}).

create_user(Name, Age, Email) ->
    #user{name=Name, age=Age, email=Email}.

update_age(#user{} = User, NewAge) ->
    User#user{age=NewAge}.

get_name(#user{name=Name}) ->
    Name.
```

**Roc:**
```roc
User : {
    name : Str,
    age : U32,
    email : Str,
}

createUser : Str, U32, Str -> User
createUser = \name, age, email ->
    { name, age, email }

updateAge : User, U32 -> User
updateAge = \user, newAge ->
    { user & age: newAge }

getName : User -> Str
getName = \{ name } ->
    name
```

**Why this translation:**
- Erlang records map directly to Roc records
- Record update syntax is similar (`#record{}` vs `{ record & }`)
- Pattern matching on records works similarly
- Roc records are structural, not nominal

### Pattern 5: gen_server State Machine → Pure State Functions

**Erlang:**
```erlang
-module(counter_server).
-behaviour(gen_server).

-export([start_link/0, increment/0, get_count/0]).
-export([init/1, handle_call/3, handle_cast/2]).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

increment() ->
    gen_server:cast(?MODULE, increment).

get_count() ->
    gen_server:call(?MODULE, get_count).

init([]) ->
    {ok, 0}.

handle_call(get_count, _From, Count) ->
    {reply, Count, Count}.

handle_cast(increment, Count) ->
    {noreply, Count + 1}.
```

**Roc:**
```roc
# Pure state machine - no processes
State : I64

init : State
init = 0

increment : State -> State
increment = \count ->
    count + 1

getCount : State -> I64
getCount = \count ->
    count

# If you need effects, use platform Tasks
# Platform would provide state management primitives
```

**Why this translation:**
- gen_server becomes pure state functions
- No process lifecycle - just data transformation
- State is explicit parameter and return value
- Effects would be handled by platform, not shown here
- Platform provides concurrency if needed

### Pattern 6: Error Handling with Result

**Erlang:**
```erlang
divide(_, 0) ->
    {error, division_by_zero};
divide(A, B) ->
    {ok, A / B}.

safe_divide(A, B) ->
    case divide(A, B) of
        {ok, Result} -> Result;
        {error, _} -> 0
    end.
```

**Roc:**
```roc
divide : F64, F64 -> Result F64 [DivisionByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivisionByZero)
    else
        Ok(a / b)

safeDivide : F64, F64 -> F64
safeDivide = \a, b ->
    divide(a, b)
    |> Result.withDefault(0)
```

**Why this translation:**
- Erlang error tuples map to Roc Result type
- Pattern matching on Result works like case
- Result combinators (`withDefault`) are idiomatic
- Compile-time exhaustiveness checking

### Pattern 7: Optional Values

**Erlang:**
```erlang
find_user(Id, Users) ->
    case lists:keyfind(Id, #user.id, Users) of
        false -> undefined;
        User -> User
    end.

get_email(undefined) -> "no email";
get_email(#user{email=Email}) -> Email.
```

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
```

**Why this translation:**
- Erlang `undefined` maps to tag union with None
- `false` from failed search becomes None
- Pattern matching on option types is explicit
- Type system prevents forgetting to handle None case

### Pattern 8: List Comprehensions

**Erlang:**
```erlang
squares(List) ->
    [X * X || X <- List].

evens(List) ->
    [X || X <- List, X rem 2 == 0].

pairs(List1, List2) ->
    [{X, Y} || X <- List1, Y <- List2].
```

**Roc:**
```roc
squares : List I64 -> List I64
squares = \list ->
    List.map(list, \x -> x * x)

evens : List I64 -> List I64
evens = \list ->
    List.keepIf(list, \x -> x % 2 == 0)

pairs : List a, List b -> List (a, b)
pairs = \list1, list2 ->
    List.joinMap(list1, \x ->
        List.map(list2, \y -> (x, y))
    )
```

**Why this translation:**
- Comprehensions become map/filter operations
- Nested comprehensions use `joinMap` (flatMap)
- More verbose but explicit
- Type signatures make intent clear

---

## Concurrency Patterns

### Erlang Process Model vs Roc Task Model

Erlang's concurrency is built on lightweight processes with message passing. Roc has no built-in concurrency - it's all platform-provided.

**Erlang:**
```erlang
% Spawn a worker process
Pid = spawn(fun() -> worker_loop() end),

% Send message
Pid ! {self(), work, Data},

% Receive response
receive
    {Pid, result, Result} -> Result
after 5000 ->
    timeout
end.

worker_loop() ->
    receive
        {From, work, Data} ->
            Result = process(Data),
            From ! {self(), result, Result},
            worker_loop();
        stop ->
            ok
    end.
```

**Roc:**
```roc
# No processes - pure functions operating on data
processWork : Data -> Result
processWork = \data ->
    # Pure computation
    transform(data)

# If concurrent work is needed, platform provides Tasks
# Platform interface might look like:
doWork : Data -> Task Result []
doWork = \data ->
    # Platform handles execution
    Task.fromResult(processWork(data))

# Multiple concurrent tasks (platform-dependent)
doMultipleWork : List Data -> Task (List Result) []
doMultipleWork = \dataList ->
    dataList
    |> List.map(doWork)
    |> Task.sequence  # Platform parallelizes
```

**Why this approach:**
- Roc applications don't manage processes
- Concurrency is a platform capability
- Business logic stays pure
- Platform provides Task-based effects

### Supervision Trees → Error Handling

**Erlang:**
```erlang
-module(my_supervisor).
-behaviour(supervisor).

init([]) ->
    SupFlags = #{
        strategy => one_for_one,
        intensity => 5,
        period => 60
    },

    ChildSpecs = [
        #{
            id => worker1,
            start => {worker, start_link, []},
            restart => permanent,
            shutdown => 5000,
            type => worker
        }
    ],

    {ok, {SupFlags, ChildSpecs}}.
```

**Roc:**
```roc
# Roc doesn't have supervision trees
# Instead, errors are explicit via Result types
# Platform handles process-level concerns

# Application code propagates errors explicitly
doWorkflow : Input -> Result Output [WorkerFailed, ValidationFailed]
doWorkflow = \input ->
    validated = validate!(input)
    processed = processData!(validated)
    saved = saveResult!(processed)
    Ok(saved)

# Platform provides retry/recovery if needed
withRetry : Task a err, U32 -> Task a err
withRetry = \task, maxAttempts ->
    # Platform-provided retry logic
    Task.retry(task, maxAttempts)
```

**Why this translation:**
- Supervision is platform responsibility, not application code
- Errors are explicit Result values
- No automatic restart - retry is explicit
- Crash recovery happens at platform/host level

### Distributed Erlang → Platform Networking

**Erlang:**
```erlang
% Connect to remote node
net_adm:ping('node2@hostname'),

% Spawn on remote node
Pid = spawn('node2@hostname', worker, loop, []),

% Send to remote process
{worker, 'node2@hostname'} ! Message,

% RPC call
rpc:call('node2@hostname', module, function, [Args]).
```

**Roc:**
```roc
# No distributed Erlang equivalent
# Platform provides networking as I/O capability

# Hypothetical platform networking API
sendRequest : Str, Request -> Task Response [NetworkErr]
sendRequest = \url, request ->
    # Platform handles HTTP/networking
    Http.post(url, request)

# Distributed work requires platform support
# Not a language feature
```

**Why this approach:**
- Distribution is platform capability, not language
- No node clustering built-in
- Network calls are explicit I/O via Tasks
- Platform defines distribution model

---

## Error Handling

### Let It Crash → Explicit Result Types

**Erlang Philosophy:**
```erlang
% Let it crash - supervisor will restart
process_data(Data) ->
    validate(Data),      % May throw
    transform(Data),     % May throw
    save(Data).         % May throw
```

**Roc Philosophy:**
```roc
# Make errors explicit with Result types
processData : Data -> Result Success [ValidationErr, TransformErr, SaveErr]
processData = \data ->
    validated = validate!(data)
    transformed = transform!(validated)
    saved = save!(transformed)
    Ok(saved)
```

**Key Differences:**
- Erlang: Crash and restart via supervisor
- Roc: Explicit error propagation via Result
- Erlang: Fault tolerance via process isolation
- Roc: Fault tolerance via platform (if needed)

### Error Pattern Translation

| Erlang Pattern | Roc Pattern | Notes |
|----------------|-------------|-------|
| `throw(Error)` | `Err(error)` | No exceptions, use Result |
| `exit(Reason)` | `Err(reason)` | Process exit becomes error value |
| `error(Reason)` | `Err(reason)` | Runtime error becomes Result |
| `try...catch` | `when result is Ok/Err` | Pattern match on Result |
| Supervisor restart | Platform responsibility | Not in application code |
| Process link | Error propagation via Result | No process links |
| Monitor/demonitor | - | No monitoring in Roc |

---

## Module System

### Erlang Module → Roc Interface

**Erlang:**
```erlang
-module(calculator).
-export([add/2, subtract/2]).
-export_type([result/0]).

-type result() :: {ok, number()} | {error, atom()}.

add(A, B) -> {ok, A + B}.
subtract(A, B) -> {ok, A - B}.
```

**Roc:**
```roc
interface Calculator
    exposes [Result, add, subtract]
    imports []

Result : [Ok F64, Err [InvalidInput]]

add : F64, F64 -> Result
add = \a, b -> Ok(a + b)

subtract : F64, F64 -> Result
subtract = \a, b -> Ok(a - b)
```

**Why this translation:**
- `-module` becomes `interface`
- `-export` becomes `exposes`
- `-export_type` types also go in `exposes`
- Type definitions use Roc syntax

### Application Structure

**Erlang Application:**
```
my_app/
├── src/
│   ├── my_app.erl
│   ├── my_app_sup.erl
│   └── my_worker.erl
├── include/
│   └── my_app.hrl
└── ebin/
```

**Roc Application:**
```
my-app/
├── main.roc          # Entry point
├── Worker.roc        # Worker module
└── Types.roc         # Shared types
```

**Key Differences:**
- Roc: Single entry point (`main.roc`)
- No supervision tree in application code
- Platform provides I/O capabilities
- Simpler directory structure

---

## Platform Architecture

### OTP Application → Roc Application + Platform

**Erlang OTP Application:**
```erlang
% Application behavior
-module(my_app).
-behaviour(application).

start(_Type, _Args) ->
    my_app_sup:start_link().

stop(_State) ->
    ok.
```

**Roc Application:**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/..."
}

import pf.Stdout
import pf.Task exposing [Task]

main : Task {} []
main =
    Stdout.line!("Hello, World!")
```

**Why this approach:**
- Roc separates platform (I/O) from application (logic)
- Platform provides lifecycle, not application
- No application behavior callback
- Platform handles startup/shutdown

### BEAM Runtime → Platform + Host

```
┌─────────────────────────────────┐
│   Erlang on BEAM                │
│                                 │
│  • Processes                    │
│  • Schedulers                   │
│  • Message passing              │
│  • Hot code reload              │
│  • Distribution                 │
└─────────────────────────────────┘

             ⬇

┌─────────────────────────────────┐
│   Roc Application (Pure)        │
│                                 │
│  • Pure functions               │
│  • Data transformations         │
│  • Business logic               │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   Platform + Host               │
│                                 │
│  • Task execution               │
│  • I/O operations               │
│  • Concurrency (if provided)    │
│  • Memory management            │
└─────────────────────────────────┘
```

---

## Testing Strategy

### EUnit → Roc expect

**Erlang EUnit:**
```erlang
-module(calculator_tests).
-include_lib("eunit/include/eunit.hrl").

add_test() ->
    ?assertEqual({ok, 5}, calculator:add(2, 3)).

subtract_test() ->
    ?assertEqual({ok, 1}, calculator:subtract(3, 2)).
```

**Roc expect:**
```roc
# Inline tests with expect
add : I64, I64 -> I64
add = \a, b -> a + b

expect add(2, 3) == 5
expect add(0, 0) == 0
expect add(-1, 1) == 0

# Top-level expects run with `roc test`
expect
    result = add(2, 3)
    result == 5
```

**Why this translation:**
- Roc uses inline `expect` statements
- No test framework needed
- Tests live with code
- Run with `roc test`

### Property-Based Testing

**Erlang PropEr:**
```erlang
prop_reverse_twice() ->
    ?FORALL(List, list(integer()),
            lists:reverse(lists:reverse(List)) =:= List).
```

**Roc:**
```roc
# Roc doesn't have built-in property testing yet
# For now, write explicit test cases

expect
    list = [1, 2, 3, 4, 5]
    reversed = List.reverse(list)
    doubleReversed = List.reverse(reversed)
    doubleReversed == list

# Future: property testing libraries may emerge
```

---

## Common Pitfalls

1. **Trying to translate processes directly**: Erlang processes don't exist in Roc. Redesign around pure functions and platform Tasks.

2. **Missing the paradigm shift**: Erlang is concurrent-first, Roc is pure-first. Separate computation from effects.

3. **Assuming mutable state**: Erlang has process state, Roc uses immutable data. State changes are new values.

4. **Ignoring the platform boundary**: In Roc, all I/O goes through the platform. Don't expect direct system calls.

5. **Translating supervisors**: Supervision is platform-level. Don't try to implement restart logic in application code.

6. **Dynamic typing habits**: Erlang allows `any()`, Roc requires explicit types. Use tag unions for variants.

7. **Hot code reload**: Erlang supports this, Roc doesn't. Not a conversion concern.

8. **Binary pattern matching**: Erlang's binary patterns are powerful, Roc works with List U8. May need rethinking.

9. **Distributed Erlang features**: node clustering, global registry, etc. - these are BEAM features, not Roc capabilities.

10. **Atom literals everywhere**: Erlang uses atoms liberally, Roc needs explicit tag unions or strings.

---

## Tooling

| Purpose | Erlang | Roc | Notes |
|---------|--------|-----|-------|
| Build tool | rebar3, mix | `roc` CLI | Roc has single tool |
| Package manager | hex.pm | Platform URLs | No package registry yet |
| Testing | EUnit, CT, PropEr | `roc test` | Built-in testing |
| REPL | `erl` shell | - | No Roc REPL yet |
| Formatter | erlfmt | `roc format` | Automatic formatting |
| Documentation | EDoc | Comments | No doc tool yet |
| Debugger | debugger | - | No debugger yet |
| Profiling | fprof, eprof | - | Platform-specific |

---

## Examples

### Example 1: Simple - Function with Pattern Matching

**Before (Erlang):**
```erlang
-module(color).
-export([to_string/1]).

to_string(red) -> "Red";
to_string(green) -> "Green";
to_string(blue) -> "Blue";
to_string({rgb, R, G, B}) ->
    io_lib:format("RGB(~p, ~p, ~p)", [R, G, B]).
```

**After (Roc):**
```roc
interface Color
    exposes [Color, toString]
    imports []

Color : [Red, Green, Blue, Rgb U8 U8 U8]

toString : Color -> Str
toString = \color ->
    when color is
        Red -> "Red"
        Green -> "Green"
        Blue -> "Blue"
        Rgb(r, g, b) -> "RGB(\(Num.toStr(r)), \(Num.toStr(g)), \(Num.toStr(b)))"
```

### Example 2: Medium - State Machine with Error Handling

**Before (Erlang):**
```erlang
-module(bank_account).
-export([new/0, deposit/2, withdraw/2, balance/1]).

-record(account, {
    balance = 0 :: integer()
}).

new() -> #account{}.

deposit(#account{balance=Balance} = Account, Amount) when Amount > 0 ->
    {ok, Account#account{balance=Balance + Amount}};
deposit(_, _) ->
    {error, invalid_amount}.

withdraw(#account{balance=Balance} = Account, Amount)
        when Amount > 0, Amount =< Balance ->
    {ok, Account#account{balance=Balance - Amount}};
withdraw(#account{balance=Balance}, Amount) when Amount > Balance ->
    {error, insufficient_funds};
withdraw(_, _) ->
    {error, invalid_amount}.

balance(#account{balance=Balance}) ->
    Balance.
```

**After (Roc):**
```roc
interface BankAccount
    exposes [Account, new, deposit, withdraw, balance]
    imports []

Account : { balance : U64 }

new : Account
new = { balance: 0 }

deposit : Account, U64 -> Result Account [InvalidAmount]
deposit = \account, amount ->
    if amount > 0 then
        Ok({ account & balance: account.balance + amount })
    else
        Err(InvalidAmount)

withdraw : Account, U64 -> Result Account [InvalidAmount, InsufficientFunds]
withdraw = \account, amount ->
    if amount == 0 then
        Err(InvalidAmount)
    else if amount > account.balance then
        Err(InsufficientFunds)
    else
        Ok({ account & balance: account.balance - amount })

balance : Account -> U64
balance = \account ->
    account.balance
```

### Example 3: Complex - gen_server Reimagined as Pure State Machine

**Before (Erlang):**
```erlang
-module(task_queue).
-behaviour(gen_server).

-export([start_link/0, add_task/1, get_next/0, count/0]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2]).

-record(state, {
    tasks = [] :: list(),
    processed = 0 :: integer()
}).

%% API
start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

add_task(Task) ->
    gen_server:cast(?MODULE, {add, Task}).

get_next() ->
    gen_server:call(?MODULE, get_next).

count() ->
    gen_server:call(?MODULE, count).

%% Callbacks
init([]) ->
    {ok, #state{}}.

handle_call(get_next, _From, #state{tasks=[]} = State) ->
    {reply, empty, State};
handle_call(get_next, _From, #state{tasks=[H|T], processed=P} = State) ->
    NewState = State#state{tasks=T, processed=P+1},
    {reply, {ok, H}, NewState};
handle_call(count, _From, #state{tasks=Tasks, processed=P} = State) ->
    {reply, {length(Tasks), P}, State}.

handle_cast({add, Task}, #state{tasks=Tasks} = State) ->
    NewState = State#state{tasks=Tasks ++ [Task]},
    {noreply, NewState}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.
```

**After (Roc):**
```roc
interface TaskQueue
    exposes [Queue, empty, addTask, getNext, count]
    imports []

Queue task : {
    tasks : List task,
    processed : U64,
}

empty : Queue task
empty = {
    tasks: [],
    processed: 0,
}

addTask : Queue task, task -> Queue task
addTask = \queue, task ->
    { queue & tasks: List.append(queue.tasks, task) }

getNext : Queue task -> Result (Queue task, task) [Empty]
getNext = \queue ->
    when queue.tasks is
        [] -> Err(Empty)
        [first, ..rest] ->
            newQueue = {
                tasks: rest,
                processed: queue.processed + 1,
            }
            Ok((newQueue, first))

count : Queue task -> { pending : U64, processed : U64 }
count = \queue ->
    {
        pending: List.len(queue.tasks),
        processed: queue.processed,
    }

# Usage example:
expect
    queue = empty
    queue1 = addTask(queue, "task1")
    queue2 = addTask(queue1, "task2")

    result = getNext(queue2)
    when result is
        Ok((queue3, task)) ->
            task == "task1" && count(queue3).pending == 1
        Err(Empty) -> Bool.false

# Note: This is a pure data structure
# If you need concurrent access, platform provides that capability
```

---

## Limitations

### Areas Where Direct Translation Is Difficult

1. **Hot Code Reload**: Erlang's live code update has no Roc equivalent. Requires restart.

2. **Distributed Features**: BEAM's clustering, global names, distributed process groups - not available in Roc.

3. **Process Isolation**: Erlang's per-process memory isolation doesn't map to Roc's data structures.

4. **Selective Receive**: Erlang's mailbox pattern matching doesn't exist - Roc uses function parameters.

5. **Binary Pattern Matching**: Erlang's bit-level patterns are more powerful than Roc's List U8.

6. **Dynamic Code**: Erlang's ability to load/call modules dynamically doesn't exist in statically-typed Roc.

7. **Process Monitoring**: Links, monitors, trapping exits - these are BEAM features, not portable to Roc.

### Working Around Limitations

- **Instead of hot reload**: Design for fast restart or use platform-provided mechanism
- **Instead of distribution**: Use explicit networking via platform HTTP/TCP
- **Instead of processes**: Use pure functions + platform Tasks
- **Instead of selective receive**: Structure data for pattern matching
- **Instead of binary patterns**: Work with List U8 and helper functions
- **Instead of dynamic code**: Use tag unions for known variants
- **Instead of process monitoring**: Use Result types for error handling

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-erlang-dev` - Erlang development patterns and OTP
- `lang-roc-dev` - Roc development patterns and platform model

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Processes vs actors vs tasks across languages
- `patterns-serialization-dev` - Encoding/decoding across languages
- `patterns-metaprogramming-dev` - Code generation approaches
