---
name: eio
description: "Eio concurrency patterns for OCaml applications. Use when Claude needs to: (1) Write concurrent OCaml code with Eio, (2) Handle network operations with cohttp-eio, (3) Manage resource lifecycles with switches, (4) Implement rate limiting or synchronization, (5) Create parallel operations with fibers, (6) Test async code with Eio_mock, (7) Integrate with bytesrw for streaming, or any other Eio-based concurrency tasks"
license: ISC
---

# Eio Concurrency

## Core Concepts

### Why Eio

Eio is an effects-based IO library for OCaml 5. Advantages over Lwt/Async:

- **Direct-style code**: No monads, concurrent code looks like sequential code
- **Performance**: Real stacks, no heap allocations to simulate continuations
- **Better backtraces**: Exceptions show proper call traces
- **Platform optimization**: Generic API with optimized backends (Linux io_uring, POSIX, Windows)

### Capability-Based Design

Pass capabilities explicitly instead of using global resources:

```ocaml
type t = {
  net : _ Eio.Net.t;
  clock : _ Eio.Time.clock;
  fs : _ Eio.Path.t;
}

(* Function signature reveals what resources it needs *)
val connect : net:_ Eio.Net.t -> host:string -> connection
```

**Do**: Pass `net`, `clock`, `fs` explicitly—makes dependencies clear and testable.

**Don't**: Use global modules like `Unix.gettimeofday` or access ambient resources.

### Structured Concurrency with Switches

`Eio.Switch.run` manages resource and fiber lifecycles:

```ocaml
Eio.Switch.run @@ fun sw ->
  let conn = connect ~sw server in
  (* conn automatically closed when sw exits *)
  process conn
```

**Do**: Create switches in the smallest possible scope.

**Don't**: Take a switch argument if you could create one internally.

### Fibers

Lightweight concurrent units running on a single core:

```ocaml
(* Run two operations concurrently *)
Eio.Fiber.both
  (fun () -> download file1)
  (fun () -> download file2)

(* Only one fiber executes at a time until one performs an effect *)
```

### Cancellation

Cancellation contexts form a tree. Uncaught exceptions propagate upward, cancelling siblings:

```ocaml
(* If one branch fails, the other gets Cancelled *)
Eio.Fiber.both
  (fun () -> may_fail ())
  (fun () -> other_work ())  (* receives Cancelled if may_fail raises *)
```

Use `Cancel.protect` for operations that must complete:

```ocaml
Eio.Cancel.protect @@ fun () ->
  (* This won't be cancelled even if parent is *)
  flush_and_close connection
```

## Common Patterns

### Concurrent Operations

```ocaml
(* Parallel map *)
let fetch_all_items api item_ids =
  Eio.Fiber.List.map (fun id -> Api.item_info api id) item_ids

(* Race with timeout *)
let with_timeout ~clock duration fn =
  Eio.Fiber.first
    (fun () -> Eio.Time.sleep clock duration; Error `Timeout)
    (fun () -> Ok (fn ()))

(* Fork background task attached to switch *)
Eio.Fiber.fork ~sw (fun () -> background_work ())
```

### File Operations

```ocaml
let ( / ) = Eio.Path.( / )

(* Read file *)
let content = Eio.Path.load (fs / "config.json")

(* Write file with permissions *)
Eio.Path.save ~create:(`Or_truncate 0o600) (fs / "data.bin") content

(* Create directory if needed *)
Eio.Path.mkdirs ~exists_ok:true ~perm:0o755 (fs / "cache")

(* Clean up directory tree *)
Eio.Path.rmtree (fs / "tmp")

(* Check file type *)
match Eio.Path.kind ~follow:true path with
| `Directory -> ...
| `Regular_file -> ...
| `Not_found -> ...
```

### Network Operations

```ocaml
(* TCP client *)
Eio.Net.connect ~sw net (`Tcp (addr, port))

(* TCP server *)
Eio.Net.run_server sock ~on_error:log_error
  ~max_connections:100
  (fun ~sw flow addr -> handle_client ~sw flow)
```

### HTTPS with cohttp-eio

```ocaml
let https_handler uri raw_flow =
  let tls_config = create_tls_config () in
  let host = Uri.host uri |> Option.map Domain_name.(host_exn % of_string_exn) in
  Tls_eio.client_of_flow ?host tls_config raw_flow

let client = Cohttp_eio.Client.make net ~https:(Some https_handler)
```

### Buffered Reading

Always use `max_size` to prevent memory exhaustion:

```ocaml
let body = Eio.Buf_read.(of_flow ~max_size:10_000_000 flow |> take_all)
```

### Synchronization Primitives

**Mutex**:
```ocaml
let mutex = Eio.Mutex.create ()
Eio.Mutex.use_rw mutex (fun () -> shared_state := new_value)
```

**Semaphore for rate limiting**:
```ocaml
let limiter = Eio.Semaphore.make 10
let with_rate_limit fn =
  Eio.Semaphore.acquire limiter;
  Fun.protect ~finally:(fun () -> Eio.Semaphore.release limiter) fn
```

**Stream for producer/consumer**:
```ocaml
let queue = Eio.Stream.create 100
Eio.Stream.add queue item      (* producer *)
let item = Eio.Stream.take queue  (* consumer, blocks if empty *)
```

**Condition variables** (must check in loop):
```ocaml
let cond = Eio.Condition.create ()
let mutex = Eio.Mutex.create ()

(* Waiter - MUST use while loop *)
Eio.Mutex.use_rw ~protect:false mutex (fun () ->
  while not (check_condition ()) do
    Eio.Condition.await cond mutex
  done)

(* Signaler *)
Eio.Condition.broadcast cond
```

## Integration with bytesrw

Bridge Eio flows to bytesrw for streaming binary parsing:

```ocaml
(* Eio flow → bytesrw reader *)
let reader_of_flow ?(buf_len = 4096) flow =
  let cs = Cstruct.create buf_len in
  let read () =
    match Eio.Flow.single_read flow cs with
    | 0 -> Bytesrw.Bytes.Slice.eod
    | n ->
        let buf = Cstruct.to_bytes (Cstruct.sub cs 0 n) in
        Bytesrw.Bytes.Slice.make buf ~first:0 ~length:n
    | exception End_of_file -> Bytesrw.Bytes.Slice.eod
  in
  Bytesrw.Bytes.Reader.make read

(* Then use with Binary.Reader *)
let r = Binary.Reader.of_reader (reader_of_flow flow)
let frame = Tc_frame.parse r  (* effects propagate through *)
```

Note: This involves a copy from Cstruct (Bigarray) to bytes (heap). Unavoidable until OCaml has non-moving bytes.

## RNG Initialization

**Critical for crypto**: Initialize RNG before any crypto operations.

```ocaml
(* For Eio applications *)
Eio_main.run @@ fun env ->
  Mirage_crypto_rng_eio.run (module Mirage_crypto_rng.Fortuna) env @@ fun () ->
    (* RNG now available *)
    let iv = Mirage_crypto_rng.generate 12 in
    ...

(* For Unix applications (simpler but less integrated) *)
Mirage_crypto_rng_unix.initialize (module Mirage_crypto_rng.Fortuna)
```

Failure to initialize results in predictable random numbers, breaking crypto security.

## Error Handling

Errors use `Eio.Io (err, context)` with nested error codes:

```ocaml
try
  Eio.Net.connect ~sw net addr
with
| Eio.Io (Eio.Net.E (Connection_failure _), _) ->
    (* Specific error *)
    Error `Connection_failed
| Eio.Io (Eio.Net.E _, _) ->
    (* Any network error *)
    Error `Network_error
| Eio.Io _ ->
    (* Any Eio error *)
    Error `Io_error
```

Add context when re-raising:

```ocaml
Eio.Exn.reraise_with_context exn "while connecting to %s" host
```

For tests, hide backend details:

```ocaml
Eio.Exn.Backend.show := false
```

## Testing with Eio_mock

Library: `eio.mock` (not `eio_mock`)

### Test Setup Pattern

```ocaml
let setup_test f () =
  Mirage_crypto_rng_unix.use_default ();  (* or initialize RNG *)
  Eio_main.run @@ fun env ->
  Eio.Switch.run @@ fun sw ->
  let fs = Eio.Stdenv.fs env in
  let tmp = Eio.Path.(fs / Filename.get_temp_dir_name () / "test-dir") in
  (try Eio.Path.rmtree tmp with _ -> ());
  Eio.Path.mkdirs ~exists_ok:true ~perm:0o755 tmp;
  Fun.protect
    ~finally:(fun () -> try Eio.Path.rmtree tmp with _ -> ())
    (fun () -> f ~sw tmp)

let test_something = setup_test @@ fun ~sw tmp ->
  (* test code here *)
```

### Mock Flow

```ocaml
let test_api_call () =
  Eio_main.run @@ fun _env ->
  let flow = Eio_mock.Flow.make "response" in
  (* IMPORTANT: Always end with `Raise End_of_file *)
  Eio_mock.Flow.on_read flow [
    `Return "{\"ok\": true}";
    `Raise End_of_file;
  ];
  (* use flow *)
```

### Simulating Chunked Data

```ocaml
let test_partial_reads () =
  Eio_main.run @@ fun _env ->
  let flow = Eio_mock.Flow.make "chunked" in
  Eio_mock.Flow.on_read flow [
    `Return "\x00\x01";      (* First 2 bytes *)
    `Return "\x02\x03";      (* Next 2 bytes *)
    `Raise End_of_file;
  ];
  (* Parser must handle values spanning chunks *)
```

### Mock Network

```ocaml
let test_network () =
  Eio_main.run @@ fun _env ->
  let net = Eio_mock.Net.make "mocknet" in
  let flow = Eio_mock.Flow.make "conn" in
  Eio_mock.Net.on_connect net [`Return flow];
  Eio_mock.Flow.on_read flow [`Return "data"; `Raise End_of_file];
  (* test network operations *)
```

### Deadlock Detection

`Eio_mock.Backend.run` automatically detects deadlocks in tests.

## Common Gotchas

| Issue | Problem | Solution |
|-------|---------|----------|
| Racing reads | Both reads may complete at kernel level | Don't rely on `Fiber.first` for mutual exclusion |
| Signal handlers | Most operations risk deadlock | Only `Eio.Condition.broadcast` is safe |
| Condition spurious wakeup | May wake without signal | Always check condition in `while` loop |
| Mutex in signal handler | Re-entrancy issues | Use conditions instead |
| Forgetting End_of_file | Mock flow hangs | Always end mock reads with `Raise End_of_file` |
| Missing RNG init | Predictable crypto | Initialize before any crypto operations |

## Library Integration

| Library | Purpose | Notes |
|---------|---------|-------|
| Lwt_eio | Run Lwt + Eio together | Gradual migration path |
| Async_eio | Run Async + Eio together | Experimental |
| bytesrw | Streaming byte parsing | Requires copy (Cstruct→bytes) |
| cohttp-eio | HTTP client/server | Native Eio support |
| tls-eio | TLS connections | Use with cohttp-eio for HTTPS |
| mirage-crypto-rng-eio | Crypto RNG | Required for crypto operations |

## Best Practices

| Practice | Description |
|----------|-------------|
| Capability passing | Pass `net`, `clock`, `fs` explicitly |
| Structured concurrency | Use `Switch.run`, keep scopes small |
| Handle errors at boundaries | Convert `Eio.Io` to domain errors |
| Buffered reading | Use `Buf_read` with `max_size` |
| Parallel with fibers | `Fiber.List.map`, `Fiber.both`, `Fiber.first` |
| Isolate blocking | `Eio_unix.run_in_systhread` for non-Eio blocking |
| Test with mocks | `Eio_mock` for deterministic tests |
| Initialize RNG | Before any crypto operations |

## References

- Eio repository: https://github.com/ocaml-multicore/eio
- Eio documentation: https://ocaml.org/p/eio/latest/doc/
- cohttp-eio: https://github.com/mirage/ocaml-cohttp
- bytesrw: https://erratique.ch/software/bytesrw
