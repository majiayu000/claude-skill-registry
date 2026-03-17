---
name: sveltekit-data-flow
description: SvelteKit data flow guidance. Use for load functions, form actions, and server/client data. Covers +page.server.ts vs +page.ts, serialization, fail(), redirect(), error().
---

# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
# SvelteKit Data Flow

## Quick Start

**Which file?** Server-only (DB/secrets): `+page.server.ts` |
Universal (runs both): `+page.ts` | API: `+server.ts`

**Load decision:** Need server resources? → server load | Need client
APIs? → universal load

**Form actions:** Always `+page.server.ts`. Return `fail()` for
errors, throw `redirect()` to navigate, throw `error()` for failures.

## Example

```typescript
// +page.server.ts
import { fail, redirect } from '@sveltejs/kit';

export const load = async ({ locals }) => {
	const user = await db.users.get(locals.userId);
	return { user }; // Must be JSON-serializable
};

export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();
		const email = data.get('email');

		if (!email) return fail(400, { email, missing: true });

		await updateEmail(email);
		throw redirect(303, '/success');
	},
};
```

## Reference Files

- [load-functions.md](references/load-functions.md) - Server vs
  universal
- [form-actions.md](references/form-actions.md) - Form handling
  patterns
- [serialization.md](references/serialization.md) - What can/can't
  serialize
- [error-redirect-handling.md](references/error-redirect-handling.md) -
  fail/redirect/error

## Notes

- Server load → universal load via `data` param | ALWAYS
  `throw redirect()/error()`
- No class instances/functions from server load (not serializable)
- **Last verified:** 2025-01-11

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
