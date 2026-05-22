---
name: convert-elm-erlang
description: Convert Elm code to idiomatic Erlang/OTP. Use when migrating Elm frontend applications to Erlang backend services, translating Elm patterns to OTP behaviors, or refactoring functional code to BEAM VM. Extends meta-convert-dev with Elm-to-Erlang specific patterns.
---

# Convert Elm to Erlang

Convert Elm code to idiomatic Erlang/OTP. This skill extends `meta-convert-dev` with Elm-to-Erlang specific type mappings, idiom translations, and architectural patterns for moving from pure functional frontend code to fault-tolerant backend systems.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elm types → Erlang types (records, maps, atoms)
- **Idiom translations**: The Elm Architecture (TEA) → OTP behaviors (gen_server, gen_statem)
- **Error handling**: Elm Result/Maybe → Erlang tuples and let-it-crash
- **Concurrency**: Elm Cmd/Sub → Erlang processes and message passing
- **Architecture**: Pure functions → Supervised process trees

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Erlang language fundamentals - see `lang-erlang-dev`
- Reverse conversion (Erlang → Elm) - see `convert-erlang-elm`

---

## Quick Reference

| Elm | Erlang | Notes |
|-----|--------|-------|
| `String` | `binary()` or `list()` | Use binaries for efficiency |
| `Int` | `integer()` | Direct mapping |
| `Float` | `float()` | Direct mapping |
| `Bool` | `true` / `false` | Atoms in Erlang |
| `List a` | `[a]` | Direct mapping |
| `Maybe a` | `{ok, a}` / `undefined` / `error` | Tagged tuples |
| `Result e a` | `{ok, a}` / `{error, e}` | Standard Erlang convention |
| `type alias` | `-record()` or `map()` | Records for structure |
| `type Msg` | Message patterns | Process mailbox messages |
| `Model` | `gen_server` state | OTP state management |
| `update` function | `handle_call/cast` | OTP callbacks |
| `Cmd Msg` | `spawn` / `!` / `gen_server:call` | Process operations |
| `Sub Msg` | `receive` / timers | Message reception |

## When Converting Code

1. **Analyze Elm architecture** - Understand TEA structure (Model, View, Update, Subscriptions)
2. **Map to OTP behaviors** - Model → gen_server state, Msg → messages, update → handle_call/cast
3. **Preserve pure functions** - Keep business logic pure, wrap in processes
4. **Adopt OTP patterns** - Don't transliterate; use supervision trees and fault tolerance
5. **Handle guarantees** - Elm's no-runtime-errors → Erlang's let-it-crash
6. **Test equivalence** - Property-based testing for both languages

---

## Type System Mapping

### Primitive Types

| Elm | Erlang | Notes |
|-----|--------|-------|
| `String` | `binary()` | UTF-8 binary: `<<"Hello">>` |
| `String` | `string()` | List of codepoints: `"Hello"` (less efficient) |
| `Int` | `integer()` | Arbitrary precision |
| `Float` | `float()` | IEEE 754 double precision |
| `Bool` | `true` / `false` | Atoms, not a separate type |
| `Char` | `integer()` | Unicode codepoint |
| `()` (unit) | `ok` / `undefined` | Atom for no value |

### Collection Types

| Elm | Erlang | Notes |
|-----|--------|-------|
| `List a` | `[a]` | Linked list |
| `Array a` | `array:array(a)` | Fixed-size arrays (rare) |
| `Dict k v` | `maps:map(k, v)` | Modern maps (Erlang 17+) |
| `Dict k v` | `dict:dict(k, v)` | Legacy dict module |
| `Set a` | `sets:set(a)` | Set data structure |
| `(a, b)` | `{a, b}` | Tuple (fixed size) |
| `(a, b, c)` | `{a, b, c}` | Tuple with 3+ elements |

### Composite Types

| Elm | Erlang | Notes |
|-----|--------|-------|
| `type alias User = { name : String, age : Int }` | `-record(user, {name :: binary(), age :: integer()}).` | Record with type specs |
| `type alias User = { name : String, age : Int }` | `#{name => binary(), age => integer()}` | Map (more flexible) |
| `type Msg = Increment \| Decrement` | Message patterns in receive | Patterns, not types |
| `type Result e a = Ok a \| Err e` | `{ok, a} \| {error, e}` | Tagged tuples |
| `type Maybe a = Just a \| Nothing` | `{ok, a} \| undefined \| {error, not_found}` | Multiple conventions |

### Union Types → Pattern Matching

**Elm:**
```elm
type TrafficLight
    = Red
    | Yellow
    | Green

canGo : TrafficLight -> Bool
canGo light =
    case light of
        Green -> True
        Yellow -> False
        Red -> False
```

**Erlang:**
```erlang
% Define as atoms or tagged tuples
can_go(green) -> true;
can_go(yellow) -> false;
can_go(red) -> false.

% Or with more structure
can_go(Light) ->
    case Light of
        green -> true;
        yellow -> false;
        red -> false
    end.
```

**Why this translation:**
- Elm's union types become atoms or tagged tuples in Erlang
- Pattern matching in function heads is idiomatic in both languages
- Erlang doesn't enforce exhaustiveness at compile time (use dialyzer)

---

## Idiom Translation

### Pattern 1: The Elm Architecture → gen_server

**Elm:**
```elm
type alias Model = { count : Int }

type Msg
    = Increment
    | Decrement

init : () -> ( Model, Cmd Msg )
init _ = ( { count = 0 }, Cmd.none )

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment -> ( { model | count = model.count + 1 }, Cmd.none )
        Decrement -> ( { model | count = model.count - 1 }, Cmd.none )
```

**Erlang:**
```erlang
-module(counter).
-behaviour(gen_server).

-export([start_link/0, increment/0, decrement/0, get_count/0]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

-record(state, {count = 0 :: integer()}).

%%% API
start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

increment() ->
    gen_server:cast(?MODULE, increment).

decrement() ->
    gen_server:cast(?MODULE, decrement).

get_count() ->
    gen_server:call(?MODULE, get_count).

%%% Callbacks
init([]) ->
    {ok, #state{count = 0}}.

handle_call(get_count, _From, State) ->
    {reply, State#state.count, State}.

handle_cast(increment, State = #state{count = Count}) ->
    {noreply, State#state{count = Count + 1}};
handle_cast(decrement, State = #state{count = Count}) ->
    {noreply, State#state{count = Count - 1}}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.
```

**Why this translation:**
- Elm's Model → gen_server state record
- Elm's Msg type → message patterns in handle_cast/handle_call
- Elm's update function → handle_cast/handle_call callbacks
- Elm's init → gen_server init/1 callback
- gen_server provides supervision, hot code reloading, and OTP integration

### Pattern 2: Maybe/Result → Tagged Tuples

**Elm:**
```elm
findUser : Int -> Maybe User
findUser id =
    if id == 1 then
        Just { name = "Alice", age = 30 }
    else
        Nothing

name : String
name =
    findUser 1
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"
```

**Erlang:**
```erlang
find_user(Id) ->
    case Id of
        1 -> {ok, #{name => <<"Alice">>, age => 30}};
        _ -> {error, not_found}
    end.

% Using case for pattern matching
get_name() ->
    case find_user(1) of
        {ok, User} -> maps:get(name, User);
        {error, _} -> <<"Anonymous">>
    end.

% Or with function clauses
get_name_clause({ok, User}) -> maps:get(name, User);
get_name_clause({error, _}) -> <<"Anonymous">>.
```

**Why this translation:**
- `Nothing` → `{error, Reason}` or `undefined`
- `Just value` → `{ok, Value}`
- Erlang convention: `{ok, Result}` for success, `{error, Reason}` for failure
- Pattern matching in case or function clauses replaces Maybe combinators

### Pattern 3: List Operations

**Elm:**
```elm
result : Int
result =
    [1, 2, 3, 4, 5]
        |> List.filter (\x -> x > 2)
        |> List.map (\x -> x * 2)
        |> List.foldl (+) 0
```

**Erlang:**
```erlang
result() ->
    lists:foldl(
        fun(X, Acc) -> X + Acc end,
        0,
        lists:map(
            fun(X) -> X * 2 end,
            lists:filter(
                fun(X) -> X > 2 end,
                [1, 2, 3, 4, 5]
            )
        )
    ).

% Or with list comprehensions (more idiomatic)
result_comprehension() ->
    Sum = fun(List) -> lists:sum(List) end,
    Sum([X * 2 || X <- [1, 2, 3, 4, 5], X > 2]).
```

**Why this translation:**
- Elm's pipeline `|>` → nested function calls or list comprehensions
- List comprehensions are more idiomatic in Erlang for filter+map
- `lists:` module provides functional primitives

### Pattern 4: Record Updates

**Elm:**
```elm
type alias User = { name : String, age : Int, email : String }

user : User
user = { name = "Alice", age = 30, email = "alice@example.com" }

updatedUser : User
updatedUser = { user | age = 31 }
```

**Erlang:**
```erlang
-record(user, {
    name :: binary(),
    age :: integer(),
    email :: binary()
}).

user() ->
    #user{name = <<"Alice">>, age = 30, email = <<"alice@example.com">>}.

updated_user() ->
    User = user(),
    User#user{age = 31}.

% Or with maps
user_map() ->
    #{name => <<"Alice">>, age => 30, email => <<"alice@example.com">>}.

updated_user_map() ->
    User = user_map(),
    User#{age := 31}.  % := for updating existing key
```

**Why this translation:**
- Elm records → Erlang records (compile-time) or maps (runtime)
- Records provide type checking with dialyzer
- Maps are more flexible but less type-safe

### Pattern 5: Cmd → Process Operations

**Elm:**
```elm
type Msg
    = GotUsers (Result Http.Error (List User))

getUsers : Cmd Msg
getUsers =
    Http.get
        { url = "https://api.example.com/users"
        , expect = Http.expectJson GotUsers usersDecoder
        }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | loading = True }, getUsers )

        GotUsers result ->
            case result of
                Ok users -> ( { model | users = users, loading = False }, Cmd.none )
                Err error -> ( { model | error = Just error, loading = False }, Cmd.none )
```

**Erlang:**
```erlang
-module(user_fetcher).
-behaviour(gen_server).

handle_cast(fetch_users, State) ->
    % Spawn async HTTP request
    Self = self(),
    spawn(fun() ->
        case httpc:request(get, {"https://api.example.com/users", []}, [], []) of
            {ok, {{_, 200, _}, _, Body}} ->
                Users = decode_users(Body),
                Self ! {users_fetched, {ok, Users}};
            {error, Reason} ->
                Self ! {users_fetched, {error, Reason}}
        end
    end),
    {noreply, State#{loading => true}}.

handle_info({users_fetched, {ok, Users}}, State) ->
    {noreply, State#{users => Users, loading => false, error => undefined}};
handle_info({users_fetched, {error, Reason}}, State) ->
    {noreply, State#{error => Reason, loading => false}}.
```

**Why this translation:**
- Elm's Cmd → spawn/spawn_link + message passing
- HTTP in Elm runtime → explicit httpc or third-party libraries (hackney, gun)
- Elm's managed effects → Erlang's explicit process control
- Error handling moves from Result type to message patterns

### Pattern 6: Sub → Timers and Receives

**Elm:**
```elm
subscriptions : Model -> Sub Msg
subscriptions model =
    Time.every 1000 Tick  -- Every second

type Msg
    = Tick Time.Posix
```

**Erlang:**
```erlang
init([]) ->
    % Set up recurring timer
    {ok, TRef} = timer:send_interval(1000, self(), tick),
    {ok, #{timer_ref => TRef}}.

handle_info(tick, State) ->
    % Handle timer tick
    NewState = do_periodic_work(State),
    {noreply, NewState};
handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, #{timer_ref := TRef}) ->
    timer:cancel(TRef),
    ok.
```

**Why this translation:**
- Elm's Time.every → timer:send_interval
- Sub message → handle_info callback
- Cleanup handled in terminate/2

---

## Error Handling

### Elm's Guarantees → Erlang's Let-It-Crash

**Elm Approach (No Runtime Errors):**
```elm
-- Elm: Everything must be handled at compile time
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
```

**Erlang Approach (Let It Crash):**
```erlang
% Erlang: Let supervisor restart on invalid input
parse_age(Str) ->
    Age = list_to_integer(Str),  % Crashes on invalid input
    true = Age >= 0,              % Crashes if negative
    Age.

% Or with explicit error handling when needed
parse_age_safe(Str) ->
    try list_to_integer(Str) of
        Age when Age >= 0 -> {ok, Age};
        Age -> {error, {negative_age, Age}}
    catch
        error:badarg -> {error, not_a_number}
    end.
```

**Translation Strategy:**
- Elm's Result → `{ok, Value}` / `{error, Reason}` for APIs
- Elm's Maybe → `{ok, Value}` / `undefined` / `{error, not_found}`
- Critical paths: explicit error tuples
- Internal functions: let it crash, supervisor restarts
- Supervision tree ensures fault tolerance

### Elm Result Chains → Erlang Error Tuples

**Elm:**
```elm
processUser : String -> Result String ProcessedUser
processUser input =
    parseJson input
        |> Result.andThen validateUser
        |> Result.andThen enrichUser
        |> Result.map processUser
```

**Erlang:**
```erlang
process_user(Input) ->
    case parse_json(Input) of
        {ok, Json} ->
            case validate_user(Json) of
                {ok, User} ->
                    case enrich_user(User) of
                        {ok, Enriched} ->
                            {ok, process_user_data(Enriched)};
                        {error, Reason} -> {error, Reason}
                    end;
                {error, Reason} -> {error, Reason}
            end;
        {error, Reason} -> {error, Reason}
    end.

% Or with helper for chaining
chain(Value, []) -> {ok, Value};
chain({ok, Value}, [F | Rest]) ->
    chain(F(Value), Rest);
chain({error, Reason}, _) ->
    {error, Reason}.

process_user_chain(Input) ->
    chain(parse_json(Input), [
        fun validate_user/1,
        fun enrich_user/1,
        fun(U) -> {ok, process_user_data(U)} end
    ]).
```

---

## Concurrency Patterns

### Elm Managed Effects → Erlang Explicit Processes

**Conceptual Mapping:**

| Elm Concept | Erlang Equivalent | Notes |
|-------------|-------------------|-------|
| Elm Runtime manages concurrency | You spawn and manage processes | Explicit control |
| Cmd.batch | Multiple spawn/cast calls | Parallel operations |
| Cmd.none | Don't spawn, synchronous | Stay in current process |
| update guaranteed sequential | gen_server callbacks sequential | OTP guarantees |
| Multiple Subs | Multiple receive patterns | Pattern match messages |

### Example: Concurrent HTTP Requests

**Elm:**
```elm
-- Runtime handles concurrency automatically
update msg model =
    case msg of
        FetchAll ->
            ( { model | loading = True }
            , Cmd.batch
                [ Http.get { url = "/api/users", expect = Http.expectJson GotUsers decoder }
                , Http.get { url = "/api/posts", expect = Http.expectJson GotPosts decoder }
                , Http.get { url = "/api/comments", expect = Http.expectJson GotComments decoder }
                ]
            )
```

**Erlang:**
```erlang
handle_cast(fetch_all, State) ->
    Self = self(),
    % Spawn three concurrent requests
    spawn_link(fun() -> fetch_and_send(Self, "/api/users", users) end),
    spawn_link(fun() -> fetch_and_send(Self, "/api/posts", posts) end),
    spawn_link(fun() -> fetch_and_send(Self, "/api/comments", comments) end),
    {noreply, State#{loading => true, pending => 3}}.

fetch_and_send(Parent, Url, Type) ->
    Result = httpc:request(get, {Url, []}, [], []),
    Parent ! {fetched, Type, Result}.

handle_info({fetched, Type, Result}, State = #{pending := Pending}) ->
    NewState = State#{Type => Result, pending => Pending - 1},
    case maps:get(pending, NewState) of
        0 -> {noreply, NewState#{loading => false}};
        _ -> {noreply, NewState}
    end.
```

---

## Architecture Translation

### TEA → OTP Application

**Elm Application Structure:**
```
src/
  Main.elm          -- Entry point (Browser.element)
  Types.elm         -- Shared types (Model, Msg)
  Api.elm           -- HTTP functions
  Page/
    Home.elm        -- Page modules
```

**Erlang/OTP Application Structure:**
```
src/
  myapp.app.src        -- Application metadata
  myapp_app.erl        -- Application behavior (entry point)
  myapp_sup.erl        -- Top-level supervisor
  myapp_server.erl     -- Main gen_server (Model + update)
  myapp_api.erl        -- HTTP client functions
  myapp_worker.erl     -- Worker processes
```

### Supervision Tree

**Elm:** Single runtime, no crashes
**Erlang:** Supervision tree for fault tolerance

```erlang
-module(myapp_sup).
-behaviour(supervisor).

init([]) ->
    SupFlags = #{
        strategy => one_for_one,
        intensity => 5,
        period => 60
    },
    ChildSpecs = [
        #{
            id => main_server,
            start => {myapp_server, start_link, []},
            restart => permanent,
            shutdown => 5000,
            type => worker
        },
        #{
            id => worker_pool_sup,
            start => {myapp_worker_sup, start_link, []},
            restart => permanent,
            shutdown => infinity,
            type => supervisor
        }
    ],
    {ok, {SupFlags, ChildSpecs}}.
```

---

## JSON Handling

### Elm Decoders → Erlang Parsing

**Elm:**
```elm
import Json.Decode as Decode exposing (Decoder)

type alias User = { name : String, age : Int, email : String }

userDecoder : Decoder User
userDecoder =
    Decode.map3 User
        (Decode.field "name" Decode.string)
        (Decode.field "age" Decode.int)
        (Decode.field "email" Decode.string)
```

**Erlang:**
```erlang
-record(user, {
    name :: binary(),
    age :: integer(),
    email :: binary()
}).

% Using jsone library
decode_user(Json) ->
    case jsone:decode(Json, [{object_format, map}]) of
        #{<<"name">> := Name, <<"age">> := Age, <<"email">> := Email} ->
            {ok, #user{name = Name, age = Age, email = Email}};
        _ ->
            {error, invalid_json}
    end.

% Or with jiffy
decode_user_jiffy(Json) ->
    {Props} = jiffy:decode(Json),
    Name = proplists:get_value(<<"name">>, Props),
    Age = proplists:get_value(<<"age">>, Props),
    Email = proplists:get_value(<<"email">>, Props),
    #user{name = Name, age = Age, email = Email}.
```

**Elm Encoders → Erlang Encoding:**

**Elm:**
```elm
import Json.Encode as Encode

encodeUser : User -> Encode.Value
encodeUser user =
    Encode.object
        [ ( "name", Encode.string user.name )
        , ( "age", Encode.int user.age )
        , ( "email", Encode.string user.email )
        ]
```

**Erlang:**
```erlang
encode_user(#user{name = Name, age = Age, email = Email}) ->
    jsone:encode(#{
        <<"name">> => Name,
        <<"age">> => Age,
        <<"email">> => Email
    }).
```

---

## Common Pitfalls

### 1. Assuming Compile-Time Safety

**Problem:** Elm catches all errors at compile time; Erlang relies on runtime checks and supervision.

**Elm:**
```elm
-- Compiler forces you to handle all cases
processResult : Result Error Value -> String
processResult result =
    case result of
        Ok value -> "Success"
        Err error -> "Failed"  -- MUST handle or won't compile
```

**Erlang:**
```erlang
% No compile-time exhaustiveness checking
process_result({ok, _Value}) -> "Success".
% Forgot {error, _} case → runtime crash (but supervisor restarts)
```

**Solution:** Use dialyzer for static analysis, embrace let-it-crash philosophy with supervision.

### 2. Misunderstanding String Types

**Problem:** Elm's String is always Unicode text; Erlang has both binaries and lists.

**Bad:**
```erlang
% Mixing strings and binaries
Name = "Alice",  % List of integers
Email = <<"alice@example.com">>,  % Binary
Combined = Name ++ Email.  % ERROR: can't concatenate list and binary
```

**Good:**
```erlang
% Be consistent: use binaries for text
Name = <<"Alice">>,
Email = <<"alice@example.com">>,
Combined = <<Name/binary, <<" - ">>/binary, Email/binary>>.
```

### 3. Over-Using Try-Catch

**Problem:** Translating Elm's explicit error handling to defensive try-catch everywhere.

**Bad:**
```erlang
% Over-defensive (not idiomatic Erlang)
process_data(Data) ->
    try
        Step1 = validate(Data),
        Step2 = transform(Step1),
        Step3 = save(Step2),
        {ok, Step3}
    catch
        _:_ -> {error, something_failed}
    end.
```

**Good:**
```erlang
% Let it crash in workers, handle errors at API boundaries
process_data(Data) ->
    Step1 = validate(Data),    % Crash if invalid
    Step2 = transform(Step1),  % Crash if transform fails
    save(Step2).               % Crash if save fails
    % Supervisor will restart this process if it crashes
```

### 4. Not Using OTP Behaviors

**Problem:** Writing raw process loops instead of using gen_server, gen_statem.

**Bad:**
```erlang
% Reimplementing gen_server
loop(State) ->
    receive
        {From, get} ->
            From ! {self(), State},
            loop(State);
        {From, set, NewState} ->
            From ! {self(), ok},
            loop(NewState)
    end.
```

**Good:**
```erlang
% Use OTP behaviors
-behaviour(gen_server).

handle_call(get, _From, State) ->
    {reply, State, State};
handle_call({set, NewState}, _From, _State) ->
    {reply, ok, NewState}.
```

### 5. Forgetting Binary Pattern Matching

**Problem:** Not using Erlang's powerful binary pattern matching for parsing.

**Elm (can't do this):**
```elm
-- Must use String functions
parseHeader : String -> Maybe Header
```

**Erlang (idiomatic):**
```erlang
% Binary pattern matching is idiomatic
parse_header(<<Type:8, Length:16, Rest/binary>>) ->
    <<Payload:Length/binary, Remaining/binary>> = Rest,
    {ok, {Type, Payload}, Remaining}.
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| `rebar3` | Build tool | Like Elm's build system |
| `dialyzer` | Static analysis | Catches type errors |
| `elvis` | Style checker | Code linting |
| `xref` | Cross-reference | Find unused functions |
| `eunit` | Unit testing | Like elm-test |
| `common_test` | Integration testing | Full test suites |
| `proper` | Property-based testing | Like elm-explorations/test |
| `jsone` / `jiffy` | JSON parsing | External libraries |
| `hackney` / `gun` | HTTP client | Like elm/http |

---

## Examples

### Example 1: Simple - Counter

**Elm:**
```elm
type alias Model = { count : Int }

type Msg = Increment | Decrement | Reset

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment -> ( { model | count = model.count + 1 }, Cmd.none )
        Decrement -> ( { model | count = model.count - 1 }, Cmd.none )
        Reset -> ( { count = 0 }, Cmd.none )
```

**Erlang:**
```erlang
-module(counter).
-behaviour(gen_server).
-export([start_link/0, increment/0, decrement/0, reset/0, get/0]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

increment() -> gen_server:cast(?MODULE, increment).
decrement() -> gen_server:cast(?MODULE, decrement).
reset() -> gen_server:cast(?MODULE, reset).
get() -> gen_server:call(?MODULE, get).

init([]) ->
    {ok, 0}.

handle_call(get, _From, Count) ->
    {reply, Count, Count}.

handle_cast(increment, Count) ->
    {noreply, Count + 1};
handle_cast(decrement, Count) ->
    {noreply, Count - 1};
handle_cast(reset, _Count) ->
    {noreply, 0}.

handle_info(_Info, State) -> {noreply, State}.
terminate(_Reason, _State) -> ok.
code_change(_Old, State, _Extra) -> {ok, State}.
```

### Example 2: Medium - User Management

**Elm:**
```elm
type alias User = { id : Int, name : String, email : String }

type Msg
    = FetchUsers
    | GotUsers (Result Http.Error (List User))
    | DeleteUser Int
    | UserDeleted (Result Http.Error ())

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | loading = True }, fetchUsers )

        GotUsers result ->
            case result of
                Ok users -> ( { model | users = users, loading = False }, Cmd.none )
                Err error -> ( { model | error = Just error, loading = False }, Cmd.none )

        DeleteUser id ->
            ( model, deleteUser id )

        UserDeleted result ->
            case result of
                Ok _ -> ( model, fetchUsers )
                Err error -> ( { model | error = Just error }, Cmd.none )
```

**Erlang:**
```erlang
-module(user_manager).
-behaviour(gen_server).

-record(state, {
    users = [] :: [map()],
    loading = false :: boolean(),
    error = undefined :: undefined | binary()
}).

%% API
-export([start_link/0, fetch_users/0, delete_user/1]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

fetch_users() ->
    gen_server:cast(?MODULE, fetch_users).

delete_user(Id) ->
    gen_server:cast(?MODULE, {delete_user, Id}).

init([]) ->
    {ok, #state{}}.

handle_cast(fetch_users, State) ->
    Self = self(),
    spawn_link(fun() ->
        Result = fetch_users_http(),
        Self ! {users_fetched, Result}
    end),
    {noreply, State#state{loading = true}};

handle_cast({delete_user, Id}, State) ->
    Self = self(),
    spawn_link(fun() ->
        Result = delete_user_http(Id),
        Self ! {user_deleted, Result}
    end),
    {noreply, State}.

handle_info({users_fetched, {ok, Users}}, State) ->
    {noreply, State#state{users = Users, loading = false, error = undefined}};
handle_info({users_fetched, {error, Reason}}, State) ->
    {noreply, State#state{loading = false, error = format_error(Reason)}};

handle_info({user_deleted, {ok, _}}, State) ->
    % Refetch users after deletion
    gen_server:cast(self(), fetch_users),
    {noreply, State};
handle_info({user_deleted, {error, Reason}}, State) ->
    {noreply, State#state{error = format_error(Reason)}}.

handle_call(_Request, _From, State) ->
    {reply, ok, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

%% Internal functions
fetch_users_http() ->
    case httpc:request(get, {"https://api.example.com/users", []}, [], []) of
        {ok, {{_, 200, _}, _, Body}} ->
            {ok, jsone:decode(Body, [{object_format, map}])};
        {error, Reason} ->
            {error, Reason}
    end.

delete_user_http(Id) ->
    Url = "https://api.example.com/users/" ++ integer_to_list(Id),
    case httpc:request(delete, {Url, []}, [], []) of
        {ok, {{_, 204, _}, _, _}} ->
            {ok, deleted};
        {error, Reason} ->
            {error, Reason}
    end.

format_error(Reason) ->
    list_to_binary(io_lib:format("~p", [Reason])).
```

### Example 3: Complex - State Machine with Timers

**Elm:**
```elm
type State
    = Idle
    | Running { startTime : Time.Posix, elapsed : Float }
    | Paused { elapsed : Float }

type Msg
    = Start
    | Stop
    | Pause
    | Tick Time.Posix

update : Msg -> State -> ( State, Cmd Msg )
update msg state =
    case ( msg, state ) of
        ( Start, Idle ) ->
            ( Running { startTime = Time.millisToPosix 0, elapsed = 0 }, Cmd.none )

        ( Stop, Running _ ) ->
            ( Idle, Cmd.none )

        ( Stop, Paused _ ) ->
            ( Idle, Cmd.none )

        ( Pause, Running { elapsed } ) ->
            ( Paused { elapsed = elapsed }, Cmd.none )

        ( Start, Paused { elapsed } ) ->
            ( Running { startTime = Time.millisToPosix 0, elapsed = elapsed }, Cmd.none )

        ( Tick now, Running { startTime, elapsed } ) ->
            let
                delta = Time.posixToMillis now - Time.posixToMillis startTime
            in
            ( Running { startTime = now, elapsed = elapsed + toFloat delta / 1000 }, Cmd.none )

        _ ->
            ( state, Cmd.none )

subscriptions : State -> Sub Msg
subscriptions state =
    case state of
        Running _ ->
            Time.every 100 Tick

        _ ->
            Sub.none
```

**Erlang:**
```erlang
-module(stopwatch).
-behaviour(gen_statem).

-export([start_link/0, start/0, stop/0, pause/0, get_elapsed/0]).
-export([init/1, callback_mode/0, idle/3, running/3, paused/3, terminate/3]).

-record(data, {
    start_time = undefined :: undefined | integer(),
    elapsed = 0 :: float(),
    timer_ref = undefined :: undefined | reference()
}).

%% API
start_link() ->
    gen_statem:start_link({local, ?MODULE}, ?MODULE, [], []).

start() -> gen_statem:cast(?MODULE, start).
stop() -> gen_statem:cast(?MODULE, stop).
pause() -> gen_statem:cast(?MODULE, pause).
get_elapsed() -> gen_statem:call(?MODULE, get_elapsed).

%% Callbacks
callback_mode() -> state_functions.

init([]) ->
    {ok, idle, #data{}}.

%% State: idle
idle(cast, start, Data) ->
    {ok, TRef} = timer:send_interval(100, tick),
    {next_state, running, Data#data{
        start_time = erlang:monotonic_time(millisecond),
        elapsed = 0,
        timer_ref = TRef
    }};
idle({call, From}, get_elapsed, Data) ->
    {keep_state, Data, [{reply, From, 0}]};
idle(_EventType, _Event, Data) ->
    {keep_state, Data}.

%% State: running
running(cast, stop, Data = #data{timer_ref = TRef}) ->
    timer:cancel(TRef),
    {next_state, idle, #data{}};
running(cast, pause, Data = #data{timer_ref = TRef, elapsed = Elapsed}) ->
    timer:cancel(TRef),
    {next_state, paused, Data#data{timer_ref = undefined}};
running(info, tick, Data = #data{start_time = StartTime, elapsed = Elapsed}) ->
    Now = erlang:monotonic_time(millisecond),
    Delta = (Now - StartTime) / 1000.0,
    {keep_state, Data#data{
        start_time = Now,
        elapsed = Elapsed + Delta
    }};
running({call, From}, get_elapsed, Data = #data{elapsed = Elapsed}) ->
    {keep_state, Data, [{reply, From, Elapsed}]};
running(_EventType, _Event, Data) ->
    {keep_state, Data}.

%% State: paused
paused(cast, start, Data = #data{elapsed = Elapsed}) ->
    {ok, TRef} = timer:send_interval(100, tick),
    {next_state, running, Data#data{
        start_time = erlang:monotonic_time(millisecond),
        timer_ref = TRef
    }};
paused(cast, stop, _Data) ->
    {next_state, idle, #data{}};
paused({call, From}, get_elapsed, Data = #data{elapsed = Elapsed}) ->
    {keep_state, Data, [{reply, From, Elapsed}]};
paused(_EventType, _Event, Data) ->
    {keep_state, Data}.

terminate(_Reason, _State, #data{timer_ref = TRef}) when TRef =/= undefined ->
    timer:cancel(TRef),
    ok;
terminate(_Reason, _State, _Data) ->
    ok.
```

---

## See Also

- `meta-convert-dev` - Foundational conversion patterns with cross-language examples
- `lang-elm-dev` - Elm development patterns and The Elm Architecture
- `lang-erlang-dev` - Erlang/OTP fundamentals, processes, and behaviors
- `patterns-concurrency-dev` - Concurrency patterns across languages (Cmd/Sub vs processes)
- `patterns-serialization-dev` - JSON handling across languages (decoders vs parsing)
- `patterns-metaprogramming-dev` - Compile-time vs runtime code generation
