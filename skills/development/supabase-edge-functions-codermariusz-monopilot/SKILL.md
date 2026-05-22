---
name: supabase-edge-functions
description: Apply when building serverless functions in Supabase: webhooks, background jobs, third-party integrations, or complex server-side logic. Runs on Deno 2.1+.
version: 1.1.0
tokens: ~600
confidence: high
sources:
  - https://supabase.com/docs/guides/functions
  - https://supabase.com/docs/reference/javascript/functions-invoke
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [supabase, edge-functions, serverless, deno]
---

## When to Use

Apply when building serverless functions in Supabase: webhooks, background jobs, third-party integrations, or complex server-side logic. Runs on Deno 2.1+.

## Patterns

### Pattern 1: Basic Edge Function
```typescript
// Source: https://supabase.com/docs/guides/functions
// supabase/functions/hello/index.ts
// Note: Deno 2.1+ is now supported (Dec 2025)
import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';

serve(async (req) => {
  const { name } = await req.json();

  return new Response(
    JSON.stringify({ message: `Hello ${name}!` }),
    { headers: { 'Content-Type': 'application/json' } }
  );
});
```

### Pattern 2: With Supabase Client
```typescript
// Source: https://supabase.com/docs/guides/functions
import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')! // Full access
  );

  const { data, error } = await supabase
    .from('users')
    .select('*')
    .limit(10);

  return new Response(JSON.stringify({ data, error }), {
    headers: { 'Content-Type': 'application/json' },
  });
});
```

### Pattern 3: Invoke from Client
```typescript
// Source: https://supabase.com/docs/reference/javascript/functions-invoke
const { data, error } = await supabase.functions.invoke('hello', {
  body: { name: 'World' },
});

// With custom headers
const { data, error } = await supabase.functions.invoke('process', {
  body: { orderId: '123' },
  headers: { 'x-custom-header': 'value' },
});
```

### Pattern 4: Webhook Handler
```typescript
// Source: https://supabase.com/docs/guides/functions
// supabase/functions/stripe-webhook/index.ts
import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import Stripe from 'https://esm.sh/stripe@12.0.0?target=deno';

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
});

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')!;
  const body = await req.text();

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      Deno.env.get('STRIPE_WEBHOOK_SECRET')!
    );

    if (event.type === 'checkout.session.completed') {
      // Handle successful payment
    }

    return new Response(JSON.stringify({ received: true }), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 400 });
  }
});
```

### Pattern 5: CORS Headers
```typescript
// Source: https://supabase.com/docs/guides/functions
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  // ... handler logic

  return new Response(JSON.stringify(data), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
});
```

## Anti-Patterns

- **Secrets in code** - Use `Deno.env.get()` for secrets
- **No CORS for browser calls** - Add CORS headers
- **Long-running functions** - Edge functions timeout at 60s
- **No error handling** - Return proper error responses

## Verification Checklist

- [ ] Using Deno 2.1+ compatible imports
- [ ] Secrets stored in Supabase dashboard, not code
- [ ] CORS headers for browser invocations
- [ ] Error responses with appropriate status codes
- [ ] Function completes within 60s timeout
- [ ] Deployed with `supabase functions deploy`
