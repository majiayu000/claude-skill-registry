---
name: error-handling-patterns
# prettier-ignore
description: Svelte 5 error handling. Use for error boundaries, async await expressions, loading states, and form errors.
---

# Error Handling Patterns

## Quick Start

```svelte
<svelte:boundary>
	<ul>
		{#each await get_contacts() as contact}
			<li>{contact.name}</li>
		{/each}
	</ul>

	{#snippet pending()}
		<div class="loading">Loading...</div>
	{/snippet}

	{#snippet failed(error, reset)}
		<div class="error">
			<p>Error: {error.message}</p>
			<button onclick={reset}>Retry</button>
		</div>
	{/snippet}
</svelte:boundary>
```

## Core Principles

- **Error boundaries**: Use `<svelte:boundary>` to catch component
  errors
- **Pending snippet**: Show loading state while awaiting data
- **Failed snippet**: Display errors with retry via `reset` function
- **Await expressions**: Use `{#each await query()}` directly in
  markup
- **Granular boundaries**: Wrap individual features, not entire pages
- **Form errors**: Check remote function `.error` property (e.g.,
  `create_contact.error`)

## Reference Files

- [error-handling-guide.md](references/error-handling-guide.md) -
  Complete patterns and examples
