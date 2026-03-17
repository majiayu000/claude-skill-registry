---
name: supabase-patterns
description: Patterns for Supabase integration in Battery. Use this skill when working with database schemas, row-level security policies, edge functions, or Supabase client usage in Next.js.
---

# Supabase Patterns

## Database Schema Conventions

### Naming

- Tables: `snake_case`, plural (e.g., `organizations`, `deployed_apps`)
- Columns: `snake_case`
- Primary keys: `id` (UUID)
- Foreign keys: `{table_singular}_id`

### Standard Columns

Every table should include:

```sql
CREATE TABLE deployed_apps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- domain columns here
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Auto-update updated_at
CREATE TRIGGER update_deployed_apps_updated_at
  BEFORE UPDATE ON deployed_apps
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### Update Trigger Function

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## Row-Level Security (RLS)

### Enable RLS

```sql
ALTER TABLE deployed_apps ENABLE ROW LEVEL SECURITY;
```

### Organization-Based Access

Battery uses organizations for multi-tenancy:

```sql
-- Users can only see apps in their organization
CREATE POLICY "Users can view org apps"
  ON deployed_apps
  FOR SELECT
  USING (
    org_id IN (
      SELECT org_id FROM org_members WHERE user_id = auth.uid()
    )
  );

-- Only admins can delete apps
CREATE POLICY "Admins can delete org apps"
  ON deployed_apps
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM org_members
      WHERE user_id = auth.uid()
        AND org_id = deployed_apps.org_id
        AND role = 'admin'
    )
  );
```

### Service Role Bypass

For server-side operations that need to bypass RLS:

```typescript
import { createClient } from '@supabase/supabase-js'

// Use service role key (server-side only!)
const supabaseAdmin = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

// This bypasses RLS
await supabaseAdmin.from('deployed_apps').insert({ ... })
```

## Client Usage in Next.js

### Server Components

```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options)
          })
        },
      },
    }
  )
}
```

### Client Components

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### Route Handlers

```typescript
// app/api/apps/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()

  const { data, error } = await supabase
    .from('deployed_apps')
    .select('*')
    .order('created_at', { ascending: false })

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data)
}
```

## Edge Functions

### Structure

```
supabase/
  functions/
    deploy-webhook/
      index.ts
    scan-credentials/
      index.ts
```

### Basic Edge Function

```typescript
// supabase/functions/deploy-webhook/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  const { deployment_id, status } = await req.json()

  const { error } = await supabase
    .from('deployments')
    .update({ status })
    .eq('id', deployment_id)

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  return new Response(JSON.stringify({ success: true }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

## Type Generation

Generate TypeScript types from your schema:

```bash
pnpm supabase gen types typescript --project-id $PROJECT_ID > lib/database.types.ts
```

### Using Generated Types

```typescript
import { Database } from '@/lib/database.types'

type DeployedApp = Database['public']['Tables']['deployed_apps']['Row']
type InsertApp = Database['public']['Tables']['deployed_apps']['Insert']

// Typed client
const supabase = createClient<Database>(url, key)

const { data } = await supabase
  .from('deployed_apps')
  .select('id, name, status')
  .returns<Pick<DeployedApp, 'id' | 'name' | 'status'>[]>()
```

## Vault for Credentials

Battery stores extracted credentials in Supabase Vault:

```sql
-- Store a secret
SELECT vault.create_secret('snowflake_password', 'secret_value', 'Snowflake password for app X');

-- Retrieve a secret (in edge function or with service role)
SELECT vault.decrypted_secrets WHERE name = 'snowflake_password';
```

## Patterns to Follow

1. **Always enable RLS** on tables with user data
2. **Use server components** for initial data fetching
3. **Type everything** with generated types
4. **Use transactions** for multi-table operations
5. **Service role** only on server, never expose to client
