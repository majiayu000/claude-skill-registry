---
name: svelte
description: Svelte 5 patterns including TanStack Query mutations, shadcn-svelte components, and component composition. Use when writing Svelte components, using TanStack Query, or working with shadcn-svelte UI.
---

# Svelte Guidelines

# Mutation Pattern Preference

## In Svelte Files (.svelte)

Always prefer `createMutation` from TanStack Query for mutations. This provides:

- Loading states (`isPending`)
- Error states (`isError`)
- Success states (`isSuccess`)
- Better UX with automatic state management

### The Preferred Pattern

Pass `onSuccess` and `onError` as the second argument to `.mutate()` to get maximum context:

```svelte
<script lang="ts">
	import { createMutation } from '@tanstack/svelte-query';
	import * as rpc from '$lib/query';

	// Create mutation with just .options (no parentheses!)
	const deleteSessionMutation = createMutation(
		rpc.sessions.deleteSession.options,
	);

	// Local state that we can access in callbacks
	let isDialogOpen = $state(false);
</script>

<Button
	onclick={() => {
		// Pass callbacks as second argument to .mutate()
		deleteSessionMutation.mutate(
			{ sessionId },
			{
				onSuccess: () => {
					// Access local state and context
					isDialogOpen = false;
					toast.success('Session deleted');
					goto('/sessions');
				},
				onError: (error) => {
					toast.error(error.title, { description: error.description });
				},
			},
		);
	}}
	disabled={deleteSessionMutation.isPending}
>
	{#if deleteSessionMutation.isPending}
		Deleting...
	{:else}
		Delete
	{/if}
</Button>
```

### Why This Pattern?

- **More context**: Access to local variables and state at the call site
- **Better organization**: Success/error handling is co-located with the action
- **Flexibility**: Different calls can have different success/error behaviors

## In TypeScript Files (.ts)

Always use `.execute()` since createMutation requires component context:

```typescript
// In a .ts file (e.g., load function, utility)
const result = await rpc.sessions.createSession.execute({
	body: { title: 'New Session' },
});

const { data, error } = result;
if (error) {
	// Handle error
} else if (data) {
	// Handle success
}
```

## Exception: When to Use .execute() in Svelte Files

Only use `.execute()` in Svelte files when:

1. You don't need loading states
2. You're performing a one-off operation
3. You need fine-grained control over async flow

## Inline Simple Handler Functions

When a handler function only calls `.mutate()`, inline it directly:

```svelte
<!-- Avoid: Unnecessary wrapper function -->
<script>
	function handleShare() {
		shareMutation.mutate({ id });
	}
</script>

<!-- Good: Inline simple handlers -->
<Button onclick={() => shareMutation.mutate({ id })}>Share</Button>
<Button onclick={handleShare}>Share</Button>
```

# Styling

For general CSS and Tailwind guidelines, see the `styling` skill.

# shadcn-svelte Best Practices

## Component Organization

- Use the CLI: `bunx shadcn-svelte@latest add [component]`
- Each component in its own folder under `$lib/components/ui/` with an `index.ts` export
- Follow kebab-case for folder names (e.g., `dialog/`, `toggle-group/`)
- Group related sub-components in the same folder
- When using $state, $derived, or functions only referenced once in markup, inline them directly

## Import Patterns

**Namespace imports** (preferred for multi-part components):

```typescript
import * as Dialog from '$lib/components/ui/dialog';
import * as ToggleGroup from '$lib/components/ui/toggle-group';
```

**Named imports** (for single components):

```typescript
import { Button } from '$lib/components/ui/button';
import { Input } from '$lib/components/ui/input';
```

**Lucide icons** (always use individual imports from `@lucide/svelte`):

```typescript
// Good: Individual icon imports
import Database from '@lucide/svelte/icons/database';
import MinusIcon from '@lucide/svelte/icons/minus';
import MoreVerticalIcon from '@lucide/svelte/icons/more-vertical';

// Bad: Don't import multiple icons from lucide-svelte
import { Database, MinusIcon, MoreVerticalIcon } from 'lucide-svelte';
```

The path uses kebab-case (e.g., `more-vertical`, `minimize-2`), and you can name the import whatever you want (typically PascalCase with optional Icon suffix).

## Styling and Customization

- Always use the `cn()` utility from `$lib/utils` for combining Tailwind classes
- Modify component code directly rather than overriding styles with complex CSS
- Use `tailwind-variants` for component variant systems
- Follow the `background`/`foreground` convention for colors
- Leverage CSS variables for theme consistency

## Component Usage Patterns

Use proper component composition following shadcn-svelte patterns:

```svelte
<Dialog.Root bind:open={isOpen}>
	<Dialog.Trigger>
		<Button>Open</Button>
	</Dialog.Trigger>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Title</Dialog.Title>
		</Dialog.Header>
	</Dialog.Content>
</Dialog.Root>
```

## Custom Components

- When extending shadcn components, create wrapper components that maintain the design system
- Add JSDoc comments for complex component props
- Ensure custom components follow the same organizational patterns
- Consider semantic appropriateness (e.g., use section headers instead of cards for page sections)

# Self-Contained Component Pattern

## A2UI Widget Generation

**Purpose**: Create dynamically generated UI components from agent configurations with type safety and shadcn-svelte integration.

**Pattern**:
```svelte
<script lang="ts">
	import { createMutation } from '@tanstack/svelte-query';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	
	interface AgentWidgetProps {
		widgetType: string;
		config: Record<string, unknown>;
		onAction: (action: string, data: unknown) => void;
	}
	
	let { widgetType, config, onAction }: AgentWidgetProps = $props();
	
	// Dynamic component loading based on agent-generated config
	let WidgetComponent: any;
	$effect(async () => {
		try {
			WidgetComponent = (await import(`./widgets/${widgetType}.svelte`)).default;
		} catch (e) {
			console.error(`Failed to load widget: ${widgetType}`, e);
		}
	});
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>{config.title || 'Agent Widget'}</Card.Title>
		<Badge variant={config.status === 'active' ? 'default' : 'secondary'}>
			{config.status || 'idle'}
		</Badge>
	</Card.Header>
	<Card.Content>
		{#if WidgetComponent}
			<svelte:component this={WidgetComponent} {config} onAction={onAction} />
		{:else}
			<p>Loading widget...</p>
		{/if}
	</Card.Content>
	<Card.Footer>
		<Button onclick={() => onAction('refresh', config)}>
			Refresh
		</Button>
	</Card.Footer>
</Card.Root>
```

**Widget Component Example**:
```svelte
<!-- widgets/caption-editor.svelte -->
<script lang="ts">
	interface CaptionEditorProps {
		config: {
			mediaId: string;
			currentCaption: string;
			platform: string;
		};
		onAction: (action: string, data: unknown) => void;
	}
	
	let { config, onAction }: CaptionEditorProps = $props();
	let caption = $state(config.currentCaption);
	
	function handleSave() {
		onAction('save-caption', { mediaId: config.mediaId, caption });
	}
</script>

<div class="p-4 border rounded">
	<h3 class="text-lg font-semibold mb-2">Edit Caption</h3>
	<p class="text-sm text-gray-600 mb-2">Platform: {config.platform}</p>
	<textarea 
		bind:value={caption} 
		class="w-full p-2 border rounded"
		rows="4"
		placeholder="Enter caption..."
	/>
	<div class="flex gap-2 mt-4">
		<Button onclick={handleSave}>Save</Button>
		<Button variant="outline" onclick={() => onAction('cancel', config)}>Cancel</Button>
	</div>
</div>
```

**Type Safety for Agent-Generated Props**:
```typescript
// types/agent-widgets.ts
export interface AgentWidgetConfig {
	title: string;
	widgetType: 'caption-editor' | 'media-preview' | 'schedule-picker' | 'analytics';
	status: 'idle' | 'loading' | 'active' | 'error';
	data: Record<string, unknown>;
}

export interface CaptionEditorConfig extends AgentWidgetConfig {
	widgetType: 'caption-editor';
	mediaId: string;
	currentCaption: string;
	platform: 'instagram' | 'facebook' | 'linkedin' | 'twitter' | 'tiktok';
}

export interface MediaPreviewConfig extends AgentWidgetConfig {
	widgetType: 'media-preview';
	mediaUrl: string;
	mediaType: 'image' | 'video';
	thumbnailUrl?: string;
}

// Type guard for widget configs
function isCaptionEditorConfig(config: AgentWidgetConfig): config is CaptionEditorConfig {
	return config.widgetType === 'caption-editor';
}
```

## Twick Timeline Integration

**Purpose**: Integrate Twick timeline component with agent-generated events and optimistic updates.

**Pattern**:
```svelte
<script lang="ts">
	import { Timeline, TimelineEvent } from 'twick-svelte';
	import { createMutation } from '@tanstack/svelte-query';
	import * as rpc from '$lib/query';
	
	let events = $state<TimelineEvent[]>([]);
	
	const addEventMutation = createMutation({
		mutationFn: async (event: TimelineEvent) => {
			// Optimistic update
			events = [...events, event];
			
			// Then sync with backend
			await window.electronAPI.addTimelineEvent(event);
		},
		onSuccess: () => {
			console.log('Event added successfully');
		},
		onError: (error) => {
			console.error('Failed to add event:', error);
			// Rollback optimistic update
			events = events.filter(e => e.id !== event.id);
		}
	});
	
	// Listen for agent-generated events
	$effect(() => {
		const listener = (event: CustomEvent) => {
			addEventMutation.mutate(event.detail);
		};
		window.addEventListener('agent:event', listener);
		return () => window.removeEventListener('agent:event', listener);
	});
</script>

<div class="p-6">
	<h2 class="text-2xl font-bold mb-4">Content Timeline</h2>
	
	<Timeline {events} bind:events>
		<svelte:fragment slot="event" let:event>
			<div class="timeline-event">
				<div class="event-header">
					<span class="event-type">{event.type}</span>
					<span class="event-time">{new Date(event.timestamp).toLocaleString()}</span>
				</div>
				<div class="event-content">
					{event.data}
				</div>
			</div>
		</svelte:fragment>
	</Timeline>
</div>

<style>
	.timeline-event {
		@apply p-4 mb-4 border-l-2 border-gray-200 rounded;
	}
	
	.event-header {
		@apply flex justify-between items-center mb-2;
	}
	
	.event-type {
		@apply px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm font-medium;
	}
	
	.event-time {
		@apply text-sm text-gray-500;
	}
	
	.event-content {
		@apply text-gray-700;
	}
</style>
```

**Agent Event Generation**:
```typescript
// utils/agent-events.ts
export interface AgentEvent {
	id: string;
	type: 'thinking' | 'tool_call' | 'result' | 'error' | 'progress';
	timestamp: number;
	data: Record<string, unknown>;
}

export function createAgentEvent(
	type: AgentEvent['type'],
	data: Record<string, unknown>
): AgentEvent {
	return {
		id: crypto.randomUUID(),
		type,
		timestamp: Date.now(),
		data
	};
}

// Convert agent SSE events to timeline events
export function agentEventToTimelineEvent(agentEvent: AgentEvent): TimelineEvent {
	return {
		id: agentEvent.id,
		timestamp: agentEvent.timestamp,
		type: agentEvent.type,
		data: agentEvent.data,
		metadata: {
			source: 'agent',
			agentId: agentEvent.data.agentId
		}
	};
}
```

**Optimistic Update Pattern**:
```svelte
<script lang="ts">
	import { createMutation } from '@tanstack/svelte-query';
	
	let events = $state<TimelineEvent[]>([]);
	
	const updateEventMutation = createMutation({
		mutationFn: async (updates: Partial<TimelineEvent>) => {
			// Find and update event optimistically
			const index = events.findIndex(e => e.id === updates.id);
			if (index !== -1) {
				const updatedEvents = [...events];
				updatedEvents[index] = { ...events[index], ...updates };
				events = updatedEvents;
			}
			
			// Sync with backend
			await window.electronAPI.updateTimelineEvent(updates);
		},
		onError: (error, variables) => {
			console.error('Failed to update event:', error);
			// Rollback on error
			if (variables.id) {
				const originalEvent = events.find(e => e.id === variables.id);
				if (originalEvent) {
					events = events.map(e => 
						e.id === variables.id ? originalEvent : e
					);
				}
			}
		}
	});
</script>
```

## SSE Streaming Components

**Purpose**: Create components that receive real-time streaming updates from agents via Server-Sent Events.

**Pattern**:
```svelte
<script lang="ts">
	import { onMount } from 'svelte';
	
	let messages = $state<string[]>([]);
	let isConnected = $state(false);
	let error = $state<string | null>(null);
	let eventSource: EventSource | null = null;
	
	onMount(() => {
		connectToStream();
		
		return () => {
			if (eventSource) {
				eventSource.close();
			}
		};
	});
	
	function connectToStream() {
		eventSource = new EventSource('http://localhost:8000/agent/stream/req-123');
		
		eventSource.onopen = () => {
			isConnected = true;
			error = null;
			console.log('SSE connection opened');
		};
		
		eventSource.onmessage = (e) => {
			try {
				const data = JSON.parse(e.data);
				
				switch (data.event_type) {
					case 'thinking':
						messages = [...messages, `🤔 ${data.data.message}`];
						break;
					case 'tool_call':
						messages = [...messages, `🔧 Tool: ${data.data.tool}`];
						break;
					case 'result':
						messages = [...messages, `✅ Result: ${JSON.stringify(data.data.result)}`];
						break;
					case 'error':
						messages = [...messages, `❌ Error: ${data.data.message}`];
						error = data.data.message;
						break;
					case 'progress':
						messages = [...messages, `⏳ Progress: ${data.data.progress}%`];
						break;
				}
			} catch (err) {
				console.error('Failed to parse SSE message:', err);
			}
		};
		
		eventSource.onerror = () => {
			isConnected = false;
			error = 'Connection lost';
			console.error('SSE connection error');
			
			// Attempt reconnection after 5 seconds
			setTimeout(() => {
				if (!isConnected) {
					connectToStream();
				}
			}, 5000);
		};
	}
	
	function disconnect() {
		if (eventSource) {
			eventSource.close();
			eventSource = null;
			isConnected = false;
		}
	}
</script>

<div class="agent-stream-container">
	<!-- Connection Status -->
	<div class="status-bar mb-4 p-3 rounded border">
		{#if error}
			<div class="flex items-center gap-2 text-red-600">
				<span class="text-xl">⚠️</span>
				<span>{error}</span>
				<button onclick={connectToStream} class="text-blue-600 underline">
					Reconnect
				</button>
			</div>
		{:else if isConnected}
			<div class="flex items-center gap-2 text-green-600">
				<span class="text-xl">🟢</span>
				<span>Connected to agent stream</span>
				<button onclick={disconnect} class="text-red-600 underline">
					Disconnect
				</button>
			</div>
		{:else}
			<div class="flex items-center gap-2 text-gray-600">
				<span class="text-xl">⚪</span>
				<span>Disconnected</span>
				<button onclick={connectToStream} class="text-blue-600 underline">
					Connect
				</button>
			</div>
		{/if}
	</div>
	
	<!-- Stream Messages -->
	<div class="messages-container space-y-2 max-h-96 overflow-y-auto">
		{#each messages as message, index (message)}
			<div class="message p-3 rounded bg-gray-50 border" class:animate-in={index === messages.length - 1}>
				{message}
			</div>
		{/each}
	</div>
</div>

<style>
	.agent-stream-container {
		@apply max-w-4xl mx-auto p-6;
	}
	
	.status-bar {
		@apply bg-gray-100;
	}
	
	.messages-container {
		@apply bg-white border rounded p-4;
	}
	
	.message {
		@apply text-sm;
	}
	
	.message.animate-in {
		animation: fadeIn 0.3s ease-in;
	}
	
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
```

**SSE Event Types**:
```typescript
// types/sse-events.ts
export interface SSEMessage {
	event_type: 'thinking' | 'tool_call' | 'result' | 'error' | 'progress' | 'keepalive';
	data: {
		message?: string;
		tool?: string;
		result?: unknown;
		progress?: number;
		agentId?: string;
	};
	timestamp: number;
}

export interface AgentThinkingEvent {
	event_type: 'thinking';
	data: {
		agentId: string;
		message: string;
		step: number;
		totalSteps: number;
	};
	timestamp: number;
}

export interface AgentToolCallEvent {
	event_type: 'tool_call';
	data: {
		agentId: string;
		tool: string;
		parameters: Record<string, unknown>;
	};
	timestamp: number;
}

export interface AgentResultEvent {
	event_type: 'result';
	data: {
		agentId: string;
		result: unknown;
		executionTime: number;
	};
	timestamp: number;
}
```

**Error Handling and Reconnection**:
```svelte
<script lang="ts">
	let reconnectAttempts = $state(0);
	const MAX_RECONNECT_ATTEMPTS = 5;
	const RECONNECT_DELAY = 3000; // 3 seconds
	
	function handleConnectionError() {
		if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
			reconnectAttempts += 1;
			console.log(`Reconnection attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS}`);
			setTimeout(connectToStream, RECONNECT_DELAY);
		} else {
			error = 'Max reconnection attempts reached. Please refresh the page.';
		}
	}
	
	function resetConnection() {
		reconnectAttempts = 0;
		error = null;
	}
</script>
```


## Prefer Component Composition Over Parent State Management

When building interactive components (especially with dialogs/modals), create self-contained components rather than managing state at the parent level.

### The Anti-Pattern (Parent State Management)

```svelte
<!-- Parent component -->
<script>
	let deletingItem = $state(null);

	function handleDelete(item) {
		// delete logic
		deletingItem = null;
	}
</script>

{#each items as item}
	<Button onclick={() => (deletingItem = item)}>Delete</Button>
{/each}

<AlertDialog open={!!deletingItem}>
	<!-- Single dialog for all items -->
</AlertDialog>
```

### The Pattern (Self-Contained Components)

```svelte
<!-- DeleteItemButton.svelte -->
<script>
	let { item } = $props();
	let open = $state(false);

	function handleDelete() {
		// delete logic directly in component
	}
</script>

<AlertDialog.Root bind:open>
	<AlertDialog.Trigger>
		<Button>Delete</Button>
	</AlertDialog.Trigger>
	<AlertDialog.Content>
		<!-- Dialog content -->
	</AlertDialog.Content>
</AlertDialog.Root>

<!-- Parent component -->
{#each items as item}
	<DeleteItemButton {item} />
{/each}
```

### Why This Pattern Works

- **No parent state pollution**: Parent doesn't need to track which item is being deleted
- **Better encapsulation**: All delete logic lives in one place
- **Simpler mental model**: Each row has its own delete button with its own dialog
- **No callbacks needed**: Component handles everything internally
- **Scales better**: Adding new actions doesn't complicate the parent

### When to Apply This Pattern

- Action buttons in table rows (delete, edit, etc.)
- Confirmation dialogs for list items
- Any repeating UI element that needs modal interactions
- When you find yourself passing callbacks just to update parent state

The key insight: It's perfectly fine to instantiate multiple dialogs (one per row) rather than managing a single shared dialog with complex state. Modern frameworks handle this efficiently, and the code clarity is worth it.
