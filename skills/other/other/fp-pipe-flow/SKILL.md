---
name: fp-pipe-flow
description: Master function composition in fp-ts using pipe and flow for building
  elegant, type-safe data transformation pipelines
version: 1.0.0
author: Claude
tags:
- fp-ts
- functional-programming
- typescript
- composition
- pipe
- flow
- data-transformation
risk: safe
source: community
license: MIT
---

# fp-ts Pipe and Flow Composition

Function composition is the heart of functional programming. fp-ts provides two powerful utilities for composing functions: `pipe` and `flow`. This guide covers everything you need to build elegant, type-safe pipelines.

## Imports

```typescript
import { pipe, flow, identity } from 'fp-ts/function'
```

## Understanding Pipe vs Flow

### pipe: Immediate Execution with a Starting Value

`pipe` takes a value and passes it through a series of functions, executing immediately.

```typescript
// pipe(value, fn1, fn2, fn3) === fn3(fn2(fn1(value)))

const result = pipe(
  5,
  n => n * 2,      // 10
  n => n + 1,      // 11
  n => `Result: ${n}` // "Result: 11"
)
```

**Use pipe when:**
- You have a value and want to transform it immediately
- Building one-off transformations
- Working with fp-ts data types (Option, Either, Task, etc.)
- You need readable, top-to-bottom data flow

### flow: Creating Reusable Pipelines

`flow` composes functions into a new function without executing them.

```typescript
// flow(fn1, fn2, fn3) === (x) => fn3(fn2(fn1(x)))

const processNumber = flow(
  (n: number) => n * 2,
  n => n + 1,
  n => `Result: ${n}`
)

processNumber(5)  // "Result: 11"
processNumber(10) // "Result: 21"
```

**Use flow when:**
- Creating reusable transformations
- Defining functions to pass as callbacks
- Building composable utilities
- You don't have the input value yet

## Quick Comparison

| Aspect | pipe | flow |
|--------|------|------|
| Execution | Immediate | Deferred |
| First argument | Value | Function |
| Returns | Transformed value | New function |
| Use case | Transform data now | Create reusable transform |

```typescript
// These are equivalent:
const result1 = pipe(5, double, increment, toString)
const result2 = flow(double, increment, toString)(5)
```

## Working with Different Arities

### Unary Functions (Single Argument)

Most fp-ts operations return unary functions, making them ideal for composition.

```typescript
import { pipe } from 'fp-ts/function'
import * as A from 'fp-ts/Array'

const numbers = [1, 2, 3, 4, 5]

const result = pipe(
  numbers,
  A.filter(n => n % 2 === 0),
  A.map(n => n * 10)
)
// [20, 40]
```

### Handling Multi-Argument Functions

When you need to use functions with multiple arguments, use currying or partial application.

```typescript
// Method 1: Inline arrow function
const add = (a: number, b: number) => a + b

pipe(
  5,
  n => add(n, 10), // Wrap in arrow function
  n => n * 2
)

// Method 2: Curried version
const addCurried = (b: number) => (a: number) => a + b

pipe(
  5,
  addCurried(10), // Clean composition
  n => n * 2
)

// Method 3: Using fp-ts curry utilities
import { curry2 } from 'fp-ts-std/Function'

const addC = curry2(add)

pipe(
  5,
  addC(10),
  n => n * 2
)
```

## Data Transformation Pipelines

### Array Transformations

```typescript
import { pipe } from 'fp-ts/function'
import * as A from 'fp-ts/Array'
import * as NEA from 'fp-ts/NonEmptyArray'

interface User {
  id: number
  name: string
  age: number
  active: boolean
}

const users: User[] = [
  { id: 1, name: 'Alice', age: 30, active: true },
  { id: 2, name: 'Bob', age: 25, active: false },
  { id: 3, name: 'Charlie', age: 35, active: true },
]

// Complex transformation pipeline
const activeUserNames = pipe(
  users,
  A.filter(u => u.active),
  A.map(u => u.name),
  A.sort(S.Ord)
)
// ['Alice', 'Charlie']

// With grouping
import * as R from 'fp-ts/Record'
import * as S from 'fp-ts/string'

const usersByActiveStatus = pipe(
  users,
  A.groupBy(u => u.active ? 'active' : 'inactive')
)
// { active: [...], inactive: [...] }
```

### Record/Object Transformations

```typescript
import { pipe } from 'fp-ts/function'
import * as R from 'fp-ts/Record'

const scores: Record<string, number> = {
  alice: 85,
  bob: 92,
  charlie: 78
}

const adjustedScores = pipe(
  scores,
  R.map(score => score * 1.1),
  R.filter(score => score >= 85)
)
```

### String Transformations

```typescript
import { pipe, flow } from 'fp-ts/function'
import * as S from 'fp-ts/string'

const normalizeString = flow(
  S.trim,
  S.toLowerCase,
  s => s.replace(/\s+/g, '-')
)

const slug = normalizeString('  Hello World  ') // 'hello-world'

// With validation
import * as O from 'fp-ts/Option'

const safeSlug = flow(
  O.fromPredicate((s: string) => s.length > 0),
  O.map(normalizeString)
)
```

## Composing with fp-ts Data Types

### With Option

```typescript
import { pipe } from 'fp-ts/function'
import * as O from 'fp-ts/Option'

interface Config {
  database?: {
    host?: string
    port?: number
  }
}

const getConnectionString = (config: Config): O.Option<string> =>
  pipe(
    O.fromNullable(config.database),
    O.flatMap(db => O.fromNullable(db.host)),
    O.map(host => `postgresql://${host}`)
  )

// Chaining multiple Option operations
const findUser = (id: number): O.Option<User> => { /* ... */ }
const getUserEmail = (user: User): O.Option<string> => { /* ... */ }
const validateEmail = (email: string): O.Option<string> => { /* ... */ }

const getValidatedEmail = (userId: number): O.Option<string> =>
  pipe(
    findUser(userId),
    O.flatMap(getUserEmail),
    O.flatMap(validateEmail)
  )
```

### With Either

```typescript
import { pipe } from 'fp-ts/function'
import * as E from 'fp-ts/Either'

type ValidationError = { type: 'validation'; message: string }
type NetworkError = { type: 'network'; message: string }
type AppError = ValidationError | NetworkError

const validateAge = (age: number): E.Either<ValidationError, number> =>
  age >= 0 && age <= 150
    ? E.right(age)
    : E.left({ type: 'validation', message: 'Invalid age' })

const validateName = (name: string): E.Either<ValidationError, string> =>
  name.length >= 2
    ? E.right(name)
    : E.left({ type: 'validation', message: 'Name too short' })

// Sequential validation (fail on first error)
const validateUser = (name: string, age: number) =>
  pipe(
    E.Do,
    E.bind('name', () => validateName(name)),
    E.bind('age', () => validateAge(age)),
    E.map(({ name, age }) => ({ name, age, createdAt: new Date() }))
  )

// Accumulating errors with Validation
import * as A from 'fp-ts/Apply'
import * as NEA from 'fp-ts/NonEmptyArray'

type ValidationErrors = NEA.NonEmptyArray<string>
type Validation<A> = E.Either<ValidationErrors, A>

const applicativeValidation = E.getApplicativeValidation(NEA.getSemigroup<string>())

const validateUserAll = (name: string, age: number) =>
  pipe(
    A.sequenceS(applicativeValidation)({
      name: validateName(name),
      age: validateAge(age)
    }),
    E.map(({ name, age }) => ({ name, age }))
  )
```

### With Task and TaskEither

```typescript
import { pipe } from 'fp-ts/function'
import * as T from 'fp-ts/Task'
import * as TE from 'fp-ts/TaskEither'

// Composing async operations
const fetchUser = (id: number): TE.TaskEither<Error, User> =>
  TE.tryCatch(
    () => fetch(`/api/users/${id}`).then(r => r.json()),
    (error) => new Error(String(error))
  )

const fetchUserPosts = (userId: number): TE.TaskEither<Error, Post[]> =>
  TE.tryCatch(
    () => fetch(`/api/users/${userId}/posts`).then(r => r.json()),
    (error) => new Error(String(error))
  )

const getUserWithPosts = (id: number): TE.TaskEither<Error, UserWithPosts> =>
  pipe(
    fetchUser(id),
    TE.flatMap(user =>
      pipe(
        fetchUserPosts(user.id),
        TE.map(posts => ({ ...user, posts }))
      )
    )
  )

// Parallel execution
import * as A from 'fp-ts/Array'

const fetchAllUsers = (ids: number[]): TE.TaskEither<Error, User[]> =>
  pipe(
    ids,
    A.map(fetchUser),
    A.sequence(TE.ApplicativePar) // Parallel execution
  )
```

### With Reader and ReaderTaskEither

```typescript
import { pipe } from 'fp-ts/function'
import * as RTE from 'fp-ts/ReaderTaskEither'

interface Dependencies {
  userRepo: UserRepository
  emailService: EmailService
  logger: Logger
}

const getUser = (id: number): RTE.ReaderTaskEither<Dependencies, Error, User> =>
  pipe(
    RTE.ask<Dependencies>(),
    RTE.flatMapTaskEither(deps => deps.userRepo.findById(id))
  )

const sendWelcomeEmail = (user: User): RTE.ReaderTaskEither<Dependencies, Error, void> =>
  pipe(
    RTE.ask<Dependencies>(),
    RTE.flatMapTaskEither(deps => deps.emailService.send(user.email, 'Welcome!'))
  )

const onboardUser = (id: number): RTE.ReaderTaskEither<Dependencies, Error, User> =>
  pipe(
    getUser(id),
    RTE.tap(sendWelcomeEmail),
    RTE.tap(user =>
      RTE.fromTask(deps => deps.logger.info(`Onboarded: ${user.name}`))
    )
  )
```

## Best Practices for Readable Pipelines

### 1. Keep Functions Small and Focused

```typescript
// Good: Each step does one thing
const processOrder = pipe(
  order,
  validateOrder,
  calculateTotals,
  applyDiscounts,
  formatForDisplay
)

// Avoid: Large inline functions
const processOrder = pipe(
  order,
  o => {
    // 50 lines of validation, calculation, and formatting
  }
)
```

### 2. Extract Named Functions for Clarity

```typescript
// Good: Named functions explain intent
const isAdult = (user: User) => user.age >= 18
const formatName = (user: User) => `${user.firstName} ${user.lastName}`

const adultNames = pipe(
  users,
  A.filter(isAdult),
  A.map(formatName)
)

// Less clear: Anonymous functions inline
const adultNames = pipe(
  users,
  A.filter(u => u.age >= 18),
  A.map(u => `${u.firstName} ${u.lastName}`)
)
```

### 3. Use flow for Reusable Transformations

```typescript
// Define reusable pipelines
const normalizeEmail = flow(
  S.trim,
  S.toLowerCase
)

const validateEmailFormat = flow(
  O.fromPredicate((s: string) => s.includes('@')),
  O.filter(s => s.length >= 5)
)

// Compose them
const processEmail = flow(
  normalizeEmail,
  validateEmailFormat
)
```

### 4. Group Related Operations

```typescript
// Good: Logical grouping with comments
const processUsers = pipe(
  users,
  // Filter
  A.filter(isActive),
  A.filter(isVerified),
  // Transform
  A.map(enrichWithMetadata),
  A.map(formatForAPI),
  // Sort
  A.sort(byCreatedAt)
)
```

### 5. Handle Errors at Appropriate Levels

```typescript
// Good: Handle errors where you can meaningfully respond
const getUserSafely = (id: number) =>
  pipe(
    fetchUser(id),
    TE.mapLeft(toAppError),
    TE.orElse(error =>
      error.type === 'not_found'
        ? TE.right(defaultUser)
        : TE.left(error)
    )
  )
```

### 6. Use Do Notation for Complex Dependencies

```typescript
// Good: Clear when steps depend on previous results
const createOrder = pipe(
  E.Do,
  E.bind('user', () => validateUser(userData)),
  E.bind('items', () => validateItems(itemsData)),
  E.bind('shipping', ({ user }) => calculateShipping(user.address)),
  E.bind('total', ({ items, shipping }) => calculateTotal(items, shipping)),
  E.map(({ user, items, total }) => ({ user, items, total }))
)
```

## Common Composition Patterns

### Pattern 1: Transform and Validate

```typescript
const processInput = flow(
  S.trim,
  O.fromPredicate(s => s.length > 0),
  O.map(S.toLowerCase),
  O.filter(isValidFormat)
)
```

### Pattern 2: Fetch, Transform, Persist

```typescript
const syncUser = (id: number) =>
  pipe(
    fetchExternalUser(id),
    TE.map(transformToInternalUser),
    TE.flatMap(saveUser),
    TE.map(user => ({ success: true, user }))
  )
```

### Pattern 3: Parallel with Aggregation

```typescript
const fetchDashboardData = pipe(
  TE.Do,
  TE.apS('users', fetchUsers()),
  TE.apS('orders', fetchOrders()),
  TE.apS('metrics', fetchMetrics()),
  TE.map(({ users, orders, metrics }) =>
    buildDashboard(users, orders, metrics)
  )
)
```

### Pattern 4: Sequential with Early Exit

```typescript
const processPayment = (paymentData: PaymentData) =>
  pipe(
    validatePayment(paymentData),
    TE.flatMap(checkFunds),
    TE.flatMap(reserveFunds),
    TE.flatMap(processTransaction),
    TE.flatMap(sendConfirmation)
  )
```

### Pattern 5: Fallback Chain

```typescript
const getConfig = pipe(
  getEnvConfig(),
  O.alt(() => getFileConfig()),
  O.alt(() => getDefaultConfig()),
  O.getOrElse(() => hardcodedDefaults)
)
```

### Pattern 6: Conditional Branching

```typescript
const processUser = (user: User) =>
  pipe(
    user,
    O.fromPredicate(isAdmin),
    O.match(
      () => processRegularUser(user),
      () => processAdminUser(user)
    )
  )
```

### Pattern 7: Accumulate Results

```typescript
const processAll = (items: Item[]) =>
  pipe(
    items,
    A.map(processItem),
    A.separate, // Split into { left: errors[], right: successes[] }
    ({ left: errors, right: successes }) => ({
      successes,
      errors,
      successRate: successes.length / items.length
    })
  )
```

## Type Inference Tips

### Let TypeScript Infer When Possible

```typescript
// Good: Types flow through
const result = pipe(
  users,
  A.filter(u => u.active), // TypeScript knows u is User
  A.map(u => u.name)       // TypeScript knows result is string[]
)

// Only annotate when necessary
const processNumber = flow(
  (n: number) => n * 2,  // First function needs annotation
  n => n + 1,            // Rest are inferred
  String
)
```

### Use Explicit Types for Public APIs

```typescript
// Good: Clear contract for public function
const processOrder: (order: Order) => E.Either<OrderError, ProcessedOrder> =
  flow(
    validateOrder,
    E.flatMap(calculateTotals),
    E.map(formatOrder)
  )
```

## Performance Considerations

### pipe vs flow Performance

- `pipe` has minimal overhead - essentially just function calls
- `flow` creates a new function, slight overhead on creation but not on execution
- For hot paths with known values, `pipe` is marginally faster
- For reusable functions, `flow` avoids recreation

### Avoiding Unnecessary Intermediate Arrays

```typescript
// Less efficient: Multiple array iterations
const result = pipe(
  largeArray,
  A.filter(predicate1),
  A.filter(predicate2),
  A.map(transform)
)

// More efficient: Combine predicates
const result = pipe(
  largeArray,
  A.filter(x => predicate1(x) && predicate2(x)),
  A.map(transform)
)

// Or use filterMap for filter + map
const result = pipe(
  largeArray,
  A.filterMap(x =>
    predicate1(x) && predicate2(x)
      ? O.some(transform(x))
      : O.none
  )
)
```

## Debugging Pipelines

### Using tap for Side Effects

```typescript
import { tap } from 'fp-ts/function'

const debugPipeline = pipe(
  data,
  tap(x => console.log('Step 1:', x)),
  transform1,
  tap(x => console.log('Step 2:', x)),
  transform2
)
```

### Using trace Helper

```typescript
const trace = <A>(label: string) => (a: A): A => {
  console.log(label, a)
  return a
}

const result = pipe(
  data,
  trace('input'),
  transform1,
  trace('after transform1'),
  transform2,
  trace('final')
)
```

## Summary

| Use Case | Use `pipe` | Use `flow` |
|----------|------------|------------|
| Transform a value now | Yes | No |
| Create reusable function | No | Yes |
| Pass as callback | No | Yes |
| One-off transformation | Yes | No |
| Build utility library | No | Yes |
| fp-ts operations chain | Yes | Either |

Remember:
- `pipe(value, f, g)` executes immediately
- `flow(f, g)` returns a function for later
- Keep pipeline steps small and focused
- Extract named functions for clarity
- Use Do notation for complex dependencies
- Let TypeScript infer types when possible

## When to Use
- Use this skill when you need for functional programming or specific domain tasks.
