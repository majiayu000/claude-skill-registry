---
name: jane-street-functional-trading
description: Build trading systems in the style of Jane Street, the elite market maker known for functional programming and intellectual rigor. Emphasizes OCaml, correctness by construction, real-time systems, and principled risk management. Use when building market making systems, pricing engines, or mission-critical financial software.
---

# Jane Street Style Guide

## Overview

Jane Street is a quantitative trading firm and market maker that trades ~$17 billion daily across equities, bonds, options, and ETFs. Famous for using OCaml (a functional programming language) for nearly all trading infrastructure, they prioritize correctness, expressiveness, and the ability to reason about code.

## Core Philosophy

> "We use OCaml because when you're trading billions of dollars, you want to be able to reason about your code."

> "The type system is your first line of defense. If it compiles, it's probably correct."

> "Make illegal states unrepresentable."

Jane Street believes that in high-stakes systems, the cost of bugs is astronomical. Functional programming, strong typing, and immutability dramatically reduce error rates compared to imperative approaches.

## Design Principles

1. **Correctness by Construction**: Design types so invalid states cannot be represented.

2. **Immutability by Default**: Mutable state is explicit and contained.

3. **Types as Documentation**: The type signature should tell you what a function does.

4. **Explicit Effects**: Side effects are visible in the type system.

5. **Composition Over Inheritance**: Build complex systems from simple, composable parts.

## When Building Trading Systems

### Always

- Make illegal states unrepresentable through types
- Use immutable data structures by default
- Make side effects explicit (IO, mutable state, time)
- Write property-based tests for invariants
- Use sum types (variants) for state machines
- Handle all error cases explicitly (no exceptions for control flow)

### Never

- Use null/None where you can use Option types
- Allow implicit type coercion
- Share mutable state across components
- Ignore compiler warnings
- Use inheritance when composition works
- Leave error cases unhandled

### Prefer

- Pattern matching over if/else chains
- Result types over exceptions
- Pipelines over nested function calls
- Record types over positional arguments
- Modules for abstraction boundaries
- Property-based tests over example-based

## Code Patterns

### Make Illegal States Unrepresentable

```ocaml
(* BAD: Invalid states are possible *)
type order_bad = {
  order_id: string;
  status: string;  (* "pending", "filled", "cancelled"... or typo? *)
  fill_price: float option;
  fill_quantity: int option;
  cancel_reason: string option;
}

(* GOOD: Type system enforces valid states *)
type order_status =
  | Pending of { submitted_at: Time.t }
  | PartiallyFilled of { 
      filled_qty: int; 
      remaining_qty: int; 
      avg_price: Price.t 
    }
  | Filled of { 
      filled_qty: int; 
      avg_price: Price.t; 
      filled_at: Time.t 
    }
  | Cancelled of { 
      reason: cancel_reason; 
      cancelled_at: Time.t 
    }
  | Rejected of { 
      reason: reject_reason 
    }

type order = {
  order_id: Order_id.t;
  symbol: Symbol.t;
  side: Side.t;
  quantity: int;
  price: Price.t;
  status: order_status;
}

(* Now it's impossible to have a Cancelled order with a fill_price *)
```

### Explicit Error Handling with Result Types

```ocaml
(* Jane Street's approach: errors in the type system, not exceptions *)

type 'a order_result = ('a, order_error) Result.t

and order_error =
  | Insufficient_buying_power of { required: Money.t; available: Money.t }
  | Position_limit_exceeded of { limit: int; requested: int }
  | Market_closed
  | Invalid_price of { price: Price.t; reason: string }
  | Risk_check_failed of risk_violation

let submit_order order ~account ~risk_limits : Order_id.t order_result =
  let open Result.Let_syntax in
  
  (* Each check returns Result.t, errors propagate automatically *)
  let%bind () = check_buying_power account order in
  let%bind () = check_position_limits account order risk_limits in
  let%bind () = check_market_hours order.symbol in
  let%bind () = check_price_reasonableness order in
  let%bind () = check_risk_limits order risk_limits in
  
  (* All checks passed, submit *)
  let order_id = Exchange.submit order in
  Ok order_id

(* Caller MUST handle all error cases - compiler enforces it *)
let handle_submission order =
  match submit_order order ~account ~risk_limits with
  | Ok order_id -> 
      Log.info "Order submitted" order_id
  | Error (Insufficient_buying_power { required; available }) ->
      Log.warn "Insufficient funds" required available
  | Error (Position_limit_exceeded { limit; requested }) ->
      Log.warn "Position limit" limit requested
  | Error Market_closed ->
      Log.info "Market closed, queuing for open"
  | Error (Invalid_price { price; reason }) ->
      Log.error "Invalid price" price reason
  | Error (Risk_check_failed violation) ->
      Risk_alerts.trigger violation
```

### Pricing Engine with Pure Functions

```ocaml
(* Jane Street's pricing: pure functions, easy to test and reason about *)

module Black_scholes : sig
  type inputs = {
    spot: Price.t;
    strike: Price.t;
    time_to_expiry: float;  (* years *)
    volatility: float;
    risk_free_rate: float;
    dividend_yield: float;
  }

  type greeks = {
    delta: float;
    gamma: float;
    theta: float;
    vega: float;
    rho: float;
  }

  (* Pure function: same inputs always give same outputs *)
  val price : inputs -> call_or_put:Side.t -> Price.t
  val greeks : inputs -> call_or_put:Side.t -> greeks
  val implied_vol : inputs -> market_price:Price.t -> call_or_put:Side.t -> float option
end = struct
  let cdf x = (* Normal CDF *) ...
  let pdf x = (* Normal PDF *) ...

  let d1 { spot; strike; time_to_expiry = t; volatility = σ; risk_free_rate = r; dividend_yield = q } =
    let s = Price.to_float spot in
    let k = Price.to_float strike in
    (Float.log (s /. k) +. (r -. q +. σ *. σ /. 2.) *. t) /. (σ *. Float.sqrt t)

  let d2 inputs =
    d1 inputs -. inputs.volatility *. Float.sqrt inputs.time_to_expiry

  let price inputs ~call_or_put =
    let d1 = d1 inputs in
    let d2 = d2 inputs in
    let s = Price.to_float inputs.spot in
    let k = Price.to_float inputs.strike in
    let t = inputs.time_to_expiry in
    let r = inputs.risk_free_rate in
    let q = inputs.dividend_yield in
    
    let price = match call_or_put with
      | Call -> 
          s *. Float.exp (-.q *. t) *. cdf d1 
          -. k *. Float.exp (-.r *. t) *. cdf d2
      | Put -> 
          k *. Float.exp (-.r *. t) *. cdf (-.d2) 
          -. s *. Float.exp (-.q *. t) *. cdf (-.d1)
    in
    Price.of_float price
end
```

### State Machine with Exhaustive Pattern Matching

```ocaml
(* Order lifecycle as explicit state machine *)

type order_event =
  | Ack of { exchange_order_id: string; acked_at: Time.t }
  | Fill of { qty: int; price: Price.t; filled_at: Time.t }
  | Partial_fill of { qty: int; price: Price.t; filled_at: Time.t }
  | Cancel_ack of { cancelled_at: Time.t }
  | Reject of { reason: string; rejected_at: Time.t }

let apply_event (order : order) (event : order_event) : order =
  (* Compiler warns if we don't handle all status × event combinations *)
  match order.status, event with
  
  (* Pending state transitions *)
  | Pending _, Ack { exchange_order_id; acked_at } ->
      { order with status = Acknowledged { exchange_order_id; acked_at } }
  | Pending _, Reject { reason; rejected_at } ->
      { order with status = Rejected { reason; rejected_at } }
  | Pending _, (Fill _ | Partial_fill _ | Cancel_ack _) ->
      (* Invalid: can't fill before ack *)
      Log.error "Invalid event for pending order";
      order
  
  (* Acknowledged state transitions *)
  | Acknowledged _, Fill { qty; price; filled_at } ->
      { order with status = Filled { qty; avg_price = price; filled_at } }
  | Acknowledged _, Partial_fill { qty; price; filled_at } ->
      { order with status = PartiallyFilled { 
          filled_qty = qty; 
          remaining_qty = order.quantity - qty;
          avg_price = price 
        } 
      }
  | Acknowledged _, Cancel_ack { cancelled_at } ->
      { order with status = Cancelled { reason = User_requested; cancelled_at } }
  
  (* Already terminal - no transitions *)
  | (Filled _ | Cancelled _ | Rejected _), _ ->
      Log.warn "Event received for terminal order";
      order
```

### Real-Time Pricing Pipeline

```ocaml
(* Incremental computation for real-time pricing *)

module Incremental = struct
  (* Jane Street's Incremental library: recompute only what changed *)
  
  type 'a t  (* Incrementally computed value *)
  
  val map : 'a t -> f:('a -> 'b) -> 'b t
  val map2 : 'a t -> 'b t -> f:('a -> 'b -> 'c) -> 'c t
  val bind : 'a t -> f:('a -> 'b t) -> 'b t
end

let build_pricing_graph ~market_data ~positions =
  let open Incremental.Let_syntax in
  
  (* When spot price changes, only recompute affected options *)
  let%bind spot_prices = market_data.spots in
  let%bind vol_surface = market_data.implied_vols in
  let%bind positions = positions in
  
  (* Compute Greeks for each position *)
  let position_greeks = 
    List.map positions ~f:(fun pos ->
      let%map spot = Map.find_exn spot_prices pos.underlying
      and vol = Vol_surface.get vol_surface ~strike:pos.strike ~expiry:pos.expiry
      in
      let inputs = { spot; strike = pos.strike; volatility = vol; ... } in
      { position = pos; greeks = Black_scholes.greeks inputs }
    )
  in
  
  (* Aggregate to portfolio level *)
  let%map position_greeks = Incremental.all position_greeks in
  aggregate_greeks position_greeks
```

### Property-Based Testing

```ocaml
(* Jane Street uses property-based testing extensively *)

let%test_unit "order matching is fair" =
  Quickcheck.test
    (Quickcheck.Generator.tuple2
      Order.quickcheck_generator
      Order.quickcheck_generator)
    ~f:(fun (order1, order2) ->
      (* Property: if order1 arrived before order2 at same price,
         order1 should fill first *)
      if Price.equal order1.price order2.price
         && Time.( < ) order1.timestamp order2.timestamp
      then begin
        let fills = Matching_engine.match_orders [order1; order2] in
        assert (List.hd fills |> Option.map ~f:(fun f -> f.order_id) 
                = Some order1.order_id)
      end
    )

let%test_unit "Greeks are consistent" =
  Quickcheck.test Black_scholes.Inputs.quickcheck_generator ~f:(fun inputs ->
    let call_price = Black_scholes.price inputs ~call_or_put:Call in
    let put_price = Black_scholes.price inputs ~call_or_put:Put in
    
    (* Put-call parity must hold *)
    let parity_diff = 
      Float.abs (
        Price.to_float call_price -. Price.to_float put_price
        -. (Price.to_float inputs.spot -. Price.to_float inputs.strike 
            *. Float.exp (-.inputs.risk_free_rate *. inputs.time_to_expiry))
      )
    in
    assert (parity_diff < 0.0001)
  )
```

## Mental Model

Jane Street approaches trading systems by asking:

1. **What are the states?** Model them as sum types
2. **What transitions are valid?** Encode in the type system
3. **What can go wrong?** Return Result types, not exceptions
4. **Is it testable?** Pure functions, property-based tests
5. **Can I reason about it?** If the code is confusing, redesign it

## Signature Jane Street Moves

- OCaml for trading systems
- Make illegal states unrepresentable
- Sum types for state machines
- Result types over exceptions
- Pure functions for calculations
- Incremental computation for real-time
- Property-based testing
- Module signatures for abstraction
- Immutable by default
