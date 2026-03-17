---
name: domain-predicates
description: Generate comprehensive predicates and orders for domain types using typeclass patterns
---

# Domain Predicates Skill

Generate complete sets of predicates and Order instances for domain types, derived from typeclass implementations.

## Pattern: Equality with Schema.Data

When using schemas, leverage `Schema.Data` for automatic structural equality:

```typescript
import { Schema, Equal } from "effect"

export const Task = Schema.TaggedStruct("pending", {
  id: Schema.String,
  createdAt: Schema.DateTimeUtcFromSelf,
}).pipe(Schema.Data) // Implements Equal.Symbol automatically

// Usage: Automatic structural equality
const task1 = makeTask({ id: "123", createdAt: now })
const task2 = makeTask({ id: "123", createdAt: now })

Equal.equals(task1, task2) // true - structural equality
```

## Pattern: Equivalence from Schema

When you need an `Equivalence` instance (for use with combinators), derive it from the schema:

```typescript
import * as Equivalence from "effect/Equivalence"

// Derive from schema (structural equality)
export const Equivalence = Schema.equivalence(Task)

// Usage with combinators
const uniqueTasks = Array.dedupeWith(tasks, Equivalence)
```

## Pattern: Field-Based Equivalence with Equivalence.mapInput

Compare by specific fields using `Equivalence.mapInput`:

```typescript
import * as Equivalence from "effect/Equivalence"

/**
 * Compare tasks by ID only.
 *
 * @category Equivalence
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import * as Array from "effect/Array"
 *
 * const uniqueById = Array.dedupeWith(tasks, Task.EquivalenceById)
 */
export const EquivalenceById = Equivalence.mapInput(
  Equivalence.string,
  (task: Task) => task.id
)

/**
 * Compare by status tag.
 *
 * @category Equivalence
 * @since 0.1.0
 */
export const EquivalenceByTag = Equivalence.mapInput(
  Equivalence.string,
  (task: Task) => task._tag
)

/**
 * Compare by creation date.
 *
 * @category Equivalence
 * @since 0.1.0
 */
export const EquivalenceByCreatedAt = Equivalence.mapInput(
  DateTime.Equivalence,
  (task: Task) => task.createdAt
)
```

**Key Pattern: Equivalence.mapInput**
- Signature: `Equivalence.mapInput(baseEquivalence, (value) => extractField)`
- Compose from simpler equivalences
- Map domain type to comparable value
- Dual API: data-first and data-last

## Pattern: Combining Equivalences

Use `Equivalence.combine` for multi-field equality:

```typescript
import * as Equivalence from "effect/Equivalence"

/**
 * Compare by tag first, then by ID.
 *
 * Both must match for equivalence.
 *
 * @category Equivalence
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 *
 * const areSame = Task.EquivalenceByTagAndId(task1, task2)
 */
export const EquivalenceByTagAndId = Equivalence.combine(
  EquivalenceByTag,
  EquivalenceById
)

/**
 * Compare by multiple criteria for exact equality.
 *
 * @category Equivalence
 * @since 0.1.0
 */
export const EquivalenceComplete = Equivalence.combine(
  EquivalenceByTag,
  EquivalenceById,
  EquivalenceByCreatedAt
)
```

**Key Pattern: Equivalence.combine**
- Combines multiple equivalences
- All must match for equivalence (AND logic)
- Order doesn't matter (unlike Order.combine)

## Pattern: Typeclass-Derived Predicates

When a domain type implements a typeclass, re-export all relevant predicates:

```typescript
import * as Schedulable$ from "@/typeclass/Schedulable"
import * as Durable$ from "@/typeclass/Durable"
import * as Order from "effect/Order"

// Create typeclass instances
export const Schedulable = Schedulable$.make<Appointment>(
  (self) => self.date,
  (self, date) => Appointment.make({ ...self, date: DateTime.toUtc(date) })
)

export const Durable = Durable$.make<Appointment>(
  (self) => self.duration,
  (self, duration) => Appointment.make({ ...self, duration: Duration.decode(duration) })
)

// Re-export all Schedulable predicates
export const isScheduledBefore = Schedulable$.isScheduledBefore(Schedulable)
export const isScheduledAfter = Schedulable$.isScheduledAfter(Schedulable)
export const isScheduledBetween = Schedulable$.isScheduledBetween(Schedulable)
export const isScheduledOn = Schedulable$.isScheduledOn(Schedulable)
export const isScheduledToday = Schedulable$.isScheduledToday(Schedulable)
export const isScheduledThisWeek = Schedulable$.isScheduledThisWeek(Schedulable)
export const isScheduledThisMonth = Schedulable$.isScheduledThisMonth(Schedulable)

// Re-export all Durable predicates
export const hasMinimumDuration = Durable$.isMoreThan(Durable)
export const hasMaximumDuration = Durable$.isLessThan(Durable)
export const hasDurationBetween = Durable$.isBetween(Durable)
export const hasExactDuration = Durable$.hasExactDuration(Durable)
```

## Pattern: Order Instances with Order.mapInput

Compose orders from simpler base orders using `Order.mapInput`:

```typescript
import * as Order from "effect/Order"
import * as DateTime from "effect/DateTime"
import * as String from "effect/String"

/**
 * Order by ID using Order.mapInput.
 *
 * @category Orders
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import * as Array from "effect/Array"
 *
 * const sorted = Array.sort(tasks, Task.OrderById)
 */
export const OrderById: Order.Order<Task> =
  Order.mapInput(Order.string, (task) => task.id)

/**
 * Order by creation date.
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderByCreatedAt: Order.Order<Task> =
  Order.mapInput(DateTime.Order, (task) => task.createdAt)

/**
 * Order by status tag.
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderByTag: Order.Order<Task> =
  Order.mapInput(Order.string, (task) => task._tag)

/**
 * Order by priority (domain-specific logic).
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderByPriority: Order.Order<Task> =
  Order.mapInput(Order.number, (task) => {
    const priorities = { pending: 0, active: 1, completed: 2 }
    return priorities[task._tag]
  })
```

**Key Pattern: Order.mapInput**
- Signature: `Order.mapInput(baseOrder, (value) => extractField)`
- Compose from existing orders (Order.string, Order.number, DateTime.Order, etc.)
- Map domain type to comparable value
- Dual API: data-first and data-last

## Pattern: Combining Orders with Order.combine

Use `Order.combine` for multi-criteria sorting:

```typescript
import * as Order from "effect/Order"

/**
 * Sort by priority first, then by creation date.
 *
 * @category Orders
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import * as Array from "effect/Array"
 *
 * // High priority tasks first, then by oldest
 * const sorted = Array.sort(tasks, Task.OrderByPriorityThenDate)
 */
export const OrderByPriorityThenDate: Order.Order<Task> = Order.combine(
  OrderByPriority,
  OrderByCreatedAt
)

/**
 * Sort by tag, then ID, then creation date.
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderComplex: Order.Order<Task> = Order.combine(
  OrderByTag,
  OrderById,
  OrderByCreatedAt
)
```

**Key Pattern: Order.combine**
- Combines multiple orders for multi-criteria sorting
- First order takes precedence, then second, etc.
- Order matters (unlike Equivalence.combine)
- Returns combined order that can be used with Array.sort

## Pattern: Comprehensive Order Instances

Provide extensive sorting capabilities:

```typescript
// Schedulable orders (temporal sorting)
export const OrderByScheduledTime = Schedulable$.OrderByScheduledTime(Schedulable)
export const OrderByDayOfWeek = Schedulable$.OrderByDayOfWeek(Schedulable)
export const OrderByTimeOfDay = Schedulable$.OrderByTimeOfDay(Schedulable)
export const OrderByHour = Schedulable$.OrderByHour(Schedulable)
export const OrderByMonth = Schedulable$.OrderByMonth(Schedulable)
export const OrderByYear = Schedulable$.OrderByYear(Schedulable)
export const OrderByYearMonth = Schedulable$.OrderByYearMonth(Schedulable)
export const OrderByDateOnly = Schedulable$.OrderByDateOnly(Schedulable)
export const OrderByDayPeriod = Schedulable$.OrderByDayPeriod(Schedulable)
export const OrderByBusinessHours = Schedulable$.OrderByBusinessHours(Schedulable)
export const OrderByWeekdayFirst = Schedulable$.OrderByWeekdayFirst(Schedulable)

// Durable orders (duration sorting)
export const OrderByDuration = Durable$.OrderByDuration(Durable)
export const OrderByHours = Durable$.OrderByHours(Durable)
export const OrderByMinutes = Durable$.OrderByMinutes(Durable)
export const OrderBySeconds = Durable$.OrderBySeconds(Durable)

// Domain-specific orders using Order.mapInput
export const OrderByStatus: Order.Order<Appointment> =
  Order.mapInput(String.Order, (appt) => appt.status)

export const OrderByStatusPriority: Order.Order<Appointment> =
  Order.mapInput(Order.number, (appt) => {
    const priorities: Record<AppointmentStatus, number> = {
      scheduled: 0,
      confirmed: 1,
      completed: 2,
      cancelled: 3,
    }
    return priorities[appt.status]
  })

// Combined orders for complex sorting
export const OrderByStatusThenTime: Order.Order<Appointment> = Order.combine(
  OrderByStatusPriority,
  OrderByScheduledTime
)
```

## Usage Examples

### Equality Examples

```typescript
import { Equal } from "effect"
import * as Task from "@/schemas/Task"
import * as Array from "effect/Array"

// Structural equality (automatic from Schema.Data)
const areSame = Equal.equals(task1, task2)

// Deduplicate by ID only
const uniqueById = Array.dedupeWith(tasks, Task.EquivalenceById)

// Deduplicate by tag and ID
const uniqueByTagAndId = Array.dedupeWith(tasks, Task.EquivalenceByTagAndId)

// Find if array contains equivalent task
const hasTask = Array.containsWith(tasks, Task.EquivalenceById)(searchTask)
```

### Filtering Examples

Document how these predicates enable powerful filtering:

```typescript
/**
 * Filter appointments scheduled before a date.
 *
 * @example
 * import * as Appointment from "@/schemas/Appointment"
 * import * as DateTime from "effect/DateTime"
 * import * as Duration from "effect/Duration"
 * import * as Array from "effect/Array"
 * import { pipe } from "effect/Function"
 *
 * const tomorrow = DateTime.addDuration(
 *   DateTime.unsafeNow(),
 *   Duration.days(1)
 * )
 *
 * const beforeTomorrow = pipe(
 *   appointments,
 *   Array.filter(Appointment.isScheduledBefore(tomorrow))
 * )
 */
```

### Sorting Examples

```typescript
import * as Array from "effect/Array"
import * as Order from "effect/Order"
import { pipe } from "effect/Function"

// Simple sort by single field
const sortedById = Array.sort(tasks, Task.OrderById)

// Multi-criteria sort
const sortedComplex = Array.sort(
  tasks,
  Order.combine(
    Task.OrderByPriority,
    Task.OrderByCreatedAt
  )
)

// Sort with filter
const sortedFiltered = pipe(
  tasks,
  Array.filter(Task.isPending),
  Array.sort(Task.OrderByCreatedAt)
)
```

## Pattern: Complex Filtering

Combine predicates for sophisticated queries:

```typescript
import { pipe } from "effect/Function"
import * as Array from "effect/Array"

// Find long appointments this week
const longThisWeek = pipe(
  appointments,
  Array.filter(Appointment.isScheduledThisWeek),
  Array.filter(Appointment.hasMinimumDuration(Duration.hours(2)))
)

// Sort by multiple criteria
const sorted = pipe(
  appointments,
  Array.filter(Appointment.isScheduledToday),
  Array.sort(
    Order.combine(
      Appointment.OrderByStatusPriority,
      Appointment.OrderByScheduledTime
    )
  )
)

// Deduplicate and sort
const uniqueSorted = pipe(
  appointments,
  Array.dedupeWith(Appointment.EquivalenceById),
  Array.sort(Appointment.OrderByPriorityThenDate)
)
```

## Checklist for Complete Coverage

### Equality
- [ ] Use `Schema.Data` for automatic `Equal.equals()`
- [ ] Export `Schema.equivalence()` when needed for combinators
- [ ] Export field-based equivalences using `Equivalence.mapInput`
- [ ] Export combined equivalences using `Equivalence.combine`

### Orders
- [ ] Export orders for all sortable fields using `Order.mapInput`
- [ ] Export combined orders using `Order.combine`
- [ ] Document which field takes precedence in combined orders

### Schedulable types
- [ ] isScheduledBefore
- [ ] isScheduledAfter
- [ ] isScheduledBetween
- [ ] isScheduledOn
- [ ] isScheduledToday
- [ ] isScheduledThisWeek
- [ ] isScheduledThisMonth
- [ ] All Order instances

### Durable types
- [ ] hasMinimumDuration (isMoreThan)
- [ ] hasMaximumDuration (isLessThan)
- [ ] hasDurationBetween (isBetween)
- [ ] hasExactDuration
- [ ] All Order instances

### Domain-specific fields
- [ ] Predicate for each variant (isPending, isActive, etc.)
- [ ] Order by field value using `Order.mapInput`
- [ ] Order by priority/importance if applicable
- [ ] Combined orders for common sorting patterns

## Documentation Requirements

Every predicate, equivalence, and order MUST have:
- JSDoc description
- @category tag
- @since tag
- @example with realistic usage showing imports and pipe

## Key Patterns Summary

**1. Schema.Data for Equality**
```typescript
Schema.TaggedStruct("task", { ... }).pipe(Schema.Data)
// Usage: Equal.equals(t1, t2)
```

**2. Schema.equivalence() for Combinators**
```typescript
export const Equivalence = Schema.equivalence(Task)
// Usage: Array.dedupeWith(tasks, Equivalence)
```

**3. Equivalence.mapInput for Field-Based**
```typescript
Equivalence.mapInput(Equivalence.string, (t: Task) => t.id)
```

**4. Equivalence.combine for Multi-Field**
```typescript
Equivalence.combine(EquivalenceByTag, EquivalenceById)
```

**5. Order.mapInput for Field-Based Sorting**
```typescript
Order.mapInput(Order.string, (t: Task) => t.id)
```

**6. Order.combine for Multi-Criteria Sorting**
```typescript
Order.combine(OrderByPriority, OrderByDate)
```

This ensures comprehensive equality checking, predicates, and sorting capabilities are discoverable and developers understand how to use them effectively with Effect's compositional patterns.
