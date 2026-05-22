---
name: svelte-5-runes
description: Complete guide for Svelte 5 runes ($state, $derived, $effect, $props, $bindable). Use for any Svelte 5 project or when code contains $ prefixed runes. Essential for reactive state management, computed values, side effects, and component props. Covers migration from Svelte 4 reactive statements.
license: MIT
category: development-tools
---

# Svelte 5 Runes

> **Feature Status:** Stable in Svelte 5.0+ (October 2024)
> **Documentation Source:** https://svelte.dev/docs/svelte/what-are-runes

Complete guide to Svelte 5's reactivity system using runes.

## When to Use This Skill

Use this skill for any Svelte 5 project. Runes are the core reactivity primitives:
- Creating reactive state with `$state`
- Computing derived values with `$derived`
- Running side effects with `$effect`
- Defining component props with `$props`
- Creating bindable props with `$bindable`
- Debugging with `$inspect`

## What Are Runes?

Runes are **symbols prefixed with `$`** that control Svelte's compiler. They are:
- **Built-in language keywords** - No imports required
- **Not functions** - Cannot be assigned to variables or passed around
- **Position-dependent** - Only valid in specific contexts

**Available Runes:**
- `$state` - Declare reactive state
- `$derived` - Create computed values
- `$effect` - Manage side effects
- `$props` - Define component properties
- `$bindable` - Enable two-way binding on props
- `$inspect` - Debug tool for state inspection
- `$host` - Access custom element host (web components)
- `$props.id()` - Generate consistent component-scoped IDs

## Quick Start Patterns

### Reactive State ($state)

```svelte
<script>
	let count = $state(0);
	let user = $state({ name: 'Ada', age: 28 });
</script>

<button onclick={() => count++}>
	Clicks: {count}
</button>

<button onclick={() => user.age++}>
	Happy birthday {user.name}! Age: {user.age}
</button>
```

**Key features:**
- Deep reactivity by default (objects/arrays)
- Mutations trigger UI updates
- Use `$state.raw()` for non-reactive data
- Works in class fields

### Computed Values ($derived)

```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);

	// Complex derivations
	let status = $derived.by(() => {
		if (count < 5) return 'low';
		if (count < 10) return 'medium';
		return 'high';
	});
</script>

<p>{count} doubled is {doubled}</p>
<p>Status: {status}</p>
```

**When to use:**
- Transforming state values
- Computing aggregations
- Filtering/mapping arrays
- ANY value derived from other state

### Side Effects ($effect)

```svelte
<script>
	let count = $state(0);
	let canvas;

	$effect(() => {
		// Runs when count changes
		console.log('Count changed:', count);

		// Cleanup function (optional)
		return () => {
			console.log('Cleanup before re-run');
		};
	});

	$effect(() => {
		if (!canvas) return;
		const ctx = canvas.getContext('2d');
		ctx.clearRect(0, 0, 100, 100);
		ctx.fillRect(0, 0, count, count);
	});
</script>

<canvas bind:this={canvas} width="100" height="100"></canvas>
```

**Use for:**
- Canvas drawing
- Third-party library integration
- Analytics tracking
- Network requests (with caution)

**DON'T use for:**
- Synchronizing state (use `$derived`)
- Computing values (use `$derived`)

### Component Props ($props)

```svelte
<!-- Parent.svelte -->
<script>
	import Child from './Child.svelte';
</script>

<Child name="Ada" age={28} />
```

```svelte
<!-- Child.svelte -->
<script>
	// Destructure with defaults
	let { name, age = 18 } = $props();

	// Or get all props
	let props = $props();
</script>

<p>{name} is {age} years old</p>
```

**TypeScript:**
```svelte
<script lang="ts">
	interface Props {
		name: string;
		age?: number;
	}

	let { name, age = 18 }: Props = $props();
</script>
```

### Two-Way Binding ($bindable)

```svelte
<!-- TextInput.svelte -->
<script>
	let { value = $bindable(''), placeholder } = $props();
</script>

<input bind:value {placeholder} />
```

```svelte
<!-- App.svelte -->
<script>
	import TextInput from './TextInput.svelte';

	let message = $state('');
</script>

<TextInput bind:value={message} placeholder="Type here" />
<p>You typed: {message}</p>
```

## Common Workflows

### Form with Validation

```svelte
<script>
	let email = $state('');
	let password = $state('');

	let isValidEmail = $derived(email.includes('@') && email.includes('.'));
	let isValidPassword = $derived(password.length >= 8);
	let canSubmit = $derived(isValidEmail && isValidPassword);

	function handleSubmit() {
		if (!canSubmit) return;
		// Submit form
	}
</script>

<form onsubmit={handleSubmit}>
	<input bind:value={email} type="email" />
	{#if email && !isValidEmail}
		<p class="error">Invalid email</p>
	{/if}

	<input bind:value={password} type="password" />
	{#if password && !isValidPassword}
		<p class="error">Password must be 8+ characters</p>
	{/if}

	<button disabled={!canSubmit}>Submit</button>
</form>
```

### Data Fetching with Loading States

```svelte
<script>
	let userId = $state(1);
	let userData = $state(null);
	let loading = $state(false);
	let error = $state(null);

	$effect(() => {
		// Tracks userId - refetches when it changes
		loading = true;
		error = null;

		fetch(`/api/users/${userId}`)
			.then(r => r.json())
			.then(data => {
				userData = data;
				loading = false;
			})
			.catch(e => {
				error = e.message;
				loading = false;
			});
	});
</script>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p class="error">{error}</p>
{:else if userData}
	<div>
		<h2>{userData.name}</h2>
		<p>{userData.email}</p>
	</div>
{/if}

<button onclick={() => userId++}>Next User</button>
```

### Class-Based State

```svelte
<script>
	class Counter {
		count = $state(0);

		increment = () => {
			this.count++;
		}

		reset() {
			this.count = 0;
		}
	}

	let counter = new Counter();
</script>

<button onclick={counter.increment}>
	Count: {counter.count}
</button>
<button onclick={() => counter.reset()}>Reset</button>
```

## Best Practices

### 1. Use $derived, Not $effect for Computed Values

❌ **Don't do this:**
```svelte
<script>
	let count = $state(0);
	let doubled = $state(0);

	$effect(() => {
		doubled = count * 2;
	});
</script>
```

✅ **Do this:**
```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
</script>
```

### 2. Understand Deep Reactivity

```svelte
<script>
	let items = $state([1, 2, 3]);

	// All these trigger reactivity:
	items.push(4);          // ✅ Works
	items[0] = 10;          // ✅ Works
	items = items.filter(x => x > 1); // ✅ Works

	// Destructuring breaks reactivity:
	let [first] = items;
	items[0] = 99;          // first still has old value
</script>
```

### 3. Use $state.raw for Large Immutable Data

```svelte
<script>
	// Don't need deep reactivity - performance win
	let config = $state.raw({
		apiUrl: 'https://api.example.com',
		timeout: 5000,
		// ... hundreds of properties
	});

	// Only reassign, don't mutate
	config = { ...config, timeout: 10000 };
</script>
```

### 4. Effect Dependencies Are Automatic

```svelte
<script>
	let a = $state(1);
	let b = $state(2);
	let c = $state(3);

	$effect(() => {
		// Only depends on `a` and `b`
		console.log(a + b);

		// `c` is not a dependency - won't rerun when c changes
	});
</script>
```

### 5. Props Flow Down, Events Flow Up

```svelte
<!-- Child.svelte -->
<script>
	let { count, onIncrement } = $props();
</script>

<button onclick={onIncrement}>
	Count: {count}
</button>
```

```svelte
<!-- Parent.svelte -->
<script>
	import Child from './Child.svelte';

	let count = $state(0);
</script>

<Child {count} onIncrement={() => count++} />
```

### 6. Don't Mutate Props (Use $bindable)

❌ **Don't:**
```svelte
<script>
	let { count } = $props();
</script>

<button onclick={() => count++}>
	{count}
</button>
```

✅ **Do:**
```svelte
<script>
	let { count = $bindable() } = $props();
</script>

<button onclick={() => count++}>
	{count}
</button>
```

### 7. Use $inspect for Debugging

```svelte
<script>
	let count = $state(0);

	$inspect(count); // Logs when count changes with stack trace

	// Custom logging
	$inspect(count).with((type, value) => {
		if (type === 'update') {
			console.log('Count updated to:', value);
		}
	});
</script>
```

## Common Pitfalls

### Async State in Effects

**Issue:** Async code doesn't track dependencies.

```svelte
<script>
	let userId = $state(1);
	let user = $state(null);

	$effect(() => {
		// userId IS tracked (read before await)
		const id = userId;

		fetch(`/api/users/${id}`)
			.then(r => r.json())
			.then(data => {
				// This works, but any state read HERE
				// is NOT tracked as a dependency
				user = data;
			});
	});
</script>
```

### Effect Cleanup

**Always cleanup subscriptions:**
```svelte
<script>
	let count = $state(0);

	$effect(() => {
		const interval = setInterval(() => {
			count++;
		}, 1000);

		// Cleanup when effect re-runs or component unmounts
		return () => clearInterval(interval);
	});
</script>
```

### Infinite Loops

**Don't read and write same state in effect:**
```svelte
<script>
	let count = $state(0);

	// ❌ Infinite loop!
	$effect(() => {
		count = count + 1;
	});

	// ✅ Use derived instead
	let incremented = $derived(count + 1);
</script>
```

## Migration from Svelte 4

### Reactive Declarations

**Svelte 4:**
```svelte
<script>
	let count = 0;
	$: doubled = count * 2;
	$: console.log('Count changed:', count);
</script>
```

**Svelte 5:**
```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);

	$effect(() => {
		console.log('Count changed:', count);
	});
</script>
```

### Component Props

**Svelte 4:**
```svelte
<script>
	export let name;
	export let age = 18;
</script>
```

**Svelte 5:**
```svelte
<script>
	let { name, age = 18 } = $props();
</script>
```

### Two-Way Binding

**Svelte 4:**
```svelte
<script>
	export let value;
</script>

<input bind:value />
```

**Svelte 5:**
```svelte
<script>
	let { value = $bindable() } = $props();
</script>

<input bind:value />
```

## Detailed Documentation

For complete implementation details, read the reference files:

- **references/quick-reference.md** - All runes syntax at a glance
- **references/state.md** - Complete $state documentation (deep reactivity, classes, raw state)
- **references/derived.md** - $derived patterns and dependencies
- **references/effect.md** - $effect lifecycle, cleanup, and when NOT to use
- **references/props.md** - $props type safety and patterns
- **references/other-runes.md** - $bindable, $inspect, $host usage

## Important Notes

- Runes are **compile-time features** - no runtime imports
- Effects run **after DOM updates** (use `$effect.pre` for before)
- Dependencies are tracked **synchronously** - async code won't track
- `$state` creates **deep reactive proxies** for objects/arrays
- Can't export `$state` directly from `.svelte.js` if reassigned
- Props should not be mutated unless marked with `$bindable`
