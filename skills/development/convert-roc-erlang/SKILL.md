---
name: convert-roc-erlang
description: Convert Roc code to idiomatic Erlang. Use when migrating Roc projects to Erlang/OTP, translating functional patterns to process-based architectures, or refactoring Roc codebases. Extends meta-convert-dev with Roc-to-Erlang specific patterns.
---

# Convert Roc to Erlang

Convert Roc code to idiomatic Erlang. This skill extends `meta-convert-dev` with Roc-to-Erlang specific type mappings, idiom translations, and architectural patterns for moving from pure functional programming to process-based concurrency.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Roc static types → Erlang dynamic types
- **Paradigm translation**: Pure functional + platform Tasks → Process-based concurrency
- **Idiom translations**: Roc functional patterns → OTP patterns
- **Error handling**: Result types → Let-it-crash + supervisors
- **Concurrency**: Roc platform Tasks → Erlang processes
- **Module system**: Roc platform/application → Erlang OTP application architecture

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Erlang language fundamentals - see `lang-erlang-dev`
- Reverse conversion (Erlang → Roc) - see `convert-erlang-roc`

---

## Quick Reference

| Roc | Erlang | Notes |
|-----|--------|-------|
| `[Tag]` | `atom()` | Tags become atoms |
| `I64` / `U64` | `integer()` | Erlang integers are arbitrary precision |
| `F64` | `float()` | 64-bit float |
| `List U8` | `binary()` | Byte sequences |
| `List a` | `list()` | Heterogeneous possible |
| `(a, b, c)` | `{a, b, c}` | Fixed-size tuples |
| `Dict k v` | `map()` or `#{k => v}` | Key-value maps |
| `Ok(value)` | `{ok, Value}` | Success result |
| `Err(reason)` | `{error, Reason}` | Error result |
| `Task a err` | Process/gen_server | Platform tasks become processes |
| `{} -> T` | `fun(() -> T)` | Zero-arg function |
| `None` in tag union | `undefined` | Optional values |

## When Converting Code

1. **Identify pure vs effectful** - Pure functions translate directly, effects need processes
2. **Design process architecture** - Tasks become gen_server or simple processes
3. **Map static types to dynamic patterns** - Use tagged tuples and specs
4. **Implement supervision** - Add supervision trees for fault tolerance
5. **Extract platform logic** - Platform becomes OTP behaviors
6. **Test equivalence** - Verify behavior matches despite different architecture

---

## Paradigm Translation

### Mental Model Shift: Pure Functions + Platform → Processes + Message Passing

| Roc Concept | Erlang Approach | Key Insight |
|-------------|-----------------|-------------|
| Pure function with data | Function or process state | Processes add lifecycle management |
| Function composition | Message passing or function calls | Choose based on concurrency needs |
| Platform task | Process with message loop | Effects require process model |
| Task chaining | Sequential message sends | Or gen_server calls |
| Result type | Tagged tuples `{ok, Val}` / `{error, Reason}` | Explicit error tuples |
| Tag unions | Tagged tuples and pattern matching | Multiple atoms as tags |
| Platform capabilities | OTP behaviors (gen_server, supervisor) | Framework provides structure |

### Concurrency Mental Model

| Roc Model | Erlang Model | Conceptual Translation |
|-----------|--------------|------------------------|
| Platform Tasks | Lightweight processes | Tasks become spawned processes |
| Task composition | Message passing | Chain via messages or calls |
| Pure data flow | Explicit message protocols | Messages are data flow |
| Platform error handling | Supervision trees | Let it crash philosophy |
| Platform-managed lifecycle | Process lifecycle + monitors | Explicit lifecycle management |

---

## Type System Mapping

### Primitive Types

| Roc | Erlang | Notes |
|-----|--------|-------|
| `Bool` | `true` / `false` | Boolean atoms |
| `I8`, `I16`, `I32`, `I64`, `I128` | `integer()` | Arbitrary precision in Erlang |
| `U8`, `U16`, `U32`, `U64`, `U128` | `integer()` | Erlang doesn't distinguish signed/unsigned |
| `F32`, `F64` | `float()` | 64-bit floating point |
| `Str` | `string()` / `binary()` | Use binary for efficiency |
| `List U8` | `binary()` | Byte sequences |

### Collection Types

| Roc | Erlang | Notes |
|-----|--------|-------|
| `List a` | `[a]` | Erlang lists can be heterogeneous |
| `Dict k v` | `#{k => v}` | Maps (Erlang 17+) |
| `Set a` | `sets:set(a)` or `gb_sets:set(a)` | Standard library modules |
| `(A, B, C)` | `{A, B, C}` | Direct tuple mapping |

### Composite Types

| Roc | Erlang | Notes |
|-----|--------|-------|
| `{ field : Type }` | `-record(name, {field :: type()})` | Records with type specs |
| `{ field : Type }` | `#{field => Type}` | Or maps for flexibility |
| `[Tag]` | `atom()` | Single tag becomes atom |
| `[Tag1, Tag2]` | Tagged tuple or atom | Multiple tags use tuples |
| `[Tag(A)]` | `{tag, A}` | Tag with payload |
| `Result a e` | `{ok, A} \| {error, E}` | Standard error convention |

### Function Types

| Roc | Erlang | Notes |
|-----|--------|-------|
| `{} -> R` | `fun(() -> R)` | Zero-argument function |
| `A -> R` | `fun((A) -> R)` | Single argument |
| `A, B -> R` | `fun((A, B) -> R)` | Multiple arguments |
| Generic `<a>` | Dynamic typing | No generics needed |

### Error Types

| Roc | Erlang | Notes |
|-----|--------|-------|
| `Ok(value)` | `{ok, Value}` | Success case |
| `Err(reason)` | `{error, Reason}` | Error case |
| `Result V R` | `{ok, V} \| {error, R}` | Result pattern |
| Tag unions for errors | Multiple error atoms/tuples | Explicit error variants |

---

## Idiom Translation

### Pattern 1: Simple Pure Function

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

**Erlang:**
```erlang
-module(math_utils).
-export([add/2, square/1]).

-spec add(integer(), integer()) -> integer().
add(A, B) -> A + B.

-spec square(integer()) -> integer().
square(N) -> N * N.
```

**Why this translation:**
- Roc interfaces become Erlang modules
- `exposes` maps to `-export`
- Type signatures become `-spec` declarations
- Lambda syntax becomes function clauses
- No process needed for pure functions

### Pattern 2: Pattern Matching on Tags

**Roc:**
```roc
processResult : [Ok Data, Err Reason, Unknown] -> [Success Data, Failure Reason]
processResult = \result ->
    when result is
        Ok(data) -> Success(data)
        Err(reason) -> Failure(reason)
        Unknown -> Failure(UnknownResult)
```

**Erlang:**
```erlang
-spec process_result({ok, Data} | {error, Reason} | unknown) ->
    {success, Data} | {failure, Reason}.
process_result({ok, Data}) ->
    {success, Data};
process_result({error, Reason}) ->
    {failure, Reason};
process_result(unknown) ->
    {failure, unknown_result}.
```

**Why this translation:**
- Roc tags map to Erlang atoms and tagged tuples
- `when` becomes multiple function clauses
- Pattern matching syntax is similar
- Tag payloads become tuple elements

### Pattern 3: List Processing

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

**Erlang:**
```erlang
-spec sum([integer()]) -> integer().
sum(List) ->
    lists:foldl(fun(X, Acc) -> X + Acc end, 0, List).

-spec map([A], fun((A) -> B)) -> [B].
map(List, Fn) ->
    lists:map(Fn, List).

-spec filter([A], fun((A) -> boolean())) -> [A].
filter(List, Pred) ->
    lists:filter(Pred, List).
```

**Why this translation:**
- `List.walk` becomes `lists:foldl`
- `List.map` becomes `lists:map`
- `List.keepIf` becomes `lists:filter`
- Higher-order functions translate directly
- Erlang lists module provides standard operations

### Pattern 4: Records

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

**Erlang:**
```erlang
-record(user, {
    name :: string(),
    age :: non_neg_integer(),
    email :: string()
}).

-spec create_user(string(), non_neg_integer(), string()) -> #user{}.
create_user(Name, Age, Email) ->
    #user{name=Name, age=Age, email=Email}.

-spec update_age(#user{}, non_neg_integer()) -> #user{}.
update_age(User, NewAge) ->
    User#user{age=NewAge}.

-spec get_name(#user{}) -> string().
get_name(#user{name=Name}) ->
    Name.
```

**Why this translation:**
- Roc records map to Erlang records
- Record update syntax is similar
- Pattern matching on records works similarly
- Use type specs for record field types

### Pattern 5: Pure State Functions → gen_server

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

# Platform would provide state management primitives
```

**Erlang:**
```erlang
-module(counter_server).
-behaviour(gen_server).

-export([start_link/0, increment/0, get_count/0]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2,
         terminate/2, code_change/3]).

%% API
start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

increment() ->
    gen_server:cast(?MODULE, increment).

get_count() ->
    gen_server:call(?MODULE, get_count).

%% gen_server callbacks
init([]) ->
    {ok, 0}.

handle_call(get_count, _From, Count) ->
    {reply, Count, Count};
handle_call(_Request, _From, State) ->
    {reply, ok, State}.

handle_cast(increment, Count) ->
    {noreply, Count + 1};
handle_cast(_Msg, State) ->
    {noreply, State}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.
```

**Why this translation:**
- Pure state functions become gen_server state machine
- State is maintained by process, not passed as parameter
- Function calls become gen_server:call or cast
- OTP provides supervision and fault tolerance
- Process lifecycle adds start_link, terminate

### Pattern 6: Result Type → Tagged Tuples

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

**Erlang:**
```erlang
-spec divide(float(), float()) -> {ok, float()} | {error, division_by_zero}.
divide(_A, 0.0) ->
    {error, division_by_zero};
divide(A, B) ->
    {ok, A / B}.

-spec safe_divide(float(), float()) -> float().
safe_divide(A, B) ->
    case divide(A, B) of
        {ok, Result} -> Result;
        {error, _} -> 0.0
    end.
```

**Why this translation:**
- Roc Result type maps to `{ok, Value}` / `{error, Reason}`
- Pattern matching on result works like case
- `Result.withDefault` becomes case with fallback
- Error tags become atoms

### Pattern 7: Optional Values

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

**Erlang:**
```erlang
-spec find_user(non_neg_integer(), [user()]) -> user() | undefined.
find_user(Id, Users) ->
    case lists:keyfind(Id, #user.id, Users) of
        #user{} = User -> User;
        false -> undefined
    end.

-spec get_email(user() | undefined) -> string().
get_email(undefined) ->
    "no email";
get_email(#user{email=Email}) ->
    Email.
```

**Why this translation:**
- Roc None maps to Erlang `undefined` atom
- Some(value) becomes the value directly
- Pattern matching on undefined is explicit
- Alternatively use `{ok, Value}` / `error` pattern

### Pattern 8: List Operations

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

**Erlang:**
```erlang
-spec squares([integer()]) -> [integer()].
squares(List) ->
    [X * X || X <- List].

-spec evens([integer()]) -> [integer()].
evens(List) ->
    [X || X <- List, X rem 2 == 0].

-spec pairs([A], [B]) -> [{A, B}].
pairs(List1, List2) ->
    [{X, Y} || X <- List1, Y <- List2].
```

**Why this translation:**
- Roc map/filter operations become list comprehensions
- List comprehensions are idiomatic in Erlang
- `joinMap` (flatMap) becomes nested comprehension
- More concise than explicit map/filter calls

---

## Concurrency Patterns

### Roc Task Model → Erlang Process Model

Roc has no built-in concurrency - it's platform-provided. Erlang's concurrency is core to the language via lightweight processes.

**Roc:**
```roc
# No processes - pure functions
processWork : Data -> Result
processWork = \data ->
    transform(data)

# Platform provides Tasks
doWork : Data -> Task Result []
doWork = \data ->
    Task.fromResult(processWork(data))

# Multiple concurrent tasks (platform-dependent)
doMultipleWork : List Data -> Task (List Result) []
doMultipleWork = \dataList ->
    dataList
    |> List.map(doWork)
    |> Task.sequence
```

**Erlang:**
```erlang
% Direct process spawning
process_work(Data) ->
    transform(Data).

do_work(Data) ->
    % Spawn process to do work
    Self = self(),
    spawn(fun() ->
        Result = process_work(Data),
        Self ! {result, Result}
    end),
    receive
        {result, Result} -> Result
    end.

% Multiple concurrent processes
do_multiple_work(DataList) ->
    Self = self(),
    % Spawn workers
    _Pids = [spawn(fun() ->
        Result = process_work(Data),
        Self ! {result, Result}
    end) || Data <- DataList],
    % Collect results
    [receive {result, R} -> R end || _ <- DataList].
```

**Why this approach:**
- Roc Tasks are abstracted by platform
- Erlang exposes processes directly
- spawn creates lightweight processes
- Message passing is explicit
- Erlang gives fine-grained control

### Platform Effects → OTP Behaviors

**Roc:**
```roc
# Hypothetical platform API
doWorkflow : Input -> Result Output [WorkerFailed, ValidationFailed]
doWorkflow = \input ->
    validated = validate!(input)
    processed = processData!(validated)
    saved = saveResult!(processed)
    Ok(saved)
```

**Erlang:**
```erlang
% gen_server for stateful workflow
-module(workflow_server).
-behaviour(gen_server).

-export([start_link/0, execute/1]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2,
         terminate/2, code_change/3]).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

execute(Input) ->
    gen_server:call(?MODULE, {execute, Input}).

init([]) ->
    {ok, #{}}.

handle_call({execute, Input}, _From, State) ->
    Result = do_workflow(Input),
    {reply, Result, State}.

do_workflow(Input) ->
    case validate(Input) of
        {ok, Validated} ->
            case process_data(Validated) of
                {ok, Processed} ->
                    save_result(Processed);
                {error, Reason} ->
                    {error, {worker_failed, Reason}}
            end;
        {error, Reason} ->
            {error, {validation_failed, Reason}}
    end.

% ... other callbacks
```

**Why this translation:**
- Roc platform Tasks become gen_server
- Error handling is explicit with tagged tuples
- Process provides lifecycle management
- Supervision can be added for fault tolerance

### Supervision → Explicit Supervision Trees

**Roc:**
```roc
# Platform handles process-level concerns
# Application code doesn't deal with supervision
```

**Erlang:**
```erlang
-module(my_supervisor).
-behaviour(supervisor).

-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    SupFlags = #{
        strategy => one_for_one,
        intensity => 5,
        period => 60
    },

    ChildSpecs = [
        #{
            id => worker1,
            start => {worker_module, start_link, []},
            restart => permanent,
            shutdown => 5000,
            type => worker,
            modules => [worker_module]
        }
    ],

    {ok, {SupFlags, ChildSpecs}}.
```

**Why this approach:**
- Roc platforms hide supervision
- Erlang exposes supervision trees
- Design supervision hierarchy explicitly
- Configure restart strategies
- Implement "let it crash" philosophy

---

## Error Handling

### Result Types → Let It Crash + Tagged Tuples

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

**Erlang Philosophy:**
```erlang
% Let it crash - supervisor will restart
process_data(Data) ->
    Validated = validate(Data),      % May crash
    Transformed = transform(Validated),     % May crash
    save(Transformed).         % May crash

% Or use tagged tuples for recoverable errors
process_data_safe(Data) ->
    case validate(Data) of
        {ok, Validated} ->
            case transform(Validated) of
                {ok, Transformed} ->
                    save(Transformed);
                {error, Reason} ->
                    {error, {transform_error, Reason}}
            end;
        {error, Reason} ->
            {error, {validation_error, Reason}}
    end.
```

**Key Differences:**
- Roc: Explicit error propagation via Result
- Erlang: Let it crash OR explicit error tuples
- Roc: Fault tolerance via platform
- Erlang: Fault tolerance via process isolation + supervisors

### Error Pattern Translation

| Roc Pattern | Erlang Pattern | Notes |
|-------------|----------------|-------|
| `Err(error)` | `{error, Reason}` or crash | Choose based on recoverability |
| `Ok(value)` | `{ok, Value}` | Standard success pattern |
| `Result.try` (!) | `case` or crash | Chain error handling |
| Tag unions for errors | Atoms or tagged tuples | Multiple error types |
| Platform retry | Explicit retry or supervisor restart | No automatic retry |

---

## Module System

### Roc Interface → Erlang Module

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

**Erlang:**
```erlang
-module(calculator).
-export([add/2, subtract/2]).
-export_type([result/0]).

-type result() :: {ok, float()} | {error, invalid_input}.

-spec add(float(), float()) -> result().
add(A, B) -> {ok, A + B}.

-spec subtract(float(), float()) -> result().
subtract(A, B) -> {ok, A - B}.
```

**Why this translation:**
- `interface` becomes `-module`
- `exposes` becomes `-export`
- Type exports use `-export_type`
- Type definitions use `-type`
- Specs provide type signatures

### Application Structure

**Roc Application:**
```
my-app/
├── main.roc          # Entry point
├── Worker.roc        # Worker module
└── Types.roc         # Shared types
```

**Erlang OTP Application:**
```
my_app/
├── src/
│   ├── my_app.app.src    # Application resource file
│   ├── my_app_app.erl    # Application behavior
│   ├── my_app_sup.erl    # Top-level supervisor
│   └── my_worker.erl     # Worker gen_server
├── include/
│   └── my_app.hrl        # Header files
└── rebar.config          # Build configuration
```

**Key Differences:**
- Roc: Single entry point
- Erlang: Application behavior + supervisor tree
- Roc: Platform provides I/O
- Erlang: OTP behaviors structure application
- Erlang adds supervision hierarchy

---

## Platform Architecture

### Roc Application + Platform → OTP Application

**Roc:**
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

**Erlang:**
```erlang
% my_app.app.src
{application, my_app, [
    {description, "My Application"},
    {vsn, "1.0.0"},
    {registered, []},
    {mod, {my_app_app, []}},
    {applications, [kernel, stdlib]},
    {env, []}
]}.

% my_app_app.erl
-module(my_app_app).
-behaviour(application).

-export([start/2, stop/1]).

start(_Type, _Args) ->
    io:format("Hello, World!~n"),
    my_app_sup:start_link().

stop(_State) ->
    ok.

% my_app_sup.erl
-module(my_app_sup).
-behaviour(supervisor).

-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    SupFlags = #{strategy => one_for_one, intensity => 5, period => 60},
    ChildSpecs = [],
    {ok, {SupFlags, ChildSpecs}}.
```

**Why this approach:**
- Roc separates platform from application
- Erlang uses application behavior
- OTP requires supervisor even if empty
- Application file defines metadata
- Erlang exposes more lifecycle control

---

## Testing Strategy

### Roc expect → EUnit

**Roc:**
```roc
add : I64, I64 -> I64
add = \a, b -> a + b

expect add(2, 3) == 5
expect add(0, 0) == 0
expect add(-1, 1) == 0

expect
    result = add(2, 3)
    result == 5
```

**Erlang:**
```erlang
-module(calculator_tests).
-include_lib("eunit/include/eunit.hrl").

add_test() ->
    ?assertEqual(5, calculator:add(2, 3)).

add_zero_test() ->
    ?assertEqual(0, calculator:add(0, 0)).

add_negative_test() ->
    ?assertEqual(0, calculator:add(-1, 1)).

add_complex_test() ->
    Result = calculator:add(2, 3),
    ?assertEqual(5, Result).
```

**Why this translation:**
- Roc inline expects become EUnit test functions
- Test function names end with `_test`
- `?assertEqual` provides assertion
- Tests run with `rebar3 eunit`

---

## Common Pitfalls

1. **Trying to keep everything pure**: Erlang embraces processes and side effects. Don't avoid them.

2. **Not using OTP behaviors**: Raw processes are harder to supervise. Use gen_server, gen_statem, supervisor.

3. **Ignoring dynamic typing**: Erlang is dynamically typed. Use specs and dialyzer, but don't expect compile-time type safety.

4. **Over-engineering for fault tolerance**: Not everything needs to be a process. Pure functions can stay functions.

5. **Translating Result chains literally**: Erlang's error handling is often simpler with let-it-crash. Only use explicit error handling when recovery is possible.

6. **Forgetting about distribution**: Erlang makes distribution easy. Consider whether your application should be distributed.

7. **Not thinking about hot code reload**: Erlang supports hot code reloading. Design with code_change in mind.

8. **Assuming immutability everywhere**: While Erlang data is immutable, process state is mutable via message passing.

9. **Missing the message passing idiom**: Don't just call functions - think about message protocols between processes.

10. **Not using ETS for shared state**: For shared read-heavy state, ETS is more efficient than message passing.

---

## Tooling

| Purpose | Roc | Erlang | Notes |
|---------|-----|--------|-------|
| Build tool | `roc` CLI | rebar3 | Erlang has mature build ecosystem |
| Package manager | Platform URLs | hex.pm + rebar3 | Hex is standard package registry |
| Testing | `roc test` | EUnit, CT, PropEr | Multiple testing frameworks |
| REPL | - | `erl` shell | Interactive development |
| Formatter | `roc format` | erlfmt, rebar3 fmt | Multiple formatters available |
| Documentation | Comments | EDoc | Generate HTML docs |
| Debugger | - | debugger, observer | GUI debugging tools |
| Profiling | - | fprof, eprof | Multiple profiling tools |
| Static analysis | Type system | dialyzer | Gradual typing via specs |
| Release building | Platform | relx (via rebar3) | Production releases |

---

## Examples

### Example 1: Simple - Pure Function Translation

**Before (Roc):**
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

**After (Erlang):**
```erlang
-module(color).
-export([to_string/1]).

-type color() :: red | green | blue | {rgb, byte(), byte(), byte()}.

-spec to_string(color()) -> string().
to_string(red) -> "Red";
to_string(green) -> "Green";
to_string(blue) -> "Blue";
to_string({rgb, R, G, B}) ->
    io_lib:format("RGB(~p, ~p, ~p)", [R, G, B]).
```

### Example 2: Medium - State Machine with Error Handling

**Before (Roc):**
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

**After (Erlang):**
```erlang
-module(bank_account).
-behaviour(gen_server).

%% API
-export([start_link/0, deposit/1, withdraw/1, balance/0]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, handle_info/2,
         terminate/2, code_change/3]).

-record(state, {
    balance = 0 :: non_neg_integer()
}).

%%% API

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

deposit(Amount) ->
    gen_server:call(?MODULE, {deposit, Amount}).

withdraw(Amount) ->
    gen_server:call(?MODULE, {withdraw, Amount}).

balance() ->
    gen_server:call(?MODULE, balance).

%%% gen_server callbacks

init([]) ->
    {ok, #state{}}.

handle_call({deposit, Amount}, _From, State) when Amount > 0 ->
    NewState = State#state{balance = State#state.balance + Amount},
    {reply, {ok, NewState#state.balance}, NewState};
handle_call({deposit, _}, _From, State) ->
    {reply, {error, invalid_amount}, State};

handle_call({withdraw, Amount}, _From, State) when Amount =< 0 ->
    {reply, {error, invalid_amount}, State};
handle_call({withdraw, Amount}, _From, State) when Amount > State#state.balance ->
    {reply, {error, insufficient_funds}, State};
handle_call({withdraw, Amount}, _From, State) ->
    NewState = State#state{balance = State#state.balance - Amount},
    {reply, {ok, NewState#state.balance}, NewState};

handle_call(balance, _From, State) ->
    {reply, State#state.balance, State}.

handle_cast(_Msg, State) ->
    {noreply, State}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.
```

### Example 3: Complex - Pure State Machine to Full OTP Application

**Before (Roc):**
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
```

**After (Erlang):**
```erlang
%% task_queue.erl - gen_server implementation
-module(task_queue).
-behaviour(gen_server).

%% API
-export([start_link/0, add_task/1, get_next/0, count/0, stop/0]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, handle_info/2,
         terminate/2, code_change/3]).

-record(state, {
    tasks = [] :: [term()],
    processed = 0 :: non_neg_integer()
}).

%%% API Functions

-spec start_link() -> {ok, pid()} | {error, term()}.
start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

-spec add_task(term()) -> ok.
add_task(Task) ->
    gen_server:cast(?MODULE, {add, Task}).

-spec get_next() -> {ok, term()} | {error, empty}.
get_next() ->
    gen_server:call(?MODULE, get_next).

-spec count() -> #{pending => non_neg_integer(), processed => non_neg_integer()}.
count() ->
    gen_server:call(?MODULE, count).

-spec stop() -> ok.
stop() ->
    gen_server:stop(?MODULE).

%%% gen_server Callbacks

init([]) ->
    {ok, #state{}}.

handle_call(get_next, _From, #state{tasks = []} = State) ->
    {reply, {error, empty}, State};
handle_call(get_next, _From, #state{tasks = [First | Rest], processed = P} = State) ->
    NewState = State#state{
        tasks = Rest,
        processed = P + 1
    },
    {reply, {ok, First}, NewState};

handle_call(count, _From, #state{tasks = Tasks, processed = P} = State) ->
    Result = #{
        pending => length(Tasks),
        processed => P
    },
    {reply, Result, State}.

handle_cast({add, Task}, #state{tasks = Tasks} = State) ->
    NewState = State#state{tasks = Tasks ++ [Task]},
    {noreply, NewState};
handle_cast(_Msg, State) ->
    {noreply, State}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

%% task_queue_sup.erl - Supervisor
-module(task_queue_sup).
-behaviour(supervisor).

-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    SupFlags = #{
        strategy => one_for_one,
        intensity => 5,
        period => 60
    },

    ChildSpecs = [
        #{
            id => task_queue,
            start => {task_queue, start_link, []},
            restart => permanent,
            shutdown => 5000,
            type => worker,
            modules => [task_queue]
        }
    ],

    {ok, {SupFlags, ChildSpecs}}.

%% task_queue_app.erl - Application
-module(task_queue_app).
-behaviour(application).

-export([start/2, stop/1]).

start(_Type, _Args) ->
    task_queue_sup:start_link().

stop(_State) ->
    ok.
```

---

## Limitations

### Areas Where Direct Translation Is Difficult

1. **Static Type Safety**: Roc's compile-time type checking doesn't exist in Erlang. Use specs and dialyzer for gradual typing.

2. **Platform Abstraction**: Roc platforms hide implementation details. In Erlang, you must design process architecture explicitly.

3. **Pure Functional Guarantees**: Roc guarantees purity. Erlang processes have side effects - embrace it.

4. **Zero-Cost Abstractions**: Roc compiles to native code. Erlang runs on BEAM VM with different performance characteristics.

5. **Automatic Memory Management**: Roc has predictable memory, Erlang uses per-process GC.

### Working Around Limitations

- **Instead of static types**: Use comprehensive specs and run dialyzer regularly
- **Instead of platform abstraction**: Design OTP application structure explicitly
- **Instead of purity**: Use processes for effects, keep business logic pure where practical
- **Instead of native performance**: Leverage Erlang's concurrency for throughput
- **Instead of predictable memory**: Design for process isolation and let GC handle each process

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-erlang-roc` - Reverse conversion (Erlang → Roc)
- `lang-roc-dev` - Roc development patterns and platform model
- `lang-erlang-dev` - Erlang development patterns and OTP

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Pure functions vs actors vs tasks across languages
- `patterns-serialization-dev` - Encoding/decoding across languages
- `patterns-metaprogramming-dev` - Compile-time vs runtime code generation
