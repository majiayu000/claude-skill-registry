---
name: typescript-code-review
description: TypeScript and React code review guidelines (type safety, React patterns, performance). Auto-loads when reviewing TypeScript/React code.
user-invocable: false
---

# TypeScript/React Code Review Patterns

This skill provides TypeScript and React-specific code review guidelines. Use alongside `typescript-style` for comprehensive review.

## Critical Security Issues

### XSS Vulnerabilities

```typescript
// VULNERABLE - dangerouslySetInnerHTML without sanitization
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// VULNERABLE - innerHTML assignment
element.innerHTML = userContent;

// SAFE - use DOMPurify
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />

// SAFER - avoid innerHTML entirely
<div>{userContent}</div>  // React auto-escapes
```

### Insecure Data Exposure

```typescript
// VULNERABLE - logging sensitive data
console.log("User data:", user);  // May include tokens, passwords
console.log("Request:", request.headers);  // Auth headers

// VULNERABLE - exposing in error messages
throw new Error(`Auth failed for ${credentials}`);

// SAFE - sanitize before logging
console.log("User ID:", user.id);  // Only necessary fields
```

### Unsafe eval/Function Constructor

```typescript
// VULNERABLE - code execution from strings
eval(userInput);
new Function(userInput)();
setTimeout(userInput, 1000);  // String argument

// SAFE - avoid string evaluation
setTimeout(() => { processInput(userInput); }, 1000);
```

### Missing CSRF Protection

```typescript
// VULNERABLE - no CSRF token
fetch('/api/delete', { method: 'POST', body: data });

// SAFE - include CSRF token
fetch('/api/delete', {
  method: 'POST',
  headers: { 'X-CSRF-Token': csrfToken },
  body: data,
});
```

## High Priority Type Safety Issues

### Unsafe Type Assertions

```typescript
// DANGEROUS - bypasses type checking
const user = data as User;
const items = response as any[];

// SAFER - use type guards
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'id' in data;
}

if (isUser(data)) {
  // data is now typed as User
}
```

### Non-null Assertion Abuse

```typescript
// DANGEROUS - runtime error if null
const name = user!.profile!.name!;

// SAFE - explicit null handling
const name = user?.profile?.name ?? 'Unknown';

// Or with explicit checks
if (user?.profile?.name) {
  const name = user.profile.name;
}
```

### Missing Error Handling in Async Code

```typescript
// BUG - unhandled promise rejection
async function fetchData() {
  const response = await fetch(url);
  return response.json();  // What if fetch fails?
}

// CORRECT - handle errors
async function fetchData() {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;  // Re-throw or return default
  }
}
```

### Ignoring Promise Results

```typescript
// BUG - fire and forget
saveUser(userData);  // No await, no error handling

// CORRECT
await saveUser(userData);
// or
saveUser(userData).catch(console.error);
```

## React Anti-Patterns

### Missing useEffect Dependencies

```typescript
// BUG - stale closure, missing dependency
useEffect(() => {
  fetchUser(userId);  // userId not in deps!
}, []);  // Empty deps = runs once with initial userId

// CORRECT - include all dependencies
useEffect(() => {
  fetchUser(userId);
}, [userId]);
```

### State Updates on Unmounted Components

```typescript
// BUG - memory leak, state update after unmount
useEffect(() => {
  fetchData().then(setData);
}, []);

// CORRECT - cleanup with flag or AbortController
useEffect(() => {
  let mounted = true;
  fetchData().then((data) => {
    if (mounted) setData(data);
  });
  return () => { mounted = false; };
}, []);

// BETTER - use AbortController
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal })
    .then(res => res.json())
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });
  return () => controller.abort();
}, [url]);
```

### Missing Key Prop in Lists

```typescript
// BUG - using index as key (causes issues on reorder)
items.map((item, index) => <Item key={index} data={item} />)

// CORRECT - use stable unique identifier
items.map((item) => <Item key={item.id} data={item} />)
```

### Inline Functions in JSX (Performance)

```typescript
// PERFORMANCE - new function on every render
<Button onClick={() => handleClick(id)} />

// BETTER - memoize if passed to memoized child
const handleButtonClick = useCallback(() => handleClick(id), [id]);
<MemoizedButton onClick={handleButtonClick} />
```

### Props Drilling Deep

```typescript
// CODE SMELL - passing props through many levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserProfile user={user} />

// BETTER - use Context for cross-cutting concerns
const UserContext = createContext<User | null>(null);
<UserContext.Provider value={user}>
  <App />
</UserContext.Provider>
```

## Performance Anti-Patterns

### Re-rendering Entire Lists

```typescript
// SLOW - all items re-render when one changes
function ItemList({ items }: { items: Item[] }) {
  return items.map(item => <ItemRow item={item} />);
}

// FAST - memoize individual items
const MemoizedItemRow = memo(ItemRow);
function ItemList({ items }: { items: Item[] }) {
  return items.map(item => <MemoizedItemRow key={item.id} item={item} />);
}
```

### Expensive Calculations Without Memoization

```typescript
// SLOW - recalculates on every render
function ExpensiveComponent({ data }: { data: number[] }) {
  const sorted = [...data].sort((a, b) => a - b);  // Every render!
  const sum = data.reduce((a, b) => a + b, 0);      // Every render!
  return <div>{sorted.join(',')}: {sum}</div>;
}

// FAST - memoize expensive operations
function ExpensiveComponent({ data }: { data: number[] }) {
  const sorted = useMemo(() => [...data].sort((a, b) => a - b), [data]);
  const sum = useMemo(() => data.reduce((a, b) => a + b, 0), [data]);
  return <div>{sorted.join(',')}: {sum}</div>;
}
```

### Unnecessary State

```typescript
// OVERHEAD - derived state should be computed
const [items, setItems] = useState<Item[]>([]);
const [itemCount, setItemCount] = useState(0);  // Unnecessary!

// Update both when items change - easy to forget
setItems(newItems);
setItemCount(newItems.length);  // Must keep in sync

// BETTER - derive from source of truth
const [items, setItems] = useState<Item[]>([]);
const itemCount = items.length;  // Always in sync
```

### Large Bundle Imports

```typescript
// HEAVY - imports entire library
import _ from 'lodash';
import moment from 'moment';  // 300KB+

// LIGHT - import specific functions
import debounce from 'lodash/debounce';
import { format } from 'date-fns';  // Much smaller
```

## Accessibility Issues

### Missing ARIA Labels

```typescript
// INACCESSIBLE - icon-only button without label
<button onClick={onClose}>
  <CloseIcon />
</button>

// ACCESSIBLE
<button onClick={onClose} aria-label="Close dialog">
  <CloseIcon />
</button>
```

### Non-Interactive Elements with Handlers

```typescript
// INACCESSIBLE - div with click handler
<div onClick={handleClick}>Click me</div>

// ACCESSIBLE - use button or add role/keyboard
<button onClick={handleClick}>Click me</button>
// or
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</div>
```

### Missing Form Labels

```typescript
// INACCESSIBLE - input without label
<input type="email" placeholder="Email" />

// ACCESSIBLE
<label>
  Email
  <input type="email" />
</label>
// or
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

### Color-Only Indicators

```typescript
// INACCESSIBLE - status only indicated by color
<span style={{ color: isError ? 'red' : 'green' }}>
  {status}
</span>

// ACCESSIBLE - include text or icon
<span style={{ color: isError ? 'red' : 'green' }}>
  {isError ? '❌ ' : '✓ '}{status}
</span>
```

## Common TypeScript Mistakes

### Improper Null Checking

```typescript
// BUG - falsy check catches 0 and ''
if (!value) return;  // Fails for value = 0 or ''

// CORRECT - explicit null/undefined check
if (value == null) return;  // Catches null and undefined
// or
if (value === null || value === undefined) return;
```

### Object Spread Overwrites

```typescript
// BUG - order matters, later overwrites earlier
const config = { ...defaultConfig, ...userConfig, timeout: 5000 };
// timeout is always 5000, even if userConfig.timeout was set!

// CORRECT - put defaults first
const config = { timeout: 5000, ...defaultConfig, ...userConfig };
```

### Array Method Return Values

```typescript
// BUG - forEach doesn't return
const doubled = items.forEach(x => x * 2);  // undefined!

// CORRECT - use map for transformation
const doubled = items.map(x => x * 2);

// BUG - filter callback should return boolean
const active = items.filter(item => item.status);  // Works but unclear

// CORRECT - explicit boolean return
const active = items.filter(item => item.status === 'active');
```

## Test Coverage Gaps

Flag missing tests for:

1. **Error states**: Network failures, invalid inputs, edge cases
2. **User interactions**: Button clicks, form submissions, keyboard navigation
3. **Async behavior**: Loading states, success/error handling
4. **Accessibility**: Screen reader compatibility, keyboard navigation
5. **Edge cases**: Empty arrays, null values, boundary conditions

```typescript
// Missing test coverage examples
it('should show error message on fetch failure', async () => {});
it('should be keyboard navigable', () => {});
it('should handle empty item list', () => {});
it('should show loading state while fetching', () => {});
```

## Code Review Checklist

### Security
- [ ] No XSS vectors (dangerouslySetInnerHTML, innerHTML)
- [ ] No sensitive data in logs or error messages
- [ ] No eval or dynamic code execution
- [ ] CSRF protection on mutations

### Type Safety
- [ ] No `any` types (use `unknown` + type guards)
- [ ] No unsafe type assertions without validation
- [ ] Proper null/undefined handling
- [ ] All promises handled (await or .catch)

### React Patterns
- [ ] useEffect dependencies complete
- [ ] Cleanup functions for subscriptions/timers
- [ ] Stable keys in lists (not array index)
- [ ] No unnecessary state (derive when possible)

### Performance
- [ ] Expensive operations memoized (useMemo)
- [ ] Event handlers memoized when needed (useCallback)
- [ ] Large components use React.memo
- [ ] Tree-shakeable imports

### Accessibility
- [ ] Interactive elements have labels
- [ ] Keyboard navigation works
- [ ] Form inputs have associated labels
- [ ] Status not conveyed by color alone
