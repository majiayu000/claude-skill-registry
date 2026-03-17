---
name: justicehub-reviewer
description: Platform audit for JusticeHub pages, API routes, Supabase patterns, and Empathy Ledger integration.
---

# JusticeHub Platform Reviewer

## When to Use
- Audit pages/routes for data fetching issues
- Verify Supabase connection patterns
- Check Empathy Ledger integration
- Review API route security
- Generate platform health reports

## Invocation

```
/justicehub-review [scope]
```

| Scope | What It Checks |
|-------|----------------|
| `full` | Complete platform audit |
| `pages` | All Next.js pages |
| `api` | All API routes |
| `supabase` | Connection patterns |
| `empathy-ledger` | Integration health |
| `functions` | Utility services |

## Quick Patterns

### Correct Server Component
```typescript
import { createServiceClient } from '@/lib/supabase/service';
export const dynamic = 'force-dynamic';

export default async function Page() {
  const supabase = createServiceClient();
  const { data } = await supabase.from('table').select('*');
  return <Component data={data} />;
}
```

### Correct API Route
```typescript
import { createServiceClient } from '@/lib/supabase/service';
export async function GET() {
  const supabase = createServiceClient();
  const { data, error } = await supabase.from('table').select('*');
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data);
}
```

## Red Flags
- `createClient` in server component (should be `createServiceClient`)
- Missing `force-dynamic` for dynamic data
- Server cookie client without await
- No error handling in API routes

## File References

| Need | Reference |
|------|-----------|
| Page patterns | `references/page-patterns.md` |
| API patterns | `references/api-patterns.md` |
| Supabase patterns | `references/supabase-patterns.md` |
| Empathy Ledger | `references/empathy-ledger.md` |
