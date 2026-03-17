---
name: effects
description: "OCaml 5 algebraic effects design patterns. Use when Claude needs to: (1) Design APIs that interact with effect-based schedulers, (2) Decide between effects vs exceptions, (3) Integrate libraries with Eio or affect, (4) Handle suspension vs error cases in streaming code, (5) Understand the layered effect design principle"
license: ISC
---

# OCaml 5 Effects Design

## Core Principle

**Effects for control flow, exceptions for errors.**

| Concern | Mechanism | Example |
|---------|-----------|---------|
| Suspension (wait for data) | Effects | `perform Block`, `perform Yield` |
| Error (EOF, malformed) | Exceptions | `raise End_of_file`, `Invalid_argument` |

## Layered Design

Effects should be handled at the **source level**, not in protocol parsers:

```
Application
    ↓
Protocol parser (Binary.Reader, Cbor, etc.)
    ↓  raises exceptions on EOF/error
bytesrw (effect-agnostic)
    ↓  just calls pull function
Source (Eio flow, affect fd, Unix fd)
    ↓  performs effects for suspension
Effect handler (Eio scheduler, affect runtime)
```

### Why This Matters

- **Parsers stay pure**: No effect dependencies, easy to test
- **Sources control blocking**: Handler decides wait vs fail vs timeout
- **Composability**: Same parser works with any effect system

## Effect Libraries

### Eio

Effects are internal to the scheduler. User code looks synchronous:

```ocaml
(* Reading blocks via internal effects *)
let data = Eio.Flow.read flow buf
```

### affect

Explicit effects for fiber scheduling:

```ocaml
type _ Effect.t +=
| Block : 'a block -> 'a Effect.t   (* suspension *)
| Await : await -> unit Effect.t    (* wait on fibers *)
| Yield : unit Effect.t             (* cooperative yield *)

(* Block has callbacks for scheduler integration *)
type 'a block = {
  block : handle -> unit;      (* register blocked fiber *)
  cancel : handle -> bool;     (* handle cancellation *)
  return : handle -> 'a        (* extract result *)
}
```

### bytesrw

Effect-agnostic streaming. The pull function you provide can perform any effects:

```ocaml
(* bytesrw just calls your function *)
let reader = Bytesrw.Bytes.Reader.make my_pull_fn

(* If my_pull_fn performs Eio effects, they propagate *)
(* If my_pull_fn performs affect Block, they propagate *)
(* bytesrw doesn't care - it just calls the function *)
```

## Integration Pattern

Wire effect-performing sources to effect-agnostic libraries:

```ocaml
(* With Eio *)
let reader = Bytesrw_eio.bytes_reader_of_flow flow in
let r = Binary.Reader.of_reader reader in
parse r  (* Eio effects happen in pull function *)

(* With affect *)
let pull () =
  let buf = Bytes.create 4096 in
  perform (Block { block; cancel; return = fun _ ->
    Slice.make buf ~first:0 ~length:n })
in
let reader = Bytesrw.Bytes.Reader.make pull in
parse (Binary.Reader.of_reader reader)
```

## When EOF Is Reached

`Slice.eod` from bytesrw means **final EOF** - no more data will ever come.

- Not "data not ready" (that's handled by effects in pull function)
- Not "try again later" (source already waited via effects)
- Parser should raise exception (EOF is an error condition)

## Anti-Patterns

**Don't**: Define `Await` effect in protocol parsers
```ocaml
(* WRONG - parser shouldn't know about suspension *)
let get_byte t =
  if no_data then perform Await; ...
```

**Do**: Let the source handle suspension
```ocaml
(* RIGHT - parser just reads, source handles waiting *)
let get_byte t =
  match pull_next_slice t with  (* may perform effects *)
  | Some slice -> ...
  | None -> raise End_of_file   (* true EOF *)
```

## References

- Eio: https://github.com/ocaml-multicore/eio
- affect: https://github.com/dbuenzli/affect
- bytesrw: https://erratique.ch/software/bytesrw
- OCaml effects tutorial: https://github.com/ocaml-multicore/ocaml-effects-tutorial
- Retrofitting Effect Handlers onto OCaml (PLDI 2021): https://dl.acm.org/doi/10.1145/3453483.3454039
- Collège de France 2023-2024 lectures on control structures: https://xavierleroy.org/CdF/2023-2024/
