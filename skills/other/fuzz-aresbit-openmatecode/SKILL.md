---
name: fuzz
description: "OCaml fuzz testing with Crowbar for protocol implementations. Use when Claude needs to: (1) Write fuzz tests for parsers and encoders, (2) Test roundtrip invariants (parse(encode(x)) = x), (3) Verify boundary conditions and error handling, (4) Test state machines and transitions, (5) Organize fuzz test suites for large codebases"
license: ISC
---

# OCaml Fuzz Testing with Crowbar

## Core Philosophy

1. **One fuzz file per module**: `fuzz_foo.ml` tests `lib/foo.ml`. Keeps tests organized and discoverable.
2. **Roundtrip everything**: If you have `encode` and `decode`, test `decode(encode(x)) = x`.
3. **Crash-safety first**: Parsers must never crash on arbitrary input, even malformed data.
4. **Boundary conditions matter**: Test edge cases (0, max values, empty input, overflow).
5. **State machines need transition coverage**: Test all valid and invalid state transitions.

## Build Configuration

### Dune setup for fuzz tests

```lisp
(executable
 (name fuzz)
 (libraries crowbar borealis)
 (modules
  fuzz
  fuzz_common
  fuzz_foo
  fuzz_bar))
```

### Main entry point (`fuzz/fuzz.ml`)

```ocaml
(* Force linking of modules that register tests via side effects *)
let () =
  Fuzz_common.run ();
  Fuzz_foo.run ();
  Fuzz_bar.run ()
```

Each fuzz module ends with:

```ocaml
let run () = ()
```

This ensures the module is linked and its `add_test` calls execute.

---

## Test Patterns

### 1. Crash-safety test (parsers must not crash)

```ocaml
open Crowbar
open Fuzz_common

let () =
  add_test ~name:"foo: decode" [ bytes ] @@ fun buf ->
  (match Foo.decode (to_bytes buf) with
   | Ok _ -> ()
   | Error _ -> ());
  check true
```

**Key points**:
- Use `bytes` generator for arbitrary binary input
- Match both `Ok` and `Error` branches (don't crash on either)
- `check true` signals test passed

### 2. Roundtrip test (encode/decode pairs)

```ocaml
let () =
  add_test ~name:"foo: roundtrip" [ bytes ] @@ fun buf ->
  match Foo.decode (to_bytes buf) with
  | Error _ -> check true  (* Invalid input is fine *)
  | Ok original ->
      let encoded = Foo.encode original in
      match Foo.decode encoded with
      | Error _ -> fail "re-decode failed"
      | Ok decoded ->
          if original <> decoded then fail "roundtrip mismatch"
          else check true
```

**Key points**:
- If initial decode fails, that's OK (input was invalid)
- If re-decode fails after encode, that's a bug
- Compare original and decoded values

### 3. Constrained type roundtrip (smart constructors)

```ocaml
(* For types with range constraints like 11-bit APID (0-2047) *)
let () =
  add_test ~name:"apid: roundtrip" [ range 2048 ] @@ fun n ->
  match Apid.of_int n with
  | None -> check (n < 0 || n > 2047)  (* Correctly rejected *)
  | Some apid ->
      let n' = Apid.to_int apid in
      if n <> n' then fail "roundtrip mismatch"
      else check true
```

### 4. Boundary tests

```ocaml
(* Test boundary values explicitly *)
let () =
  add_test ~name:"apid: max_valid" [ const () ] @@ fun () ->
  match Apid.of_int 2047 with
  | None -> fail "2047 should be valid"
  | Some apid ->
      if Apid.to_int apid <> 2047 then fail "value mismatch"
      else check true

let () =
  add_test ~name:"apid: min_valid" [ const () ] @@ fun () ->
  match Apid.of_int 0 with
  | None -> fail "0 should be valid"
  | Some apid ->
      if Apid.to_int apid <> 0 then fail "value mismatch"
      else check true
```

**Key points**:
- Use `[ const () ]` for tests with no random input
- Never use `[]` as generator list (causes type error)

### 5. Invalid input rejection

```ocaml
(* Values above max must be rejected *)
let () =
  add_test ~name:"apid: invalid_above" [ range 1000 ] @@ fun n ->
  let invalid = 2048 + n in
  match Apid.of_int invalid with
  | None -> check true
  | Some _ -> fail "should reject values > 2047"

(* Negative values must be rejected *)
let () =
  add_test ~name:"apid: invalid_negative" [ range 1000 ] @@ fun n ->
  let invalid = -(n + 1) in
  match Apid.of_int invalid with
  | None -> check true
  | Some _ -> fail "should reject negative values"
```

### 6. Pretty-printer safety

```ocaml
(* pp functions must never crash *)
let () =
  add_test ~name:"foo: pp" [ bytes ] @@ fun buf ->
  match Foo.decode (to_bytes buf) with
  | Error _ -> check true
  | Ok v ->
      let _ = Format.asprintf "%a" Foo.pp v in
      check true
```

### 7. State machine transitions

```ocaml
(* Test valid state transitions *)
let () =
  add_test ~name:"key: activate Pending" [ uint8; uint8; bytes ]
  @@ fun kid algo material_buf ->
  let material = to_bytes material_buf in
  if Bytes.length material > 0 then begin
    let key = Key.v ~kid ~algorithm:algo ~material in
    match Key.activate key with
    | Error _ -> check true  (* May fail if material invalid *)
    | Ok active_key ->
        if Key.state active_key <> Key.Active then fail "wrong state"
        else check true
  end
  else check true

(* Test invalid state transitions return errors *)
let () =
  add_test ~name:"key: activate Empty fails" [ uint8; uint8 ]
  @@ fun kid algo ->
  let key = Key.empty ~kid ~algorithm:algo in
  match Key.activate key with
  | Ok _ -> fail "should fail on Empty key"
  | Error (Key.Invalid_state_transition _) -> check true
  | Error _ -> fail "wrong error type"
```

### 8. Unit conversion roundtrips

```ocaml
(* Test all unit conversions *)
let () =
  add_test ~name:"duration: ns_roundtrip" [ int64 ] @@ fun n ->
  let d = Duration.of_ns n in
  let n' = Duration.to_ns d in
  if n <> n' then fail "ns roundtrip mismatch"
  else check true

(* Test cross-unit conversions *)
let () =
  add_test ~name:"duration: us_to_ms" [ range 1000000 ] @@ fun n ->
  let us = Int64.of_int n in
  let d = Duration.of_us us in
  let ms = Duration.to_ms d in
  let expected = Int64.div us 1000L in
  if ms <> expected then fail "us to ms conversion failed"
  else check true
```

### 9. Filestore/resource operations

```ocaml
(* Test create/exists invariant *)
let () =
  add_test ~name:"filestore: create_exists" [ bytes ] @@ fun name_buf ->
  let name = Bytes.to_string (to_bytes name_buf) in
  if String.length name = 0 then check true
  else
    let fs = Filestore.in_memory () in
    match Filestore.create fs name with
    | Error _ -> check true
    | Ok () ->
        if not (Filestore.exists fs name) then
          fail "created file should exist"
        else check true
```

---

## Common Module: fuzz_common.ml

```ocaml
(** Common utilities for fuzz tests. *)

open Crowbar

let to_bytes buf =
  let len = String.length buf in
  let b = Bytes.create len in
  Bytes.blit_string buf 0 b 0 len;
  b

let catch_invalid_arg f =
  try f () with Invalid_argument _ -> check true

let run () = ()
```

---

## Generators Reference

| Generator | Type | Use for |
|-----------|------|---------|
| `bytes` | `string` | Arbitrary binary data |
| `uint8` | `int` | 0-255 |
| `int8` | `int` | -128 to 127 |
| `int32` | `int32` | Full int32 range |
| `int64` | `int64` | Full int64 range |
| `range n` | `int` | 0 to n-1 |
| `bool` | `bool` | true/false |
| `const v` | `'a` | Fixed value (for no-input tests) |
| `list gen` | `'a list` | Lists of generated values |
| `option gen` | `'a option` | Some/None |

---

## File Organization

```
fuzz/
├── fuzz.ml              # Main entry, links all modules
├── fuzz_common.ml       # Shared utilities
├── fuzz_tc_frame.ml     # Tests for lib/frames/tc_frame.ml
├── fuzz_tm_frame.ml     # Tests for lib/frames/tm_frame.ml
├── fuzz_apid.ml         # Tests for lib/frames/apid.ml
├── fuzz_keyid.ml        # Tests for lib/sdls/keyid.ml
└── ...
```

**Naming convention**: `fuzz_<module>.ml` tests `lib/**/<module>.ml`

---

## Running Fuzz Tests

### Without AFL (quick check)

```bash
dune exec fuzz/fuzz.exe
```

### With AFL (thorough fuzzing)

```bash
dune build fuzz/fuzz.exe
mkdir -p fuzz/input
echo -n "" > fuzz/input/empty
afl-fuzz -m none -i fuzz/input -o _fuzz -- \
  _build/default/fuzz/fuzz.exe @@
```

### Check for duplicate test names

```bash
grep -h 'add_test ~name:"' fuzz/fuzz_*.ml | \
  sed 's/.*~name:"\([^"]*\)".*/\1/' | sort | uniq -d
```

---

## Coverage Checklist

For each module with a public API (`.mli` file):

- [ ] **Crash safety**: All `decode_*`, `parse_*`, `read_*`, `of_*` functions
- [ ] **Roundtrip**: All `encode`/`decode`, `to_*`/`of_*` pairs
- [ ] **Boundaries**: Min/max valid values, edge cases
- [ ] **Invalid input**: Values outside valid range rejected
- [ ] **State machines**: All transitions (valid and invalid)
- [ ] **Pretty-printers**: All `pp_*` functions don't crash
- [ ] **Comparison**: `equal` and `compare` are consistent

---

## Priority Order

When adding fuzz tests to a codebase:

1. **Security-critical**: Crypto primitives, authentication, key management
2. **Protocol parsers**: Wire format decoders, frame parsers
3. **State machines**: Lifecycle transitions, session state
4. **Constrained types**: Smart constructors, ID validators
5. **Utility functions**: Encoding helpers, time conversions

---

## Common Mistakes

### Wrong: Empty generator list with function

```ocaml
(* ERROR: This expression should not be a function *)
add_test ~name:"test" [] @@ fun () -> ...
```

### Right: Use `const ()` for no-input tests

```ocaml
add_test ~name:"test" [ const () ] @@ fun () -> ...
```

### Wrong: Ignoring error cases

```ocaml
(* BAD: Only tests happy path *)
add_test ~name:"foo: decode" [ bytes ] @@ fun buf ->
  let Ok v = Foo.decode (to_bytes buf) in
  check true
```

### Right: Handle both Ok and Error

```ocaml
add_test ~name:"foo: decode" [ bytes ] @@ fun buf ->
  (match Foo.decode (to_bytes buf) with
   | Ok _ -> ()
   | Error _ -> ());
  check true
```

### Wrong: Asserting on invalid input

```ocaml
(* BAD: Fails on invalid input *)
add_test ~name:"foo: roundtrip" [ bytes ] @@ fun buf ->
  match Foo.decode (to_bytes buf) with
  | Error _ -> fail "decode failed"  (* Wrong! Invalid input is expected *)
  | Ok v -> ...
```

### Right: Accept invalid input gracefully

```ocaml
add_test ~name:"foo: roundtrip" [ bytes ] @@ fun buf ->
  match Foo.decode (to_bytes buf) with
  | Error _ -> check true  (* Invalid input is fine *)
  | Ok v -> ...
```

---

## Expected Outputs

When adding fuzz tests, produce:

1. **New fuzz file**: `fuzz/fuzz_<module>.ml` with comprehensive tests
2. **Update fuzz.ml**: Add `Fuzz_<module>.run ()` call
3. **Verify build**: `dune build` succeeds
4. **No duplicates**: Test names are unique across all fuzz files
5. **Coverage summary**: List of tests added and what they cover
