---
name: supabase-functions
description: Supabase Edge Functions development and deployment using Deno runtime. Use when creating serverless functions, webhooks, API endpoints, or scheduled tasks.
---

# Supabase Edge Functions Skill

Serverless functions with Deno runtime.

## Quick Reference

| Task | Command |
|------|---------|
| Create function | `supabase functions new <name>` |
| Serve locally | `supabase functions serve` |
| Deploy | `supabase functions deploy <name>` |
| Delete | `supabase functions delete <name>` |
| Set secrets | `supabase secrets set KEY=value` |
| List secrets | `supabase secrets list` |

## Create Function

```bash
supabase functions new hello-world
```

Creates: `supabase/functions/hello-world/index.ts`

## Basic Function Structure

```typescript
// supabase/functions/hello-world/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts"

Deno.serve(async (req: Request) => {
  const { name } = await req.json()

  return new Response(
    JSON.stringify({ message: `Hello ${name}!` }),
    { headers: { "Content-Type": "application/json" } }
  )
})
```

## Local Development

### Serve All Functions

```bash
supabase functions serve
```

### Serve with Environment Variables

```bash
supabase functions serve --env-file .env
```

### Serve without JWT Verification

```bash
supabase functions serve --no-verify-jwt
```

### Test Function

```bash
curl -i --request POST \
  'http://localhost:54321/functions/v1/hello-world' \
  --header 'Authorization: Bearer <ANON_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{"name":"World"}'
```

## CORS Handling

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

Deno.serve(async (req: Request) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { name } = await req.json()

    return new Response(
      JSON.stringify({ message: `Hello ${name}!` }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
    )
  }
})
```

## Using Supabase Client

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from 'jsr:@supabase/supabase-js@2'

Deno.serve(async (req: Request) => {
  // Create Supabase client with service role
  const supabaseAdmin = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  // Or with user's JWT (respects RLS)
  const authHeader = req.headers.get('Authorization')!
  const supabaseClient = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    { global: { headers: { Authorization: authHeader } } }
  )

  // Query with user context
  const { data, error } = await supabaseClient
    .from('posts')
    .select('*')

  return new Response(
    JSON.stringify({ data, error }),
    { headers: { 'Content-Type': 'application/json' } }
  )
})
```

## Get User from JWT

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from 'jsr:@supabase/supabase-js@2'

Deno.serve(async (req: Request) => {
  const supabaseClient = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  )

  const { data: { user }, error } = await supabaseClient.auth.getUser()

  if (error || !user) {
    return new Response(
      JSON.stringify({ error: 'Unauthorized' }),
      { status: 401, headers: { 'Content-Type': 'application/json' } }
    )
  }

  return new Response(
    JSON.stringify({ userId: user.id, email: user.email }),
    { headers: { 'Content-Type': 'application/json' } }
  )
})
```

## Environment Variables & Secrets

### Set Secrets

```bash
# Single secret
supabase secrets set API_KEY=abc123

# Multiple secrets
supabase secrets set API_KEY=abc123 DB_PASSWORD=secret

# From file
supabase secrets set --env-file .env
```

### Access in Function

```typescript
const apiKey = Deno.env.get('API_KEY')
const supabaseUrl = Deno.env.get('SUPABASE_URL')
const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
```

### Built-in Variables

- `SUPABASE_URL` - Project URL
- `SUPABASE_ANON_KEY` - Anon key
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key
- `SUPABASE_DB_URL` - Direct database connection

## Deploy Function

### Deploy Single Function

```bash
supabase functions deploy hello-world
```

### Deploy without JWT Verification

```bash
supabase functions deploy webhook-handler --no-verify-jwt
```

### Deploy All Functions

```bash
supabase functions deploy
```

## Invoke from JavaScript

```javascript
const { data, error } = await supabase.functions.invoke('hello-world', {
  body: { name: 'World' }
})
```

### With Custom Headers

```javascript
const { data, error } = await supabase.functions.invoke('api-handler', {
  body: { action: 'create' },
  headers: { 'x-custom-header': 'value' }
})
```

## Webhook Function

```typescript
// supabase/functions/stripe-webhook/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import Stripe from 'npm:stripe@14'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16'
})

const cryptoProvider = Stripe.createSubtleCryptoProvider()

Deno.serve(async (req: Request) => {
  const signature = req.headers.get('Stripe-Signature')!
  const body = await req.text()

  let event: Stripe.Event

  try {
    event = await stripe.webhooks.constructEventAsync(
      body,
      signature,
      Deno.env.get('STRIPE_WEBHOOK_SECRET')!,
      undefined,
      cryptoProvider
    )
  } catch (err) {
    return new Response(
      JSON.stringify({ error: `Webhook Error: ${err.message}` }),
      { status: 400 }
    )
  }

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object
      // Handle successful checkout
      break
    default:
      console.log(`Unhandled event type ${event.type}`)
  }

  return new Response(JSON.stringify({ received: true }))
})
```

## Database Webhook

Trigger function on database changes:

```sql
-- Create webhook trigger
CREATE OR REPLACE FUNCTION notify_function()
RETURNS trigger AS $$
BEGIN
  PERFORM net.http_post(
    url := 'https://<project>.supabase.co/functions/v1/handle-insert',
    headers := '{"Authorization": "Bearer <SERVICE_KEY>"}'::jsonb,
    body := row_to_json(NEW)::text
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_insert
  AFTER INSERT ON posts
  FOR EACH ROW
  EXECUTE FUNCTION notify_function();
```

## Scheduled Functions (Cron)

```sql
-- Using pg_cron extension
SELECT cron.schedule(
  'daily-cleanup',
  '0 0 * * *',  -- Every day at midnight
  $$
  SELECT net.http_post(
    url := 'https://<project>.supabase.co/functions/v1/cleanup',
    headers := '{"Authorization": "Bearer <SERVICE_KEY>"}'::jsonb
  )
  $$
);
```

## Configuration (config.toml)

```toml
[functions.hello-world]
verify_jwt = true

[functions.webhook-handler]
verify_jwt = false

[functions.api-handler]
verify_jwt = true
import_map = "./supabase/functions/import_map.json"
```

## Shared Code

Create `_shared` folder for reusable code:

```
supabase/functions/
├── _shared/
│   ├── cors.ts
│   └── supabase.ts
├── hello-world/
│   └── index.ts
└── api-handler/
    └── index.ts
```

```typescript
// _shared/cors.ts
export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// _shared/supabase.ts
import { createClient } from 'jsr:@supabase/supabase-js@2'

export const supabaseAdmin = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)
```

```typescript
// hello-world/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { corsHeaders } from '../_shared/cors.ts'
import { supabaseAdmin } from '../_shared/supabase.ts'

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  // Use shared client
  const { data } = await supabaseAdmin.from('posts').select('*')

  return new Response(
    JSON.stringify({ data }),
    { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
  )
})
```

## Limits

| Limit | Value |
|-------|-------|
| CPU Time | 2 seconds |
| Request Timeout | 150 seconds |
| Wall Clock (Pro) | 400 seconds |
| Bundle Size | 20 MB |

## References

- [function-patterns.md](references/function-patterns.md) - Common patterns
- [deno-imports.md](references/deno-imports.md) - Import syntax
