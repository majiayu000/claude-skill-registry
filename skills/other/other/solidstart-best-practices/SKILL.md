---
name: solidstart-best-practices
description: Comprehensive SolidStart and SolidJS development guide with patterns for reactivity, data fetching, routing, state management, and SSR. Use when building SolidStart apps, optimizing performance, or implementing CMS-driven features.
version: 1.0.0
author: Antenne Deutschland Engineering
license: MIT
tags: [SolidStart, SolidJS, Reactivity, SSR, Signals, Stores, Routing, Performance]
dependencies: []
---

# SolidStart Best Practices

Comprehensive development guide for SolidStart and SolidJS applications with patterns organized by impact level. Designed to help developers build performant, maintainable applications with fine-grained reactivity.

## When to use this skill

**Use SolidStart Best Practices when:**
- Building new SolidStart applications or features
- Implementing data fetching with `query` and `createAsync`
- Managing state with signals and stores
- Creating reactive components with control flow
- Integrating with CMS backends (Payload CMS)
- Optimizing SSR and streaming performance
- Implementing forms, search, or real-time features

**Key areas covered:**
- **Data Fetching** (CRITICAL): Server functions, queries, caching, preloading
- **Reactivity & State** (CRITICAL): Signals, stores, derived state, effects
- **Component Patterns** (HIGH): Control flow, blocks, renderers
- **Routing** (HIGH): File-based routing, navigation, preloading
- **Performance** (MEDIUM-HIGH): SSR optimization, Suspense management
- **Hooks & Utilities** (MEDIUM): Reusable patterns with cleanup
- **Forms & Validation** (MEDIUM): Form state, validation, submission
- **Testing** (LOW-MEDIUM): Unit tests, store testing, E2E

## Quick reference

### Critical patterns

1. **Use `query` + `createAsync`** - Server-side data fetching with caching
2. **Route preloading** - Fetch data before component renders
3. **Control flow components** - `<Show>`, `<For>`, `<Switch>` for conditional rendering
4. **Store pattern** - Separate read-only state from mutation actions
5. **SSR guards** - `typeof window === "undefined"` for browser-only code

### Common patterns

**Data fetching with preload:**
```typescript
import { query, createAsync, type RouteDefinition } from '@solidjs/router';

const getArticle = query(async (slug: string) => {
  "use server";
  return await getArticleBySlugQuery(slug, TENANT_SLUG);
}, "article");

export const route = {
  preload: ({ params }) => getArticle(params.slug),
} satisfies RouteDefinition;

export default function ArticlePage() {
  const params = useParams();
  const article = createAsync(() => getArticle(params.slug));

  return (
    <Show when={article()} fallback={<Loading />}>
      <Article data={article()} />
    </Show>
  );
}
```

**Store with actions:**
```typescript
import { createStore } from 'solid-js/store';

const [state, setState] = createStore<PlayerState>({
  isPlaying: false,
  currentStream: null,
});

export const audioPlayerStore = state;  // Read-only export

export const audioPlayerActions = {
  setIsPlaying: (value: boolean) => setState('isPlaying', value),
  setCurrentStream: (stream: PlayerChannel | null) => setState('currentStream', stream),
};
```

**Derived state with memos:**
```typescript
import { createMemo } from 'solid-js';

const currentTitle = createMemo(() => {
  return audioPlayerStore.streamMetadata?.title || audioPlayerStore.currentStream?.displayName || '';
});
```

## Using the guidelines

The complete guidelines are organized by category below. Each pattern includes:
- Correct/incorrect code comparisons
- Specific use cases and impact
- Integration with CMS and SSR
- Real-world examples from the codebase

## Categories overview

### 1. Data Fetching (CRITICAL)

Server-side data fetching is the foundation of SolidStart applications.

**`query` + `createAsync` (Recommended):**
```typescript
const getPosts = query(async () => {
  "use server";
  const posts = await fetch("https://my-api.com/posts");
  return await posts.json();
}, "posts");

export const route = {
  preload: () => getPosts(),
} satisfies RouteDefinition;

export default function Page() {
  const posts = createAsync(() => getPosts());
  return (
    <ErrorBoundary fallback={<div>Something went wrong!</div>}>
      <For each={posts()}>{(post) => <PostCard post={post} />}</For>
    </ErrorBoundary>
  );
}
```

**Benefits**: Automatic caching, request deduplication, SSR optimized.

**Streaming SSR with `deferStream`:**
```typescript
const data = createAsync(
  async () => await fetchHeavyData(),
  { deferStream: true }
);
```

**Cache invalidation:**
```typescript
import { revalidate } from "@solidjs/router";

revalidate(getHeaderByTenantQuery.key);  // Invalidate all
revalidate(getHeaderByTenantQuery.keyFor(tenantSlug));  // Specific key
```

**CMS query depth guidelines:**

| Content Type | Depth | Reason |
|--------------|-------|--------|
| Headers/Navigation | 3 | tenant → navigation → navItems → references |
| Articles | 4 | content blocks with nested relationships |
| Channel Pages | 5 | deeply nested channel + shows + blocks |

### 2. Reactivity & State (CRITICAL)

SolidJS uses fine-grained reactivity with signals and stores.

**createSignal basics:**
```typescript
import { createSignal } from 'solid-js';

const [count, setCount] = createSignal(0);

// Reading value (call the accessor)
const currentCount = count();

// Updating with value
setCount(5);

// Updating with function
setCount((prev) => prev + 1);
```

**createEffect for side effects:**
```typescript
import { createSignal, createEffect } from 'solid-js';

const [count, setCount] = createSignal(0);

createEffect(() => {
  console.log("Count changed:", count());
});
```

**createMemo for derived values:**
```typescript
import { createMemo, createSignal } from 'solid-js';

const [count, setCount] = createSignal(0);
const isEven = createMemo(() => count() % 2 === 0);

console.log(isEven()); // true
setCount(3);
console.log(isEven()); // false
```

**Store pattern for complex state:**
```typescript
import { createStore } from 'solid-js/store';

const [state, setState] = createStore<PlayerState>({
  isPlaying: false,
  currentStream: null,
});

// Export read-only store
export const audioPlayerStore = state;

// Export actions (mutations)
export const audioPlayerActions = {
  setIsPlaying: (value: boolean) => setState('isPlaying', value),
  setCurrentStream: (stream: PlayerChannel | null) => setState('currentStream', stream),
};
```

### 3. Component Patterns (HIGH)

SolidJS uses control flow components instead of JSX conditionals.

**Conditional rendering with `<Show>`:**
```typescript
import { Show } from 'solid-js';

<Show when={data()} fallback={<Loading />}>
  <Content data={data()} />
</Show>
```

**List rendering with `<For>`:**
```typescript
import { For } from 'solid-js';

<For each={items()}>{(item) => <Item {...item} />}</For>
```

**Multiple conditions with `<Switch>`:**
```typescript
import { Switch, Match } from 'solid-js';

<Switch>
  <Match when={type === 'a'}><ComponentA /></Match>
  <Match when={type === 'b'}><ComponentB /></Match>
</Switch>
```

**Block pattern for CMS content:**
```typescript
// components/blocks/ArticleBlock/ArticleBlock.tsx
interface ArticleBlockProps {
  block: ArticleBlockType;
}

export function ArticleBlock({ block }: ArticleBlockProps) {
  return <section class={styles.container}>{/* ... */}</section>;
}

// Register in BlockRenderer.tsx
switch (block.blockType) {
  case 'articleBlock': return <ArticleBlock block={block} />;
}
```

**Renderer pattern:**
```typescript
// ContentRenderer - orchestrates content arrays
<ContentRenderer items={page.content} />

// BlockRenderer - renders individual blocks by type
<BlockRenderer block={blockData} />

// RichTextRenderer - converts Lexical JSON to HTML
<RichTextRenderer content={richTextContent} />
```

### 4. Routing (HIGH)

SolidStart uses file-based routing.

**File conventions:**

| Pattern | Example | URL |
|---------|---------|-----|
| `index.tsx` | `routes/index.tsx` | `/` |
| `[param].tsx` | `routes/sender/[stationId].tsx` | `/sender/rock-antenne` |
| `[...slug].tsx` | `routes/[...404].tsx` | Any unmatched |
| `(group)/` | `routes/(home)/index.tsx` | `/` (group doesn't affect URL) |

**Route definition with preload:**
```typescript
import { type RouteDefinition } from "@solidjs/router";

export const route = {
  preload: ({ params }) => {
    getArticleBySlugQuery(params.slug, TENANT_SLUG);
  },
} satisfies RouteDefinition;
```

**Navigation:**
```typescript
import { A, useNavigate } from '@solidjs/router';

// Declarative - use <A> not <a>
<A href="/sender/rock-antenne">Rock Antenne</A>
<A href="/" end>Home</A>  // 'end' for exact match

// Programmatic
const navigate = useNavigate();
navigate('/sender/rock-antenne');
```

### 5. Performance (MEDIUM-HIGH)

Optimize SSR and client-side performance.

**Avoiding Suspense triggers:**
```typescript
// createResource triggers parent Suspense boundary
const [data] = createResource(() => fetchData());

// Signals + createEffect for isolated loading state
const [searchResults, setSearchResults] = createSignal(null);
const [isLoading, setIsLoading] = createSignal(false);

createEffect(on(query, async (q) => {
  setIsLoading(true);
  const results = await searchCMSQuery(q);
  setSearchResults(results);
  setIsLoading(false);
}));
```

**SSR-safe dynamic imports:**
```typescript
async function getClientModule() {
  if (typeof window === "undefined") return null;
  return await import("browser-only-module");
}
```

**Search with debouncing & abort:**
```typescript
export function useSearch(options: { debounceMs?: number } = {}) {
  const [query, setQuery] = createSignal("");
  const [debouncedQuery, setDebouncedQuery] = createSignal("");
  let debounceTimer: ReturnType<typeof setTimeout>;
  let abortController: AbortController | null = null;

  onCleanup(() => {
    clearTimeout(debounceTimer);
    abortController?.abort();
  });

  createEffect(on(debouncedQuery, async (q) => {
    abortController?.abort();
    abortController = new AbortController();

    try {
      const response = await searchCMSQuery(q, 10, abortController.signal);
      if (!abortController.signal.aborted) {
        setSearchResults(response);
      }
    } catch (error) {
      if (error instanceof Error && error.name !== "AbortError") {
        setError("Search unavailable");
      }
    }
  }));
}
```

### 6. Hooks & Utilities (MEDIUM)

Reusable patterns with proper cleanup.

**Basic hook with cleanup:**
```typescript
import { onCleanup } from 'solid-js';

export function usePolling(callback: () => void, interval: number) {
  const id = setInterval(callback, interval);
  onCleanup(() => clearInterval(id));
}
```

**Click outside detection:**
```typescript
export function useClickOutside(props: {
  ref: () => HTMLElement | undefined;
  callback: (event: Event) => void;
  enabled?: Accessor<boolean>;
}) {
  createEffect(() => {
    if (props.enabled && !props.enabled()) return;

    const handleClick = (event: Event) => {
      const el = props.ref();
      if (el && !el.contains(event.target as Node)) {
        props.callback(event);
      }
    };

    document.addEventListener("click", handleClick);
    onCleanup(() => document.removeEventListener("click", handleClick));
  });
}
```

**Theme with localStorage persistence:**
```typescript
export function useTheme() {
  const [theme, setTheme] = createSignal<"light" | "dark">("light");

  onMount(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") {
      setTheme(saved);
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      setTheme("dark");
    }
  });

  createEffect(() => {
    localStorage.setItem("theme", theme());
    document.documentElement.setAttribute("data-theme", theme());
  });

  return { theme, setTheme, toggleTheme: () => setTheme(t => t === "light" ? "dark" : "light") };
}
```

**Media queries:**
```typescript
export function useMediaQuery(query: string) {
  const [matches, setMatches] = createSignal(false);

  createEffect(() => {
    if (typeof window === "undefined") return;
    const mq = window.matchMedia(query);
    setMatches(mq.matches);

    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mq.addEventListener("change", handler);
    onCleanup(() => mq.removeEventListener("change", handler));
  });

  return matches;
}

export const useIsMobile = () => useMediaQuery("(max-width: 767px)");
export const useIsDesktop = () => useMediaQuery("(min-width: 1024px)");
```

**Key rules:**
1. Use `onCleanup` for subscriptions, intervals, event listeners
2. Return accessor functions (not raw values) to preserve reactivity
3. Guard SSR with `typeof window === "undefined"` checks
4. Provide fallback values for loading/error states

### 7. Forms & Validation (MEDIUM)

Form patterns with reactive validation.

**Basic form pattern:**
```typescript
import { createSignal } from 'solid-js';

function ContactForm() {
  const [email, setEmail] = createSignal('');
  const [error, setError] = createSignal('');

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    if (!email().includes('@')) {
      setError('Invalid email');
      return;
    }
    // Submit logic
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        inputmode="email"
        value={email()}
        onInput={(e) => setEmail(e.currentTarget.value)}
      />
      <Show when={error()}><span class="error">{error()}</span></Show>
      <button type="submit">Submit</button>
    </form>
  );
}
```

**Multi-field form hook:**
```typescript
export function useFormState(fields: CMSFormField[]) {
  const [formData, setFormData] = createSignal<FormData>({});
  const [errors, setErrors] = createSignal<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = createSignal(false);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    fields.forEach(field => {
      if (field.required && !formData()[field.name]) {
        newErrors[field.name] = 'Required';
      }
      if (field.blockType === 'email' && !isValidEmail(formData()[field.name])) {
        newErrors[field.name] = 'Invalid email';
      }
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isFormValid = createMemo(() =>
    fields.filter(f => f.required).every(f => formData()[f.name])
  );

  return { formData, setFormData, errors, isSubmitting, validateForm, isFormValid };
}
```

### 8. Middleware & Configuration (MEDIUM)

SolidStart middleware and app configuration.

**Middleware configuration:**
```typescript
// src/middleware/index.ts
import { createMiddleware } from "@solidjs/start/middleware";

export default createMiddleware({
  onRequest: (event) => {
    console.log("Request received:", event.request.url);
    event.locals.startTime = Date.now();
  },
  onBeforeResponse: (event) => {
    const duration = Date.now() - event.locals.startTime;
    console.log(`Request took ${duration}ms`);
  },
});
```

**App config:**
```typescript
// app.config.ts
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  middleware: "src/middleware/index.ts",
});
```

**CSP with nonce:**
```typescript
import { createMiddleware } from "@solidjs/start/middleware";
import { randomBytes } from "crypto";

export default createMiddleware({
  onRequest: (event) => {
    const nonce = randomBytes(16).toString("base64");
    event.locals.nonce = nonce;

    const csp = `
      default-src 'self';
      script-src 'nonce-${nonce}' 'strict-dynamic' 'unsafe-eval';
      object-src 'none';
      base-uri 'none';
    `.replace(/\s+/g, " ");

    event.response.headers.set("Content-Security-Policy", csp);
  },
});
```

### 9. Testing (LOW-MEDIUM)

Unit tests with Vitest and reactive scope isolation.

**Unit tests with createRoot:**
```typescript
import { createRoot } from "solid-js";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

describe("useSearch", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    mockSearchCMSQuery.mockReset();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("should debounce search requests", async () => {
    await createRoot(async (dispose) => {
      const { setQuery } = useSearch({ debounceMs: 300 });

      setQuery("test");
      expect(mockSearchCMSQuery).not.toHaveBeenCalled();

      await vi.advanceTimersByTimeAsync(300);
      expect(mockSearchCMSQuery).toHaveBeenCalledWith("test", 10, expect.any(AbortSignal));

      dispose();
    });
  });
});
```

**Store testing:**
```typescript
function resetStore() {
  setAudioPlayerStore({
    isPlaying: false,
    currentStream: null,
    streamMetadata: null,
  });
}

describe("Audio Player Store", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    resetStore();
  });

  it("should update metadata", () => {
    audioPlayerActions.setStreamMetadata({ title: "Song" });
    expect(audioPlayerStore.streamMetadata?.title).toBe("Song");
  });
});
```

## Anti-patterns to avoid

### Using `<a>` instead of `<A>`
```typescript
// WRONG - full page reload
<a href="/about">About</a>

// CORRECT - client-side navigation
<A href="/about">About</A>
```

### Missing SSR guards
```typescript
// WRONG - breaks SSR
fetchOptions.credentials = 'include';

// CORRECT - only client-side
if (typeof window !== 'undefined') {
  fetchOptions.credentials = 'include';
}
```

### Meta tags without Show guard
```typescript
// WRONG - causes duplicate tags
<Title>{page()?.meta?.title || "Fallback"}</Title>

// CORRECT - wait for data
<Show when={page()}>
  <Title>{page().meta?.title}</Title>
</Show>
```

### Missing limit in CMS queries
```typescript
// WRONG - Payload defaults to limit=10
GET /api/channels?depth=2

// CORRECT - explicit limit
GET /api/channels?depth=2&limit=100
```

### Using createResource for search
```typescript
// WRONG - triggers parent Suspense boundary
const [results] = createResource(query, searchAPI);

// CORRECT - isolated loading state with signals
const [results, setResults] = createSignal(null);
createEffect(on(query, async (q) => {
  setResults(await searchAPI(q));
}));
```

### Memory leaks in hooks

| Issue | Solution |
|-------|----------|
| Race condition in global refs | Use promise-based accessor |
| Memory leak in callbacks | Return removal function |
| Timeout timer leak | Cleanup on all exit paths |
| localStorage errors | Wrap in try-catch |
| Pending requests on unmount | Use AbortController with onCleanup |

## Implementation approach

When building a SolidStart application:

1. **Use server functions**: Mark data fetching with `"use server"` for automatic SSR
2. **Preload routes**: Export `route` object with `preload` function
3. **Prefer signals over resources**: For UI that shouldn't trigger Suspense
4. **Clean up effects**: Always use `onCleanup` for subscriptions
5. **Guard browser APIs**: Check `typeof window` before using browser-only features

## Key metrics to track

- **Time to First Byte (TTFB)**: Server response time
- **First Contentful Paint (FCP)**: When content becomes visible
- **Largest Contentful Paint (LCP)**: When main content is visible
- **Cumulative Layout Shift (CLS)**: Visual stability
- **Hydration time**: Time to make page interactive

## Resources

- [SolidJS Documentation](https://docs.solidjs.com)
- [SolidStart Documentation](https://docs.solidjs.com/solid-start)
- [SolidJS Router](https://docs.solidjs.com/solid-router)
- [Solid Primitives](https://primitives.solidjs.community)

## Version history

**v1.0.0** (January 2026)
- Initial release
- Patterns from Antenne Deutschland codebase
- Integration with Payload CMS
- SSR and streaming best practices
