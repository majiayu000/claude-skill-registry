---
name: sveltekit-patterns
# prettier-ignore
description: SvelteKit patterns for devhub-crm. Use for remote functions (query, form, command), routing, and server-side logic.
---

# SvelteKit Patterns

## Quick Start

```typescript
// Query: Read data
export const get_contacts = query(() =>
	db.prepare('SELECT * FROM contacts').all(),
);

// Form: Validated mutation with redirect
export const create = form(
	v.object({ name: v.string() }),
	async ({ name }) => {
		db.prepare('INSERT INTO contacts ...').run(id, name);
		redirect(303, '/contacts');
	},
);

// Command: Mutation with refresh
export const delete_contact = command(v.string(), async (id) => {
	db.prepare('DELETE FROM contacts WHERE id = ?').run(id);
	await get_contacts().refresh();
	return { success: true };
});
```

## Core Principles

- **Types**: `query` (read), `form` (mutations + redirects), `command`
  (mutations only)
- **Validation**: Use valibot schemas for all inputs
- **Security**: Always include `user_id` in WHERE clauses
- **Batching**: Use `query.batch()` for N+1 prevention
- **Refresh**: Call `.refresh()` in form/command handlers
- **Use `.current`**: Store queries in variables, check
  `.current === undefined` for initial load
- **No manual keys**: Never use `refresh_key++` or `{#key}` blocks
- **Return values**: Commands must return `{ success: true }`

## Reference Files

- [remote-functions.md](references/remote-functions.md) - Complete
  remote functions API
- [routing.md](references/routing.md) - File-based routing patterns
- [database-patterns.md](references/database-patterns.md) - Advanced
  database queries
