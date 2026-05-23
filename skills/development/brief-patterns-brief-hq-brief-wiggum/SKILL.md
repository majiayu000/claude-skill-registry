---
description: Brief-specific code patterns and conventions
---

# Brief Code Patterns

## API Route Pattern

Every API route must:
- Use Zod for request validation (import from 'zod')
- Check authentication via authenticateApiKey() or auth() from Clerk
- Return standardized error responses (use NextResponse)
- Log errors properly (use lib/logger)

Example:
```typescript
import { z } from 'zod';
import { authenticateApiKey } from '@/lib/api/auth';
import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

const schema = z.object({ /* ... */ });

export async function POST(req: Request) {
  // API key auth (reads from headers internally)
  const apiAuth = await authenticateApiKey();
  if (!apiAuth.ok) {
    return NextResponse.json({ error: apiAuth.error }, { status: 401 });
  }

  // OR session auth
  const session = await auth();
  if (!session.userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = schema.parse(await req.json());
  // ...
}
```

## Brief MCP Integration

- folder_id is REQUIRED for create_document (no default)
- ALWAYS call get_folder_tree first to find valid folder IDs
- Documents use soft delete (go to trash, recoverable)
- ASK before delete_document, delete_folder, bulk_delete

## Database Patterns

- RLS is enforced on all tables via Supabase
- Use `createAdminClient()` from `@/lib/supabase/admin` for server-side queries
- NEVER bypass RLS in application code
- Always filter by `org_id` in queries (RLS handles this automatically)

### Database Migrations (CRITICAL)

**⚠️ NEVER hand-write migration SQL files. ALWAYS use drizzle-kit generate.**

```bash
# 1. Edit schema.ts with your changes
vim lib/db/drizzle/schema.ts

# 2. Generate migration (REQUIRED - never skip this)
DRIZZLE_DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:54322/postgres" pnpm db:drizzle:generate

# 3. For non-schema objects (functions, triggers, extensions):
DRIZZLE_DATABASE_URL="..." pnpm db:drizzle:generate --custom --name=my-functions

# 4. Review the generated SQL, then apply locally
DRIZZLE_DATABASE_URL="..." pnpm db:drizzle:migrate
```

**Migration Types:**

| Type | Use For | Command |
|------|---------|---------|
| Generated | Columns, tables, indexes, constraints | `pnpm db:drizzle:generate` |
| Custom | Functions, triggers, extensions, data migrations | `pnpm db:drizzle:generate --custom --name=description` |

**Why This Matters:**
- Hand-written migrations break Drizzle's state tracking (journal + snapshots)
- Without proper state, `drizzle-kit generate` regenerates the ENTIRE schema
- This causes massive migrations that recreate all 48 tables

**Full documentation:** `docs/architecture/database.md`

## Testing Requirements

- All API routes need tests (use Vitest)
- All custom hooks need tests
- Mock Supabase with test fixtures
- Mock Clerk auth in tests:
  ```typescript
  vi.mock('@clerk/nextjs/server', () => ({
    auth: vi.fn(),
  }));

  const mockAuth = vi.mocked(await import('@clerk/nextjs/server')).auth;
  mockAuth.mockResolvedValue({ userId: 'test-user', orgId: 'test-org' });
  ```
- Test error paths, not just happy path

## Component Reuse & Design System

> **Deep Dive**: For typography, colors, motion, and anti-patterns, see the `brief-design` skill and its `reference/` docs.

### Design System Enforcement

**Before creating any component**:
1. Search for existing components in codebase
2. Check TailStack design system (`@/components/ui/*`)
3. Prefer composition and extension over duplication
4. Run `/design-audit` to check compliance

**TailStack Components** (`@/components/ui/*`):
- Button, Input, Card, Dialog, Select, Textarea, etc.
- ALWAYS use these over custom implementations
- Extend via composition, not duplication

**Good - Compose from design system:**
```typescript
import { Button } from '@/components/ui/button';

export function SubmitButton({ children, ...props }) {
  return (
    <Button variant="primary" size="lg" {...props}>
      {children}
    </Button>
  );
}
```

**Bad - Create custom button:**
```typescript
// ❌ DON'T create custom button when Button exists
export function MyButton() {
  return <button className="px-4 py-2 bg-blue-500">Submit</button>;
}
```

### Tailwind CSS Best Practices

- Use utility classes, not custom CSS files
- Use semantic color tokens (`bg-primary`, `text-muted-foreground`) — see `brief-design` skill
- Use spacing scale (p-4, m-2, gap-3) consistently
- Use semantic typography classes (`.title-1`, `.body`, `.callout`) — see `reference/typography.md`
- Don't create one-off font sizes, colors, or hardcode hex values

### Component Organization

**Note**: Brief has a Chrome extension. Components may be shared via `chat-ui/` package.

- `chat-ui/` - Shared components (web app + Chrome extension)
- `components/` - Web-specific components
- `chrome-extension/` - Extension-specific components

**Before creating a component**:
- Search existing components: `grep -r "ComponentName" .`
- Check if similar functionality exists in `chat-ui/` or `components/`
- Reuse or compose from existing components when possible

## File Organization

- API routes: app/api/v1/[resource]/route.ts
- Hooks: hooks/use-[resource].ts
- Shared components: chat-ui/ (web + extension)
- Web components: components/[feature]/[component].tsx
- Utilities: lib/[utility].ts
- Types: types/[domain].ts

## Documentation

- Update /docs when adding new API endpoints
- Update /docs when changing architecture
- Keep README.md in sync with setup instructions
