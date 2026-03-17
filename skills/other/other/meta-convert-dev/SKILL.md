---
name: meta-convert-dev
description: Create language conversion skills for translating code from language A to language B. Use when building 'convert-X-Y' skills, designing type mappings between languages, establishing idiom translation patterns, or defining conversion methodologies. Provides foundational patterns that specific conversion skills extend.
---

# Language Conversion Skill Development

Foundational patterns for creating one-way language conversion skills. This meta-skill guides the creation of `convert-X-Y` skills (e.g., `convert-typescript-rust`, `convert-python-golang`) that assist in translating/refactoring code from a source language to a target language.

## When to Use This Skill

- Creating a new `convert-X-Y` skill for language translation
- Designing type system mappings between languages
- Establishing idiom translation strategies
- Defining conversion workflows and validation approaches
- Building tooling recommendations for transpilation

## This Skill Does NOT Cover

- Actual code conversion (use specific `convert-X-Y` skills or `meta-convert-guide`)
- Language tutorials (see `lang-*-dev` skills)
- Bidirectional translation (each direction is a separate skill)
- Runtime interop/FFI (see language-specific interop skills)

## Related Skills

- `meta-convert-guide` - Patterns and strategies for performing conversions
- `convert-*` skills - Language-pair specific conversion skills

---

## Existing Conversion Skills

For concrete, language-pair-specific examples, see these skills:

| Skill | Description |
|-------|-------------|
| `convert-typescript-rust` | TypeScript → Rust (GC → ownership, exceptions → Result) |
| `convert-typescript-python` | TypeScript → Python (static → dynamic typing) |
| `convert-typescript-golang` | TypeScript → Go (OOP → simplicity, Promise → goroutine) |
| `convert-golang-rust` | Go → Rust (GC → ownership, interface → trait) |
| `convert-python-rust` | Python → Rust (dynamic → static, GC → ownership) |
| `convert-python-fsharp` | Python → F# (dynamic → static, OOP → functional) |
| `convert-python-erlang` | Python → Erlang (single-threaded → BEAM actors) |
| `convert-python-clojure` | Python → Clojure (imperative → functional, OOP → data-oriented) |
| `convert-clojure-roc` | Clojure → Roc (JVM → native, dynamic → static) |
| `convert-clojure-elixir` | Clojure → Elixir (JVM → BEAM, STM → actors) |
| `convert-clojure-haskell` | Clojure → Haskell (dynamic → static, practical → pure) |

**Note:** This list may not be complete. Search `components/skills/convert-*` for all available conversion skills.

### Skill Categories

| Category | Examples | Key Challenges |
|----------|----------|----------------|
| **Static → Static** | TypeScript→Go, Rust→Go | Type system mapping, idiom differences |
| **Dynamic → Static** | Python→Rust, Clojure→Haskell | Add types, handle runtime flexibility |
| **Static → Dynamic** | TypeScript→Python, Go→Elixir | Remove type annotations, embrace flexibility |
| **Dynamic → Dynamic** | Python→Clojure, Clojure→Elixir | Paradigm and runtime differences |
| **OOP → Functional** | Java→Clojure, Python→Haskell | Replace classes with data+functions |
| **Functional → Functional** | Clojure→Elixir, Haskell→Scala | FP dialect differences |
| **GC → Ownership** | Any→Rust | Add explicit lifetimes and borrowing |
| **Platform Migration** | JVM→BEAM, JVM→Native | Runtime semantics, library ecosystem |

When creating a new conversion skill, refer to the specific `convert-X-Y` skills for production-ready examples.

### Platform Ecosystem Considerations

When converting between languages on different platforms (JVM, BEAM, .NET, Native), consider:

| Platform | Key Characteristics |
|----------|---------------------|
| **JVM** | Bytecode, JIT, GC, thread-based concurrency, rich stdlib |
| **BEAM** | Lightweight processes, preemptive scheduling, fault tolerance, hot reload |
| **.NET** | Similar to JVM, async/await primitives, strong Windows integration |
| **Native** | Direct compilation, manual/ownership memory, no runtime overhead |
| **Scripting** | Interpreted/JIT, dynamic typing, GIL (Python) |

**See:** [Platform Ecosystem Reference](references/platform-ecosystem.md) for detailed runtime characteristics, stdlib mapping strategies, transpiler options, and FFI considerations.

### Paradigm Translation Patterns

Cross-paradigm conversions require mental model shifts:

| Source → Target | Key Transformation |
|-----------------|-------------------|
| **OOP → FP** | Classes → data + functions, mutation → immutable updates |
| **Imperative → Declarative** | Loops → higher-order functions, statements → expressions |
| **Dynamic → Static** | Add type annotations, handle runtime flexibility statically |
| **Mutable-first → Immutable-first** | State threading, persistent data structures |

**See:** [Paradigm Translation Reference](references/paradigm-translation.md) for detailed patterns and examples.

### Additional Reference Materials

| Topic | Reference File |
|-------|---------------|
| **Numeric edge cases** | [references/numeric-edge-cases.md](references/numeric-edge-cases.md) - Overflow handling, division semantics, float precision |
| **Stdlib mapping** | [references/stdlib-mapping.md](references/stdlib-mapping.md) - Finding equivalent functions across languages |
| **Build systems** | [references/build-system-mapping.md](references/build-system-mapping.md) - Package managers and project structure |
| **Module systems** | [references/module-system-comparison.md](references/module-system-comparison.md) - Import/export patterns |

---

## Conversion Skill Naming Convention

```
convert-<source>-<target>
```

| Component | Description | Example |
|-----------|-------------|---------|
| `convert` | Fixed prefix | `convert-` |
| `<source>` | Source language (lowercase) | `typescript`, `python`, `golang` |
| `<target>` | Target language (lowercase) | `rust`, `python`, `golang` |

**Examples:**
- `convert-typescript-rust` - TypeScript → Rust
- `convert-python-golang` - Python → Go
- `convert-golang-rust` - Go → Rust

**Note:** Each skill is ONE-WAY. `convert-A-B` and `convert-B-A` are separate skills with different patterns.

---

## Conversion Skill Structure

Every `convert-X-Y` skill should follow this structure:

```markdown
# Convert <Source> to <Target>

## Overview
Brief description of the conversion, common use cases, and what to expect.

## When to Use
- Scenarios where this conversion makes sense
- Benefits of the target language for this use case

## When NOT to Use
- Scenarios where conversion is not recommended
- Better alternatives

## Type System Mapping
Complete mapping table from source types to target types.

## Idiom Translation
Source patterns and their idiomatic target equivalents.

## Error Handling
How to convert error handling patterns.

## Concurrency Patterns
How async/threading models translate.

## Memory & Ownership
If applicable, how memory models differ and translate.

## Testing Strategy
How to verify functional equivalence.

## Tooling
Available tools, transpilers, and validation helpers.

## Common Pitfalls
Mistakes to avoid during conversion.

## Examples
Concrete before/after conversion examples.
```

---

## The 8 Pillars Framework

Every conversion skill should address these 8 pillars for comprehensive coverage:

| Pillar | What to Document |
|--------|------------------|
| **1. Module System** | Import/export, visibility, package structure |
| **2. Error Handling** | Exception/Result/Option patterns, error propagation |
| **3. Concurrency** | Async/await, threads, processes, channels |
| **4. Metaprogramming** | Macros, decorators, reflection, code generation |
| **5. Zero/Default Values** | Null handling, default initialization, optional types |
| **6. Serialization** | JSON, binary formats, validation patterns |
| **7. Build System** | Package managers, build tools, project structure |
| **8. Testing** | Test frameworks, property-based testing, verification |

### 9th Pillar: Dev Workflow (for REPL-centric languages)

For conversions involving REPL-centric languages (Clojure, Elixir, Erlang, Haskell, Lisp, F#), add:

| Pillar | What to Document |
|--------|------------------|
| **9. Dev Workflow & REPL** | REPL patterns, hot reload, interactive debugging |

See `meta-convert-guide` for detailed guidance on each pillar.

---

## Skill Creation Workflow

When creating a new `convert-X-Y` skill:

### 1. Assess the Conversion

- **Check for existing skill**: Search `components/skills/convert-*`
- **Check for reverse skill**: If creating `convert-A-B`, check if `convert-B-A` exists
- **Identify category**: Static→Dynamic, GC→Ownership, etc.
- **Estimate difficulty**: See [difficulty-matrix.md](../meta-convert-guide/reference/difficulty-matrix.md) for pre-calculated ratings

### 2. Gather Language Knowledge

- Read `lang-X-dev` skill for source language
- Read `lang-Y-dev` skill for target language
- Identify key differences in the 8 pillars

### 3. Create Type Mapping Tables

For each pillar, create comprehensive mapping tables:

```markdown
| Source (X) | Target (Y) | Notes |
|------------|------------|-------|
| `string`   | `String`   | ...   |
```

### 4. Document Idiom Translations

Show idiomatic translations, not literal ports:

```markdown
// Source: X
[source code]

// Target: Y (idiomatic)
[target code]

// Avoid: Y (transliterated)
[non-idiomatic code]
```

### 5. Include Testing Strategy

- Port existing tests first
- Add property-based tests for invariants
- Use golden testing for output comparison

### 6. Self-Review Checklist

Before finalizing the skill:

- [ ] All 8 pillars addressed (9 if REPL-centric)
- [ ] Type mappings are complete
- [ ] Examples are idiomatic, not transliterated
- [ ] Common pitfalls documented
- [ ] Testing strategy included
- [ ] Cross-references to related skills

---

## Concurrency Pattern Translation

When converting code between languages, concurrency models are often the most challenging aspect. Different languages embody fundamentally different concurrency philosophies, from shared-memory threads to isolated processes, from promises to channels, from Software Transactional Memory (STM) to actor models.

This section provides a comprehensive guide to translating concurrency patterns across languages.

### Concurrency Model Matrix

Understanding the mapping between source and target concurrency models is crucial for successful conversion:

| Source Model | Target Model | Translation Strategy | Key Considerations |
|--------------|--------------|---------------------|-------------------|
| **Actors (BEAM)** | **STM (Clojure)** | Use atoms/refs for state, core.async for message-passing | BEAM processes → atoms for simple state, refs+dosync for coordinated updates |
| **Actors (BEAM)** | **IO Monad (Haskell)** | Use TVar for shared state, async for spawning | GenServers → IORef or TVar, supervision → exception handling |
| **Actors (BEAM)** | **Goroutines (Go)** | Channels for message passing, structs for state | GenServer → goroutine with channel, supervisor → error handling |
| **STM (Clojure)** | **Actors (BEAM)** | Wrap refs in GenServer, use supervisor for coordination | dosync transactions → GenServer serializes updates |
| **STM (Clojure)** | **Goroutines (Go)** | Channels + select for coordination, mutexes for shared state | refs → channels or sync.Mutex, atoms → atomic package |
| **Channels (Go)** | **Actors (BEAM)** | GenStage/Flow for backpressure, GenServer for state | Buffered channels → GenServer queue, select → receive |
| **Channels (Go)** | **Promises (JS/TS)** | Promise wraps channel receive, async/await for coordination | Goroutine → async function, channel receive → await |
| **IO Monad (Haskell)** | **Tasks (Roc)** | Map IO actions to Task effects | IO-based concurrency → Task-based effects system |
| **Promises (JS/TS)** | **Goroutines (Go)** | Goroutines for async execution, channels for communication | async function → goroutine, Promise → channel or direct return |
| **Promises (JS/TS)** | **Futures (Rust)** | Tokio runtime for async, futures for lazy evaluation | Promise (eager) → Future (lazy), await → .await |
| **Threads (Python)** | **Actors (BEAM)** | Spawn processes for each thread, message passing for communication | GIL limitations → true parallelism, threading.Thread → spawn |
| **Asyncio (Python)** | **Async/Await (Rust)** | Tokio runtime, async functions, futures | Event loop → runtime, coroutines → async fn |

**Key Insight**: Most conversions require not just syntactic translation but a fundamental shift in how you think about concurrency. For example:
- **Shared memory (threads) → Message passing (actors)**: Stop thinking about locks; start thinking about process isolation
- **Eager execution (Promises) → Lazy evaluation (Futures)**: Understand when work actually starts
- **Preemptive scheduling (OS threads) → Cooperative scheduling (async/await)**: Be aware of blocking operations

### Pattern Translation Examples

#### Example 1: Clojure STM → Elixir Actors (Coordinated State Updates)

**Problem**: Clojure's STM allows multiple refs to be updated atomically in a transaction. Elixir's actor model has isolated processes.

**Clojure (Source):**
```clojure
(def account-a (ref 1000))
(def account-b (ref 500))

(defn transfer [from to amount]
  (dosync
    (alter from - amount)
    (alter to + amount)))

;; Atomic bank transfer
(transfer account-a account-b 100)
;; account-a: 900, account-b: 600
```

**Elixir (Target - Idiomatic Translation):**
```elixir
defmodule Bank do
  use GenServer

  # Client API
  def start_link(initial_accounts) do
    GenServer.start_link(__MODULE__, initial_accounts, name: __MODULE__)
  end

  def transfer(from_account, to_account, amount) do
    GenServer.call(__MODULE__, {:transfer, from_account, to_account, amount})
  end

  def get_balance(account) do
    GenServer.call(__MODULE__, {:get_balance, account})
  end

  # Server Callbacks
  @impl true
  def init(initial_accounts) do
    {:ok, initial_accounts}
  end

  @impl true
  def handle_call({:transfer, from, to, amount}, _from, accounts) do
    case accounts do
      %{^from => from_balance, ^to => to_balance} when from_balance >= amount ->
        updated_accounts = accounts
        |> Map.update!(from, &(&1 - amount))
        |> Map.update!(to, &(&1 + amount))
        {:reply, :ok, updated_accounts}

      _ ->
        {:reply, {:error, :insufficient_funds}, accounts}
    end
  end

  @impl true
  def handle_call({:get_balance, account}, _from, accounts) do
    {:reply, Map.get(accounts, account, 0), accounts}
  end
end

# Usage
{:ok, _pid} = Bank.start_link(%{account_a: 1000, account_b: 500})
:ok = Bank.transfer(:account_a, :account_b, 100)
# account_a: 900, account_b: 600
```

**Translation Strategy**:
1. **Centralize coordinated state**: All accounts in single GenServer (serializes transactions)
2. **Transaction semantics**: GenServer's synchronous call provides atomicity
3. **Pattern matching**: Use guards to validate sufficient funds before update
4. **Immutable updates**: Map.update! returns new map, pattern matches for validation

**Edge Cases & Gotchas**:
- **Deadlock prevention**: Single GenServer eliminates distributed deadlocks
- **Scalability tradeoff**: STM allows concurrent reads; GenServer serializes all operations
- **Alternative**: For high throughput, shard accounts across multiple GenServers with distributed coordination

**Performance Implications**:
- Clojure STM: Optimistic concurrency (retry on conflict), parallel reads
- Elixir GenServer: Pessimistic serialization, all operations sequential
- For read-heavy workloads, consider Agent for each account + coordinator for transfers

**Cross-reference**: See `convert-clojure-elixir` for complete STM → Actor translation patterns.

---

#### Example 2: Go Channels → TypeScript Promises (Backpressure-Aware Pipeline)

**Problem**: Go channels provide natural backpressure through blocking sends/receives. JavaScript Promises execute eagerly and don't support backpressure natively.

**Go (Source):**
```go
func processStream(items []string) <-chan string {
    out := make(chan string, 10) // Buffered channel

    go func() {
        defer close(out)
        for _, item := range items {
            // Simulate slow processing
            time.Sleep(100 * time.Millisecond)
            processed := strings.ToUpper(item)
            out <- processed // Blocks if buffer full (backpressure!)
        }
    }()

    return out
}

func main() {
    results := processStream([]string{"a", "b", "c", "d", "e"})

    for result := range results {
        fmt.Println("Got:", result)
        time.Sleep(200 * time.Millisecond) // Slow consumer
    }
}
```

**TypeScript (Target - Idiomatic Translation):**
```typescript
async function* processStream(items: string[]): AsyncGenerator<string> {
  for (const item of items) {
    // Simulate slow processing
    await new Promise(resolve => setTimeout(resolve, 100));
    const processed = item.toUpperCase();
    yield processed; // Yields control back to consumer
  }
}

async function main() {
  const items = ["a", "b", "c", "d", "e"];

  for await (const result of processStream(items)) {
    console.log("Got:", result);
    await new Promise(resolve => setTimeout(resolve, 200)); // Slow consumer
  }
}

main();
```

**Alternative (Explicit Promise Queue with Backpressure):**
```typescript
class Channel<T> {
  private queue: T[] = [];
  private waiting: ((value: T) => void)[] = [];
  private maxSize: number;

  constructor(bufferSize: number = 10) {
    this.maxSize = bufferSize;
  }

  async send(value: T): Promise<void> {
    // Backpressure: wait if queue is full
    while (this.queue.length >= this.maxSize) {
      await new Promise(resolve => setTimeout(resolve, 10));
    }

    if (this.waiting.length > 0) {
      const resolve = this.waiting.shift()!;
      resolve(value);
    } else {
      this.queue.push(value);
    }
  }

  async receive(): Promise<T> {
    if (this.queue.length > 0) {
      return this.queue.shift()!;
    }

    return new Promise<T>(resolve => {
      this.waiting.push(resolve);
    });
  }
}

async function processStreamWithChannel(items: string[]): Promise<Channel<string>> {
  const ch = new Channel<string>(10);

  (async () => {
    for (const item of items) {
      await new Promise(resolve => setTimeout(resolve, 100));
      await ch.send(item.toUpperCase());
    }
  })();

  return ch;
}
```

**Translation Strategy**:
1. **Async generators**: Most idiomatic for streaming data in TypeScript
2. **Yield control**: `yield` allows consumer to control pace (like channel receive blocking)
3. **Custom Channel class**: For explicit buffering and backpressure semantics
4. **Event-driven alternative**: Use Node.js streams for larger data pipelines

**Edge Cases & Gotchas**:
- **No native backpressure**: Promises execute eagerly; must implement queue manually
- **Memory growth**: Without backpressure, fast producer overwhelms slow consumer
- **Cancellation**: Go channels close; async generators must handle cleanup explicitly
- **Error propagation**: Go errors via multiple returns; TypeScript uses try/catch or rejected promises

**Performance Implications**:
- Go channels: OS-level blocking, true concurrency across cores
- TypeScript async: Event loop, single-threaded unless using worker threads
- For CPU-bound work, consider worker threads or external processing

**Cross-reference**: See `convert-typescript-golang` and `convert-golang-rust` for channel translation patterns.

---

#### Example 3: Python Asyncio → Erlang Processes (Event Loop → Actor Model)

**Problem**: Python's asyncio uses a single-threaded event loop with coroutines. Erlang uses lightweight processes with true preemptive concurrency.

**Python (Source):**
```python
import asyncio
from typing import Dict

class ConnectionPool:
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.active_connections: Dict[str, asyncio.Task] = {}
        self.semaphore = asyncio.Semaphore(max_connections)

    async def connect(self, conn_id: str):
        async with self.semaphore:
            print(f"Connecting {conn_id}")
            await asyncio.sleep(1)  # Simulate connection
            self.active_connections[conn_id] = asyncio.current_task()
            print(f"Connected {conn_id}")
            return conn_id

    async def disconnect(self, conn_id: str):
        if conn_id in self.active_connections:
            print(f"Disconnecting {conn_id}")
            del self.active_connections[conn_id]

async def main():
    pool = ConnectionPool(max_connections=3)

    # Start 5 connections (only 3 concurrent due to semaphore)
    tasks = [pool.connect(f"conn-{i}") for i in range(5)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

**Erlang (Target - Idiomatic Translation):**
```erlang
-module(connection_pool).
-behaviour(gen_server).

%% API
-export([start_link/1, connect/2, disconnect/2, stop/1]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2]).

-record(state, {
    max_connections :: integer(),
    active_connections :: #{binary() => pid()},
    waiting_queue :: queue:queue()
}).

%% Client API
start_link(MaxConnections) ->
    gen_server:start_link(?MODULE, MaxConnections, []).

connect(PoolPid, ConnId) ->
    gen_server:call(PoolPid, {connect, ConnId}, infinity).

disconnect(PoolPid, ConnId) ->
    gen_server:cast(PoolPid, {disconnect, ConnId}).

stop(PoolPid) ->
    gen_server:stop(PoolPid).

%% Server Callbacks
init(MaxConnections) ->
    State = #state{
        max_connections = MaxConnections,
        active_connections = #{},
        waiting_queue = queue:new()
    },
    {ok, State}.

handle_call({connect, ConnId}, From, State) ->
    #state{
        max_connections = Max,
        active_connections = Active,
        waiting_queue = Queue
    } = State,

    case maps:size(Active) < Max of
        true ->
            %% Spawn connection process
            Pid = spawn_link(fun() -> connection_worker(ConnId) end),
            io:format("Connecting ~s~n", [ConnId]),
            NewActive = maps:put(ConnId, Pid, Active),
            {reply, {ok, ConnId}, State#state{active_connections = NewActive}};

        false ->
            %% Queue is full, add to waiting queue
            NewQueue = queue:in({ConnId, From}, Queue),
            {noreply, State#state{waiting_queue = NewQueue}}
    end.

handle_cast({disconnect, ConnId}, State) ->
    #state{
        active_connections = Active,
        waiting_queue = Queue
    } = State,

    io:format("Disconnecting ~s~n", [ConnId]),
    NewActive = maps:remove(ConnId, Active),

    %% Process waiting queue
    case queue:out(Queue) of
        {{value, {NextConnId, From}}, NewQueue} ->
            Pid = spawn_link(fun() -> connection_worker(NextConnId) end),
            gen_server:reply(From, {ok, NextConnId}),
            FinalActive = maps:put(NextConnId, Pid, NewActive),
            {noreply, State#state{
                active_connections = FinalActive,
                waiting_queue = NewQueue
            }};

        {empty, _} ->
            {noreply, State#state{active_connections = NewActive}}
    end.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

%% Internal Functions
connection_worker(ConnId) ->
    timer:sleep(1000),  %% Simulate connection
    io:format("Connected ~s~n", [binary_to_list(ConnId)]),
    receive
        disconnect -> ok
    end.

%% Usage example
%% 1> {ok, Pool} = connection_pool:start_link(3).
%% 2> [connection_pool:connect(Pool, list_to_binary("conn-" ++ integer_to_list(I))) || I <- lists:seq(1, 5)].
```

**Translation Strategy**:
1. **Event loop → GenServer**: Central coordinator manages connection state
2. **Semaphore → Capacity check**: Manual tracking of active connections vs max
3. **Coroutines → Processes**: Each connection is a separate process (true isolation)
4. **Async tasks → spawn_link**: Lightweight processes with supervision
5. **Queue for backpressure**: Explicitly manage waiting clients when pool full

**Edge Cases & Gotchas**:
- **Blocking vs message passing**: Python blocks on semaphore; Erlang queues requests
- **Error handling**: Python exceptions in event loop; Erlang links and monitors for crash detection
- **Process cleanup**: Must handle process termination and queue cleanup
- **Timeout handling**: Add receive timeout patterns for connection timeouts

**Performance Implications**:
- Python asyncio: Single thread, cooperative scheduling, GIL limitations
- Erlang: True concurrency, processes scheduled across cores, no GIL
- Erlang's preemptive scheduling handles blocking better (processes don't block each other)
- Consider supervision tree for fault tolerance in Erlang

**Cross-reference**: See `convert-python-erlang` for complete asyncio → BEAM translation patterns.

---

### Supervision and Fault Tolerance Translation

Supervision is a key pattern in fault-tolerant systems. Different concurrency models provide different supervision mechanisms:

| Source Model | Target Model | Translation Pattern |
|--------------|--------------|---------------------|
| **BEAM Supervision Trees** | **Go error handling** | Explicit error returns, retry loops, health checks |
| **BEAM Supervision Trees** | **Rust Result + retry crate** | Result types for errors, tokio::task for spawning, manual restart |
| **BEAM let-it-crash** | **Clojure agents + error handlers** | Agent error-handler and error-mode, restart-agent |
| **Go defer/panic/recover** | **BEAM try/catch + supervisor** | Convert panic → exit, recover → supervisor restart |
| **Python try/except** | **BEAM let-it-crash** | Remove defensive error handling, use supervisor for recovery |
| **Rust panic=abort** | **BEAM supervision** | Change panic strategy to supervised process restart |

#### Supervision Pattern: Erlang Supervision Tree → Go Error Handling

**Erlang (Source - Let It Crash):**
```erlang
-module(worker_sup).
-behaviour(supervisor).

-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    SupFlags = #{
        strategy => one_for_one,      %% Restart individual workers
        intensity => 5,                %% Max 5 restarts
        period => 60                   %% In 60 seconds
    },

    ChildSpecs = [
        #{
            id => worker1,
            start => {worker, start_link, [worker1]},
            restart => permanent,      %% Always restart
            shutdown => 5000,
            type => worker
        }
    ],

    {ok, {SupFlags, ChildSpecs}}.

%% Worker module (crashes are OK, supervisor restarts)
-module(worker).
-behaviour(gen_server).

handle_call({process, Data}, _From, State) ->
    Result = risky_operation(Data),  %% May crash - that's fine!
    {reply, Result, State}.

risky_operation(Data) ->
    case Data of
        invalid -> error(badarg);     %% Crash - supervisor will restart
        _ -> process_data(Data)
    end.
```

**Go (Target - Explicit Error Handling + Retry):**
```go
package main

import (
    "context"
    "errors"
    "fmt"
    "log"
    "time"
)

// WorkerSupervisor manages worker lifecycle with restart logic
type WorkerSupervisor struct {
    maxRestarts int
    period      time.Duration
    restartLog  []time.Time
    workerFunc  func(context.Context) error
    ctx         context.Context
    cancel      context.CancelFunc
}

func NewWorkerSupervisor(
    maxRestarts int,
    period time.Duration,
    workerFunc func(context.Context) error,
) *WorkerSupervisor {
    ctx, cancel := context.WithCancel(context.Background())
    return &WorkerSupervisor{
        maxRestarts: maxRestarts,
        period:      period,
        workerFunc:  workerFunc,
        restartLog:  make([]time.Time, 0),
        ctx:         ctx,
        cancel:      cancel,
    }
}

func (s *WorkerSupervisor) Start() {
    go s.supervise()
}

func (s *WorkerSupervisor) Stop() {
    s.cancel()
}

func (s *WorkerSupervisor) supervise() {
    for {
        select {
        case <-s.ctx.Done():
            log.Println("Supervisor shutting down")
            return
        default:
            // Check restart intensity
            if s.exceedsRestartIntensity() {
                log.Println("Max restart intensity exceeded, shutting down")
                return
            }

            // Run worker
            err := s.workerFunc(s.ctx)
            if err != nil {
                log.Printf("Worker crashed: %v, restarting...", err)
                s.logRestart()
                time.Sleep(1 * time.Second) // Backoff before restart
            }
        }
    }
}

func (s *WorkerSupervisor) exceedsRestartIntensity() bool {
    now := time.Now()
    cutoff := now.Add(-s.period)

    // Remove old restart entries
    validRestarts := make([]time.Time, 0)
    for _, t := range s.restartLog {
        if t.After(cutoff) {
            validRestarts = append(validRestarts, t)
        }
    }
    s.restartLog = validRestarts

    return len(s.restartLog) >= s.maxRestarts
}

func (s *WorkerSupervisor) logRestart() {
    s.restartLog = append(s.restartLog, time.Now())
}

// Worker implementation
type Worker struct {
    id string
}

func (w *Worker) Run(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            // Simulate work with potential errors
            if err := w.riskyOperation(); err != nil {
                return fmt.Errorf("worker %s failed: %w", w.id, err)
            }
            time.Sleep(1 * time.Second)
        }
    }
}

func (w *Worker) riskyOperation() error {
    // Simulate occasional failures
    if time.Now().Unix()%10 == 0 {
        return errors.New("random failure")
    }
    log.Printf("Worker %s processing...", w.id)
    return nil
}

func main() {
    worker := &Worker{id: "worker1"}

    supervisor := NewWorkerSupervisor(
        5,                    // Max 5 restarts
        60*time.Second,       // In 60 seconds
        worker.Run,
    )

    supervisor.Start()

    // Run for demo duration
    time.Sleep(120 * time.Second)
    supervisor.Stop()
}
```

**Translation Strategy**:
1. **Supervisor behavior → Supervisor struct**: Encapsulate restart logic in struct
2. **Restart strategies**: Implement one-for-one manually (each worker independent)
3. **Intensity tracking**: Log restart times, check against intensity limits
4. **Context for cancellation**: Use context.Context for graceful shutdown
5. **Error propagation**: Workers return errors instead of crashing

**Supervision Translation Rules**:
- `one_for_one` → Independent goroutines with individual supervisors
- `one_for_all` → Cancel all workers if one fails, restart all
- `rest_for_one` → Cancel dependent workers (those started after failed worker)
- Restart intensity → Track restart timestamps, check against limits

**Error Isolation Strategies**:

| Language | Isolation Mechanism | Fault Containment |
|----------|---------------------|-------------------|
| **Erlang/Elixir** | Separate processes, supervision trees | Process crash doesn't affect others |
| **Go** | Goroutines + defer/recover, error returns | Panic in goroutine kills goroutine only (with recover) |
| **Rust** | Result/Option types, panic=abort or unwind | Thread panic isolated, Result forces error handling |
| **Clojure** | Agents with error-mode, futures with deref | Agent errors caught in error-handler |
| **Haskell** | Async with catches, STM for atomicity | Exceptions in async isolated, catchable |
| **Python** | Threading/asyncio with try/except | Thread exceptions isolated, asyncio tasks can be cancelled |

**Cross-reference**:
- See `convert-python-erlang` for asyncio → supervision patterns
- See `convert-golang-rust` for panic/recover → Result type patterns
- See `convert-clojure-elixir` for agent error handling → OTP patterns

---

### Common Concurrency Anti-Patterns to Avoid

When translating concurrency patterns, avoid these common mistakes:

1. **Literal Translation of Synchronization Primitives**
   - ❌ Don't translate `lock()` in Python to `Mutex` in every target language
   - ✓ Use target's idiomatic concurrency: actors for Erlang, STM for Clojure, channels for Go

2. **Ignoring Backpressure**
   - ❌ Don't translate bounded channels to unbounded Promises (memory leak!)
   - ✓ Implement explicit backpressure with async generators or custom queues

3. **Mixing Concurrency Models**
   - ❌ Don't mix threads + async/await without understanding implications
   - ✓ Choose one concurrency model and use it consistently

4. **Over-Serialization**
   - ❌ Don't funnel all parallel operations through a single actor/GenServer
   - ✓ Shard state across multiple actors/processes for scalability

5. **Under-Isolation**
   - ❌ Don't share mutable state across goroutines without synchronization
   - ✓ Use message passing or proper synchronization primitives

6. **Ignoring Ordering Guarantees**
   - ❌ Don't assume message ordering when target language doesn't guarantee it
   - ✓ Add explicit sequence numbers or use ordered channels if needed

---

## Skill Template

When creating a new `convert-X-Y` skill, use this template:

```markdown
---
name: convert-<source>-<target>
description: Convert <Source> code to <Target>. Use when migrating <Source> projects to <Target>, translating <Source> patterns to idiomatic <Target>, or refactoring <Source> codebases into <Target>. Extends meta-convert-dev with <Source>-to-<Target> specific patterns.
---

# Convert <Source> to <Target>

Convert <Source> code to idiomatic <Target>. This skill extends `meta-convert-dev` with <Source>-to-<Target> specific type mappings, idiom translations, and tooling.

## This Skill Extends

- `meta-convert-dev` - Skill creation patterns
- `meta-convert-guide` - Conversion methodology (APTV workflow, testing strategies)

## This Skill Adds

- **Type mappings**: <Source> types → <Target> types
- **Idiom translations**: <Source> patterns → idiomatic <Target>
- **Error handling**: <Source> exceptions/errors → <Target> approach
- **Async patterns**: <Source> async → <Target> async
- **Tooling**: <Source>-to-<Target> specific tools

## Quick Reference

| <Source> | <Target> | Notes |
|----------|----------|-------|
| `<type1>` | `<type1>` | ... |
| `<type2>` | `<type2>` | ... |

## [Continue with 8 Pillar sections...]
```

---

## References

### Reference Materials (in `references/` directory)

- [platform-ecosystem.md](references/platform-ecosystem.md) - Platform families, runtime characteristics, FFI, stdlib mapping
- [paradigm-translation.md](references/paradigm-translation.md) - OOP↔FP, imperative↔declarative, type system shifts
- [ownership-translation.md](references/ownership-translation.md) - GC↔ownership, borrowing patterns, lifetime translation
- [numeric-edge-cases.md](references/numeric-edge-cases.md) - Overflow, division semantics, float precision, arbitrary precision
- [stdlib-mapping.md](references/stdlib-mapping.md) - Common stdlib function equivalents across languages
- [build-system-mapping.md](references/build-system-mapping.md) - Package managers and build tools
- [migration-strategies.md](references/migration-strategies.md) - Migration approaches and strategies
- [module-system-comparison.md](references/module-system-comparison.md) - Import/export and visibility patterns
- [naming-conventions.md](references/naming-conventions.md) - Naming conventions across languages
- [performance-considerations.md](references/performance-considerations.md) - Performance patterns and considerations

### Conversion Methodology

- `meta-convert-guide` - APTV workflow, type system strategies, idiom patterns, testing approaches, common pitfalls

### Skills That Extend This Meta-Skill

These skills provide concrete, language-pair-specific implementations:

- `convert-typescript-rust` - TypeScript → Rust conversion
- `convert-typescript-python` - TypeScript → Python conversion
- `convert-typescript-golang` - TypeScript → Go conversion
- `convert-golang-rust` - Go → Rust conversion
- `convert-python-rust` - Python → Rust conversion

### Related Meta-Skills

- `meta-library-dev` - Library development patterns

### Language Skills

For language-specific fundamentals (not conversion):

- `lang-typescript-dev` - TypeScript development patterns
- `lang-python-dev` - Python development patterns
- `lang-golang-dev` - Go development patterns
- `lang-rust-dev` - Rust development patterns

### Commands

- `/create-lang-conversion-skill <source> <target>` - Create a new conversion skill using this meta-skill as foundation
