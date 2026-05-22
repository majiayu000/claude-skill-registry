---
name: code-review
description: Senior React/TypeScript/PWA code reviewer specializing in component architecture, hook discipline, frontend security, async state, lifecycle cleanup, browser resource management, client-side data access, temporal handling, props API contracts, and monitoring. Detects subtle bugs like stale closures, unbounded Dexie queries, and silent promise failures. Brutally picky.
---

# /code-review - Rigorous React/TypeScript Code Reviewer

Launches the **code-reviewer agent** to perform a comprehensive React/TypeScript/PWA code review of your changes.

## Usage

```bash
# Review current branch changes
/code-review

# Review specific files
/code-review src/components/CartSummary.tsx

# Review with specific instructions
/code-review focus on memoization issues in the dashboard widgets
```

## Search Tools

Use the right tool for the job:

| Need                                      | Tool                | Example                                             |
| ----------------------------------------- | ------------------- | --------------------------------------------------- |
| Find where a prop or hook is used         | `Grep`              | `Grep("useCheckoutTotal", "src/features")`          |
| Discover structural patterns (hooks, JSX) | `ast-grep`          | `ast-grep --pattern "useEffect($$)" src/dashboard`  |
| Jump to symbol definitions or references  | `LSP`               | `lsp_symbols src/components/Chart.tsx`              |
| Find files by glob pattern                | `Glob`              | `Glob("**/*.tsx")`                                  |
| Trace bundle boundaries / imports         | `Grep` + `ast-grep` | `ast-grep --pattern "import $$ from '$MODULE'" src` |

**For code review, prefer `ast-grep` + LSP when:**

- Verifying hook usage order and dependency arrays
- Finding all consumers of a context/provider pair
- Discovering related prop interfaces to check for backwards compatibility

## What Gets Reviewed

The code reviewer is extremely strict and checks for:

### Component Architecture

- Business logic/data shaping embedded inside presentation components (should live in hooks or shared libs)
- Side effects triggered during render instead of inside `useEffect`
- Prop drilling across more than two layers without context or composition
- "God components" that mix orchestration, view logic, and data fetching

**Red flags:**

```tsx
// BAD: Business logic and network calls in render
export const CheckoutSummary = ({ cart }: { cart: LineItem[] }) => {
  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
  if (total > 1000) {
    analytics.track('whale'); // fires on every render
  }
  fetch('/api/checkout/fees'); // runs during render
  return <span>{formatCurrency(total)}</span>;
};

// BAD: Prop drilling through every layout layer
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <Nav user={user} />
    </Sidebar>
  </Layout>
</App>;

// GOOD: Extract domain logic into a hook
function useCheckoutTotal(cart: LineItem[]): number {
  return useMemo(
    () => cart.reduce((sum, item) => sum + item.price * item.qty, 0),
    [cart]
  );
}

export const CheckoutSummary = () => {
  const cart = useCartContext();
  const total = useCheckoutTotal(cart);
  useEffect(() => {
    if (total > 1000) analytics.track('whale');
  }, [total]);
  return <Amount value={total} />;
};

// GOOD: Replace prop drilling with context/provider
const UserProvider = ({ user, children }: PropsWithChildren<{ user: User }>) => (
  <UserContext.Provider value={user}>{children}</UserContext.Provider>
);
```

### Code Quality (TypeScript-Focused)

- `any` type usage leaking into exported APIs
- Missing explicit return types on exported hooks/functions/components
- Magic strings/numbers that should be enums or constants
- Barrel exports that re-export everything and introduce circular dependencies

**Red flags:**

```typescript
// BAD: any everywhere
export function buildPayload(data: any) {
  return data['value'] || 'default';
}

// BAD: Missing return type on exported hook
export const usePrice = (sku) => {
  const [price, setPrice] = useState(0);
  /* ... */
  return price;
};

// BAD: Magic values sprinkled inline
if (plan === 'enterprise') {
  setTimeout(startTrial, 45000);
}

// BAD: Barrel export cycle
// src/features/index.ts
export * from './FeatureProvider';
export * from './useFeature';
// src/features/useFeature.ts
import { FeatureProvider } from '.'; // circular import

// GOOD: Narrow types and explicit returns
export interface CheckoutPayload {
  sku: string;
  quantity: number;
}
export function buildPayload(data: CheckoutPayload): string {
  return JSON.stringify(data);
}

export const usePrice = (sku: string): number => {
  const [price, setPrice] = useState<number>(0);
  /* ... */
  return price;
};

// GOOD: Shared enums/constants and explicit exports
export enum PlanTier {
  Starter = 'starter',
  Enterprise = 'enterprise',
}
export const REQUEST_TIMEOUT_MS = 30_000;
export { FeatureProvider } from './FeatureProvider';
export { useFeature } from './useFeature';
```

### Test Quality (React Focus)

- Duplicate React Testing Library/Jest tests that should be parameterized with `it.each`
- Tests asserting implementation details (class names, state) instead of accessible behavior
- Missing cleanup for fake timers, mocks, or global spies between tests
- Async interactions not awaited (`userEvent.click` without `await`)
- Snapshot-only coverage for complex conditional UI

**Red flags:**

```tsx
// BAD: Copy/paste tests
it('renders primary button', () => {
  render(<Button variant="primary" />);
  expect(screen.getByText('Save')).toHaveClass('btn--primary');
});
it('renders secondary button', () => {
  render(<Button variant="secondary" />);
  expect(screen.getByText('Cancel')).toHaveClass('btn--secondary');
});

// BAD: Implementation detail assertion
const wrapper = shallow(<Toggle />);
expect(wrapper.find('.toggle__thumb').prop('data-state')).toBe('on');

// BAD: Missing await for async user interaction
userEvent.click(screen.getByRole('button', { name: /submit/i }));
expect(mockSubmit).toHaveBeenCalled(); // may run before promise resolves

// GOOD: Parameterized, user-facing assertions
it.each`
  variant        | label
  ${'primary'}   | ${'Save'}
  ${'secondary'} | ${'Cancel'}
`('renders $variant button', ({ variant, label }) => {
  render(<Button variant={variant}>{label}</Button>);
  expect(screen.getByRole('button', { name: label })).toBeEnabled();
});

// GOOD: Focus on behavior, await async APIs
await userEvent.click(screen.getByRole('button', { name: /submit/i }));
await waitFor(() => expect(mockSubmit).toHaveBeenCalled());

// GOOD: Cleanup timers/mocks
afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
});
```

### Frontend Security

**Input validation & XSS:**

- `dangerouslySetInnerHTML` fed by unsanitized user content
- Directly rendering user data without encoding or escaping

**Secrets & sensitive data:**

- API keys, tokens, or customer secrets committed to client bundles
- Storing sensitive data in `localStorage`/`sessionStorage` instead of `httpOnly` cookies

**Prototype pollution & unsafe merges:**

- `Object.assign({}, userInput)` or `{ ...userInput }` without filtering keys
- Merging untrusted data into global config objects

**Red flags:**

```tsx
// BAD: Unsanitized HTML injection
const Comment = ({ html }: { html: string }) => (
  <div dangerouslySetInnerHTML={{ __html: html }} />
);

// BAD: Shipping secrets
export const config = {
  mapsApiKey: 'pk_live_abc123',
};

// BAD: Storing sensitive tokens client-side
localStorage.setItem('refreshToken', token);

// BAD: Prototype pollution
const payload = { ...userInput };
Object.assign(globalTheme, payload);

// GOOD: Sanitize or render as text
const sanitized = DOMPurify.sanitize(html);
return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;

// GOOD: Secrets fetched from server-only env vars
const { data } = await fetch('/api/config');

// GOOD: Keep sensitive data in httpOnly cookies; store opaque ids only
document.cookie = `session=${sessionId}; Secure; SameSite=Lax`;

// GOOD: Validate and whitelist keys before merging
const safe = pick(userInput, ['theme', 'density']);
const merged = { ...defaultTheme, ...safe };
```

### React Performance

- Components doing heavy work without `React.memo`
- Inline object/function creation inside JSX causing prop identity churn
- Missing `useMemo`/`useCallback` around stable dependencies
- Rendering thousands of nodes without virtualization/windowing
- Bundle bloat from importing whole libraries instead of subpaths; unused code not tree-shaken
- Memory leaks: `useEffect` without cleanup, stray timers, lingering event listeners

**Red flags:**

```tsx
// BAD: Inline functions + no memoization
export const ExpensiveList = ({ items }: { items: Item[] }) => (
  <div>
    {items.map((item) => (
      <Row key={item.id} item={item} onSelect={() => select(item.id)} />
    ))}
  </div>
);

// BAD: Giant list rendered all at once
{
  users.map((user) => <UserRow key={user.id} user={user} />);
}

// BAD: Unbounded imports
import _ from 'lodash';
const formatted = _.startCase(name);

// BAD: Missing cleanup
useEffect(() => {
  window.addEventListener('resize', onResize);
}, []); // never removed

// GOOD: Memo + stable callbacks
const Row = React.memo(({ item, onSelect }: RowProps) => {
  /* ... */
});
const handleSelect = useCallback((id: string) => select(id), [select]);

export const ExpensiveList = ({ items }: Props) => (
  <div>
    {items.map((item) => (
      <Row key={item.id} item={item} onSelect={handleSelect} />
    ))}
  </div>
);

// GOOD: Virtualization & focused imports
import startCase from 'lodash/startCase';
const rows = useVirtualizer({ count: users.length, estimateSize: () => 48 });

// GOOD: Cleanup effects
useEffect(() => {
  window.addEventListener('resize', onResize);
  return () => window.removeEventListener('resize', onResize);
}, [onResize]);
```

### React/TypeScript Specific

- Violations of the Rules of Hooks (conditional hooks, hooks inside loops)
- Stale closures inside `useEffect`/`useCallback`
- Missing dependency arrays or intentionally empty arrays without refs
- Mixing controlled and uncontrolled component state
- Misusing React keys (array index for dynamic lists)
- Forgetting `forwardRef` when exposing DOM nodes
- Missing error boundaries around critical UI segments

**Red flags:**

```tsx
// BAD: Conditional hook
if (isAdmin) {
  const data = useDashboardData();
}

// BAD: Missing deps leading to stale closure
useEffect(() => {
  fetchData(filter);
}, []); // ignores filter updates

// BAD: Controlled/uncontrolled mix
<input defaultValue={value} value={value} onChange={setValue} />;

// BAD: Index as key
{
  items.map((item, index) => <Row key={index} item={item} />);
}

// GOOD: Hooks called unconditionally
const data = useDashboardData({ role: isAdmin ? 'admin' : 'user' });

// GOOD: Stable dependencies or refs
const stableFilter = useDeepCompareMemoize(filter);
useEffect(() => {
  fetchData(stableFilter);
}, [stableFilter]);

// GOOD: Controlled OR uncontrolled, not both
const [value, setValue] = useState('');
<input value={value} onChange={(e) => setValue(e.target.value)} />;

// GOOD: Deterministic keys & proper refs
{
  items.map((item) => <Row key={item.id} item={item} />);
}

const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} />
));

<ErrorBoundary fallback={<CrashScreen />}>
  <CriticalPanel />
</ErrorBoundary>;
```

### Return Value Semantics (Critical)

**Pattern: "Return Value Conflation"** - When a function/promise returns the same value for cases requiring different handling.

- **Boolean returns**: Does `false` mean "already handled" or "request failed"?
- **`undefined`/`null`**: Does missing data mean "not found" or "error fetching"?
- **Promise resolution vs rejection**: Are rejections only thrown for network errors while validation issues slip through as `null`?

**Red flags:**

```typescript
// BAD: Conflates duplicate purchase with missing customer
export async function activatePremium(
  orderId: string,
  customerId: string
): Promise<boolean> {
  const response = await fetch(`/api/customers/${customerId}/activate`, {
    method: 'POST',
    body: JSON.stringify({ orderId }),
  });
  if (!response.ok) {
    return false; // could be 404, 409, or 500
  }
  return true;
}

if (!(await activatePremium(orderId, user.id))) {
  // UI silently ignores: no refund, no error state
}

// GOOD: Distinguish each case explicitly
export type ActivationResult =
  | { status: 'success' }
  | { status: 'duplicate'; orderId: string }
  | { status: 'user-missing'; customerId: string }
  | { status: 'error'; message: string };

export async function activatePremium(
  orderId: string,
  customerId: string
): Promise<ActivationResult> {
  const response = await fetch(`/api/customers/${customerId}/activate`, {
    method: 'POST',
    body: JSON.stringify({ orderId }),
  });
  if (response.status === 409) return { status: 'duplicate', orderId };
  if (response.status === 404) return { status: 'user-missing', customerId };
  if (!response.ok) return { status: 'error', message: await response.text() };
  return { status: 'success' };
}
```

### Async State Management

- Race conditions in `useEffect` where async work resolves after unmount and still calls `setState`
- Missing `AbortController`/`signal` when canceling fetches
- Concurrent state updates that should use functional `setState`
- IndexedDB/Dexie live queries not canceled on dependency change

**Red flags:**

```tsx
// BAD: setState after unmount
useEffect(() => {
  let active = true;
  fetchUser().then(user => {
    if (active) setUser(user);
  });
}, []); // never flips active, setState after unmount

// BAD: No abort controller
useEffect(() => {
  fetch(`/api/search?q=${query}`).then(setResults);
}, [query]);

// BAD: Concurrent updates using stale value
onScroll={() => setOffset(offset + 1)};

// GOOD: Abort + cleanup
useEffect(() => {
  const controller = new AbortController();
  fetch(`/api/search?q=${query}`, { signal: controller.signal })
    .then(resp => resp.json())
    .then(setResults)
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });
  return () => controller.abort();
}, [query]);

// GOOD: Functional updates prevent stale closures
onScroll={() => setOffset(prev => prev + 1)};

// GOOD: Dexie liveQuery cleanup
useEffect(() => {
  const sub = liveQuery(() => db.todos.where({ status }).toArray()).subscribe(setTodos);
  return () => sub.unsubscribe();
}, [status]);
```

### React Lifecycle

- `useEffect` missing cleanup functions (subscriptions, observers)
- Event listeners registered but never removed
- `setInterval`/`setTimeout` without `clearInterval`/`clearTimeout`
- Dexie `liveQuery`, Firebase, or socket subscriptions not cleaned up when dependencies change

**Red flags:**

```tsx
// BAD: Window listener leaks
useEffect(() => {
  window.addEventListener('resize', onResize);
}, []);

// BAD: Interval never cleared
useEffect(() => {
  const id = setInterval(poll, 1000);
}, []);

// BAD: Firestore subscription persists
useEffect(() => {
  firebase.firestore().collection('rooms').onSnapshot(setRooms);
}, []);

// GOOD: Cleanup everything
useEffect(() => {
  window.addEventListener('resize', onResize);
  return () => window.removeEventListener('resize', onResize);
}, [onResize]);

useEffect(() => {
  const id = setInterval(poll, 1000);
  return () => clearInterval(id);
}, [poll]);

useEffect(() => {
  const unsubscribe = firebase.firestore().collection('rooms').onSnapshot(setRooms);
  return () => unsubscribe();
}, []);
```

### Browser Resources

- Fetch requests kicked off without `AbortController` or timeout management
- Web Workers spawned but never terminated
- `BroadcastChannel` not closed when component unmounts
- Service Worker registrations not checked for outdated versions or errors

**Red flags:**

```typescript
// BAD: Unbounded fetch
const promise = fetch('/api/report'); // never canceled if user navigates away

// BAD: Worker leak
const worker = new Worker(new URL('./heavy.ts', import.meta.url));
worker.postMessage(payload); // no termination

// BAD: BroadcastChannel leak
const channel = new BroadcastChannel('notifications');
channel.onmessage = handleMessage;

// GOOD: Abort fetch and clear references
const controller = new AbortController();
fetch('/api/report', { signal: controller.signal });
return () => controller.abort();

// GOOD: Terminate workers/broadcast channels
useEffect(() => {
  const worker = new Worker(new URL('./heavy.ts', import.meta.url));
  worker.postMessage(payload);
  return () => worker.terminate();
}, [payload]);

useEffect(() => {
  const channel = new BroadcastChannel('notifications');
  channel.onmessage = handleMessage;
  return () => channel.close();
}, []);

// GOOD: Guard service worker registration
navigator.serviceWorker.register('/sw.js').then((reg) => {
  reg.update();
});
```

### IndexedDB/Dexie.js Data Access

- Using `.toArray()` on large tables without bounding queries
- Missing indexes for frequently queried fields
- Schema migrations that fail to bump versions or handle upgrades
- No handling for `QuotaExceededError` or storage full scenarios

**Red flags:**

```typescript
// BAD: Unbounded query pulling entire table
const allLogs = await db.logs.toArray();

// BAD: Missing index and filtering client-side
const tasks = await db.tasks.toArray();
const open = tasks.filter((t) => t.status === 'open');

// BAD: Migration ignored
db.version(3).stores({ tasks: '++id' }); // new fields but no upgrade handling

// BAD: No quota handling
await db.files.add(blob); // QuotaExceededError crashes app

// GOOD: Bounded queries + indexes
db.version(4).stores({ tasks: '++id,status,assigneeId' });
const open = await db.tasks.where('status').equals('open').limit(100).toArray();

// GOOD: Upgrade hook
db.version(4)
  .stores({ tasks: '++id,status,assigneeId' })
  .upgrade((tx) =>
    tx
      .table('tasks')
      .toCollection()
      .modify((task) => (task.slug ??= slugify(task.title)))
  );

// GOOD: Graceful quota handling
try {
  await db.files.add(blob);
} catch (error) {
  if ((error as DOMException).name === 'QuotaExceededError') {
    await evictOldFiles();
    throw new Error('Storage full, try again after clearing space');
  }
  throw error;
}
```

### Temporal & Time Handling

- Mixing `Date.now()` with `new Date()` objects from different timezones
- Persisting local times without timezone/offset info
- Hardcoded timezone math (e.g., subtracting hours manually)
- Assuming 24 hours per day (DST issues)
- No abstraction for time during testing (difficult to freeze time)

**Red flags:**

```typescript
// BAD: Mixing local and UTC
const createdAt = new Date(); // local
const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000); // treated as UTC elsewhere

// BAD: Hardcoded timezone adjustments
const est = utcDate.getTime() - 4 * 60 * 60 * 1000;

// BAD: Direct Date.now in business logic
if (Date.now() > subscription.expiresAt) {
  cancel();
}

// GOOD: Always use ISO strings + DateTime libraries
const now = Temporal.Now.instant();
const expiresAt = now.add({ days: 1 });

// GOOD: Convert with Intl/Temporal APIs
const nyTime = now.toZonedDateTimeISO('America/New_York');

// GOOD: Inject clock during tests
const clock = useClock();
if (clock.now() > subscription.expiresAt) {
  cancel();
}
```

### Props API & Monitoring

- Breaking prop interface changes without migration path
- Missing prop validation / defaults (required vs optional) causing runtime `undefined`
- Not wrapping remote widgets in error boundaries
- `console.log`/`debugger` remnants shipped to production
- No integration with error reporting tools (Sentry, LogRocket, etc.) for UI crashes

**Red flags:**

```tsx
// BAD: Breaking prop rename without alias
export interface ButtonProps {
  onSubmit: () => void; // renamed from onClick without backwards compat
}

// BAD: Required prop treated as optional
const Avatar = ({ src }: { src?: string }) => <img src={src} />; // crashes when undefined

// BAD: No error boundary
<RemoteWidget />;

// BAD: Console noise in prod
console.log('Render metrics', data);

// GOOD: Provide shims/deprecations
export interface ButtonProps {
  onClick: () => void;
  /** @deprecated use onClick */
  onSubmit?: () => void;
}

// GOOD: Validate props via runtime guards or defaults
const Avatar: FC<{ src: string }> = ({ src, ...rest }) => (
  <img src={src ?? fallbackAvatar} {...rest} />
);

// GOOD: Wrap third-party components
<ErrorBoundary fallback={<WidgetCrashed />}>
  <RemoteWidget />
</ErrorBoundary>;

// GOOD: Structured monitoring
console.debug = noop;
reportErrorToSentry(error, context);
```

### Documentation Completeness (REQUEST CHANGES if gaps found)

Documentation gaps are **not advisory** — they are blocking. If any of the following are missing or outdated after a change, the verdict MUST be **REQUEST CHANGES**.

**What must be kept in sync:**

- **README.md**: New features, changed scripts, new environment variables, updated project structure, changed tech stack entries
- **ROADMAP.md**: Task completion status, sprint progress, checklist items
- **AGENTS.md**: Architecture rules, build commands, project structure if files/folders were added or removed
- **JSDoc/TSDoc**: All exported hooks, functions, and components must have doc comments explaining behavior and edge cases
- **Inline comments**: Non-obvious logic, workarounds, or browser-specific behavior

**When to flag:**

- A new component/hook was added but README project structure was not updated
- A new script was added to package.json but not documented in README
- A roadmap task was implemented but ROADMAP.md still shows it as pending
- An exported function has no TSDoc comment
- A PR adds a feature listed in the roadmap but doesn't check off the corresponding checklist item
- Architecture rules in AGENTS.md no longer match actual code (e.g., new folders, changed dependency direction)

**Red flags:**

```typescript
// BAD: Exported hook undocumented
export function usePaymentsGateway() {
  /* ... */
}

// GOOD: TSDoc explains behavior and edge cases
/**
 * usePaymentsGateway pulls the current PSP config, refreshes every 5 minutes,
 * and throws when credentials are missing. Consumers must catch errors.
 */
export function usePaymentsGateway(): PaymentsGatewayState {
  /* ... */
}
```

## Verdict Decision Guide

| Condition                                              | Verdict                     |
| ------------------------------------------------------ | --------------------------- |
| No issues found                                        | **APPROVE**                 |
| Minor style/naming suggestions only                    | **APPROVE** (with comments) |
| Documentation gaps (README, ROADMAP, AGENTS.md, TSDoc) | **REQUEST CHANGES**         |
| Bugs, missing error handling, test gaps                | **REQUEST CHANGES**         |
| Security vulnerabilities, data loss, crash risks       | **BLOCK MERGE**             |

> **Documentation gaps always block.** A feature without updated docs is an incomplete feature.

## Review Output

The review is saved based on context:

**When working on an issue:**

```
.md/issues/{issue-number}/code-review.md
.md/issues/{issue-number}/code-review-round-2.md  # subsequent rounds
```

**When not on an issue (standalone):**

```
.md/standalone/code-review-{branch-name}.md
.md/standalone/code-review-{date}.md  # if no branch context
```

Examples:

- Issue #123: `.md/issues/123/code-review.md`
- Branch `feat/pwa-offline`: `.md/standalone/code-review-feat-pwa-offline.md`
- No context: `.md/standalone/code-review-2026-01-29.md`

The file includes:

### Header Section

- **Context**: Branch name, related issue number (if applicable), or a brief description of the work being reviewed
- **Review Date**: Timestamp of the review

### Review Sections

- **Critical Issues**: Blockers that must be fixed (security, data loss, crashes)
- **Component Architecture**: Hook discipline, prop boundaries, component responsibilities
- **React Performance & Async State**: Memoization, virtualization, fetch cancellation
- **React Lifecycle & Resources**: Cleanup for effects, timers, workers, subscriptions
- **Return Value Semantics**: Ambiguous returns, silent failures, conflated error cases
- **Client Data Access**: IndexedDB/Dexie usage, schema, migrations
- **Props API & Monitoring**: Contract issues, logging/monitoring problems
- **Code Quality & Tests**: Type safety, code smells, test coverage gaps
- **Documentation Gaps**: Missing updates to README, ROADMAP, AGENTS.md, or TSDoc (triggers REQUEST CHANGES)
- **Verdict**: APPROVE / REQUEST CHANGES / BLOCK MERGE

### Footer Section (MANDATORY)

- **Model**: The exact model ID that performed this review (e.g., claude-sonnet-4-5, claude-opus-4-6)
- **Persona**: The agent persona that wrote it (e.g., Sisyphus-Junior, Oracle)

## Review Workflow

When conducting a code review, follow these steps:

1. **Gather Context Information**:
   - Run `git branch --show-current` to get the current branch name
   - Check if there's a related GitHub issue by:
     - Looking for issue numbers in commit messages (`git log --oneline`)
     - Checking branch name for patterns like `feat/123-description` or `issue-123`
     - Using `gh issue list` if gh CLI is available
   - If no issue is found, extract a brief description from recent commits or branch name
   - Get the current model name and persona from your environment/config

2. **Perform Code Review**:
   - Run `git diff master...HEAD` (or `main`) to see all changes
   - Read and analyze modified files (components, hooks, tests, Dexie stores, worker scripts)
   - Apply all review criteria listed above

3. **Write Review File**:
   - Determine output path based on context:
     - **Issue context** (from commits, branch name like `feat/123-*`, or `gh issue`):
       - First review: `.md/issues/{issue-number}/code-review.md`
       - Subsequent rounds: `.md/issues/{issue-number}/code-review-round-{N}.md`
     - **Branch only** (no issue): `.md/standalone/code-review-{branch-name}.md`
     - **No context**: `.md/standalone/code-review-{date}.md`
   - Create directories if they don't exist (`mkdir -p`)
   - Sanitize branch names for filename (replace `/` with `-`, remove special chars)
   - Follow the exact markdown format specified below
   - Include context information in the header
   - Include model name and persona in the footer

## Markdown Output Format

The review markdown file MUST follow this structure:

```markdown
# Code Review

**Context**: [Branch: feature/xyz] OR [Issue #123: Description] OR [Brief description of changes]  
**Date**: YYYY-MM-DD HH:MM

---

## Critical Issues

[Security vulnerabilities, data loss risks, crash scenarios]

## Component Architecture

[Hook discipline, prop boundaries, component responsibilities]

## React Performance & Async State

[Memoization, virtualization, fetch cancellation, concurrency issues]

## React Lifecycle & Resources

[Effect cleanup, timers, workers, subscriptions, browser resources]

## Return Value Semantics

[Ambiguous returns, silent failures, conflated error cases]

## Client Data Access

[IndexedDB/Dexie usage, schema, migrations, quota handling]

## Props API & Monitoring

[Contract issues, monitoring gaps, error boundaries, logging]

## Code Quality & Tests

[Type safety, code smells, Jest/RTL issues]

## Documentation Gaps

[Missing updates to README, Storybook, MDX, ADRs]

## Verdict

[APPROVE / REQUEST CHANGES / BLOCK MERGE]

---

**Model**: [e.g., claude-sonnet-4-5, claude-opus-4-6]
**Persona**: [e.g., Sisyphus-Junior, Oracle]
```

## Example

```bash
# After making changes for issue #123
/code-review

# The agent will:
# 1. git diff master...HEAD to see all changes
# 2. Detect issue context (from branch name feat/123-description or commits)
# 3. Read modified files (components, hooks, tests, Dexie stores, workers)
# 4. Analyze against React/TypeScript best practices (including memoization, hook rules, Dexie bounds)
# 5. Write review to .md/issues/123/code-review.md
```

## Notes

- The reviewer is intentionally strict - don't take it personally
- Reviews focus on the **changes**, not the entire codebase
- If you disagree with feedback, that's valid - use your judgment
- The review can be resumed with additional instructions if needed
