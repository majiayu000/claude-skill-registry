---
name: react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. Contains 45+ rules across 8 categories, prioritized by impact. Use when writing new React components, implementing data fetching, reviewing code for performance issues, or optimizing bundle size.
---

# React Best Practices

Comprehensive performance optimization guide for React and Next.js applications. Contains 45 rules across 8 categories, prioritized by impact from critical (eliminating waterfalls, reducing bundle size) to incremental (advanced patterns).

## When to Apply

Reference these guidelines when:

- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category                  | Impact      | Prefix       |
| -------- | ------------------------- | ----------- | ------------ |
| 1        | Eliminating Waterfalls    | CRITICAL    | `async-`     |
| 2        | Bundle Size Optimization  | CRITICAL    | `bundle-`    |
| 3        | Server-Side Performance   | HIGH        | `server-`    |
| 4        | Client-Side Data Fetching | MEDIUM-HIGH | `client-`    |
| 5        | Re-render Optimization    | MEDIUM      | `rerender-`  |
| 6        | Rendering Performance     | MEDIUM      | `rendering-` |
| 7        | JavaScript Performance    | LOW-MEDIUM  | `js-`        |
| 8        | Advanced Patterns         | LOW         | `advanced-`  |

---

## 1. Eliminating Waterfalls (CRITICAL)

### 1.1 Defer Await Until Needed

**Impact: HIGH**

Move `await` operations into branches where they're actually used.

```typescript
// ❌ Incorrect: blocks both branches
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId);
  if (skipProcessing) {
    return { skipped: true };
  }
  return processUserData(userData);
}

// ✅ Correct: only blocks when needed
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    return { skipped: true };
  }
  const userData = await fetchUserData(userId);
  return processUserData(userData);
}
```

### 1.2 Promise.all() for Independent Operations

**Impact: CRITICAL (2-10× improvement)**

Execute independent async operations concurrently.

```typescript
// ❌ Incorrect: sequential, 3 round trips
const user = await fetchUser();
const posts = await fetchPosts();
const comments = await fetchComments();

// ✅ Correct: parallel, 1 round trip
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments(),
]);
```

### 1.3 Dependency-Based Parallelization

**Impact: CRITICAL**

Use `better-all` for partial dependencies to maximize parallelism.

```typescript
import { all } from "better-all";

const { user, config, profile } = await all({
  async user() {
    return fetchUser();
  },
  async config() {
    return fetchConfig();
  },
  async profile() {
    return fetchProfile((await this.$.user).id);
  },
});
```

### 1.4 Prevent Waterfall Chains in API Routes

**Impact: CRITICAL**

Start independent operations immediately, await later.

```typescript
// ✅ Correct: auth and config start immediately
export async function GET(request: Request) {
  const sessionPromise = auth();
  const configPromise = fetchConfig();
  const session = await sessionPromise;
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id),
  ]);
  return Response.json({ data, config });
}
```

### 1.5 Strategic Suspense Boundaries

**Impact: HIGH**

Use Suspense to show wrapper UI faster while data loads.

```tsx
// ✅ Correct: wrapper shows immediately, data streams in
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
      <div>Footer</div>
    </div>
  );
}

async function DataDisplay() {
  const data = await fetchData();
  return <div>{data.content}</div>;
}
```

---

## 2. Bundle Size Optimization (CRITICAL)

### 2.1 Avoid Barrel File Imports

**Impact: CRITICAL (200-800ms import cost)**

Import directly from source files instead of barrel files.

```tsx
// ❌ Incorrect: imports entire library
import { Check, X, Menu } from "lucide-react";

// ✅ Correct: imports only what you need
import Check from "lucide-react/dist/esm/icons/check";
import X from "lucide-react/dist/esm/icons/x";
import Menu from "lucide-react/dist/esm/icons/menu";

// ✅ Alternative: Next.js 13.5+ config
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ["lucide-react", "@mui/material"],
  },
};
```

Affected libraries: `lucide-react`, `@mui/material`, `@tabler/icons-react`, `react-icons`, `lodash`, `date-fns`.

### 2.2 Dynamic Imports for Heavy Components

**Impact: CRITICAL**

Use `next/dynamic` to lazy-load large components.

```tsx
import dynamic from "next/dynamic";

const MonacoEditor = dynamic(
  () => import("./monaco-editor").then((m) => m.MonacoEditor),
  { ssr: false },
);
```

### 2.3 Defer Non-Critical Third-Party Libraries

**Impact: MEDIUM**

Load analytics/logging after hydration.

```tsx
import dynamic from "next/dynamic";

const Analytics = dynamic(
  () => import("@vercel/analytics/react").then((m) => m.Analytics),
  { ssr: false },
);
```

### 2.4 Conditional Module Loading

**Impact: HIGH**

Load large data only when feature is activated.

```tsx
useEffect(() => {
  if (enabled && !frames && typeof window !== "undefined") {
    import("./animation-frames.js").then((mod) => setFrames(mod.frames));
  }
}, [enabled, frames]);
```

### 2.5 Preload Based on User Intent

**Impact: MEDIUM**

Preload heavy bundles on hover/focus.

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== "undefined") {
      void import("./monaco-editor");
    }
  };

  return (
    <button onMouseEnter={preload} onFocus={preload} onClick={onClick}>
      Open Editor
    </button>
  );
}
```

---

## 3. Server-Side Performance (HIGH)

### 3.1 Per-Request Deduplication with React.cache()

**Impact: MEDIUM**

```typescript
import { cache } from "react";

export const getCurrentUser = cache(async () => {
  const session = await auth();
  if (!session?.user?.id) return null;
  return await db.user.findUnique({ where: { id: session.user.id } });
});
```

### 3.2 Cross-Request LRU Caching

**Impact: HIGH**

```typescript
import { LRUCache } from "lru-cache";

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000,
});

export async function getUser(id: string) {
  const cached = cache.get(id);
  if (cached) return cached;
  const user = await db.user.findUnique({ where: { id } });
  cache.set(id, user);
  return user;
}
```

### 3.3 Minimize Serialization at RSC Boundaries

**Impact: HIGH**

Only pass fields that the client actually uses.

```tsx
// ❌ Incorrect: serializes all 50 fields
async function Page() {
  const user = await fetchUser();
  return <Profile user={user} />;
}

// ✅ Correct: serializes only 1 field
async function Page() {
  const user = await fetchUser();
  return <Profile name={user.name} />;
}
```

### 3.4 Parallel Data Fetching with Component Composition

**Impact: CRITICAL**

```tsx
// ✅ Correct: both fetch simultaneously
async function Header() {
  const data = await fetchHeader();
  return <div>{data}</div>;
}

async function Sidebar() {
  const items = await fetchSidebarItems();
  return <nav>{items.map(renderItem)}</nav>;
}

export default function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  );
}
```

### 3.5 Use after() for Non-Blocking Operations

**Impact: MEDIUM**

```tsx
import { after } from "next/server";

export async function POST(request: Request) {
  await updateDatabase(request);

  after(async () => {
    logUserAction({ userAgent: request.headers.get("user-agent") });
  });

  return Response.json({ status: "success" });
}
```

---

## 4. Client-Side Data Fetching (MEDIUM-HIGH)

### 4.1 Use SWR for Automatic Deduplication

**Impact: MEDIUM-HIGH**

```tsx
import useSWR from "swr";

function UserList() {
  const { data: users } = useSWR("/api/users", fetcher);
}
```

### 4.2 Deduplicate Global Event Listeners

**Impact: LOW**

Use `useSWRSubscription()` to share listeners across instances.

### 4.3 Use Passive Event Listeners

**Impact: MEDIUM**

```typescript
document.addEventListener("touchstart", handleTouch, { passive: true });
document.addEventListener("wheel", handleWheel, { passive: true });
```

### 4.4 Version and Minimize localStorage Data

**Impact: MEDIUM**

```typescript
const VERSION = "v2";

function saveConfig(config: { theme: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config));
  } catch {}
}
```

---

## 5. Re-render Optimization (MEDIUM)

### 5.1 Defer State Reads to Usage Point

**Impact: MEDIUM**

Don't subscribe to dynamic state if you only read it in callbacks.

```tsx
// ❌ Incorrect: subscribes to all searchParams changes
const searchParams = useSearchParams();
const handleShare = () => shareChat(searchParams.get("ref"));

// ✅ Correct: reads on demand
const handleShare = () => {
  const params = new URLSearchParams(window.location.search);
  shareChat(params.get("ref"));
};
```

### 5.2 Use Functional setState Updates

**Impact: MEDIUM**

```tsx
// ❌ Incorrect: requires state as dependency
const addItems = useCallback(
  (newItems) => {
    setItems([...items, ...newItems]);
  },
  [items],
);

// ✅ Correct: stable callback, no dependencies
const addItems = useCallback((newItems) => {
  setItems((curr) => [...curr, ...newItems]);
}, []);
```

### 5.3 Use Lazy State Initialization

**Impact: MEDIUM**

```tsx
// ❌ Incorrect: runs on every render
const [settings, setSettings] = useState(
  JSON.parse(localStorage.getItem("settings")),
);

// ✅ Correct: runs only once
const [settings, setSettings] = useState(() => {
  const stored = localStorage.getItem("settings");
  return stored ? JSON.parse(stored) : {};
});
```

### 5.4 Use Transitions for Non-Urgent Updates

**Impact: MEDIUM**

```tsx
import { startTransition } from "react";

const handler = () => {
  startTransition(() => setScrollY(window.scrollY));
};
```

### 5.5 Subscribe to Derived State

**Impact: MEDIUM**

```tsx
// ❌ Incorrect: re-renders on every pixel
const width = useWindowWidth();
const isMobile = width < 768;

// ✅ Correct: re-renders only on boolean change
const isMobile = useMediaQuery("(max-width: 767px)");
```

### 5.6 Narrow Effect Dependencies

**Impact: LOW**

```tsx
// ❌ Incorrect: re-runs on any user field
useEffect(() => {
  console.log(user.id);
}, [user]);

// ✅ Correct: re-runs only when id changes
useEffect(() => {
  console.log(user.id);
}, [user.id]);
```

### 5.7 Extract to Memoized Components

**Impact: MEDIUM**

```tsx
const UserAvatar = memo(function UserAvatar({ user }) {
  const id = useMemo(() => computeAvatarId(user), [user]);
  return <Avatar id={id} />;
});
```

---

## 6. Rendering Performance (MEDIUM)

### 6.1 CSS content-visibility for Long Lists

**Impact: HIGH**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

### 6.2 Animate SVG Wrapper Instead of SVG

**Impact: LOW**

```tsx
// ✅ Correct: hardware accelerated
<div className="animate-spin">
  <svg>...</svg>
</div>
```

### 6.3 Hoist Static JSX Elements

**Impact: LOW**

```tsx
const loadingSkeleton = <div className="animate-pulse h-20" />;

function Container() {
  return <div>{loading && loadingSkeleton}</div>;
}
```

### 6.4 Prevent Hydration Mismatch Without Flickering

**Impact: MEDIUM**

Use inline script to update DOM before React hydrates.

### 6.5 Use Activity Component for Show/Hide

**Impact: MEDIUM**

```tsx
import { Activity } from "react";

function Dropdown({ isOpen }) {
  return (
    <Activity mode={isOpen ? "visible" : "hidden"}>
      <ExpensiveMenu />
    </Activity>
  );
}
```

### 6.6 Use Explicit Conditional Rendering

**Impact: LOW**

```tsx
// ❌ Incorrect: renders "0" when count is 0
{
  count && <span>{count}</span>;
}

// ✅ Correct: renders nothing when count is 0
{
  count > 0 ? <span>{count}</span> : null;
}
```

---

## 7. JavaScript Performance (LOW-MEDIUM)

### 7.1 Build Index Maps for Repeated Lookups

**Impact: LOW-MEDIUM**

```typescript
// ✅ O(1) per lookup
const userById = new Map(users.map((u) => [u.id, u]));
return orders.map((order) => ({
  ...order,
  user: userById.get(order.userId),
}));
```

### 7.2 Use Set/Map for O(1) Lookups

**Impact: LOW-MEDIUM**

```typescript
const allowedIds = new Set(["a", "b", "c"]);
items.filter((item) => allowedIds.has(item.id));
```

### 7.3 Cache Repeated Function Calls

**Impact: MEDIUM**

```typescript
const slugifyCache = new Map<string, string>();

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) return slugifyCache.get(text)!;
  const result = slugify(text);
  slugifyCache.set(text, result);
  return result;
}
```

### 7.4 Use toSorted() Instead of sort()

**Impact: MEDIUM-HIGH**

```typescript
// ❌ Incorrect: mutates original
const sorted = users.sort((a, b) => a.name.localeCompare(b.name));

// ✅ Correct: creates new array
const sorted = users.toSorted((a, b) => a.name.localeCompare(b.name));
```

### 7.5 Early Length Check for Array Comparisons

**Impact: MEDIUM-HIGH**

```typescript
function hasChanges(current: string[], original: string[]) {
  if (current.length !== original.length) return true;
  // Only compare when lengths match
}
```

### 7.6 Combine Multiple Array Iterations

**Impact: LOW-MEDIUM**

```typescript
// ❌ Incorrect: 3 iterations
const admins = users.filter((u) => u.isAdmin);
const testers = users.filter((u) => u.isTester);

// ✅ Correct: 1 iteration
const admins = [],
  testers = [];
for (const user of users) {
  if (user.isAdmin) admins.push(user);
  if (user.isTester) testers.push(user);
}
```

### 7.7 Hoist RegExp Creation

**Impact: LOW-MEDIUM**

```tsx
const regex = useMemo(
  () => new RegExp(`(${escapeRegex(query)})`, "gi"),
  [query],
);
```

### 7.8 Cache Storage API Calls

**Impact: LOW-MEDIUM**

```typescript
const storageCache = new Map<string, string | null>();

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key));
  }
  return storageCache.get(key);
}
```

---

## 8. Advanced Patterns (LOW)

### 8.1 Store Event Handlers in Refs

**Impact: LOW**

```tsx
import { useEffectEvent } from "react";

function useWindowEvent(event: string, handler: () => void) {
  const onEvent = useEffectEvent(handler);

  useEffect(() => {
    window.addEventListener(event, onEvent);
    return () => window.removeEventListener(event, onEvent);
  }, [event]);
}
```

### 8.2 useLatest for Stable Callback Refs

**Impact: LOW**

```typescript
function useLatest<T>(value: T) {
  const ref = useRef(value);
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref;
}
```

---

## References

- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org)
- [SWR](https://swr.vercel.app)
- [better-all](https://github.com/shuding/better-all)
- [node-lru-cache](https://github.com/isaacs/node-lru-cache)
- [How We Optimized Package Imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [How We Made the Vercel Dashboard Twice as Fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)


## Parent Hub
- [_frontend-mastery](../_frontend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
