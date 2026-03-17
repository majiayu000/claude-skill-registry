---
name: typeclass-design
description: Implement typeclasses with curried signatures and dual APIs for both data-first and data-last usage
---

# Typeclass Design Skill

Use this skill when implementing typeclasses that provide reusable abstractions across multiple types.

## Pattern: Curried Typeclass Functions

All typeclass functions must be **fully curried** to enable partial application:

```typescript
import { Function } from "effect"

// Create a typeclass function that takes the typeclass instance first,
// then curries out all other parameters
export const isMoreThan =
  <A>(D: Durable<A>) =>
  (minimum: Duration.DurationInput) =>
  (self: A): boolean => {
    const current = D.getDuration(self)
    return Duration.greaterThanOrEqualTo(current, minimum)
  }
```

## Pattern: Dual APIs

Provide both **data-first** (uncurried) and **data-last** (curried) variants using `Function.dual`:

```typescript
import { Function } from "effect"

export const isMoreThan = <A>(D: Durable<A>) =>
  Function.dual<
    // Data-last (curried) - pipe-friendly
    (minimum: Duration.DurationInput) => (self: A) => boolean,
    // Data-first (uncurried) - direct call
    (self: A, minimum: Duration.DurationInput) => boolean
  >(
    2,  // Number of arguments for data-first form
    (self: A, minimum: Duration.DurationInput): boolean => {
      const current = D.getDuration(self)
      return Duration.greaterThanOrEqualTo(current, minimum)
    }
  )
```

## Usage Patterns

The dual API enables both styles:

```typescript
import { pipe } from "effect/Function"
import * as Duration from "effect/Duration"

// Data-first: Direct function call
const hasMinimum = isMoreThan(Appointment.Durable)(
  appointment,
  Duration.hours(1)
)

// Data-last: Pipe-friendly
const hasMinimum = pipe(
  appointment,
  isMoreThan(Appointment.Durable)(Duration.hours(1))
)

// Partial application for filtering
const longAppointments = appointments.filter(
  isMoreThan(Appointment.Durable)(Duration.hours(1))
)
```

## Complete Typeclass Example

```typescript
import { Function, Duration, Order } from "effect"

/**
 * Typeclass for types that have a duration.
 */
export interface Durable<A> {
  readonly getDuration: (self: A) => Duration.Duration
  readonly setDuration: (self: A, duration: Duration.DurationInput) => A
}

/**
 * Create a Durable instance.
 */
export const make = <A>(
  getDuration: (self: A) => Duration.Duration,
  setDuration: (self: A, duration: Duration.DurationInput) => A
): Durable<A> => ({
  getDuration,
  setDuration
})

/**
 * Check if duration is more than minimum.
 */
export const isMoreThan = <A>(D: Durable<A>) =>
  Function.dual<
    (minimum: Duration.DurationInput) => (self: A) => boolean,
    (self: A, minimum: Duration.DurationInput) => boolean
  >(
    2,
    (self: A, minimum: Duration.DurationInput): boolean =>
      Duration.greaterThanOrEqualTo(
        D.getDuration(self),
        Duration.decode(minimum)
      )
  )

/**
 * Order by duration.
 */
export const OrderByDuration = <A>(D: Durable<A>): Order.Order<A> =>
  Order.mapInput(Duration.Order, (self: A) => D.getDuration(self))
```

## When to Use

- Creating reusable abstractions (Schedulable, Durable, Priceable)
- Implementing operations that work across multiple types
- Providing composable, pipe-friendly APIs
- Enabling partial application for filtering/mapping

## Key Principles

1. **Curry everything** - Enable partial application
2. **Dual APIs always** - Support both usage styles
3. **Typeclass first** - First parameter is always the typeclass instance
4. **Type lambda for HKT** - Use TypeLambda pattern when needed
