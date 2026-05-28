---
name: sharp-edges
description: Identify dangerous API footguns, surprising default behaviors, and sharp edges in codebases and dependencies. Adapted from Trail of Bits. Use during code review to catch APIs that are easy to misuse, configurations that surprise, and abstractions that leak.
---

# Sharp Edges Detection

Sharp edges are APIs, configurations, and patterns that are easy to use incorrectly. They work in the happy path but break in subtle, dangerous ways.

## Three Adversary Types

When evaluating sharp edges, consider three types of users:

### 1. The Naive Developer
- Uses the API without reading docs carefully
- Copies examples from Stack Overflow
- Assumes defaults are safe
- **Question**: "Will this API hurt someone who doesn't know its quirks?"

### 2. The Malicious User
- Intentionally sends unexpected input
- Exploits race conditions and edge cases
- Chains small issues into big exploits
- **Question**: "Can someone deliberately trigger the bad behavior?"

### 3. The Future Maintainer
- Modifies code without full context
- Refactors without understanding invariants
- Doesn't know why something was done a certain way
- **Question**: "Will a reasonable change to this code introduce a bug?"

## Sharp Edge Categories

### 1. Surprising Default Behavior

APIs whose defaults do something unexpected:

```typescript
// SHARP: parseInt without radix
parseInt("08")    // 0 in old engines (octal), 8 in modern
parseInt("08", 10)  // Always 8

// SHARP: Array.sort() without comparator
[10, 2, 1].sort()  // [1, 10, 2] -- sorts as strings!
[10, 2, 1].sort((a, b) => a - b)  // [1, 2, 10]

// SHARP: JSON.parse reviver runs bottom-up
JSON.parse('{"a": {"b": 1}}', (key, val) => {
  // 'b' fires before 'a' -- counterintuitive
})

// SHARP: fetch() doesn't reject on HTTP errors
const res = await fetch('/api')  // 404 doesn't throw!
if (!res.ok) throw new Error(`HTTP ${res.status}`)
```

### 2. Silent Failures

Operations that fail without telling you:

```typescript
// SHARP: Object.freeze is shallow
const obj = Object.freeze({ nested: { value: 1 } })
obj.nested.value = 2  // Succeeds! Only top level is frozen

// SHARP: Map vs Object key coercion
const map = new Map()
map.set(1, 'number')
map.set('1', 'string')
map.get(1)   // 'number' -- Map preserves key types
// But:
const obj = {}
obj[1] = 'number'
obj['1'] = 'string'
obj[1]  // 'string' -- Object coerces keys to strings

// SHARP: Promise.all fails fast
Promise.all([p1, p2, p3])  // If p1 fails, p2/p3 results are lost
Promise.allSettled([p1, p2, p3])  // Always returns all results
```

### 3. Type Coercion Traps

```typescript
// SHARP: == vs ===
null == undefined   // true
0 == ''            // true
false == '0'       // true
// Always use ===

// SHARP: typeof null
typeof null  // 'object' -- historical bug, never fixed

// SHARP: NaN
NaN === NaN  // false
Number.isNaN(x)  // Use this instead of x === NaN
```

### 4. Concurrency Sharp Edges

```typescript
// SHARP: async forEach doesn't await
[1, 2, 3].forEach(async (item) => {
  await processItem(item)  // Fires all at once, doesn't wait
})
// Use for...of instead
for (const item of [1, 2, 3]) {
  await processItem(item)
}

// SHARP: Race condition in check-then-act
const exists = await db.findOne({ email })
if (!exists) {
  await db.create({ email })  // Another request might create it between check and act
}
// Use upsert or unique constraint instead
```

### 5. Security Sharp Edges

```typescript
// SHARP: URL parsing inconsistencies
new URL('http://evil.com\\@good.com')  // Different browsers parse differently

// SHARP: RegExp without anchors
/admin/.test('not-admin-page')  // true! No ^ or $

// SHARP: Timing attacks on string comparison
if (userToken === storedToken) { }  // Vulnerable to timing attack
// Use crypto.timingSafeEqual instead

// SHARP: Path traversal via join
path.join('/uploads', userInput)  // '../../../etc/passwd' works!
path.resolve('/uploads', userInput)  // Still dangerous
// Validate that result starts with base directory
```

### 6. Database Sharp Edges

```typescript
// SHARP: MongoDB operator injection
db.users.find({ username: req.body.username })
// If req.body.username = { "$ne": "" }, returns all users!
// Sanitize: validate input is a string

// SHARP: SQL LIKE injection
db.query(`SELECT * FROM users WHERE name LIKE '%${input}%'`)
// Input: "%" returns all, "_" matches any char
// Use parameterized queries with ESCAPE clause

// SHARP: ORM lazy loading in loops (N+1)
const users = await User.findAll()
for (const user of users) {
  const posts = await user.getPosts()  // N+1 queries!
}
// Use eager loading: User.findAll({ include: Post })
```

### 7. Framework Sharp Edges

```typescript
// SHARP: React useEffect cleanup race
useEffect(() => {
  let cancelled = false
  fetchData().then(data => {
    if (!cancelled) setState(data)  // Without this, stale updates
  })
  return () => { cancelled = true }
}, [])

// SHARP: Express middleware order matters
app.use(cors())
app.use(helmet())
app.use(authMiddleware)
app.use(rateLimiter)
// If rateLimiter is AFTER auth, unauthenticated requests aren't limited

// SHARP: Next.js revalidate: 0 is NOT "no cache"
// revalidate: 0 means "revalidate on every request" (still caches)
// Use { cache: 'no-store' } for truly no cache
```

## Detection Checklist

```
For each API/function/config in review:
[ ] What happens with empty/null/undefined input?
[ ] What happens with extremely large input?
[ ] What happens with concurrent access?
[ ] What happens when the network is slow/down?
[ ] What are the default values? Are they safe?
[ ] Does it fail silently or loudly?
[ ] Is the error message helpful or misleading?
[ ] Will a future developer understand the constraints?
[ ] Is there a safer alternative API?
```

## Documentation Pattern

When you find a sharp edge, document it:

```
SHARP EDGE: [API/pattern name]
SURPRISE: [What happens that developers don't expect]
DANGER: [What can go wrong -- security, data loss, correctness]
FIX: [The safe alternative]
AFFECTED: [Which files/modules in this codebase use it]
```

## Integration with vibecosystem

- **code-reviewer agent**: Check for known sharp edges during review
- **security-reviewer agent**: Focus on security sharp edges
- **self-learner agent**: When a sharp edge causes a bug, learn and add to detection
- **tdd-guide agent**: Write tests that exercise sharp edge behavior

Inspired by [Trail of Bits](https://github.com/trailofbits/skills) sharp-edges plugin.
