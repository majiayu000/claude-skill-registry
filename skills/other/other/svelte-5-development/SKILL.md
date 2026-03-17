---
name: svelte5-development
description: Svelte 5 and SvelteKit development with shadcn-svelte components and Bits UI patterns. Use when building Svelte components, working with runes ($state, $derived, $effect), using shadcn-svelte UI (dialog, tooltip, sidebar, form, button, card), Bits UI patterns (child snippet, wrapper), or developing SvelteKit routes.
---

This skill provides guidance for Svelte 5 and SvelteKit development, covering runes, component patterns, routing, and common pitfalls.

## Svelte 5 Runes - Core Reactivity

### $state - Reactive State
Creates reactive state that updates the UI when changed.

```svelte
<script>
	let count = $state(0);
	let user = $state({ name: 'Alice', age: 30 });
</script>

<button onclick={() => count++}>Clicks: {count}</button>
<button onclick={() => user.age++}>Age: {user.age}</button>
```

**Deep Reactivity**: Objects and arrays become deeply reactive proxies. Mutations trigger updates:
```js
let todos = $state([{ done: false, text: 'learn svelte' }]);
todos[0].done = true; // triggers update
todos.push({ done: false, text: 'build app' }); // triggers update
```

**Classes**: Use $state in class fields:
```js
class Todo {
	done = $state(false);
	constructor(text) {
		this.text = $state(text);
	}
	reset = () => {
		this.text = '';
		this.done = false;
	}
}
```

**Important**: When you destructure reactive state, references are NOT reactive:
```js
let { done, text } = todos[0];
todos[0].done = true; // `done` variable won't update
```

**$state.raw**: Use for non-reactive objects (performance optimization):
```js
let data = $state.raw({ large: 'dataset' });
data.large = 'new value'; // no effect, must reassign entire object
data = { large: 'new value' }; // this works
```

### $derived - Computed Values
Creates values that automatically update when dependencies change.

```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
	let tripled = $derived(count * 3);
</script>

<p>{count} × 2 = {doubled}</p>
<p>{count} × 3 = {tripled}</p>
```

**For complex logic, use $derived.by**:
```js
let numbers = $state([1, 2, 3]);
let total = $derived.by(() => {
	let sum = 0;
	for (const n of numbers) sum += n;
	return sum;
});
```

**Critical Rule**: NEVER update state inside $derived - it should be side-effect free.

**Overriding deriveds** (Svelte 5.25+): Useful for optimistic UI:
```js
let likes = $derived(post.likes);

async function onclick() {
	likes += 1; // optimistic update
	try {
		await likePost();
	} catch {
		likes -= 1; // rollback on error
	}
}
```

### $effect - Side Effects
Runs when state changes. Use for DOM manipulation, third-party libraries, analytics.

```svelte
<script>
	let size = $state(50);
	let canvas;

	$effect(() => {
		const ctx = canvas.getContext('2d');
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		// reruns when `size` changes
		ctx.fillRect(0, 0, size, size);
	});
</script>

<canvas bind:this={canvas} width="100" height="100"></canvas>
```

**Lifecycle**: Effects run after component mounts and after state changes (in microtask).

**Teardown functions**: Return a function to clean up:
```js
$effect(() => {
	const interval = setInterval(() => count++, 1000);
	return () => clearInterval(interval); // cleanup
});
```

**Dependencies**: Automatically tracks any $state/$derived read synchronously. Async reads (after await) are NOT tracked:
```js
$effect(() => {
	context.fillStyle = color; // tracked
	setTimeout(() => {
		context.fillRect(0, 0, size, size); // size NOT tracked!
	}, 0);
});
```

**Conditional dependencies**: Only depends on values read in the last run:
```js
$effect(() => {
	if (condition) {
		confetti({ colors: [color] }); // only depends on color if condition is true
	}
});
```

**$effect.pre**: Runs BEFORE DOM updates (rare, for things like autoscroll).

**CRITICAL - When NOT to use $effect**:
- ❌ Don't synchronize state (use $derived instead)
- ❌ Don't use for computed values
- ✅ DO use for: canvas drawing, third-party libs, analytics, intervals, DOM manipulation

```svelte
<!-- ❌ BAD - Don't do this -->
<script>
	let count = $state(0);
	let doubled = $state();
	$effect(() => {
		doubled = count * 2; // WRONG! Use $derived
	});
</script>

<!-- ✅ GOOD - Do this -->
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
</script>
```

### $props - Component Props
Receives data from parent components.

```svelte
<!-- Parent.svelte -->
<Child message="hello" count={42} />

<!-- Child.svelte -->
<script>
	let { message, count = 0 } = $props(); // destructuring with defaults
</script>

<p>{message} - {count}</p>
```

**Renaming props** (for reserved words or invalid identifiers):
```js
let { super: trouper = 'default' } = $props();
```

**Rest props**:
```js
let { a, b, ...others } = $props();
```

**Type safety** (TypeScript):
```svelte
<script lang="ts">
	let { message }: { message: string } = $props();
	// or
	interface Props {
		message: string;
		count?: number;
	}
	let { message, count = 0 }: Props = $props();
</script>
```

**Important**: Props update reactively, but you should NOT mutate them (unless $bindable).

### $bindable - Two-Way Binding
Allows child components to update parent state.

```svelte
<!-- FancyInput.svelte -->
<script>
	let { value = $bindable(), ...props } = $props();
</script>

<input bind:value {...props} />

<!-- Parent.svelte -->
<script>
	import FancyInput from './FancyInput.svelte';
	let message = $state('hello');
</script>

<FancyInput bind:value={message} />
<p>{message}</p>
```

**Fallback values**:
```js
let { value = $bindable('default value') } = $props();
```

**Use sparingly**: Most components should use callback props instead of $bindable.

## Common Patterns and Pitfalls

### Effect vs Derived
```svelte
<script>
	let a = $state(1);
	let b = $state(2);

	// ✅ GOOD - Use $derived for computed values
	let sum = $derived(a + b);

	// ❌ BAD - Don't use $effect for this
	let sum2 = $state(0);
	$effect(() => {
		sum2 = a + b; // WRONG!
	});

	// ✅ GOOD - Use $effect for side effects only
	$effect(() => {
		console.log('Sum changed:', sum);
		analytics.track('calculation', { sum });
	});
</script>
```

### Navigation with Remote Functions
When using SvelteKit's `remoteFunctions` feature, standard `<a href>` links don't work for client-side navigation.

```svelte
<script>
	import { goto } from '$app/navigation';
</script>

<!-- ❌ DON'T use regular links with remote functions -->
<a href="/songs/{id}/edit">{title}</a>

<!-- ✅ DO use goto() -->
<button onclick={() => goto(`/songs/${id}/edit`)}>{title}</button>
```

Style buttons as links:
```css
.link-button {
	background: none;
	border: none;
	padding: 0;
	color: inherit;
	cursor: pointer;
	text-decoration: underline;
}
```

### Async Operations and Form Initialization
```svelte
<script>
	let song = $state({ current: null });
	let title = $state('');
	let initialized = $state(false);

	// ✅ GOOD - Use $effect for async initialization
	$effect(() => {
		if (song.current && !initialized) {
			title = song.current.title || '';
			initialized = true;
		}
	});
</script>
```

## SvelteKit Routing

### File Structure
- `+page.svelte` - Page component
- `+page.js` - Universal load (runs server + client)
- `+page.server.js` - Server-only load
- `+layout.svelte` - Layout component (wraps pages)
- `+layout.js` / `+layout.server.js` - Layout load functions
- `+error.svelte` - Error page
- `+server.js` - API endpoints

### Dynamic Routes
- `[slug]` - Single parameter
- `[...rest]` - Rest parameter (catches multiple segments)
- `[[optional]]` - Optional parameter

Example: `src/routes/blog/[slug]/+page.svelte` matches `/blog/hello-world`

### Loading Data

**Page Load** (`+page.js` or `+page.server.js`):
```js
/** @type {import('./$types').PageLoad} */
export function load({ params, url, fetch }) {
	return {
		post: {
			title: `Post ${params.slug}`,
			content: 'Content here'
		}
	};
}
```

**Layout Load** (`+layout.server.js`):
```js
/** @type {import('./$types').LayoutServerLoad} */
export async function load() {
	return {
		sections: [
			{ slug: 'profile', title: 'Profile' },
			{ slug: 'settings', title: 'Settings' }
		]
	};
}
```

**Accessing Data in Components**:
```svelte
<script>
	/** @type {import('./$types').PageProps} */
	let { data } = $props();
</script>

<h1>{data.post.title}</h1>
```

**Parent Data Access**:
```js
export async function load({ parent }) {
	const { user } = await parent();
	return { username: user.name };
}
```

### Universal vs Server Load

**Use `+page.js` (Universal) when**:
- Fetching from public APIs
- No private credentials needed
- Returning custom classes or constructors
- Running same logic server + client

**Use `+page.server.js` (Server) when**:
- Accessing database directly
- Using private environment variables
- Reading from filesystem
- Need to serialize data for client

**Server load returns must be serializable** (JSON + Date, Map, Set, RegExp, BigInt).

### Form Actions

```js
// +page.server.js
export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();
		const email = data.get('email');
		// process form...
		return { success: true };
	}
};
```

```svelte
<!-- +page.svelte -->
<script>
	/** @type {import('./$types').PageProps} */
	let { form } = $props();
</script>

{#if form?.success}
	<p>Success!</p>
{/if}

<form method="POST">
	<input name="email" type="email" />
	<button>Submit</button>
</form>
```

### Real-time Updates (Server-Sent Events)

## shadcn-svelte & Bits UI Integration

This project uses **shadcn-svelte** (built on **Bits UI**) for all UI components.

### MCP Server Tools
The `shadcn-svelte-mcp-server` provides real-time access to component documentation:

| Tool | Purpose |
|------|---------|
| `shadcn-svelte-search` | Find components by name or keyword |
| `shadcn-svelte-get` | Get component installation + code examples |
| `shadcn-svelte-icons` | Search ~1,600 Lucide Svelte icons |
| `bits-ui-get` | Access Bits UI API docs (props, events, data attributes) |

### Knowledge Files
- `@docs/BITS-UI-library-instructions-quick.txt` — Bits UI patterns, styling, date/time components
- `@docs/shadcn-svelte-MCP-SERVER-instructions.md` — MCP server setup and tools

### Workflow for UI Components
1. **Find**: `shadcn-svelte-search("dialog")` → locate component
2. **Install**: `shadcn-svelte-get("dialog")` → `npx shadcn-svelte@latest add dialog`
3. **API Details**: `bits-ui-get("dialog")` → props, events, data attributes
4. **Validate**: `svelte-autofixer(code)` → ensure correct Svelte 5 syntax

### Pre-installed Components
Button, Card, Dialog, Dropdown Menu, Form, Input, Label, Select, Separator, Sheet, Sidebar, Skeleton, Tabs, Tooltip, Avatar, Badge, Scroll Area, Sonner (toast)

## Bits UI Patterns

Bits UI is the headless component library that powers shadcn-svelte. Learn these patterns for custom implementations.

### Child Snippet Pattern (Custom Elements)
Use `child` snippet to replace default elements with custom ones:

```svelte
<Dialog.Trigger>
  {#snippet child({ props })}
    <button {...props} class="my-custom-trigger">Open Dialog</button>
  {/snippet}
</Dialog.Trigger>
```

**Important**: Always spread `{...props}` to maintain ARIA attributes and event handlers.

### Floating Component Wrapper Pattern
For tooltips, popovers, dropdowns - requires wrapper + content elements:

```svelte
<Tooltip.Content>
  {#snippet child({ wrapperProps, props, open })}
    {#if open}
      <div {...wrapperProps}><!-- wrapper for positioning -->
        <div {...props}>Tooltip content here</div><!-- styled content -->
      </div>
    {/if}
  {/snippet}
</Tooltip.Content>
```

**Rule**: Never style the wrapper element - it handles positioning only.

### Data Attributes Styling
Each component applies data attributes for styling without class dependencies:

```css
/* Target all triggers */
[data-dialog-trigger] { padding: 1rem; }

/* Target state */
[data-state="open"] { background-color: var(--accent); }

/* Target disabled */
[data-disabled] { opacity: 0.5; cursor: not-allowed; }
```

**Benefits**: Decouples styling from component naming, works with any CSS framework.

## Lucide Icons (@lucide/svelte)

The project uses Lucide for consistent iconography (~1,600 icons available).

```svelte
<script>
  import { House, Settings, Image, Bot, Pencil } from '@lucide/svelte';
</script>

<!-- Size and color control -->
<House class="size-4" />
<Bot class="size-6 text-muted-foreground" />
<Settings class="size-5 text-primary" />
```

**Find icons**: Use MCP tool `shadcn-svelte-icons` with search terms:
- By name: `"arrow", "user", "settings"`
- By category: `"chevron", "menu", "share"`

## Project References

For deeper context, see:
- **AGENTS.md** → "shadcn-svelte MCP Server & Bits UI" for MCP workflows
- **AGENTS.md** → "Svelte MCP" for mandatory code validation
- **AGENTS.md** → "Desktop UI rules" for Electron + Svelte patterns

## Remote Functions Navigation

**Purpose**: Navigate using `goto()` when SvelteKit remote functions are enabled, styling buttons as links.

**Pattern**:
```svelte
<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	
	let { id, title } = $props();
</script>

<!-- ❌ DON'T use regular links with remote functions -->
<a href="/songs/{id}/edit">{title}</a>

<!-- ✅ DO use goto() -->
<button 
	onclick={() => goto(`/songs/${id}/edit`)}
	class="link-button"
>
	{title}
</button>

<style>
	.link-button {
		background: none;
		border: none;
		padding: 0;
		color: inherit;
		cursor: pointer;
		text-decoration: underline;
		font-family: inherit;
		font-size: inherit;
	}
	
	.link-button:hover {
		color: #3b82f6;
	}
</style>
```

**Navigation with Parameters**:
```svelte
<script lang="ts">
	import { goto } from '$app/navigation';
	
	let { albumId, photoId } = $props();
	
	function navigateToPhoto() {
		goto(`/albums/${albumId}/photos/${photoId}`);
	}
	
	function navigateToEdit() {
		goto(`/photos/${photoId}/edit`);
	}
</script>

<div class="navigation-buttons">
	<button onclick={navigateToPhoto} class="link-button">
		View Photo
	</button>
	<button onclick={navigateToEdit} class="link-button">
		Edit Photo
	</button>
</div>
```

**Programmatic Navigation**:
```typescript
// utils/navigation.ts
import { goto } from '$app/navigation';

export async function navigateWithConfirmation(
	path: string,
	message: string
): Promise<boolean> {
	const confirmed = confirm(message);
	if (confirmed) {
		await goto(path);
		return true;
	}
	return false;
}

export function navigateBack() {
	window.history.back();
}

export function navigateWithState(path: string, state: Record<string, unknown>) {
	// Store state before navigation
	sessionStorage.setItem('navigationState', JSON.stringify(state));
	goto(path);
}
```

## Server-Sent Events for Agent Communication

**Purpose**: Implement SSE client in Svelte 5 for real-time agent updates with reconnection logic.

**Pattern**:
```svelte
<script lang="ts">
	import { onMount } from 'svelte';
	
	let agentStatus = $state<'idle' | 'working' | 'error'>('idle');
	let progress = $state(0);
	let lastMessage = $state('');
	let isConnected = $state(false);
	let error = $state<string | null>(null);
	let eventSource: EventSource | null = null;
	
	onMount(() => {
		connectToAgentStream();
		
		return () => {
			if (eventSource) {
				eventSource.close();
			}
		};
	});
	
	function connectToAgentStream() {
		eventSource = new EventSource('/api/agent/stream');
		
		eventSource.onopen = () => {
			isConnected = true;
			error = null;
			agentStatus = 'idle';
			console.log('SSE connection opened');
		};
		
		eventSource.onmessage = (e) => {
			try {
				const data = JSON.parse(e.data);
				
				switch (data.status) {
					case 'thinking':
						agentStatus = 'working';
						lastMessage = data.message || 'Processing...';
						break;
					case 'working':
						agentStatus = 'working';
						progress = data.progress || 0;
						lastMessage = data.message || 'Working...';
						break;
					case 'result':
						agentStatus = 'idle';
						lastMessage = 'Completed!';
						progress = 100;
						break;
					case 'error':
						agentStatus = 'error';
						error = data.message || 'Unknown error';
						lastMessage = 'Failed';
						break;
				}
			} catch (err) {
				console.error('Failed to parse SSE message:', err);
				error = 'Invalid data received';
			}
		};
		
		eventSource.onerror = () => {
			isConnected = false;
			agentStatus = 'error';
			error = 'Connection lost';
			console.error('SSE connection error');
			
			// Attempt reconnection after 5 seconds
			setTimeout(() => {
				if (!isConnected) {
					connectToAgentStream();
				}
			}, 5000);
		};
	}
	
	function disconnect() {
		if (eventSource) {
			eventSource.close();
			eventSource = null;
			isConnected = false;
			agentStatus = 'idle';
		}
	}
</script>

<div class="agent-status-container">
	<!-- Status Badge -->
	<div class="status-bar mb-4 p-4 rounded border">
		{#if error}
			<div class="flex items-center gap-2 text-red-600">
				<span class="text-xl">⚠️</span>
				<span>{error}</span>
				<button onclick={connectToAgentStream} class="text-blue-600 underline">
					Reconnect
				</button>
			</div>
		{:else}
			<div class="flex items-center gap-2">
				<span class="text-xl">
					{#if agentStatus === 'idle'}
						🟢
					{:else if agentStatus === 'working'}
						🔄
					{:else if agentStatus === 'error'}
						🔴
					{/if}
				</span>
				<span class="font-medium">
					{#if agentStatus === 'idle'}
						Idle
					{:else if agentStatus === 'working'}
						Working
					{:else if agentStatus === 'error'}
						Error
					{/if}
				</span>
				{#if isConnected}
					<button onclick={disconnect} class="text-red-600 underline ml-4">
						Disconnect
					</button>
				{/if}
			</div>
		{/if}
	</div>
	
	<!-- Progress Bar -->
	{#if agentStatus === 'working' && progress > 0}
		<div class="progress-container mb-4">
			<div class="progress-bar">
				<div class="progress-fill" style="width: {progress}%"></div>
			</div>
			<span class="progress-text">{progress}%</span>
		</div>
	{/if}
	
	<!-- Last Message -->
	{#if lastMessage}
		<div class="message-box p-3 rounded bg-gray-50 border">
			{lastMessage}
		</div>
	{/if}
</div>

<style>
	.agent-status-container {
		@apply max-w-2xl mx-auto p-6;
	}
	
	.status-bar {
		@apply bg-gray-100;
	}
	
	.progress-container {
		@apply bg-white border rounded p-4;
	}
	
	.progress-bar {
		@apply h-4 bg-gray-200 rounded-full overflow-hidden;
	}
	
	.progress-fill {
		@apply h-full bg-blue-600 transition-all duration-300;
	}
	
	.progress-text {
		@apply text-sm font-medium text-gray-600;
	}
	
	.message-box {
		@apply text-sm;
	}
</style>
```

**SSE Event Types**:
```typescript
// types/sse-events.ts
export interface AgentSSEEvent {
	event: string;
	data: {
		status: 'idle' | 'thinking' | 'working' | 'result' | 'error';
		message?: string;
		progress?: number;
		result?: unknown;
		agentId?: string;
	};
	timestamp: number;
}

export interface AgentStatusUpdate {
	status: 'idle' | 'thinking' | 'working' | 'result' | 'error';
	message?: string;
	progress?: number;
}

export interface AgentResult {
	result: unknown;
	executionTime: number;
	agentId: string;
}
```

**Reconnection Logic**:
```svelte
<script lang="ts">
	let reconnectAttempts = $state(0);
	let reconnectDelay = $state(1000); // Start with 1 second
	const MAX_RECONNECT_ATTEMPTS = 5;
	const MAX_RECONNECT_DELAY = 30000; // 30 seconds max
	
	function handleConnectionError() {
		if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
			reconnectAttempts += 1;
			console.log(`Reconnection attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS} in ${reconnectDelay}ms`);
			
			setTimeout(() => {
				connectToAgentStream();
			}, reconnectDelay);
			
			// Exponential backoff
			reconnectDelay = Math.min(reconnectDelay * 2, MAX_RECONNECT_DELAY);
		} else {
			error = 'Max reconnection attempts reached. Please refresh the page.';
		}
	}
	
	function resetConnection() {
		reconnectAttempts = 0;
		reconnectDelay = 1000;
		error = null;
	}
</script>
```


**Server** (`+server.js`):
```js
export function GET() {
	const stream = new ReadableStream({
		start(controller) {
			const encoder = new TextEncoder();
			const send = (data) => {
				controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`));
			};
			// Send updates...
			setInterval(() => send({ time: Date.now() }), 1000);
		}
	});

	return new Response(stream, {
		headers: {
			'Content-Type': 'text/event-stream',
			'Cache-Control': 'no-cache'
		}
	});
}
```

**Client**:
```svelte
<script>
	let data = $state({ time: 0 });

	$effect(() => {
		const source = new EventSource('/updates');
		source.onmessage = (e) => {
			data = JSON.parse(e.data);
		};
		return () => source.close();
	});
</script>
```

## Environment Variables

**Public** (exposed to client):
```js
import { PUBLIC_STATION_NAME } from '$env/static/public';
```

**Private** (server-only):
```js
import { DATABASE_URL } from '$env/static/private';
```

## Component Patterns

### Snippets and Render
Reusable markup patterns:

```svelte
<script>
	let items = $state(['a', 'b', 'c']);
</script>

{#snippet listItem(item)}
	<li>{item}</li>
{/snippet}

<ul>
	{#each items as item}
		{@render listItem(item)}
	{/each}
</ul>
```

### Conditional Rendering
```svelte
{#if condition}
	<p>True</p>
{:else if otherCondition}
	<p>Other</p>
{:else}
	<p>False</p>
{/if}
```

### Lists
```svelte
{#each items as item, index (item.id)}
	<div>{index}: {item.name}</div>
{/each}
```

**Always use keys** (the `(item.id)` part) for dynamic lists!

### Async/Await (Svelte 5.36+)
Requires `experimental.async: true` in config:

```svelte
<script>
	async function fetchData() {
		const res = await fetch('/api/data');
		return res.json();
	}
</script>

<p>{await fetchData()}</p>

<!-- Or with #await -->
{#await fetchData()}
	Loading...
{:then data}
	<p>{data.message}</p>
{:catch error}
	<p>Error: {error.message}</p>
{/await}
```

## Best Practices

1. **Use $derived, not $effect, for computed values**
2. **Don't mutate props** (use callbacks or $bindable)
3. **Use $effect.pre only when necessary** (before DOM updates)
4. **Always provide keys in {#each} blocks** for dynamic lists
5. **Prefer server load functions** for sensitive data
6. **Use goto() for navigation** when remote functions are enabled
7. **Type your components** with `PageProps`, `LayoutProps`, etc.

## When to Consult External Resources

This skill covers the most common Svelte 5 and SvelteKit patterns. For advanced topics, refer to:
- SvelteKit adapters and deployment
- Advanced routing (route groups, breaking layouts)
- Hooks (handle, handleFetch, handleError)
- Service workers and offline support
- Custom Svelte stores (when not using runes)
- Migration from Svelte 4
- Testing strategies
- TypeScript advanced types

Remember: Start with the fundamentals in this skill, then explore advanced topics as needed.
