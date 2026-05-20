---
name: svelte-ninja
description: This skill should be used when the user mentions "Svelte", "SvelteKit", "runes", "$state", "$derived", "$effect", "$props", discusses component patterns, reactive state, routing, load functions, form actions, or needs help with Svelte/SvelteKit code. Addresses Svelte 5 patterns using runes, SvelteKit conventions, and best practices.
version: 1.0.0
---

# Svelte/SvelteKit Patterns

Comprehensive guide to Svelte 5 and SvelteKit development patterns. Emphasizes runes-based reactivity ($state, $derived, $effect, $props), component composition, SvelteKit routing, data loading, form handling, and performance optimization.

---

## When This Skill Applies

Use this skill when:
- Building Svelte components
- Managing reactive state with runes
- Implementing SvelteKit routes and pages
- Creating load functions or form actions
- Handling component composition
- Optimizing Svelte/SvelteKit performance
- Questions about Svelte 5 patterns or SvelteKit conventions

---

## Svelte 5 Fundamentals

### Runes Overview

**Runes** are compiler instructions (marked with `$`) that enable explicit reactivity:
- `$state` - Reactive state
- `$derived` - Computed values
- `$effect` - Side effects
- `$props` - Component props
- `$bindable` - Two-way bindable props

**Key principle**: Reactivity is explicit, not implicit. Works in `.js`, `.ts`, and `.svelte` files.

---

## Reactive State with $state

### Basic State
```svelte
<script>
	let count = $state(0);
	
	function increment() {
		count++; // Just a number, no wrapper needed
	}
</script>

<button onclick={increment}>
	Clicks: {count}
</button>
```

**Key points**:
- `$state` creates reactive state
- State is the value itself (not `.value` or `getCount()`)
- Updates trigger UI re-renders

### Deep Reactivity
```svelte
<script>
	let todos = $state([
		{ id: 1, text: 'Learn Svelte 5', done: false }
	]);
	
	function toggle(id) {
		const todo = todos.find(t => t.id === id);
		todo.done = !todo.done; // Deep reactivity works
	}
	
	function addTodo(text) {
		todos.push({ id: Date.now(), text, done: false });
		// Array methods trigger reactivity
	}
</script>
```

**Deep reactivity**:
- Objects and arrays are automatically proxied
- Nested mutations trigger updates
- Array methods (`.push`, `.splice`, etc.) work reactively

### State in .svelte.js Files
```javascript
// counter.svelte.js
export function createCounter(initial = 0) {
	let count = $state(initial);
	
	return {
		get count() { return count; },
		increment: () => count++,
		reset: () => count = initial
	};
}
```
```svelte
<!-- App.svelte -->
<script>
	import { createCounter } from './counter.svelte.js';
	
	const counter = createCounter(5);
</script>

<button onclick={counter.increment}>
	Count: {counter.count}
</button>
```

**Benefits**:
- Share state logic across components
- Testable outside Svelte components
- No store boilerplate needed

---

## Derived State with $derived

### Basic Derivations
```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
	let isEven = $derived(count % 2 === 0);
</script>

<p>{count} doubled is {doubled}</p>
<p>Count is {isEven ? 'even' : 'odd'}</p>
```

**Key points**:
- Automatically recalculates when dependencies change
- Memoized (only recalculates when needed)
- Must be free of side-effects

### Complex Derivations with $derived.by
```svelte
<script>
	let numbers = $state([1, 2, 3, 4, 5]);
	
	let stats = $derived.by(() => {
		const total = numbers.reduce((a, b) => a + b, 0);
		const average = total / numbers.length;
		return { total, average };
	});
</script>

<p>Total: {stats.total}, Average: {stats.average}</p>
```

**Use $derived.by when**:
- Logic doesn't fit in short expression
- Need multiple statements
- Complex calculations required

### $derived vs $effect

**$derived** - Computing values (pure, returns value):
```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2); // ✓ Good
</script>
```

**$effect** - Side effects (impure, no return value):
```svelte
<script>
	let count = $state(0);
	
	$effect(() => {
		console.log('Count changed:', count); // ✓ Good
	});
</script>
```

---

## Side Effects with $effect

### Basic Effects
```svelte
<script>
	let count = $state(0);
	
	$effect(() => {
		// Runs on mount and whenever count changes
		document.title = `Count: ${count}`;
	});
</script>
```

**When $effect runs**:
- Initially when component mounts
- Whenever dependencies change
- After DOM updates (unlike Svelte 4's `$:`)

### Effect Cleanup
```svelte
<script>
	let intervalId = $state(null);
	let elapsed = $state(0);
	
	$effect(() => {
		const id = setInterval(() => {
			elapsed++;
		}, 1000);
		
		// Cleanup runs when effect re-runs or component unmounts
		return () => clearInterval(id);
	});
</script>
```

### $effect.pre (Before DOM Update)
```svelte
<script>
	let messages = $state([]);
	let div;
	
	$effect.pre(() => {
		const isAtBottom = 
			div.scrollHeight - div.scrollTop === div.clientHeight;
		
		if (isAtBottom) {
			// After DOM updates, scroll to bottom
			$effect(() => {
				div.scrollTop = div.scrollHeight;
			});
		}
	});
</script>
```

### Common $effect Patterns

**Local storage sync**:
```svelte
<script>
	let preferences = $state(JSON.parse(
		localStorage.getItem('prefs') || '{}'
	));
	
	$effect(() => {
		localStorage.setItem('prefs', JSON.stringify(preferences));
	});
</script>
```

**API calls**:
```svelte
<script>
	let userId = $state('123');
	let user = $state(null);
	
	$effect(() => {
		fetch(`/api/users/${userId}`)
			.then(r => r.json())
			.then(data => user = data);
	});
</script>
```

**Avoid $effect for**:
- Derived values (use `$derived`)
- DOM manipulation Svelte handles (bindings, directives)
- Setting document.title (use `<svelte:head>`)

---

## Component Props with $props

### Basic Props
```svelte
<!-- Button.svelte -->
<script>
	let { label, variant = 'primary' } = $props();
</script>

<button class="btn btn--{variant}">
	{label}
</button>
```

**Usage**:
```svelte
<Button label="Click me" variant="secondary" />
```

### Props with TypeScript
```svelte
<script lang="ts">
	interface Props {
		label: string;
		variant?: 'primary' | 'secondary' | 'danger';
		onclick?: () => void;
	}
	
	let { label, variant = 'primary', onclick }: Props = $props();
</script>

<button class="btn btn--{variant}" {onclick}>
	{label}
</button>
```

### Rest Props
```svelte
<script>
	let { label, ...rest } = $props();
</script>

<button {...rest}>
	{label}
</button>
```

### Bindable Props with $bindable
```svelte
<!-- Input.svelte -->
<script>
	let { value = $bindable('') } = $props();
</script>

<input bind:value />
```

**Usage**:
```svelte
<script>
	let text = $state('');
</script>

<Input bind:value={text} />
<p>You typed: {text}</p>
```

---

## Component Patterns

### Slot Patterns

**Basic slot**:
```svelte
<!-- Card.svelte -->
<div class="card">
	<slot />
</div>
```

**Named slots**:
```svelte
<!-- Modal.svelte -->
<div class="modal">
	<header>
		<slot name="header" />
	</header>
	<main>
		<slot />
	</main>
	<footer>
		<slot name="footer" />
	</footer>
</div>
```

**Usage**:
```svelte
<Modal>
	<svelte:fragment slot="header">
		<h2>Title</h2>
	</svelte:fragment>
	
	<p>Content here</p>
	
	<svelte:fragment slot="footer">
		<button>Close</button>
	</svelte:fragment>
</Modal>
```

**Slot props**:
```svelte
<!-- List.svelte -->
<script>
	let { items } = $props();
</script>

<ul>
	{#each items as item}
		<li>
			<slot {item} />
		</li>
	{/each}
</ul>
```

**Usage**:
```svelte
<List items={users}>
	{#snippet children({ item })}
		<strong>{item.name}</strong>
	{/snippet}
</List>
```

### Composition Patterns

**Compound components**:
```svelte
<!-- Tabs.svelte -->
<script>
	let { children } = $props();
	let activeTab = $state(0);
	
	export function setActive(index) {
		activeTab = index;
	}
</script>

<div class="tabs">
	{@render children({ activeTab, setActive })}
</div>
```

**Higher-order components**:
```javascript
// withAuth.js
export function withAuth(Component) {
	return (props) => {
		const { user } = useAuth();
		if (!user) return 'Please log in';
		return new Component({ ...props, user });
	};
}
```

---

## SvelteKit Routing

### File-based Routing
```
src/routes/
├── +page.svelte              # /
├── about/
│   └── +page.svelte          # /about
├── blog/
│   ├── +page.svelte          # /blog
│   └── [slug]/
│       └── +page.svelte      # /blog/:slug
└── (app)/
    ├── dashboard/
    │   └── +page.svelte      # /dashboard
    └── settings/
        └── +page.svelte      # /settings
```

**Route groups** `(app)`: Don't affect URL, useful for layouts

### Dynamic Routes
```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script>
	let { data } = $props();
</script>

<h1>{data.post.title}</h1>
<div>{@html data.post.content}</div>
```
```javascript
// src/routes/blog/[slug]/+page.js
export async function load({ params }) {
	const post = await fetchPost(params.slug);
	return { post };
}
```

### Optional Parameters
```
src/routes/archive/[[year]]/[[month]]/+page.svelte
```

Matches:
- `/archive`
- `/archive/2024`
- `/archive/2024/12`

---

## Data Loading

### +page.js Load Functions
```javascript
// src/routes/blog/[slug]/+page.js
export async function load({ params, fetch }) {
	const post = await fetch(`/api/posts/${params.slug}`).then(r => r.json());
	
	return {
		post
	};
}
```

**Load function context**:
- `params` - Route parameters
- `fetch` - Enhanced fetch (credentials, relative URLs)
- `url` - URL object
- `route` - Route info
- `parent` - Parent load data

### +page.server.js Server Load
```javascript
// src/routes/dashboard/+page.server.js
import { db } from '$lib/server/database';

export async function load({ locals }) {
	const user = locals.user;
	const stats = await db.query('SELECT * FROM stats WHERE user_id = $1', [user.id]);
	
	return {
		stats
	};
}
```

**Server-only**:
- Access to database
- Access to environment variables
- Runs on server, never exposed to client

### Streaming with Promises
```javascript
// +page.js
export async function load({ fetch }) {
	const quick = fetch('/api/quick').then(r => r.json());
	const slow = fetch('/api/slow').then(r => r.json());
	
	return {
		quick: await quick,  // Wait for this
		slow                  // Stream this
	};
}
```
```svelte
<!-- +page.svelte -->
<script>
	let { data } = $props();
</script>

<div>{data.quick.title}</div>

{#await data.slow}
	<p>Loading...</p>
{:then slow}
	<p>{slow.content}</p>
{/await}
```

---

## Form Actions

### Basic Form Actions
```javascript
// src/routes/login/+page.server.js
export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const email = data.get('email');
		const password = data.get('password');
		
		const user = await authenticate(email, password);
		
		if (!user) {
			return { success: false, error: 'Invalid credentials' };
		}
		
		cookies.set('session', user.sessionId, { path: '/' });
		return { success: true };
	}
};
```
```svelte
<!-- src/routes/login/+page.svelte -->
<script>
	import { enhance } from '$app/forms';
	let { form } = $props();
</script>

<form method="POST" use:enhance>
	<input name="email" type="email" required />
	<input name="password" type="password" required />
	<button>Log in</button>
	
	{#if form?.error}
		<p class="error">{form.error}</p>
	{/if}
</form>
```

### Named Actions
```javascript
// +page.server.js
export const actions = {
	create: async ({ request }) => {
		// Handle create
	},
	update: async ({ request }) => {
		// Handle update
	},
	delete: async ({ request }) => {
		// Handle delete
	}
};
```
```svelte
<form method="POST" action="?/create">
	<!-- create form -->
</form>

<form method="POST" action="?/update">
	<!-- update form -->
</form>
```

### Progressive Enhancement
```svelte
<script>
	import { enhance } from '$app/forms';
</script>

<form 
	method="POST" 
	use:enhance={({ formData, cancel }) => {
		// Run before submission
		if (!confirm('Are you sure?')) {
			cancel();
		}
		
		return async ({ result, update }) => {
			// Run after response
			if (result.type === 'success') {
				await update();
				alert('Success!');
			}
		};
	}}
>
	<!-- form fields -->
</form>
```

---

## Performance Optimization

### Lazy Loading Components
```svelte
<script>
	import { onMount } from 'svelte';
	
	let HeavyComponent;
	
	onMount(async () => {
		const module = await import('./HeavyComponent.svelte');
		HeavyComponent = module.default;
	});
</script>

{#if HeavyComponent}
	<svelte:component this={HeavyComponent} />
{/if}
```

### Virtualizing Long Lists
```svelte
<script>
	let items = $state(Array.from({ length: 10000 }, (_, i) => i));
	let scrollTop = $state(0);
	
	const itemHeight = 50;
	const visibleCount = 20;
	
	let visibleItems = $derived(() => {
		const start = Math.floor(scrollTop / itemHeight);
		return items.slice(start, start + visibleCount);
	});
</script>

<div class="viewport" bind:scrollTop>
	<div style="height: {items.length * itemHeight}px">
		<div style="transform: translateY({Math.floor(scrollTop / itemHeight) * itemHeight}px)">
			{#each visibleItems as item}
				<div class="item">{item}</div>
			{/each}
		</div>
	</div>
</div>
```

### Memoizing Expensive Calculations
```svelte
<script>
	let data = $state([/* large dataset */]);
	
	// Automatically memoized
	let processed = $derived.by(() => {
		return data
			.filter(/* expensive filter */)
			.map(/* expensive transform */)
			.sort(/* expensive sort */);
	});
</script>
```

### Avoiding Unnecessary Re-renders
```svelte
<script>
	let todos = $state([
		{ id: 1, text: 'Task 1', done: false }
	]);
	
	// Each todo is keyed, only changed todos re-render
</script>

{#each todos as todo (todo.id)}
	<TodoItem {todo} />
{/each}
```

---

## Common Patterns

### Form Validation
```svelte
<script>
	let email = $state('');
	let password = $state('');
	
	let errors = $derived.by(() => {
		const errs = {};
		if (!email.includes('@')) errs.email = 'Invalid email';
		if (password.length < 8) errs.password = 'Too short';
		return errs;
	});
	
	let isValid = $derived(Object.keys(errors).length === 0);
</script>

<form>
	<input bind:value={email} />
	{#if errors.email}<span class="error">{errors.email}</span>{/if}
	
	<input type="password" bind:value={password} />
	{#if errors.password}<span class="error">{errors.password}</span>{/if}
	
	<button disabled={!isValid}>Submit</button>
</form>
```

### Modal Management
```svelte
<script>
	let isOpen = $state(false);
	
	$effect(() => {
		if (isOpen) {
			document.body.style.overflow = 'hidden';
		}
		
		return () => {
			document.body.style.overflow = '';
		};
	});
</script>

<button onclick={() => isOpen = true}>Open Modal</button>

{#if isOpen}
	<div class="modal-backdrop" onclick={() => isOpen = false}>
		<div class="modal" onclick={(e) => e.stopPropagation()}>
			<slot />
			<button onclick={() => isOpen = false}>Close</button>
		</div>
	</div>
{/if}
```

### Debounced Input
```svelte
<script>
	let searchQuery = $state('');
	let debouncedQuery = $state('');
	
	$effect(() => {
		const timeout = setTimeout(() => {
			debouncedQuery = searchQuery;
		}, 300);
		
		return () => clearTimeout(timeout);
	});
	
	// Use debouncedQuery for API calls
	$effect(() => {
		if (debouncedQuery) {
			fetch(`/api/search?q=${debouncedQuery}`);
		}
	});
</script>

<input bind:value={searchQuery} placeholder="Search..." />
```

---

## Anti-Patterns

### Don't: Use $effect for Derived Values
```svelte
<!-- ✗ Bad -->
<script>
	let count = $state(0);
	let doubled = $state(0);
	
	$effect(() => {
		doubled = count * 2; // Wrong! Use $derived
	});
</script>

<!-- ✓ Good -->
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
</script>
```

### Don't: Mutate Props Directly
```svelte
<!-- ✗ Bad -->
<script>
	let { user } = $props();
	
	function updateName() {
		user.name = 'New Name'; // Wrong! Props are read-only
	}
</script>

<!-- ✓ Good -->
<script>
	let { user, onUpdate } = $props();
	
	function updateName() {
		onUpdate({ ...user, name: 'New Name' });
	}
</script>
```

### Don't: Create Unnecessary $state
```svelte
<!-- ✗ Bad -->
<script>
	let count = $state(0);
	let doubled = $state(0);
	let isEven = $state(false);
	
	function increment() {
		count++;
		doubled = count * 2;     // Derived!
		isEven = count % 2 === 0; // Derived!
	}
</script>

<!-- ✓ Good -->
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
	let isEven = $derived(count % 2 === 0);
</script>
```

---

## Success Criteria

Svelte/SvelteKit code is well-structured when:
- Runes used appropriately ($state for state, $derived for computed, $effect for side effects)
- Components are composable and reusable
- Load functions fetch data efficiently
- Forms use progressive enhancement
- Performance optimized (lazy loading, memoization)
- TypeScript types are accurate
- Code is maintainable and follows Svelte 5 conventions