---
name: Gleam Erlang Interop
description: Use when gleam-Erlang interoperability including calling Erlang code from Gleam, using Erlang libraries, external functions, working with Erlang types, NIFs, and leveraging the BEAM ecosystem from Gleam applications.
allowed-tools: []
---

# Gleam Erlang Interop

## Introduction

Gleam compiles to Erlang, enabling seamless interoperability with the vast Erlang
ecosystem. This interop allows Gleam developers to leverage battle-tested Erlang
libraries while writing type-safe Gleam code, combining modern language features
with decades of production-proven libraries.

The interop mechanism uses external functions to call Erlang code, with Gleam's
type system providing safety at the boundary. Gleam can call any Erlang function,
use Erlang processes, and integrate with OTP behaviors while maintaining type
safety.

This skill covers external function declarations, calling Erlang modules, working
with Erlang types, using Erlang standard library, NIFs and ports, and patterns
for safe type boundaries when integrating with Erlang code.

## External Function Declarations

External functions declare Erlang functions with Gleam types, providing typed
interfaces to Erlang code.

```gleam
// Basic external function
@external(erlang, "erlang", "list_to_binary")
pub fn list_to_binary(list: List(Int)) -> BitArray

// Using external functions
pub fn convert_list() {
  let list = [72, 101, 108, 108, 111]
  let binary = list_to_binary(list)
  io.debug(binary)
}

// External function with multiple arguments
@external(erlang, "string", "concat")
pub fn string_concat(a: String, b: String) -> String

pub fn join_strings() {
  let result = string_concat("Hello, ", "World!")
  io.debug(result)
}

// External function returning Result
@external(erlang, "file", "read_file")
fn erlang_read_file(path: String) -> Result(BitArray, Dynamic)

pub fn read_file(path: String) -> Result(String, String) {
  case erlang_read_file(path) {
    Ok(contents) -> {
      case bit_array.to_string(contents) {
        Ok(str) -> Ok(str)
        Error(_) -> Error("Invalid UTF-8")
      }
    }
    Error(_) -> Error("File read error")
  }
}

// External function with erlang types
@external(erlang, "maps", "get")
fn map_get(key: a, map: Map(a, b)) -> Result(b, Nil)

@external(erlang, "maps", "put")
fn map_put(key: a, value: b, map: Map(a, b)) -> Map(a, b)

// Using Erlang's timer module
@external(erlang, "timer", "sleep")
pub fn sleep(milliseconds: Int) -> Nil

pub fn wait_a_second() {
  io.println("Waiting...")
  sleep(1000)
  io.println("Done!")
}

// External function with tuples
@external(erlang, "calendar", "local_time")
pub fn local_time() -> #(#(Int, Int, Int), #(Int, Int, Int))

pub fn get_current_time() {
  let #(date, time) = local_time()
  let #(year, month, day) = date
  let #(hour, minute, second) = time
  io.debug(#(year, month, day, hour, minute, second))
}

// External functions with atoms
pub type Atom

@external(erlang, "erlang", "binary_to_atom")
fn binary_to_atom(binary: BitArray) -> Atom

@external(erlang, "erlang", "atom_to_binary")
fn atom_to_binary(atom: Atom) -> BitArray

// Creating safe wrappers
pub opaque type ErlangAtom {
  ErlangAtom(atom: Dynamic)
}

pub fn atom_from_string(str: String) -> ErlangAtom {
  let bits = bit_array.from_string(str)
  let atom = binary_to_atom(bits)
  ErlangAtom(atom: dynamic.from(atom))
}

// External function with callbacks
@external(erlang, "lists", "map")
pub fn erlang_map(f: fn(a) -> b, list: List(a)) -> List(b)

pub fn double_list(list: List(Int)) -> List(Int) {
  erlang_map(fn(x) { x * 2 }, list)
}

// Process-related external functions
@external(erlang, "erlang", "self")
pub fn self() -> process.Pid

@external(erlang, "erlang", "spawn")
pub fn spawn(f: fn() -> Nil) -> process.Pid

// System external functions
@external(erlang, "erlang", "system_time")
fn system_time_nanos() -> Int

pub fn current_timestamp() -> Int {
  system_time_nanos() / 1_000_000
}
```

External declarations bridge Gleam's type system with Erlang's dynamic runtime.

## Using Erlang Standard Library

Gleam can leverage Erlang's comprehensive standard library for various operations.

```gleam
// Crypto module
@external(erlang, "crypto", "hash")
fn crypto_hash(algorithm: Atom, data: BitArray) -> BitArray

pub fn sha256(data: String) -> BitArray {
  let algo = atom_from_string("sha256")
  let bits = bit_array.from_string(data)
  crypto_hash(algo.atom, bits)
}

pub fn md5(data: String) -> String {
  let algo = atom_from_string("md5")
  let bits = bit_array.from_string(data)
  let hash = crypto_hash(algo.atom, bits)
  bit_array.base16_encode(hash, False)
}

// Random module
@external(erlang, "rand", "uniform")
fn uniform() -> Float

@external(erlang, "rand", "uniform")
fn uniform_int(n: Int) -> Int

pub fn random_float() -> Float {
  uniform()
}

pub fn random_int(max: Int) -> Int {
  uniform_int(max)
}

pub fn random_choice(list: List(a)) -> Option(a) {
  case list {
    [] -> None
    items -> {
      let index = uniform_int(list.length(items))
      list.at(items, index - 1)
    }
  }
}

// ETS (Erlang Term Storage)
pub type EtsTable

@external(erlang, "ets", "new")
fn ets_new(name: Atom, options: List(Atom)) -> EtsTable

@external(erlang, "ets", "insert")
fn ets_insert(table: EtsTable, tuple: #(a, b)) -> Bool

@external(erlang, "ets", "lookup")
fn ets_lookup(table: EtsTable, key: a) -> List(#(a, b))

pub fn create_cache() -> EtsTable {
  let name = atom_from_string("my_cache")
  let public = atom_from_string("public")
  let set = atom_from_string("set")
  ets_new(name.atom, [set.atom, public.atom])
}

pub fn cache_put(table: EtsTable, key: String, value: String) -> Bool {
  ets_insert(table, #(key, value))
}

pub fn cache_get(table: EtsTable, key: String) -> Option(String) {
  case ets_lookup(table, key) {
    [#(_, value)] -> Some(value)
    _ -> None
  }
}

// HTTP client via Erlang's httpc
@external(erlang, "httpc", "request")
fn httpc_request(url: String) -> Result(Dynamic, Dynamic)

pub fn http_get(url: String) -> Result(String, String) {
  case httpc_request(url) {
    Ok(response) -> {
      // Parse Erlang response tuple
      Ok("Response received")
    }
    Error(_) -> Error("HTTP request failed")
  }
}

// JSON via jiffy library
@external(erlang, "jiffy", "encode")
fn jiffy_encode(term: Dynamic) -> BitArray

@external(erlang, "jiffy", "decode")
fn jiffy_decode(json: BitArray) -> Result(Dynamic, Dynamic)

pub fn encode_json(data: Dict(String, String)) -> String {
  let dynamic_data = dynamic.from(data)
  let bits = jiffy_encode(dynamic_data)
  case bit_array.to_string(bits) {
    Ok(str) -> str
    Error(_) -> "{}"
  }
}

// OS module
@external(erlang, "os", "getenv")
fn os_getenv(var: String) -> Result(String, Nil)

pub fn get_env(var: String) -> Option(String) {
  case os_getenv(var) {
    Ok(value) -> Some(value)
    Error(_) -> None
  }
}

@external(erlang, "os", "cmd")
pub fn shell_command(cmd: String) -> String

pub fn list_files() -> String {
  shell_command("ls -la")
}

// Code loading
@external(erlang, "code", "ensure_loaded")
fn code_ensure_loaded(module: Atom) -> Result(Atom, Atom)

pub fn ensure_module_loaded(module_name: String) -> Bool {
  let atom = atom_from_string(module_name)
  case code_ensure_loaded(atom.atom) {
    Ok(_) -> True
    Error(_) -> False
  }
}
```

Erlang's standard library provides production-tested functionality for common
operations.

## Working with Erlang Types

Gleam's Dynamic type enables safe interop with Erlang's dynamic type system.

```gleam
import gleam/dynamic

// Dynamic value handling
pub fn handle_dynamic(value: Dynamic) -> String {
  case dynamic.string(value) {
    Ok(str) -> "String: " <> str
    Error(_) -> case dynamic.int(value) {
      Ok(n) -> "Int: " <> int.to_string(n)
      Error(_) -> "Unknown type"
    }
  }
}

// Decoding Erlang tuples
pub fn decode_tuple(value: Dynamic) ->
  Result(#(String, Int), List(dynamic.DecodeError)) {
  dynamic.tuple2(dynamic.string, dynamic.int)(value)
}

// Decoding Erlang lists
pub fn decode_string_list(value: Dynamic) ->
  Result(List(String), List(dynamic.DecodeError)) {
  dynamic.list(dynamic.string)(value)
}

// Complex Erlang term decoder
pub type Person {
  Person(name: String, age: Int, email: Option(String))
}

pub fn person_decoder() -> dynamic.Decoder(Person) {
  dynamic.decode3(
    Person,
    dynamic.field("name", dynamic.string),
    dynamic.field("age", dynamic.int),
    dynamic.optional_field("email", dynamic.string),
  )
}

pub fn decode_person(value: Dynamic) ->
  Result(Person, List(dynamic.DecodeError)) {
  person_decoder()(value)
}

// Encoding to Erlang terms
pub fn person_to_dynamic(person: Person) -> Dynamic {
  dynamic.from([
    #("name", dynamic.from(person.name)),
    #("age", dynamic.from(person.age)),
    #("email", case person.email {
      Some(email) -> dynamic.from(email)
      None -> dynamic.from(Nil)
    }),
  ])
}

// Working with Erlang records (tuples)
pub fn erlang_record_decoder(
  tag: String,
) -> fn(Dynamic) -> Result(List(Dynamic), List(dynamic.DecodeError)) {
  fn(value) {
    use tuple <- result.try(dynamic.tuple(value))
    use first <- result.try(case list.at(tuple, 0) {
      Ok(elem) -> dynamic.string(elem)
      Error(_) -> Error([dynamic.DecodeError("Expected tuple with string tag", "")])
    })

    case first == tag {
      True -> Ok(list.drop(tuple, 1))
      False -> Error([dynamic.DecodeError("Wrong record tag", "")])
    }
  }
}

// Proplist (Erlang key-value list) handling
pub type Proplist =
  List(#(Dynamic, Dynamic))

pub fn proplist_get(proplist: Proplist, key: String) -> Option(Dynamic) {
  list.find_map(proplist, fn(pair) {
    let #(k, v) = pair
    case dynamic.string(k) {
      Ok(str) if str == key -> Ok(v)
      _ -> Error(Nil)
    }
  })
  |> result.to_option
}

// Atom handling via dynamic
pub fn decode_atom(value: Dynamic) -> Result(String, List(dynamic.DecodeError)) {
  case dynamic.string(value) {
    Ok(str) -> Ok(str)
    Error(_) -> Error([dynamic.DecodeError("Expected atom", "")])
  }
}

// BitString operations
@external(erlang, "erlang", "bit_size")
pub fn bit_size(bits: BitArray) -> Int

pub fn analyze_bitarray(bits: BitArray) -> String {
  let size = bit_size(bits)
  "BitArray of " <> int.to_string(size) <> " bits"
}

// Reference handling
pub opaque type Ref {
  Ref(ref: Dynamic)
}

@external(erlang, "erlang", "make_ref")
fn make_ref() -> Dynamic

pub fn new_reference() -> Ref {
  Ref(ref: make_ref())
}

pub fn compare_refs(a: Ref, b: Ref) -> Bool {
  dynamic.from(a.ref) == dynamic.from(b.ref)
}
```

Dynamic decoders provide safe conversion from Erlang's dynamic types to Gleam's
static types.

## NIFs and Ports

Native Implemented Functions and ports enable integration with C code and
external programs.

```gleam
// NIF declaration
@external(erlang, "my_nif_module", "fast_computation")
pub fn fast_computation(input: Int) -> Int

// Port for external program communication
pub type Port

@external(erlang, "erlang", "open_port")
fn open_port(name: #(Atom, String), options: List(Atom)) -> Port

@external(erlang, "erlang", "port_command")
fn port_command(port: Port, data: BitArray) -> Bool

@external(erlang, "erlang", "port_close")
fn port_close(port: Port) -> Bool

pub fn start_external_program(program: String) -> Port {
  let spawn = atom_from_string("spawn")
  let binary = atom_from_string("binary")
  open_port(#(spawn.atom, program), [binary.atom])
}

pub fn send_to_port(port: Port, data: String) -> Bool {
  let bits = bit_array.from_string(data)
  port_command(port, bits)
}

pub fn close_port(port: Port) -> Bool {
  port_close(port)
}

// Using ports for external processes
pub fn python_integration() {
  let port = start_external_program("python3 script.py")
  send_to_port(port, "input data\n")
  // Receive response
  close_port(port)
}

// NIF loading pattern
@external(erlang, "my_module", "init")
fn init_nif() -> Atom

pub fn load_nif_library() {
  let result = init_nif()
  io.debug(result)
}

// Port with message passing
pub type PortMessage {
  PortData(data: BitArray)
  PortClosed
}

pub fn port_receiver(port: Port) {
  let selector = process.new_selector()
    |> process.selecting(fn(msg) {
      case dynamic.tuple2(dynamic.dynamic, dynamic.dynamic)(dynamic.from(msg)) {
        Ok(#(port_atom, data)) -> {
          case decode_atom(port_atom) {
            Ok("data") -> PortData(bit_array.from_string(""))
            _ -> PortClosed
          }
        }
        Error(_) -> PortClosed
      }
    })

  case process.select(selector, 5000) {
    Ok(PortData(data)) -> {
      io.println("Received data from port")
      port_receiver(port)
    }
    Ok(PortClosed) -> io.println("Port closed")
    Error(_) -> port_receiver(port)
  }
}

// Async NIF scheduling
@external(erlang, "my_nif", "async_computation")
fn async_nif(input: Int, callback: fn(Int) -> Nil) -> Nil

pub fn use_async_nif() {
  async_nif(42, fn(result) {
    io.println("NIF result: " <> int.to_string(result))
  })
}
```

NIFs provide performance-critical native code while ports enable safe external
process communication.

## OTP Integration

Gleam integrates seamlessly with OTP behaviors and supervision trees.

```gleam
// Using Erlang gen_server directly
@external(erlang, "gen_server", "call")
fn gen_server_call(server: process.Pid, request: Dynamic) -> Dynamic

@external(erlang, "gen_server", "cast")
fn gen_server_cast(server: process.Pid, request: Dynamic) -> Nil

// Wrapping Erlang gen_server
pub fn call_server(server: process.Pid, request: String) ->
  Result(String, String) {
  let dynamic_request = dynamic.from(request)
  let response = gen_server_call(server, dynamic_request)
  case dynamic.string(response) {
    Ok(str) -> Ok(str)
    Error(_) -> Error("Invalid response")
  }
}

// Using Erlang supervisor
@external(erlang, "supervisor", "start_link")
fn supervisor_start_link(module: Atom, args: List(Dynamic)) ->
  Result(process.Pid, Dynamic)

// Application behavior
@external(erlang, "application", "start")
fn app_start(name: Atom) -> Result(Atom, Atom)

@external(erlang, "application", "stop")
fn app_stop(name: Atom) -> Result(Atom, Atom)

pub fn start_app(name: String) -> Bool {
  let atom = atom_from_string(name)
  case app_start(atom.atom) {
    Ok(_) -> True
    Error(_) -> False
  }
}

// Using Erlang registry
@external(erlang, "erlang", "register")
fn register_process(name: Atom, pid: process.Pid) -> Bool

@external(erlang, "erlang", "whereis")
fn whereis(name: Atom) -> Result(process.Pid, Nil)

pub fn register(name: String, pid: process.Pid) -> Bool {
  let atom = atom_from_string(name)
  register_process(atom.atom, pid)
}

pub fn find_process(name: String) -> Option(process.Pid) {
  let atom = atom_from_string(name)
  case whereis(atom.atom) {
    Ok(pid) -> Some(pid)
    Error(_) -> None
  }
}

// Global registration
@external(erlang, "global", "register_name")
fn global_register(name: Dynamic, pid: process.Pid) -> Result(Atom, Atom)

pub fn register_globally(name: String, pid: process.Pid) -> Bool {
  case global_register(dynamic.from(name), pid) {
    Ok(_) -> True
    Error(_) -> False
  }
}
```

OTP integration enables building production-grade applications with proven
patterns.

## Best Practices

1. **Wrap external functions with safe interfaces** that handle errors and provide
   Gleam types

2. **Use Dynamic decoders** for all data received from Erlang to ensure type
   safety

3. **Document external function behavior** as Erlang code lacks static type
   information

4. **Handle all Erlang error cases** explicitly rather than assuming success

5. **Use opaque types for Erlang types** that have no direct Gleam equivalent

6. **Test interop boundaries thoroughly** as type mismatches cause runtime errors

7. **Prefer Gleam stdlib over Erlang** when functionality exists in both

8. **Use Result types for fallible Erlang calls** to make errors explicit

9. **Validate data at boundaries** when calling Erlang code with complex
   requirements

10. **Keep interop code isolated** in specific modules for easier maintenance

## Common Pitfalls

1. **Not handling Erlang errors** causes unexpected crashes at runtime

2. **Incorrect type annotations** on external functions lead to type confusion

3. **Forgetting Dynamic decoders** bypasses type safety at Erlang boundaries

4. **Assuming Erlang returns specific types** without validation causes crashes

5. **Not testing with actual Erlang values** misses type mismatch issues

6. **Using Dynamic everywhere** defeats Gleam's type safety benefits

7. **Ignoring Erlang atoms** in response handling causes decoding failures

8. **Not handling Erlang tuple formats** correctly leads to pattern match errors

9. **Forgetting error atoms** from Erlang functions that return ok/error tuples

10. **Blocking on synchronous Erlang calls** can cause process deadlocks

## When to Use This Skill

Apply interop when leveraging existing Erlang libraries unavailable in Gleam.

Use external functions to access Erlang standard library functionality.

Leverage NIFs for performance-critical operations requiring native code.

Integrate with OTP when building production systems requiring proven reliability.

Use ports when communicating with external programs or system commands.

Apply Dynamic decoders when receiving data from Erlang or external systems.

## Resources

- [Gleam External Functions Guide](<https://gleam.run/writing-gleam/external-functions/>)
- [Erlang Reference Manual](<https://www.erlang.org/doc/reference_manual/introduction.html>)
- [Gleam Dynamic Module](<https://hexdocs.pm/gleam_stdlib/gleam/dynamic.html>)
- [Erlang Interoperability Guide](<https://gleam.run/book/tour/external-functions>)
- [BEAM Book](<https://blog.stenmans.org/theBeamBook/>)
